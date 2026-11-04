---
title: "Compose 1.13 RC, Apple Subscription Retention Messages, Transformers MIC (2026. 11. 05)"
description: "Compose 1.13.0-rc01 and Apple retention messages arrive, and Transformers adds MIC model-integration tests to CI."
date: 2026-11-05 08:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## Today's Threads: Compose 1.13 RC, Subscription Retention API, Model Integration Tests, Small-Model Fine-Tuning

-   Compose 1.13.0-rc01 ships with Material 3 1.5.0-rc01
-   Apple subscription retention messages and Retention Messaging API
-   27.3 betas out, Xcode 27.3 recommended
-   Transformers adds MIC tests on shrunken fixtures
-   Palette: a 20B model that builds slide decks

---

### Android & Apple Toolchain

*   **Compose 1.13.0-rc01 released — Material 3 moves to 1.5.0-rc01 alongside it**
    -   Runtime, UI, Foundation, Animation and Material are all at 1.13.0-rc01.
    -   Compose Remote is 1.0.0-alpha23 and Wear Compose is 1.8.0-alpha03.
    [Source URL](https://developer.android.com/jetpack/androidx/versions/all-channel) (Android Developers)
    > Takeaway: Build the RC on a separate branch before stable and report regressions early.

*   **27.3 betas out for iOS, iPadOS, macOS, tvOS, visionOS and watchOS — Xcode 27.3 recommended**
    -   All six platforms have 27.3 betas available.
    -   The announcement does not say whether Xcode 27.3 is itself a beta.
    [Source URL](https://developer.apple.com/news/?id=6gpufove) (Apple Developer News)
    > Takeaway: Add a separate Xcode 27.3 CI job and check build warnings first.

*   **Subscription retention messages now available — text, image or offer shown in the cancellation flow**
    -   App Store Connect lets you set eligible subscribers and the wait time between messages.
    -   The Retention Messaging API lets your app pick a message per subscriber; API access is by request.
    [Source URL](https://developer.apple.com/news/?id=fk9ps3gv) (Apple Developer News)
    > Takeaway: If you run subscriptions, request API access now and draft messages per cancellation reason.

---

### AI Engineering Practice

*   **Transformers adds Model Integration Contracts (MIC) — regression tests on shrunken models**
    -   Llama 4 Scout shrinks from 108.6B to 44.7M parameters while keeping every layer kind.
    -   In a Whisper study, random-weight fixtures caught 18 of 24 injected faults and overfit fixtures caught all 24.
    -   The MIC CI job currently reports failures without blocking PRs.
    [Source URL](https://huggingface.co/blog/transformers-mic) (Hugging Face)
    > Takeaway: If you wrap models yourself, consider pinning shrunken fixtures and baseline outputs in CI.

*   **Palette released — a 20B open-weight model that builds slide decks in the IBM Design Language**
    -   One LoRA adapter acts as both designer (JSON brief) and coder (pptxgenjs), and parallel coding is 6–7× faster.
    -   A render-and-check harness for overlap and clipping added 3.5 points on average across 131 decks.
    -   Its three-domain PresentBench mean is 59.7, second place and 1.1 behind NotebookLM (60.8). (vendor 측정)
    [Source URL](https://huggingface.co/blog/ibm-research/palette-deck-building) (Hugging Face)
    > Takeaway: The render-then-verify loop transfers directly to your own agents.

---

Today's items are all beta, RC or experimental, so each can be tried before it goes stable.
