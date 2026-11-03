---
title: "Android Through a Flutter Developer's Eyes (1) suspend Doesn't Block the Thread"
description: "A reference point for understanding Kotlin coroutines if you know Dart's async/await: suspend, launch and async, structured concurrency, and Dispatchers"
date: 2026-06-30 21:00:00 +0900
categories: [android, coroutine]
tags: [Kotlin, Coroutine, Dart, Flutter, Structured Concurrency]
series: "Android Through a Flutter Developer's Eyes"
series_order: 1
toc: true
---

When I opened Android code again after three years of Flutter, coroutines didn't feel foreign.
`suspend` is `async`, calling a function is `await`, `Deferred` is `Future`.
It seemed like memorizing a mapping table would be enough.

Once I actually used them, it wasn't.
The syntax looks alike, but **the execution model was different.**
A Dart Future runs only on the event loop of a single Isolate, which means a single thread.
A Kotlin coroutine moves between threads depending on its Dispatcher.
If you line up things at the same level, a Future maps to a coroutine and an Isolate maps to a thread. The difference is that Isolates don't share memory, while threads do.
Read only through the mapping table, without this difference in mind, and you end up writing code that blocks the main thread while believing it is "asynchronous."

This series is a record of looking at Android again through a Flutter developer's eyes.
Part 1 starts where coroutines start: `suspend`.

## Does suspend block the thread?

The short answer: **`suspend` pauses the coroutine and releases the thread.**

```kotlin
Thread.sleep(1000)  // blocks the thread. On main, the screen freezes
delay(1000)         // suspends only the coroutine. The thread does other work
```

When `delay` is called, the compiler-generated Continuation stores "where to stop and how to resume," and the thread is released.
One second later, the coroutine resumes from that point.
The points where it can pause (suspension points) are `delay`, `await`, `withContext`, and calls to other suspend functions.

There is one point worth noting here.
**Adding `suspend` does not change the thread.**
Until the first suspension point, the function runs on whichever thread called it.
This is the same as a Dart `async` function running synchronously until its first `await`.

```kotlin
suspend fun parseAll(raw: List<String>): List<Article> {
    // no suspension point → called from main, it blocks main
    return raw.map { heavyParse(it) }
}
```

| Code | Thread | Used on main |
|---|---|---|
| `Thread.sleep` | Blocked | Screen freezes |
| `delay` | Released | Doesn't freeze |
| Heavy loop inside a suspend function | Blocked | Screen freezes |

In Dart, heavy computation goes to `Isolate.run` (or `compute`).
In Kotlin, `withContext` sends it to another Dispatcher.

```kotlin
suspend fun parseAll(raw: List<String>): List<Article> =
    withContext(Dispatchers.Default) {
        raw.map { heavyParse(it) }
    }
```

### Mapping to Dart

| Dart | Kotlin |
|---|---|
| `async` keyword | `suspend` |
| `await` | Just call the suspend function |
| `Future<T>` | `Deferred<T>` |
| Calling without `await` | `async { }` |
| Isolate (no shared memory) | Thread (shared memory) |

The last row matters most.
Dart Isolates don't share memory, so concurrent modification is ruled out by design.
Kotlin threads share memory, so when several coroutines change the same state, you have to handle it yourself.
That is why you use `MutableStateFlow.update { }`. It retries compare-and-set, so no change gets lost even when updates happen at the same time. StateFlow is covered in detail in part 3.

## launch and async

- **`launch`**: starts work without a result and returns a `Job`. You use the `Job` to cancel it or wait for it to finish (`join`).
- **`async`**: starts work with a result and returns a `Deferred<T>`. You get the value with `.await()`. `Deferred` is a kind of `Job`, and it is the equivalent of Dart's `Future`.

Calling two one-second requests in sequence takes two seconds; starting them together with two `async` calls and awaiting both takes a little over one second.

```kotlin
coroutineScope {
    val article = async { repository.getArticle(id) }
    val comments = async { repository.getComments(id) }
    show(article.await(), comments.await())
}
```

It is the same picture as Dart's `Future.wait([...])`.

`withContext` is not a new coroutine.
The current coroutine moves to another thread, does the work, and comes back with the result.
So it runs in order.

### Holding the Job lets you drop late responses

The `Job` that `launch` returns is more useful than it looks.
Refreshing a list is a typical case.

```kotlin
private var loadJob: Job? = null

fun refresh() {
    loadJob?.cancel()   // cancel the in-flight request first
    loadJob = viewModelScope.launch {
        val articles = repository.getArticles(page = 1)
        _uiState.update { it.copy(articles = articles) }
    }
}
```

