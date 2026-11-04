---
title: "Compose 1.13 RC, Apple 구독 retention messages, Transformers MIC (2026. 11. 05)"
description: "Compose 1.13.0-rc01과 Apple retention messages가 나왔고, Transformers는 모델 통합 테스트 MIC를 CI에 붙였습니다."
date: 2026-11-05 08:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## 오늘의 흐름: Compose 1.13 RC, 구독 해지 방어 API, 모델 통합 테스트, 소형 모델 파인튜닝

-   Compose 1.13.0-rc01, Material 3 1.5.0-rc01 동반 공개
-   Apple 구독 retention messages와 Retention Messaging API
-   iOS 27.3 베타 공개, Xcode 27.3 권장
-   Transformers, 축소 fixture 기반 MIC 테스트 도입
-   Palette, 20B 모델로 슬라이드 덱 생성

---

### Android & Apple Toolchain

*   **Compose 1.13.0-rc01 공개 — Material 3도 1.5.0-rc01로 함께 올라왔습니다**
    -   Runtime, UI, Foundation, Animation, Material이 모두 1.13.0-rc01입니다.
    -   Compose Remote는 1.0.0-alpha23, Wear Compose는 1.8.0-alpha03입니다.
    [Source URL](https://developer.android.com/jetpack/androidx/versions/all-channel) (Android Developers)
    > 시사점: 안정판 전에 RC를 별도 브랜치에서 빌드해 보고 회귀가 있으면 일찍 보고하세요.

*   **iOS·iPadOS·macOS·tvOS·visionOS·watchOS 27.3 베타 공개 — Xcode 27.3으로 빌드하길 권장**
    -   여섯 플랫폼 모두 27.3 베타가 열렸습니다.
    -   Xcode 27.3의 베타 여부는 공지에 적혀 있지 않습니다.
    [Source URL](https://developer.apple.com/news/?id=6gpufove) (Apple Developer News)
    > 시사점: CI에 Xcode 27.3 잡을 따로 추가해 빌드 경고부터 확인하세요.

*   **구독 retention messages 정식 제공 — 해지 흐름에서 텍스트·이미지·할인 제안을 보여 줍니다**
    -   App Store Connect에서 대상 구독자와 메시지 간 대기 시간을 설정합니다.
    -   Retention Messaging API로 구독자별 메시지를 앱이 직접 고르며, API는 신청 후 사용할 수 있습니다.
    [Source URL](https://developer.apple.com/news/?id=fk9ps3gv) (Apple Developer News)
    > 시사점: 구독 앱이라면 API 접근 신청을 먼저 넣고 해지 사유별 메시지 후보를 정리해 두세요.

---

### AI Engineering Practice

*   **Transformers, Model Integration Contracts(MIC) 도입 — 축소 모델로 모델 통합을 회귀 테스트**
    -   Llama 4 Scout를 108.6B에서 44.7M 파라미터로 줄여 layer 종류는 모두 유지합니다.
    -   Whisper 실험에서 random-weight fixture는 주입 결함 24개 중 18개, overfit fixture는 24개 전부 잡았습니다.
    -   현재 CI의 MIC 잡은 실패를 보고만 하고 PR을 막지는 않습니다.
    [Source URL](https://huggingface.co/blog/transformers-mic) (Hugging Face)
    > 시사점: 자체 모델 래퍼가 있다면 축소 fixture와 baseline 출력을 고정하는 방식을 CI에 도입해 볼 만합니다.

*   **Palette 공개 — IBM Design Language로 슬라이드 덱을 만드는 20B 오픈 웨이트 모델**
    -   LoRA 어댑터 하나가 designer(JSON brief)와 coder(pptxgenjs)를 겸하고, coder를 병렬로 돌려 6~7배 빨라집니다.
    -   렌더링 후 겹침·잘림을 검사하는 harness가 131개 덱에서 평균 3.5점을 더했습니다.
    -   PresentBench 3개 도메인 평균 59.7점으로 NotebookLM(60.8)에 1.1점 뒤진 2위입니다. (vendor 측정)
    [Source URL](https://huggingface.co/blog/ibm-research/palette-deck-building) (Hugging Face)
    > 시사점: 생성 결과를 렌더링해 검사하고 통과할 때만 채택하는 루프는 우리 에이전트에도 그대로 옮길 수 있습니다.

---

오늘 항목은 모두 베타·RC·실험 단계라, 정식 전환 전에 먼저 돌려 볼 수 있다는 점이 같습니다.
