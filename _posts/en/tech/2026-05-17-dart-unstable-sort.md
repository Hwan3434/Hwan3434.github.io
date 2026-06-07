---
title: "The Betrayal of Dart's List.sort(): Still Using Unstable Sort?"
description: "A story of struggling for over an hour due to the instability of Dart's default sort and the solution (collection package)"
date: 2026-05-17 12:16:00 +0900
categories: [flutter, troubleshooting]
tags: [Dart, Sort, Stable Sort, Troubleshooting]
toc: true
---

When developing, there is basic knowledge we firmly believe languages or frameworks will naturally provide. For me, that belief was 'the default sort algorithm must naturally be a stable sort'.

Recently, while implementing a secondary sort (multi-condition sort) logic in Dart (Flutter), this belief was shattered. There was clearly no problem with the logic, yet I experienced a bizarre phenomenon where the sort results kept getting jumbled. After spending over an hour looking for the cause, I discovered a shocking fact.

The biggest reason I wandered for so long was **'because I completely didn't suspect the language itself'**. Since almost all modern languages adopt stable sort by default, I firmly believed Dart wouldn't be any different and only kept staring at my own logic, which was the root of the trouble.

## The Problem: Why isn't the secondary sort working?

Usually, when sorting a list based on multiple conditions, an intuitive method is to perform the sort twice consecutively. For example, sorting first by the secondary condition, and then overwriting the sort with the primary condition.

Since most languages support stable sort (a sort that guarantees the original order when values are identical), this method works well. However, when I called `List.sort()` twice in a row in Dart, the order that had been sorted previously was completely ruined.

## The Cause: Dart's default sort is an 'unstable sort'

Upon checking the official documentation, I found out that **Dart's default `List.sort()` method does not guarantee a stable sort**.

> "The sort function is not guaranteed to be stable, so distinct objects that compare as equal might change their relative order."
> — [*Dart API Reference: List.sort()*](https://api.dart.dev/stable/dart-core/List/sort.html)

Dart adopts an unstable sort method internally for performance. Therefore, even for elements with the same priority, you should not expect their relative positions to remain the same after sorting.

## The Solution: collection package

The solution was very obvious and simple. If you absolutely need a stable sort, you can use `mergeSort` from the `collection` package provided by the official Dart team.

```dart
import 'package:collection/collection.dart';

// Instead of the existing unstable myList.sort(), use as follows
mergeSort(myList, compare: (a, b) => a.compareTo(b));
```

Because `mergeSort` uses the merge sort algorithm, it perfectly guarantees a stable sort. As soon as I applied this, the multi-sort problem was cleanly resolved, making my hour of struggle seem pointless.

## Conclusion: An anti-pattern committed in the name of efficiency?

In fact, the biggest problem I felt through this struggle is something else. It is that **the language secretly switches sort methods based on the number of data elements (32) for performance optimization**.

Weighing efficiency and taking a strategy that changes the sorting method depending on the data size itself could be excellent. However, I think this is an area that a developer should intentionally choose and control according to the situation at the service logic or business level, **not a role that the core API of a language should implicitly perform.**

Isn't sacrificing the operational consistency of an API that developers expect, just to grab a few bytes of memory efficiency, a clear **anti-pattern** in framework design? It was troubleshooting that left me with a strange sense of betrayal thinking, **"There's still a language that uses unstable sort as its default sort in this day and age?"**, and a deep question of why the Dart team doesn't change this.

If there is anyone who, like me, tries to attempt multi-sorting by calling `.sort()` multiple times in Dart and ends up with a twisted order, I hope you quickly reach for the `collection` package after checking the language's inconsistent default sorting method before doubting your logic.
