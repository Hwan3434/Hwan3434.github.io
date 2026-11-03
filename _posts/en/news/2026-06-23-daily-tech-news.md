---
title: "AI Agents, LLM Optimization, and the Evolution of Open Source (2026. 06. 23)"
description: "Google's Jules coding agent and cross-language agent teams with ADK and A2A, running GLM-5.2 locally with Unsloth, OpenAI's Daybreak security tools, Flutter's AI coffee shop, and es-toolkit's growth."
date: 2026-06-23 09:30:48 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## Developer Talk: AI Agents, LLM Optimization, and the Evolution of Open Source (June 23, 2026)

Hello, developers! For June 23, 2026, here is tech news developers shouldn't miss, from the evolution of AI agents and optimizing LLMs to run locally to news from the open-source ecosystem.

---

### AI Agent Development: Toward Collaboration and Autonomy

AI agents are moving quickly beyond simple assistance toward performing complex work autonomously and cooperating with each other. Recent news from Google and Naver shows how.

*   **The AI Coding Agent "Jules": Driving the Development Cycle**
    AI coding agents are evolving from responding to prompts toward understanding multiple stages of software development and leading work on their own. Google's "Jules" focuses on managing complex development workflows effectively by setting long-term goals and priorities, opening the possibility of using AI as a core collaborator on a project rather than just a tool.
    [https://developers.googleblog.com/measuring-what-matters-with-jules/](https://developers.googleblog.com/measuring-what-matters-with-jules/) (Google Developers Blog)

*   **Google ADK and the A2A Protocol: Cross-Language Agent Teams**
    Google's Agent Development Kit (ADK) and Agent-to-Agent (A2A) protocol are changing how AI agents work together. Concrete examples show agents written in different languages, such as Python and Go, cooperating over A2A to solve tasks like complex contract compliance. A2A is designed so agents can delegate tasks securely, avoid context pollution, and collaborate flexibly without the constraints of traditional APIs. Real applications presented for its first anniversary, such as "FoldRun," an agent interface for the life sciences, offer important insight into designing distributed AI systems.
    [https://developers.googleblog.com/build-cross-language-multi-agent-team-with-google-agent-development-kit-and-a2a/](https://developers.googleblog.com/build-cross-language-multi-agent-team-with-google-agent-development-kit-and-a2a/) (Google Developers Blog)
    [https://developers.googleblog.com/how-a2a-is-building-a-world-of-collaborative-agents/](https://developers.googleblog.com/how-a2a-is-building-a-world-of-collaborative-agents/) (Google Developers Blog)

*   **Naver D2: Building a Unified Context Provider for People and AI Agents**
    To stop AI agents from "saying off-the-wall things," Naver built a unified context provider that automatically collects and serves the team's data and serving-layer assets. The platform focuses on giving agents accurate, timely context to maximize efficiency. The talk offers deep insight into why context management matters in agent development and how to implement it.
    [https://d2.naver.com/helloworld/7056385](https://d2.naver.com/helloworld/7056385) (Naver D2)

---

### LLM Technology and AI Security: The Front Line of Research and Practice

Optimizing large language models and using AI to strengthen cybersecurity bring new opportunities and challenges for developers.

*   **Unsloth GLM-5.2: Optimizing LLMs to Run Locally**
    The Unsloth team published documentation on running the GLM-5.2 model efficiently on a local machine. Unsloth is known for speeding up LLM fine-tuning and inference. The guide reduces memory use and increases speed, which is useful for developers who want to use LLMs effectively with limited GPU resources or on a local PC.
    [https://unsloth.ai/docs/models/glm-5.2](https://unsloth.ai/docs/models/glm-5.2) (Unsloth)

*   **OpenAI's Daybreak Initiative and Strategies for Using Codex**
    OpenAI introduced AI-based security tools under a new initiative called "Daybreak." "Codex Security" and "GPT-5.5-Cyber" detect, verify, and patch software vulnerabilities in organizations, and "Patch the Planet" focuses on helping fix security vulnerabilities in open-source projects. Through Jason Liu's case, it also presents "Codex-maxxing," a technique for keeping context and managing work in long, complex projects with Codex. It shows AI extending developers' capabilities beyond coding assistance into security and complex project management.
    [https://openai.com/index/daybreak-securing-the-world](https://openai.com/index/daybreak-securing-the-world) (OpenAI Blog)
    [https://openai.com/index/patch-the-planet](https://openai.com/index/patch-the-planet) (OpenAI Blog)
    [https://openai.com/index/codex-maxxing-long-running-work](https://openai.com/index/codex-maxxing-long-running-work) (OpenAI Blog)

---

### Frontend and Open Source: Real Applications and the Power of Growth

Frontend technology and the open-source ecosystem keep innovating and inspiring developers.

*   **How the Flutter Team Built an AI Coffee Shop**
    The Flutter team shared an interesting demo of a working coffee shop kiosk system built with AI. It explains the technical implementation of a Flutter app connected to AI that handles orders and user interaction, a good reference for Flutter's flexibility and for how AI and mobile/web frontend technology can combine successfully in a real commercial setting.
    [https://blog.flutter.dev/how-we-built-a-flutter-powered-ai-coffee-shop-878c60a11f1a?source=rss----4da7dfd21a33---4](https://blog.flutter.dev/how-we-built-a-flutter-powered-ai-coffee-shop-878c60a11f1a?source=rss----4da7dfd21a33---4) (Flutter Blog)

*   **Toss Tech: The Worldwide Growth of `es-toolkit`**
    Toss shared how `es-toolkit`, a small utility function library started inside the company, grew into an open-source library used around the world. It offers practical experience and insight on developing and maintaining a library, including internal development culture, the open-source contribution process, and interaction with the community, and can inspire developers who want to start and grow an open-source project.
    [https://toss.tech/article/50761](https://toss.tech/article/50761) (Toss Tech Blog)
