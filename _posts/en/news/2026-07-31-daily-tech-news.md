---
layout: post
title: "Daily Tech News - 2026-07-31"
date: 2026-07-31 06:00:54 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## Today's Developer News: GPT-5.6 Pricing, Gemini Robotics 2, GitHub Stacked PRs, and the Cost of Refactoring Agent-Written Code

Here is a developer-focused digest for July 31, 2026, covering new GPT-5.6 API pricing and processing modes, developer access to Gemini Robotics 2 embodied reasoning, GitHub's public preview of stacked pull requests, and an experiment measuring how refactoring agent-written code affects the token cost of later changes. Stock-market, earnings, executive, and broad business news has been excluded.

---

### AI APIs

*   **OpenAI cuts GPT-5.6 Luna and Terra prices and introduces Fast mode for Sol**
    Effective July 30, OpenAI prices GPT-5.6 Luna at $0.20 per million input tokens and $1.20 per million output tokens, while Terra costs $2 and $12 respectively. The company describes those changes as reductions of 80% for Luna and 20% for Terra. GPT-5.6 Sol gains a Fast mode that is priced at twice the Standard rate and promises up to 2.5 times the speed; existing Priority Processing requests automatically map to Fast mode. Codex and ChatGPT Work subscription prices and quota budgets do not change, but Terra and Luna consume fewer credits. Instead of choosing one default model for an entire workflow, teams can evaluate a staged design—for example, using Sol for planning and uncertainty resolution, then Luna for well-specified implementation and testing. The price reductions and speedup are provider claims, so real latency and task success still need workload-specific evaluation.
    [Source URL](https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/) (OpenAI)

---

### Physical AI

*   **Google DeepMind introduces Gemini Robotics 2 for whole-body control and multi-robot collaboration**
    The Gemini Robotics 2 family includes a vision-language-action model that turns visual and language input into motor control, `Gemini Robotics ER 2` for planning tasks that last several minutes, and `Gemini Robotics On-Device 2` for local execution on robotic hardware. ER 2 is available in Google AI Studio and in private preview on Gemini Enterprise Agent Platform, while the VLA and On-Device models are limited to early-access partners. DeepMind says the on-device model can typically adapt to a new bi-arm embodiment with fewer than 200 examples and a few hours of data. A new `ASIMOV-Agentic` benchmark evaluates whether the reasoning agent rejects unsafe VLA tool calls, recognizes impossible tasks, and requests human intervention under uncertainty. The release also acknowledges that multi-finger manipulation remains difficult, and the full VLA checkpoint is not a generally available API, so hands-on access for most developers currently centers on ER 2.
    [Source URL](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/) (Google DeepMind)

---

### Developer Workflow

*   **GitHub launches a public preview of stacked pull requests for dependent, reviewable changes**
    GitHub's stacked pull requests split a large change into an ordered sequence of smaller PRs, with each PR targeting the layer below it. Reviewers can inspect each layer's diff independently and use a stack map to understand its place in the larger change. Merging the latest ready PR can land every unmerged lower layer in one operation. If only part of the stack is merged, higher layers remain open and are automatically rebased and retargeted; existing branch protections, required checks, and review requirements continue to apply. Developers can install the CLI extension with `gh extension install github/gh-stack`, and stacks also work on the web, GitHub Mobile, and with coding agents using the `gh-stack` skill. The preview is rolling out to all repositories over several days, while merge-queue support will arrive progressively over the following weeks, so CI automation should account for rollout status and base-branch changes after automatic retargeting.
    [Source URL](https://github.blog/changelog/2026-07-30-stacked-pull-requests-are-now-in-public-preview/) (GitHub)

---

### Agentic Engineering

*   **A MartinFowler.com experiment finds an 83% input-token reduction after structural refactoring**
    Giles Edwards-Alexander took a 17,155-line Rust data-access file from an approximately 150,000-line, agent-written application and refactored it in stages. After every stage, a fresh sub-agent performed the same representative change. By the final stage, the largest file had fallen to 3,695 lines and estimated input tokens for the task dropped from 159,564 to 27,360, an 83% reduction, while output-token use changed little. Total code in the data-access layer stayed almost constant, suggesting the gain came not from deleting code but from making it possible for the agent to identify and read a smaller relevant set of files. Token use rose at some intermediate stages, the experiment estimated tokens by dividing character counts by four rather than using reliable live accounting, and it covered one task in one codebase. The result is therefore evidence that clear module boundaries can reduce agent context-discovery cost, not proof that mechanically splitting files always saves tokens.
    [Source URL](https://martinfowler.com/articles/exploring-gen-ai/refactoring-economic-benefit.html) (Giles Edwards-Alexander / MartinFowler.com)

---

Today's common thread is that AI development cost is shaped by more than model pricing. Matching models and processing modes to workflow stages, giving agents clear code boundaries, and splitting large changes into reviewable PR layers can reduce both token overhead and review bottlenecks.
