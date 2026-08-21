---
layout: post
title: "AI · 모바일 다이제스트 - 2026-08-22"
date: 2026-08-22 06:10:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## 오늘의 흐름: 정답지를 외운 ASR, Wasm으로 두 배 빨라진 Flutter web

-   ASR 11종, 마스킹한 숫자를 30~40% 복원
-   DeepSeek 비전 모델, 이미지당 토큰 384 상한
-   Flutter Wasm, 위젯 빌드 29.3ms → 11.4ms
-   Antigravity 4개 에이전트로 Dart 패키지 포팅
-   Kotlin 벤치 105태스크, 최고 85.71%

---

### ASR Evaluation

*   **오픈소스 ASR 11종이 오디오 대신 벤치마크 정답지를 재현하는 정황 — 마스킹한 숫자를 30~40% 복원**
    -   LibriSpeech에서 숫자를 무음 처리했는데도 상위 모델 일부가 30~40% 확률로 그 숫자를 그대로 써냈습니다.
    -   VoxPopuli 테스트 클립 40%에서 레퍼런스 오류가 발견됐고, 오류 전사를 그대로 따라 쓴 비율은 18~30%였습니다.
    -   `any one`/`anyone`, `Mr.`/`Mister` 같은 데이터셋별 표기 규칙 전환 정확도는 약 90%까지 올라갔습니다.
    [Source URL](https://huggingface.co/blog/asr-benchmark-optimization) (Hugging Face)
    > 시사점: 음성 모델을 WER 단일 점수로 고르지 말고 완전히 분리된 held-out 세트로 다시 재보세요.

---

### Multimodal API

*   **DeepSeek가 `deepseek-v4-flash-vision-exp` 공개 — 요청당 이미지 600장, 이미지당 토큰은 384 상한**
    -   모든 이미지는 추론 전 약 800×800으로 리사이즈되고 한 변은 8192px, 이미지가 15장 이상이면 4096px가 상한입니다.
    -   입력은 base64 인라인, HTTP(S) URL(8192자 이내), Files API 참조 세 가지이고 Files API를 쓰면 요청 총량이 64MiB에서 200MiB로 늘어납니다.
    -   `detail`을 `low`로 주면 512×512로 처리하고 `high`/`original`은 원본 해상도를 유지합니다.
    [Source URL](https://api-docs.deepseek.com/guides/vision/) (DeepSeek API Docs)
    > 시사점: 스크린샷이나 차트를 배치로 넣을 계획이면 이미지당 384토큰 상한을 기준으로 비용부터 다시 계산하세요.

---

### Flutter Web

*   **Flutter Web WebAssembly Week — Wasm 빌드가 위젯 빌드 시간을 29.3ms에서 11.4ms로 (vendor 측정)**
    -   프레임 타임은 JS 34.5ms(약 30 FPS)에서 Wasm 17.4ms(60 FPS 유지)로 떨어지고 지터는 ±1.5ms에서 ±0.5ms입니다.
    -   압축 전송 기준 번들 크기 증가는 5% 이내이며, 기존 Flutter web 앱의 58%가 코드 수정 없이 Wasm으로 컴파일됩니다.
    -   진입 경로는 Flutter 3.47로 올린 뒤 `flutter build web --wasm`입니다.
    [Source URL](https://flutter.dev/blog/try-flutter-web-with-webassembly-week) (Flutter Blog)
    > 시사점: Flutter web을 운영 중이라면 3.47에서 `--wasm` 빌드를 한 번 돌려 컴파일이 그대로 통과하는지부터 확인하세요.

---

### Agent Workflow

*   **Flutter 팀이 Antigravity Agent Hub로 에이전트 넷을 붙여 Python 라이브러리를 Dart 패키지로 포팅**
    -   Architect는 `lib/`·`test/`·`example/` 쓰기 금지, Tester는 `lib/`·`specs/` 접근 금지처럼 역할별로 디렉터리 권한을 잘랐습니다.
    -   대상이 metaclass와 런타임 콜백에 의존하는 python-statemachine이라 `dart:mirrors`가 막힌 환경에서 구조를 새로 설계해야 했습니다.
    -   스켈레톤 정리 중 테스트 유틸이 삭제되는 등 마찰점 세 개가 나와 중간에 skill을 고쳤고, 결과물은 proof-of-concept입니다.
    [Source URL](https://flutter.dev/blog/building-multi-agent-dev-teams) (Flutter Blog)
    > 시사점: 에이전트를 여러 개 붙일 계획이면 역할 프롬프트보다 디렉터리 쓰기 권한 분리를 먼저 설계하세요.

---

### Kotlin Tooling

*   **JetBrains Kotlin Benchmark 리더보드 — 실제 Kotlin 이슈 105개에서 최고 해결률 85.71%**
    -   Claude Code + Opus 4.7 xhigh가 90/105로 1위, Junie + Opus 4.7 max와 Codex + GPT 5.5 xHigh가 86개로 공동 2위입니다.
    -   태스크는 오픈소스 저장소의 실제 이슈이고, 컨테이너에서 지정된 테스트를 통과해야만 resolved로 집계됩니다.
    [Source URL](https://kotlinlang.org/benchmark/) (JetBrains)
    > 시사점: Android 코드베이스에 코딩 에이전트를 도입 중이라면 범용 SWE 벤치 대신 이 Kotlin 리더보드를 기준선으로 잡으세요.

---

오늘 항목은 공개된 벤치마크 숫자와 API 상한을 그대로 받아쓰지 말고 자기 워크로드에서 다시 재보라는 쪽으로 모입니다.
