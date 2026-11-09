---
title: "Android Through a Flutter Developer's Eyes (3) Flow Is Not a Stream"
description: "Cold and Hot, stateIn and shareIn, collectAsStateWithLifecycle, the properties of StateFlow, one-off events, and flow versus channelFlow"
date: 2026-07-14 21:20:00 +0900
categories: [android, coroutine]
tags: [Kotlin, Flow, StateFlow, Dart, Stream]
series: "Android Through a Flutter Developer's Eyes"
series_order: 3
---

When you first see `Flow`, Dart's `Stream` comes to mind.
`flow { emit(x) }` is `async* { yield x }`, and `collect` is `listen`.
On a mapping table, that is how it looks.

In practice it feels different.
`collect` is not a callback registration but **a suspend function that stops on that line**, and unsubscribing is not `cancel()` but **coroutine cancellation**.
And if you don't tell Cold from Hot, the same DB query runs once per subscriber.

> Part 3 starts from the difference between Cold and Hot, then follows the path from turning a Cold Flow into a `StateFlow` to reading it on screen.
> On top of that, it covers how to send one-off events and the tools for building and combining Flows (`channelFlow`, `combine`, `flatMapLatest`).

## Mapping to Dart

| Kotlin | Dart |
|---|---|
| `suspend fun` | `Future` + `async`/`await` |
| `flow { emit(x) }` | `async*` + `yield x` |
| `channelFlow { launch { send(x) } }` | Several tasks calling `StreamController.add(x)`, with closing and cancellation handled for you |
| `StateFlow` | rxdart `BehaviorSubject` |
| `SharedFlow` | `StreamController.broadcast()` |
| `collect { }` | `listen()`, except it suspends on that line and you stop it by cancelling the coroutine |

The fact that `collect` suspends matters more than you might expect.

```kotlin
viewModelScope.launch {
    repository.observeArticles().collect { render(it) }
    println("This runs only after the Flow completes")
}
```

In Dart, the line after `listen` runs right away.
In Kotlin, the line after `collect` doesn't run until the Flow completes.
If the Flow never completes (watching a DB, for example), it never runs.
To collect two Flows at once, you `launch` twice.

## Cold and Hot

- **Cold**: It starts only when someone calls `collect`. Each subscriber gets its own run from the beginning. `flow { }` and Room DAOs that return a Flow work this way.
- **Hot**: It has values even with no subscribers, and subscribers share the same stream. `StateFlow` and `SharedFlow` work this way.

Cold is food cooked to order; Hot is a radio that is already playing.

Dart's single-subscription `Stream` is close to Cold, and a broadcast `Stream` is close to Hot.
But in Dart, listening to a single-subscription Stream twice throws.
A Kotlin Cold Flow collected twice **quietly runs twice**.

```kotlin
val articles = articleDao.observeAll()   // Cold

launch { articles.collect { renderList(it) } }    // query 1
launch { articles.collect { updateBadge(it) } }   // query 2
```

When several places need the same data, you make it Hot and share one stream.
The functions that turn a Cold Flow into a Hot one are `stateIn` and `shareIn`.

## Making It Hot: stateIn and shareIn

| | `stateIn` → `StateFlow` | `shareIn` → `SharedFlow` |
|---|---|---|
| Initial value | Required | Not needed |
| Current value | `.value` | `replayCache` (when replay is set) |
| New subscriber | Gets the current value | Gets `replay` values, none if 0 |
| Same value twice | Ignored | Emitted as is |

When to start and stop is decided by `SharingStarted`.

| `SharingStarted` | Behavior |
|---|---|
| `Eagerly` | Starts immediately, runs until the scope ends |
| `Lazily` | Starts with the first subscriber, keeps running after that |
| `WhileSubscribed(5_000)` | Runs only while there are subscribers, stops 5 seconds after the last one leaves |

```kotlin
val uiState: StateFlow<ArticleListUiState> = observeArticles()
    .map { it.toUiState() }
    .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), ArticleListUiState())
```

The 5 seconds are a margin so the upstream doesn't restart when the subscription drops for a moment, as during a screen rotation.

Here the subscriber is the screen.
When the screen starts and stops subscribing is decided by the function the screen uses.

## Reading It on Screen: collectAsStateWithLifecycle

This function reads a Flow as a `State` in Compose.

- `collectAsState()` keeps collecting even when the screen goes to the background.
- `collectAsStateWithLifecycle()` collects only while the lifecycle is at least `STARTED` by default. When the screen is no longer visible (`onStop`) it stops, and when it becomes visible again it resumes.

```kotlin
@Composable
fun ArticleListRoute(viewModel: ArticleListViewModel = hiltViewModel()) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    ArticleListScreen(state = state, onRefresh = viewModel::onRefresh)
}
```

It pairs with the `WhileSubscribed(5_000)` above.
When the screen is not visible, the collecting coroutine is cancelled, and 5 seconds later the upstream (DB watching, location updates) stops as well.
This is what "unsubscribing is coroutine cancellation" from the introduction looks like.
It is similar to `StreamBuilder` in Flutter dropping its subscription when it leaves the widget tree, but here the subscription stops **even while the screen is still in the tree, as long as it isn't visible**.

Outside Compose (in an Activity), `repeatOnLifecycle(Lifecycle.State.STARTED) { flow.collect { } }` plays the same role.

## Where stateIn Belongs

The default is the ViewModel.
A Hot Flow needs a scope that decides how long it lives, and that is `viewModelScope`.
Repositories and UseCases return Cold Flows by default.

