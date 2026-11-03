---
title: "WWDC26 Highlights, Gemini Memory, Simulating Black Holes with Codex (2026. 06. 11)"
description: "WWDC26 updates, DiffusionGemma and Gemma 4 12B, Gemini's new memory feature, Codex for black hole simulations, a 16GB Raspberry Pi 5, and Korean tech blog posts."
date: 2026-06-11 09:34:52 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## Key Tech News for Developers, June 11, 2026

Hello! For June 11, 2026, we picked recent tech news that is interesting and useful from a purely technical point of view: AI progress, platform updates, new developer tools and open-source projects, and in-depth posts from Korean tech companies.

---

### Apple Developer Updates: WWDC26 Highlights

At WWDC26, Apple shared new features across its platforms and improvements to the developer experience, including important changes coming in iOS 27, iPadOS 27, and macOS 27.

*   **The latest advances across Apple platforms**
    WWDC26 summarizes the latest advances on every Apple platform. The focus is on new APIs, frameworks, and improvements to existing features that help developers build more distinctive and intelligent app experiences.
    [https://developer.apple.com/news/?id=8rgqj83s](https://developer.apple.com/news/?id=8rgqj83s) (Apple Developer News)

*   **"Time Allowances" in iOS 27, iPadOS 27, and macOS 27**
    iOS 27, iPadOS 27, and macOS 27 introduce "Time Allowances," which lets parents manage their children's app time flexibly. It can be set per category, such as entertainment, games, and social media, with recommended settings for each age. Developers should consider how to integrate parental controls or improve the user experience around it.
    [https://developer.apple.com/news/?id=0d2gpmml](https://developer.apple.com/news/?id=0d2gpmml) (Apple Developer News)

*   **Apple Developer Program License Agreement and App Review Guidelines updated**
    The Apple Developer Program License Agreement and the App Review Guidelines were revised to support new features, reflect updated policies, and clarify wording. All developers must review and accept the new terms, a required step for developing and submitting apps.
    [https://developer.apple.com/news/?id=a233fmpw](https://developer.apple.com/news/?id=a233fmpw) (Apple Developer News)

---

### Google AI and Developer Tools

Google announced news ranging from a new AI model architecture to tools that change development workflows.

*   **DiffusionGemma: A Guide to Diffusion-Based Parallel Generation**
    DiffusionGemma is an experimental text generation model based on the Gemma 4 architecture. Instead of autoregressive token-by-token generation, it uses diffusion-based parallel generation, which allows much faster inference, bidirectional context awareness, and real-time self-correction. Generating and refining 256-token blocks in parallel makes it more efficient on tasks with complex constraints, such as Sudoku. It can also be deployed on consumer GPUs.
    [https://developers.googleblog.com/diffusiongemma-the-developer-guide/](https://developers.googleblog.com/diffusiongemma-the-developer-guide/) (Google Developers Blog)

*   **Gemma 4 12B on Your Laptop: Local, Agentic Workflows with Google AI Edge**
    Google DeepMind's Gemma 4 12B brings agentic and multimodal AI to an ordinary laptop with 16GB of RAM. On macOS, Google AI Edge Gallery offers dynamic Python code execution and visualization, and Google AI Edge Eloquent offers fully offline voice dictation and text editing. A new `serve` command in the LiteRT-LM CLI strengthens the developer workflow, opening new possibilities for AI development and data processing on local machines.
    [https://developers.googleblog.com/bringing-gemma-4-12b-to-your-laptop-unlocking-local-agentic-workflows-with-google-ai-edge/](https://developers.googleblog.com/bringing-gemma-4-12b-to-your-laptop-unlocking-local-agentic-workflows-with-google-ai-edge/) (Google Developers Blog)

*   **Introducing the Google Colab CLI**
    Google announced the Google Colab Command-Line Interface (CLI), a new tool that connects a local terminal to a remote Colab runtime. With this lightweight CLI you can request high-performance GPUs, run local Python scripts remotely, and retrieve artifact logs or models such as fine-tuned Gemma 3 adapters. It integrates directly with a standard terminal, is scriptable, and should raise productivity for AI developers.
    [https://developers.googleblog.com/introducing-the-google-colab-cli/](https://developers.googleblog.com/introducing-the-google-colab-cli/) (Google Developers Blog)

*   **Google Gemini's New "Memory" Feature**
    The Google Gemini chatbot gained a "memory" feature that remembers the context of past conversations and user preferences, so interactions become more consistent and personalized over time. It improves long-term context management, a core element of agentic AI, and is an important step toward smarter AI agents.
    [https://news.google.com/rss/articles/CBMiggFBVV95cUxOd1RFYmdSaVBNY0h0ZFU2MUU5eDBQSlZvdDVMaS1SSVhHUmdfY3lqNW1taUxpdmM0d1U2a1hvbHFHSlFiM09fUzgzcWtfYkljN0g0eEowbExRZ0NzSUtKVE9CdGZOWTh2Z09vZEUwME04dENyT25WMTRRa1VpREJ6ZEtR0gGWAUFVX3lxTFBwUXZKNG83aHN2SUNKMkxTZnJmRVFaSXhNUzNVeUtrcTlyUl9RT0ZNOWphVjJZWmZzWkdLVVV0cWVUd1VfZnpfR3NpeHRHbjNHQXNjQ3ZIc3NnQ2pzQzVtclJ0MjJmTTNrTHhqS0Z2N2Vfb2xuaHhzX0YyVG1oYmQtR0RadDhjOGQxcEhic1lTeDZfY3FzZw?oc=5](https://news.google.com/rss/articles/CBMiggFBVV95cUxOd1RFYmdSaVBNY0h0ZFU2MUU5eDBQSlZvdDVMaS1SSVhHUmdfY3lqNW1taUxpdmM0d1U2a1hvbHFHSlFiM09fUzgzcWtfYkljN0g0eEowbExRZ0NzSUtKVE9CdGZOWTh2Z09vZEUwME04dENyT25WMTRRa1VpREJ6ZEtR0gGWAUFVX3lxTFBwUXZKNG83aHN2SUNKMkxTZnJmRVFaSXhNUzNVeUtrcTlyUl9RT0ZNOWphVjJZWmZzWkdLVVV0cWVUd1VfZnpfR3NpeHRHbjNHQXNjQ3ZIc3NnQ2pzQzVtclJ0MjJmTTNrTHhqS0Z2N2Vfb2xuaHhzX0YyVG1oYmQtR0RadDhjOGQxcEhic1lTeDZfY3FzZw?oc=5) (WRDW)

---

### OpenAI and Applied AI

OpenAI shared use cases for its models and an expansion of its enterprise offering.

*   **An Astrophysicist Simulates Black Holes with Codex**
    OpenAI described how astrophysicist Chi-kwan Chan uses Codex to build black hole simulations that help scientists study extreme physics and test Einstein's general relativity. It is a notable example of AI code generation and understanding contributing to real problems in complex scientific research.
    [https://openai.com/index/using-codex-to-simulate-black-holes](https://openai.com/index/using-codex-to-simulate-black-holes) (OpenAI)

*   **OpenAI Models and Codex on Oracle Cloud**
    OpenAI models and Codex are now available through Oracle Cloud. Companies can use their existing cloud commitments to build and deploy AI with enterprise-grade security and governance, which makes it easier for Oracle Cloud customers to adopt OpenAI's technology.
    [https://openai.com/index/openai-on-oracle-cloud](https://openai.com/index/openai-on-oracle-cloud) (OpenAI)

---

### Open Source and Hardware

A few open-source projects and hardware updates are worth a look.

*   **The πFS Open-Source Project**
    A new open-source file system project called πFS was published in the GitHub repository `philipl/pifs`. File systems are one of the core interfaces between an operating system and hardware, and a new one can suggest different approaches to data management or performance. It is especially interesting for developers into low-level systems programming or embedded systems.
    [https://github.com/philipl/pifs](https://github.com/philipl/pifs) (GitHub)

*   **Raspberry Pi 5 with 16GB of RAM**
    A 16GB RAM model of the Raspberry Pi 5 single-board computer is out. It makes the Pi 5 more viable for memory-hungry projects, such as running larger AI models locally, complex server applications, or a lightweight desktop replacement. Good news for embedded and IoT developers and hobbyists.
    [https://www.adafruit.com/product/6125?src=raspberrypi](https://www.adafruit.com/product/6125?src=raspberrypi) (Adafruit)

---

### Korean Tech Blogs and Development Experience

Major Korean tech companies also shared in-depth articles and development experience.

*   **Naver D2: AI National Assistant, Building a Public-Sector Agent**
    Naver shared lessons learned from developing its "AI National Assistant" agent. It covers the whole process of building a public service agent in detail, including choosing a HyperClovaX model, adjusting problem difficulty, speed optimization, safety handling, and building evaluation and QA, which makes it practical for developers working with HyperClovaX or agents.
    [https://d2.naver.com/helloworld/6647064](https://d2.naver.com/helloworld/6647064) (네이버 D2)

*   **Kakao Tech: MCP Player 10 Wraps Up, and What's Next**
    Kakao announced the successful close of "PlayMCP Developer Contest, MCP Player 10," held to broaden the agentic AI ecosystem. About 150 teams took part, showing strong interest from the developer community, and Kakao appears set to keep applying agentic AI to real services and growing the ecosystem.
    [https://tech.kakao.com/posts/818](https://tech.kakao.com/posts/818) (카카오 테크)

*   **Toss Tech Blog: The History of Face Recognition and the Future of FacePay**
    Toss published a look back at 60 years of face recognition technology and, building on it, the future of its FacePay technology. It covers the development of computer vision and biometrics in depth and explains the potential and importance of face recognition in financial services. Useful for developers interested where AI meets security.
    [https://toss.tech/article/history-of-face-recognition-facepay](https://toss.tech/article/history-of-face-recognition-facepay) (토스 기술 블로그)

*   **Naver D2: Preventing Unintended Changes in Android Apps**
    Naver explains how to detect and block unintended changes caused by external library updates when developing Android apps and libraries. It shares concrete experience building a defense based on "Manifest Shield" and baselines, offering practical ways to improve build stability for Android developers who track dependencies and manage AndroidManifest files.
    [https://d2.naver.com/helloworld/3431313](https://d2.naver.com/helloworld/3431313) (네이버 D2)

*   **Naver D2: Eliminating Android Build Wait Times**
    Naver shared how it reduced Android build wait times, a long-standing pain point. By combining its in-house pod orchestration tool N3R with GitHub ARC, it dynamically allocates resource-heavy Android build environments and resolves CI/CD bottlenecks. Useful for Android developers interested in Gradle build caching and multi-module optimization.
    [https://d2.naver.com/helloworld/4372269](https://d2.naver.com/helloworld/4372269) (네이버 D2)

*   **Toss Tech Blog: Designing a Rubric and Building a System for Skill Quality**
    Toss shared how it designed a rubric to minimize quality variation between "Skills" and turned it into a system. It is an important method for keeping service quality consistent and developing and managing Skills efficiently in a complex system, and a good reference for developers interested in quality management, system design, and architecture.
    [https://toss.tech/article/skill-quality-rubric](https://toss.tech/article/skill-quality-rubric) (토스 기술 블로그)

*   **Toss Tech Blog: How Do TAMs Solve Problems in a Fast-Moving Organization?**
    Technical Account Managers (TAMs) from Toss and Kakao Pay met to share how they solve and coordinate technical problems in fast-changing organizations. It highlights the TAM's role in closing the gap between developers, customers, and the business, and offers insight on growing skills beyond pure technology and having more impact inside an organization.
    [https://toss.tech/article/tam-connect-2025](https://toss.tech/article/tam-connect-2025) (토스 기술 블로그)

---

Today again brought interesting technical progress and in-depth development experience across many areas.
