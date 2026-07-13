---
layout: post
title: "Daily Tech News - 2026-07-14"
date: 2026-07-14 06:00:15 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## Today's Developer News: AI Security Analysis, Agent Harnesses, and Open-Source Tools

Here is a developer-focused digest for July 14, 2026, covering App Store submission requirements, static-analysis security rules, AI coding-agent operations, and open-source productivity tools. Stock-market, earnings, executive, and broad business news has been excluded.

---

### Platforms and Application Security

*   **Apple adds social-media questions to the App Store Connect age-rating questionnaire**
    Apple added questions asking whether an app can redistribute, amplify, or interact with user-generated content through a social feed or similar discovery mechanism. Apps with those capabilities will show a new Social Media content descriptor, while capabilities disabled for users under 13 will not place those users in the Social Media Time Allowance category. Developers can answer now, and responses become mandatory in September 2026 for new apps, updates, and notarization submissions for alternative distribution, so submission documentation and review checklists should be updated in advance.
    [Source URL](https://developer.apple.com/news/?id=tlur8uvi) (Apple Developer)

*   **CodeQL 2.26.0 adds JavaScript and TypeScript system-prompt injection detection**
    GitHub added the `js/system-prompt-injection` query to CodeQL 2.26.0 to find paths where untrusted user input flows into an AI model's system prompt. The release expands prompt-sink modeling for OpenAI, Anthropic, and Google GenAI SDKs and improves support for Kotlin 2.4.0, C# Razor Pages, Go `log/slog`, and Swift CryptoKit. GitHub.com code scanning receives the update automatically, but older GitHub Enterprise Server installations must upgrade CodeQL manually to use the new detection.
    [Source URL](https://github.blog/changelog/2026-07-10-codeql-2-26-0-adds-kotlin-2-4-0-support-and-ai-prompt-injection-detection/) (GitHub Changelog)

---

### Operating AI Coding Agents

*   **Martin Fowler highlights context focus and validation sensors as the core of agent harnesses**
    Drawing on discussions at the Future of Software Development Retreat, Martin Fowler argues that a large context window matters less than helping a model focus on the right information through compact context and files such as `AGENTS.md`. On the validation side, participants emphasized computational sensors including property-based testing and formal methods; they also observed that harnesses can reduce token usage and make weaker or self-hosted models practical. As teams delegate larger units of work to agents, explicit acceptance criteria and automated validation boundaries should come before additional instructions.
    [Source URL](https://martinfowler.com/fragments/2026-07-13.html) (Martin Fowler)

---

### Open-Source Developer Tools

*   **Logseq ships the first public beta of its 2.0.1 database version**
    Logseq released the first 2.0 database-version beta for desktop and Android after a long development cycle. The project labels it an early beta, recommends backing up important data before testing, and links to its roadmap for operating the existing and database versions separately. Developers maintaining plugins or automated workflows should test data compatibility and extension behavior against a separate backup before moving a production graph.
    [Source URL](https://github.com/logseq/logseq/releases/tag/2.0.1) (Logseq)

*   **`dom-docx` converts semantic HTML into editable native OOXML documents**
    The MIT-licensed TypeScript project `dom-docx`, which drew attention on Hacker News, converts HTML fragments into native Word paragraphs, lists, tables, and images instead of screenshots or 1×1 layout tables. Its default inline-style path runs as pure JavaScript in Node.js and browsers, while computed styles and complex charts can opt into Playwright and rasterization. The current v0.1.x does not support CSS grid, web fonts, complex SVG, or guaranteed multi-page layout fidelity, so adopters should evaluate its supported subset and regression-scoring harness before using it for document exports.
    [Source URL](https://github.com/floodtide/dom-docx) (GitHub Repository)

---

Today's theme is a shift from merely adding AI features to controlling and validating their behavior. Data flow into system prompts, agent context and acceptance criteria, beta data migration, and preservation of document structure are all boundaries worth checking automatically before deployment.
