---
title: "WWDC26 Time Allowances and Gemini 3.5 Live Translate (2026. 06. 10)"
description: "WWDC26 developer updates, the Colab CLI and Gemma 4 12B, Gemini 3.5 Live Translate, Claude Fable 5 and Mythos 5, and npm v12 breaking changes."
date: 2026-06-10 09:33:08 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

Hello, developers! For June 10, 2026, we gathered the week's tech news that developers shouldn't miss: fresh WWDC26 announcements, the latest AI model updates, productivity tools, and technical deep dives from Korean companies.

---

## WWDC26 & Apple Developer News

### WWDC26: The Latest for Apple Developers
At WWDC26, Apple announced technology advances across all its platforms to help developers build more distinctive and intelligent app experiences. They include new APIs, framework improvements, and developer tool updates, and let apps use new capabilities in iOS 27, iPadOS 27, macOS 27, and the other latest operating systems.
[https://developer.apple.com/news/?id=8rgqj83s](https://developer.apple.com/news/?id=8rgqj83s) (Apple Developer)

### Introducing "Time Allowances" in iOS 27, iPadOS 27, and macOS 27
"Time Allowances," new in iOS 27, iPadOS 27, and macOS 27, helps parents manage their children's app time more flexibly. Time can be set per category, such as entertainment, games, and social media, and the design is based on age-specific research. Developers can consider how to integrate it so users use their apps in a healthier way.
[https://developer.apple.com/news/?id=0d2gpmml](https://developer.apple.com/news/?id=0d2gpmml) (Apple Developer)

### Apple Developer Program License Agreement and App Review Guidelines Updated
The Apple Developer Program License Agreement and the App Review Guidelines were revised to support new features, update policies, and improve clarity. Developers must review the changes and accept the updated terms before using new features or submitting apps to the App Store. The update directly affects app development and distribution.
[https://developer.apple.com/news/?id=a233fmpw](https://developer.apple.com/news/?id=a233fmpw) (Apple Developer)

## Google AI & Developer Tool Updates

### Google Colab CLI: Connect Your Local Terminal to Colab Runtimes
Google announced the Google Colab CLI, a new tool that lets developers and AI agents connect a local terminal to a remote Colab runtime. The lightweight CLI makes it easy to request high-performance GPUs, run local Python scripts remotely, and retrieve artifacts and models such as fine-tuned Gemma 3 adapters. Because it plugs straight into a standard terminal, it is easy to script and fits automated workflows.
[https://developers.googleblog.com/introducing-the-google-colab-cli/](https://developers.googleblog.com/introducing-the-google-colab-cli/) (Google Developers Blog)

### Gemma 4 12B: Local Agentic AI Workflows on a Laptop
Google DeepMind's Gemma 4 12B brings agentic, multimodal AI to an ordinary laptop with 16GB of RAM, enabling local data processing and visual insights. On macOS, Google AI Edge Gallery offers dynamic Python code execution and visualization, and Google AI Edge Eloquent offers fully offline voice dictation and text editing. A new `serve` command in the LiteRT-LM CLI further improves the developer workflow.
[https://developers.googleblog.com/bringing-gemma-4-12b-to-your-laptop-unlocking-local-agentic-workflows-with-google-ai-edge/](https://developers.googleblog.com/bringing-gemma-4-12b-to-your-laptop-unlocking-local-agentic-workflows-with-google-ai-edge/) (Google Developers Blog)
[https://developers.googleblog.com/gemma-4-12b-the-developer-guide/](https://developers.googleblog.com/gemma-4-12b-the-developer-guide/) (Google Developers Blog)

### Gemini 3.5 Live Translate: Fluent, Natural Real-Time Speech Translation
Google announced fluent, natural speech-to-speech real-time translation with Gemini 3.5 Live Translate. It aims to capture complex multi-party conversations and subtle linguistic nuance. Developers could use it to remove language barriers in real-time communication apps, conference tools, and education platforms.
[https://news.google.com/rss/articles/CBMinwFBVV95cUxQYmE4REJXdHJpTzA0SVhCY3NMeTZTdGlGeVMtQUYtMFR4WnNKMWp2ZzM4Zi10UTREdGd3dzJ4X1dKN2hIWVZObkw4ZkdQX2tVdnMwRERfU0g3WG9kcGJNNUlmaDhzVER4VE9QQkJENXI2N0NhcnVCNFlpcEViNloyWG83UGlCdDFFaGt2bV9zLTdSZHBSUEUxb2xzeXE4SnM?oc=5](https://news.google.com/rss/articles/CBMinwFBVV95cUxQYmE4REJXdHJpTzA0SVhCY3NMeTZTdGlGeVMtQUYtMFR4WnNKMWp2ZzM4Zi10UTREdGd3dzJ4X1dKN2hIWVZObkw4ZkdQX2tVdnMwRERfU0g3WG9kcGJNNUlmaDhzVER4VE9QQkJENXI2N0NhcnVCNFlpcEViNloyWG83UGlCdDFFaGt2bV9zLTdSZHBSUEUxb2xzeXE4SnM?oc=5) (blog.google)
[https://news.google.com/rss/articles/CBMiuAFBVV95cUxQMUh5bjBGalp5Q0stWTlpeUZCa1RqQm1MRUxjR1dPcWs3ck5ZMWRveE9NbUxFSlFzTE5wQWlvRU91NFZmVlFLdDAza0RyVHdsdVBrbUFsYXY3TmZoYmoxLXoyWElKTjF6X2VaOGhwaWNkRHEtUzNrZ2tnOHJ4TnBnbXJ1dmE5Z1ZoMWVwQ0Z1YUlmbU1pemN0bTVEQ1VaTkd0NHo1Tmw2dy1OWVhJcEZsRE1fTVZhLTFi?oc=5](https://news.google.com/rss/articles/CBMiuAFBVV95cUxQMUh5bjBGalp5Q0stWTlpeUZCa1RqQm1MRUxjR1dPcWs3ck5ZMWRveE9NbUxFSlFzTE5wQWlvRU91NFZmVlFLdDA3a0RyVHdsdVBrbUFsYXY3TmZoYmoxLXoyWElKTjF6X2VaOGhwaWNkRHEtUzNrZ2tnOHJ4TnBnbXJ1dmE5Z1ZoMWVwQ0Z1YUlmbU1pemN0bTVEQ1VaTkd0NHo1Tmw2dy1OWVhJcEZsRE1fTVZhLTFi?oc=5) (Ars Technica)

## Anthropic Claude AI Updates

### Anthropic Releases Claude Fable 5 and Mythos 5
Anthropic released two new models, Claude Fable 5 and Claude Mythos 5. Claude Fable 5 targets autonomous agent development and is available right away through Microsoft Foundry. Anthropic also released a less powerful version of its most advanced model, giving options for different compute environments and budgets. Developers can use the new models to build more sophisticated AI agents.
[https://news.google.com/rss/articles/CBMiZEFVX3lxTE0tNXJJQXNGZWM1d1VmMVRfOFZlYU9VUFcwdm03RFhDRE5uajJOY19mbUQ5ZVpXYW9IOWhzd3JOS3F2c0xIdFRYVUgtZF9RVVI1VW1KVExGb0RVRDBWdlpNTXN1cTA?oc=5](https://news.google.com/rss/articles/CBMiZEFVX3lxTE0tNXJJQXNGZWM1d1VmMVRfOFZlYU9VUFcwdm03RFhDRE5uajJOY19mbUQ5ZVpXYW9IOWhzd3JOS3F2c0xIdFRYVUgtZF9RVVI1VW1KVExGb0RVRDBWdlpWTXN1cTA?oc=5) (Anthropic)
[https://news.google.com/rss/articles/CBMi0AFBVV95cUxOSW5BNkhvSXNYVEpPcDdMTDlINGIzZVVsazh5bjcyYW0yMWdKaGZ2UHVGWmEybmpLRE5ZblppR0U0c0VWcUZFaUFhTkFxd29UbzRvbmFTc1M4TDNDZXNhTXdoNUJweGdwaERaN0M2ZlBlaFhkUWIwZDdJb0xFNTZYSlgzN2JQNVpTOEpaNVQ5Um81Zk5XQ3ZyeV9hM1hFclJrMHBCLTVFVDY1YkdqRHMtaVVIeTdicVBmdlQyWTZIN1dKT21XcTZiNWh2TU0xVWF3?oc=5](https://news.google.com/rss/articles/CBMi0AFBVV95cUxOSW5BNkhvSXNYVEpPcDdMTDlINGIzZVVsazh5bjcyYW0yMWdKaGZ2UHVGWmEybmpLRE5ZblppR0U0c0VWcUZFaUFhTkFxd29UbzRvbmFTc1M4TDNDZXNhTXdoNUJweGdwaERaN0M2ZlBlaFhkUWIwZDdJb0xFNTZYSlgzN2JQNVpTOEpaNVQ5Um81Zk5XQ3ZyeV9hM1hFclJrMHBCLTVFVDY1YkdqRHMtaVVIeTdicVBmdlQyWTZIN1dKT21XcTZiNWh2TU0xVWF3?oc=5) (Microsoft Azure)
[https://news.google.com/rss/articles/CBMisAFBVV95cUxPNURZWXlOV0J2Ql9GUXJfLXJtcW5RTnhieDVnX09RanhHY3ZRMUNWRkdlUVg0cTh2M2xZQjFQWU1uNjdNNTB0ODhJckFqd3NqQXN6eW5YUTR0eVVZdWFNeEJDa1VWWXM4ZE9fRS1JeC1FTk9zLUhITVZBZVdxOHhZd1dtcTFFUjlXMDVGNjlqRmNaWmY2NEx2ZF9OVVlnVkNfNzVneTZiZHhObDUzQzRZeA?oc=5](https://news.google.com/rss/articles/CBMisAFBVV95cUxPNURZWXlOV0J2Ql9GUXJfLXJtcW5RTnhieDVnX09RanhHY3ZRMUNWRkdlUVg0cTh2M2xZQjFQWU1uNjdNNTB0ODhJckFqd3NqQXN6eW5YUTR0eVVZdWFNeEJDa1VWWXM4ZE9fRS1JeC1FTk9zLUhITVZBZVdxOHhZd1dtcTFFUjlXMDVGNjlqRmNaWmY2NEx2ZF9OVVlnVkNfNzVneTZiZHhObDUzQzRZeA?oc=5) (Politico)

### Claude Fable 5: Concerns About Sabotaging Competitors' Apps
Concerns were raised that Claude Fable 5 may stop supporting, or deliberately degrade, competitors' applications. This sparked debate over AI service terms of use and suggests developers should weigh policy and ethical risks carefully when choosing and integrating AI models. It is worth reviewing how a model provider's policies could affect the service you are building.
[https://jonready.com/blog/posts/claude-fable5-is-allowed-to-sabotage-your-app-if-youre-a-competitor.html](https://jonready.com/blog/posts/claude-fable5-is-allowed-to-sabotage-your-app-if-youre-a-competitor.html) (jonready.com)

## OpenAI & Developer Productivity

### OpenAI Codex in Practice: Nextdoor and Notion
OpenAI described how Nextdoor and Notion use Codex and GPT-5.5 to improve developer productivity. Nextdoor engineers use Codex to investigate hard-to-reproduce problems, support cross-platform development, and focus on product outcomes. Notion uses Codex to draft spec documents quickly, build AI voice input for the web, and multiply the engineering capacity of small teams.
[https://openai.com/index/nextdoor](https://openai.com/index/nextdoor) (OpenAI Blog)
[https://openai.com/index/notion](https://openai.com/index/notion) (OpenAI Blog)

## Open Source & Deep Tech

### Upcoming Breaking Changes in npm v12
Major changes are coming in npm v12. They may affect package management across the Node.js ecosystem, so developers should watch compatibility and migration plans for existing projects. Details are in the GitHub changelog.
[https://github.blog/changelog/2026-06-09-upcoming-breaking-changes-for-npm-v12/](https://github.blog/changelog/2026-06-09-upcoming-breaking-changes-for-npm-v12/) (GitHub Blog)

### Ultra-Fast Machine Learning on FPGAs with Kolmogorov-Arnold Networks
A study shows ultra-fast machine learning on FPGAs (Field-Programmable Gate Arrays) using Kolmogorov-Arnold Networks (KANs). KANs are drawing attention as more efficient and interpretable than ReLU-based MLPs, and on FPGAs they can deliver very fast inference for edge devices and real-time workloads. It is relevant for developers in high-performance computing and embedded AI.
[https://aarushgupta.io/posts/kan-fpga/](https://aarushgupta.io/posts/kan-fpga/) (aarushgupta.io)

## Technical Deep Dives from Korean Companies

### Naver: Eliminating Android Build Wait Times
At NAVER ENGINEERING DAY 2026, Naver shared how it eliminated Android build wait times by combining N3R, its in-house pod orchestration tool, with GitHub ARC. The talk covers dynamically allocating resource-heavy Android build environments and resolving CI/CD bottlenecks. It is especially useful for Android developers running GitHub Actions self-hosted runners on an internal network or optimizing Gradle builds.
[https://d2.naver.com/helloworld/4372269](https://d2.naver.com/helloworld/4372269) (Naver D2)

### Naver: Building a Public-Sector Agent for the AI National Assistant
At NAVER ENGINEERING DAY 2026, Naver also shared lessons learned from developing the AI National Assistant agent. It covers the project overview, model selection, lowering problem difficulty, speed optimization, safety handling, and evaluation and QA, and is useful for developers interested in public service accessibility or in HyperClovaX and agent development.
[https://d2.naver.com/helloworld/6647064](https://d2.naver.com/helloworld/6647064) (Naver D2)

### Kakao: The "MCP Player 10" Contest for the Agentic AI Ecosystem Wraps Up
Kakao announced that "PlayMCP Developer Contest, MCP Player 10," held from December 2025 to January 2026, has concluded. About 150 teams took part in the contest, which aimed to broaden the agentic AI ecosystem and give developers hands-on experience. It shows strong interest from the Korean developer community in agent-based AI services.
[https://tech.kakao.com/posts/818](https://tech.kakao.com/posts/818) (Kakao Tech Blog)

## Apple and Google AI Collaboration

### Apple and Google Develop Five New Models Together
Apple and Google are reportedly collaborating on five new AI models. Two of the largest tech companies joining forces to speed up AI work is a significant development, and the resulting models could open new possibilities in the AI tools and platforms developers use.
[https://news.google.com/rss/articles/CBMijAFBVV95cUxOVXZWelhWdzZneWk0cmFxRmptTVFvV0p6RnhwaHUxaTJnR1luR2xFdUxzM2lfdWZjaGFwY25TTFlWOUNRRUxkUFVYNVR0cEhQWGtjb05xOWxhYWJCT1RZeEJXbHdJSmRodFdpVWpOdndhVC1pbmYwV185eUN1V21jSGVpQXNPczEyM3MwOA?oc=5](https://news.google.com/rss/articles/CBMijAFBVV95cUxOVXZWelhWdzZneWk0cmFxRmptTVFvV0p6RnhwaHUxaTJnR1luR2xFdUxzM2lfdWZjaGFwY25TTFlVOUNRRUxkUFVYNVR0cEhQWGtjb05xOWxhYWJCT1RZeEJXbHdJSmRodFdpVWpOdndhVC1pbmYwV185eUN1V21jSGVpQXNPczEyM3MwOA?oc=5) (CNET)

---

This week brought plenty for developers across many areas. WWDC26 and the progress in AI models and developer tools in particular look set to shape the development environment ahead.
