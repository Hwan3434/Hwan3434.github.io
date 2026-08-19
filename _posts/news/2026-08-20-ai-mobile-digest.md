---
layout: post
title: "AI · 모바일 다이제스트 - 2026-08-20"
date: 2026-08-20 06:10:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## 오늘의 흐름: 6.2GB로 줄인 27B, 앱을 죽이는 메모리 상한, 스스로 태스크를 만드는 모델

-   Unsloth Dynamic 3.0, 6.2GB로 top-1% 72% 유지
-   Android 17, 앱별 메모리 상한 넘으면 zRAM 후 종료
-   EAS Observe GA, 무료 월 10만 이벤트·보존 90일
-   Ornith-1.5, self-scaffolding RL로 SWE-Bench 86.0
-   Mojo 컴파일러·툴체인 Apache 2.0으로 공개

---

### On-Device Quantization

*   **Unsloth Dynamic 3.0 GGUF, 같은 용량에서 top-1% 정확도 10%p 우위를 주장 (vendor 측정)**
    -   Qwen3.8-27B의 `UD-IQ1_S`는 6.2GB로 원본 대비 89% 작으면서 top-1% 정확도 약 72%를 유지합니다.
    -   Gemma 3 27B 기준 `Q2_K_XL`이 9.95GB에서 MMLU 5-shot 68.70%, `Q4_K_XL`이 15.64GB에서 71.47%입니다.
    -   llama.cpp를 포함한 대부분의 추론 엔진에서 그대로 로드되고, 작은 quant는 MTP 모듈을 빼 약 500MB를 더 줄입니다.
    [Source URL](https://unsloth.ai/docs/basics/dynamic-3.0-ggufs) (Unsloth)
    > 시사점: 로컬·온디바이스용 GGUF를 고르는 중이라면 Q4 대신 Q2_K_XL로 내렸을 때의 5.7GB 절감분부터 재보세요.

---

### Android Runtime

*   **Android 17이 앱별 메모리 상한을 도입 — 넘으면 zRAM으로 밀리고 계속 넘기면 종료**
    -   상한을 넘긴 앱은 페이지가 zRAM으로 압축돼 CPU 오버헤드와 UI jank가 생기고, 사용량이 계속 늘면 프로세스가 종료됩니다.
    -   이 종료는 `ApplicationExitInfo.getDescription()`이 `MemoryLimiter:AnonSwap`을 담은 `REASON_OTHER`로 식별합니다.
    -   Pixel부터 적용되며 4GB~16GB+ 기기에 걸쳐 앞으로 1년간 제조사가 확대됩니다.
    [Source URL](https://android-developers.googleblog.com/2026/08/app-broader-memory-limits.html) (Android Developers)
    > 시사점: Android Vitals의 Memory Usage(RSS+swap)와 Bitmap Memory Usage부터 확인하고 API 35의 ProfilingManager로 프로덕션 힙 덤프를 걸어 두세요.

---

### App Observability

*   **Expo EAS Observe가 오늘 GA 전환 — 무료 티어에도 이벤트 쿼터가 생김**
    -   Free는 월 10만 이벤트, Starter 이상은 월 50만 이벤트이고 초과분은 100만 이벤트당 $5입니다.
    -   모든 플랜의 데이터 보존 기간이 90일로 통일됩니다.
    -   app startup, navigation, EAS Update 대시보드를 제공하며 GA 시점에 코드 변경은 필요 없습니다.
    [Source URL](https://expo.dev/changelog/eas-observe-moves-to-general-availability-on-august-20) (Expo)
    > 시사점: 베타 때 샘플링 없이 켜 뒀다면 과금이 시작되기 전에 sampling rate를 조정하거나 ingestion을 끄세요.

---

### Coding Agents

*   **Ornith-1.5, 스스로 태스크와 스캐폴드를 만들어 RL 루프를 도는 모델 (vendor 측정)**
    -   397B MoE가 Terminal-Bench 2.1에서 86.1, SWE-Bench Verified에서 86.0을 기록했다고 밝혔습니다.
    -   모델이 태스크를 제안하고 태스크별 스캐폴드와 solution rollout까지 생성해, GRPO로 harness와 rollout 품질을 따로 최적화합니다.
    -   397B MoE, 35B MoE, 9B dense 세 가지 규모로 나옵니다.
    [Source URL](https://ornith.ai/ornith_1_5.html) (Ornith)
    > 시사점: 서드파티 재현이 나올 때까지 수치는 보류하고 self-scaffolding 루프의 3단계 구조만 참고하세요.

---

### Language Toolchain

*   **Mojo 컴파일러와 툴체인이 Apache 2.0으로 공개**
    -   1.0 릴리스 약 일주일 뒤에 컴파일러와 툴체인 전체가 Apache 2.0으로 열렸습니다.
    -   Python superset 목표는 접었고 GPU 프로그래밍용 독립 언어로 방향을 정리했습니다.
    [Source URL](https://simonwillison.net/2026/Aug/18/mojo-is-now-open-source/) (Simon Willison)
    > 시사점: 당장 조치는 불필요합니다.

---

오늘은 quant 용량이든 앱 메모리든 이벤트 쿼터든, 그동안 재지 않고 넘어가던 것에 상한이 붙고 그 안에서 예산을 다시 나눠야 하는 항목이 많았습니다.
