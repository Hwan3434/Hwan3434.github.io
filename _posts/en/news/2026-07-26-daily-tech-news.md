---
layout: post
title: "Daily Tech News - 2026-07-26"
date: 2026-07-26 06:02:15 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## Today's Developer News: Claude Opus 5 API, Stateless MCP, PostgreSQL Notification Scaling, and Android On-Device ADB

Here is a developer-focused digest for July 26, 2026, covering the official Claude Opus 5 API and agent controls, the next MCP specification's stateless core, an experiment that works around PostgreSQL `LISTEN/NOTIFY`'s global-lock bottleneck, and an early discussion about restricting on-device ADB connections. Stock-market, earnings, executive, and broad business news has been excluded.

---

### AI Model APIs

*   **Anthropic releases Claude Opus 5 with beta support for mid-conversation tool changes and automatic fallbacks**
    Claude Opus 5 is available through the Claude API as `claude-opus-5` at $5 per million input tokens and $25 per million output tokens, unchanged from Opus 4.8. Fast mode runs about 2.5 times faster at twice the base price. Two accompanying beta features are particularly relevant to agent developers: an application can change the tools available during a conversation without invalidating the prompt cache, and it can automatically route a request flagged by a safety classifier to another model instead of returning a block. The safeguards allow source-code vulnerability discovery but restrict binary scanning, penetration testing, and exploit generation; in Claude apps and Claude Code, affected requests can fall back to Opus 4.8 by default. Even a model-name-only migration should record fallback model identity in telemetry alongside cost and latency because the effective model and output may change.
    [Source URL](https://www.anthropic.com/news/claude-opus-5) (Anthropic)

---

### Agent Protocols

*   **The next MCP specification moves to a stateless core without sessions or `initialize`**
    The next Model Context Protocol specification, scheduled for July 28, removes sessions and `initialize` from the core, allowing clients to parallelize the handshake and making remote servers easier to scale horizontally. GitHub MCP Server already supports the new specification. It removed Redis sessions and per-call database reads, and now obtains values needed for logging and secret scanning from guaranteed HTTP headers instead of inspecting every request payload. Its elicitation implementation also supports the new multi-request flow while remaining compatible with older clients. Tier 1 SDKs preserve backward compatibility and have shipped beta support, so existing users do not need an immediate change. Authors of bespoke clients and servers should still run the new official conformance suite to find session assumptions and validate header and elicitation behavior.
    [Source URL](https://github.blog/changelog/2026-07-23-github-mcp-server-supports-the-next-mcp-specification/) (GitHub)

---

### Database Streaming

*   **A PostgreSQL `LISTEN/NOTIFY` design reaches 60,000 stream writes per second by batching notifications**
    DBOS's benchmark shows why calling `NOTIFY` in every transaction can serialize writes even when CPU and I/O remain available: PostgreSQL holds a global exclusive lock through `fsync()` to preserve notification commit order. Its initial trigger-based implementation stalled around 2,900 writes per second. Keeping the table as the source of truth while buffering notifications in memory and periodically flushing them in one transaction produced up to 60,000 writes per second with concurrent readers and 15–100ms latency. Low-frequency polling provides a fallback for notifications lost if the buffering process crashes. The benchmark code is public, but these are results for a specific workload on one server; production users should test their own durability requirements, batch interval, connection count, and payload distribution.
    [Source URL](https://www.dbos.dev/blog/postgres-listen-notify-scalability) (DBOS)

---

### Android Developer Tooling

*   **A possible Android loopback ADB restriction raises concerns for Shizuku- and Termux-based workflows**
    A technical analysis gaining attention on Hacker News examines a Google Issue Tracker request to let developers choose which network interface the ADB daemon binds to, plus a response from an ADB maintainer discussing a security-motivated option that would allow only `wlan0`. If adopted, that approach could affect on-device ADB, where a client on the same phone connects to the daemon through `127.0.0.1`, as well as VPN- and Ethernet-based setups. Shizuku, `libadb-android`, Termux mobile-development workflows, and rootless power-user apps are prominent dependent use cases. This is an ongoing public discussion, not an official Google announcement or a finalized Android change. Maintainers should audit their loopback assumptions and contribute reproducible use cases and alternatives when uniquely affected, but it is too early to build around a presumed final design.
    [Source URL](https://kitsumed.github.io/blog/posts/android-may-soon-restrict-on-device-adb/) (Kitsumed / Hacker News)

---

Today's common thread is the redesign of state and boundaries hidden beneath convenient abstractions. Model fallback, MCP sessions, PostgreSQL notification ordering, and ADB network binding are easy to ignore until they become performance, security, or compatibility constraints. Adoption checks should therefore cover fallback observability, protocol conformance, durability, and network topology—not only the happy path.
