---
title: "ImageCreator Deprecated, Swift TrueType Hinting, DiffusionGemma (2026. 06. 13)"
description: "Apple deprecates ImageCreator and moves its TrueType hinting interpreter to Swift, Google ships DiffusionGemma and Gemini Omni, and Naver shares LLM serving and Android talks."
date: 2026-06-13 09:34:38 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

Hello, developers! From the tech news collected today (June 13, 2026), we picked only the items with real technical depth: core technology updates of the kind announced at Google I/O or WWDC, open source, AI model research, and problem-solving in real production environments.

---

## Apple Ecosystem Updates: API Changes and Swift Modernization

Two important changes to Apple's development environment were announced today: an API deprecation and the migration of core system logic to Swift.

### ImageCreator Class to Be Deprecated
Apple announced that the `ImageCreator` class, provided for apps using the on-device image generation model, will no longer be supported starting with iOS 27, iPadOS 27, macOS 27, and visionOS 27. It is part of refining Apple's approach to image generation and points toward newer approaches such as the `Image Playground` framework. Developers using `ImageCreator` should prepare to migrate.
[Source URL](https://developer.apple.com/news/?id=dz9wvq0r) (Apple Developer)

### TrueType Hinting Interpreter Migrated to Swift
Apple said it successfully migrated the TrueType hinting interpreter, a core system component, to Swift. TrueType hinting is key to font rendering quality, and moving complex, performance-sensitive C code to Swift can greatly improve stability, performance, and maintainability. It is an important example of system-level code continuing to move to Swift.
[Source URL](https://www.swift.org/blog/migrating-truetype-hinting-to-swift/) (Swift.org)

## Google AI and Developer Tools: From Models to Local Environments

Google released a broad set of updates, from a new AI model architecture to productivity tools and AI on local machines.

### DiffusionGemma: Developer Guide to a Diffusion-Based Text Model
Google announced DiffusionGemma, an experimental text generation model based on the Gemma 4 architecture. Instead of token-by-token autoregression, it uses diffusion-based parallel generation, offering much faster inference, bidirectional context awareness, and real-time self-correction. It can be deployed on consumer GPUs and is effective on complex constraint-based tasks such as Sudoku. It is seen as an important step for LLM inference speed and efficiency.
[Source URL](https://developers.googleblog.com/diffusiongemma-the-developer-guide/) (Google Developers Blog)

### Google Colab CLI: Bringing Local and Remote Together
The Google Colab team released a new command-line interface. With it, developers and AI agents can connect from a local terminal directly to a remote Colab runtime and run code. You can request high-performance GPUs, run local Python scripts remotely, and retrieve artifacts and models such as fine-tuned Gemma 3 adapters, and because it integrates directly with a standard terminal it is highly scriptable. It should greatly simplify AI development workflows.
[Source URL](https://developers.googleblog.com/introducing-the-google-colab-cli/) (Google Developers Blog)

### Gemma 4 12B Supports Agentic Workflows on Laptops
Google DeepMind announced that Gemma 4 12B brings agentic, multimodal AI to an ordinary laptop with 16GB of RAM. On macOS, Google AI Edge Gallery provides dynamic Python code execution and visualization, and Google AI Edge Eloquent supports fully offline voice dictation and text editing. A new `serve` command in the LiteRT-LM CLI further strengthens the developer workflow. Running AI locally brings clear benefits for privacy and latency.
[Source URL](https://developers.googleblog.com/bringing-gemma-4-12b-to-your-laptop-unlocking-local-agentic-workflows-with-google-ai-edge/) (Google Developers Blog)

### Gemini Omni Introduced
Google introduced "Gemini Omni," a next-generation AI model. More technical detail is expected, but the "Introducing" framing and the blog.google channel suggest a new flagship in the Gemini family or a major update to an existing model.
[Source URL](https://news.google.com/rss/articles/CBMiYkFVX3lxTE0wOVZjc2o4dFdxdHljVS0yNWNNNU01NmFWNW82TVI0T1ptb1JxS0wzV3FoMkp6NGtoWDB0MmxiTFNodnUzSGpoOElDTDVlRWRpdDNRRFdzY2pRTWZULWxxRDh3?oc=5) (blog.google)

## Insights from Korean Developers: Naver D2

Sessions published on Naver D2 show how Korean developers approach LLM serving, Android app development, and build optimization.

### MLXP: Adopting LLM Serving Optimizations on Kubernetes
At NAVER ENGINEERING DAY 2026, its internal tech event, Naver shared how it brought techniques for maximizing LLM inference performance (KV cache-aware routing, prefix caching, distributed multi-node serving, and more) into a Kubernetes production environment. It covers conflicts with the existing stack, such as the Istio service mesh, the scheduler, and pod protection policies, and how they were solved, which makes it practical for MLOps and infrastructure engineers running GPU workloads or LLM serving on Kubernetes.
[Source URL](https://d2.naver.com/helloworld/1059238) (Naver D2)

### Preventing Unintended Changes in Android Apps
The same event published a session for Android app and library developers on preventing unintended changes. It shows how to detect unexpected changes from external library updates in advance and build "Manifest Shield," a baseline-based defense. Important for Android developers who track dependencies and the AndroidManifest.
[Source URL](https://d2.naver.com/helloworld/3431313) (Naver D2)

### Eliminating Android Build Wait Times
Naver shared how it combined its in-house pod orchestration tool N3R with GitHub ARC (Actions Runner Controller) to dynamically allocate resource-heavy Android build environments and resolve CI/CD bottlenecks. It is useful for Android developers interested in Gradle build caching and multi-module optimization, and for teams running GitHub Actions self-hosted runners on internal networks with outbound or permission restrictions.
[Source URL](https://d2.naver.com/helloworld/4372269) (Naver D2)

---

That's it for today's tech news.
