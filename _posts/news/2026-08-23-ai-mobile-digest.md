---
layout: post
title: "AI · 모바일 다이제스트 - 2026-08-23"
date: 2026-08-23 06:10:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## 오늘의 흐름: 폰 안으로 들어온 structured output, 기본값 하나가 삼킨 TTFT 20초

-   Firebase AI Logic, 온디바이스 `generateObject` 추가
-   Android Studio Rabbit 1, Play 테스트 트랙 직접 업로드
-   토스: prefix cache가 꺼진 채 TTFT 20초
-   Qwen3-TTS, p95 TTFA 50ms 미만
-   llm 0.33, openai 3.x와 httpx2로 이동

---

### On-Device Inference

*   **Firebase AI Logic 17.16.0 — 온디바이스 추론에서도 `generateObject`로 structured output을 받을 수 있음**
    -   Android BoM `34.18.0`에 포함되고, 같이 나온 On-Device SDK `16.0.0-beta05`는 모델 선택을 받습니다.
    -   같은 릴리스에서 deprecated Imagen 메서드와 타입이 제거됐고, Imagen 모델 자체가 2026년 8월에 종료됩니다.
    -   Apple SDK `12.18.0`에는 `LiveSession`에 `sendStartActivityRealtime`/`sendStopActivityRealtime`가 추가됐습니다.
    [Source URL](https://firebase.google.com/support/release-notes/android) (Firebase Release Notes)
    > 시사점: Imagen 호출이 남아 있다면 BoM을 올리기 전에 Gemini Image 모델로 먼저 이전하세요.

---

### Android Tooling

*   **Android Studio Rabbit 1(2026.2.1) canary — Generate Signed App Bundle에서 Play 테스트 트랙으로 바로 업로드**
    -   신규 앱의 첫 릴리스는 internal test track으로, 이후 릴리스는 다른 테스트 트랙으로도 올릴 수 있습니다.
    -   Compose Preview Screenshot Testing이 HTML 리포트로 UI 변경을 눈으로 비교하게 해줍니다.
    -   Model Assignment 탭에서 Agent Mode에는 pro급, 지연에 민감한 작업에는 경량 모델을 따로 지정합니다.
    [Source URL](https://developer.android.com/studio/preview/features) (Android Developers)
    > 시사점: 내부 배포에 별도 CI 스텝을 두고 있다면 canary에서 이 경로가 그걸 대체할 수 있는지 재보세요.

---

### LLM Serving

*   **토스가 사내 LLM 서빙 TTFT 20초의 범인으로 모델 기본값에서 꺼져 있던 prefix cache를 지목**
    -   켜고 나서 prefix cache hit rate가 90%를 넘고 TTFT는 약 1/10로 떨어졌습니다.
    -   throughput이 1,000 TPS 근처인데 KV cache 사용률은 1% 미만이라 GPU 증설 없이 4배 트래픽 여유가 확인됐습니다.
    -   thinking token 처리 vLLM 버그로 출력이 잘리던 문제를 잡아 에러율이 0.2%에서 0.02%로 내려갔습니다.
    [Source URL](https://toss.tech/article/tech_talk_talk_2) (토스 기술블로그)
    > 시사점: 자체 서빙 중이라면 모델별 prefix cache 기본값과 KV cache 사용률부터 대시보드에 올리세요.

---

### Speech Serving

*   **Nari Labs가 Qwen3-TTS 1.7B를 H100 한 장에서 p95 TTFA 50ms 미만으로 서빙 (vendor 측정)**
    -   10 RPS에서 초당 약 630자, 20 RPS에서도 TTFA는 100ms 아래를 유지합니다.
    -   앞부분 무음을 잘라내는 dynamic silence trimming만으로 TTFA가 약 80ms 줄었습니다.
    -   Talker·Code Predictor·Codec을 스케줄러 하나로 묶고 고정 15스텝 구간에 CUDA graph를 씌웠습니다.
    [Source URL](https://nari-labs.com/blog/qwen3-tts-speed-cost-frontier/) (Nari Labs)
    > 시사점: 음성 응답 지연을 줄일 계획이면 모델 교체보다 무음 트리밍과 스케줄러 통합을 먼저 재보세요.

---

### Agent Tooling

*   **llm 0.33 — OpenAI Python 3.x로 올라가면서 HTTP 클라이언트가 `httpx`에서 `httpx2`로 교체됨**
    -   전날 0.32.1은 신규 설치 실패를 막으려 `openai<3`을 임시로 핀한 핫픽스였습니다.
    -   `-t/--template`를 반복해서 줄 수 있어 모델 설정용 템플릿과 프롬프트용 템플릿을 겹쳐 씁니다.
    -   Responses API 계열 reasoning 모델에 `reasoning_summary`가 `auto`/`concise`/`detailed`로 붙습니다.
    [Source URL](https://simonwillison.net/2026/Aug/22/llm/) (Simon Willison)
    > 시사점: llm 플러그인을 유지 중이라면 `httpx` 직접 의존이 남아 있는지부터 확인하세요.

---

오늘 항목은 모델을 바꾸는 대신 기본값과 릴리스 배관을 손대는 쪽에서 성과가 나온다는 점에서 겹칩니다.
