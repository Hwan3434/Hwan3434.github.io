---
layout: post
title: "Daily Tech News - 2026-07-19"
date: 2026-07-19 06:01:30 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## Today's Developer News: AI Code Review Controls, Copilot Metrics, Firefox in WebAssembly, and Lua AOT

Here is a developer-focused digest for July 19, 2026, covering execution and network controls for AI code review, repository-level AI usage metrics, Firefox running inside a browser, and an AOT compiler that turns Lua into native executables. Stock-market, earnings, executive, and broad business news has been excluded.

---

### Operating AI Code Review

*   **GitHub Copilot code review adds branch-level instruction validation and an independent execution environment**
    Copilot code review now reads `copilot-instructions.md`, `AGENTS.md`, agent skills, and related instructions from the pull request's head branch rather than its base, allowing review rules themselves to be tested before merge. It also recognizes `REVIEW.md`, `GEMINI.md`, and `CLAUDE.md`, while `.github/workflows/copilot-code-review.yml` can install dependencies and run preparation steps. Review runners now use a default firewall, with network access and runner type configured separately from the cloud agent. Teams should note that self-hosted runners do not yet support the firewall.
    [Source URL](https://github.blog/changelog/2026-07-17-copilot-code-review-customization-and-configurability-improvements/) (GitHub Changelog)

*   **GitHub makes repository-level Copilot coding agent and code review metrics generally available**
    The Copilot usage metrics REST API for enterprises and organizations now includes daily per-repository report endpoints. Responses cover pull requests created and merged by the coding agent, pull requests examined by Copilot code review, and suggestion counts broken down by comment type. This makes it easier to distinguish repositories where adoption is producing activity instead of relying on organization- or user-level totals. Access requires the `View Copilot Metrics` permission and an enabled usage metrics policy.
    [Source URL](https://github.blog/changelog/2026-07-17-repository-level-github-copilot-usage-metrics-generally-available/) (GitHub Changelog)

---

### WebAssembly and Browser Runtimes

*   **Puter publishes a prototype that compiles Gecko to WebAssembly and runs Firefox inside a browser tab**
    `firefox-wasm` targets the Gecko engine at WebAssembly through Emscripten and proxies network traffic through the WISP protocol, placing Firefox's interface and rendering engine inside another browser. It offers WebGL-based GPU acceleration and an experimental JavaScript-to-Wasm JIT option, although the JIT is not yet usable on many sites. The current early release builds on Linux with Emscripten 6.0.1 and Rust's `wasm32-unknown-emscripten` target, making it more useful as an exploration of large native application ports and sandboxed runtimes than as a production browser.
    [Source URL](https://github.com/HeyPuter/firefox-wasm) (Puter / Hacker News)

---

### Programming Language Tooling

*   **`clx` compiles Lua 5.5 code through a C++20 backend into standalone native executables**
    The beta-stage `clx` project translates Lua source to C++ and then ahead-of-time compiles it with Clang, GCC, or MSVC, producing deployable binaries without an interpreter. It can also emit object files, static modules, or generated C++ source, and says a `--minimal` build can keep small programs below 100 KB. Dynamic code-loading functions, the `debug` module, and the traditional Lua C API remain unsupported because they do not fit the pure AOT model. Its public performance figures vary substantially by workload and are project-authored, so teams should benchmark their own applications before adoption.
    [Source URL](https://github.com/samyeyo/clx) (clx / Hacker News)

---

Today's common thread is a wider automation surface paired with more explicit execution boundaries and validation evidence. AI review can now manage repository instructions, setup steps, and firewalls independently while measuring results per repository. The Firefox and Lua AOT experiments likewise show how established runtimes can move into new deployment forms, but their early compatibility limits and self-reported benchmarks still need direct evaluation.
