---
title: "Compose 1.13, Google Play Foldable Quality Rules, MoE Expert Streaming (2026. 11. 19)"
description: "Compose 1.13 is stable, Play requires foldable quality from April 2027, and Transformers tries SSD expert streaming."
date: 2026-11-19 08:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## Today's Threads: MoE Expert Streaming, curl Rust Rewrites, Compose 1.13, Play Foldable Rules

-   180B MoE running on a 32GB Mac
-   Rust rewrites of curl and vulnerability stats
-   Compose 1.13 stable, ConstraintLayout deprecated
-   Play requires foldable quality from April 2027

---

### AI Engineering

*   **Hugging Face runs a 180B MoE on a 32GB Mac by streaming experts from SSD**
    -   Only router-selected experts are read from SSD into a 12 GiB cache, and experts are quantized to 3-bit.
    -   Qwen3.8-Flash-Next (180B) decodes at 13.9 tok/s on an M5 MacBook with a 25.4 GiB peak.
    -   Transformers PR #50717 adds an `experts_offload` option to `from_pretrained`.
    [Source URL](https://huggingface.co/blog/moe-expert-streaming) (Hugging Face Blog)
    > Takeaway: It is still a PR, so only check whether expert-level offload could work for large on-device MoE.

*   **curl's maintainer comments on AI-agent Rust rewrites of curl — curl merged 300+ commits in three weeks**
    -   Agents turned about 185,000 lines of C into about 340,000 lines of Rust, while curl took roughly 200 bugfixes.
    -   Of 81 confirmed vulnerabilities this year, 14 (17.3%) would likely have been avoided in a memory-safe language.
    [Source URL](https://daniel.haxx.se/blog/2026/11/17/actual-curl-rewrites-in-rust/) (daniel.haxx.se)
    > Takeaway: If you consider an agent port, weigh the cost of tracking upstream fixes before the language switch.

---

### Android Compose

*   **Jetpack Compose 1.13 is stable — BOM 2026.11.01, needs Kotlin 2.2 and compileSdk 37.1**
    -   `computedStateOf` is added as a lighter alternative to `derivedStateOf` for condition checks.
    -   `FlexBox` and `Grid` are stable, and `constraintlayout-compose` is deprecated.
    -   `material3-a2ui:1.0.0-alpha02` renders A2UI messages as Compose components.
    [Source URL](https://developer.android.com/blog/posts/jetpack-compose-november-2026-release.md.txt) (Android Developers Blog)
    > Takeaway: Before upgrading, check where you use `ConstraintLayout` and `Modifier.onFocusedBoundsChanged`.

*   **Google Play requires foldable quality from April 2027 — apps that miss it cannot publish or update**
    -   Apps must meet adaptive app quality Tier 3 and add 3 foldable screenshots on top of 2 phone screenshots.
    -   From August 2027, new and updated apps must target API 37 (Android 17).
    [Source URL](https://developer.android.com/blog/posts/google-play-adaptive-quality-standards.md.txt) (Android Developers Blog)
    > Takeaway: Test state preservation across rotation and fold/unfold on a foldable emulator.

---

All four ask you to check how far existing tools and rules protect you before adopting the new thing.
