---
layout: post
title: "Daily Tech News - 2026-06-24"
date: 2026-06-24 21:26:58 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## Today's Developer News: Team AI Agents, Gemini API Changes, and Mobile Platform Updates

Here is a developer-focused digest for June 24, 2026. It focuses on AI agents, APIs, mobile/frontend tooling, and engineering practice, while excluding stock-market, earnings, executive, and broad business news.

---

### AI Agents and Developer Workflows

*   **Anthropic introduces Claude Tag beta for Slack-based team collaboration**
    Anthropic introduced Claude Tag, a way for teams to tag `@Claude` in Slack channels and delegate work. Claude Enterprise and Team customers can grant Claude access to selected channels, tools, data, and codebases so it can build shared context over time. For engineering teams, this is another step from single-user coding assistants toward collaborative agents embedded in day-to-day team workflows.
    [Source URL](https://www.anthropic.com/news/introducing-claude-tag) (Anthropic)

*   **OpenAI expands Codex beyond software development**
    OpenAI says Codex is increasingly used for research, data analysis, workflow automation, and creating documents, spreadsheets, presentations, and lightweight internal tools. A separate Codex update introduced role-specific plugins, Sites, and annotations to make Codex fit more team workflows. Developers may need to review and operate more AI-generated artifacts outside the codebase, not just code changes.
    [Source URL](https://openai.com/index/codex-for-knowledge-work/) (OpenAI)
    [Source URL](https://openai.com/index/codex-for-every-role-tool-workflow/) (OpenAI)

*   **Google Developers highlights ADK, A2A, and multi-agent patterns**
    Google Developers Blog is currently highlighting Agent Development Kit, the A2A protocol, cross-language multi-agent examples, Jules metrics, agentic UI, and resource discovery. The trend is useful for teams designing agents across Python, Go, Android/Kotlin, and cloud environments rather than treating AI tools as isolated scripts.
    [Source URL](https://developers.googleblog.com/) (Google Developers Blog)

---

### APIs and Platform Changes

*   **Gemini API: Interactions API is GA and speech streaming lands**
    Google AI for Developers now lists the Interactions API as generally available and recommends it for access to the latest Gemini models and features. The June 17 release notes also add streaming support for speech generation with `gemini-3.1-flash-tts-preview`. Existing `generateContent` integrations remain supported, but teams planning new Gemini features should evaluate the Interactions API path.
    [Source URL](https://ai.google.dev/gemini-api/docs/changelog) (Google AI for Developers)
    [Source URL](https://ai.google.dev/gemini-api/docs/interactions-overview) (Google AI for Developers)

*   **Gemini image and video model deprecations need migration checks**
    Google announced deprecation schedules for several Imagen 4, Gemini 3 Image, and Veo model IDs. Some Veo model IDs are scheduled for shutdown on June 30, 2026, while selected Imagen 4 and Gemini 3 Image models are scheduled for August 17, 2026. Teams with image or video generation in production should verify model IDs, replacements, and rollout timing.
    [Source URL](https://ai.google.dev/gemini-api/docs/deprecations) (Google AI for Developers)

*   **Apple ships iOS, iPadOS, and macOS 27 design kits plus beta releases**
    Apple Developer published Figma and Sketch design kits for iOS, iPadOS, and macOS 27, including Liquid Glass updates, expanded component and state coverage, naming changes aligned with code, improved resizing, and macOS Dark Mode support. Apple's releases page also lists Xcode 27 beta 2 and iOS/iPadOS/macOS/tvOS/visionOS 27 beta 2, making this a good time for app teams to test SDK and UI changes together.
    [Source URL](https://developer.apple.com/news/) (Apple Developer)
    [Source URL](https://developer.apple.com/news/releases/) (Apple Developer Releases)

---

### App Development and Engineering Practice

*   **Flutter shows a Gemini/Firebase-powered AI coffee shop demo**
    The Flutter team shared how it built an AI coffee shop experience using Flutter, Firebase, and Gemini. The code is presented as an inspirational demo rather than maintained production software, but it is a useful reference for combining cross-platform UI with generative AI-backed interactions.
    [Source URL](https://blog.flutter.dev/how-we-built-a-flutter-powered-ai-coffee-shop-878c60a11f1a) (Flutter Blog)

*   **Toss Tech shares a rubric system for coding-agent Skills**
    Toss Tech described how its AI DX Team designed a six-section, 30-item rubric to improve the quality of internal Skills used by coding agents. Because these Skills are read and invoked by LLMs, traditional compile/test gates are not enough; the post is relevant for teams trying to make agent tooling discoverable, reliable, and useful.
    [Source URL](https://toss.tech/article/skill-quality-rubric) (Toss Tech)

*   **NAVER D2 publishes AI agent experimentation and Playwright E2E harness sessions**
    NAVER D2 published engineering talks about how AI agents experiment with and improve code, plus how to build a Playwright E2E test harness for AI agents. The common theme is closing the loop between generated changes, execution, verification, and feedback.
    [Source URL](https://d2.naver.com/helloworld/8061804) (NAVER D2)
    [Source URL](https://d2.naver.com/helloworld/6811215) (NAVER D2)

*   **Hacker News continues discussing AI development stacks**
    A recent Hacker News thread asks developers what AI development stack and workflow they use. It is not a product announcement, but it is a useful community signal for how practitioners are combining agentic IDEs, LLM CLIs, test/review automation, and local models.
    [Source URL](https://news.ycombinator.com/item?id=48413629) (Hacker News)

---

The main theme today is that agents are moving from individual coding assistance into team collaboration, API design, test harnesses, and internal tool quality. API deprecations and beta SDKs can affect production systems, so those integrations deserve an early review.
