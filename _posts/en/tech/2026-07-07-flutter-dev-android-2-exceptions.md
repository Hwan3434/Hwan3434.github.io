---
title: "Android Through a Flutter Developer's Eyes (2) Coroutine Exceptions and Cancellation"
description: "Which way failure and cancellation flow, SupervisorJob, CoroutineExceptionHandler, not swallowing cancellation, cooperative cancellation, and the rule of keeping try/catch out of the ViewModel"
date: 2026-07-07 21:00:00 +0900
categories: [android, coroutine]
tags: [Kotlin, Coroutine, Exception Handling, Cancellation, SupervisorJob]
series: "Android Through a Flutter Developer's Eyes"
series_order: 2
toc: true
---

Exceptions from a Dart `Future` are simple.
They surface where you `await` and you catch them with `try/catch`.
If nobody catches them, they bubble up to the Zone and get logged, and the app usually keeps running.

Kotlin coroutines are different.
Following the parent-child relationship from part 1, **exceptions travel up and cancellation travels down.**
And on Android, an exception that nobody handles kills the app.

Part 2 looks at how exceptions and cancellation flow on top of that structure, and, given that flow, where exception handling should live.

## Failure goes up, cancellation goes down

Under a regular `Job`, when one child fails with an exception, it reports the failure to its parent.
The parent cancels all its other children, fails with the same exception itself, and reports further up.
If an exception that reached the top is handled by nobody, the app crashes.

This behavior fits work that "only makes sense together."
If you load an article body and its comments to build one screen, continuing to fetch comments after the body failed is wasted work.

Cancellation flows the other way.
When a parent is canceled, all its children are canceled, but a canceled child does not notify its parent.
The reason for the opposite direction becomes clear with code like `loadMoreJob?.cancel()`.
If cancellation also traveled up, turning off a single next-page request would stop its siblings and its parent too.
You couldn't switch off just one piece.

A `Job` tells failure and cancellation apart by one thing: the exception's type.
If a coroutine ends with `CancellationException`, it counts as "canceled"; any other exception counts as "failed."
The `TimeoutCancellationException` thrown by `withTimeout` is a subclass, so it is treated as cancellation.

## SupervisorJob and viewModelScope

A `SupervisorJob` does not propagate a child's failure to its parent.
Even if one child fails, its siblings keep running.

`viewModelScope` is built from `SupervisorJob + Dispatchers.Main.immediate`.
That's because loading the list should continue even if saving a bookmark fails.

What `SupervisorJob` does stops at keeping siblings alive, though.
The exception from the failed `launch` is still unhandled, and on Android the app still crashes.

Passing a `SupervisorJob` directly behaves differently from what you'd expect.

```kotlin
viewModelScope.launch(SupervisorJob()) { ... }
```

The newly created `SupervisorJob` becomes this coroutine's parent, cutting its link to `viewModelScope`.
So this coroutine isn't canceled when you leave the screen.
To let coroutines in a group fail independently of each other, use `supervisorScope { }`.

## Catch exceptions inside the coroutine

Wrapping `launch` in `try/catch` does not catch exceptions thrown inside it.
`launch` returns as soon as it starts the coroutine, and the exception is thrown later, inside that coroutine.
To catch it, the `try/catch` has to be inside the coroutine.

```kotlin
// A try/catch outside launch can't catch exceptions inside the coroutine
try {
    viewModelScope.launch { throw IOException() }
} catch (e: Exception) { }

// Catch inside the coroutine
viewModelScope.launch {
    try { load() } catch (e: IOException) { showError() }
}
```

`launch` and `async` also differ in when an exception surfaces.
`launch` reports to its parent the moment it fails.
`async` holds the exception in its `Deferred` and throws it when you call `await()`.
That matches how a Dart `Future` throws where you `await` it.

One condition applies here.
An `async` under a regular `Job` cancels its parent the moment it fails, even before anyone calls `await()`.
From the parent's point of view, one of its children has failed.
So regardless of the `try/catch` around `await()` receiving the exception, the siblings are already canceled.

## The last safety net: CoroutineExceptionHandler

`CoroutineExceptionHandler` is where you can intercept an exception that has reached the top before it kills the app.

```kotlin
private val handler = CoroutineExceptionHandler { _, throwable ->
    logger.report(throwable)
    _uiState.update { it.copy(error = true) }
}

fun bookmark(id: Long) {
    viewModelScope.launch(handler) {
        repository.bookmark(id)
    }
}
```

The handler is where an exception nobody handled finally arrives.
You can log it or show an error state there, but you can't bring the coroutine back.
By the time the handler runs, that coroutine has already finished as failed.

Where the handler takes effect is fixed.

- **It works only on a root `launch`.** A handler is called when it is on a `launch` started directly under a scope, or in the scope's own context. A handler attached to a child coroutine is ignored, because a child's exception goes up to its parent without looking at the handler.
- **It has no effect on `async`.** `async` hands its exception to whoever calls `await()` through the `Deferred`, so the exception isn't treated as unhandled.
- **A direct child of a `SupervisorJob` is treated like a root.** That's why `viewModelScope.launch(handler)` works.

