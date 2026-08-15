---
layout: post
title: "AI · 모바일 다이제스트 - 2026-08-16"
date: 2026-08-16 06:20:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## 오늘의 흐름: 생성 UI를 미리 만들어 캐시하기, 날짜가 박힌 모바일 이전 작업, 작은 모델의 실제 점유율

-   A2UI 메시지를 미리 생성해 Firestore에 캐시
-   Flutter 3.47, Material·Cupertino가 별도 패키지로
-   Media3 1.11, 숏폼 피드용 PlayerPool 추가
-   한국 App Store, GRAC RCN으로 등급 override 가능
-   Claude 텍스트 워터마크, 8월 2일 이후 모델부터
-   1B 미만 모델이 전체 다운로드의 83%

---

### Generative UI

*   **Flutter genui — A2UI를 요청 시점에 만들지 말고 미리 생성해 캐시하는 패턴**
    -   `genui`가 렌더링하는 A2UI는 JSON 메시지라 Firestore에 그대로 저장해 재사용할 수 있습니다.
    -   Cloud Functions에서 `gemini-3.1-flash-lite`로 미리 만들어 두고 앱 시작 시엔 DB만 읽습니다.
    [Source URL](https://flutter.dev/blog/speeding-up-generative-ui-with-async-a2ui) (The Flutter Blog)
    > 시사점: LLM 호출을 앱 시작 경로에서 빼고 생성 단계와 소비 단계를 분리하세요.

---

### Flutter Toolchain

*   **Flutter 3.47 — Material·Cupertino가 SDK에서 분리되고 iOS 최소 버전이 15로 상향**
    -   `material_ui`, `cupertino_ui` 1.0으로 분리되고 기존 라이브러리는 11월에 공식 deprecated 예정입니다.
    -   `dart fix --apply --code=migrate_design_widgets`로 import를 자동 이전할 수 있습니다.
    -   최소 지원이 iOS 15·macOS 12로 오르고 Impeller가 macOS·Windows·Linux에서 기본값이 됩니다.
    [Source URL](https://flutter.dev/blog/whats-new-in-flutter-3-47) (The Flutter Blog)
    > 시사점: 패키지를 배포 중이라면 이 이전을 major 버전으로 끊고 `MaterialUiCompatibilityBridge`로 과도기를 넘기세요.

---

### Android Media

*   **Media3 1.11 — 숏폼 피드용 player 재활용 API와 session 보안 기본값 변경**
    -   `common-ktx`의 `PlayerPool`과 `ui-compose`의 `rememberPooledPlayer`가 피드에서 player 인스턴스를 재활용합니다.
    -   session 데이터가 신뢰되지 않은 controller에 기본적으로 더 이상 공유되지 않습니다.
    -   `media3-datasource-ktor` 모듈이 추가돼 HTTP 스택을 Ktor로 교체할 수 있습니다.
    [Source URL](https://android-developers.googleblog.com/2026/08/media3-1-11-whats-new.html) (Android Developers Blog)
    > 시사점: 숏폼 화면에서 player를 매번 새로 생성하고 있다면 `rememberPooledPlayer` 교체 대상을 먼저 추려 두세요.

---

### App Store Policy

*   **한국 App Store 연령 등급 — GRAC 등급분류번호로 override 가능, 10월부터 일부 descriptor가 12+로**
    -   게임·엔터테인먼트 앱은 GRAC RCN을 다음 버전에 제출해 All/12+/15+/19+로 등급을 덮어쓸 수 있습니다.
    -   10월부터 경미한 비속어·저속한 유머와 경미한 성적 암시가 All에서 12+로 이동합니다.
    [Source URL](https://developer.apple.com/news/?id=oj3r9pvw) (Apple Developer News)
    > 시사점: 해당 descriptor를 켜 둔 앱이라면 10월 전에 등급 상승 여부를 확인하고 필요하면 RCN을 준비하세요.

---

### AI Provenance

*   **Anthropic, Claude 텍스트 워터마크 동작 방식 공개 — 8월 2일 이후 출시 모델부터 적용**
    -   단어 선택의 난수원을 key와 직전 단어들로 대체하는 DeepMind SynthID-Text 방식입니다.
    -   짧은 문장, 정확한 용어가 강제되는 사실 서술, 사람이 크게 고쳐 쓴 텍스트에서는 신호가 희박해집니다.
    -   탐지 API는 아직 없고 제공 예정으로만 안내됐습니다.
    [Source URL](https://www.anthropic.com/news/claude-text-watermark) (Anthropic)
    > 시사점: 워터마크를 검증 수단으로 쓸 계획이라면 짧은 출력에는 사실상 동작하지 않는다는 전제로 설계하세요.

---

### Open Models

*   **Hugging Face 오픈 모델 결산 — 관심은 대형 모델에, 다운로드는 1B 미만에 쏠림**
    -   1B 미만 모델이 전체 다운로드의 83%, 100B 초과 모델은 1%를 차지합니다.
    -   Qwen GGUF 변환본이 월 3,960만 다운로드로 Gemma 2,080만의 약 두 배입니다.
    -   Hub에 접근한 agent 트래픽 중 Claude Code가 7월 기준 44.4%였습니다.
    [Source URL](https://huggingface.co/blog/state-of-open-models-summer-2026) (Hugging Face)
    > 시사점: on-device 후보를 고를 때 리더보드 상위가 아니라 GGUF 다운로드가 실제로 몰린 소형 모델부터 보세요.

---

오늘 모바일 쪽 항목은 기능 추가보다 날짜가 박힌 이전 작업 — 11월 Material·Cupertino deprecation, 10월 한국 등급 재분류 — 에 실제 비용이 몰려 있습니다.
