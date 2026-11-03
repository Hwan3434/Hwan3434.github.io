---
title: "Sign in with Apple Domain Consolidation and Playwright E2E for AI Agents (2026. 06. 16)"
description: "Apple moves Sign in with Apple and Hide My Email to private.icloud.com, Google ships DiffusionGemma and Gemini 3.5 Live Translate, and Naver builds a Playwright E2E harness for AI agents."
date: 2026-06-16 09:39:15 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## Key Developer Tech News Highlights, June 16, 2026

From the latest tech news collected today (June 16, 2026), we selected and summarized the items most notable for developers, focusing on Google, Apple, Flutter, and AI research.

---

### DiffusionGemma: A Next-Generation Text Model Based on Diffusion, Not Tokens

Google published a developer guide for **DiffusionGemma**, an experimental text generation model based on the Gemma 4 architecture. Instead of token-by-token autoregression, it uses **diffusion-based parallel generation**, offering much faster inference, bidirectional context awareness, and real-time self-correction. It can also be deployed on consumer GPUs. Its architecture generates 256-token blocks in parallel and refines them through iterative denoising, which is especially effective on complex constraint-based tasks such as Sudoku. It opens new possibilities for on-device AI and local agents.

[https://developers.googleblog.com/diffusiongemma-the-developer-guide/](https://developers.googleblog.com/diffusiongemma-the-developer-guide/) (Google Developers Blog)

### Google Colab CLI: Control Remote Colab Runtimes from Your Local Terminal

Google announced the **Google Colab Command-Line Interface (CLI)**, a new tool that lets developers and AI agents connect a local terminal to a remote Colab runtime and run code there. With this lightweight CLI you can easily request high-performance GPUs, run local Python scripts remotely, and retrieve artifact logs or models such as fine-tuned Gemma 3 adapters. It integrates directly with a standard terminal, is highly scriptable, and should improve ML/AI development workflows considerably.

[https://developers.googleblog.com/introducing-the-google-colab-cli/](https://developers.googleblog.com/introducing-the-google-colab-cli/) (Google Developers Blog)

### Gemma 4 12B Runs Locally: Agentic Workflows with Google AI Edge

Google DeepMind announced that **Gemma 4 12B** runs on an ordinary laptop with 16GB of RAM and, through **Google AI Edge**, supports agentic AI features including local data processing and visual insights. On macOS, Google AI Edge Gallery offers dynamic Python code execution and visualization, and Google AI Edge Eloquent offers fully offline voice dictation and text editing. A new `serve` command in the LiteRT-LM CLI further strengthens the developer workflow. It could speed up the spread of on-device AI and local agent development.

[https://developers.googleblog.com/bringing-gemma-4-12b-to-your-laptop-unlocking-local-agentic-workflows-with-google-ai-edge/](https://developers.googleblog.com/bringing-gemma-4-12b-to-your-laptop-unlocking-local-agentic-workflows-with-google-ai-edge/) (Google Developers Blog)

### Google Gemini 3.5 Live Translate Shows Performance Tuned for Real Conversations

CNET reports that Google's **Gemini 3.5 Live Translate** performs well in real-life conversations, suggesting the Gemini 3.5 model translates in real time with more natural phrasing and better grasp of context. For developers, this is a chance to improve the user experience in conversational AI interfaces, language learning apps, and multilingual communication tools.

[https://news.google.com/rss/articles/CBMisgFBVV95cUxNcW9DYjVEZlFaYzF1MVppU2RTOWRXM2ZaOERRbTJ5WUVfVUI5TTdrMWJ5cjI3SloyWWRwMnRvWFdKaXhnMGdHQXAzQ1cwMElHUWVCTEZPdjJaZkZGWnN2YnVhTk9pZktSWWF4LTFjZ2I2OWFoUzJhejBZTmhRZjc2LXF3SWNRMktINXNYNVRfWlo1NnhKY2o0NkJ4dlFIRlgwYUtWdkI1UC1iMGFNSjBhbmdn?oc=5](https://news.google.com/rss/articles/CBMisgFBVV95cUxNcW9DYjVEZlFaYzF1MVppU2RTOWRXM2ZaOERRbTJ5WUVfVUI5TTdrMWJ5cjI3SloyWWRwMnRvWFdKaXhnMGdHQXAzQ1cwMElHUWVCTEZPdjJaZkZGWnN2YnVhTk9pZktSWWF4LTFjZ2I2OWFoUzJhejBVMmFNSjBhbkdn?oc=5) (CNET)

### Apple Consolidates the Sign in with Apple and Hide My Email Domains

Apple announced that the email domain used for "Sign in with Apple" and iCloud+ "Hide My Email" will be unified as **`private.icloud.com`**. Sign in with Apple addresses previously used the `privaterelay.appleid.com` domain, but all newly created addresses will use the new unified domain. This reduces the number of domains developers need to expect in email handling logic, but systems that depend on the old domain may need updates.

[https://developer.apple.com/news/?id=sus6t6ab](https://developer.apple.com/news/?id=sus6t6ab) (Apple Developer News)

### Flutter Q2 Survey: Give Feedback on the Roadmap

The Flutter team encouraged developers to take part in its **Q2 survey**, reminding them that it closes on Friday, June 19. It is a chance to directly influence the direction of Flutter's roadmap, so Flutter developers should share their views.

[https://blog.flutter.dev/flutter-q2-survey-475913d622ec?source=rss----4da7dfd21a33---4](https://blog.flutter.dev/flutter-q2-survey-475913d622ec?source=rss----4da7dfd21a33---4) (Flutter Blog)

### Building a Playwright E2E Test Harness for AI Agents' Code (NAVER ENGINEERING DAY 2026)

Naver D2 published **"Building a Playwright E2E Test Harness for AI Agents,"** a session from NAVER ENGINEERING DAY 2026. In an era when AI agents write code, it answers how to trust and verify the code they generate. It shares how the team built Playwright-based E2E tests and a workflow in which the agent writes and verifies the test code itself, a practical guide for developers automating large codebases with agents and considering E2E testing.

[https://d2.naver.com/helloworld/6811215](https://d2.naver.com/helloworld/6811215) (NAVER D2)
