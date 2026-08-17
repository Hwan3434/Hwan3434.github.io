---
layout: post
title: "AI & Mobile Digest - 2026-08-18"
date: 2026-08-18 06:10:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## Today's threads: how AI-written code breaks CI, the real cost of over-reasoning, and an August 31 deadline

-   A Copilot Autofix PR introduced a CI script injection
-   Qwen 3.8 27B defaults to xhigh reasoning effort
-   llama.cpp adds Kimi-K3 with lossless MXFP4 repacking
-   Android Studio Quail 4 runs Gemma 4 locally in the IDE
-   targetSdk under 36 loses new users from August 31
-   klibs.io ships an MCP server for KMP libraries

---

### Agent Security

*   **A PR authored by Copilot Autofix created a GitHub Actions script injection, and a Jira token leaked**
    -   The `snowflake-connector-net` workflow replaced `env:` passing with `echo '${{ github.event.issue.title }}'`, so a quote in an issue title could execute commands.
    -   The guard condition checked `github.event.pull_request.user.login`, which is null on issue events and therefore always passed.
    -   Exposure ran five days from the June 18 merge to the June 23 patch, and the leaked token granted read access to Jira projects.
    [Source URL](https://www.wiz.io/blog/red-agent-snowflake-copilot-cicd-bug) (Wiz)
    > Takeaway: Add a review item for AI-generated CI/CD changes that checks whether template expansion inside `run:` was moved back to `env:` or `jq --arg`.

---

### Local Inference

*   **Qwen 3.8 27B defaults to xhigh reasoning effort and overthinks even simple requests**
    -   Drawing a single SVG consumed 22,276 reasoning tokens and 21 minutes, versus 137 seconds with reasoning disabled.
    -   It is 27B dense under Apache 2.0, 17GB at Q4_K_M, with a 262,144-token context.
    -   It runs at 15–30 tokens/s in LM Studio on a 128GB M5 Max, and about 72% faster with Multi-Token Prediction enabled.
    [Source URL](https://simonwillison.net/2026/Aug/16/qwen-38-27b/) (Simon Willison)
    > Takeaway: If you wire this model in locally, make `low` or disabled reasoning effort your default setting.

---

### On-Device Runtime

*   **llama.cpp adds Kimi-K3 — MXFP4 tensors are repacked without requantization**
    -   The routed experts' mxfp4-pack-quantized weights repack losslessly into ggml MXFP4, removing a roughly 5.5TB bf16 conversion step.
    -   It implements hybrid attention mixing KDA (linear) and MLA (full), latent MoE, and cross-layer residual attention.
    -   Final logits were verified at 6.7e-05 relative error and 1.00000000 correlation against the fp32 reference.
    [Source URL](https://github.com/ggml-org/llama.cpp/releases/tag/b10448) (llama.cpp)
    > Takeaway: If conversion disk and time are your bottleneck when bringing large MoE models local, move to a build after b10448.

---

### Android Tooling

*   **Android Studio Quail 4 RC — Gemma 4 runs locally inside the IDE**
    -   Enabling it under Settings > Tools > AI > Model Providers > Gemma gives local code assistance with no third-party hosting.
    -   Agent Mode's Firebase agent skills complete Authentication and Cloud Firestore setup without leaving the IDE.
    -   Compose Interactive Preview gains a Navigate Back action and a Predictive Back Progress slider.
    [Source URL](https://developer.android.com/studio/preview/features) (Android Developers)
    > Takeaway: If your organization blocks code from leaving the network, evaluate the local Gemma 4 provider first.

---

### Store Policy

*   **Google Play stops showing apps below targetSdk 36 to new users starting August 31**
    -   New apps and updates must target Android 16 (API 36) or higher, with Wear OS and Automotive at 35 and TV and XR at 34.
    -   Apps are not removed from the store; they simply stop reaching new users on an OS newer than the app's target.
    -   An extension to November 1 can be requested from the Policy status page in Play Console.
    [Source URL](https://support.google.com/googleplay/android-developer/answer/11926878?hl=en) (Google Play Console Help)
    > Takeaway: Check your `targetSdkVersion` this week and file the extension request if the move to 36 is not finished.

---

### KMP Tooling

*   **klibs.io grows to 4,200 KMP projects — an MCP server and expert skill arrive**
    -   The MCP server lets agents search by platform and target and pull the latest published versions straight from the index.
    -   The Kotlin Multiplatform Libraries expert skill covers platform-support checks and dependency coordinate lookup.
    -   A recommended AGENTS.md snippet ships alongside for projects to adopt.
    [Source URL](https://blog.jetbrains.com/kotlin/2026/08/klibsio-grows-to-4200-kmp-projects-with-smarter-discovery-and-new-ai-integrations/) (JetBrains)
    > Takeaway: If agents pick your KMP dependencies, point them at the klibs.io MCP server instead of training data to cut version hallucination.

---

Today's items converge on where to verify code and dependencies that AI produced, and on mobile that point splits between a local model inside the IDE and an August 31 policy deadline.
