---
layout: post
title: "AI · 모바일 다이제스트 - 2026-08-27"
date: 2026-08-27 06:10:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## 오늘의 흐름: 벤더가 낸 수치를 받아 적기 전에 내 환경에서 다시 재는 날

-   470M ASR 모델이 WER 5.00%, 속도는 H200 기준
-   GLM-5.3-Flash MIT 공개, 320B 중 18B active
-   vLLM TPU 임베딩, 백엔드 간 코사인 0.999 일치
-   Play 품질 기준에 DEX 최적화 25%가 들어감
-   Compose Multiplatform 1.12.0에 Hot Reload MCP
-   Flutter가 WWDC 145개 세션을 Gemini로 분류

---

### On-Device Speech

*   **Granite Speech 5.0 Turbo CTC 공개 — 470M ASR 모델을 엣지 타깃으로 내놓음**
    -   self-conditioning과 chunkwise attention을 쓴 Conformer 16 블록의 encoder-only 구성이고, 2배 temporal subsampling 3단으로 초당 12.5 토큰을 냅니다.
    -   OpenASR 공개 테스트셋에서 Apache 2.0판이 WER 5.00%, CC-BY-NC판이 4.85%입니다 (vendor 측정).
    -   공개된 속도 수치는 H200 배치 추론 기준 12,600 RTFx 이상으로, 실기기 측정이 아닙니다.
    [Source URL](https://huggingface.co/blog/ibm-granite/granite-speech-5-0-470m-turboctc) (Hugging Face / IBM Granite)
    > 시사점: 온디바이스 STT 후보로 본다면 Apache 2.0판을 받아 실기기 latency부터 직접 재세요.

---

### Open Models

*   **GLM-5.3-Flash가 MIT로 공개 — 320B 중 18B만 활성화되는 하이브리드 어텐션 구성**
    -   sparse attention과 linear attention을 섞고 Manifold-Constrained Hyper-Connections를 얹은 네이티브 멀티모달 모델입니다.
    -   컨텍스트는 1,048,576 토큰이고 30T 토큰 멀티모달 코퍼스로 사전학습했습니다.
    -   Terminal-Bench 2.1 84.3, DeepSWE 63.4를 기록했습니다 (vendor 측정).
    [Source URL](https://huggingface.co/zai-org/GLM-5.3-Flash) (Hugging Face / Z.ai)
    > 시사점: MIT라 사내 배포 제약이 없으니 코딩 에이전트 백엔드 후보에 넣고 자체 태스크로 다시 재보세요.

---

### Embedding Serving

*   **vLLM에 TPU 네이티브 지원이 들어감 — 백엔드를 바꿔도 임베딩 값이 어긋나지 않음**
    -   GKE Custom Compute Classes로 TPU, GPU, spot 인스턴스 사이를 오가며 임베딩 워크로드를 스케일링합니다.
    -   Qwen3-Embedding-8B가 16K 이상 시퀀스, bfloat16에서 초당 83,996 토큰과 5.13 요청을 처리했습니다 (vendor 측정).
    -   백엔드가 달라져도 텍스트 임베딩은 코사인 유사도 0.999 이상, 멀티모달은 0.995 이상으로 맞췄습니다.
    [Source URL](https://developers.googleblog.com/en/enterprise-grade-precision-for-long-context-multimodal-embedding-inference-on-cloud-tpu/) (Google Developers Blog)
    > 시사점: 임베딩 서빙 백엔드를 옮길 계획이면 배포 전에 코사인 유사도 parity 검사를 파이프라인에 넣으세요.

---

### Play Quality Bar

*   **Play 품질 기준에 메모리와 DEX 최적화가 편입 — 시행일은 2027년 2월과 4월**
    -   동적 메모리(anonymous RSS + swap), bitmap 메모리 보유, DEX 코드 최적화가 기준 항목으로 들어갑니다.
    -   DEX는 optimization·shrinking·obfuscation을 합쳐 최소 25% 커버리지를 요구하며 2027년 2월부터 적용됩니다.
    -   로그인 앱은 Restore Credentials API로 기기 이전 시 로그인 상태를 자동 복원해야 하고 2027년 4월부터 적용됩니다(게임은 예외).
    [Source URL](https://android-developers.googleblog.com/2026/08/app-quality-memory-optimization-secure-onboarding.html) (Android Developers)
    > 시사점: R8 커버리지와 Restore Credentials 도입 여부를 지금 확인해 두 마감에 나눠 배치하세요.

---

### Compose Multiplatform

*   **Compose Multiplatform 1.12.0 — Hot Reload에 코딩 에이전트용 MCP 서버가 붙음**
    -   실험적 MCP 서버로 에이전트가 리로드 트리거, 스크린샷, semantic tree 조회, 클릭·텍스트 입력, 로그 읽기를 수행합니다.
    -   데스크톱 window/dialog v2 API가 `androidx.compose.ui.window.v2` 패키지에 실험 단계로 들어와 기존 API는 그대로입니다.
    -   iOS는 lazy layout의 item deactivation이 drawing phase 밖으로 빠져 스크롤 구간이 개선됐습니다.
    [Source URL](https://blog.jetbrains.com/kotlin/2026/08/compose-multiplatform-1-12-0/) (Kotlin Blog)
    > 시사점: KMP 앱 UI를 에이전트로 검증하고 싶다면 Hot Reload MCP 서버부터 붙여보세요.

---

### Flutter iOS Readiness

*   **Flutter가 iOS 대응을 앞당기는 방식 공개 — WWDC 세션 자막을 뽑아 Gemini로 분류**
    -   Dart 코드로 WWDC 기술 세션 자막을 추출한 뒤 약 145개 영상을 중요도, 영향 영역, 권장 조치로 순위화합니다.
    -   분류 문서가 다음 날 나오고 그 결과가 iOS 27 대응 GitHub Projects 트래킹으로 이어집니다.
    -   UIScene 지원은 2026년 2월 Flutter 3.41 stable에 들어갔고, add-to-app 구성만 별도 마이그레이션이 필요했습니다.
    [Source URL](https://flutter.dev/blog/how-flutter-stays-ahead-of-ios-releases) (Flutter Blog)
    > 시사점: 대부분은 `flutter upgrade`로 끝나지만 add-to-app 구성이라면 UIScene 마이그레이션 가이드를 확인하세요.

---

오늘 항목은 모델이든 앱이든 벤더가 낸 수치와 기준을 그대로 쓰지 말고 내 기기, 내 태스크, 내 백엔드에서 다시 재보라는 쪽으로 모입니다.
