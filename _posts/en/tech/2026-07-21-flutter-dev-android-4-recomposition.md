---
title: "Android Through a Flutter Developer's Eyes (4) Recomposition and Rebuild"
description: "Compose's three phases, stability and Strong Skipping, deferring state reads, derivedStateOf and snapshotFlow, Lazy keys, and effects, compared with Flutter's rebuild"
date: 2026-07-21 21:20:00 +0900
categories: [android, compose]
tags: [Jetpack Compose, Recomposition, Flutter, Performance, State Management]
series: "Android Through a Flutter Developer's Eyes"
series_order: 4
---

When you first see Compose, it looks so much like Flutter that it is easy to relax.
A `@Composable` function is `build()`, `mutableStateOf` is `setState`, and `remember` is a field on a `State` object.
The picture of "the function runs again when state changes" is the same too.

The difference is in **what gets skipped**.
Flutter reruns `build()` from the widget that called `setState` downward, and stops when it meets the same widget instance.
Compose reruns **only the scope that read the State**, and skips children whose parameters are the same as before.
And what counts as "the same" depends on the type.

> Part 4 starts from the three phases that produce a frame, then follows two ways to do less work: rerunning fewer functions (stability and Strong Skipping) and reading State in a later phase.
> On top of that, it covers `derivedStateOf` and `snapshotFlow`, keys in Lazy lists, and effects.

## A frame is built in three phases

| Phase | What it does | In Flutter terms |
|---|---|---|
| Composition | Runs Composable functions to build the UI tree | build |
| Layout | Measures and places | layout |
| Drawing | Draws to the screen | paint |

Recomposition means redoing the first phase.
It is not the same as "redrawing."

Compose records **which State was read in which phase**.
When that State changes, it redoes the work only from that phase on.

- If it was read in Composition, all three phases run again.
- If it was read in Layout, only Layout and Drawing run again.
- If it was read in Drawing, only Drawing runs again.

So optimization goes in two directions:
rerun fewer functions, and read State in a later phase.

## Skipping and stability

Even when a parent reruns, a child is not rerun if its parameters are the same as before.
This is the biggest mechanism for reducing recomposition.

To trust that a value is "the same as before," it must not change behind Compose's back.
Types Compose can trust this way are called **stable**.

| stable | unstable |
|---|---|
| Primitive types like `Int`, `String`, `Boolean` | Any class with even one `var` property |
| A data class whose properties are all `val` and of stable types | `List`, `Map`, `Set` |
| `State<T>`, classes annotated with `@Immutable` or `@Stable` | Classes from other modules the Compose compiler did not process |

`List` is unstable because it is an interface.
It may actually be a mutable list like `ArrayList`, and Compose has no way to check.

### Strong Skipping

Since Kotlin 2.0.20, Strong Skipping is on by default.

| Parameter | How it is compared |
|---|---|
| stable | `equals`. Skipped if the contents are equal |
| unstable | Same instance (`===`). Skipped if it is the same object |

Before, a single unstable parameter meant the function was never skipped.
Now it is skipped if the instance is the same.
Lambdas are also `remember`ed automatically, so the same instance is kept as long as the captured values are the same.

For a Flutter developer, the unstable rule is familiar.
It is the same as passing a `const` widget or a prebuilt `child`: because it is the same instance, Flutter skips `build()` below it.
Compose adds **content comparison** for stable types on top of that.

One problem remains.
If you build a new list every time you `copy` the state, it is a different instance even with the same contents, so it reruns.
`ImmutableList` is a stable type, so it is compared with `equals` rather than by instance.
Even if you build a new list, it is skipped when the contents are equal.

### ImmutableList for lists, @Immutable for UI models

```kotlin
data class ArticleListUiState(
    val articles: ImmutableList<ArticleUiModel> = persistentListOf(),
)

@Immutable
data class ArticleUiModel(
    val id: Long,
    val title: String,
    val publishedAt: Instant,   // even with a type from another module, promise it with @Immutable
)
```

- For lists, use `ImmutableList` from `kotlinx.collections.immutable`. Build it with `toPersistentList()`.
- Don't pass domain models through as they are; convert them to screen-specific UI models. Make every property `val` and add `@Immutable`.

`@Immutable` and `@Stable` are promises to the compiler, and nothing checks them.
If you put `@Immutable` on a class that actually changes, Compose skips even when the value changes, and the screen does not update.

## Read state late, and further down

If you read a value that changes every frame, like scroll or drag, in Composition, the function reruns every frame.
Read the same value in Layout or Drawing, and Composition is skipped.

| Passing a value (read in Composition) | Lambda version (read in a later phase) |
|---|---|
| `Modifier.offset(x = 10.dp)` | `Modifier.offset { IntOffset(x, 0) }` Layout phase |
| `Modifier.background(color)` | `Modifier.drawBehind { drawRect(color) }` Drawing phase |
| `Modifier.alpha(a)` | `Modifier.graphicsLayer { alpha = a }` Drawing phase |

```kotlin
val offsetY = remember { Animatable(0f) }

Box(
    Modifier
        .offset { IntOffset(0, offsetY.value.roundToInt()) }   // read inside the lambda → Layout
        .graphicsLayer { alpha = 1f - offsetY.value / 1000f }  // read inside the lambda → Drawing
)
```

Build a drag-to-dismiss image viewer this way, and Composition never reruns while you drag.

