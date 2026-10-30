---
layout: post
title: "Anthropic Scion Source Control, App Review Guidelines Update, iPhone Duo (2026. 10. 31)"
description: "Anthropic details Scion, its git replacement, while Apple updates App Review Guidelines and announces iPhone Duo screenshot rules."
date: 2026-10-31 08:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## Today's threads: agent-scale source control, Claude in the lab, Apple review rule changes

-   Anthropic replaces git with in-house VCS Scion
-   Claude cuts pharma doc review 25h to 3h (vendor-reported)
-   App Review Guidelines revised, new 2.5.19
-   iPhone Duo screenshots required from April 2027
-   Swift ecosystem: Vapor 5 beta, SE-0554 in review

---

### Agent Infrastructure

*   **Anthropic moved its monorepo from git to an in-house VCS, Scion — agent-scale merges were the bottleneck**
    -   Daily merges grew from about 2,500 in May 2026 to over 30,000 by September, with about 25 million CI checkouts per day.
    -   A server-side design with three cache tiers cut CPU and memory about 200x versus the old git mirrors (vendor-reported).
    [Source URL](https://www.anthropic.com/research/redesigning-source-control) (Anthropic)
    > Takeaway: This is overkill for most teams, but watch whether shallow and sparse clones hit their limits first as agents drive up CI checkouts.

*   **Anthropic published Claude use cases from drug development — document review and design proposals lead**
    -   On 1,061 pages of manufacturing documents, Enveda's Claude setup caught all 11 issues humans found plus 7 more, cutting review from over 25 hours to under 3 (vendor-reported).
    -   Most of the work is preclinical, and Claude's role in clinical trials is not yet defined.
    [Source URL](https://www.anthropic.com/research/early-progress-drug-development) (Anthropic)
    > Takeaway: No action needed right now.

---

### App Store Policy

*   **Apple revised the App Review Guidelines — hidden features moved to 2.5.19 and AI-generated imagery is now explicit**
    -   2.5.19 covers hidden or undocumented features; bait-and-switch apps can be removed and their developers dropped from the Program.
    -   1.2 names nonconsensual intimate imagery, including AI-generated, under content moderation, and 3.1.1(a) merges the Music Streaming Services entitlement into the StoreKit External Purchase Link Entitlement.
    [Source URL](https://developer.apple.com/news/) (Apple Developer News)
    > Takeaway: Before submitting, check for remotely toggled features or undocumented debug code left in the app.

*   **iPhone Duo ships October 23 — screenshots required for submissions from April 2027**
    -   It runs iOS 27.1, Xcode 27.1 supports development, and Device Hub previews behavior across poses and orientations.
    [Source URL](https://developer.apple.com/news/) (Apple Developer News)
    > Takeaway: Use Device Hub in Xcode 27.1 to check that your layouts handle pose changes.

---

### Swift Ecosystem

*   **Swift ecosystem after 6.4 — Vapor 5 beta and the SE-0554 review stand out**
    -   The Vapor 5 beta is a full rewrite that removes `EventLoopFuture` in favor of structured concurrency.
    -   SE-0554, now in review, proposes `#if deploymentTargetAtLeast(...)` to select imports and declarations by minimum deployment target.
    [Source URL](https://www.swift.org/blog/) (Swift.org)
    > Takeaway: If you run Swift server code, estimate the async migration scope now for moving from Vapor 4 to 5.

---

All five items show existing tools and practices hitting their limits first when scale or rules change.
