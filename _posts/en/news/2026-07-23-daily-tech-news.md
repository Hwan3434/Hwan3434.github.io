---
layout: post
title: "Daily Tech News - 2026-07-23"
date: 2026-07-23 06:02:04 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## Today's Developer News: Agentic RL Throughput, a High-speed Tokenizer, Practical SIMD, and Postgres Operations

Here is a developer-focused digest for July 23, 2026, covering an agentic RL training pipeline that hides tool-call latency, an LLM tokenizer operating at GB/s on CPUs, a practical SIMD pattern for everyday developers, and production Postgres lessons from a startup. Stock-market, earnings, executive, and broad business news has been excluded.

---

### Agentic RL Infrastructure

*   **Google Tunix uses asynchronous rollouts to reduce TPU idle time during tool-using agent training**
    Tunix, Google's JAX-native post-training library, targets accelerator stalls while an agent waits for environment steps such as code execution, database queries, or web searches. Its `RolloutOrchestrator` uses Python `asyncio` with vLLM-TPU and SGLang-Jax to advance many trajectories concurrently, then sends completed trajectories through a producer-consumer queue to `AgenticRLLearner`, decoupling rollout generation from synchronous training. Separate agent and environment APIs allow environments such as SWE-bench, WebArena, and Gymnasium to be swapped without rewriting the training loop, while lightweight RL-specific metrics continuously expose bottlenecks in rollout, tool calls, and weight synchronization. Teams training multi-turn GRPO or tool-using agents on JAX and TPUs should validate improvements in tail latency and queue backpressure on their own workloads, not only average throughput.
    [Source URL](https://developers.googleblog.com/scaling-agentic-rl-high-throughput-agentic-training-with-tunix/) (Google Developers Blog)

---

### LLM Data Pipeline Performance

*   **Gigatoken applies SIMD and cache-hierarchy optimization to push BPE tokenization into GB/s territory**
    Gigatoken is an MIT-licensed Rust project with compatibility modes for Hugging Face Tokenizers and Tiktoken; its native API can read files directly in Rust to avoid moving Python objects across the boundary. Its main optimizations replace regex-driven pretokenization with SIMD, cache token mappings for repeated words, and minimize interaction between worker threads. In the project's own 11.9GB OpenWebText benchmark, the GPT-2 tokenizer reached 24.53GB/s on a dual-socket AMD EPYC 9565 and 8.79GB/s on an Apple M4 Max. These are project-reported measurements, and gains vary from roughly an order of magnitude to more than 1,000 times depending on tokenizer and hardware. WordPiece is not yet supported, while SentencePiece and Windows support remain limited, so adopters should use `gigatoken bench --validate` to test both output equivalence and target-corpus performance.
    [Source URL](https://github.com/marcelroed/gigatoken/) (GitHub)

---

### Practical CPU Optimization

*   **Mitchell Hashimoto explains a five-step pattern for turning ordinary loops into SIMD code**
    Mitchell Hashimoto presents SIMD as a repeatable pattern for sufficiently large byte, string, or array loops rather than an exotic low-level technique. The five steps are to broadcast constants into vector lanes, iterate one vector width at a time, perform lane-wise operations, reduce or store the result, and handle the remainder with a scalar tail. A Zig example from Ghostty compares generic vector code with a scalar loop that searches for the printable-codepoint run before a control character, and explains where explicit SIMD helps when compiler auto-vectorization is unavailable or unreliable. Short inputs and branch-heavy loops may not recover the conversion and maintenance cost, so benchmarks should decide whether to keep the vectorized path.
    [Source URL](https://mitchellh.com/writing/everyone-should-know-simd) (Mitchell Hashimoto)

---

### Production Postgres

*   **Hatchet publishes a startup Postgres survival guide spanning schemas, query plans, and autovacuum**
    Hatchet distilled two years of production experience into guidance on schemas, queries, migrations, connections, the query planner, bulk writes, autovacuum, and partitioning. Practical recommendations include keeping transactions short, using `CREATE INDEX CONCURRENTLY` on large live tables, applying additive expand-contract migrations, pooling connections, and comparing estimated and actual rows with `EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS, FORMAT JSON)`. High-write tables may require workload-specific autovacuum thresholds and scale factors so dead-tuple cleanup and statistics updates keep pace, while batched writes can reduce round trips and internal-lock overhead. The quantitative results reflect Hatchet's workload, so teams should roll changes out incrementally while observing lock waits, bloat, connection counts, and query latency.
    [Source URL](https://hatchet.run/blog/postgres-survival-guide) (Hatchet)

---

Today's common thread is refusing to leave bottlenecks hidden beneath abstractions. Agent training requires visibility into environment waits and queue flow, tokenization and ordinary loops require attention to CPU lanes and caches, and databases require direct observation of planners, locks, and vacuum behavior before an optimization becomes a production improvement.
