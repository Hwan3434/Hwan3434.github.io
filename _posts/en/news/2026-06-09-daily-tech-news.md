---
title: "Apple WWDC26 Developer Updates and Apple AI Built on Gemini (2026. 06. 09)"
description: "WWDC26 brings Time Allowances and new agreements, Apple builds its AI architecture on Gemini, and Google ships the Colab CLI and Gemma 4 12B."
date: 2026-06-09 09:29:30 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## Latest Tech News Summary for Developers, June 9, 2026

From the tech news collected today (June 9, 2026), we picked the items with real technical depth for developers. General economic and stock news is excluded in favor of development technology and AI research.

---

### Apple WWDC26: Key Developer Updates and Platform Changes

At WWDC26, Apple presented the latest advances across all its platforms to help developers build more distinctive and intelligent app experiences. The new "Time Allowances" feature in iOS 27, iPadOS 27, and macOS 27 lets parents manage children's app time flexibly by category, which becomes an important design consideration for apps that integrate or account for parental controls. The Apple Developer Program License Agreement and the App Review Guidelines were also updated to reflect new features and policy changes, so developers must review and accept them. These changes directly affect app development and distribution plans.

*   [https://developer.apple.com/news/?id=8rgqj83s](https://developer.apple.com/news/?id=8rgqj83s) (Apple Developer)
*   [https://developer.apple.com/news/?id=0d2gpmml](https://developer.apple.com/news/?id=0d2gpmml) (Apple Developer)
*   [https://developer.apple.com/news/?id=a233fmpw](https://developer.apple.com/news/?id=a233fmpw) (Apple Developer)

### Apple's New AI Architecture Is Built on Google Gemini

One of the most notable announcements is that Apple built its new AI architecture on Google's Gemini models. It looks like a strategic choice for running on-device AI on Apple hardware. CNET's coverage stresses privacy as a core design principle, suggesting Apple aims to use Gemini while keeping its strict privacy policy. For developers, it opens the possibility of integrating more capable AI features into apps in the Apple ecosystem, and attention now turns to what concrete APIs or frameworks come out of the partnership.

*   [https://www.macrumors.com/2026/06/08/apple-reveals-new-ai-architecture/](https://www.macrumors.com/2026/06/08/apple-reveals-new-ai-architecture/) (MacRumors)
*   [https://news.google.com/rss/articles/CBMijAFBVV95cUxOVXZWelhWdzZneWk0cmFxRmptTVFvV0p6RnhwaHUxaTJnR1luR2xFdUxzM2lfdWZjaGFwY25TTFlWOUNRRUxkUFVYNVR0cEhQWGtjb05xOWxhYWJCT1RZeEJXbHdJSmRodFdpVWpOdndhVC1pbmYwV185eUN1V21jR2VpQXNPczEyM3MwOA?oc=5](https://news.google.com/rss/articles/CBMijAFBVV95cUxOVXZWelhWdzZneWk0cmFxRmptTVFvV0p6RnhwaHUxaTJnR1luR2xFdUxzM2lfdWZjaGFwY25TTFlWOUNRRUxkUFVYNVR0cEhQWGtjb05xOWxhYWJCT1RZeEJXbHdJSmRodFdpVWpOdndhVC1pbmYwV185eUN1V21jR2VpQXNPczEyM3MwOA?oc=5) (CNET)

### Google Strengthens Local AI Development: Colab CLI and Gemma 4 12B

Google announced two tools that change workflows for developers and AI agents. First, the **Google Colab CLI** connects a local terminal to a remote Colab runtime, so you can request high-performance GPUs, run local Python scripts remotely, and retrieve artifacts and models such as fine-tuned Gemma 3 adapters without friction. Bringing AI/ML training and experimentation into the local development environment can raise productivity considerably.

Second, **Gemma 4 12B** is a new dense multimodal model from Google DeepMind, designed to run agentic local AI workflows on an ordinary laptop with 16GB of RAM. Its encoder-free architecture skips the traditional vision and audio encoders and feeds multimodal data directly into the LLM backbone. On macOS, Google AI Edge Gallery provides dynamic Python code execution and visualization, and Google AI Edge Eloquent provides fully offline voice dictation and text editing. A new `serve` command in the LiteRT-LM CLI rounds out the developer workflow. This is an important step for developers who want on-device AI that keeps data private on the local machine.

*   [https://developers.googleblog.com/introducing-the-google-colab-cli/](https://developers.googleblog.com/introducing-the-google-colab-cli/) (Google Developers Blog)
*   [https://developers.googleblog.com/bringing-gemma-4-12b-to-your-laptop-unlocking-local-agentic-workflows-with-google-ai-edge/](https://developers.googleblog.com/bringing-gemma-4-12b-to-your-laptop-unlocking-local-agentic-workflows-with-google-ai-edge/) (Google Developers Blog)
*   [https://developers.googleblog.com/gemma-4-12b-the-developer-guide/](https://developers.googleblog.com/gemma-4-12b-the-developer-guide/) (Google Developers Blog)

### Korean Tech: Building AI Agents and Managing Quality

Korean tech companies also shared useful material. The Toss Tech blog covered **designing a rubric and building a system for Skill quality management**, sharing practical methods and system-building experience for narrowing the growing quality gap between Skills. It is useful for any developer interested in managing service quality systematically.

Naver D2 published the session **"AI National Assistant: Building a Public-Sector Agent,"** which shares lessons learned and know-how from developing an AI agent on Naver's HyperClovaX model. It covers the whole process of agent development, including model selection, tuning problem difficulty, speed optimization, safety handling, and evaluation and QA, and offers practical insight for developers working on public service accessibility or on HyperClovaX agents.

*   [https://toss.tech/article/skill-quality-rubric](https://toss.tech/article/skill-quality-rubric) (Toss Tech)
*   [https://d2.naver.com/helloworld/6647064](https://d2.naver.com/helloworld/6647064) (Naver D2)

### Developer Privacy: Signal's Statement Against UK Surveillance Law

Signal, the privacy-focused messaging app, published a statement (PDF) taking a firm stance against the UK's latest surveillance law. Titled "Surveillance Is Not Safety," it raises concerns about privacy and security being undermined through surveillance. For a service built on end-to-end encryption, laws like this threaten not only the technical implementation but the reason the service exists. Developers should consider how their apps protect user data and how they would respond to potential legal and technical threats.

*   [https://signal.org/blog/pdfs/2026-06-08-uk-surveillance-is-not-safety.pdf](https://signal.org/blog/pdfs/2026-06-08-uk-surveillance-is-not-safety.pdf) (Signal Blog)
