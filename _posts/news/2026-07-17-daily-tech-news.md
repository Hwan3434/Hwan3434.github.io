---
layout: post
title: "데일리 테크 뉴스 - 2026-07-17"
date: 2026-07-17 06:01:37 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## 오늘의 개발자 뉴스: 웹 Grounding, Prompt 빌드, Xcode 27 CI, 소프트웨어 보존

2026년 7월 17일 기준으로 개발자에게 직접 영향이 있는 AI agent의 실시간 웹 grounding, 대규모 prompt 관리 패턴, Apple 앱용 CI runner, 역사적 소프트웨어의 오픈소스 공개 소식을 정리했습니다. 주가, 실적, 경영진 중심 뉴스는 제외했습니다.

---

### AI Agent의 검색과 Prompt 운영

*   **Gemini Enterprise Agent Platform, Parallel Web Search를 native grounding provider로 추가**
    Google Cloud는 Parallel Web Systems의 검색 인프라를 Gemini Enterprise Agent Platform에 통합했습니다. 개발자는 Gemini API에서 호출하거나 Agent Studio에서 선택해 실시간 웹 결과와 원문 citation을 agent 응답에 연결할 수 있습니다. 검색 결과를 추출·영구 cache하거나 다른 LLM으로 후처리할 수 있어 catalog enrichment와 multi-agent orchestration 같은 구성에도 활용할 수 있으며, 민감한 workload를 위한 zero data retention 옵션도 제공합니다. 이용하려면 Google Cloud Marketplace에서 Parallel 서비스를 구독해야 하고 기존 Cloud 청구서에 사용량이 합산되므로, 도입 전 가격과 데이터 보존 설정을 함께 확인해야 합니다.
    [Source URL](https://developers.googleblog.com/expanding-choice-in-gemini-enterprise-agent-platform-introducing-grounding-with-parallel-web-search/) (Google Developers Blog)

*   **Google Developers Blog, 대규모 agent prompt를 build artifact로 관리하는 패턴 제안**
    단일 system prompt에 안전 정책, domain 규칙, tool 지침을 계속 추가하면 변경 영향 파악과 재사용이 어려워지고 누락된 변수 같은 오류가 runtime까지 미뤄집니다. 글은 prompt를 작은 skill template로 나눈 뒤 transpiler가 import와 변수를 해석하도록 하고, missing dependency·circular import·undefined variable를 build 시점에 검사하는 방식을 제안합니다. CI에서 생성된 golden file의 drift를 확인하고, runtime에는 필요한 skill만 불러오는 progressive disclosure를 적용하면 token 낭비도 줄일 수 있습니다. Agent가 새 skill을 제안하더라도 직접 실행 중인 지침을 바꾸는 대신 pull request와 eval을 거치게 하는 것이 핵심입니다.
    [Source URL](https://developers.googleblog.com/building-scalable-ai-agents-with-modular-prompt-transpilation/) (Google Developers Blog)

---

### CI/CD와 Apple 개발

*   **GitHub Actions, Xcode 27 runner image public preview 시작**
    GitHub-hosted macOS runner에서 Xcode 27과 최신 Apple SDK로 앱을 build·test할 수 있게 됐습니다. Workflow의 `runs-on`을 `xcode-27` 또는 `xcode-27-xlarge`로 지정하면 되며, 새 image는 기반 macOS 버전이 아니라 major Xcode 버전을 기준으로 지원됩니다. 다만 arm64 macOS runner에서만 제공되고 Intel runner는 지원하지 않으며 기존 image와 설치 도구 및 버전 구성이 다릅니다. Preview를 도입할 팀은 production workflow를 바로 교체하기보다 별도 job에서 compatibility와 dependency 차이를 먼저 검증하는 편이 안전합니다.
    [Source URL](https://github.blog/changelog/2026-07-16-xcode-27-runner-image-now-in-public-preview/) (GitHub Changelog)

---

### 오픈소스와 소프트웨어 보존

*   **Microsoft, 1990년대 IRC client `Comic Chat` 소스 공개**
    IRC 대화를 인물의 표정·동작과 speech bubble이 있는 comic panel로 자동 배치했던 Microsoft Comic Chat의 원본 source가 공개됐습니다. 1995년 Visual C++ 4.0과 MFC로 개발된 code snapshot뿐 아니라, 현재 Visual Studio에서 build하고 modern IRC server와 고해상도 Windows 환경에 맞추려는 AI-assisted modernization 예제도 포함됩니다. 완성된 재출시판은 아니지만 개발자는 오래된 C++/MFC codebase의 복원과 porting을 실험하고, rule-based 대화 해석 및 자동 layout이라는 초기 interface 설계를 직접 살펴볼 수 있습니다.
    [Source URL](https://opensource.microsoft.com/blog/2026/07/16/microsoft-comic-chat-is-now-open-source/) (Microsoft Open Source Blog)

---

오늘의 흐름은 agent와 개발 도구를 production에 넣기 위해 외부 정보, 내부 지침, build 환경을 모두 검증 가능한 artifact로 다루는 것입니다. Web grounding은 출처와 데이터 흐름을, prompt transpilation은 지침의 dependency와 변경 이력을, versioned runner는 toolchain을 명시적으로 고정합니다. 동시에 Comic Chat 공개는 오래된 source도 현대 도구로 다시 검증하고 학습할 수 있는 자산임을 보여줍니다.
