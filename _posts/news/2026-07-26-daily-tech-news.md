---
layout: post
title: "데일리 테크 뉴스 - 2026-07-26"
date: 2026-07-26 06:02:15 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## 오늘의 개발자 뉴스: Claude Opus 5 API, Stateless MCP, PostgreSQL 알림 확장, Android On-Device ADB 논의

2026년 7월 26일 기준으로 Claude Opus 5의 공식 API와 agent 제어 기능, stateless core로 전환하는 차기 MCP 사양, PostgreSQL `LISTEN/NOTIFY`의 global lock 병목을 우회한 실험, Android 기기 내부 ADB 연결을 제한할 수 있다는 초기 논의를 정리했습니다. 주가, 실적, 경영진 중심 뉴스는 제외했습니다.

---

### AI Model APIs

*   **Anthropic, Claude Opus 5와 실행 중 tool 변경·자동 fallback beta 공개**
    Claude Opus 5는 Claude API에서 `claude-opus-5`로 제공되며 가격은 input 100만 token당 5달러, output 100만 token당 25달러로 Opus 4.8과 같습니다. Fast mode는 약 2.5배 빠른 대신 기본 가격의 두 배입니다. 개발자 관점에서 함께 나온 beta 두 가지가 중요합니다. 대화 도중 사용 가능한 tool을 바꿔도 prompt cache가 무효화되지 않으며, safety classifier에 걸린 요청을 차단하는 대신 다른 model로 자동 전달하도록 설정할 수 있습니다. 다만 source-code vulnerability 탐지는 허용하면서 binary scanning, penetration testing, exploit generation은 제한하고, Claude 앱과 Claude Code에서는 해당 요청이 기본적으로 Opus 4.8로 fallback될 수 있습니다. model 이름만 교체하는 migration이라도 비용·latency뿐 아니라 fallback 시 model identity와 결과 차이를 telemetry에 기록하는 편이 안전합니다.
    [Source URL](https://www.anthropic.com/news/claude-opus-5) (Anthropic)

---

### Agent Protocols

*   **차기 MCP 사양, session과 `initialize`를 없앤 stateless core로 전환**
    7월 28일 공개 예정인 차기 Model Context Protocol 사양은 session과 `initialize`를 core에서 제거해 client handshake를 병렬화하고 remote server의 수평 확장을 단순화합니다. GitHub MCP Server는 이미 새 사양을 지원하며, Redis session과 요청별 database read를 제거하고 logging·secret scanning에 필요한 값을 보장된 HTTP header에서 읽도록 바꿨습니다. 여러 HTTP round trip이 필요한 elicitation도 새 방식과 이전 client를 함께 처리합니다. Tier 1 SDK는 backward compatibility와 beta 지원을 제공하므로 기존 사용자는 즉시 변경할 필요가 없지만, 직접 만든 client·server는 새 official conformance suite로 session 의존성, header 처리, elicitation 흐름을 미리 검증하는 것이 좋습니다.
    [Source URL](https://github.blog/changelog/2026-07-23-github-mcp-server-supports-the-next-mcp-specification/) (GitHub)

---

### Database Streaming

*   **PostgreSQL `LISTEN/NOTIFY`, 알림을 batch 처리해 초당 6만 stream write 실험**
    DBOS의 벤치마크는 transaction마다 `NOTIFY`를 호출하면 commit 순서를 보장하기 위한 global exclusive lock이 `fsync()`까지 유지돼, CPU·I/O가 남아 있어도 write가 직렬화되는 과정을 보여줍니다. 초기 trigger 방식은 초당 약 2,900건에서 막혔지만, table을 source of truth로 유지한 채 알림을 memory에 buffer하고 한 transaction으로 주기적으로 flush하자 concurrent reader 조건에서 초당 최대 6만 write와 15~100ms latency를 기록했습니다. process crash로 buffer가 사라지는 경우는 낮은 빈도의 polling을 fallback으로 추가했습니다. 공개 benchmark code가 있지만 이는 특정 workload와 단일 server의 결과이므로, production 적용 전 durability 요구, batch interval, connection 수, payload 분포를 자체 부하 테스트해야 합니다.
    [Source URL](https://www.dbos.dev/blog/postgres-listen-notify-scalability) (DBOS)

---

### Android Developer Tooling

*   **Android loopback ADB 제한 가능성, Shizuku·Termux 기반 workflow 영향 논의**
    Hacker News에서 주목받은 기술 분석은 ADB daemon이 binding할 network interface를 선택하게 해 달라는 Google Issue Tracker 요청과, 보안상 `wlan0`만 허용하는 방안을 언급한 ADB maintainer의 답변을 다룹니다. 이 방식이 채택되면 같은 기기의 client가 `127.0.0.1`을 통해 daemon에 연결하는 on-device ADB뿐 아니라 VPN·Ethernet 기반 설정에도 영향을 줄 수 있습니다. Shizuku, `libadb-android`, Termux 기반 mobile development와 rootless power-user app이 대표적인 의존 사례입니다. 다만 이는 Google의 공식 발표나 확정된 Android 변경이 아니라 진행 중인 공개 논의입니다. 관련 도구 maintainer는 loopback 가정이 있는지 점검하고, 영향이 고유하다면 issue에 재현 가능한 use case와 대안을 제공하되 아직 우회 구현을 서두를 단계는 아닙니다.
    [Source URL](https://kitsumed.github.io/blog/posts/android-may-soon-restrict-on-device-adb/) (Kitsumed / Hacker News)

---

오늘의 공통점은 편리한 abstraction 아래 남아 있던 state와 경계가 다시 설계되고 있다는 점입니다. Model API의 fallback, MCP session, PostgreSQL notification ordering, ADB network binding은 평소에는 감춰지지만 성능·보안·호환성 문제에서 핵심이 됩니다. 변경을 도입할 때는 정상 경로만 확인하지 말고 fallback의 관측 가능성, protocol conformance, durability, network topology를 함께 검증해야 합니다.
