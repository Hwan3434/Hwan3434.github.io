---
layout: post
title: "AI & Mobile Digest - 2026-08-19"
date: 2026-08-19 06:10:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## Today's threads: 47% from a single keep rule, how to cage an agent, and new EU terms on October 1

-   Tinder cuts cold starts 47% via R8 Config Analyzer
-   Zero-trust ADK reference: gVisor plus a semantic gateway
-   Agent memory is a dose per model, not a switch
-   Sentence Transformers 6.0 adds MultiVectorEncoder
-   Jetpack XR hits beta02; AnchorEntity becomes AnchorSpace
-   Apple drops the CTF for a 5% Core Technology Commission

---

### App Performance

*   **Tinder cut cold starts 47% with the R8 Configuration Analyzer — the culprit was one keep rule**
    -   An overly broad keep rule in an in-house library left roughly 70% of the app unoptimized, with an optimization score of 28%.
    -   App size fell 28.98% from 86.6MB to 61.5MB, and dex files went from 17 to 11 (startup path 3 → 2).
    -   AGP 9.3 generates the report at `build/outputs/mapping/release/configanalyzer.html`, and `./gradlew :app:analyzeReleaseR8Config` produces it on demand.
    [Source URL](https://android-developers.googleblog.com/2026/08/tinder-app-cold-start-r8-configuration-analyzer.html) (Android Developers)
    > Takeaway: Move to AGP 9.3, run the report once, and start with your optimization score.

---

### Agent Sandboxing

*   **Google publishes a zero-trust agent reference implementation built on ADK**
    -   Dynamically generated code runs only inside a gVisor sandbox with `--runtime=runsc`, `--network=none`, `--memory=64m`, and a 5-second timeout.
    -   Every database mutation is signed with a Cloud KMS HSM key, with HMAC standing in for local demos.
    -   A semantic gateway blocks PII, credit card patterns, and `sk_live_`-style secrets in model input and output via deterministic rules.
    [Source URL](https://developers.googleblog.com/en/build-zero-trust-ai-agents-with-googles-agent-development-kit/) (Google Developers Blog)
    > Takeaway: If your agent has a code-execution tool, port the three layers from the zero-trust-agents reference as they are.

---

### Agent Memory

*   **Agent memory is a dose you calibrate per model, not a feature you switch on**
    -   gpt-oss-120b goes from 39.9% to 56.0% TGC with curated retrieval, at only a 5% token increase.
    -   DeepSeek-V3.2 gains +9.5pp but costs 78% more tokens, and Claude Opus 4.6 gains just +4.1pp.
    -   The comparison ran ALTK-Evolve across eight models on AppWorld's 585 multi-step tasks.
    [Source URL](https://huggingface.co/blog/ibm-research/altk-evolve-hmm) (Hugging Face / IBM Research)
    > Takeaway: If you feed a strong model a large guideline set, re-measure accuracy against the token increase first.

---

### Retrieval

*   **Sentence Transformers 6.0 makes late interaction models first class**
    -   `MultiVectorEncoder` loads ColBERT-family models, with `encode_query()` and `encode_document()` for asymmetric encoding.
    -   4,874 Natural Questions passages take 311.5MB as float32, 92MB in a PLAID index, versus 7.5MB for the dense 384d equivalent.
    -   `HierarchicalTokenPooling` at `pool_factor=2` cuts vectors 1.99x while retaining 100.6% of BEIR performance.
    [Source URL](https://huggingface.co/blog/multi-vector-encoder) (Hugging Face)
    > Takeaway: If you are weighing late interaction, budget the storage cost first — it is over 10x the dense equivalent.

---

### Android XR

*   **Jetpack XR core libraries reach beta — names and signatures changed**
    -   SceneCore, ARCore for Jetpack XR, and XR Runtime are all at 1.0.0-beta02, while Compose for XR remains at 1.0.0-alpha17.
    -   `AnchorEntity` is renamed to `AnchorSpace` and now extends `SpaceEntity` alongside `ActivitySpace`.
    -   `Session.create` became a suspend function, and testing APIs were added for spatial audio and session configuration.
    [Source URL](https://android-developers.googleblog.com/2026/08/jetpack-xr-sdk-core-libraries-beta.html) (Android Developers)
    > Takeaway: If you wired up XR code against alpha, handle the `AnchorEntity` rename and the `Session.create` suspend change first.

---

### Store Policy

*   **Apple reworks EU app business terms — effective October 1**
    -   The per-install Core Technology Fee is gone, replaced by a 5% Core Technology Commission on digital transactions in apps distributed outside the App Store.
    -   The Initial Acquisition Fee and Store Services Fee are eliminated, and App Store apps may offer alternative payments alongside IAP.
    -   Attachment 14 of the Apple Developer Program License Agreement was updated and must be accepted from your account.
    [Source URL](https://developer.apple.com/news/?id=gmws0jgp) (Apple Developer News)
    > Takeaway: If you ship in the EU, accept Attachment 14 and recalculate per-payment-path fees against the October 1 date.

---

On the AI side today the story is re-measuring an agent's defaults — how much memory, how much execution privilege — while on mobile it is applying what a tool or a release note already flagged, before the deadline.
