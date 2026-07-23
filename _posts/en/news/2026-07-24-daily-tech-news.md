---
layout: post
title: "Daily Tech News - 2026-07-24"
date: 2026-07-24 06:02:18 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## Today's Developer News: Dependabot Supply-chain Defense, a Java JSON API, Unity CLI, and Metrics at Scale

Here is a developer-focused digest for July 24, 2026, covering a dependency-update policy that avoids adopting brand-new packages immediately, a proposed JSON API built into the JDK, a Unity command surface for CI and AI agents, and optimization of a metrics pipeline serving millions of containers. Stock-market, earnings, executive, and broad business news has been excluded.

---

### Software Supply Chain Security

*   **Dependabot now applies a default three-day cooldown to ordinary version updates**
    GitHub has changed Dependabot's default behavior so that non-security version updates wait at least three days after a package release before opening a pull request, reducing the chance that a newly published malicious version enters an automated update pipeline immediately. Security updates that deliver fixes for known vulnerabilities still open without delay, and projects can tune the waiting period through the `cooldown` option in `dependabot.yml`. The GitHub Advisory Database recorded more than 6,500 npm malware advisories in the year ending May 2026, but a cooldown only addresses malicious releases that are exposed and removed quickly. Lockfile pinning, restricting install scripts in CI, narrowly scoped build tokens, and human review of updates remain necessary layers.
    [Source URL](https://github.blog/security/supply-chain-security/the-case-for-a-cooldown-why-dependabot-now-waits-before-issuing-version-updates/) (GitHub)

---

### Java Platform

*   **JEP 540 proposes a small standard JSON API that needs no external library**
    Updated on July 23, JEP 540 proposes the incubating `jdk.incubator.json` API for parsing and generating RFC 8259-compliant JSON documents. Its `JsonValue`-centered tree model focuses on navigating known structures and handling missing or unexpected values, while deliberately excluding data binding, streaming, and extended syntaxes such as JSON5. The goal is not to replace Jackson or Gson, but to offer a built-in option for simple scripts, tools, and potential JDK configuration use cases where an external dependency would be excessive. The JEP is currently a `Candidate`, not a feature confirmed in a production JDK, so both the API and its target release can still change during review.
    [Source URL](https://openjdk.org/jeps/540) (OpenJDK)

---

### Game Development Automation

*   **Unity CLI manages editors, projects, modules, and authentication from the terminal and can control a running project**
    The standalone `unity` binary, currently available as a beta, installs editors and modules and opens projects without a UI. JSON and TSV output, defined exit codes, non-interactive installation, and service-account authentication make it suitable for CI automation. The experimental `com.unity.pipeline` package sends local API commands to a running Editor or development Player on Unity 6.0 LTS or later; projects can expose methods with `[CliCommand]`, while `unity command eval` executes C# immediately. This gives AI agents a loop for opening, changing, testing, and verifying a project in Play mode. Runtime endpoints are localhost-only and disabled by default, `eval` is protected by a security token, and production automation should account for the Pipeline API's experimental status with version pinning and careful permission boundaries.
    [Source URL](https://unity.com/blog/meet-the-unity-cli) (Unity)

---

### Observability Infrastructure

*   **NAVER optimizes VictoriaMetrics for millions of containers across query, storage, and collection layers**
    NAVER Search split a cluster-wide container aggregation into 36 queries based on the first character of a label, distributing result merging instead of concentrating it in one `vmselect`. Per-query memory use fell from 45% to 12%, while maximum API response time dropped from 40 seconds to seven. Analysis showing that 99.997% of queries covered the most recent month also supported reducing the Hot Tier `RetentionPeriod` from 12 to six months. Finally, the team stopped collecting from non-service containers, which accounted for more than 90% of collection targets; collected containers fell 91.6%, active time series 63.6%, and ingestion rate 64.4%. The broader lesson is to observe query fan-out, IndexDB rotation, retention demand, and collection cardinality as one pipeline instead of only raising resource limits.
    [Source URL](https://d2.naver.com/helloworld/5788040) (NAVER D2)

---

Today's common thread is that automation speed must be matched by clear adoption boundaries. New dependencies need time for scrutiny, a standard-API proposal must be distinguished from a shipped release, and an agent command surface needs explicit permissions and review points. At observability scale, real query and collection data may also justify reducing scope before buying more hardware.
