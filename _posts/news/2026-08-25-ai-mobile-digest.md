---
layout: post
title: "AI · 모바일 다이제스트 - 2026-08-25"
date: 2026-08-25 06:10:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## 오늘의 흐름: 새로 만들기 전에 이미 있는 설정과 문자열을 점검하는 날

-   keep rule 한 줄이 콜드 스타트 47%를 잡아먹음
-   Jetpack XR beta, `AnchorEntity`가 `AnchorSpace`로
-   Sign in with Apple 새 도메인 `private.icloud.com`
-   에이전트 메모리는 스위치가 아니라 모델별 투여량
-   ADK가 음성 에이전트를 시뮬레이션 유저로 평가

---

### App Size & Startup

*   **Tinder가 keep rule 한 줄을 걷어내 콜드 스타트 47% 단축 — R8 Configuration Analyzer 공개**
    -   사내 라이브러리의 `-keep public class * { public protected *; }` 하나가 앱 코드 약 70%를 최적화 대상에서 제외시키고 있었습니다.
    -   정리 후 앱 크기가 86.6MB에서 61.5MB로, dex 파일은 17개에서 11개로 줄었습니다.
    -   AGP 9.3+에서는 `build/outputs/mapping/release/configanalyzer.html`로 리포트가 자동 생성됩니다.
    [Source URL](https://android-developers.googleblog.com/2026/08/tinder-app-cold-start-r8-configuration-analyzer.html) (Android Developers)
    > 시사점: `./gradlew :app:analyzeReleaseR8Config`를 한 번 돌려 optimization score부터 확인하세요.

---

### Android XR

*   **Jetpack XR SDK 코어 라이브러리 3종이 beta — `AnchorEntity`가 `AnchorSpace`로 이름이 바뀜**
    -   SceneCore, ARCore for Jetpack XR, XR Runtime이 모두 1.0.0-beta02이고 Compose for XR은 1.0.0-alpha17로 뒤따릅니다.
    -   `ActivitySpace`와 `AnchorSpace`가 이제 공통 `SpaceEntity`를 상속합니다.
    -   `Session.create`가 suspend 함수로 바뀌어 coroutine 호출부 수정이 필요합니다.
    [Source URL](https://android-developers.googleblog.com/2026/08/jetpack-xr-sdk-core-libraries-beta.html) (Android Developers)
    > 시사점: alpha 기준 XR 코드가 있다면 클래스 rename과 `Session.create` 시그니처 두 곳부터 고치세요.

---

### Apple Identity

*   **Sign in with Apple 비공개 릴레이 주소가 `private.icloud.com`으로 이동**
    -   신규 발급분만 새 도메인을 쓰고 기존 `privaterelay.appleid.com` 주소는 계속 동작합니다.
    -   iCloud+ Hide My Email 주소는 `icloud.com`으로 그대로 유지됩니다.
    -   전환 시점은 2026년 하반기로 예고됐습니다.
    [Source URL](https://developer.apple.com/news/?id=1ptvdtcm) (Apple Developer News)
    > 시사점: 이메일 도메인 allowlist나 검증 로직이 있다면 두 도메인을 모두 받도록 지금 넓혀두세요.

---

### Agent Memory

*   **AppWorld 585개 태스크로 잰 에이전트 메모리 — 모델 체급에 따라 투여량이 달라짐**
    -   ALTK-Evolve는 weight 업데이트 없이 실행 trajectory에서 뽑은 guideline을 추론 시점에 다시 주입합니다.
    -   gpt-oss-120b는 선별 검색만으로 토큰 5% 증가에 TGC +16.1%p를 얻었습니다.
    -   DeepSeek-V3.2는 전체 guideline 주입에서 TGC +9.5%p·SGC +16.1%p였고, GLM-5는 측정 가능한 이득이 없었습니다.
    [Source URL](https://huggingface.co/blog/ibm-research/altk-evolve-hmm) (Hugging Face / IBM Research)
    > 시사점: 에이전트에 메모리를 붙일 때 전량 주입부터 하지 말고 모델 체급별로 선별 검색과 비교하세요.

---

### Agent Evaluation

*   **ADK가 라이브·음성 에이전트를 시뮬레이션 유저로 자동 평가하는 경로를 제공**
    -   `user_simulator_config`에 `llm_audio` 타입을 지정하면 턴 제어용 LLM과 Gemini TTS가 사용자 역할을 대신합니다.
    -   `rubric_based_multi_turn_trajectory_quality_v1` 메트릭이 자연어 rubric을 LLM judge로 채점합니다.
    -   `NOVICE` 같은 페르소나로 즉흥 대화를 돌리거나 고정 스크립트 대화를 재생할 수 있습니다.
    [Source URL](https://developers.googleblog.com/en/how-to-evaluate-live-voice-agents-in-adk/) (Google Developers Blog)
    > 시사점: 음성 플로우를 수동 통화로 회귀 테스트하고 있다면 시나리오를 `adk eval`로 옮겨 담아보세요.

---

오늘 항목은 새 기능을 붙이는 쪽이 아니라 이미 있는 keep rule, 클래스 이름, 도메인 문자열, 컨텍스트 분량을 다시 점검하라는 요구에 가깝습니다.
