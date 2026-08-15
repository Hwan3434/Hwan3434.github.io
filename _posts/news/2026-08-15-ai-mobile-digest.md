---
layout: post
title: "AI · 모바일 다이제스트 - 2026-08-15"
date: 2026-08-15 23:20:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## 오늘의 흐름: on-device 모델 세대교체, 툴체인 승급, agent를 여럿 돌릴 때의 대가

-   Pixel 11에 Gemini Nano 4, Prompt API가 structured output 지원
-   Compose 1.12는 compileSdk 37·AGP 9.1.1을 요구
-   Dart 3.13, primary constructor stable 승격
-   agent 30개 중 18개가 같은 branch 이름을 만듦
-   GPT-5.6 Sol Ultrafast, 초당 750 token limited preview
-   분류하지 말고 생성시킨 뒤 embedding으로 매칭

---

### On-Device Inference

*   **Pixel 11이 Gemini Nano 4를 on-device로 구동 — ML Kit GenAI Prompt API에 structured output과 thinking mode 추가**
    -   Prompt API가 structured output, thinking mode, 140개 이상 언어를 지원합니다.
    -   진입점은 AICore 위의 ML Kit GenAI API로 유지돼 호출 구조는 그대로입니다.
    [Source URL](https://android-developers.googleblog.com/2026/08/pixel-app-experience-made-by-google.html) (Android Developers Blog)
    > 시사점: 서버로 왕복하던 요약·태깅 기능을 Prompt API의 structured output으로 프로토타입해 단말 latency를 직접 재 보세요.

---

### Jetpack Compose

*   **Jetpack Compose 1.12 stable — compileSdk 37과 AGP 9.1.1이 사실상 강제**
    -   BOM은 `2026.08.00`이고 core 모듈이 1.12로, compileSdk가 API 37로 올라갑니다.
    -   `Modifier.onFirstVisible()`이 deprecated되고 `Modifier.onVisibilityChanged()`로 대체됩니다.
    -   key 인자를 받는 `SideEffect`가 `LaunchedEffect`보다 최대 90% 빠릅니다 (vendor 측정).
    [Source URL](https://android-developers.googleblog.com/2026/08/jetpack-compose-august-2026-release.html) (Android Developers Blog)
    > 시사점: `onFirstVisible` 사용처를 grep해 먼저 옮기고, AGP 9.1.1 승급을 이번 분기 작업 항목으로 잡으세요.

---

### Dart Toolchain

*   **Dart 3.13 — primary constructor stable, dart2wasm에 deferred loading preview**
    -   primary constructor가 stable로 승격되고 자동 fix가 붙은 lint 6종이 함께 제공됩니다.
    -   `dart compile wasm -O2 --enable-deferred-loading`으로 deferred loading을 preview 사용할 수 있습니다.
    -   `@RecordUse()` 애노테이션으로 실제 호출되는 native 함수만 남기는 tree-shaking이 가능합니다.
    [Source URL](https://dart.dev/blog/announcing-dart-3-13) (The Dart Blog)
    > 시사점: import 구간을 분리하는 formatter 변경은 코드베이스 전체에 diff를 내므로 기능 커밋과 섞지 마세요.

---

### Multi-Agent Systems

*   **Anthropic, agent 여럿을 같은 코드베이스에 풀었을 때의 실패 양상을 측정해 공개**
    -   agent 30개 중 18개가 `mvp-game-loop`라는 동일한 branch 이름을 만들었습니다.
    -   한 job queue는 수용 가능한 작업이 117건인데 240만 건의 요청을 받았습니다.
    -   조율된 swarm은 27M token으로 취약점 266건, 독립 병렬 agent는 6.5M token으로 21건을 찾았습니다.
    [Source URL](https://www.anthropic.com/research/multiagent-systems) (Anthropic Research)
    > 시사점: 병렬 coding agent를 쓰고 있다면 branch 이름 namespace와 queue rate limit을 지금 걸어 두세요.

---

### Inference Serving

*   **OpenAI·Cerebras, GPT-5.6 Sol Ultrafast tier를 초당 750 token으로 limited preview 공개**
    -   출력은 최대 초당 750 token이며 model 지능은 Standard와 동일하다고 밝혔습니다.
    -   GDP-Val 기준 end-to-end 5.6배 단축, 품질 손실 없음으로 보고됐습니다 (vendor 측정).
    -   Wafer-Scale Engine은 wafer당 SRAM 44GB에 weight를 올려 memory bandwidth 병목을 우회합니다.
    [Source URL](https://www.cerebras.ai/blog/accelerating-gpt-5-6-sol-ultrafast-with-openai) (Cerebras)
    > 시사점: 앱에서 LLM 응답을 스트리밍한다면 초당 수백 token 구간에서 typewriter 애니메이션과 rebuild가 새 병목이 되므로 렌더링 경로를 점검해 두세요.

---

### Prompt Engineering

*   **분류 대신 생성 — 태그를 제약하지 말고 만들게 한 뒤 embedding으로 실제 corpus에 매칭**
    -   Doug Turnbull의 패턴은 LLM에 "novel, never seen before" 분류를 생성시킨 뒤 vector 유사도로 실제 태그에 연결합니다.
    -   prompt에 기존 태그 계층 예시를 넣어야 생성되는 후보의 품질이 올라갑니다.
    [Source URL](https://simonwillison.net/2026/Aug/14/dont-classify-hallucinate/) (Simon Willison's Weblog)
    > 시사점: 후보 목록이 큰 분류 기능은 전체 태그를 context에 밀어 넣는 대신 생성 후 매칭 구조로 바꿔 보세요.

---

오늘 항목의 절반 이상은 기능 자체보다 그것을 켜기 위한 승급 조건 — compileSdk 37, AGP 9.1.1, formatter diff, agent 격리 — 쪽에 실제 비용이 몰려 있습니다.
