---
layout: post
title: "Agent Skills 재단 이관, Anthropic Scion, Swift 6.4 (2026. 10. 29)"
description: "Agent Skills가 재단으로 이관되고, Anthropic이 Scion으로 옮겼으며, Swift 6.4와 App Review 개정이 나왔습니다."
date: 2026-10-29 08:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## 오늘의 흐름: 에이전트가 쓰는 도구와 인프라의 규격이 바뀌는 날

-   Agent Skills가 Linux Foundation 산하로 이관
-   Anthropic이 모노레포를 git에서 Scion으로 이전
-   Swift 6.4, SwiftPM 기본 빌드가 Swift Build로
-   App Review에 2.5.19 신설, 3.1.1(a) 개편

---

### Agent Tooling

*   **Agent Skills 표준이 Agentic AI Foundation으로 이관 — 이름, 로고, GitHub org까지 넘어감**
    -   스킬은 `SKILL.md`와 스크립트·참고 자료를 담은 폴더이고 70개 넘는 에이전트 플랫폼이 연동했습니다.
    -   공개 스킬은 100만 개, 설치는 약 2억 8천만 건입니다 (vendor 측정).
    -   로드맵에는 버전 릴리스, 공식 제안 절차, 스킬 작성·설치용 보안 가이드가 올라 있습니다.
    [Source URL](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation) (Anthropic)
    > 시사점: 스킬을 직접 만든다면 agentskills.io 명세를 기준으로 삼고 버전 정책이 나오는지 지켜보세요.

---

### Source Control for Agents

*   **Anthropic이 모노레포를 git에서 Scion으로 이전 — 에이전트 규모에서 git이 병목이 됨**
    -   하루 병합 변경이 2026년 5월 약 2,500건에서 9월 3만 건 넘게 늘었고 CI 체크아웃은 하루 약 2,500만 회입니다 (vendor 측정).
    -   changeset 기반 서버 중심 설계로 인프라 CPU와 메모리가 기존 git 미러 대비 약 200배 줄었습니다 (vendor 측정).
    -   저자들은 범용 git 대체가 아니라고 밝히며 서버 측 RPC와 sparse 기능을 git 플랫폼이 가져가길 제안합니다.
    [Source URL](https://www.anthropic.com/research/redesigning-source-control) (Anthropic)
    > 시사점: 당장 조치는 불필요합니다.

---

### Swift Toolchain

*   **Swift 6.4 출시 — SwiftPM 기본 빌드 시스템이 Swift Build로 바뀜**
    -   SwiftPM이 SBOM 생성(SE-0509)을 SPDX와 CycloneDX로 내보내고 `defer` 안에서 `await`를 쓸 수 있습니다(SE-0493).
    -   Android SDK는 NDK r30(LTS)로 빌드되며 SwiftPM에서 후처리 스크립트 없이 Android를 지원합니다.
    -   Wasm에서 JavaScriptKit 브리징이 최대 40배 빨라졌습니다 (vendor 측정).
    [Source URL](https://swift.org/blog/swift-6.4-released/) (Swift.org)
    > 시사점: Swift 패키지를 쓰는 CI가 있다면 Swift Build 전환 뒤에도 빌드 결과가 같은지 먼저 확인하세요.

---

### App Store Policy

*   **App Review Guidelines 개정 — 숨은 기능 조항이 2.5.19로 분리되고 3.1.1(a)가 정리됨**
    -   2.5.19가 신설되어 숨겨졌거나 문서화되지 않은 기능 정책이 기존 2.3.1에서 옮겨 왔습니다.
    -   3.1.1(a)에서 Music Streaming Services Entitlements 항목이 빠지고 StoreKit External Purchase Link Entitlements 항목에 합쳐졌습니다.
    -   2.3.14는 creative assets를 다루는 신규 조항입니다.
    [Source URL](https://developer.apple.com/news/?id=92th7e5i) (Apple Developer News)
    > 시사점: 외부 결제 링크나 음악 스트리밍 entitlement를 쓰는 앱은 3.1.1(a) 변경분을 심사 제출 전에 대조하세요.
