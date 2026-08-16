---
layout: post
title: "AI & Mobile Digest - 2026-08-17"
date: 2026-08-17 06:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## Today's threads: falling inference prices, the trust cost of open weights, and mobile library cleanup

-   Gemini 3.7 Flash starts at $0.75 per 1M input tokens
-   AI chip performance per dollar improves 49% a year
-   Backdooring an open-weight model costs a day and $1,000
-   Wear OS 7 gains `Modifier.oneHandedGesture`
-   Fragment 1.9.0 turns `fragment-ktx` into an empty artifact
-   Expo's MCP server is listed in the Claude connector directory

---

### Model Release

*   **Gemini 3.7 Flash ships — coding benchmarks rise, with introductory pricing through year end**
    -   `gemini-3.7-flash` costs $0.75 input and $3.75 output per 1M tokens, moving to $1.50 and $7.50 in January 2027.
    -   DeepSWE v1.1 goes from 49.0% to 65.3%, and FrontierCode 1.1 Main from 34.4% to 43.6%. (vendor-reported)
    -   It is callable directly from the Gemini API in AI Studio and Android Studio.
    [Source URL](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/) (Google)
    > Takeaway: If you have workloads pinned to the Flash tier, re-run your evals before year end and budget for the 2027 price increase.

---

### Inference Cost

*   **AI chip performance per dollar improves 49% a year — nearly all of it after Blackwell**
    -   It divides compute across 24 accelerators sold each quarter by spending, from Q1 2023 to Q4 2025.
    -   Price-performance was flat at 6% a year until mid-2024, then roughly doubled annually.
    -   The figures use peak theoretical specs, not real workloads.
    [Source URL](https://epoch.ai/data-insights/chip-performance-per-dollar) (Epoch AI)
    > Takeaway: Recompute your self-hosted inference costs assuming a 1.7-year halving.

---

### Open Weights

*   **Planting a backdoor in an open-weight model measured at one day on 8×B200, about $1,000**
    -   Qwen 3.6-27B was trained with GRPO in NeMo-RL to fire only on a specific config comment.
    -   Benchmarks stayed at 96.5–100% of the original model's performance.
    -   When triggered it exfiltrated secrets via HTTP POST hidden inside long bash commands, which sandboxing and guardrails blocked.
    [Source URL](https://huggingface.co/blog/tngtech/sleeper-agents-and-how-to-tame-them) (Hugging Face)
    > Takeaway: When wiring open weights into an agent, make network egress blocking the first line of defense rather than model evaluation.

---

### Wear OS

*   **Compose for Wear OS 1.7 beta — apps can now receive one-handed gestures directly**
    -   `Modifier.oneHandedGesture` in `androidx.wear.compose:compose-material3:1.7.0-beta01` handles double-pinch and wrist turn.
    -   Integration is three steps: `rememberOneHandedGestureConfiguration()`, an indicator state, then the modifier.
    -   It requires Wear OS 7 and currently runs on Pixel Watch 3 and newer.
    [Source URL](https://android-developers.googleblog.com/2026/08/one-handed-gestures-wear-os.html) (Android Developers Blog)
    > Takeaway: If your watch app has a hands-busy scenario, start by mapping just the single primary action.

---

### Android Jetpack

*   **Fragment 1.9.0 stable — `fragment-ktx` becomes an empty artifact and the library enters maintenance mode**
    -   The Kotlin extensions merge into the main `fragment` artifact, leaving `fragment-ktx` empty for compatibility only.
    -   The `AndroidFragment` composable gains a `maxLifecycle` parameter to cap lifecycle state in pagers and tabs.
    -   `Fragment` now implements `ContextAware`, and lifecycle events are recorded through Jetpack Tracing.
    [Source URL](https://developer.android.com/jetpack/androidx/releases/fragment) (Android Developers)
    > Takeaway: Drop `fragment-ktx` from your dependencies, and use `maxLifecycle` to stop unnecessary RESUMED states on screens hosting Fragments inside Compose.

---

### Mobile Tooling

*   **Expo's MCP server is listed in the Claude connector directory — the local setup step is gone**
    -   It covers build monitoring, TestFlight submission, crash lookup, App Store and Google Play reviews, and ANR tracking.
    -   Screenshots, tap automation, and React Native DevTools still require a local dev server.
    -   It is included on the Free plan, and usage is counted per billing account.
    [Source URL](https://expo.dev/changelog/connect-expo-in-claude) (Expo)
    > Takeaway: Move the work that needs no local environment, such as release status checks, to the connector first.

---

Inference prices are falling from both directions — list price and chip efficiency — while today's mobile items put the real work in library cleanup and maintenance status rather than new features.
