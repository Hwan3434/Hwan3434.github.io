---
layout: post
title: "AI & Mobile Digest - 2026-08-21"
date: 2026-08-21 06:10:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## Today's threads: 2x from a 300M draft, a 125M running on a phone, and a VM for agent code

-   LFM2.5-DSpark hits 2.27x on-device with 300M drafts
-   A 125M Core ML INT8 model does 108 notes/s on iPhone 15
-   smolvm 1.8.3: 0.6-1.5s cold start, ~50ms warm
-   Swift 6.4 Embedded gets `any` types and untyped throws
-   Kotlin domain errors belong in signatures: sealed + Either

---

### On-Device Inference

*   **Liquid AI's LFM2.5-DSpark claims 2.27x on-device decoding from 300M draft models (vendor-reported)**
    -   All three drafts are roughly 300M (295.7M-327.7M), and on an M4 Max, LFM2.5-2.6B goes from 61 to 139 tok/s, a 2.27x gain.
    -   On an H100 in BF16 the same model goes 323 to 864 tok/s (2.67x), and function-calling latency drops 57% on average.
    -   They ship as Safetensors and GGUF, with integration code upstreamed to llama.cpp and SGLang for day-one support.
    [Source URL](https://huggingface.co/blog/LiquidAI/lfm25-dspark) (Hugging Face / Liquid AI)
    > Takeaway: If you already run an on-device LLM through llama.cpp, keep the target model and bolt on a draft to measure the acceptance rate first.

---

### On-Device Deployment

*   **A 125M decoder transformer exported to Core ML with INT8 weights generates 108 notes/s on an iPhone 15**
    -   Tokenization bundles pitch, delta_onset, duration, and velocity into one note so a single forward pass advances the music by one note.
    -   The training context is 512 notes, but inference keeps a 384-note sliding window so long sessions stay bounded.
    -   DPO using Gemini 3.5 Flash as a pairwise judge lifted the preference score from 24.55% to 69.05%.
    [Source URL](https://simedw.com/2026/08/20/midi-autocomplete/) (simedw.com)
    > Takeaway: For domain-specific small models the tokenizer design decides your speed, so check first whether several fields can collapse into one step.

---

### Agent Sandboxing

*   **smolvm 1.8.3 isolates agent-generated code in Firecracker VMs — 0.6-1.5s cold start**
    -   It uses hardware-isolated VMs instead of shared-kernel containers, with warm executions around 50ms.
    -   Verified controls include CPU and RAM limits, network isolation, read-only input plus writable output mounts, storage quotas, and guest-enforced timeouts.
    -   The Claude Code container, itself a Firecracker guest, has no `/dev/kvm` and failed; the tests only ran on a GitHub Actions runner.
    [Source URL](https://simonwillison.net/2026/Aug/19/smolmachines-untrusted-sandbox/) (Simon Willison)
    > Takeaway: If you plan to execute LLM-generated code, first confirm the host exposes `/dev/kvm` and the vmx/svm CPU flags.

---

### Swift Toolchain

*   **Swift 6.4 narrows the Embedded Swift subset gap by allowing `any` existentials and untyped throws**
    -   The `AnyObject`-constrained restriction is lifted so all `any` types including `Any` are allowed, though a generic function still cannot be called on an `any` type.
    -   It also adds `throws` without a declared error type, metatypes, string-to-double parsing such as `Double(inputText)`, and throwing task groups.
    -   Performance-sensitive code can enable the `PerformanceHints` diagnostic group to get warnings about dynamic feature use.
    [Source URL](https://www.swift.org/blog/embedded-swift-improvements-coming-in-swift-6.4/) (Swift.org)
    > Takeaway: This is still development-snapshot only, so start by listing the `AnyObject` constraints and typed throws you worked around in Embedded targets.

---

### Kotlin Architecture

*   **Kotlin domain errors belong in the signature, not in exceptions — sealed interface plus Either**
    -   Of the three failure kinds — API client errors (4xx), unexpected exceptions (500s), and domain errors — only domain errors go into the type contract.
    -   Instead of `Result<T>` or `Either<Throwable, T>`, enumerate failures with a sealed interface such as `Either<DocumentSignError, T>` so `when` stays exhaustive.
    -   Chain with an early return via `getOrElse` or Arrow's `either { }` and `bind()`, and map to HTTP at exactly one place, the route boundary.
    [Source URL](https://blog.jetbrains.com/kotlin/2026/08/signatures-be-true-domain-errors-and-functional-handling-in-kotlin/) (JetBrains Kotlin Blog)
    > Takeaway: If your services or repositories leak business failures as exceptions, narrow them into a per-method sealed error type.

---

Today's items split evenly between squeezing more tokens out of a phone and making execution boundaries and failure paths explicit outside the code.
