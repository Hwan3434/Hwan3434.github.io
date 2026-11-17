---
title: "GPT-6.2 Astra and Sol, Flutter A2UI 1.0, R8 Consumer Keep Rules (2026. 11. 18)"
description: "GPT-6.2 Astra and Sol pricing is out, Flutter shipped A2UI 1.0, and Android published R8 keep rule guidance for library authors."
date: 2026-11-18 08:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## Today's Threads: GPT-6.2 Astra and Sol, Coding-Agent Sandboxes, Flutter A2UI 1.0, R8 Consumer Keep Rules

-   GPT-6.2 Astra $8/$40, Sol $2/$10
-   Three external sandboxes for coding agents
-   llm 0.37.3 fixes logging on SQLite 3.54.1
-   Flutter A2UI 1.0 and a2ui_flutter
-   R8: narrowing library consumer keep rules

---

### AI Engineering

*   **OpenAI launches GPT-6.2 Astra and Sol — Astra is 20% cheaper than GPT-6 Astra**
    -   Astra costs $8/$40 per 1M input/output tokens, with cached input at $0.40.
    -   Sol is $2/$10, the same as GPT-6.1 Sol and half of GPT-5.6 Sol ($4/$20).
    -   llm 0.38 supports both models.
    [Source URL](https://simonwillison.net/2026/Nov/17/gpt62-astra-and-sol/) (Simon Willison)
    > Takeaway: If you make many repeated calls, recalculate costs with the lower cached input price ($1 to $0.40).

*   **Running coding agents outside the sandbox — three servers share one localhost API**
    -   `external-sandbox-v86`, `external-sandbox-container`, and `external-sandbox-quicksand` run Alpine Linux via WebAssembly, Apple Containers, and QEMU.
    -   An HTTP/HTTPS allow-list proxy limits reachable hosts, and authenticated calls work without handing secrets to the agent.
    [Source URL](https://simonwillison.net/2026/Nov/17/external-sandboxes-for-coding-agents/) (Simon Willison)
    > Takeaway: When a local model executes code, run it behind a sandbox and an allow-list rather than on the host.

*   **llm 0.37.3 — fixes logging broken by Homebrew's SQLite 3.54.1**
    -   `select json_object('a', (select json_array(1)))` returns `{"a":[1]}` on 3.54.0 but `{"a":"[1]"}` on 3.54.1.
    -   Per the docs a subquery returns SQL text rather than JSON, and wrapping it in `json()` fixes it.
    [Source URL](https://simonwillison.net/2026/Nov/16/llm/) (Simon Willison)
    > Takeaway: If you pass subquery results into `json_object`, wrap them in `json()`.

---

### Flutter GenUI

*   **Flutter ships A2UI 1.0 and `a2ui_flutter` — formerly `genui`**
    -   `MessageProcessor` replaces `SurfaceController` and `Conversation`, and transport is no longer part of the package.
    -   Setting `allowedParents`/`allowedChildren` in a catalog returns `UNALLOWED_PARENT` or `UNALLOWED_CHILD` on violations, and one surface can use several catalogs.
    -   `callAgentFunction` lets a widget call a backend function without an LLM turn.
    [Source URL](https://flutter.dev/blog/a2ui-launch) (Flutter Blog)
    > Takeaway: If you use `genui`, check the migration scope against `MessageProcessor`.

---

### Android Optimization

*   **Android publishes R8 consumer keep rule guidance for library providers — broad rules block app-level DEX optimization**
    -   Package-wide rules like `-keep public class com.google.android.gms.** { *; }` override an app's narrower rules.
    -   Prefer codegen over reflection, keep only entry points when reflection is unavoidable, and use conditional keep rules for ad adapters.
    -   The Android CLI `analyze` command and R8 Configuration Analyzer show which classes are kept.
    [Source URL](https://developer.android.com/blog/posts/ship-smarter-keep-rules-unblock-dex-optimization.md.txt) (Android Developers Blog)
    > Takeaway: If you ship an SDK, find package-wide keeps in your consumer rules and narrow them to entry points.

---

All of today's items are about how narrowly the environment around an agent or a library is scoped.
