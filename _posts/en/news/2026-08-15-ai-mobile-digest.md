---
layout: post
title: "AI & Mobile Digest - 2026-08-15"
date: 2026-08-15 23:20:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## Today's threads: an on-device model generation shift, toolchain upgrades, and the cost of running many agents

-   Gemini Nano 4 on Pixel 11, Prompt API gains structured output
-   Compose 1.12 requires compileSdk 37 and AGP 9.1.1
-   Dart 3.13 promotes primary constructors to stable
-   18 of 30 agents created the same branch name
-   GPT-5.6 Sol Ultrafast, 750 tokens/sec limited preview
-   Don't classify — generate, then match by embedding

---

### On-Device Inference

*   **Pixel 11 runs Gemini Nano 4 on-device — ML Kit GenAI Prompt API adds structured output and thinking mode**
    -   The Prompt API supports structured output, thinking mode, and over 140 languages.
    -   The entry point stays the ML Kit GenAI API on top of AICore, so the call structure is unchanged.
    [Source URL](https://android-developers.googleblog.com/2026/08/pixel-app-experience-made-by-google.html) (Android Developers Blog)
    > Takeaway: Prototype your summarization and tagging round-trips with the Prompt API's structured output and measure on-device latency yourself.

---

### Jetpack Compose

*   **Jetpack Compose 1.12 stable — compileSdk 37 and AGP 9.1.1 are effectively mandatory**
    -   The BOM is `2026.08.00` with core modules at 1.12, and compileSdk moves to API 37.
    -   `Modifier.onFirstVisible()` is deprecated in favor of `Modifier.onVisibilityChanged()`.
    -   `SideEffect` with key arguments is up to 90% faster than `LaunchedEffect` (vendor-measured).
    [Source URL](https://android-developers.googleblog.com/2026/08/jetpack-compose-august-2026-release.html) (Android Developers Blog)
    > Takeaway: Grep for `onFirstVisible` call sites and migrate them first, then schedule the AGP 9.1.1 bump as a work item this quarter.

---

### Dart Toolchain

*   **Dart 3.13 — primary constructors go stable, dart2wasm gets a deferred loading preview**
    -   Primary constructors are promoted to stable, shipping with six lints that carry automated fixes.
    -   `dart compile wasm -O2 --enable-deferred-loading` enables deferred loading in preview.
    -   The `@RecordUse()` annotation allows tree-shaking down to the native functions actually called.
    [Source URL](https://dart.dev/blog/announcing-dart-3-13) (The Dart Blog)
    > Takeaway: The formatter change that separates import sections produces a codebase-wide diff, so keep it out of feature commits.

---

### Multi-Agent Systems

*   **Anthropic measured how agents fail when several are turned loose on the same codebase**
    -   18 of 30 agents created the identical branch name `mvp-game-loop`.
    -   One job queue received 2.4 million requests against 117 acceptable jobs.
    -   A coordinated swarm found 266 vulnerabilities over 27M tokens; independent parallel agents found 21 over 6.5M.
    [Source URL](https://www.anthropic.com/research/multiagent-systems) (Anthropic Research)
    > Takeaway: If you run coding agents in parallel, put branch-name namespacing and queue rate limits in place now.

---

### Inference Serving

*   **OpenAI and Cerebras preview a GPT-5.6 Sol Ultrafast tier at up to 750 tokens per second**
    -   Output runs at up to 750 tokens/sec, and model intelligence is stated to match Standard.
    -   GDP-Val shows a 5.6x end-to-end speedup with no reported quality loss (vendor-measured).
    -   The Wafer-Scale Engine keeps weights in 44GB of on-chip SRAM per wafer, bypassing the memory bandwidth bottleneck.
    [Source URL](https://www.cerebras.ai/blog/accelerating-gpt-5-6-sol-ultrafast-with-openai) (Cerebras)
    > Takeaway: If your app streams LLM output, check the client render path — at hundreds of tokens per second the typewriter animation and rebuild rate become the new bottleneck.

---

### Prompt Engineering

*   **Don't classify, generate — let the model invent tags, then match them to your real corpus by embedding**
    -   Doug Turnbull's pattern asks the LLM for "novel, never seen before" classifications, then links them to real tags by vector similarity.
    -   Including examples of the existing tag hierarchy in the prompt is what lifts candidate quality.
    [Source URL](https://simonwillison.net/2026/Aug/14/dont-classify-hallucinate/) (Simon Willison's Weblog)
    > Takeaway: For classification over a large candidate list, replace stuffing every tag into context with a generate-then-match structure.

---

More than half of today's items put the real cost not in the feature but in the upgrade conditions that unlock it — compileSdk 37, AGP 9.1.1, formatter diffs, and agent isolation.
