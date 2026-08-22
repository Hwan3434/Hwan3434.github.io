---
layout: post
title: "AI & Mobile Digest - 2026-08-23"
date: 2026-08-23 06:10:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## Today's threads: structured output moves on-device, and one default swallows 20 seconds of TTFT

-   Firebase AI Logic adds on-device `generateObject`
-   Android Studio Rabbit 1 uploads straight to Play test tracks
-   Toss: prefix cache was off, TTFT sat at 20s
-   Qwen3-TTS holds p95 TTFA under 50ms
-   llm 0.33 moves to openai 3.x and httpx2

---

### On-Device Inference

*   **Firebase AI Logic 17.16.0 — `generateObject` now returns structured output from on-device inference too**
    -   It ships in Android BoM `34.18.0`, and the companion On-Device SDK `16.0.0-beta05` accepts a model selection.
    -   The same release removes the deprecated Imagen methods and types, and the Imagen models themselves shut down in August 2026.
    -   Apple SDK `12.18.0` adds `sendStartActivityRealtime`/`sendStopActivityRealtime` to `LiveSession`.
    [Source URL](https://firebase.google.com/support/release-notes/android) (Firebase Release Notes)
    > Takeaway: If any Imagen calls remain, migrate them to the Gemini Image models before you bump the BoM.

---

### Android Tooling

*   **Android Studio Rabbit 1 (2026.2.1) canary — upload to a Play test track directly from Generate Signed App Bundle**
    -   A new app's first release goes to the internal test track, and later releases can go to the other test tracks as well.
    -   Compose Preview Screenshot Testing generates HTML reports so UI changes can be compared visually.
    -   The Model Assignment tab lets you pin a pro-tier model to Agent Mode and a lightweight one to latency-sensitive tasks.
    [Source URL](https://developer.android.com/studio/preview/features) (Android Developers)
    > Takeaway: If you maintain a separate CI step for internal distribution, measure on canary whether this path can replace it.

---

### LLM Serving

*   **Toss traced a 20-second TTFT in its internal LLM serving to a prefix cache that was off by model default**
    -   Once enabled, prefix cache hit rate passed 90% and TTFT dropped to roughly a tenth.
    -   Throughput sat near 1,000 TPS while KV cache usage stayed under 1%, leaving room for 4× traffic with no extra GPUs.
    -   Fixing a vLLM bug in thinking-token handling that truncated output cut the error rate from 0.2% to 0.02%.
    [Source URL](https://toss.tech/article/tech_talk_talk_2) (Toss Tech)
    > Takeaway: If you self-host serving, put per-model prefix cache defaults and KV cache utilization on the dashboard first.

---

### Speech Serving

*   **Nari Labs serves Qwen3-TTS 1.7B on a single H100 at p95 TTFA under 50ms (vendor-reported)**
    -   It produces about 630 characters per second at 10 RPS, and TTFA stays below 100ms even at 20 RPS.
    -   Dynamic silence trimming on the leading audio alone cut TTFA by roughly 80ms.
    -   Talker, Code Predictor, and Codec share one scheduler, with a CUDA graph over the Code Predictor's fixed 15-step section.
    [Source URL](https://nari-labs.com/blog/qwen3-tts-speed-cost-frontier/) (Nari Labs)
    > Takeaway: To cut voice response latency, measure silence trimming and scheduler unification before swapping models.

---

### Agent Tooling

*   **llm 0.33 — the jump to OpenAI Python 3.x swaps the HTTP client from `httpx` to `httpx2`**
    -   The previous day's 0.32.1 was a hotfix that temporarily pinned `openai<3` to stop fresh installs from failing.
    -   `-t/--template` can now be repeated, so a model-configuration template and a prompt template can be layered.
    -   Reasoning models on the Responses API gain a `reasoning_summary` option with `auto`/`concise`/`detailed`.
    [Source URL](https://simonwillison.net/2026/Aug/22/llm/) (Simon Willison)
    > Takeaway: If you maintain an llm plugin, check whether it still depends on `httpx` directly.

---

Today's items overlap on the same point: the gains came from touching defaults and release plumbing, not from swapping models.