Without canceling the previous `Job`, an old response that arrives late can overwrite the new result.
In Dart, the code that carries a request number around to check "am I the latest request?" becomes a single `cancel()` call here.

## Structured concurrency: why there is no mounted check

One of the most common pieces of defensive code in Flutter is this.

```dart
final articles = await repository.getArticles();
if (!mounted) return;   // skip setState if the widget is gone
setState(() => _articles = articles);
```

Kotlin has no such check.
That is because coroutines run **inside a Scope tied to the screen's lifetime.**

A Scope holds two things.
A `Job` that defines its lifetime, and a default Dispatcher.
Coroutines launched in a Scope are its children, and there are three rules between parent and child.

- When the parent is canceled, all children are canceled.
- The parent doesn't finish until all its children finish.
- When a child fails, the failure is passed to the parent (covered in part 2).

This is **structured concurrency.**
It is the rule that keeps coroutines from floating around unattached.

When you close the screen, the ViewModel is cleared, `viewModelScope` is canceled, and every request launched under it is canceled too.
A running coroutine stops with `CancellationException` at its next suspension point, and the `_uiState.update` below it never runs.
There is simply nothing left for a `mounted` check to guard.

| Scope | Lifetime | Default Dispatcher |
|---|---|---|
| `viewModelScope` | Until the ViewModel is cleared. Survives rotation | `Main.immediate` |
| `lifecycleScope` | Until the Activity or Fragment hits `onDestroy`. Canceled on rotation | `Main.immediate` |
| `rememberCoroutineScope()` | Until the Composable leaves the composition | Main |
| `coroutineScope { }` | Until all children in the block finish | Same as the caller |
| `GlobalScope` | The whole app. No parent | `Default` |

`lifecycleScope` is not canceled at `onStop`.
To stop work while the screen isn't visible, use `repeatOnLifecycle(STARTED)`.

### Why not GlobalScope

`GlobalScope` has no parent, so it sits outside the rules above.

- It isn't canceled automatically when the screen goes away. If it holds on to the screen, that's a memory leak.
- There is no parent to report failures to. Without a handler, the app crashes.
- It is hard-coded, so tests can't swap it out.

Work that must outlive the screen (sending logs, for example) gets an app-lifetime Scope, **injected.**

```kotlin
@Qualifier
@Retention(AnnotationRetention.BINARY)
annotation class ApplicationScope

@Module
@InstallIn(SingletonComponent::class)
object ScopeModule {
    @Provides @Singleton @ApplicationScope
    fun provideAppScope(): CoroutineScope =
        CoroutineScope(SupervisorJob() + Dispatchers.Default)
}
```

Work that must finish even if the app process dies goes to WorkManager.
Coroutines disappear along with the process.

Just as Flutter hands dependencies down from above through `context`, Kotlin receives its Scope from above instead of pulling it from a global.
Both ecosystems share the same philosophy: who owns the lifetime should be visible in the code.

## Dispatchers and main-safety

| Dispatcher | Threads | Used for |
|---|---|---|
| `Main` | The single main thread | UI updates |
| `Main.immediate` | Main. If already on main, runs right away without queuing | Default for `viewModelScope` and `lifecycleScope` |
| `Default` | As many as CPU cores | Computation such as sorting and parsing |
| `IO` | Up to 64 (or the number of cores, whichever is larger) | Blocking I/O (files, blocking APIs) |

Despite its name, `Default` is not main; it is **a pool of threads for computation.**

**main-safe** describes a function that is safe to call from the main thread.
The function itself moves heavy work to another Dispatcher.

- Room's suspend DAO functions and Flow-returning functions run their queries on Room's own threads.
- Retrofit's suspend functions and Apollo's `execute()` also move networking to other threads internally.

So there is no need to wrap Repositories around these libraries in `withContext(Dispatchers.IO)` out of habit.
Where `withContext` is needed is computation you wrote **yourself** (`Default`) and calls to blocking APIs (`IO`).
And the responsibility for moving it belongs **inside that function**, not with the caller.

## Summary

- `suspend` pauses the coroutine and releases the thread. But it doesn't change the thread.
- Where Dart uses `Isolate.run` for heavy computation, Kotlin uses `withContext(Dispatchers.Default)`.
- `launch` returns a `Job`, `async` returns a `Deferred`. Holding the `Job` lets you drop late responses by canceling.
- Structured concurrency removes the need for a `mounted` check. Inject a Scope instead of using `GlobalScope`.
- `Dispatchers.Default` is not main.

The syntax carries over through a mapping table, but the execution model doesn't.
Next time: how exceptions and cancellation flow on top of this structure, and why `runCatching` is dangerous inside a coroutine.
