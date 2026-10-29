---
layout: post
title: "Agent Skills Foundation Move, Anthropic Scion, Swift 6.4 (2026. 10. 29)"
description: "Agent Skills moves to a foundation, Anthropic replaces git with Scion, and Swift 6.4 and App Review changes land."
date: 2026-10-29 08:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## Today's Thread: The Specs Behind Agents and Builds Are Changing

-   Agent Skills moves under the Linux Foundation
-   Anthropic moves its monorepo from git to Scion
-   Swift 6.4: SwiftPM defaults to Swift Build
-   App Review adds 2.5.19, reworks 3.1.1(a)

---

### Agent Tooling

*   **Agent Skills standard moves to the Agentic AI Foundation — name, logo, and GitHub org included**
    -   A skill is a folder holding `SKILL.md` plus scripts and reference files, and more than 70 agent platforms have integrated it.
    -   There are 1 million published skills and about 280 million installs (vendor-reported).
    -   The roadmap lists versioned releases, a formal proposal process, and security guidance for writing and installing skills.
    [Source URL](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation) (Anthropic)
    > Takeaway: If you author skills, use the agentskills.io spec as your baseline and watch for a versioning policy.

---

### Source Control for Agents

*   **Anthropic moves its monorepo from git to Scion — git became the bottleneck at agent scale**
    -   Daily merged changes grew from about 2,500 in May 2026 to over 30,000 in September, and CI runs about 25 million checkouts a day (vendor-reported).
    -   The server-centric, changeset-based design cut infrastructure CPU and memory about 200x versus the old git mirrors (vendor-reported).
    -   The authors say it is not a general git replacement and suggest git platforms adopt server-side RPCs and sparse features.
    [Source URL](https://www.anthropic.com/research/redesigning-source-control) (Anthropic)
    > Takeaway: No action needed right now.

---

### Swift Toolchain

*   **Swift 6.4 released — SwiftPM now defaults to Swift Build**
    -   SwiftPM emits SBOMs (SE-0509) in SPDX and CycloneDX, and `defer` blocks can now use `await` (SE-0493).
    -   The Android SDK is built with NDK r30 (LTS), and SwiftPM supports Android without a post-install script.
    -   JavaScriptKit bridging on Wasm is up to 40x faster (vendor-reported).
    [Source URL](https://swift.org/blog/swift-6.4-released/) (Swift.org)
    > Takeaway: If CI builds Swift packages, confirm the output is unchanged after the switch to Swift Build.

---

### App Store Policy

*   **App Review Guidelines updated — hidden-features rule splits out as 2.5.19 and 3.1.1(a) is reworked**
    -   The new 2.5.19 carries the hidden, dormant, or undocumented features policy previously in 2.3.1.
    -   3.1.1(a) drops the Music Streaming Services Entitlements bullet and folds it into the StoreKit External Purchase Link Entitlements bullet.
    -   2.3.14 is a new guideline covering creative assets.
    [Source URL](https://developer.apple.com/news/?id=92th7e5i) (Apple Developer News)
    > Takeaway: If you use external purchase links or a music streaming entitlement, check the 3.1.1(a) changes before your next submission.
