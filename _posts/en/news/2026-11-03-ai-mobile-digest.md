---
layout: post
title: "Agent Skills Moves to AAIF, Swift 6.4, New App Store Age Rating Items (2026. 11. 03)"
description: "Agent Skills moves under the Linux Foundation's AAIF, Swift 6.4 ships, and App Store Connect adds new age rating declarations."
date: 2026-11-03 08:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## Today's threads: a neutral home for an agent standard, outside evaluator access, Swift 6.4 and App Store rules

-   Agent Skills moves to AAIF under the Linux Foundation
-   Six METR staff get access to Anthropic internal systems
-   Swift 6.4 ships; Swift Build becomes the default
-   New age rating items, due January 12, 2027

---

### Agent Ecosystem

*   **Anthropic donates Agent Skills to AAIF — the skills standard becomes vendor-neutral**
    -   A skill is a folder containing `SKILL.md`; 70+ agent platforms support it, with about 280 million installs in total.
    -   The roadmap lists versioned releases, a formal proposal process, and security guidance for skill authors and installers.
    [Source URL](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation) (Anthropic)
    > Takeaway: If you write your own skills, watch whether the format changes once versioning and security guidance land.

*   **Anthropic widens internal access for outside evaluators — six METR staff use internal tools directly**
    -   Access has three tiers; at tier 3, METR can publish without Anthropic's approval, and only confidential categories may be redacted.
    -   SecureBio is reviewing the chemical and biological weapons chapter of the August 2026 Risk Report.
    [Source URL](https://www.anthropic.com/news/an-update-on-independent-evaluators) (Anthropic)
    > Takeaway: No action needed right now.

---

### Swift & App Store

*   **Swift 6.4 ships — Swift Build becomes the default build system in SwiftPM**
    -   `await` now works inside `defer` (SE-0493), and `withTaskCancellationShield` runs cleanup that ignores cancellation (SE-0504).
    -   `@Observable` gets fine-grained change notifications (SE-0506), and SBOMs can be generated in SPDX or CycloneDX (SE-0509).
    -   Android builds use NDK 30.
    [Source URL](https://swift.org/blog/swift-6.4-released/) (Swift.org)
    > Takeaway: After switching to Swift Build, compare your CI's SwiftPM build output once.

*   **App Store Connect adds two age rating items — available from November 16, due January 12, 2027**
    -   The new items are Shared Location and Dating and Relationships; the latter forces a minimum 18+ rating.
    -   In Brazil, they map to A16 and A18 respectively.
    [Source URL](https://developer.apple.com/news/) (Apple Developer News)
    > Takeaway: If your app has location sharing or dating features, fill in the items before January 12, 2027.

---

All four items turn a standard or policy into a checklist developers now have to work through.
