---
layout: post
title: "AI · 모바일 다이제스트 - 2026-08-26"
date: 2026-08-26 06:10:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## 오늘의 흐름: 줄인 모델과 올릴 앱 모두 상한선을 먼저 재두는 날

-   4-bit 모델이 원본 BF16을 9개 중 7개에서 앞섬
-   Granite 4.2 3B/8B/30B, Apache 2.0에 GGUF 동봉
-   Android 17 앱별 메모리 한도, 넘으면 zRAM 후 kill
-   Flutter 데스크톱 멀티 윈도우 API가 main 채널에
-   Play GenAI 심사가 적대적 프롬프트 증빙을 요구

---

### On-Device Quantization

*   **4-bit로 줄인 모델이 원본 BF16을 앞섬 — Multiverse가 Quantization-Aware Healing 공개**
    -   QAH는 압축 후 복구된 체크포인트가 아니라 압축 전 full-precision teacher에서 직접 distill합니다.
    -   GPT-OSS 120B를 60B·MXFP4로 줄인 모델이 60B BF16 대비 9개 벤치마크 중 7개에서 앞섰습니다 (vendor 측정).
    -   QAT가 peak 이후 19점 붕괴한 것과 달리 QAH는 약 100 step에서 peak에 도달한 뒤 안정적이었습니다.
    [Source URL](https://huggingface.co/blog/MultiverseComputingCAI/quantization-aware-healing) (Hugging Face / Multiverse Computing)
    > 시사점: 온디바이스용 4-bit 변환에서 QAT가 무너진다면 teacher를 압축 전 원본으로 바꿔 다시 재보세요.

---

### Open Models

*   **IBM Granite 4.2 공개 — 3B/8B/30B 전부 Apache 2.0에 GGUF 변환본 동봉**
    -   세 모델 모두 dense decoder-only에 GQA(40 heads / 8 KV heads) 구성이고 컨텍스트는 512K 토큰까지 확장됐습니다.
    -   3B가 AIME25 78.33%, MMLU-Pro 67.84%를 기록했습니다 (vendor 측정).
    -   llama.cpp 표준 도구로 변환한 GGUF가 Q8_0부터 Q2_K까지 14종 제공됩니다.
    [Source URL](https://huggingface.co/blog/ibm-granite/granite-4-2) (Hugging Face / IBM Granite)
    > 시사점: 온디바이스 후보로 3B를 본다면 Q4 근처 GGUF부터 실기기 latency를 재보세요.

---

### Android Memory

*   **Android 17이 앱별 메모리 한도를 도입 — 초과하면 zRAM 스왑, 더 늘면 프로세스 종료**
    -   Pixel부터 적용되며 한도를 넘긴 앱 페이지는 zRAM으로 압축돼 CPU 오버헤드와 jank로 나타납니다.
    -   kill된 경우 `ApplicationExitInfo`의 reason이 `REASON_OTHER`, description이 `MemoryLimiter:AnonSwap`으로 찍힙니다.
    -   Crashlytics 20.1.0부터 OOM과 memory limiter kill에 대한 추가 디버그 데이터가 들어옵니다.
    [Source URL](https://android-developers.googleblog.com/2026/08/app-broader-memory-limits.html) (Android Developers)
    > 시사점: Android vitals의 Memory Usage(Anonymous RSS + swap) 지표부터 열어 상위 화면의 여유를 확인하세요.

---

### Flutter Desktop

*   **Flutter 데스크톱 멀티 윈도우 API 공개 — `runApp` 대신 `runWidget`으로 시작**
    -   regular, dialog, popup, tooltip, satellite 5종 윈도우를 `WindowController`와 `Window` 위젯 쌍으로 다룹니다.
    -   모든 윈도우가 단일 위젯 트리를 공유하므로 Riverpod, Bloc 같은 기존 상태관리를 그대로 씁니다.
    -   현재는 main 채널 실험 플래그로만 열리며 `flutter config --enable-windowing`이 필요합니다.
    [Source URL](https://flutter.dev/blog/desktop-windowing-apis) (Flutter Blog)
    > 시사점: 데스크톱 타깃이 있다면 지금은 프로토타입까지만 해두고 API 변경 가능성을 감안하세요.

---

### Play Policy

*   **Play가 생성형 AI 앱 심사 요건을 명시 — 적대적 프롬프트 테스트 증빙을 요구**
    -   심사자에게 페이월이나 지역 제한 없이 모든 생성형 AI 기능을 열어주는 테스트 계정을 제공해야 합니다.
    -   모델이 deepfake와 nudify 류 요청을 거부한다는 테스트 증빙을 함께 제출해야 합니다.
    -   모델 기본 필터 외에 입출력 moderation을 따로 붙이고 렌더링 전에 출력을 검증하라고 명시했습니다.
    [Source URL](https://android-developers.googleblog.com/2026/08/ensuring-safety-genai-preventing-non-consensual-intimate-content.html) (Android Developers)
    > 시사점: 이미지 생성이나 편집 기능이 있다면 심사용 계정과 적대적 프롬프트 로그를 릴리스 체크리스트에 넣으세요.

---

오늘 항목은 모델을 줄이든 앱을 올리든, 실기기와 심사에서 걸리는 상한선을 미리 재두라는 쪽으로 모입니다.
