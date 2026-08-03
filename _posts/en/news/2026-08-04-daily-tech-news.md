---
layout: post
title: "Daily Tech News - 2026-08-04"
date: 2026-08-04 06:03:37 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## Today's Developer News: Large-Model Inference, Fabricated CVEs, Long-Horizon Coding, and Karpathy's Pelican Experiment

Here is a developer-focused digest for August 4, 2026, covering Cloudflare's production techniques for serving Kimi and GLM with less GPU memory, JFrog's reproduction-based investigation of apparently AI-generated SQLite CVEs, MirrorCode's whole-program reimplementation benchmark, and Andrej Karpathy's long-running Three.js generation experiment. Stock-market, earnings, executive, and broad business news has been excluded.

---

### AI Inference Infrastructure

*   **Cloudflare combines FP8 KV-cache quantization, INT4 weight compression, and page-integrity checks to improve large-model serving density**
    Cloudflare changed Kimi K2.6's KV cache from BF16 to FP8 e4m3 on Workers AI, increasing the context that fits in the same memory from roughly 686,000 tokens to 1.37 million. BF16 remains slightly faster per token for an individual request, but FP8 increased measured concurrency from 32 to 64 requests, raising peak throughput by about 41% and lowering cost per token by roughly 30%. For GLM 5.2, compressing weights from FP8 to INT4 reduced the checkpoint from 705 GB to 421 GB. INT4 is slower for prefill because the weights must be expanded before multiplication, so Cloudflare keeps compute-bound prefill on FP8 and uses INT4 only for memory-bound decode. Its shared KV cache also tags every physical page on reallocation and checks each request's expected page-to-tag mapping before supported decode operations, aborting a request rather than risking a read from the wrong page. The useful pattern is not one quantization format in isolation, but a design that combines disaggregated prefill and decode with cache isolation.
    [Source URL](https://blog.cloudflare.com/smaller-faster-safer-models/) (Cloudflare Blog)

---

### Software Supply Chain Security

*   **JFrog finds that six critical SQLite CVEs fail source inspection and proof-of-concept reproduction**
    JFrog compared a new GitHub account's SQLite advisories with the source of the claimed versions, built official releases under AddressSanitizer in isolated Docker containers, and ran the published proof-of-concept payloads. The investigation found nonexistent functions, line numbers beyond the end of a file, fabricated fixes in files that had not changed, and SQL that failed during parsing; none of the six PoCs reproduced the claimed memory bug. A broader audit of 55 advisories from the same account classified 54 as entirely fabricated and one as a real bug wrapped in unverified CVE metadata. If CI or a security agent turns NVD or GHSA severity directly into tickets and patches, fabricated input can create real engineering cost and unnecessary code changes. New CVEs from unknown reporters need corroboration from the maintainer, linked commits, a checkout of the affected version, and safe PoC reproduction.
    [Source URL](https://research.jfrog.com/post/sqlite-critical-cves-or-llm-slops/) (JFrog Security Research)

---

### Agent Evaluation

*   **Epoch AI and METR release MirrorCode, a long-horizon benchmark for rebuilding complete programs without their source**
    MirrorCode moves beyond bug fixes and isolated features: an agent must reimplement 25 programs spanning Unix utilities, serialization and query tools, bioinformatics, interpreters, static analysis, cryptography, and compression using only their input-output behavior. Agents work in a sandbox without internet or original-source access, and their output must match on unseen end-to-end tests. The largest single run lasted 19 days without human intervention and cost $2,600. Claude Opus 4.7 nearly recreated `gotree`, a Go bioinformatics toolkit with more than 40 commands and about 16,000 lines, in 14 hours for $251. It still failed one niche date-annotation edge case among 2,001 tests, so it was not a strict full solution, and pretraining contamination remains possible because the targets are open source. With the scaffold and 22 of 25 targets released, the benchmark is most useful as a reproducible test bed for long-horizon agents' testing discipline, budgets, and failure modes rather than as a simple model leaderboard.
    [Source URL](https://epoch.ai/MirrorCode) (Epoch AI / METR)

---

### Generative Coding Experiments

*   **Andrej Karpathy gives a coding agent a one-million-token budget to turn one literary paragraph into a 5,500-line Three.js scene**
    Looking beyond short prompts such as “draw a pelican on a bicycle,” Karpathy gave Claude Opus 5 the opening paragraph of a novel, a one-million-token budget—about $10—and asked for a Three.js rendering. The model ran for roughly two hours and produced about 5,500 lines that positioned polygonal assets in three-dimensional coordinates and orchestrated their animation. Karpathy described the result as janky, so this is not a benchmark proving correctness or productivity. It is instead a useful test case for how evaluation changes as code generation becomes a long-running agent task: teams need to inspect execution traces, asset provenance, browser performance, maintainable scene abstractions, and budget limits alongside the final visual output.
    [Source URL](https://twitter.com/karpathy/status/2083749667410727319) (Andrej Karpathy)

---

Today's common thread is that longer runs and more automation make input validation more important. Inference servers must verify cache pages, security pipelines must reproduce CVEs, and coding-agent evaluations must separate hidden-test performance from possible contamination.
