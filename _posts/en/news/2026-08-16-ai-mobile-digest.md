---
layout: post
title: "AI & Mobile Digest - 2026-08-16"
date: 2026-08-16 06:20:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## Today's threads: pre-generating and caching UI, dated mobile migrations, and where small models actually get used

-   Pre-generate A2UI messages and cache them in Firestore
-   Flutter 3.47 moves Material and Cupertino out of the SDK
-   Media3 1.11 adds PlayerPool for short-form feeds
-   Korean App Store ratings can be overridden with a GRAC RCN
-   Claude text watermarking, for models shipped after Aug 2
-   Models under 1B account for 83% of all downloads

---

### Generative UI

*   **Flutter genui — pre-generate A2UI instead of producing it at request time, then cache it**
    -   A2UI, which `genui` renders, is JSON messages, so it can be stored in Firestore and reused as-is.
    -   A Cloud Function generates them ahead of time with `gemini-3.1-flash-lite`, and app startup only reads the DB.
    [Source URL](https://flutter.dev/blog/speeding-up-generative-ui-with-async-a2ui) (The Flutter Blog)
    > Takeaway: Take the LLM call off the app startup path and split the generation phase from the consumption phase.

---

### Flutter Toolchain

*   **Flutter 3.47 — Material and Cupertino split out of the SDK, and the iOS minimum moves to 15**
    -   They become `material_ui` and `cupertino_ui` 1.0, with the in-SDK libraries formally deprecated in November.
    -   `dart fix --apply --code=migrate_design_widgets` rewrites the imports automatically.
    -   Minimums rise to iOS 15 and macOS 12, and Impeller becomes the default on macOS, Windows, and Linux.
    [Source URL](https://flutter.dev/blog/whats-new-in-flutter-3-47) (The Flutter Blog)
    > Takeaway: If you publish a package, cut this migration as a major version and use `MaterialUiCompatibilityBridge` to cover the transition.

---

### Android Media

*   **Media3 1.11 — player recycling APIs for short-form feeds and a changed session security default**
    -   `PlayerPool` in `common-ktx` and `rememberPooledPlayer` in `ui-compose` recycle player instances across a feed.
    -   Session data is no longer shared with untrusted controllers by default.
    -   A new `media3-datasource-ktor` module lets you swap the HTTP stack for Ktor.
    [Source URL](https://android-developers.googleblog.com/2026/08/media3-1-11-whats-new.html) (Android Developers Blog)
    > Takeaway: If your short-form screens build a new player every time, start by listing the call sites to move to `rememberPooledPlayer`.

---

### App Store Policy

*   **Korean App Store age ratings — override with a GRAC classification number, and two descriptors move to 12+ in October**
    -   Games and Entertainment apps can submit a GRAC RCN with the next version to override the rating to All/12+/15+/19+.
    -   From October, infrequent profanity and crude humor, and infrequent mature or suggestive themes, move from All to 12+.
    [Source URL](https://developer.apple.com/news/?id=oj3r9pvw) (Apple Developer News)
    > Takeaway: If your app declares those descriptors, check whether its rating rises before October and prepare an RCN if needed.

---

### AI Provenance

*   **Anthropic explains how Claude's text watermark works — applied to models launched after August 2**
    -   It replaces the randomness source in word selection with the key plus the preceding words, following DeepMind's SynthID-Text.
    -   The signal is sparse in short passages, in factual text that forces exact terms, and in heavily human-edited output.
    -   No detection API exists yet; one is only announced as coming.
    [Source URL](https://www.anthropic.com/news/claude-text-watermark) (Anthropic)
    > Takeaway: If you plan to use the watermark as a verification signal, design around the fact that it effectively does not work on short outputs.

---

### Open Models

*   **Hugging Face's open-model review — attention goes to the large models, downloads go to sub-1B**
    -   Models under 1B account for 83% of all-time downloads; those above 100B account for 1%.
    -   Qwen GGUF conversions pull 39.6M downloads a month, roughly twice Gemma's 20.8M.
    -   Among agents hitting the Hub, Claude Code was 44.4% of July traffic.
    [Source URL](https://huggingface.co/blog/state-of-open-models-summer-2026) (Hugging Face)
    > Takeaway: When shortlisting on-device candidates, start from the small models where GGUF downloads actually cluster rather than the top of a leaderboard.

---

Today's mobile items put the real cost not in new features but in migrations with dates attached — the November Material and Cupertino deprecation, and the October Korean rating reclassification.
