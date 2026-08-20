---
layout: post
title: "AI · 모바일 다이제스트 - 2026-08-21"
date: 2026-08-21 06:10:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## 오늘의 흐름: 300M 드래프트로 2배, 폰에서 도는 125M, 에이전트 코드용 VM

-   LFM2.5-DSpark, 300M 드래프트로 온디바이스 2.27배
-   Core ML INT8 125M, iPhone 15에서 초당 108노트
-   smolvm 1.8.3, 콜드 스타트 0.6~1.5초·warm 50ms
-   Swift 6.4 Embedded, `any` 존재 타입·untyped throws
-   Kotlin 도메인 에러는 sealed + Either로 시그니처에

---

### On-Device Inference

*   **Liquid AI LFM2.5-DSpark, 300M 드래프트 모델로 온디바이스 디코딩 2.27배 (vendor 측정)**
    -   드래프트 세 개 모두 약 300M(295.7M~327.7M)이고, M4 Max에서 LFM2.5-2.6B가 61→139 tok/s로 2.27배입니다.
    -   H100 BF16에서는 같은 모델이 323→864 tok/s(2.67배), function calling 지연은 평균 57% 줄었습니다.
    -   Safetensors와 GGUF로 배포되고 통합 코드가 llama.cpp·SGLang에 업스트림 반영돼 day-one으로 동작합니다.
    [Source URL](https://huggingface.co/blog/LiquidAI/lfm25-dspark) (Hugging Face / Liquid AI)
    > 시사점: 온디바이스 LLM을 이미 llama.cpp로 붙여 뒀다면 타깃 모델은 그대로 두고 드래프트만 얹어 acceptance rate부터 재보세요.

---

### On-Device Deployment

*   **125M 디코더 트랜스포머를 Core ML INT8로 내려 iPhone 15에서 초당 108노트 생성**
    -   pitch·delta_onset·duration·velocity를 한 노트로 묶어 토크나이즈해 forward 한 번에 노트 하나를 진행시킵니다.
    -   학습 컨텍스트는 512노트지만 실사용은 384노트 sliding window로 잘라 긴 세션에서도 유지됩니다.
    -   Gemini 3.5 Flash를 페어와이즈 평가자로 쓴 DPO가 선호도를 24.55%에서 69.05%로 올렸습니다.
    [Source URL](https://simedw.com/2026/08/20/midi-autocomplete/) (simedw.com)
    > 시사점: 도메인 전용 소형 모델은 토크나이저 설계에서 속도가 갈리니, 여러 필드를 한 스텝으로 묶을 수 있는지부터 보세요.

---

### Agent Sandboxing

*   **smolvm 1.8.3, 에이전트가 만든 코드를 Firecracker VM에 격리 — 콜드 스타트 0.6~1.5초**
    -   공유 커널 컨테이너 대신 하드웨어 격리 VM을 쓰고 warm 실행은 약 50ms입니다.
    -   CPU/RAM 상한, 네트워크 차단, read-only 입력 마운트와 writable 출력 마운트, 스토리지 쿼터, 게스트 타임아웃이 확인됐습니다.
    -   자체가 Firecracker 게스트인 Claude Code 컨테이너는 `/dev/kvm`이 없어 실패했고, GitHub Actions 러너에서만 돌았습니다.
    [Source URL](https://simonwillison.net/2026/Aug/19/smolmachines-untrusted-sandbox/) (Simon Willison)
    > 시사점: LLM이 생성한 코드를 실행할 계획이면 호스트에 `/dev/kvm`과 vmx/svm 플래그가 열려 있는지부터 확인하세요.

---

### Swift Toolchain

*   **Swift 6.4 Embedded Swift가 `any` 존재 타입과 untyped throws를 허용해 서브셋 격차를 줄임**
    -   `AnyObject` 제약이 붙은 타입만 되던 제한이 풀려 `Any`를 포함한 모든 `any` 타입이 허용되지만, 제네릭 함수는 `any` 타입에 호출할 수 없습니다.
    -   오류 타입을 적지 않는 `throws`, 메타타입, `Double(inputText)` 같은 문자열→부동소수 파싱, throwing task group이 함께 들어왔습니다.
    -   성능이 민감한 코드는 `PerformanceHints` 진단 그룹을 켜서 동적 기능 사용에 경고를 받을 수 있습니다.
    [Source URL](https://www.swift.org/blog/embedded-swift-improvements-coming-in-swift-6.4/) (Swift.org)
    > 시사점: 아직 development snapshot 단계이니 Embedded 대상 코드에서 우회해 둔 `AnyObject` 제약과 typed throws를 목록으로 잡아 두세요.

---

### Kotlin Architecture

*   **Kotlin 도메인 에러는 예외가 아니라 시그니처로 — sealed interface + Either 권장**
    -   API 클라이언트 오류(4xx), 예기치 못한 예외(500), 도메인 에러 셋 중 도메인 에러만 타입 계약에 올립니다.
    -   `Result<T>`나 `Either<Throwable, T>` 대신 `Either<DocumentSignError, T>`처럼 sealed interface로 실패를 열거해 `when`을 exhaustive하게 만듭니다.
    -   체이닝은 `getOrElse` 조기 반환이나 Arrow의 `either { }`와 `bind()`로 처리하고, HTTP 매핑은 route 경계 한 곳에서만 합니다.
    [Source URL](https://blog.jetbrains.com/kotlin/2026/08/signatures-be-true-domain-errors-and-functional-handling-in-kotlin/) (JetBrains Kotlin Blog)
    > 시사점: 서비스나 리포지토리에서 예외로 흘려보내던 비즈니스 실패가 있다면 메서드별 sealed 에러 타입으로 좁혀 두세요.

---

오늘 항목은 폰 안에서 토큰을 더 짜내는 쪽과, 실행 경계와 실패 경로를 코드 바깥에 명시해 두는 쪽으로 반씩 갈렸습니다.
