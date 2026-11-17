---
title: "GPT-6.2 Astra·Sol, Flutter A2UI 1.0, R8 consumer keep rules (2026. 11. 18)"
description: "GPT-6.2 Astra와 Sol 가격이 공개되고, Flutter는 A2UI 1.0을 냈으며, Android는 라이브러리용 R8 keep rule 가이드를 밝혔습니다."
date: 2026-11-18 08:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## 오늘의 흐름: GPT-6.2 Astra·Sol, 코딩 에이전트 sandbox, Flutter A2UI 1.0, R8 consumer keep rules

-   GPT-6.2 Astra $8/$40, Sol $2/$10
-   코딩 에이전트용 외부 sandbox 3종 공개
-   llm 0.37.3, SQLite 3.54.1 로깅 오류 수정
-   Flutter A2UI 1.0, a2ui_flutter 공개
-   R8, 라이브러리 consumer keep rule 좁히기

---

### AI Engineering

*   **OpenAI, GPT-6.2 Astra와 Sol 공개 — Astra는 GPT-6 Astra보다 20% 저렴**
    -   Astra는 입력·출력이 100만 토큰당 $8/$40이고 cached input은 $0.40입니다.
    -   Sol은 $2/$10으로 GPT-6.1 Sol과 같고, GPT-5.6 Sol($4/$20)의 절반입니다.
    -   llm 0.38이 두 모델을 지원합니다.
    [Source URL](https://simonwillison.net/2026/Nov/17/gpt62-astra-and-sol/) (Simon Willison)
    > 시사점: 반복 호출이 많다면 cached input 단가 하락($1에서 $0.40)을 반영해 비용을 다시 계산하세요.

*   **코딩 에이전트를 sandbox 밖에서 돌리는 패턴 — 같은 localhost API를 쓰는 서버 3종 공개**
    -   `external-sandbox-v86`, `external-sandbox-container`, `external-sandbox-quicksand`가 각각 WebAssembly, Apple Containers, QEMU로 Alpine Linux를 띄웁니다.
    -   HTTP/HTTPS allow-list proxy로 접속 가능한 호스트를 제한하고, 에이전트에 비밀 값을 주지 않고 인증 호출을 할 수 있습니다.
    [Source URL](https://simonwillison.net/2026/Nov/17/external-sandboxes-for-coding-agents/) (Simon Willison)
    > 시사점: 로컬 모델에 코드 실행을 맡길 때는 호스트 대신 sandbox와 allow-list 뒤에서 실행하세요.

*   **llm 0.37.3 — Homebrew의 SQLite 3.54.1에서 깨진 로깅 수정**
    -   `select json_object('a', (select json_array(1)))`가 3.54.0에서는 `{"a":[1]}`, 3.54.1에서는 `{"a":"[1]"}`를 돌려줍니다.
    -   문서상 서브쿼리는 JSON이 아니라 SQL 텍스트를 돌려주는 것이 맞고, `json()`으로 감싸면 해결됩니다.
    [Source URL](https://simonwillison.net/2026/Nov/16/llm/) (Simon Willison)
    > 시사점: 서브쿼리 결과를 `json_object`에 넣는 코드가 있다면 `json()`으로 감싸세요.

---

### Flutter GenUI

*   **Flutter, A2UI 1.0과 `a2ui_flutter` 공개 — 이전 이름은 `genui`**
    -   `MessageProcessor`가 `SurfaceController`와 `Conversation`을 대신하고, transport는 패키지에서 빠졌습니다.
    -   catalog에 `allowedParents`/`allowedChildren`을 두면 위반 시 `UNALLOWED_PARENT`, `UNALLOWED_CHILD`가 반환되고, 한 surface에서 catalog 여러 개를 쓸 수 있습니다.
    -   `callAgentFunction`으로 위젯이 LLM 호출 없이 백엔드 함수를 부릅니다.
    [Source URL](https://flutter.dev/blog/a2ui-launch) (Flutter Blog)
    > 시사점: `genui`를 쓰고 있다면 `MessageProcessor` 기준으로 마이그레이션 범위를 확인하세요.

---

### Android Optimization

*   **Android, 라이브러리 제공자용 R8 consumer keep rule 가이드 공개 — 넓은 rule이 앱의 DEX 최적화를 막음**
    -   `-keep public class com.google.android.gms.** { *; }` 같은 package 단위 rule은 앱의 좁은 rule을 덮어씁니다.
    -   reflection 대신 codegen을 쓰고, 불가피하면 진입점만 keep하며, 광고 adapter는 conditional keep rule을 씁니다.
    -   Android CLI `analyze` 명령과 R8 Configuration Analyzer로 keep된 클래스를 확인할 수 있습니다.
    [Source URL](https://developer.android.com/blog/posts/ship-smarter-keep-rules-unblock-dex-optimization.md.txt) (Android Developers Blog)
    > 시사점: SDK를 배포한다면 consumer rule에서 package 전체 keep을 찾아 진입점 단위로 좁히세요.

---

모두 에이전트가 실행되는 환경과 그 경계를 어떻게 좁게 설계하느냐의 이야기입니다.
