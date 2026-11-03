---
title: "Apple Deprecates ImageCreator, OpenAI Acquires Ona, Claude Corps (2026. 06. 12)"
description: "Apple ends ImageCreator support in iOS 27, Google publishes the DiffusionGemma guide, OpenAI plans to acquire Ona for Codex, and Naver shares LLM serving and Android build talks."
date: 2026-06-12 09:34:33 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## Today's Tech News for Developers (June 12, 2026)

From the tech news collected today (June 12, 2026), we picked the items most interesting to developers: key updates on Google I/O, WWDC, Flutter, open source, and AI technology and model research.

---

### Apple to Drop Support for the ImageCreator Class

Apple announced that the `ImageCreator` class for on-device image generation will no longer be supported starting with iOS 27, iPadOS 27, macOS 27, and visionOS 27. Introduced alongside the `Image Playground` framework, the class let apps use the on-device image generation model programmatically. Developers using it may see degraded behavior starting with the upcoming beta releases and need to migrate to new APIs or the recommended image generation approach. It reflects a shift in Apple's on-device ML and image generation API strategy and is a reminder to keep up with SDK changes.
[Source URL](https://developer.apple.com/news/?id=dz9wvq0r) (Apple Developer)

### WWDC26 Developer Survey

Apple opened a developer survey about WWDC26. It is a chance to give direct feedback on the conference experience, the sessions, and the new technologies and frameworks. Community input can shape the direction of Apple's developer tools, API improvements, and documentation, so it is worth taking part.
[Source URL](https://developer.apple.com/news/?id=15wishue) (Apple Developer)

### DiffusionGemma: Developer Guide Released

Google published a developer guide for DiffusionGemma, an experimental text generation model. Based on the Gemma 4 architecture, it replaces token-by-token autoregression with diffusion-based parallel generation, which greatly increases inference speed and allows bidirectional context awareness and real-time self-correction. Generating and refining 256-token blocks in parallel makes it effective on complex constraint-based tasks such as Sudoku, and it can be deployed on ordinary consumer GPUs. It suggests a new paradigm for text generation and could help developers build faster, more accurate, constraint-aware text generation apps.
[Source URL](https://developers.googleblog.com/diffusiongemma-the-developer-guide/) (Google Developers Blog)

### Google Colab CLI: Connecting Local and Cloud

Google announced the new Google Colab CLI. The lightweight tool lets developers and AI agents connect a local terminal directly to a remote Colab runtime. You can easily request high-performance GPUs, run local Python scripts remotely, and retrieve artifact logs or models such as fine-tuned Gemma 3 adapters. Because it integrates directly with a standard terminal, it is highly scriptable and should help automate MLOps workflows.
[Source URL](https://developers.googleblog.com/introducing-the-google-colab-cli/) (Google Developers Blog)

### Gemma 4 12B Supports Local AI Agent Workflows on Laptops

Google DeepMind announced that Gemma 4 12B runs on an ordinary laptop with 16GB of RAM, supporting local agentic and multimodal AI workflows such as local data processing and visual insights. On macOS, Google AI Edge Gallery provides dynamic Python code execution and visualization, and Google AI Edge Eloquent provides fully offline voice dictation and text editing. A new `serve` command in the LiteRT-LM CLI strengthens the developer workflow. This makes on-device AI much more accessible, widens its use for privacy and offline scenarios, and opens new opportunities for local ML applications.
[Source URL](https://developers.googleblog.com/bringing-gemma-4-12b-to-your-laptop-unlocking-local-agentic-workflows-with-google-ai-edge/) (Google Developers Blog)

### OpenAI Announces Plan to Acquire Ona, Expanding Codex

OpenAI announced plans to acquire Ona. With it, OpenAI will bring secure, persistent cloud environments into Codex, extending long-running AI agents across enterprise workflows. Developers will be able to use Codex for more complex and continuous automation and code generation, and the move should strengthen OpenAI's position in enterprise AI.
[Source URL](https://openai.com/index/openai-to-acquire-ona) (OpenAI)

### Anthropic Introduces Claude Corps

Anthropic introduced "Claude Corps." Details are scarce, but it looks like a strategic initiative related to new uses of Claude, a developer program, or enterprise solutions. The name "Corps" suggests a specialized group with a specific purpose, so it likely aims to expand the Claude ecosystem and provide focused support in particular areas.
[Source URL](https://news.google.com/rss/articles/CBMiVkFVX3lxTE40YzY4elpuaVY0ZWtDbmhNal8wc2pEWWJ1QW5MbHNOLXR3azdxNU0wLWhLOURycWd5NWNlVGZiZzR5aEd2amozaXlBQk9pQ3Y2TjZvWDJn?oc=5) (Anthropic)

### Naver D2: MLXP, Adopting LLM Serving Optimizations on Kubernetes

Naver published the "MLXP: Adopting LLM Serving Optimizations on Kubernetes" session from NAVER ENGINEERING DAY 2026, its internal tech event. The talk shares how the team brought techniques for maximizing LLM inference performance, such as KV cache-aware routing, prefix caching, and distributed multi-node serving, into a Kubernetes production environment, and how it diagnosed and fixed conflicts with the existing stack, including the Istio service mesh, the scheduler, and pod protection policies. It offers practical insight for MLOps and infrastructure engineers running GPU workloads on Kubernetes or building LLM serving infrastructure.
[Source URL](https://d2.naver.com/helloworld/1059238) (Naver D2)

### Naver D2: Preventing Unintended Changes in Android Apps

The "Preventing Unintended Changes in Android Apps" session from NAVER ENGINEERING DAY 2026 is also out. It shows Android app and library developers how to detect unexpected changes from external library updates in advance and build a baseline-based defense. It covers how "Manifest Shield" works internally and how AI was used to build it, offering practical ways to improve stability and maintainability. It is especially useful for developers struggling with dependency management in large projects.
[Source URL](https://d2.naver.com/helloworld/3431313) (Naver D2)

### Naver D2: Eliminating Android Build Wait Times

The "Eliminating Android Build Wait Times" session from NAVER ENGINEERING DAY 2026 shares how Naver combined its in-house pod orchestration tool N3R with GitHub ARC (Actions Runner Controller) to dynamically allocate resource-heavy Android build environments and resolve CI/CD bottlenecks. It offers practical insight for teams running GitHub Actions self-hosted runners in restricted environments, such as internal networks with outbound traffic blocked, and for Android developers interested in Gradle build caching and multi-module optimization.
[Source URL](https://d2.naver.com/helloworld/4372269) (Naver D2)

### Siri AI Runs on Gemini Models but Isn't Gemini?

Reports say Apple's Siri AI runs on Google Gemini models but is not Gemini itself. It suggests Apple is integrating Google's LLM technology into its core assistant. For developers, it hints that Siri may use Gemini's advanced capabilities and that more sophisticated conversational AI may become available in the Apple ecosystem. It also offers insight into how the two companies collaborate on AI.
[Source URL](https://news.google.com/rss/articles/CBMiqAFBVV95cUxObTlGQ044SjlnSG9adEpPRzkxTXk5aGJnSzFKbnhBbjhNSDZ3MkVkMEVwdXpuSXB4bEx6QmMzcFRvc3hvOTdRNDYxOEJCYThqby0xLUVYcy14SzREa1RtTDVlRTBqQnFtZnpMTm5haW5HWkhaUWV2RWxCRDQ5cUZITWxRUV9pdWFWcXVTSVlpbVF HQU0zRm82Q0J5ZWZ4REx5Q0JzekY2bk5kZGE?oc=5) (9to5Mac)

### Google Introduces Gemini Omni

Google introduced "Gemini Omni." The name "Omni" usually emphasizes comprehensive or multimodal capability, suggesting a more powerful and broadly applicable version of Gemini. Developers using Gemini or building multimodal AI apps should look closely at what the new model can do.
[Source URL](https://news.google.com/rss/articles/CBMiYkFVX3lxTE0wOVZjc2o4dFdxdHljVS0yNWNNNU01NmFWNW82TVI0T1ptb1JxS0wzV3FoMkp6NGtoWDB0MmxiTFNodnUzSGpoOElDTDVlRWRpdDNRRFdzY2pRTWZULWxxRDh3?oc=5) (blog.google)

---
