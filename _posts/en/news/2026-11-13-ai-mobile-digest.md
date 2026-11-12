---
title: "Gemini Decisions API, Flutter Native Interop Goes Stable, CameraX Case Study (2026. 11. 13)"
description: "Gemini Decisions API and the llm 0.37.2 security fix landed, Flutter stabilized FFIgen and JNIgen, and Android shared a CameraX case study."
date: 2026-11-13 08:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## Today's Threads: Gemini Decisions API, llm Security Fix, Flutter Native Interop Goes Stable, CameraX Case Study

-   Gemini Decision 1, $0.10 per 1M input tokens
-   llm 0.37.2 fixes two OpenAI API key leak paths
-   Anthropic: Claude on AMD GPUs in 3 days (vendor-reported)
-   Flutter FFIgen and JNIgen stable, Pigeon in preview
-   SmileID gets 4x selfie resolution with CameraX

---

### AI Engineering

*   **Gemini Decision 1 launches — an API with three question types: yes/no, choice, and rubric-scoring**
    -   Input costs $0.10 per 1M tokens, output is free, and it accepts text, images, audio, video, and PDFs.
    -   For yes/no questions it returns graded probabilities (e.g. 0.92, 0.05) rather than 1.0 or 0.0.
    [Source URL](https://simonwillison.net/2026/Nov/11/gemini-decisions-api/) (Simon Willison)
    > Takeaway: For classification or filtering, design around a probability threshold you choose instead of a 0/1 answer.

*   **llm 0.37.2 security release — fixes two cases where an OpenAI API key could be sent to another provider's endpoint**
    -   In `extra-openai-models.yaml`, it happens when the key named by `api_key_name` was never stored.
    -   It also happens when a `responses: true` model runs with `-o chat_completions 1`.
    [Source URL](https://simonwillison.net/2026/Nov/11/llm/) (Simon Willison)
    > Takeaway: If you registered custom endpoints with `llm openai endpoint add`, upgrade to 0.37.2.

*   **Anthropic says it got Claude running on AMD GPUs in three days — Claude wrote almost all the kernels**
    -   It says it trains and serves Claude on Trainium, TPUs, NVIDIA GPUs, and AMD GPUs (vendor-reported).
    -   It says a new chip platform used to take dozens of engineers months.
    [Source URL](https://simonwillison.net/2026/Nov/11/anthropic-ipo-roadshow/) (Simon Willison)
    > Takeaway: Hand coding agents tasks with clear verification, such as kernel ports, first.

---

### Flutter Native Interop

*   **Flutter stabilizes FFIgen (Objective-C) and JNIgen (Java/Kotlin) — Pigeon native interop is in preview**
    -   With Pigeon v30.0 or later, the `useFfi` and `useJni` options skip platform channel serialization.
    -   It enables synchronous calls and calls from background isolates; it supports Android, iOS, and macOS, while Windows and Linux keep platform channels.
    -   The `shared_preferences` plugin serves as a migration reference.
    [Source URL](https://flutter.dev/blog/stable-native-interop) (Flutter Blog)
    > Takeaway: If you maintain a plugin, enable both options in its Pigeon file and regenerate.

---

### Android Camera

*   **SmileID moved to CameraX: 4x selfie resolution and 20% higher verification pass rate (vendor-reported)**
    -   It paired `ResolutionSelector` with `STRATEGY_KEEP_ONLY_LATEST` on `ImageAnalysis` to avoid OOM on low-end devices.
    -   It compresses the face crop on-device so upload size stays unchanged, and supports 18,000+ device types.
    [Source URL](https://developer.android.com/blog/posts/smileid-camerax-android-identity-verification.md.txt) (Android Developers Blog)
    > Takeaway: For low-end device support, cap memory with `FALLBACK_RULE_CLOSEST_LOWER_THEN_HIGHER`.
