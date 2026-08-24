---
layout: post
title: "AI & Mobile Digest - 2026-08-25"
date: 2026-08-25 06:10:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## Today's threads: audit the settings and strings you already have

-   One keep rule was eating 47% of cold start
-   Jetpack XR beta renames `AnchorEntity` to `AnchorSpace`
-   Sign in with Apple moves to `private.icloud.com`
-   Agent memory is a dose, not a switch
-   ADK evaluates voice agents with a simulated user

---

### App Size & Startup

*   **Tinder cut cold starts 47% by removing a single keep rule — R8 Configuration Analyzer ships**
    -   One internal library carried `-keep public class * { public protected *; }`, which excluded roughly 70% of the app's code from optimization.
    -   After the cleanup the app shrank from 86.6MB to 61.5MB and dex files dropped from 17 to 11.
    -   On AGP 9.3+ the report is generated automatically at `build/outputs/mapping/release/configanalyzer.html`.
    [Source URL](https://android-developers.googleblog.com/2026/08/tinder-app-cold-start-r8-configuration-analyzer.html) (Android Developers)
    > Takeaway: Run `./gradlew :app:analyzeReleaseR8Config` once and start from the optimization score.

---

### Android XR

*   **Three Jetpack XR SDK core libraries hit beta — `AnchorEntity` is renamed to `AnchorSpace`**
    -   SceneCore, ARCore for Jetpack XR, and XR Runtime are all at 1.0.0-beta02, with Compose for XR following at 1.0.0-alpha17.
    -   `ActivitySpace` and `AnchorSpace` now both extend a common `SpaceEntity`.
    -   `Session.create` became a suspend function, so coroutine call sites need updating.
    [Source URL](https://android-developers.googleblog.com/2026/08/jetpack-xr-sdk-core-libraries-beta.html) (Android Developers)
    > Takeaway: If you have alpha-era XR code, fix the class rename and the `Session.create` signature first.

---

### Apple Identity

*   **Sign in with Apple private relay addresses move to `private.icloud.com`**
    -   Only newly issued addresses use the new domain; existing `privaterelay.appleid.com` addresses keep working.
    -   iCloud+ Hide My Email addresses stay on `icloud.com`.
    -   The transition is announced for later in 2026.
    [Source URL](https://developer.apple.com/news/?id=1ptvdtcm) (Apple Developer News)
    > Takeaway: If you have an email domain allowlist or validation logic, widen it to accept both domains now.

---

### Agent Memory

*   **Agent memory measured across AppWorld's 585 tasks — the right dose depends on model size**
    -   ALTK-Evolve extracts guidelines from execution trajectories and re-injects them at inference time with no weight updates.
    -   gpt-oss-120b gained +16.1pp TGC from curated retrieval alone, at only 5% more tokens.
    -   DeepSeek-V3.2 gained +9.5pp TGC and +16.1pp SGC from the full guideline set, while GLM-5 showed no measurable gain.
    [Source URL](https://huggingface.co/blog/ibm-research/altk-evolve-hmm) (Hugging Face / IBM Research)
    > Takeaway: When adding memory to an agent, compare curated retrieval per model tier instead of injecting everything.

---

### Agent Evaluation

*   **ADK adds a path to evaluate live and voice agents against a simulated user**
    -   Setting `user_simulator_config` to the `llm_audio` type puts a turn-taking LLM plus Gemini TTS in the user's seat.
    -   The `rubric_based_multi_turn_trajectory_quality_v1` metric scores natural-language rubrics with an LLM judge.
    -   Personas such as `NOVICE` drive improvised conversations, or you can replay a fixed scripted one.
    [Source URL](https://developers.googleblog.com/en/how-to-evaluate-live-voice-agents-in-adk/) (Google Developers Blog)
    > Takeaway: If you regression-test voice flows by placing calls by hand, move those scenarios into `adk eval`.

---

Rather than adding features, today's items ask you to re-examine the keep rules, class names, domain strings, and context volume you already have.
