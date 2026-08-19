---
layout: post
title: "AI & Mobile Digest - 2026-08-20"
date: 2026-08-20 06:10:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## Today's threads: a 27B squeezed into 6.2GB, a memory cap that kills apps, and a model that writes its own tasks

-   Unsloth Dynamic 3.0 keeps 72% top-1% at 6.2GB
-   Android 17 caps app memory: zRAM first, then a kill
-   EAS Observe hits GA with a 100k free event quota
-   Ornith-1.5 claims SWE-Bench 86.0 via self-scaffolding
-   Mojo's compiler and toolchain go Apache 2.0

---

### On-Device Quantization

*   **Unsloth Dynamic 3.0 GGUFs claim a 10pp top-1% accuracy edge at the same size (vendor-reported)**
    -   Qwen3.8-27B's `UD-IQ1_S` is 89% smaller at 6.2GB while retaining roughly 72% top-1% accuracy.
    -   On Gemma 3 27B, `Q2_K_XL` scores 68.70% MMLU 5-shot at 9.95GB versus 71.47% for `Q4_K_XL` at 15.64GB.
    -   The files load in most inference engines including llama.cpp, and smaller quants drop the MTP module to save another ~500MB.
    [Source URL](https://unsloth.ai/docs/basics/dynamic-3.0-ggufs) (Unsloth)
    > Takeaway: If you are picking a GGUF for local or on-device inference, first measure what the 5.7GB you save by dropping from Q4 to Q2_K_XL actually costs you.

---

### Android Runtime

*   **Android 17 introduces per-app memory limits — exceed them and you get zRAM, then termination**
    -   An app over its budget has its pages compressed into zRAM, adding CPU overhead and UI jank, and the process is killed if usage keeps climbing.
    -   Identify these kills via `ApplicationExitInfo.getDescription()` returning `REASON_OTHER` with `MemoryLimiter:AnonSwap`.
    -   It ships on Pixel first and expands across manufacturers over the coming year, spanning 4GB to 16GB+ devices.
    [Source URL](https://android-developers.googleblog.com/2026/08/app-broader-memory-limits.html) (Android Developers)
    > Takeaway: Start with Android Vitals' Memory Usage (RSS + swap) and Bitmap Memory Usage, then wire up the API 35 ProfilingManager for production heap dumps.

---

### App Observability

*   **Expo EAS Observe moves to GA today — the free tier now has an event quota**
    -   Free gets 100,000 monthly events, Starter and above get 500,000, and overages cost $5 per 1M events.
    -   Data retention is standardized at 90 days across all plans.
    -   It provides dashboards for app startup, navigation, and EAS Update, and GA requires no code changes.
    [Source URL](https://expo.dev/changelog/eas-observe-moves-to-general-availability-on-august-20) (Expo)
    > Takeaway: If you left it on unsampled during the beta, adjust your sampling rate or disable ingestion before billing starts.

---

### Coding Agents

*   **Ornith-1.5 proposes its own tasks and scaffolds to close an RL loop (vendor-reported)**
    -   The 397B MoE reportedly scores 86.1 on Terminal-Bench 2.1 and 86.0 on SWE-Bench Verified.
    -   The model proposes tasks, then generates task-specific scaffolds and solution rollouts, with harness and rollout quality optimized separately via GRPO.
    -   It ships in three sizes: 397B MoE, 35B MoE, and 9B dense.
    [Source URL](https://ornith.ai/ornith_1_5.html) (Ornith)
    > Takeaway: Hold the numbers until third-party reproductions land, and take only the three-stage self-scaffolding loop as a reference.

---

### Language Toolchain

*   **Mojo's compiler and toolchain are now Apache 2.0**
    -   The full compiler and toolchain opened under Apache 2.0 about a week after the 1.0 release.
    -   The Python-superset goal is off the table; Mojo is now positioned as a standalone language for GPU programming.
    [Source URL](https://simonwillison.net/2026/Aug/18/mojo-is-now-open-source/) (Simon Willison)
    > Takeaway: No action needed right now.

---

Today's items share a shape: quant size, app memory, event quota — things that used to go unmeasured now come with a ceiling, and the budget has to be reallocated inside it.
