---
title: "Claude Fable 5.2, Gemini 4 Carbon GA, Flutter 3.50과 CocoaPods 종료 (2026. 11. 12)"
description: "Claude Fable 5.2와 Gemini 4 Carbon이 풀리고, Flutter 3.50은 Material 분리를, CocoaPods는 12월 2일 신규 등록 중단을 알렸습니다."
date: 2026-11-12 08:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## 오늘의 흐름: 새 프런티어 모델 두 종, Flutter 3.50 마이그레이션, CocoaPods 종료 시한

-   Claude Fable 5.2 출시, 입력 $8·출력 $40
-   "코드는 네 것"이라는 한 문장으로 중복 병합 10%→50%
-   Gemini 4 Carbon GA, 12월 1일 가격 2배
-   Flutter 3.50, Material·Cupertino 폐기 예고
-   CocoaPods, 12월 2일 신규 등록 중단
-   SwiftPM 컴파일 캐시(SE-0547) 승인

---

### Frontier Models

*   **Claude Fable 5.2 출시 — 가격은 Fable 5.1보다 20% 낮은 입력 $8, 출력 $40**
    -   FrontierSWE v2에서 69.9%로 Fable 5.1의 56.3%, Opus 5.5의 62.3%를 앞섭니다 (vendor 측정).
    -   모델 ID는 `claude-fable-5-2`이고, fast mode는 최대 2.5배 빠르며 가격은 두 배입니다.
    -   Preserved thinking이 전 계정에 적용되어, 이전 컨텍스트를 고쳐서 추론을 뽑아내는 방식은 막힙니다.
    [Source URL](https://www.anthropic.com/claude-fable-and-mythos-5-2) (Anthropic)
    > 시사점: 모델 ID를 `claude-fable-5-2`로 바꿔 기존 에이전트 평가셋을 다시 돌려 보세요.

*   **Fable 5.2 프롬프트 가이드 — 코드 소유권을 한 문장으로 알려 주면 중복 코드 병합이 늘어남**
    -   "This codebase is yours" 문장을 넣으면 반복 코드를 합친 비율이 10% 미만에서 약 절반으로 올랐습니다 (vendor 측정).
    -   소유권 언급이 없거나 남의 코드로 설명하면 기존 구조에 코드를 덧붙이는 쪽으로 동작합니다.
    [Source URL](https://simonwillison.net/2026/Nov/10/prompting-claude-fable-52/) (Simon Willison)
    > 시사점: 리팩터링까지 맡길 에이전트라면 시스템 프롬프트에 코드베이스의 소유 관계를 명시하세요.

*   **Gemini 4 Carbon이 11월 10일 전체 공개 — 출시 가격은 입력 $2, 출력 $10**
    -   12월 1일에 가격이 입력 $4, 출력 $20으로 두 배가 됩니다.
    -   thinking effort는 low, medium, high 세 단계이고 기본값은 medium입니다.
    [Source URL](https://simonwillison.net/2026/Nov/10/llm-gemini/) (Simon Willison)
    > 시사점: 비용을 비교한다면 12월 1일 이후 가격 기준으로 계산하세요.

---

### Flutter Toolchain

*   **Flutter 3.50과 Dart 3.14 출시 — `material.dart`와 `cupertino.dart` 폐기**
    -   `material_ui`와 `cupertino_ui`로 옮기며, `dart fix --apply --code=migrate_design_widgets`가 자동으로 바꿔 줍니다.
    -   `IgnorePointer`와 `AbsorbPointer`에서 `ignoringSemantics`가 제거되고, `dart:html`·`dart:js`·`package:js`가 폐기 대상이 됩니다.
    -   신규 프로젝트 기본값은 AGP 9.3.1, Gradle 9.5.0, KGP 2.4.20이고 iOS 터치 입력은 60Hz 기기에서 약 16ms 빨라집니다.
    [Source URL](https://flutter.dev/blog/whats-new-in-flutter-3-50) (Flutter Blog)
    > 시사점: 업그레이드 전에 `--no-deprecated-js-interop`로 웹 코드를 점검하고, 위 `dart fix` 명령으로 디자인 위젯 import를 먼저 옮기세요.

---

### Swift Toolchain

*   **CocoaPods가 12월 2일부터 신규 pod와 버전 등록을 중단 — 기존 pod는 읽기 전용으로 유지**
    -   빌드가 곧바로 깨지지는 않지만 새 버전 배포는 더 이상 올라가지 않습니다.
    -   Flutter 3.50도 CocoaPods trunk가 12월에 읽기 전용이 되고 Swift Package Manager를 끄면 CLI 경고가 뜬다고 밝혔습니다.
    [Source URL](https://www.swift.org/blog/whats-new-in-swift-november-2026/) (Swift.org)
    > 시사점: 의존 pod의 SwiftPM 지원 여부를 Swift Package Index에서 확인하고 12월 전에 전환 계획을 세우세요.

*   **SwiftPM 컴파일 캐시(SE-0547) 승인 — `swift package build-cache configure`로 설정**
    -   콘텐츠 주소 기반 캐시이고 범위는 global, 패키지별, 빌드별 중에서 고릅니다.
    -   SE-0545의 Perfetto용 trace 파일과 task backtrace는 nightly toolchain의 실험 플래그로 먼저 나옵니다.
    [Source URL](https://www.swift.org/blog/whats-new-in-swift-november-2026/) (Swift.org)
    > 시사점: 당장 조치는 불필요합니다.

---

모델 교체와 도구 체인 전환 모두 날짜가 정해진 가격 변경이나 폐기 시한을 기준으로 일정을 잡아야 한다는 점이 같습니다.