It is the same idea as pulling out the `child` of an `AnimatedBuilder` in Flutter, or passing a `Listenable` to a `CustomPainter` so only paint reruns.
Compose exposes that choice as the **value version and lambda version** of a Modifier.

"Reading further down" works on the same principle.
If a parent reads State and passes the value to a child, the parent reruns too.
Reading it inside the child that needs it, or passing a `() -> T` lambda instead of the value, narrows the scope.

```kotlin
// if the parent reads scrollState.value, the parent reruns on every scroll
Header(scrollProvider = { scrollState.value })

@Composable
fun Header(scrollProvider: () -> Int) {
    Box(Modifier.offset { IntOffset(0, -scrollProvider()) })  // the actual read happens in Layout
}
```

The parent only passes a lambda and never reads the value, so scrolling reruns neither the parent nor the `Header` function.

## remember, derivedStateOf, snapshotFlow

There is one more way to rerun fewer functions:
instead of reading a frequently changing State directly, read only the result the screen needs.

| Situation | What to use |
|---|---|
| A value you can recompute whenever its inputs change | `remember(key) { }` |
| A State whose inputs change often but whose result rarely changes | `derivedStateOf` |
| When you need to do work in response to State changes (requests, logs) | `snapshotFlow` + `LaunchedEffect` |

```kotlin
val listState = rememberLazyListState()
val showTopButton by remember {
    derivedStateOf { listState.firstVisibleItemIndex > 0 }
}
```

`firstVisibleItemIndex` changes on every scroll, but the button only needs to know "is it greater than 0."
`derivedStateOf` notifies only when the result changes, so the button reruns only when the list leaves the top and when it comes back.

When you are simply combining two values, `derivedStateOf` gains nothing.
The result changes every time an input changes, so use `remember(a, b)` instead.

"Detecting the end of the list" for infinite scroll leads to work, "request the next page," so it is a job for `snapshotFlow`.

```kotlin
val currentOnLoadMore by rememberUpdatedState(onLoadMore)

LaunchedEffect(listState) {
    snapshotFlow {
        val info = listState.layoutInfo
        (info.visibleItemsInfo.lastOrNull()?.index ?: 0) to info.totalItemsCount
    }
        .distinctUntilChanged()
        .collect { (lastVisible, total) ->
            if (total > 0 && lastVisible >= total - 5) currentOnLoadMore()
        }
}
```

The scroll state is not read in Composition, so scrolling does not rerun the list screen function.
`rememberUpdatedState` lets the effect use the latest `onLoadMore` without restarting. The Effect section below covers it again.

## Keys in Lazy lists

```kotlin
items(state.articles, key = { it.id }) { article ->
    ArticleRow(article, onClick = { onArticleClick(article.id) })
}
```

Without a key, Compose identifies items by position (index).
Insert one at the front and every item's position shifts, and the `remember` state inside items follows the position and attaches to the wrong item.

This is exactly why you give a `ValueKey` to items in a Flutter `ListView`.
There are two differences.

- **The same key appearing twice crashes the app.** When appending the next page, filter duplicates with `distinctBy { it.id }`.
- **A key must be something that can be saved in a Bundle.** After a configuration change like rotation, the scroll position and item state are restored by key. Use values like `Int`, `Long`, `String`.

If items come in several shapes, also give a `contentType`. Off-screen items are reused only among the same type.

## Effects: work that should happen once

A Composable function can rerun at any time, any number of times.
For the same reason you don't make network calls inside `build()`, work that affects anything outside the screen goes inside an effect.

| API | When | In Flutter terms |
|---|---|---|
| `LaunchedEffect(key)` | A coroutine while on screen. Cancelled and restarted when the key changes | `initState` + `didUpdateWidget` |
| `rememberCoroutineScope()` | Starting a coroutine from a click or drag | `async` in an event handler |
| `DisposableEffect(key)` | A register/unregister pair. `onDispose` is required | `initState` + `dispose` |
| `rememberUpdatedState(x)` | Using the latest value without restarting the effect | Reading `widget.onX` each time |

The key of `LaunchedEffect` means "when to restart."
With `Unit` it runs once while the screen is shown; put in a value that changes often and it keeps getting cancelled and restarted.

## The order to check things

1. Use **Layout Inspector** to see recomposition counts and skip counts. Look for places where the numbers keep climbing as you scroll.
2. Use **Compose compiler reports** to check whether those parameters are stable and the function is skippable.
3. Check which phase reads the State.
4. After fixing, look at the counts again. If the frames themselves are slow, move on to Perfetto and Macrobenchmark.

## Summary

- Recomposition reruns only the scope that read the State. It is different from redrawing.
- Stable parameters are compared with `equals`, unstable ones by instance (Strong Skipping).
- Keep lists as `ImmutableList`, and UI models as `@Immutable` data classes with only `val`.
- Read values that change every frame in the Layout or Drawing phase, using the lambda version of a Modifier.
- If the result changes rarely, use `derivedStateOf`; if you need to do work on change, use `snapshotFlow`.
- Give Lazy lists a key. Duplicate keys crash the app.

If you learned in Flutter that "to reduce rebuilds, add `const` and split widgets," the same thinking works in Compose.
Compose just splits the basis for that judgment more finely, into **type stability** and **the phase where a value is read**.

The next part looks at how a screen gets its ViewModel, comparing Hilt with Flutter's Context-based DI.
