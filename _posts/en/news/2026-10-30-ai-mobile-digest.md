---
layout: post
title: "Agent Skills Moves to AAIF, Swift 6.4, and Apple's 27 SDK Deadline (2026. 10. 30)"
description: "The Agent Skills standard moves to AAIF, and Swift 6.4 plus Apple's 2027 SDK and certificate deadlines are set."
date: 2026-10-30 08:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## Today's thread: Agent Skills standard handoff, Swift 6.4, Apple SDK deadline

-   Agent Skills standard moves to AAIF
-   Anthropic's three-tier access model for external evaluators
-   Swift 6.4 makes Swift Build the SwiftPM default
-   Apple requires 27 SDK uploads from April 2027

---

### Agent Tooling

*   **The Agent Skills standard moves to the Agentic AI Foundation — Anthropic also donates the name and domain**
    -   The folder-based standard built around `SKILL.md` is now stewarded by AAIF under the Linux Foundation, with versioned releases and security guidance on the roadmap.
    -   More than 70 agent platforms have integrated it, with about 1 million published skills and about 280 million installs.
    [Source URL](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation) (Anthropic)
    > Takeaway: Keep internal skills conformant with the `SKILL.md` format and watch how the agentskills.io spec settles its versioning policy.

---

### Evals

*   **Anthropic organizes external evaluator access into three tiers — METR gets employee-level access**
    -   Tier 1 results need Anthropic's approval to publish; Tiers 2 and 3 publish without approval, with only designated categories subject to redaction.
    -   Six METR staff use internal hardware and tools, but customer data and model architecture details are not shared.
    [Source URL](https://www.anthropic.com/news/an-update-on-independent-evaluators) (Anthropic)
    > Takeaway: When reading a vendor safety report, check which tier the evaluation falls under first.

---

### Swift Toolchain

*   **Swift 6.4 ships — Swift Build becomes the default build system in SwiftPM**
    -   Adds `withTaskCancellationShield` (SE-0504) and allows async calls inside `defer` (SE-0493).
    -   The Android SDK is built on NDK r30 LTS, and SwiftPM can generate SPDX and CycloneDX SBOMs (SE-0509).
    [Source URL](https://www.swift.org/blog/swift-6.4-released/) (Swift.org)
    > Takeaway: If CI builds Swift packages, first confirm the output is unchanged after the switch to Swift Build.

---

### Apple Platform Deadlines

*   **Apple allows only 27 SDK builds for upload from April 2027 — the Developer ID Sub-CA also expires in February 2027**
    -   iOS 27 SDK family builds can be submitted now, and from April 2027 uploads must be built with the 27 SDKs.
    -   The original Developer ID Certification Authority (Sub-CA) expires on February 1, 2027, so affected certificates must be replaced.
    [Source URL](https://developer.apple.com/news/) (Apple Developer News)
    > Takeaway: Schedule the Xcode 27 pipeline move and the Developer ID certificate replacement before February 2027.

---

All four items point the same way: check your pipeline's formats and schedules before the standards or deadlines change.
