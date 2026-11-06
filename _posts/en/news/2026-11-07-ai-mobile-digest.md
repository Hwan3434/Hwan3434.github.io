---
layout: post
title: "Anthropic Agent Memory Dreaming, Siri AI Developer Preview, Subscription Retention Messages (2026. 11. 07)"
description: "Anthropic details agent memory experiments, and Apple ships a Siri AI developer preview and subscription retention messages."
date: 2026-11-07 08:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## Today's threads: agent memory design, LLMs reading weights, Siri AI and subscription retention

-   Agent memory with dreaming lifts benchmark scores
-   GPT-6 Astra weight-reading claim, tested on local Qwen
-   Siri AI developer preview via App Intents
-   Retention messages added to the cancellation flow

---

### Agent Memory

*   **Anthropic lays out the components of agent memory — an offline pass called dreaming is the key**
    -   On the CL-Bench 1.0 database task, Opus 5.5's mean reward rose from 0.655 to 0.838 with memory.
    -   A fixed "record only failures" rule hurt results; Opus 5 dropped by 0.234.
    -   Claude Code auto memory loads only the first 200 lines or 25 KB of `MEMORY.md`.
    [Source URL](https://www.anthropic.com/research/components-of-agent-memory) (Anthropic)
    > Takeaway: When adding memory to an agent, tell it what memory is for rather than how to use it, and keep always-loaded files short.

*   **A paper claims a model can infer a network's training goal from raw weights — Simon Willison tests it on local Qwen 3.8 27B**
    -   The paper says GPT-6 Astra edited 0.016% of Qwen3.5-0.8B's weights and lifted MATH-500 from 7.9% to 48.1%.
    -   With a Q4_K_M GGUF (about 17 GB) in LM Studio, Breakout took 52 minutes and Pong 1 hour 5 minutes; Freeway was wrong.
    -   Critics say the paper mixes a no-tools reading test with a tool-assisted editing test.
    [Source URL](https://simonwillison.net/2026/Nov/3/qwen-can-interpret-model-weights/) (Simon Willison)
    > Takeaway: No action needed.

---

### Apple Platform

*   **Siri AI opens to all developers — integrate through App Intents in the 27.3 betas**
    -   New skills let you chain several actions for complex requests, and any entity in the Spotlight semantic index can surface.
    -   It is unavailable in the EU on iOS, iPadOS, and watchOS, and App Store submission opens in spring 2027.
    -   Server-side Apple Intelligence features have daily usage limits.
    [Source URL](https://developer.apple.com/news/?id=gdk2umrf) (Apple Developer News)
    > Takeaway: Expose your app's core features as `App Intents` entities and check Siri AI behavior on the 27.3 betas.

*   **Retention messages added to the subscription cancellation flow — configured in App Store Connect**
    -   Messages can carry text, images, or a special offer, with eligibility and spacing set per subscription.
    -   The Retention Messaging API is by request and picks a message based on subscription details.
    [Source URL](https://developer.apple.com/news/?id=fk9ps3gv) (Apple Developer News)
    > Takeaway: If you sell auto-renewable subscriptions, try the setting in App Store Connect and request API access if you need server-side control.

---

All four items move the design of what an agent remembers, reads, and calls onto the developer.
