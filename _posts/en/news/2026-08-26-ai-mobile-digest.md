---
layout: post
title: "AI & Mobile Digest - 2026-08-26"
date: 2026-08-26 06:10:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## Today's threads: measure the ceiling before you shrink a model or ship an app

-   A 4-bit model beats its BF16 source on 7 of 9
-   Granite 4.2 3B/8B/30B ship Apache 2.0 with GGUF
-   Android 17 caps per-app memory: zRAM, then kill
-   Flutter desktop multi-window API lands on main
-   Play now wants adversarial-prompt proof at review

---

### On-Device Quantization

*   **A 4-bit model outperforms its full-precision source — Multiverse publishes Quantization-Aware Healing**
    -   QAH distills from the original full-precision teacher rather than the recovered checkpoint after compression.
    -   GPT-OSS 120B compressed to 60B at MXFP4 beat the 60B BF16 baseline on 7 of 9 benchmarks (vendor-reported).
    -   QAT collapsed 19 points after its peak, while QAH reached its peak in roughly 100 steps and stayed stable.
    [Source URL](https://huggingface.co/blog/MultiverseComputingCAI/quantization-aware-healing) (Hugging Face / Multiverse Computing)
    > Takeaway: If QAT falls apart in your 4-bit on-device conversion, swap the teacher for the pre-compression original and measure again.

---

### Open Models

*   **IBM releases Granite 4.2 — 3B/8B/30B all under Apache 2.0 with GGUF conversions included**
    -   All three are dense decoder-only models with GQA (40 heads / 8 KV heads), extended to a 512K-token context.
    -   The 3B scores 78.33% on AIME25 and 67.84% on MMLU-Pro (vendor-reported).
    -   GGUF builds made with the canonical llama.cpp tool ship in 14 formats from Q8_0 down to Q2_K.
    [Source URL](https://huggingface.co/blog/ibm-granite/granite-4-2) (Hugging Face / IBM Granite)
    > Takeaway: If you are eyeing the 3B for on-device, start measuring real-device latency around the Q4 GGUF.

---

### Android Memory

*   **Android 17 introduces per-app memory limits — exceed them and you get zRAM swap, then termination**
    -   It starts on Pixel devices, and pages past the limit are compressed into zRAM, surfacing as CPU overhead and jank.
    -   On a kill, `ApplicationExitInfo` reports reason `REASON_OTHER` with the description `MemoryLimiter:AnonSwap`.
    -   Crashlytics 20.1.0 adds extra debug data for OOM exceptions and memory limiter kills.
    [Source URL](https://android-developers.googleblog.com/2026/08/app-broader-memory-limits.html) (Android Developers)
    > Takeaway: Open the Memory Usage (Anonymous RSS + swap) metric in Android vitals and check the headroom on your heaviest screens.

---

### Flutter Desktop

*   **Flutter's desktop multi-window API lands — you start with `runWidget` instead of `runApp`**
    -   Five window types — regular, dialog, popup, tooltip, satellite — are handled through paired `WindowController` and `Window` widgets.
    -   All windows share a single widget tree, so existing state management like Riverpod or Bloc works unchanged.
    -   It is currently gated behind an experimental flag on the main channel and needs `flutter config --enable-windowing`.
    [Source URL](https://flutter.dev/blog/desktop-windowing-apis) (Flutter Blog)
    > Takeaway: If you ship a desktop target, keep this at prototype scope for now and budget for API changes.

---

### Play Policy

*   **Play spells out review requirements for generative AI apps — adversarial prompt testing must be documented**
    -   You must give reviewers a test account with full access to every generative AI feature, with no paywall or geo-fence.
    -   You must submit evidence that the underlying model rejects deepfake and nudify-style requests.
    -   Beyond the model's native filters, you are told to add your own input/output moderation and validate output before rendering.
    [Source URL](https://android-developers.googleblog.com/2026/08/ensuring-safety-genai-preventing-non-consensual-intimate-content.html) (Android Developers)
    > Takeaway: If you have image generation or editing, add the review test account and adversarial prompt logs to your release checklist.

---

Whether you are shrinking a model or shipping an app, today's items ask you to measure the ceiling — device or review — before you hit it.
