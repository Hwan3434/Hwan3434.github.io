---
layout: post
title: "AI & Mobile Digest - 2026-08-22"
date: 2026-08-22 06:10:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## Today's threads: ASR models that memorized the answer key, and Flutter web twice as fast on Wasm

-   11 ASR models recreate masked numbers 30-40% of the time
-   DeepSeek's vision model caps images at 384 tokens each
-   Flutter Wasm cuts widget builds from 29.3ms to 11.4ms
-   Four Antigravity agents port a package to Dart
-   Kotlin Benchmark: 105 tasks, 85.71% at the top

---

### ASR Evaluation

*   **Eleven open-source ASR models look like they reproduce benchmark transcripts instead of the audio — masked numbers come back 30-40% of the time**
    -   On LibriSpeech, some of the strongest models emitted the exact number even after it had been silenced from the audio, in roughly 30-40% of examples.
    -   Potential reference errors were flagged in 40% of the VoxPopuli test clips analyzed, and models reproduced those erroneous transcripts 18-30% of the time.
    -   Switch accuracy for dataset-specific spelling conventions such as `any one`/`anyone` and `Mr.`/`Mister` reached roughly 90%.
    [Source URL](https://huggingface.co/blog/asr-benchmark-optimization) (Hugging Face)
    > Takeaway: Do not pick a speech model on a single WER score — re-measure it on a fully held-out evaluation set.

---

### Multimodal API

*   **DeepSeek ships `deepseek-v4-flash-vision-exp` — 600 images per request, capped at 384 tokens per image**
    -   Every image is resized to about 800×800 before inference, with a max of 8192px per side, dropping to 4096px once a request carries 15 or more images.
    -   Inputs come as inline base64, an HTTP(S) URL up to 8192 characters, or a Files API reference, and using the Files API raises the per-request total from 64MiB to 200MiB.
    -   Setting `detail` to `low` processes at 512×512, while `high`/`original` keeps the original resolution.
    [Source URL](https://api-docs.deepseek.com/guides/vision/) (DeepSeek API Docs)
    > Takeaway: If you plan to batch screenshots or charts through it, redo your cost math against the 384-tokens-per-image ceiling first.

---

### Flutter Web

*   **Flutter Web WebAssembly Week — the Wasm build cuts widget build time from 29.3ms to 11.4ms (vendor-reported)**
    -   Frame time drops from 34.5ms on JS (about 30 FPS) to 17.4ms on Wasm (a sustained 60 FPS), and jitter goes from ±1.5ms to ±0.5ms.
    -   Bundle growth stays within 5% compressed over the wire, and 58% of existing Flutter web apps already compile to Wasm with zero code changes.
    -   The entry path is upgrading to Flutter 3.47 and then running `flutter build web --wasm`.
    [Source URL](https://flutter.dev/blog/try-flutter-web-with-webassembly-week) (Flutter Blog)
    > Takeaway: If you run Flutter web in production, start by running a `--wasm` build on 3.47 to see whether it compiles unchanged.

---

### Agent Workflow

*   **The Flutter team wired four agents through Antigravity's Agent Hub to port a Python library into a Dart package**
    -   Directory permissions were split per role: Architect cannot write to `lib/`, `test/`, or `example/`, and Tester cannot touch `lib/` or `specs/`.
    -   The target was python-statemachine, which leans on metaclasses and runtime callbacks, forcing a fresh design because `dart:mirrors` is off the table.
    -   Three friction points surfaced — including test utilities deleted during skeleton cleanup — requiring mid-flight skill fixes, and the result is a proof-of-concept.
    [Source URL](https://flutter.dev/blog/building-multi-agent-dev-teams) (Flutter Blog)
    > Takeaway: If you are wiring up multiple agents, design the directory write permissions before you polish the role prompts.

---

### Kotlin Tooling

*   **JetBrains' Kotlin Benchmark leaderboard — a top resolution rate of 85.71% across 105 real Kotlin issues**
    -   Claude Code + Opus 4.7 xhigh leads at 90/105, with Junie + Opus 4.7 max and Codex + GPT 5.5 xHigh tied at 86.
    -   Tasks are real open-source issues, and a task counts as resolved only when the patch passes the required tests in a container.
    [Source URL](https://kotlinlang.org/benchmark/) (JetBrains)
    > Takeaway: If you are rolling coding agents into an Android codebase, use this Kotlin leaderboard as your baseline rather than a general SWE benchmark.

---

Today's items converge on the same habit: don't take published benchmark numbers or API ceilings at face value — re-measure them on your own workload.
