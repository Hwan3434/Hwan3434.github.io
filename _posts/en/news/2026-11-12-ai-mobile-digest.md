---
title: "Claude Fable 5.2, Gemini 4 Carbon GA, Flutter 3.50 and the CocoaPods Cutoff (2026. 11. 12)"
description: "Claude Fable 5.2 and Gemini 4 Carbon open up, Flutter 3.50 deprecates Material in core, and CocoaPods stops new releases on December 2."
date: 2026-11-12 08:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## Today's threads: two new frontier models, the Flutter 3.50 migration, and the CocoaPods deadline

-   Claude Fable 5.2 ships at $8 input, $40 output
-   One "this code is yours" sentence lifts duplicate merging from under 10% to about half
-   Gemini 4 Carbon GA, prices double on Dec 1
-   Flutter 3.50 deprecates Material and Cupertino in core
-   CocoaPods stops accepting new pods on Dec 2
-   SwiftPM compilation caching (SE-0547) accepted

---

### Frontier Models

*   **Claude Fable 5.2 ships — priced 20% below Fable 5.1 at $8 input, $40 output**
    -   On FrontierSWE v2 it scores 69.9%, against 56.3% for Fable 5.1 and 62.3% for Opus 5.5 (vendor-reported).
    -   The model ID is `claude-fable-5-2`; fast mode is up to 2.5x faster at double the price.
    -   Preserved thinking now applies to all accounts, so editing prior context to extract reasoning no longer works.
    [Source URL](https://www.anthropic.com/claude-fable-and-mythos-5-2) (Anthropic)
    > Takeaway: Switch the model ID to `claude-fable-5-2` and rerun your existing agent eval set.

*   **Fable 5.2 prompting guide — stating who owns the code increases duplicate-code merging**
    -   Adding the sentence "This codebase is yours" raised the share of runs that merged repeated code from under 10% to about half (vendor-reported).
    -   With no ownership statement, or the code framed as someone else's, the model tends to add onto the existing structure.
    [Source URL](https://simonwillison.net/2026/Nov/10/prompting-claude-fable-52/) (Simon Willison)
    > Takeaway: If you hand refactoring to an agent, state the codebase ownership in the system prompt.

*   **Gemini 4 Carbon became generally available on November 10 — launch price $2 input, $10 output**
    -   On December 1 the price doubles to $4 input and $20 output.
    -   Thinking effort has three levels, low, medium and high, with medium as the default.
    [Source URL](https://simonwillison.net/2026/Nov/10/llm-gemini/) (Simon Willison)
    > Takeaway: Base any cost comparison on the post–December 1 price.

---

### Flutter Toolchain

*   **Flutter 3.50 and Dart 3.14 ship — `material.dart` and `cupertino.dart` are deprecated**
    -   Move to `material_ui` and `cupertino_ui`; `dart fix --apply --code=migrate_design_widgets` does it automatically.
    -   `ignoringSemantics` is removed from `IgnorePointer` and `AbsorbPointer`, and `dart:html`, `dart:js` and `package:js` are deprecated.
    -   New projects default to AGP 9.3.1, Gradle 9.5.0 and KGP 2.4.20, and iOS touch input is about 16 ms faster on 60 Hz devices.
    [Source URL](https://flutter.dev/blog/whats-new-in-flutter-3-50) (Flutter Blog)
    > Takeaway: Before upgrading, scan web code with `--no-deprecated-js-interop` and run the `dart fix` command above on your design-widget imports.

---

### Swift Toolchain

*   **CocoaPods stops accepting new pods and versions on December 2 — existing pods stay read-only**
    -   Builds do not break immediately, but new releases can no longer be published.
    -   Flutter 3.50 likewise notes that CocoaPods trunk becomes read-only in December and warns in the CLI when Swift Package Manager is disabled.
    [Source URL](https://www.swift.org/blog/whats-new-in-swift-november-2026/) (Swift.org)
    > Takeaway: Check your dependencies' SwiftPM support on Swift Package Index and plan the switch before December.

*   **SwiftPM compilation caching (SE-0547) accepted — configured with `swift package build-cache configure`**
    -   It is a content-addressable cache whose scope can be global, per package, or per build.
    -   SE-0545's Perfetto trace files and task backtraces arrive first as experimental flags in nightly toolchains.
    [Source URL](https://www.swift.org/blog/whats-new-in-swift-november-2026/) (Swift.org)
    > Takeaway: No action needed right now.

---

Both the model swaps and the toolchain moves are best scheduled around dated price changes and deprecation deadlines.
