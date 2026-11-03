---
title: "Siri AI 개발자 프리뷰, CWE-bench v2, StateBench (2026. 11. 04)"
description: "Siri AI가 App Intents 기반 개발자 프리뷰로 열리고, CWE-bench v2와 StateBench가 에이전트 한계를 수치로 보여 줍니다."
date: 2026-11-04 08:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## 오늘의 흐름: Siri AI 개발자 프리뷰, 보안 수정 벤치마크, 상태 추적 한계, Android Dev Summit 세션

-   Siri AI, App Intents로 앱 연동 프리뷰 시작
-   Android Dev Summit 세션 50여 개 공개
-   CWE-bench v2, 보안 취약점 수정 100개 과제
-   StateBench, 긴 문서의 상태 추적 평가
-   Qwen 3.8 27B가 노트북에서 가중치 해석

---

### Siri AI & Android Dev Summit

*   **Siri AI 개발자 프리뷰 시작 — App Intents로 앱의 콘텐츠와 액션을 Siri AI에 연결**
    -   iOS·iPadOS·macOS·visionOS 27.3 베타부터 모든 개발자가 쓸 수 있고 App Store 제출은 봄에 열립니다.
    -   여러 액션을 묶는 skills를 정의할 수 있고 Spotlight semantic index의 어떤 entity든 Siri AI가 불러옵니다.
    -   EU 지역의 iOS·iPadOS·watchOS에서는 아직 쓸 수 없습니다.
    [Source URL](https://developer.apple.com/news/?id=gdk2umrf) (Apple Developer News)
    > 시사점: 주문·예약·조회 같은 핵심 기능이 있다면 App Intents로 노출되어 있는지 27.3 베타에서 먼저 확인하세요.

*   **Android Dev Summit 세션 50여 개 공개 — 슬라이드가 합쳐진 전체 transcript 제공**
    -   트랙은 App Foundations, Intelligent Apps, Tools and Performance, Android XR 네 가지입니다.
    -   트랙마다 Gemini Notebook이 있고 transcript는 내려받아 에이전트에 바로 넣을 수 있습니다.
    [Source URL](https://developer.android.com/blog/posts/building-apps-developer-sessions) (Android Developers Blog)
    > 시사점: Tools and Performance 트랙의 transcript를 에이전트에 넣어 우리 앱에 적용할 항목만 추려 보세요.

---

### Agent Benchmarks

*   **CWE-bench v2 공개 — 에이전트가 실제 오픈소스 저장소의 보안 취약점을 고치는 100개 과제**
    -   91개 CWE를 다루고 채점을 프로그램이 결정적으로 처리해 재현에 비용이 들지 않습니다.
    -   pass@1은 Gemini 4 Argon 67.8%, Claude Opus 5.5 67.3%입니다.
    -   DeepSeek V4.1 Flash는 rollout당 약 $0.04로 57.0%, Opus는 $1.83입니다.
    [Source URL](https://huggingface.co/blog/cwe-bench) (Hugging Face)
    > 시사점: 취약점 수정을 에이전트에 맡길 계획이라면 모델 선택 전에 rollout당 비용과 pass@1을 같이 비교하세요.

*   **StateBench 공개 — 긴 문서에서 변수 상태 변화를 따라가는 능력을 4단계로 평가**
    -   Claude Opus 5.5와 GPT-6 Sol을 포함한 frontier 모델은 가장 어려운 단계의 가장 긴 입력에서 정확도가 13% 이하로 떨어졌습니다.
    -   직접 학습시킨 275M 모델에서는 Gated DeltaNet과 hybrid 구조가 학습 길이의 약 250배까지 거의 완벽하게 일반화했습니다.
    -   transformer는 가장 어려운 단계를 끝내 학습하지 못했습니다.
    [Source URL](https://huggingface.co/blog/allenai/statebench) (Hugging Face)
    > 시사점: 긴 로그나 설정 변경 이력을 모델이 추적하게 할 때는 중간 상태를 직접 요약해 넘기는 쪽이 안전합니다.

---

### On-Device Inference

*   **Qwen 3.8 27B가 노트북에서 신경망 가중치를 읽고 게임을 식별 — 도구 없이 raw weights만 입력**
    -   Q4_K_M GGUF(약 17GB)를 LM Studio로 돌렸고, 4개 게임 중 Breakout, Pong, Pac-Man은 맞히고 Freeway는 틀렸습니다.
    -   Pac-Man 판별에는 46분 12초와 reasoning token 43,506개가 들었습니다.
    -   같은 과제에서 Kimi K3.1 Pro(OpenRouter)는 Breakout을 9분 41초에 맞혔습니다.
    [Source URL](https://simonwillison.net/2026/Nov/3/qwen-can-interpret-model-weights/) (Simon Willison)
    > 시사점: 당장 조치는 불필요합니다.
