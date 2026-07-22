---
layout: post
title: "데일리 테크 뉴스 - 2026-07-23"
date: 2026-07-23 06:02:04 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## 오늘의 개발자 뉴스: Agentic RL 처리량, 초고속 Tokenizer, 실전 SIMD, Postgres 운영

2026년 7월 23일 기준으로 tool call 대기 시간을 숨기는 agentic RL training pipeline, CPU에서 GB/s 단위로 동작하는 LLM tokenizer, 일반 개발자를 위한 SIMD 적용 패턴, startup이 production에서 겪은 Postgres 운영 교훈을 정리했습니다. 주가, 실적, 경영진 중심 뉴스는 제외했습니다.

---

### Agentic RL Infrastructure

*   **Google Tunix, 비동기 rollout으로 tool-using agent 학습의 TPU idle time 축소**
    Google의 JAX 기반 post-training library Tunix는 agent가 code execution, database query, web search 같은 environment step을 기다릴 때 accelerator가 쉬는 문제를 겨냥합니다. `RolloutOrchestrator`가 Python `asyncio`와 vLLM-TPU·SGLang-Jax를 이용해 많은 trajectory를 동시에 진행하고, 완료된 trajectory를 producer-consumer queue로 `AgenticRLLearner`에 넘겨 rollout과 synchronous training을 분리합니다. Agent와 environment API도 training loop에서 분리해 SWE-bench, WebArena, Gymnasium 같은 환경을 교체할 수 있으며, 경량 RL 전용 metric으로 rollout·tool call·weight sync의 병목을 지속 추적합니다. JAX/TPU에서 multi-turn GRPO나 tool-use agent를 학습하는 팀이라면 평균 throughput뿐 아니라 tail latency와 queue backpressure가 실제 workload에서 개선되는지 확인할 가치가 있습니다.
    [Source URL](https://developers.googleblog.com/scaling-agentic-rl-high-throughput-agentic-training-with-tunix/) (Google Developers Blog)

---

### LLM Data Pipeline Performance

*   **Gigatoken, SIMD와 cache hierarchy로 BPE tokenization을 GB/s 수준까지 최적화**
    Rust 기반 MIT-licensed project Gigatoken은 Hugging Face Tokenizers와 Tiktoken compatibility mode를 제공하고, 전용 API에서는 file을 Rust에서 직접 읽어 Python object 전달 비용을 줄입니다. 핵심은 regex engine에 맡기던 pretokenization을 SIMD로 최적화하고, 반복 단어의 token mapping cache와 thread 간 상호작용을 줄이는 것입니다. Project가 공개한 11.9GB OpenWebText benchmark에서 GPT-2 tokenizer는 dual-socket AMD EPYC 9565에서 24.53GB/s, Apple M4 Max에서 8.79GB/s를 기록했지만, 이는 project 자체 측정이며 tokenizer와 hardware에 따라 10배대부터 1,000배 이상까지 편차가 큽니다. WordPiece는 아직 지원하지 않고 SentencePiece와 Windows 지원도 제한적이므로, 도입 전 `gigatoken bench --validate`로 output 일치와 target corpus 성능을 함께 확인해야 합니다.
    [Source URL](https://github.com/marcelroed/gigatoken/) (GitHub)

---

### Practical CPU Optimization

*   **Mitchell Hashimoto, 일반 loop를 SIMD로 옮기는 다섯 단계 패턴 설명**
    Mitchell Hashimoto는 SIMD를 특수한 low-level 기법이 아니라 충분히 큰 byte·string·array loop에 적용할 수 있는 반복 가능한 패턴으로 설명합니다. 상수를 vector lane에 broadcast하고, vector width 단위로 순회하며, lane별 연산 뒤 결과를 reduce 또는 store하고, 남은 원소는 scalar tail로 처리하는 다섯 단계입니다. Ghostty에서 control character 이전의 printable codepoint 구간을 찾는 Zig 예제로 generic vector code와 scalar 구현을 비교하며, compiler auto-vectorization이 불가능하거나 불안정한 경우 명시적 SIMD가 유용하다고 설명합니다. 다만 짧은 input이나 복잡한 분기가 많은 loop에는 전환 비용과 유지보수성이 이득을 상쇄할 수 있으므로 benchmark로 판단해야 합니다.
    [Source URL](https://mitchellh.com/writing/everyone-should-know-simd) (Mitchell Hashimoto)

---

### Production Postgres

*   **Hatchet, schema부터 autovacuum까지 startup의 Postgres 생존 가이드 공개**
    Hatchet이 2년간의 production 운영 경험을 schema, query, migration, connection, query planner, bulk write, autovacuum, partitioning 순서로 정리했습니다. 실전 권고에는 짧은 transaction 유지, 큰 table의 `CREATE INDEX CONCURRENTLY`, additive한 expand-contract migration, connection pool 사용, `EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS, FORMAT JSON)`을 통한 estimate와 실제 row 비교가 포함됩니다. High-write table에서는 dead tuple 정리와 statistics 갱신이 workload를 따라가도록 autovacuum threshold와 scale factor를 조정해야 하며, batch write는 round trip과 internal lock overhead를 줄일 수 있습니다. 수치는 Hatchet workload의 경험치이므로 그대로 복사하기보다 lock wait, bloat, connection 수, query latency를 관측하면서 단계적으로 적용하는 편이 안전합니다.
    [Source URL](https://hatchet.run/blog/postgres-survival-guide) (Hatchet)

---

오늘의 공통점은 병목을 추상화 아래에 숨겨 두지 않는다는 점입니다. Agent 학습에서는 environment wait와 queue 흐름을, tokenization과 일반 loop에서는 CPU lane과 cache를, database에서는 planner·lock·vacuum을 직접 관측해야 최적화가 실제 production 효과로 이어집니다.
