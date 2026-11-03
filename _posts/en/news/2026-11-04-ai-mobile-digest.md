---
title: "Siri AI Developer Preview, CWE-bench v2, and StateBench (2026. 11. 04)"
description: "Siri AI opens as an App Intents developer preview, while CWE-bench v2 and StateBench put numbers on agent limits."
date: 2026-11-04 08:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## Today's Threads: Siri AI Developer Preview, a Security-Fix Benchmark, State Tracking Limits, and Android Dev Summit Sessions

-   Siri AI developer preview opens via App Intents
-   50+ Android Dev Summit sessions released
-   CWE-bench v2: 100 security-fix tasks
-   StateBench: state tracking in long documents
-   Qwen 3.8 27B reads model weights on a laptop

---

### Siri AI & Android Dev Summit

*   **Siri AI developer preview starts — connect your app's content and actions to Siri AI through App Intents**
    -   Any developer can use it from the iOS, iPadOS, macOS, and visionOS 27.3 betas, and App Store submissions open in spring.
    -   You can define skills that chain several actions, and Siri AI can surface any entity in the Spotlight semantic index.
    -   It is not yet available on iOS, iPadOS, and watchOS in the EU.
    [Source URL](https://developer.apple.com/news/?id=gdk2umrf) (Apple Developer News)
    > Takeaway: If your app has core flows such as ordering, booking, or lookups, check in the 27.3 beta that they are exposed through App Intents.

*   **Android Dev Summit releases 50+ sessions — with full transcripts enriched by the slides**
    -   There are four tracks: App Foundations, Intelligent Apps, Tools and Performance, and Android XR.
    -   Each track has a Gemini Notebook, and the transcripts can be downloaded and fed straight to an agent.
    [Source URL](https://developer.android.com/blog/posts/building-apps-developer-sessions) (Android Developers Blog)
    > Takeaway: Feed the Tools and Performance transcript to an agent and pull out only the items that apply to your app.

---

### Agent Benchmarks

*   **CWE-bench v2 released — 100 tasks where an agent fixes security weaknesses in real open-source repositories**
    -   It covers 91 CWEs, and grading is programmatic and deterministic, so reproducing it costs nothing extra.
    -   pass@1 is 67.8% for Gemini 4 Argon and 67.3% for Claude Opus 5.5.
    -   DeepSeek V4.1 Flash reaches 57.0% at about $0.04 per rollout, versus $1.83 for Opus.
    [Source URL](https://huggingface.co/blog/cwe-bench) (Hugging Face)
    > Takeaway: If you plan to hand vulnerability fixes to an agent, compare cost per rollout alongside pass@1 before choosing a model.

*   **StateBench released — four difficulty levels for tracking variable state changes in long documents**
    -   Frontier models, including Claude Opus 5.5 and GPT-6 Sol, dropped to 13% or lower on the longest inputs at the hardest level.
    -   In directly trained 275M models, Gated DeltaNet and hybrid architectures generalized almost perfectly to about 250 times the training length.
    -   Transformers never learned the hardest level.
    [Source URL](https://huggingface.co/blog/allenai/statebench) (Hugging Face)
    > Takeaway: When a model has to track long logs or config change history, it is safer to summarize the intermediate state yourself and pass it along.

---

### On-Device Inference

*   **Qwen 3.8 27B identifies games from a neural network's weights on a laptop — raw weights as input, no tools**
    -   Running the Q4_K_M GGUF (about 17GB) in LM Studio, it got Breakout, Pong, and Pac-Man right and Freeway wrong among four games.
    -   Identifying Pac-Man took 46m 12s and 43,506 reasoning tokens.
    -   On the same task, Kimi K3.1 Pro (via OpenRouter) identified Breakout in 9m 41s.
    [Source URL](https://simonwillison.net/2026/Nov/3/qwen-can-interpret-model-weights/) (Simon Willison)
    > Takeaway: No action needed right now.
