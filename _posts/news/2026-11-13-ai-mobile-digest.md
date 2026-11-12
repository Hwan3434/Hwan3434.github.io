---
title: "Gemini Decisions API, Flutter 네이티브 interop 안정화, CameraX 사례 (2026. 11. 13)"
description: "Gemini Decisions API와 llm 0.37.2 보안 패치가 나왔고, Flutter는 FFIgen·JNIgen 안정화를, Android는 CameraX 사례를 공개했습니다."
date: 2026-11-13 08:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## 오늘의 흐름: Gemini Decisions API, llm 보안 패치, Flutter 네이티브 interop 안정화, CameraX 사례

-   Gemini Decision 1, 입력 100만 토큰당 $0.10
-   llm 0.37.2, OpenAI API 키 유출 경로 2건 수정
-   Anthropic, AMD GPU 포팅 3일 (vendor 측정)
-   Flutter FFIgen·JNIgen 안정화, Pigeon 프리뷰
-   SmileID, CameraX로 selfie 해상도 4배

---

### AI Engineering

*   **Gemini Decision 1 공개 — yes/no, choice, rubric-scoring 세 가지 질문 유형을 API로 제공**
    -   입력은 100만 토큰당 $0.10이고 출력은 무료이며, 텍스트·이미지·오디오·비디오·PDF를 받습니다.
    -   yes/no 질문에 1.0이나 0.0이 아니라 단계적 확률(예: 0.92, 0.05)을 돌려줍니다.
    [Source URL](https://simonwillison.net/2026/Nov/11/gemini-decisions-api/) (Simon Willison)
    > 시사점: 분류나 필터링 용도라면 0/1 대신 확률 임계값을 직접 정하는 구조로 설계하세요.

*   **llm 0.37.2 보안 릴리스 — OpenAI API 키가 다른 provider 엔드포인트로 전송될 수 있던 문제 2건 수정**
    -   `extra-openai-models.yaml`에서 `api_key_name`의 키가 저장된 적 없을 때 문제가 생깁니다.
    -   `responses: true` 모델을 `-o chat_completions 1`로 실행할 때도 같은 문제가 납니다.
    [Source URL](https://simonwillison.net/2026/Nov/11/llm/) (Simon Willison)
    > 시사점: `llm openai endpoint add`로 커스텀 엔드포인트를 등록했다면 0.37.2로 올리세요.

*   **Anthropic, AMD GPU에서 Claude를 3일 만에 구동했다고 밝힘 — 커널 거의 전부를 Claude가 작성**
    -   Trainium, TPU, NVIDIA GPU, AMD GPU 네 가지 칩에서 Claude를 학습하고 서빙한다고 설명합니다 (vendor 측정).
    -   새 칩 플랫폼 지원에 예전에는 엔지니어 수십 명이 수개월 걸렸다고 합니다.
    [Source URL](https://simonwillison.net/2026/Nov/11/anthropic-ipo-roadshow/) (Simon Willison)
    > 시사점: 커널 포팅처럼 검증이 명확한 작업부터 코딩 에이전트에 맡겨 보세요.

---

### Flutter Native Interop

*   **Flutter, FFIgen(Objective-C)과 JNIgen(Java/Kotlin) 안정화 — Pigeon의 네이티브 interop은 프리뷰**
    -   Pigeon v30.0 이상에서 `useFfi`와 `useJni` 옵션을 켜면 platform channel 직렬화를 거치지 않습니다.
    -   동기 호출과 background isolate 호출이 가능하고, 지원 대상은 Android, iOS, macOS이며 Windows와 Linux는 platform channel을 씁니다.
    -   `shared_preferences` 플러그인이 마이그레이션 참고 사례입니다.
    [Source URL](https://flutter.dev/blog/stable-native-interop) (Flutter Blog)
    > 시사점: 직접 만든 플러그인이 있다면 Pigeon 파일에 두 옵션을 켜고 다시 생성해 보세요.

---

### Android Camera

*   **SmileID, CameraX로 마이그레이션해 selfie 해상도 4배, 인증 통과율 20% 상승 (vendor 측정)**
    -   `ImageAnalysis`에 `ResolutionSelector`와 `STRATEGY_KEEP_ONLY_LATEST`를 조합해 저사양 기기의 OOM을 피했습니다.
    -   얼굴 영역을 기기에서 압축해 업로드 용량은 기존과 같게 유지했고, 지원 기기는 18,000종 이상입니다.
    [Source URL](https://developer.android.com/blog/posts/smileid-camerax-android-identity-verification.md.txt) (Android Developers Blog)
    > 시사점: 저사양 기기 대응이 필요하면 `FALLBACK_RULE_CLOSEST_LOWER_THEN_HIGHER`로 메모리 상한을 두세요.
