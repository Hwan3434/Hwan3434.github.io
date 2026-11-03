---
title: "Brazil's iOS App Ecosystem, Google's AI Agent Vision, Infrastructure Automation (2026. 06. 21)"
description: "Apple opens Brazil to alternative marketplaces and payments, Google advances A2A, ARD, and A2UI with MCP apps, OpenAI aids rare disease diagnosis, and Toss and Naver share automation work."
date: 2026-06-21 09:32:00 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## Today's Developer Hot Topics: AI Agents, Platform Changes, and Automation (June 21, 2026)

Hello, developers! From today's (June 21, 2026) tech news, here are the items most notable from a developer's point of view, from advances in AI and the spread of agent-based computing to policy changes on major platforms.

---

### Apple Ecosystem: New Ground for Brazil's iOS App Ecosystem

Following an agreement with Brazil's competition authority (CADE), Apple is making important changes to the iOS ecosystem. Starting with iOS 26.5, developers in Brazil can distribute apps on alternative app marketplaces or run their own. They also get the option to process alternative payments for digital goods and services instead of in-app purchase. This creates new business model opportunities and reduces dependence on Apple In-App Purchase. The details are in Attachment 12 of the updated Apple Developer Program License Agreement, which developers targeting Brazil must review and accept.
[https://developer.apple.com/news/?id=umq9wxmm](https://developer.apple.com/news/?id=umq9wxmm) (Apple Developer)
[https://developer.apple.com/news/?id=dhwadr2x](https://developer.apple.com/news/?id=dhwadr2x) (Apple Developer)

### Google Lays Out a Vision for AI Agents and New Architectures

Google announced important progress toward agent-based computing.

*   **One year of the A2A (Agent-to-Agent) protocol:** A2A helps autonomous AI agents collaborate and delegate work securely without the constraints of traditional APIs. Delegating complex workflows to specialized peer agents prevents context pollution, protects data privacy, and simplifies application design through modularity. FoldRun, an agent interface for the life sciences, was presented as an example.
    [https://developers.googleblog.com/how-a2a-is-building-a-world-of-collaborative-agents/](https://developers.googleblog.com/how-a2a-is-building-a-world-of-collaborative-agents/) (Google Developers Blog)
*   **Agentic Resource Discovery (ARD) specification:** ARD is an open specification for finding and verifying tools, skills, and agents across the web. It looks set to become core infrastructure that improves interoperability in the agent ecosystem and helps developers discover and integrate resources agents can use.
    [https://developers.googleblog.com/announcing-the-agentic-resource-discovery-specification/](https://developers.googleblog.com/announcing-the-agentic-resource-discovery-specification/) (Google Developers Blog)
*   **A2UI + MCP Apps: combining declarative and custom agentic UI:** Google introduced three architectural patterns for integrating Model Context Protocol (MCP) apps with Agent-to-User Interface (A2UI), resolving the tradeoff between highly customizable iframe environments and native declarative rendering. With this hybrid framework, developers can serve native-feeling UI from an MCP server, safely embed complex stateful iframe apps in declarative views, or inject generative UI components into legacy systems.
    [https://developers.googleblog.com/a2ui-and-mcp-apps/](https://developers.googleblog.com/a2ui-and-mcp-apps/) (Google Developers Blog)

### OpenAI: Model Improvements and Real Applications

OpenAI is focused on expanding ChatGPT and making it more useful in specific fields.

*   **Better health intelligence in ChatGPT:** GPT-5.5 Instant strengthens ChatGPT's health and wellness responses, with stronger reasoning, better context understanding, clearer communication, and physician evaluation. It should make handling sensitive health information more accurate and trustworthy.
    [https://openai.com/index/improving-health-intelligence-in-chatgpt](https://openai.com/index/improving-health-intelligence-in-chatgpt) (OpenAI Blog)
*   **AI support for diagnosing rare genetic diseases:** Researchers used OpenAI's reasoning model to help diagnose rare diseases. The model identified 18 new diagnoses in previously unsolved cases, demonstrating its potential as a diagnostic aid in medicine.
    [https://openai.com/index/diagnose-rare-childhood-diseases](https://openai.com/index/diagnose-rare-childhood-diseases) (OpenAI Blog)

### Korean Tech Companies: AI and Infrastructure Automation

Major Korean tech companies also shared interesting cases of using AI and improving infrastructure.

*   **Toss design chapter's AI contest:** Toss held an AI contest encouraging designers to create a range of work with AI. It shows that creative work with AI is possible outside engineering roles and helps spread AI tools and new ideas internally.
    [https://toss.tech/article/ai_contest](https://toss.tech/article/ai_contest) (Toss Tech Blog)
*   **Spark Connect on Kubernetes: building a robust Spark Connect (Toss):** Toss shared how it solved problems where sessions piling up or heavy jobs on a Spark Connect server affected other users or crashed the server. Its approach to building a stable, robust Spark Connect server on Kubernetes is practical for developers running large-scale data processing systems.
    [https://toss.tech/article/spark-connect-on-kubernetes-1](https://toss.tech/article/spark-connect-on-kubernetes-1) (Toss Tech Blog)
*   **Change the spec and the prompt follows: an automated pipeline for answer generation models (Naver D2):** For a shopping agent answer model whose input spec changes often, Naver designed and applied a pipeline in which entering the changed spec lets an agent automate defect detection, prompt optimization, and SFT (supervised fine-tuning) data generation in a closed loop. It shows the value of development automation for MLOps efficiency in LLM services and for keeping up with fast-changing business requirements.
    [https://d2.naver.com/helloworld/2852215](https://d2.naver.com/helloworld/2852215) (Naver D2)