Its role is similar to collecting unhandled errors in Dart with `runZonedGuarded` or `PlatformDispatcher.instance.onError`.
The difference is that its scope is not the whole app but the one root coroutine you attach it to.

## Don't swallow cancellation

Because cancellation is delivered as an exception, `CancellationException`, it causes a problem.
Catching `Exception` broadly catches cancellation too.

```kotlin
viewModelScope.launch {
    try {
        repository.load()
    } catch (e: Exception) {
        showError()     // the cancellation from leaving the screen is caught here too
    }
    doNext()            // the canceled coroutine keeps going
}
```

A coroutine canceled because you left the screen creates an error state and then carries on with the next task.
So wherever you catch `Exception` broadly, rethrow cancellation first.

```kotlin
try {
    Result.Success(api.fetchArticles())
} catch (e: CancellationException) {
    throw e
} catch (e: Exception) {
    Result.Failure(e)
}
```

`runCatching` from the Kotlin standard library has the same problem.
It's the first function that comes to mind when you want Dart's `try/catch` in one line, but internally it catches every `Throwable`.
Used in a suspend function, it turns `CancellationException` into `Result.failure`, and the same thing as in the example above happens.
`Error`s such as `OutOfMemoryError` are caught as well.
So in suspend functions, instead of `runCatching`, let cancellation through with `try/catch` as above, or write a separate function that does the same.

```kotlin
suspend inline fun <R> suspendRunCatching(block: () -> R): Result<R> =
    try { Result.success(block()) }
    catch (e: CancellationException) { throw e }
    catch (e: Exception) { Result.failure(e) }
```

## Cancellation is cooperative

`job.cancel()` only marks the coroutine as "canceled"; it can't forcibly stop the running thread.
The coroutine checks that mark at its next suspension point (`delay`, `emit`, a Room or Retrofit suspend call) and stops by throwing `CancellationException`.

A loop that only computes has no suspension points.
So even after cancellation, it runs until the loop finishes.
In places like this, add a point where you check for yourself.

```kotlin
withContext(Dispatchers.Default) {
    for (image in images) {
        ensureActive()          // throws CancellationException here if canceled
        makeThumbnail(image)
    }
}
```

`ensureActive()` is the most common choice.
If you have cleanup to do before stopping, just check the state with `isActive`, and if you need to briefly hand the turn to other coroutines, use `yield()`.
Inside an ordinary suspend function, call `currentCoroutineContext().ensureActive()`.
If you need to clean up with a suspend function in `finally` after cancellation, wrap it in `withContext(NonCancellable) { }`.

## No exception handling in the ViewModel

If you remember all these rules every time and write `try/catch` on every screen, missing a single spot means swallowing cancellation or crashing the app.
So I gather the places where exceptions become values in the data layer, and keep `try/catch` out of the ViewModel.

> The lower layers turn every failure that can happen in production into `Result.Failure` before passing it up.
> If they don't, fix the lower layer, not the ViewModel.

The places where exceptions become values come down to a few: network responses (connection failures, HTTP errors, parsing failures), DB writes, and the `catch` operator on Flows that observe the DB.
All of them rethrow `CancellationException`.
The ViewModel just splits the returned value with `when` and updates its state.

```kotlin
sealed interface Result<out T> {
    data class Success<T>(val value: T) : Result<T>
    data class Failure(val error: Exception) : Result<Nothing>
}

fun refresh() {
    viewModelScope.launch {
        when (val result = repository.getArticles(page = 1)) {
            is Result.Success -> _uiState.update { it.copy(articles = result.value) }
            is Result.Failure -> _uiState.update { it.copy(error = true) }
        }
    }
}
```

This is the Result pattern: return failure as a value instead of throwing it as an exception.
You can use the same pattern as-is in Flutter.
There is one difference.
In Kotlin, at the very spot where you turn exceptions into values, cancellation alone must not become a value; it has to be rethrown.

### What this rule doesn't cover

`OutOfMemoryError` is an `Error`, not an `Exception`, so it isn't caught.
Checks that catch programmer mistakes aren't turned into values either.
`require(condition)` throws `IllegalArgumentException` for a bad argument, and `check(condition)` and `error("message")` throw `IllegalStateException` for a bad state or a branch that should be impossible.
Bugs like these get fixed when they surface early by crashing, not when they are hidden behind a value.
Unlike Dart's `assert`, these functions also run in release builds.

## Summary

- Failure flows up, cancellation flows down. The only thing that separates them is whether the exception is a `CancellationException`.
- `SupervisorJob` only keeps siblings alive; it doesn't handle the exception for you.
- Catch exceptions inside the coroutine. An `async` exception surfaces at `await()`, but under a regular `Job` it cancels the siblings before that.
- `CoroutineExceptionHandler` is the last safety net for a root `launch`. It has no effect on children or on `async`.
- Catching `Exception` broadly or using `runCatching` swallows cancellation too. Rethrow cancellation.
- Cancellation is checked only at suspension points. Put `ensureActive()` in computation loops.
- Gather the places where exceptions become values in the data layer, and the ViewModel needs no `try/catch`. This is the Result pattern of returning failure as a value.

Next time we look at `Flow`, which sits where Dart's `Stream` does.
The names are similar, but if you don't tell Cold from Hot, the same query runs twice.
