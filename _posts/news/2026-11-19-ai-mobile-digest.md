---
title: "Compose 1.13, Google Play 폴더블 품질 기준, MoE expert streaming (2026. 11. 19)"
description: "Compose 1.13이 안정화되고 Play는 2027년 4월부터 폴더블 기준을 요구하며, Transformers는 SSD expert streaming을 시도했습니다."
date: 2026-11-19 08:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## 오늘의 흐름: MoE expert streaming, curl Rust 재작성, Compose 1.13, Play 폴더블 기준

-   180B MoE를 32GB 메모리 Mac에서 실행
-   curl Rust 재작성 클론과 취약점 통계
-   Compose 1.13 안정화, ConstraintLayout 지원 중단
-   Play, 2027년 4월부터 폴더블 품질 요구

---

### AI Engineering

*   **Hugging Face, MoE expert를 SSD에서 읽어 180B 모델을 32GB Mac에서 실행**
    -   router가 고른 expert만 SSD에서 읽어 12 GiB cache에 올리고, expert는 3-bit로 양자화합니다.
    -   Qwen3.8-Flash-Next(180B)는 M5 MacBook에서 decode 13.9 tok/s이고 peak 메모리는 25.4 GiB입니다.
    -   Transformers PR #50717이 `from_pretrained`에 `experts_offload` 옵션을 추가합니다.
    [Source URL](https://huggingface.co/blog/moe-expert-streaming) (Hugging Face Blog)
    > 시사점: 아직 PR 단계이므로 온디바이스 대형 MoE는 expert 단위 offload 가능성만 확인해 두세요.

*   **curl 메인테이너, AI 에이전트의 curl Rust 재작성에 대해 의견 공개 — 3주간 curl은 300+ commit**
    -   에이전트가 C 약 185,000줄을 Rust 약 340,000줄로 바꿨고, 같은 기간 curl에는 bugfix 200여 개가 들어갔습니다.
    -   올해 확인된 취약점 81개 중 14개(17.3%)만 memory-safe 언어였다면 피할 수 있었던 것입니다.
    [Source URL](https://daniel.haxx.se/blog/2026/11/17/actual-curl-rewrites-in-rust/) (daniel.haxx.se)
    > 시사점: 에이전트 포팅을 검토한다면 언어 전환 효과보다 upstream 수정을 따라가는 비용을 먼저 보세요.

---

### Android Compose

*   **Jetpack Compose 1.13 안정화 — BOM 2026.11.01, Kotlin 2.2와 compileSdk 37.1 필요**
    -   `computedStateOf`가 추가되어 `derivedStateOf`보다 가벼운 조건 계산이 가능합니다.
    -   `FlexBox`와 `Grid`가 stable이 되었고, `constraintlayout-compose`는 deprecated입니다.
    -   `material3-a2ui:1.0.0-alpha02`로 A2UI 메시지를 Compose로 렌더링할 수 있습니다.
    [Source URL](https://developer.android.com/blog/posts/jetpack-compose-november-2026-release.md.txt) (Android Developers Blog)
    > 시사점: 업그레이드 전에 `ConstraintLayout`과 `Modifier.onFocusedBoundsChanged` 사용처를 확인하세요.

*   **Google Play, 2027년 4월부터 폴더블 기준 요구 — 미달 앱은 게시와 업데이트 불가**
    -   adaptive app quality Tier 3를 충족해야 하고, 폴더블 스크린샷 3장이 phone 스크린샷 2장에 더해 필요합니다.
    -   2027년 8월부터 신규·업데이트 앱은 API 37(Android 17)을 target 해야 합니다.
    [Source URL](https://developer.android.com/blog/posts/google-play-adaptive-quality-standards.md.txt) (Android Developers Blog)
    > 시사점: 회전과 접힘 전환에서 상태가 유지되는지 폴더블 에뮬레이터로 점검하세요.

---

모두 새 기능을 쓰기 전에 기존 도구와 규칙이 어디까지 지켜 주는지 확인하라는 이야기입니다.
