---
layout: post
title: "AI & Mobile Digest - 2026-08-24"
date: 2026-08-24 06:10:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## Today's threads: tighten the contract and the defaults before swapping the model

-   MCP roadmap: sessions gone, HTTP transport unified
-   int4 KV cache breaks tool calls
-   153 autonomous runs close 81.7% of the gap
-   Dart primary constructors trade the class name for `new()`
-   AGP 10 forces the new Variant API; 9.4 has an opt-out

---

### Agent Protocol

*   **MCP roadmap update — server-initiated events and HTTP transport unification move to the top of the list**
    -   The 2026-07-28 spec removed protocol-level sessions and the initialization handshake (SEP-2575, SEP-2567) and added `server/discover`.
    -   Tasks moved out to an official extension (SEP-2663), and list results became cacheable (SEP-2549).
    -   The agent identity track targets DPoP, Workload Identity Federation, and standard token exchange.
    [Source URL](https://blog.modelcontextprotocol.io/posts/mcp-roadmap/) (Model Context Protocol Blog)
    > Takeaway: If your own MCP server leans on session-based initialization, strip that out against the 07-28 spec first.

---

### Inference Serving

*   **A measurement that blames quantization and the attention backend, not the model, for a dumb-feeling local LLM**
    -   NVIDIA NVFP4 drifted to roughly 50% token disagreement at 88k context, while INT8 W8A16 stayed the most stable.
    -   Tool calls failed under an int4 KV cache, recovered under int8, and stayed consistent under BF16.
    -   With everything else equal, a tool call that passed at TP1 and TP4 failed only at TP2.
    [Source URL](https://forum.level1techs.com/t/why-your-local-llm-feels-dumber-than-it-is/253917) (Level1Techs Forum)
    > Takeaway: If self-hosted tool calls keep failing, revert KV cache quantization to BF16 and re-measure before switching models.

---

### Research Agents

*   **18 frontier models turned loose on the nanoGPT speedrun to measure autonomous research — 153 runs total**
    -   Each run got up to 8 days on 8×H200, and the best result of 2,726 steps closed 81.7% of the remaining gap to the human record of 2,600.
    -   The stronger models separated on noise modeling and ablation design, not on how many experiments they ran.
    -   No run produced a fundamentally new method.
    [Source URL](https://www.primeintellect.ai/blog/measuring-autonomous-research) (Prime Intellect)
    > Takeaway: Before handing experiments to an agent, evaluate its ablation and noise judgment rather than its run budget.

---

### Dart Language

*   **The design story behind Dart primary constructors — `new()`/`factory()` instead of repeating the class name**
    -   A constructor that needs a body uses a `this { ... }` block, and a class with no body closes with `;` instead of `{}`.
    -   Declaring parameters are allowed only in primary constructors and were deliberately not opened up to in-body constructors.
    -   Field-based inference was dropped because constructors are the public API users must control explicitly.
    [Source URL](https://dart.dev/blog/bringing-primary-constructors-to-dart) (The Dart Blog)
    > Takeaway: When moving to primary constructors in 3.13, start by checking that the class name in a constructor declaration becomes `new()`.

---

### Android Build

*   **AGP 9.4 preview — the new Variant API becomes mandatory in AGP 10, and only 9.4 offers a per-module opt-out**
    -   Set the exception in `gradle.properties` as `android.newDsl.optOut=:example-lib1`.
    -   A strict 1:1 flavor dimension check between app and dynamic feature modules landed as a warning by default and becomes a build failure in AGP 10.
    -   `android.enforceDynamicFeatureVariantMatching=true` promotes it to an error now so you can see the damage early.
    [Source URL](https://developer.android.com/build/releases/agp-9-4-0-release-notes) (Android Developers)
    > Takeaway: If you ship dynamic features, flip that flag to surface variant mismatches before AGP 10 arrives.

---

Whether it is a spec, a build rule, or a quantization setting, today's items all moved by narrowing contracts and defaults rather than by adding features.
