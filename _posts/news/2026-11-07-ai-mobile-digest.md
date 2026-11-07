---
title: "Anthropic 에이전트 메모리 dreaming, Siri AI 개발자 프리뷰, 구독 Retention messages (2026. 11. 07)"
description: "Anthropic이 에이전트 메모리 실험을 공개하고, Apple은 Siri AI 개발자 프리뷰와 구독 리텐션 메시지를 내놨습니다."
date: 2026-11-07 08:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## 오늘의 흐름: 에이전트 메모리 설계, 가중치를 읽는 LLM, Siri AI와 구독 이탈 방어

-   에이전트 메모리, dreaming으로 벤치마크 상승
-   GPT-6 Astra 가중치 해석 주장, 로컬 Qwen으로 재현
-   Siri AI, App Intents로 연동하는 개발자 프리뷰
-   구독 취소 흐름에 Retention messages 추가

---

### Agent Memory

*   **Anthropic이 에이전트 메모리의 구성 요소를 정리 — 오프라인 정리 단계 dreaming이 핵심**
    -   CL-Bench 1.0 database 과제에서 Opus 5.5의 평균 보상이 메모리 도입 후 0.655에서 0.838로 올랐습니다.
    -   "실패만 기록하라"는 고정 규칙은 오히려 성능을 깎았고, Opus 5는 0.234 떨어졌습니다.
    -   Claude Code auto memory는 `MEMORY.md`의 첫 200줄 또는 25KB만 불러옵니다.
    [Source URL](https://www.anthropic.com/research/components-of-agent-memory) (Anthropic)
    > 시사점: 에이전트에 메모리를 붙일 때는 쓰는 방법을 규정하지 말고 용도만 알려 주고, 상시 로드되는 파일은 짧게 유지하세요.

*   **"가중치만 보고 학습 목적을 맞춘다"는 논문 주장 — Simon Willison이 로컬 Qwen 3.8 27B로 재현**
    -   논문은 GPT-6 Astra가 Qwen3.5-0.8B 가중치의 0.016%를 고쳐 MATH-500을 7.9%에서 48.1%로 올렸다고 주장합니다.
    -   Q4_K_M GGUF(약 17GB)로 LM Studio에서 돌린 결과 Breakout은 52분, Pong은 1시간 5분 걸렸고 Freeway는 틀렸습니다.
    -   도구 없이 읽는 실험과 도구를 쓴 편집 실험을 섞었다는 비판이 함께 나왔습니다.
    [Source URL](https://simonwillison.net/2026/Nov/3/qwen-can-interpret-model-weights/) (Simon Willison)
    > 시사점: 당장 조치는 불필요합니다.

---

### Apple Platform

*   **Siri AI가 모든 개발자에게 열림 — 27.3 베타에서 App Intents로 연동**
    -   새로 생긴 skills로 여러 액션을 묶어 복합 요청을 처리하게 할 수 있고, Spotlight semantic index의 모든 entity가 노출됩니다.
    -   EU의 iOS·iPadOS·watchOS에서는 쓸 수 없고, App Store 제출은 2027년 봄에 열립니다.
    -   서버 측 Apple Intelligence 기능에는 일일 사용 한도가 있습니다.
    [Source URL](https://developer.apple.com/news/?id=gdk2umrf) (Apple Developer News)
    > 시사점: 앱의 핵심 기능을 `App Intents` entity로 노출해 두고 27.3 베타에서 Siri AI 동작을 미리 확인하세요.

*   **구독 취소 흐름에 Retention messages 추가 — App Store Connect에서 설정**
    -   메시지에는 텍스트, 이미지, 특별 제안을 넣을 수 있고, 구독자 자격과 노출 간격을 구독별로 정합니다.
    -   Retention Messaging API는 요청해야 쓸 수 있으며, 구독 정보에 따라 메시지를 골라 보여 줍니다.
    [Source URL](https://developer.apple.com/news/?id=fk9ps3gv) (Apple Developer News)
    > 시사점: 자동 갱신 구독 앱이라면 App Store Connect에서 설정을 켜 보고, 서버 연동이 필요하면 API 접근을 신청하세요.

---

네 항목 모두 에이전트가 무엇을 기억하고 읽고 호출하는지 개발자가 직접 설계해야 하는 영역으로 넘어왔다는 점이 같습니다.
