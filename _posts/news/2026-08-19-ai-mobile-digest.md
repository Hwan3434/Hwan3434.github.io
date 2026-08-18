---
layout: post
title: "AI · 모바일 다이제스트 - 2026-08-19"
date: 2026-08-19 06:10:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## 오늘의 흐름: keep rule 하나가 만든 47%, 에이전트를 가두는 법, 10월 1일 EU 새 약관

-   Tinder, R8 Configuration Analyzer로 콜드 스타트 47% 단축
-   ADK zero-trust 레퍼런스, gVisor 샌드박스와 semantic gateway
-   에이전트 메모리는 스위치가 아니라 모델별 용량 조절
-   Sentence Transformers 6.0에 MultiVectorEncoder 추가
-   Jetpack XR beta02, AnchorEntity가 AnchorSpace로
-   Apple EU, CTF 폐지하고 5% Core Technology Commission

---

### App Performance

*   **Tinder가 R8 Configuration Analyzer로 콜드 스타트를 47% 줄임 — 범인은 keep rule 하나**
    -   사내 라이브러리의 광범위한 keep rule 때문에 앱의 약 70%가 최적화되지 않은 상태였고, optimization score는 28%였습니다.
    -   앱 크기가 86.6MB에서 61.5MB로 28.98% 줄고, dex 파일은 17개에서 11개(시작 경로 3개 → 2개)가 됐습니다.
    -   AGP 9.3은 `build/outputs/mapping/release/configanalyzer.html`에 리포트를 자동 생성하고, `./gradlew :app:analyzeReleaseR8Config`로도 뽑습니다.
    [Source URL](https://android-developers.googleblog.com/2026/08/tinder-app-cold-start-r8-configuration-analyzer.html) (Android Developers)
    > 시사점: AGP 9.3으로 올려 리포트를 한 번 돌리고 optimization score부터 확인하세요.

---

### Agent Sandboxing

*   **Google이 ADK 기반 zero-trust 에이전트 레퍼런스 구현을 공개**
    -   동적 생성 코드는 gVisor 샌드박스에서만 실행하며 `--runtime=runsc`, `--network=none`, `--memory=64m`, 5초 타임아웃이 걸립니다.
    -   DB 변경마다 Cloud KMS HSM 키로 서명하고, 로컬 데모는 HMAC으로 대체합니다.
    -   semantic gateway가 모델 입출력에서 PII, 카드번호 패턴, `sk_live_` 계열 시크릿을 정규식으로 차단합니다.
    [Source URL](https://developers.googleblog.com/en/build-zero-trust-ai-agents-with-googles-agent-development-kit/) (Google Developers Blog)
    > 시사점: 에이전트에 코드 실행 툴을 붙였다면 zero-trust-agents 레퍼런스의 3계층을 그대로 옮겨 오세요.

---

### Agent Memory

*   **에이전트 메모리는 켜고 끄는 기능이 아니라 모델별로 조절하는 용량**
    -   gpt-oss-120b는 curated retrieval로 TGC가 39.9%에서 56.0%로 오르는데 토큰은 5%만 늘었습니다.
    -   DeepSeek-V3.2는 +9.5pp를 얻는 대신 토큰이 78% 늘고, Claude Opus 4.6은 +4.1pp에 그칩니다.
    -   AppWorld의 멀티스텝 태스크 585개에서 8개 모델을 ALTK-Evolve로 비교한 결과입니다.
    [Source URL](https://huggingface.co/blog/ibm-research/altk-evolve-hmm) (Hugging Face / IBM Research)
    > 시사점: 강한 모델에 가이드라인을 잔뜩 물리고 있다면 토큰 증가분 대비 정확도부터 다시 재보세요.

---

### Retrieval

*   **Sentence Transformers 6.0이 late interaction 모델을 1급으로 지원**
    -   `MultiVectorEncoder`로 ColBERT 계열을 로드하고 `encode_query()`, `encode_document()`로 비대칭 인코딩합니다.
    -   Natural Questions 지문 4,874개가 float32로 311.5MB인데 PLAID 인덱스에서 92MB, 같은 데이터의 dense 384d는 7.5MB입니다.
    -   `HierarchicalTokenPooling`을 `pool_factor=2`로 걸면 벡터가 1.99배 줄어도 BEIR 성능은 100.6% 유지됩니다.
    [Source URL](https://huggingface.co/blog/multi-vector-encoder) (Hugging Face)
    > 시사점: late interaction으로 갈지 고민 중이라면 dense 대비 10배 넘는 저장 비용을 먼저 계산해 두세요.

---

### Android XR

*   **Jetpack XR 코어 라이브러리가 beta 진입 — 이름과 시그니처가 바뀜**
    -   SceneCore, ARCore for Jetpack XR, XR Runtime이 모두 1.0.0-beta02로 올라갔고 Compose for XR은 아직 1.0.0-alpha17입니다.
    -   `AnchorEntity`가 `AnchorSpace`로 바뀌었고 `ActivitySpace`와 함께 `SpaceEntity`를 상속합니다.
    -   `Session.create`가 suspend 함수가 됐고, spatial audio와 session configuration용 테스트 API가 추가됐습니다.
    [Source URL](https://android-developers.googleblog.com/2026/08/jetpack-xr-sdk-core-libraries-beta.html) (Android Developers)
    > 시사점: alpha로 붙여 둔 XR 코드가 있다면 `AnchorEntity` 리네임과 `Session.create` suspend 전환부터 처리하세요.

---

### Store Policy

*   **Apple, EU 앱 사업 조건 개편 — 10월 1일 발효**
    -   설치당 부과하던 Core Technology Fee가 폐지되고, App Store 밖으로 배포된 앱의 디지털 거래에 5% Core Technology Commission이 붙습니다.
    -   Initial Acquisition Fee와 Store Services Fee는 사라지고, App Store 앱도 IAP와 대체 결제를 함께 제공할 수 있습니다.
    -   Developer Program License Agreement의 Attachment 14가 갱신돼 계정에서 동의해야 합니다.
    [Source URL](https://developer.apple.com/news/?id=gmws0jgp) (Apple Developer News)
    > 시사점: EU에 배포 중이라면 Attachment 14에 동의하고 10월 1일 기준으로 결제 경로별 수수료를 다시 계산하세요.

---

오늘 AI 쪽은 에이전트의 기본값(메모리 양, 실행 권한)을 사람이 다시 재는 이야기이고, 모바일 쪽은 도구와 릴리스 노트가 짚어 준 것을 기한 안에 반영하는 이야기입니다.
