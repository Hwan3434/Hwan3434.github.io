---
layout: post
title: "Daily Tech News - 2026-06-30"
date: 2026-06-30 06:00:21 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## Today's Developer News: Agent Evaluation, Computer Use Models, and Quality Automation

Here is a developer-focused digest for June 30, 2026. It covers AI coding agents, model APIs, agent standards, mobile design resources, testing, and observability, while excluding stock-market, earnings, executive, and broad business news.

---

### AI Models and Coding Agents

*   **OpenAI previews GPT-5.6 Sol**
    OpenAI introduced GPT-5.6 Sol as a next-generation model with stronger coding, science, and cybersecurity capabilities. The preview adds a new `max` reasoning effort and an `ultra` mode that uses subagents to accelerate complex work, and OpenAI says Sol sets a new state of the art on Terminal-Bench 2.1 for command-line workflows. Access and safety review still matter because this is a preview, but the direction is relevant for defensive security review, patch development, and long-running coding tasks.
    [Source URL](https://openai.com/index/previewing-gpt-5-6-sol/) (OpenAI)

*   **Gemini 3.5 Flash integrates computer use as a built-in tool**
    Google added computer use directly to Gemini 3.5 Flash, enabling agents that can see, reason, and act across browser, mobile, and desktop environments. Developers can use it through the Gemini API and Gemini Enterprise Agent Platform, with long-horizon automation and software testing highlighted as target workflows. Google also introduced enterprise safeguards such as explicit confirmation for sensitive or irreversible actions and automatic task stopping when indirect prompt injection is detected.
    [Source URL](https://deepmind.google/blog/introducing-computer-use-in-gemini-3-5-flash/) (Google DeepMind)

*   **Google proposes a way to evaluate proactive coding agents with Jules**
    Google Developers Blog argues that coding agents should be evaluated not only on fixing narrow bugs, but also on their `insight policy`: deciding what matters, what evidence supports it, and when to interrupt a developer. The team built an evaluation from 705 bugs and 1,178 CLs in internal Google codebases, clustering related bug fixes into higher-level goals and measuring the insights generated after a limited exploration budget. Increasing the exploration budget from two rounds to three raised Hit@5 from 33% to 57%, a useful reminder that coding-agent quality depends on exploration cost and interruption policy as well as model accuracy.
    [Source URL](https://developers.googleblog.com/measuring-what-matters-with-jules/) (Google Developers Blog)

---

### Agent Ecosystem and Developer Platforms

*   **Google announces the Agentic Resource Discovery specification**
    Google announced Agentic Resource Discovery (ARD), an open specification for publishing, discovering, and verifying tools, skills, and agents across the web. The core pattern is for organizations to publish catalogs such as `ai-catalog.json` under their own domains, while registries index those catalogs so agents can discover capabilities and verify publisher trust through cryptographic metadata. Because ARD can describe MCP servers, A2A agents, OpenAPI tools, and nested catalogs, teams building agent platforms should evaluate how it fits their internal tool registries and egress policies.
    [Source URL](https://developers.googleblog.com/announcing-the-agentic-resource-discovery-specification/) (Google Developers Blog)

*   **Flutter shows an Antigravity workflow for multiplatform agentic development**
    The Flutter team described a workflow that combines Google Antigravity and Flutter to build apps that can run across platforms from a single agentic development loop. The practical point is that agents are moving beyond code completion into interpreting requirements, implementing changes, running the app, and iterating on feedback, while Flutter's single-codebase model fits that workflow well. Teams adopting this style still need to close the loop with automated tests and real-device checks for generated UI and platform-specific behavior.
    [Source URL](https://blog.flutter.dev/vibe-once-run-anywhere-with-antigravity-and-flutter-25af06e60a91) (Flutter Blog)

*   **Apple publishes design kits for iOS, iPadOS, and macOS 27**
    Apple released Figma and Sketch design kits for iOS, iPadOS, and macOS 27. The kits include Liquid Glass updates, expanded component and state support, naming changes aligned more closely with code, improved resizing, and Dark Mode for macOS. For app teams preparing post-WWDC platform updates, these resources can help align design-system states with SwiftUI implementation details.
    [Source URL](https://developer.apple.com/news/?id=e2lxw9l1) (Apple Developer)

---

### Quality Automation and Observability

*   **Toss Tech shares its QA platform approach to test automation**
    Toss QA Platform team explained how it platformized smoke testing, regression testing, crash monitoring, and hotfix decisions for a weekly app release cadence. Its internal platform, Tossion, moved test-case authoring and execution into a custom workflow; PRCheck analyzes change impact and test priorities; and tcgen drafts test cases from PRDs, design documents, and related context. The useful engineering lesson is that AI can help build and operate testing tools, but humans still need to define what quality means and when the process should change.
    [Source URL](https://toss.tech/article/50893) (Toss Tech)

*   **NAVER D2 publishes an End-to-End RUM session for user monitoring**
    NAVER D2 published a NAVER ENGINEERING DAY 2026 session on nFront RUM, an internal Real User Monitoring service. The session covers End-to-End user monitoring with dashboards and AI reports, designed to expose user-facing reliability and performance signals without extra integration work. For frontend and platform teams, it is a useful case study in connecting real-user latency, errors, and session flow to operational metrics that synthetic monitoring may miss.
    [Source URL](https://d2.naver.com/helloworld/9227131) (NAVER D2)

---

Today's main theme is that as agents become more capable of acting on code and screens, the surrounding operating system has to mature too: evaluation, discovery, permissions, testing, and observability. Model capability alone is not enough; teams need workflow-level decisions about which tools to connect, which actions to block, and how generated results are verified.
