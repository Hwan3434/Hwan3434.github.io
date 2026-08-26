---
layout: post
title: "AI & Mobile Digest - 2026-08-27"
date: 2026-08-27 06:10:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## Today's threads: re-measure the vendor's number in your own environment

-   A 470M ASR model hits 5.00% WER, timed on an H200
-   GLM-5.3-Flash ships MIT, 18B active out of 320B
-   vLLM on TPU keeps embeddings within 0.999 cosine
-   Play's quality bar now includes 25% DEX coverage
-   Compose Multiplatform 1.12.0 adds a Hot Reload MCP
-   Flutter triages 145 WWDC sessions with Gemini

---

### On-Device Speech

*   **IBM releases Granite Speech 5.0 Turbo CTC — a 470M ASR model aimed at edge devices**
    -   It is an encoder-only stack of 16 Conformer blocks with self-conditioning and chunkwise attention, emitting 12.5 tokens per second through three stages of 2x temporal subsampling.
    -   On the OpenASR public test sets the Apache 2.0 build scores 5.00% WER and the CC-BY-NC build 4.85% (vendor-reported).
    -   The only published speed figure is over 12,600 RTFx from batched inference on an H200 — not an on-device measurement.
    [Source URL](https://huggingface.co/blog/ibm-granite/granite-speech-5-0-470m-turboctc) (Hugging Face / IBM Granite)
    > Takeaway: If you are shortlisting it for on-device STT, pull the Apache 2.0 build and measure real-device latency yourself.

---

### Open Models

*   **GLM-5.3-Flash lands under MIT — 320B total parameters with only 18B active**
    -   It is a natively multimodal model mixing sparse and linear attention with Manifold-Constrained Hyper-Connections.
    -   The context window is 1,048,576 tokens, pre-trained on a 30T-token multimodal corpus.
    -   It scores 84.3 on Terminal-Bench 2.1 and 63.4 on DeepSWE (vendor-reported).
    [Source URL](https://huggingface.co/zai-org/GLM-5.3-Flash) (Hugging Face / Z.ai)
    > Takeaway: MIT removes the internal-deployment friction, so add it to your coding-agent backend shortlist and re-score it on your own tasks.

---

### Embedding Serving

*   **vLLM gains native TPU support — embeddings stay numerically identical across backends**
    -   GKE Custom Compute Classes let embedding workloads scale across TPU, GPU, and spot instances.
    -   Qwen3-Embedding-8B handled 83,996 tokens/second and 5.13 requests/second at 16K+ sequence length in bfloat16 (vendor-reported).
    -   Across backends, text embeddings hold cosine similarity at 0.999 or above and multimodal inputs at 0.995 or above.
    [Source URL](https://developers.googleblog.com/en/enterprise-grade-precision-for-long-context-multimodal-embedding-inference-on-cloud-tpu/) (Google Developers Blog)
    > Takeaway: If you plan to move your embedding serving backend, put a cosine-similarity parity check in the pipeline before you deploy.

---

### Play Quality Bar

*   **Play folds memory and DEX optimization into its quality requirements — enforced February and April 2027**
    -   Dynamic memory (anonymous RSS + swap), retained bitmap memory, and DEX code optimization become graded criteria.
    -   DEX requires a minimum of 25% coverage across optimization, shrinking, and obfuscation, enforced from February 2027.
    -   Apps with sign-in must auto-restore sign-in state on device transfer via the Restore Credentials API, enforced from April 2027 (games exempted).
    [Source URL](https://android-developers.googleblog.com/2026/08/app-quality-memory-optimization-secure-onboarding.html) (Android Developers)
    > Takeaway: Check your R8 coverage and whether you use Restore Credentials now, then split the work across the two deadlines.

---

### Compose Multiplatform

*   **Compose Multiplatform 1.12.0 — Hot Reload gets an MCP server for coding agents**
    -   The experimental MCP server lets an agent trigger reloads, take screenshots, inspect the semantic tree, simulate clicks and text input, and read app logs.
    -   Desktop window and dialog v2 APIs arrive as experimental in the `androidx.compose.ui.window.v2` package, leaving the original APIs untouched.
    -   On iOS, lazy layout item deactivations moved out of the drawing phase, smoothing scrolling.
    [Source URL](https://blog.jetbrains.com/kotlin/2026/08/compose-multiplatform-1-12-0/) (Kotlin Blog)
    > Takeaway: If you want agents verifying your KMP app's UI, start by wiring up the Hot Reload MCP server.

---

### Flutter iOS Readiness

*   **Flutter documents how it stays ahead of iOS — WWDC transcripts extracted, then ranked by Gemini**
    -   Dart code pulls transcripts from WWDC technical sessions, and Gemini ranks roughly 145 videos by importance, area of impact, and recommended action.
    -   The triage document lands the next day and feeds a GitHub Projects board tracking iOS 27 work.
    -   UIScene support shipped in Flutter 3.41 stable in February 2026, with only add-to-app setups needing a separate migration.
    [Source URL](https://flutter.dev/blog/how-flutter-stays-ahead-of-ios-releases) (Flutter Blog)
    > Takeaway: `flutter upgrade` covers most apps, but check the UIScene migration guide if you run an add-to-app setup.

---

Whether it is a model or an app, today's items all ask you to stop taking the vendor's number at face value and re-measure it on your device, your tasks, your backend.
