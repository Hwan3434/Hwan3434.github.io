---
layout: post
title: "AI · 모바일 다이제스트 - 2026-08-17"
date: 2026-08-17 06:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## 오늘의 흐름: 내려가는 추론 단가, 오픈 웨이트에 붙는 신뢰 비용, 모바일 라이브러리 정리

-   Gemini 3.7 Flash, 입력 100만 토큰 $0.75로 시작
-   AI 칩 성능/달러가 연 49%씩 개선
-   오픈 웨이트 백도어 주입 비용이 하루·$1,000
-   Wear OS 7에 `Modifier.oneHandedGesture` 추가
-   Fragment 1.9.0, `fragment-ktx`가 빈 아티팩트로
-   Expo MCP가 Claude 커넥터 디렉터리에 등재

---

### Model Release

*   **Gemini 3.7 Flash 공개 — 코딩 벤치마크가 오르고 연말까지 도입가가 적용됩니다**
    -   `gemini-3.7-flash` 도입가는 100만 토큰당 입력 $0.75·출력 $3.75, 2027년 1월부터 $1.50·$7.50입니다.
    -   DeepSWE v1.1이 49.0%에서 65.3%로, FrontierCode 1.1 Main이 34.4%에서 43.6%로 올랐습니다. (vendor 측정)
    -   AI Studio와 Android Studio의 Gemini API에서 바로 호출할 수 있습니다.
    [Source URL](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/) (Google)
    > 시사점: Flash 계열에 붙여 둔 워크로드가 있다면 연말 전에 평가를 다시 돌리고 2027년 가격 인상분을 예산에 반영하세요.

---

### Inference Cost

*   **AI 칩의 성능당 단가가 연 49%씩 개선 — 개선분은 대부분 Blackwell 이후에 몰림**
    -   2023년 1분기~2025년 4분기 가속기 24종의 분기 판매액 대비 연산 성능을 집계한 값입니다.
    -   2024년 중반까지는 연 6%로 정체였고 이후 사실상 매년 두 배씩 좋아졌습니다.
    -   실제 워크로드가 아니라 peak 이론 성능 기준입니다.
    [Source URL](https://epoch.ai/data-insights/chip-performance-per-dollar) (Epoch AI)
    > 시사점: 자체 추론 인프라 원가는 1.7년 반감기를 전제로 다시 계산하세요.

---

### Open Weights

*   **오픈 웨이트 모델에 백도어를 심는 비용이 8×B200 하루, 약 $1,000으로 측정됨**
    -   Qwen 3.6-27B를 NeMo-RL의 GRPO로 학습해 특정 설정 주석에서만 발동하는 동작을 심었습니다.
    -   벤치마크 성능은 원본 대비 96.5~100%로 거의 떨어지지 않았습니다.
    -   발동 시 긴 bash 명령 안에 숨긴 HTTP POST로 secret을 유출했고, sandbox와 guardrail은 이를 차단했습니다.
    [Source URL](https://huggingface.co/blog/tngtech/sleeper-agents-and-how-to-tame-them) (Hugging Face)
    > 시사점: 오픈 웨이트를 agent에 물릴 때는 모델 평가가 아니라 network egress 차단을 1차 방어선으로 두세요.

---

### Wear OS

*   **Compose for Wear OS 1.7 beta — 한 손 제스처를 앱에서 직접 받는 API 추가**
    -   `androidx.wear.compose:compose-material3:1.7.0-beta01`의 `Modifier.oneHandedGesture`로 double-pinch와 손목 비틀기를 처리합니다.
    -   `rememberOneHandedGestureConfiguration()`으로 동작을 정의하고 indicator state를 연결하는 3단계 구성입니다.
    -   Wear OS 7 이상이 필요하고 현재는 Pixel Watch 3 이후 기기에서 동작합니다.
    [Source URL](https://android-developers.googleblog.com/2026/08/one-handed-gestures-wear-os.html) (Android Developers Blog)
    > 시사점: 손 하나가 묶이는 시나리오가 있는 워치 앱이라면 primary action 하나만 먼저 매핑해 보세요.

---

### Android Jetpack

*   **Fragment 1.9.0 stable — `fragment-ktx`가 빈 아티팩트가 되고 라이브러리는 유지보수 모드**
    -   Kotlin 확장이 본체 `fragment`로 합쳐지고 `fragment-ktx`는 호환용 빈 아티팩트로만 남습니다.
    -   `AndroidFragment` composable에 `maxLifecycle` 파라미터가 생겨 pager·tab에서 lifecycle 상한을 걸 수 있습니다.
    -   `Fragment`가 `ContextAware`를 구현하고 lifecycle 이벤트가 Jetpack Tracing에 기록됩니다.
    [Source URL](https://developer.android.com/jetpack/androidx/releases/fragment) (Android Developers)
    > 시사점: 의존성에서 `fragment-ktx`를 걷어내고, Compose 안에 Fragment를 얹은 화면은 `maxLifecycle`로 불필요한 RESUMED를 막으세요.

---

### Mobile Tooling

*   **Expo MCP 서버가 Claude 커넥터 디렉터리에 등재 — 로컬 설정 단계가 사라짐**
    -   빌드 모니터링, TestFlight 제출, 크래시 조회, App Store·Google Play 리뷰와 ANR 확인을 원격에서 처리합니다.
    -   스크린샷, tap 자동화, React Native DevTools는 여전히 로컬 dev server가 필요합니다.
    -   Free 플랜에 포함되고 사용량은 결제 계정 단위로 합산됩니다.
    [Source URL](https://expo.dev/changelog/connect-expo-in-claude) (Expo)
    > 시사점: 릴리스 상태 확인처럼 로컬 환경이 필요 없는 작업부터 커넥터로 옮기세요.

---

추론 단가는 가격표와 칩 효율 양쪽에서 함께 내려가는 반면, 모바일 쪽 오늘 항목은 새 기능보다 라이브러리 정리와 유지보수 상태 확인에 실제 작업이 몰려 있습니다.
