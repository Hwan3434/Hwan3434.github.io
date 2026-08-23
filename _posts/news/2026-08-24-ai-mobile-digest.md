---
layout: post
title: "AI · 모바일 다이제스트 - 2026-08-24"
date: 2026-08-24 06:10:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## 오늘의 흐름: 모델을 바꾸기 전에 계약과 기본값을 먼저 좁히는 날

-   MCP 로드맵, 세션 제거 후 HTTP 전송 단일화로
-   int4 KV cache에서 tool call이 깨짐
-   자율 연구 153런, 인간 기록 격차의 81.7%
-   Dart primary constructor, 이름 반복을 `new()`로
-   AGP 10부터 새 Variant API 강제, 9.4에 opt-out

---

### Agent Protocol

*   **MCP 로드맵 갱신 — server-initiated 이벤트와 HTTP 전송 단일화가 다음 우선순위로 올라감**
    -   2026-07-28 스펙에서 프로토콜 레벨 세션과 초기화 핸드셰이크가 제거되고(SEP-2575, SEP-2567) `server/discover`가 추가됐습니다.
    -   Tasks는 공식 extension으로 분리됐고(SEP-2663), list 결과는 캐시 가능해졌습니다(SEP-2549).
    -   agent identity 축은 DPoP와 Workload Identity Federation, 표준 token exchange 채택을 목표로 합니다.
    [Source URL](https://blog.modelcontextprotocol.io/posts/mcp-roadmap/) (Model Context Protocol Blog)
    > 시사점: 자체 MCP 서버가 세션 기반 초기화에 기대고 있다면 07-28 스펙 기준으로 먼저 걷어내세요.

---

### Inference Serving

*   **로컬 LLM이 멍청해 보이는 원인을 모델이 아니라 quantization과 attention backend에서 찾은 실측**
    -   NVIDIA NVFP4는 88k context에서 토큰 불일치가 약 50%까지 벌어졌고, INT8 W8A16이 가장 안정적이었습니다.
    -   int4 KV cache에서는 tool call이 실패했고 int8은 회복, BF16은 일관성을 유지했습니다.
    -   같은 설정에서 TP1과 TP4는 통과한 tool call이 TP2에서만 실패했습니다.
    [Source URL](https://forum.level1techs.com/t/why-your-local-llm-feels-dumber-than-it-is/253917) (Level1Techs Forum)
    > 시사점: 자체 호스팅에서 tool call 실패가 잦다면 모델 교체 전에 KV cache 양자화를 BF16으로 되돌려 재보세요.

---

### Research Agents

*   **프런티어 모델 18종을 nanoGPT speedrun에 풀어 자율 연구 능력을 측정 — 총 153회 실행**
    -   런당 8×H200에서 최대 8일을 돌렸고, 최고 기록 2,726 step으로 인간 기록(2,600)까지 남은 격차의 81.7%를 좁혔습니다.
    -   상위 모델은 실험 횟수가 아니라 noise 모델링과 ablation 설계에서 갈렸습니다.
    -   어떤 런도 근본적으로 새로운 방법을 만들어내지는 못했습니다.
    [Source URL](https://www.primeintellect.ai/blog/measuring-autonomous-research) (Prime Intellect)
    > 시사점: 에이전트에 실험을 맡길 계획이면 실행 예산보다 ablation과 noise 판단 품질을 먼저 평가하세요.

---

### Dart Language

*   **Dart primary constructor 설계 후기 — 클래스 이름 반복 대신 `new()`/`factory()` 문법을 택함**
    -   본문이 필요하면 `this { ... }` 블록을 쓰고, 본문이 없는 클래스는 `{}` 대신 `;`로 닫습니다.
    -   declaring parameter는 primary constructor에서만 허용되고 in-body constructor에는 열지 않았습니다.
    -   필드 기반 추론안은 생성자가 사용자에게 공개되는 API라는 이유로 폐기됐습니다.
    [Source URL](https://dart.dev/blog/bringing-primary-constructors-to-dart) (The Dart Blog)
    > 시사점: 3.13에서 primary constructor로 옮길 때 생성자 선언의 클래스 이름이 `new()`로 바뀐다는 점부터 확인하세요.

---

### Android Build

*   **AGP 9.4 preview — 새 Variant API가 AGP 10부터 필수가 되고, 9.4에서만 모듈 단위 opt-out을 허용**
    -   `gradle.properties`에 `android.newDsl.optOut=:example-lib1` 형태로 예외 모듈을 지정합니다.
    -   앱 모듈과 dynamic feature 모듈의 flavor dimension 1:1 검사가 기본 warning으로 들어왔고, AGP 10에서는 빌드 실패가 됩니다.
    -   `android.enforceDynamicFeatureVariantMatching=true`로 지금 error로 승격해 미리 확인할 수 있습니다.
    [Source URL](https://developer.android.com/build/releases/agp-9-4-0-release-notes) (Android Developers)
    > 시사점: dynamic feature를 쓰고 있다면 이 플래그를 켜서 AGP 10 전에 variant 불일치를 드러내세요.

---

오늘 항목은 스펙이든 빌드 규칙이든 양자화 설정이든, 새 기능이 아니라 계약과 기본값을 좁히는 쪽에서 차이가 났다는 점에서 겹칩니다.