Only when several screens need to share the same data does the Repository `shareIn` it in an app-lifetime scope (the `@ApplicationScope` from part 1).

`stateIn` requires an initial value, so the screen needs something to show even before the first value is read from the DB.
If you use an empty list as that initial value, an empty "No items" screen flashes briefly even though there is data.
In that case, use `shareIn(replay = 1)` instead of `stateIn`, or make the initial value a `Loading` state.

## Properties of StateFlow

Whatever `stateIn` produces and the `MutableStateFlow` a ViewModel holds directly are both `StateFlow`s.
`StateFlow` is the basic container for screen state.
Knowing four of its properties heads off most problems.

1. **It always holds one value.** An initial value is required, and a new subscriber gets the current value right away.
2. **It doesn't emit the same value again.** It compares with `equals`, which is why state is kept in a `data class`.
3. **When it changes many times quickly, it skips intermediate values (conflation).** That suits state, where only the latest value matters, but not sending events one value at a time.
4. **If another coroutine gets in between a read and a write, it overwrites.** That is why you use `update { }`.

```kotlin
private val _uiState = MutableStateFlow(ArticleListUiState())
val uiState: StateFlow<ArticleListUiState> = _uiState.asStateFlow()

fun onRefreshDone() {
    // ❌ _uiState.value = _uiState.value.copy(refreshing = false)
    _uiState.update { it.copy(refreshing = false) }
}
```

The commented-out line has three steps: read, modify, write.
When two coroutines go through those three steps at the same time, you get a race condition.

1. A reads the state with `refreshing = true`.
2. B reads the same state.
3. A writes it back with `refreshing = false`.
4. B changes a different field on the old state it read and writes that. A's `refreshing = false` is overwritten and lost.

`update` reads the value, and if another coroutine changed it in the meantime, recalculates from the latest value.
So even when two coroutines change it at once, neither change is overwritten and lost.
Because the block can run more than once, it should only compute the new value.

This doesn't mean the screen receives every intermediate value.
Emission still follows property 3 and keeps only the latest value.
`update` is a safeguard on the writing side and works separately from what the screen receives.

This problem is a consequence of "threads share memory" from part 1.

Flutter's `ValueNotifier` also stays silent for the same value.
Property 2 is familiar; properties 3 and 4 are the new parts.

## One-off Events as State Too

How to send one-off events such as snackbars or navigation is a perennial debate.

| Approach | Problem |
|---|---|
| `Channel` | If the screen doesn't receive it at that moment, it piles up and shows at the wrong time, or is lost if the screen goes away before handling it |
| `SharedFlow(replay = 0)` | Sent with no subscriber, it disappears |
| Put it in UiState and clear it after handling | You have to call a separate clear function, so there is a bit more code |

Google's official guide recommends the last approach.
The gist is "express UI actions that start in the ViewModel as state updates."

```kotlin
data class ArticleListUiState(
    val articles: ImmutableList<ArticleUiModel> = persistentListOf(),
    val messages: ImmutableList<UiMessage> = persistentListOf(),
)

fun onMessageShown(id: Long) {
    _uiState.update { s -> s.copy(messages = s.messages.filterNot { it.id == id }.toPersistentList()) }
}
```

Earlier we saw that StateFlow doesn't suit sending events one value at a time (property 3).
Here the messages are not sent one by one but accumulated in a list.
Even if intermediate values are skipped, the latest list still holds the messages not yet handled, so the screen misses none of them.

Each message gets an `id` because of StateFlow's property 2.
It keeps two messages with the same text from collapsing into one.

## flow and channelFlow

| | `flow { }` | `channelFlow { }` |
|---|---|---|
| Emitting | `emit` | `send` |
| `launch` inside | Emitting from another coroutine throws | `send` from several `launch`es at once is allowed |
| Completes when | The block finishes | The block and every coroutine inside it finish |

Both are Cold.
Calling `launch { emit(x) }` inside `flow { }` throws `IllegalStateException: Flow invariant is violated`.
That is because `flow` promises to emit in order from a single coroutine.

When you need to run several things at once, such as DB watching, refresh signals and per-item extra requests, and emit them as one stream, you use `channelFlow`.

## combine and flatMapLatest

- **`combine(a, b)`**: Whenever either emits a new value, it combines the latest value of each and emits. Screen state usually uses this.
- **`zip(a, b)`**: Pairs the 1st with the 1st, the 2nd with the 2nd, and so on. If one side is slow, it waits.
- **`flatMapLatest`**: Each time the outer value changes, it switches to a new inner Flow and cancels the previous one.

```kotlin
query
    .debounce(300)
    .flatMapLatest { text -> repository.search(text) }  // a new query cancels the previous search
```

What part 1 did by holding a `Job` and cancelling the previous request, a single operator now does.

## Summary

- `collect` is a suspend function that stops on that line. You stop it by cancelling the coroutine.
- A Cold Flow runs separately for each subscriber. To share it, make it Hot with `stateIn` or `shareIn`.
- Read it on screen with `collectAsStateWithLifecycle()`. Together with `WhileSubscribed`, it also stops the upstream of a screen that isn't visible.
- `StateFlow` ignores the same value and skips intermediate values. Change values with `update { }`.
- Accumulate one-off events in a list in the state, and clear them after handling.
- To emit from several coroutines, use `channelFlow`.

Next time we move on to Compose, which takes this state and draws it.
Flutter's rebuild and Compose's recomposition look alike, but what they skip is different.
