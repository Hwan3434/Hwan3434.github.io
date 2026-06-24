---
layout: post
title: "Daily Tech News - 2026-06-25"
date: 2026-06-25 06:36:06 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## Today's Developer News: AI Security Patching, Local Agents, and Platform Changes

Here is a developer-focused digest for June 25, 2026. It focuses on AI security, agent development, APIs, platform changes, and app development, while excluding stock-market, earnings, executive, and broad business news.

---

### AI Security and Open Source Maintenance

*   **OpenAI expands Daybreak and launches Patch the Planet for open-source security fixes**
    OpenAI expanded Daybreak with an updated Codex Security plugin, the limited-release GPT-5.5-Cyber model, a cyber partner program, and Patch the Planet. Patch the Planet is built with Trail of Bits and collaborators including HackerOne and Calif to help maintainers validate vulnerabilities, develop patches, test fixes, and coordinate disclosure for critical open-source projects such as cURL, Go, Python, Sigstore, and pyca/cryptography. For engineering teams, AI security tooling is moving from alert generation toward CI/CD, threat models, patch review, and remediation workflows.
    [Source URL](https://openai.com/index/daybreak-securing-the-world/) (OpenAI)
    [Source URL](https://openai.com/index/patch-the-planet/) (OpenAI)

*   **OpenAI publishes guidance for long-running Codex work**
    OpenAI published a Codex-maxxing guide for using Codex as a persistent workspace rather than a single-prompt tool. The guidance focuses on breaking ambitious goals into verifiable steps, maintaining continuity across workstreams, and deciding when human oversight is most valuable. Teams adopting agentic development should treat task decomposition, validation, and review loops as first-class engineering work.
    [Source URL](https://openai.com/index/codex-maxxing-long-running-work/) (OpenAI)

---

### Agent Development and Local AI

*   **Google Developers shows a Python-Go multi-agent workflow with ADK and A2A**
    Google Developers Blog published an example where a Python agent uses Gemini to extract contract fields and a Go agent performs deterministic compliance checks. The system uses Agent Development Kit's `RemoteA2aAgent` and the Agent2Agent protocol to connect agents written in different languages. The post highlights a production-oriented pattern: replace one giant prompt with specialized agents, explicit failure handling, and deterministic components that can be audited.
    [Source URL](https://developers.googleblog.com/build-cross-language-multi-agent-team-with-google-agent-development-kit-and-a2a/) (Google Developers Blog)

*   **Google AI Edge demonstrates local agentic workflows with Gemma 4 12B**
    Google showed how Gemma 4 12B works with Google AI Edge Gallery, AI Edge Eloquent, and the LiteRT-LM CLI for local agentic workflows on laptops. LiteRT-LM's `serve` command can expose a local OpenAI-compatible endpoint for tools such as Continue, Aider, or internal harnesses. This is relevant for teams exploring local data analysis, voice-driven editing, and code execution where data should stay on-device.
    [Source URL](https://developers.googleblog.com/bringing-gemma-4-12b-to-your-laptop-unlocking-local-agentic-workflows-with-google-ai-edge/) (Google Developers Blog)

*   **Anthropic API notes include retired Claude models and tool-response improvements**
    Anthropic's Claude Platform release notes say `claude-sonnet-4-20250514` and `claude-opus-4-20250514` were retired on June 15 and now return errors. On June 11, Anthropic also updated the code execution tool description to expose the 90-second per-cell limit and added `response_inclusion` support for web search/fetch tools so agentic workflows can drop consumed result blocks from API responses. Claude API users should audit model IDs and tool-result handling.
    [Source URL](https://platform.claude.com/docs/en/release-notes/overview) (Anthropic Claude Platform)

---

### APIs and Platform Changes

*   **Gemini API adds speech streaming and has near-term media model shutdowns**
    Google AI for Developers added speech generation streaming for `gemini-3.1-flash-tts-preview` through `streamGenerateContent` and `stream: true` in the Interactions API. Google also lists shutdown dates for several media generation models: some Veo 2/3 model IDs are scheduled for June 30, 2026, and selected Imagen 4 and Gemini 3 Image models are scheduled for August 17, 2026. Teams using generative media in products should check model IDs, replacements, and rollout timing.
    [Source URL](https://ai.google.dev/gemini-api/docs/changelog) (Google AI for Developers)
    [Source URL](https://ai.google.dev/gemini-api/docs/deprecations) (Google AI for Developers)

*   **Apple posts iOS 27 design kits and Brazil distribution/payment changes**
    Apple Developer published Figma and Sketch design kits for iOS, iPadOS, and macOS 27, including Liquid Glass updates, expanded component states, and macOS Dark Mode support. Apple also announced Brazil-specific iOS changes following an agreement with CADE: beginning with iOS 26.5, developers can use alternative app marketplaces, alternative payment processing, and out-of-app payment offers in Brazil. Global app teams should review both UI resources and region-specific distribution/payment rules.
    [Source URL](https://developer.apple.com/news/) (Apple Developer)
    [Source URL](https://developer.apple.com/news/releases/) (Apple Developer Releases)

---

### App Development and Engineering Practice

*   **Flutter shares a Gemini/Firebase-powered AI coffee shop demo**
    The Flutter team shared an AI coffee shop demo built with Flutter, Firebase, and Gemini. It is presented as an inspirational demo rather than maintained production software, but it is still a useful reference for connecting cross-platform UI with generative AI-backed interactions.
    [Source URL](https://blog.flutter.dev/how-we-built-a-flutter-powered-ai-coffee-shop-878c60a11f1a) (Flutter Blog)

*   **Korean engineering blogs continue documenting AI harness and Skill quality practices**
    Woowahan Tech has been publishing practical AI engineering posts on team-specific coding harnesses with Cursor Rules and Skills, RAG chatbots, and LLM-assisted multilingual product work. Toss Tech shared how it manages coding-agent Skill quality with a six-section, 30-item rubric. The common theme is a shift from model selection toward context management, verification, and maintainable harness design.
    [Source URL](https://techblog.woowahan.com/) (Woowahan Tech)
    [Source URL](https://toss.tech/article/skill-quality-rubric) (Toss Tech)

*   **Hacker News discussions continue around AI dev stacks and mobile app development**
    Hacker News threads continue to discuss AI development stacks/workflows and the state of app development in 2026. These are not product announcements, but they are useful community signals for how developers are combining agentic IDEs, LLM CLIs, test automation, and changing mobile development expectations.
    [Source URL](https://news.ycombinator.com/item?id=48413629) (Hacker News)
    [Source URL](https://news.ycombinator.com/item?id=48337409) (Hacker News)

---

The main theme today is that AI agents are expanding from code-writing assistants into security patching, local execution, cross-language orchestration, and operational developer harnesses. API model shutdowns and platform policy changes can affect production systems, so those integrations deserve an early review.
