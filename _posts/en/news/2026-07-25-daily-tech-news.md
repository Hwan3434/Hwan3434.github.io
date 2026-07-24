---
layout: post
title: "Daily Tech News - 2026-07-25"
date: 2026-07-25 06:02:30 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## Today's Developer News: Ray on TPU, IntelliJ Plugin Generator, Debian's LLM Policy Debate, and Claude Opus 5

Here is a developer-focused digest for July 25, 2026, covering Ray's serving, data, and training APIs for TPUs; a unified IntelliJ plugin-project generator; competing proposals over LLM use in Debian contributions; and Claude Opus 5 in GitHub Copilot. Stock-market, earnings, executive, and broad business news has been excluded.

---

### Distributed AI Infrastructure

*   **Ray 2.55 connects Serve, Data, and Train to TPUs through officially supported high-level APIs**
    Part two of Google's Ray on TPU guide explains how the existing Ray libraries hide the requirement that a multi-host TPU workload stay within one ICI-connected slice. Ray Serve places a vLLM replica on an intact slice through `accelerator_config.topology`, while Ray Data's `iter_jax_batches()` delivers device-sharded JAX batches without a host-side NumPy-to-JAX copy. With only a topology declaration, `JaxTrainer` handles one worker per host, checkpoints, fault-tolerant restarts, and multi-slice coordination. Official `rayproject/ray:*-tpu` images and TPU utilization and memory metrics in the Ray Dashboard are also available. The lower-level `slice_placement_group()` remains an alpha API, so custom workloads that call it directly should pin their Ray version and plan for surface changes.
    [Source URL](https://developers.googleblog.com/run-ray-on-tpu-part-2-ray-ai-libraries/) (Google Developers Blog)

---

### IDE Plugin Development

*   **JetBrains unifies its IDE wizard and GitHub template in a web-API-based IntelliJ Platform Plugin Generator**
    Starting with IntelliJ IDEA 2026.1, the new generator replaces the Plugin DevKit's former offline wizard and the separately maintained GitHub template with one server-side template source. The IDE and browser now create the same project, with optional plugin dependencies, GitHub Actions workflows, issue templates, Dependabot configuration, and a Split Mode-ready structure. Because the IDE fetches current templates from the generator API, developers do not need an IDE update every time a platform release changes the default project. Organizations that require offline project creation should account for the new dependency on a server URL, and generated output should still be reviewed and committed like any other dependency-derived artifact.
    [Source URL](https://blog.jetbrains.com/platform/2026/07/ide-plugin-generator-the-new-beginning/) (JetBrains)

---

### Open Source Governance

*   **Debian opens a General Resolution discussion over banning or conditionally allowing LLM-assisted contributions**
    The discussion that began on July 24 presents two opposing approaches. Proposal A would prohibit generative-AI assistance in direct Debian code, packages, documentation, translations, web resources, and official communication. Proposal B would allow AI-assisted work if contributors verify tool terms, licensing, and attribution; accept full technical and legal responsibility; and disclose substantial AI use. Both distinguish direct Debian contributions from upstream projects that happen to use AI, but they take sharply different approaches to review burden, quality, and copyright risk. This is a discussion, not an adopted policy or voting result. Until an outcome exists, Debian contributors should follow current review and licensing requirements and keep reproducible validation evidence and disclosure ready when AI assistance is involved.
    [Source URL](https://www.debian.org/vote/2026/vote_002) (Debian)

---

### AI Coding Tools

*   **Claude Opus 5 begins rolling out across GitHub Copilot's editor, CLI, and cloud-agent surfaces**
    GitHub has added Anthropic's Claude Opus 5 as an option for complex, long-running coding tasks. It is rolling out in VS Code, Visual Studio, JetBrains IDEs, Xcode, Eclipse, Copilot CLI, github.com, GitHub Mobile, Copilot cloud agent, and the Copilot app for Pro+, Max, Business, and Enterprise plans. Business and Enterprise administrators must enable a dedicated policy, and usage is billed at the provider's API list price under usage-based billing. GitHub highlights autonomous code changes, regression verification, and multi-tool coordination, while warning that stronger cyber safeguards can also block legitimate security-adjacent prompts. Teams should define model-access policy, spending limits, and a fallback model for security work before broad rollout.
    [Source URL](https://github.blog/changelog/2026-07-24-claude-opus-5-is-now-available-in-github-copilot/) (GitHub)

---

Today's common thread is that adding AI and automation to an established development workflow requires operational boundaries, not only a convenient interface. TPU topology and centralized templates let tools absorb complexity, but teams still need to understand version and network dependencies. LLM contribution rules and a new coding model likewise call for explicit accountability, disclosure, cost controls, and security fallbacks so productivity gains do not return as extra review work.
