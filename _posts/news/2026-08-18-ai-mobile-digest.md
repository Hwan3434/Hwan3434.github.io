---
layout: post
title: "AI · 모바일 다이제스트 - 2026-08-18"
date: 2026-08-18 06:10:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## 오늘의 흐름: AI가 쓴 코드가 CI를 뚫는 방식, 과잉 reasoning의 실제 비용, 8월 31일 마감

-   Copilot Autofix가 만든 PR에 CI 스크립트 인젝션
-   Qwen 3.8 27B, 기본 reasoning effort가 xhigh
-   llama.cpp, Kimi-K3를 MXFP4 무손실 repack으로 지원
-   Android Studio Quail 4, Gemma 4를 IDE에서 로컬 실행
-   8월 31일부터 targetSdk 36 미만은 신규 배포 제한
-   klibs.io, KMP 라이브러리용 MCP 서버 공개

---

### Agent Security

*   **Copilot Autofix가 작성한 PR이 GitHub Actions 스크립트 인젝션을 만들고 Jira 토큰이 유출됨**
    -   `snowflake-connector-net`의 워크플로가 `env:` 전달을 `echo '${{ github.event.issue.title }}'`로 바꾸면서, issue 제목에 따옴표를 넣어 명령을 실행할 수 있게 됐습니다.
    -   가드 조건이 `github.event.pull_request.user.login`을 봤는데 issue 이벤트에서는 null이라 항상 통과했습니다.
    -   6월 18일 병합부터 6월 23일 패치까지 5일간 노출됐고, 유출된 토큰으로 Jira 프로젝트 읽기가 가능했습니다.
    [Source URL](https://www.wiz.io/blog/red-agent-snowflake-copilot-cicd-bug) (Wiz)
    > 시사점: AI가 생성한 CI/CD 변경은 `run:` 안의 템플릿 확장을 `env:`나 `jq --arg`로 되돌리는지부터 리뷰 항목에 넣으세요.

---

### Local Inference

*   **Qwen 3.8 27B, 기본 reasoning effort가 xhigh라 간단한 요청에도 과하게 생각함**
    -   SVG 하나를 그리는 데 reasoning token 22,276개와 21분을 썼고, reasoning을 끄면 137초에 끝났습니다.
    -   27B dense·Apache 2.0이고 Q4_K_M 기준 17GB, context는 262,144 token입니다.
    -   M5 Max 128GB의 LM Studio에서 15~30 token/s이고, Multi-Token Prediction을 켜면 약 72% 빨라집니다.
    [Source URL](https://simonwillison.net/2026/Aug/16/qwen-38-27b/) (Simon Willison)
    > 시사점: 로컬에 이 모델을 붙인다면 reasoning effort를 `low`나 off로 내린 값을 기본값으로 두세요.

---

### On-Device Runtime

*   **llama.cpp가 Kimi-K3 지원 — MXFP4 텐서를 재양자화 없이 repack**
    -   routed expert의 mxfp4-pack-quantized 가중치를 ggml MXFP4로 무손실 repack해 약 5.5TB짜리 bf16 변환 단계를 없앴습니다.
    -   KDA(linear)와 MLA(full)를 섞은 hybrid attention, latent MoE, cross-layer residual attention을 구현했습니다.
    -   fp32 reference 대비 최종 logits 상대 오차 6.7e-05, correlation 1.00000000으로 검증했습니다.
    [Source URL](https://github.com/ggml-org/llama.cpp/releases/tag/b10448) (llama.cpp)
    > 시사점: 대형 MoE를 로컬로 내릴 때 변환 디스크와 시간이 병목이라면 b10448 이후 빌드로 올리세요.

---

### Android Tooling

*   **Android Studio Quail 4 RC — Gemma 4를 IDE 안에서 로컬로 돌릴 수 있음**
    -   Settings > Tools > AI > Model Providers > Gemma에서 켜면 서드파티 호스팅 없이 코드 어시스트가 로컬에서 동작합니다.
    -   Agent Mode의 Firebase agent skill로 Authentication과 Cloud Firestore 설정을 IDE 안에서 끝냅니다.
    -   Compose Interactive Preview에 Navigate Back 액션과 Predictive Back Progress 슬라이더가 추가됐습니다.
    [Source URL](https://developer.android.com/studio/preview/features) (Android Developers)
    > 시사점: 코드 반출이 막힌 조직이라면 Gemma 4 로컬 provider를 먼저 검증해 보세요.

---

### Store Policy

*   **Google Play, 8월 31일부터 targetSdk 36 미만 앱은 신규 사용자에게 노출 중단**
    -   신규 앱과 업데이트는 Android 16(API 36) 이상을 타깃해야 하고, Wear OS·Automotive는 35, TV·XR은 34가 기준입니다.
    -   스토어에서 내려가는 것이 아니라, 앱 target보다 높은 OS를 쓰는 신규 사용자에게만 노출되지 않습니다.
    -   Play Console의 Policy status 페이지에서 11월 1일까지 연장을 신청할 수 있습니다.
    [Source URL](https://support.google.com/googleplay/android-developer/answer/11926878?hl=en) (Google Play Console Help)
    > 시사점: 이번 주에 `targetSdkVersion`을 확인하고 36 대응이 안 끝났다면 연장 신청부터 넣으세요.

---

### KMP Tooling

*   **klibs.io가 4,200개 KMP 프로젝트로 확장 — MCP 서버와 expert skill 추가**
    -   MCP 서버로 agent가 platform·target 기준 검색과 최신 published 버전 조회를 index에서 직접 수행합니다.
    -   Kotlin Multiplatform Libraries expert skill이 플랫폼 지원 확인과 dependency 좌표 조회를 담당합니다.
    -   프로젝트에 넣을 AGENTS.md 스니펫을 함께 제공합니다.
    [Source URL](https://blog.jetbrains.com/kotlin/2026/08/klibsio-grows-to-4200-kmp-projects-with-smarter-discovery-and-new-ai-integrations/) (JetBrains)
    > 시사점: KMP 의존성 선택을 agent에게 맡기고 있다면 학습 데이터 대신 klibs.io MCP를 물려 버전 환각을 줄이세요.

---

오늘 항목은 AI가 만들어 낸 코드와 의존성을 어디서 검증할 것인가로 모이고, 모바일 쪽에서는 그 지점이 IDE 안의 로컬 모델과 8월 31일 정책 마감으로 갈립니다.
