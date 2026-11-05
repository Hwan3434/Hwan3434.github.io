---
title: "AppFunctions 1.0 RC, Navigation3 1.2.1, Phonon TTS, Cosmos 3 (2026. 11. 06)"
description: "AppFunctions 1.0.0-rc01 and Navigation3 1.2.1 shipped, plus the 65MB on-device TTS Phonon and NVIDIA's Cosmos 3 Nano models."
date: 2026-11-06 08:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## Today's threads: AppFunctions RC, a Navigation3 patch, on-device speech, world-simulation models

-   AppFunctions 1.0.0-rc01 released
-   Navigation3 1.2.1 drops back to compileSdk 36
-   Phonon TTS: offline speech synthesis in 65MB on phones
-   Four new NVIDIA Cosmos 3 Nano models

---

### Android Jetpack

*   **AppFunctions 1.0.0-rc01 — the API that exposes app features to AI assistants reaches RC**
    -   It arrives two weeks after beta01 and removes the legacy aggregation compiler option.
    -   beta01 moved `AppFunctionName` to the `androidx.appfunctions` package and renamed `AppFunctionAppMetadata.description` to `instructions`.
    [Source URL](https://developer.android.com/jetpack/androidx/releases/appfunctions) (Android Developers)
    > Takeaway: Names changed since alpha and beta, so check imports and metadata attributes before moving to the RC.

*   **Navigation3 1.2.1 — compileSdk goes back from 37 to 36**
    -   Version 1.2 depends on Compose 1.10, which does not require compileSdk 37.
    -   1.3.0-alpha04 fixes a shared `NavEntry` not rendering when it is popped and pushed again before the pop completes.
    [Source URL](https://developer.android.com/jetpack/androidx/releases/navigation3) (Android Developers)
    > Takeaway: If you raised compileSdk to 37 for 1.2.0, you can lower it to 36 with 1.2.1.

---

### On-Device & Open Models

*   **Phonon TTS — 65–75MB models run on phones and browsers with no server**
    -   Phonon 31M is English-only, 40M covers English, French, German, Spanish and Portuguese, and both ship 100+ built-in voices.
    -   On the CPU streaming benchmark, p95 time-to-first-audio is 28ms for 31M EN, 38ms for 40M EN and 165ms for Pocket TTS. (vendor-reported)
    -   Only 31M is Apache 2.0; the others are CC BY-NC.
    [Source URL](https://huggingface.co/blog/phonon-tts) (Hugging Face)
    > Takeaway: To ship it in an app, start by testing the commercially usable 31M English model.

*   **NVIDIA Cosmos 3 Nano follow-ups, four models — for driving and robot world simulation**
    -   Transfer-Auto handles up to 11 camera views, and Sim-Auto handles synchronized camera and LiDAR observations.
    -   The streaming variant generates each chunk in four denoising steps after distillation stage 2, under the OpenMDW1.1 license.
    -   Running them needs Linux, an NVIDIA GPU and Docker; the vLLM-Omni setup was verified on a single GB200.
    [Source URL](https://huggingface.co/blog/nvidia/cosmos-interactive-world-simulation) (Hugging Face)
    > Takeaway: No immediate action needed.

---

Today's items all sit on the shift of app capabilities and models toward user devices and agents.
