---
layout: post
title: "Agent Skills의 AAIF 이관, Swift 6.4, App Store 연령 등급 신규 항목 (2026. 11. 03)"
description: "Agent Skills가 Linux Foundation 산하 AAIF로 넘어가고, Swift 6.4가 나왔으며, App Store Connect에 연령 등급 항목이 추가됩니다."
date: 2026-11-03 08:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## 오늘의 흐름: 에이전트 표준의 중립 이관, 외부 평가자 접근권, Swift 6.4와 App Store 규정

-   Agent Skills, Linux Foundation 산하 AAIF로 이관
-   METR 직원 6명, Anthropic 내부 시스템 접근
-   Swift 6.4 정식 출시, Swift Build가 기본
-   연령 등급 신규 항목, 2027년 1월 12일까지 응답

---

### Agent Ecosystem

*   **Anthropic이 Agent Skills를 AAIF에 기부 — 에이전트 스킬 표준이 벤더 중립으로 넘어감**
    -   스킬은 `SKILL.md`가 든 폴더 형태이고, 70개 이상의 에이전트 플랫폼이 지원하며 누적 설치는 약 2.8억 건입니다.
    -   로드맵에는 버전 릴리스, 공식 제안 절차, 스킬 작성자·설치자용 보안 가이드가 올라 있습니다.
    [Source URL](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation) (Anthropic)
    > 시사점: 스킬을 직접 만들어 쓴다면 이후 버전 정책과 보안 가이드가 나올 때 형식이 바뀌는지 확인하세요.

*   **Anthropic이 외부 평가자에게 내부 접근권을 확대 — METR 직원 6명이 사내 도구를 직접 사용**
    -   접근 수준은 3단계이며, 3단계인 METR은 Anthropic의 승인 없이 결과를 공개할 수 있고 기밀 범주만 삭제를 요구받습니다.
    -   SecureBio는 2026년 8월 Risk Report의 화학·생물 무기 챕터를 검토 중입니다.
    [Source URL](https://www.anthropic.com/news/an-update-on-independent-evaluators) (Anthropic)
    > 시사점: 당장 조치는 불필요합니다.

---

### Swift & App Store

*   **Swift 6.4 출시 — Swift Build가 SwiftPM 기본 빌드 시스템이 됨**
    -   `await`를 `defer` 안에서 쓸 수 있고(SE-0493), `withTaskCancellationShield`로 취소와 무관한 정리 작업을 돌릴 수 있습니다(SE-0504).
    -   `@Observable`에 세밀한 변경 알림(SE-0506)이 들어갔고, SBOM을 SPDX·CycloneDX 형식으로 생성합니다(SE-0509).
    -   Android는 NDK 30으로 빌드합니다.
    [Source URL](https://swift.org/blog/swift-6.4-released/) (Swift.org)
    > 시사점: CI에서 SwiftPM 빌드 결과가 달라지는지 Swift Build 전환 후 한 번 비교해 보세요.

*   **App Store Connect에 연령 등급 항목 2개 추가 — 11월 16일부터 응답 가능, 2027년 1월 12일이 기한**
    -   새 항목은 Shared Location과 Dating and Relationships이고, 후자는 최소 18+ 등급이 됩니다.
    -   브라질에서는 각각 A16과 A18이 적용됩니다.
    [Source URL](https://developer.apple.com/news/) (Apple Developer News)
    > 시사점: 위치 공유나 만남 기능이 있는 앱은 2027년 1월 12일 전에 항목을 채우세요.

---

네 항목 모두 표준이나 규정이 정리되면서 개발자가 확인할 체크리스트가 생겼다는 점이 같습니다.
