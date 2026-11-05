---
title: "AppFunctions 1.0 RC, Navigation3 1.2.1, Phonon TTS, Cosmos 3 (2026. 11. 06)"
description: "AppFunctions 1.0.0-rc01과 Navigation3 1.2.1이 나왔고, 65MB급 온디바이스 TTS Phonon과 Cosmos 3 Nano 모델이 공개됐습니다."
date: 2026-11-06 08:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## 오늘의 흐름: AppFunctions RC, Navigation3 패치, 온디바이스 음성, 월드 시뮬레이션 모델

-   AppFunctions 1.0.0-rc01 공개
-   Navigation3 1.2.1, compileSdk 36으로 복귀
-   Phonon TTS, 65MB로 폰에서 오프라인 음성 합성
-   NVIDIA Cosmos 3 Nano 후속 모델 4종 공개

---

### Android Jetpack

*   **AppFunctions 1.0.0-rc01 공개 — 앱 기능을 AI 어시스턴트에 노출하는 API가 RC에 들어왔습니다**
    -   beta01 이후 두 주 만에 RC로 올라오면서 legacy aggregation compiler 옵션이 제거됐습니다.
    -   beta01에서는 `AppFunctionName`이 `androidx.appfunctions` 패키지로 옮겨졌고 `AppFunctionAppMetadata.description`이 `instructions`로 바뀌었습니다.
    [Source URL](https://developer.android.com/jetpack/androidx/releases/appfunctions) (Android Developers)
    > 시사점: alpha·beta 때 쓰던 이름이 바뀌었으니 RC로 올리기 전에 import와 metadata 속성부터 점검하세요.

*   **Navigation3 1.2.1 — compileSdk를 37에서 36으로 되돌렸습니다**
    -   1.2는 Compose 1.10에 의존하므로 compileSdk 37이 필요하지 않았습니다.
    -   1.3.0-alpha04는 pop 직후 같은 shared `NavEntry`를 다시 push하면 화면에 그려지지 않던 문제를 고쳤습니다.
    [Source URL](https://developer.android.com/jetpack/androidx/releases/navigation3) (Android Developers)
    > 시사점: 1.2.0을 쓰면서 compileSdk를 37로 올렸다면 1.2.1에서는 36으로 내려도 됩니다.

---

### On-Device & Open Models

*   **Phonon TTS 공개 — 65~75MB 모델이 서버 없이 폰과 브라우저에서 돕니다**
    -   Phonon 31M은 영어 전용, 40M은 영어·프랑스어·독일어·스페인어·포르투갈어를 지원하며, 내장 voice는 100개가 넘습니다.
    -   CPU streaming 벤치마크의 p95 time-to-first-audio는 31M EN 28ms, 40M EN 38ms, Pocket TTS 165ms입니다. (vendor 측정)
    -   31M만 Apache 2.0이고 나머지는 CC BY-NC입니다.
    [Source URL](https://huggingface.co/blog/phonon-tts) (Hugging Face)
    > 시사점: 앱에 넣으려면 상업 이용이 가능한 31M 영어판부터 시험하세요.

*   **NVIDIA Cosmos 3 Nano 후속 모델 4종 — 주행·로봇 월드 시뮬레이션용입니다**
    -   Transfer-Auto는 최대 11개 camera view를, Sim-Auto는 camera와 LiDAR 동기 관측을 다룹니다.
    -   streaming 변형은 distillation 2단계에서 chunk 하나를 4 denoising step으로 생성하며, 라이선스는 OpenMDW1.1입니다.
    -   실행에는 Linux, NVIDIA GPU, Docker가 필요하고 vLLM-Omni 설정은 GB200 한 장에서 검증됐습니다.
    [Source URL](https://huggingface.co/blog/nvidia/cosmos-interactive-world-simulation) (Hugging Face)
    > 시사점: 당장 조치는 불필요합니다.

---

오늘 항목은 모두 앱 기능이나 모델이 사용자 기기와 에이전트 쪽으로 옮겨 가는 흐름 위에 있습니다.
