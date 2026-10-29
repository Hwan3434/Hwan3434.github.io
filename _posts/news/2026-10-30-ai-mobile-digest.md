---
layout: post
title: "Agent Skills AAIF 이관과 Swift 6.4, Apple 27 SDK 마감 (2026. 10. 30)"
description: "Agent Skills 표준이 AAIF로 넘어가고, Swift 6.4와 Apple 2027년 SDK·인증서 마감이 확정됐습니다."
date: 2026-10-30 08:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## 오늘의 흐름: Agent Skills 표준 이관, Swift 6.4, Apple SDK 마감

-   Agent Skills 표준, AAIF로 이관
-   Anthropic 외부 평가 3단계 접근 모델
-   Swift 6.4, Swift Build가 SwiftPM 기본값
-   Apple, 2027년 4월부터 27 SDK 업로드 필수

---

### Agent Tooling

*   **Agent Skills 표준이 Agentic AI Foundation으로 넘어감 — Anthropic은 이름과 도메인까지 기증**
    -   `SKILL.md` 파일을 담은 폴더 구조 표준은 Linux Foundation 산하 AAIF가 맡습니다. 로드맵에는 버전 릴리스와 보안 가이드가 잡혀 있습니다.
    -   에이전트 플랫폼 70개 이상이 연동했고, 공개된 skill은 약 100만 개, 설치는 약 2.8억 건입니다.
    [Source URL](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation) (Anthropic)
    > 시사점: 사내 skill은 `SKILL.md` 규격대로 맞춰 두고, agentskills.io 명세에서 버전 정책이 어떻게 정해지는지 지켜보세요.

---

### Evals

*   **Anthropic이 외부 평가 기관 접근을 3단계로 정리 — METR은 직원급 접근권을 받음**
    -   Tier 1은 Anthropic 승인을 받아야 공개할 수 있고, Tier 2·3은 승인 없이 공개하되 지정된 범주만 redaction할 수 있습니다.
    -   METR 직원 6명은 사내 장비와 도구를 쓰지만, 고객 데이터와 모델 아키텍처 상세는 공유받지 않습니다.
    [Source URL](https://www.anthropic.com/news/an-update-on-independent-evaluators) (Anthropic)
    > 시사점: 벤더 안전성 보고서를 볼 때는 어느 Tier의 평가인지부터 확인하세요.

---

### Swift Toolchain

*   **Swift 6.4 출시 — SwiftPM 기본 빌드 시스템이 Swift Build로 바뀜**
    -   `withTaskCancellationShield`(SE-0504)가 추가됐고, `defer` 안에서 async 호출(SE-0493)도 할 수 있습니다.
    -   Android SDK는 NDK r30 LTS를 기반으로 하고, SwiftPM은 SPDX·CycloneDX 형식 SBOM을 만들어 줍니다(SE-0509).
    [Source URL](https://www.swift.org/blog/swift-6.4-released/) (Swift.org)
    > 시사점: CI에서 Swift 패키지를 빌드한다면 Swift Build로 바뀐 뒤에도 결과가 같은지 먼저 확인하세요.

---

### Apple Platform Deadlines

*   **Apple, 2027년 4월부터 27 SDK 빌드만 업로드 허용 — Developer ID Sub-CA도 2027년 2월 만료**
    -   iOS 27 SDK 계열 빌드는 지금도 제출할 수 있고, 2027년 4월부터는 27 SDK로 빌드해야만 업로드됩니다.
    -   기존 Developer ID Certification Authority(Sub-CA)가 2027년 2월 1일에 만료되므로 해당 인증서를 교체해야 합니다.
    [Source URL](https://developer.apple.com/news/) (Apple Developer News)
    > 시사점: Xcode 27 빌드 파이프라인 전환과 Developer ID 인증서 교체를 2027년 2월 전으로 일정에 잡아 두세요.

---

네 항목이 가리키는 방향은 같습니다. 표준이나 마감이 바뀌기 전에 내 파이프라인의 규격과 일정을 미리 점검해 두라는 것입니다.
