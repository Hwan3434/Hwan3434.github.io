---
layout: post
title: "데일리 테크 뉴스 - 2026-06-25"
date: 2026-06-25 06:36:06 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## 오늘의 개발자 뉴스: AI 보안 패치, 로컬 에이전트, 그리고 플랫폼 변경

2026년 6월 25일 기준으로 개발자에게 직접 영향이 있는 AI 보안, 에이전트 개발, API/플랫폼 변경, 앱 개발 소식을 정리했습니다. 주가, 실적, 경영진 중심 뉴스는 제외했습니다.

---

### AI 보안과 오픈소스 유지보수

*   **OpenAI, Daybreak와 Patch the Planet으로 취약점 발견에서 패치까지 확장**
    OpenAI는 Daybreak를 확대하며 Codex Security 플러그인 업데이트, 제한 공개 중인 GPT-5.5-Cyber, 보안 파트너 프로그램, 오픈소스 유지보수자 지원 프로그램 Patch the Planet을 공개했습니다. Patch the Planet은 Trail of Bits, HackerOne, Calif 등과 함께 cURL, Go, Python, Sigstore, pyca/cryptography 같은 핵심 오픈소스 프로젝트의 취약점 검증, 패치 작성, 테스트, 공개 조율을 지원합니다. 개발팀 입장에서는 AI 보안 도구가 단순 보고서 생성이 아니라 CI/CD, threat model, patch review까지 들어오는 흐름으로 볼 수 있습니다.
    [Source URL](https://openai.com/index/daybreak-securing-the-world/) (OpenAI)
    [Source URL](https://openai.com/index/patch-the-planet/) (OpenAI)

*   **OpenAI, 장기 작업용 Codex 운용 가이드 공개**
    OpenAI는 Codex를 단일 프롬프트 도구가 아니라 컨텍스트를 유지하는 지속 작업 공간으로 쓰는 방법을 담은 Codex-maxxing 가이드를 공개했습니다. 큰 목표를 검증 가능한 단계로 나누고, 여러 작업 흐름의 연속성을 유지하며, 어느 지점에서 사람이 감독해야 하는지 판단하는 전략이 핵심입니다. 에이전트 기반 개발을 운영하는 팀에는 작업 분해, 검증, 리뷰 루프 설계가 더 중요해지고 있습니다.
    [Source URL](https://openai.com/index/codex-maxxing-long-running-work/) (OpenAI)

---

### 에이전트 개발과 로컬 AI

*   **Google Developers, ADK와 A2A로 Python-Go 멀티 에이전트 예제 공개**
    Google Developers Blog는 Python 에이전트가 Gemini로 계약 데이터를 추출하고 Go 에이전트가 결정론적 정책 검사를 수행하는 예제를 공개했습니다. Agent Development Kit의 `RemoteA2aAgent`와 Agent2Agent 프로토콜을 사용해 언어가 다른 에이전트를 한 파이프라인으로 묶는 방식입니다. 프로덕션 AI 시스템에서 거대한 단일 프롬프트보다 작은 책임을 가진 에이전트와 명확한 실패 처리, 감사 가능한 결정론적 컴포넌트를 조합하는 패턴이 강조됩니다.
    [Source URL](https://developers.googleblog.com/build-cross-language-multi-agent-team-with-google-agent-development-kit-and-a2a/) (Google Developers Blog)

*   **Google AI Edge, Gemma 4 12B 기반 로컬 에이전트 워크플로우 소개**
    Google은 Gemma 4 12B를 Google AI Edge Gallery, AI Edge Eloquent, LiteRT-LM CLI와 결합해 노트북에서 로컬 에이전트 작업을 실행하는 흐름을 소개했습니다. LiteRT-LM의 `serve` 명령은 로컬 OpenAI 호환 엔드포인트를 열어 Continue, Aider 같은 도구나 사내 하네스에 연결할 수 있습니다. 데이터가 로컬에 남는 분석, 음성 편집, 코드 실행 워크플로우를 검토하는 팀에 참고할 만합니다.
    [Source URL](https://developers.googleblog.com/bringing-gemma-4-12b-to-your-laptop-unlocking-local-agentic-workflows-with-google-ai-edge/) (Google Developers Blog)

*   **Anthropic API, 구형 Claude 모델 종료와 도구 응답 최적화 반영**
    Anthropic의 Claude Platform 릴리스 노트에 따르면 `claude-sonnet-4-20250514`와 `claude-opus-4-20250514`는 6월 15일 종료되어 요청 시 오류를 반환합니다. 6월 11일에는 code execution tool의 시간 제한 설명 개선, web search/fetch tool의 `response_inclusion` 파라미터가 추가되어 에이전트 응답에서 사용한 결과 블록을 줄일 수 있게 됐습니다. Claude API를 쓰는 서비스는 모델 ID와 tool 응답 처리 방식을 함께 점검해야 합니다.
    [Source URL](https://platform.claude.com/docs/en/release-notes/overview) (Anthropic Claude Platform)

---

### API와 플랫폼 변경

*   **Gemini API, 음성 생성 스트리밍과 모델 종료 일정 재확인**
    Google AI for Developers는 `gemini-3.1-flash-tts-preview`에서 `streamGenerateContent` 및 Interactions API의 `stream: true`를 통한 음성 생성 스트리밍 지원을 추가했습니다. 동시에 Veo 2/3 계열 일부 모델은 2026년 6월 30일 종료 예정이고, Imagen 4 및 Gemini 3 Image 일부 모델은 2026년 8월 17일 종료 예정입니다. 생성형 미디어 기능을 제품에 붙인 팀은 모델 ID, 대체 모델, 배포 일정을 빠르게 확인해야 합니다.
    [Source URL](https://ai.google.dev/gemini-api/docs/changelog) (Google AI for Developers)
    [Source URL](https://ai.google.dev/gemini-api/docs/deprecations) (Google AI for Developers)

*   **Apple, iOS 27 디자인 키트와 브라질 배포/결제 정책 변경 안내**
    Apple Developer는 iOS, iPadOS, macOS 27용 Figma/Sketch 디자인 키트를 공개했으며, Liquid Glass 업데이트와 컴포넌트 상태 확장, macOS Dark Mode 지원을 포함합니다. 또한 브라질 경쟁 당국 CADE와의 합의에 따라 iOS 26.5부터 브라질에서 대체 앱 마켓플레이스, 대체 결제, 외부 결제 안내 옵션을 제공한다고 공지했습니다. 글로벌 앱을 운영하는 팀은 UI 리소스와 지역별 배포/결제 정책을 함께 확인해야 합니다.
    [Source URL](https://developer.apple.com/news/) (Apple Developer)
    [Source URL](https://developer.apple.com/news/releases/) (Apple Developer Releases)

---

### 앱 개발과 국내 기술 블로그

*   **Flutter, Gemini/Firebase 기반 AI 커피숍 데모 공개**
    Flutter 팀은 Flutter, Firebase, Gemini를 사용해 주문 경험을 구성한 AI 커피숍 데모를 소개했습니다. 유지보수되는 제품 코드라기보다 참고용 데모지만, 크로스 플랫폼 UI와 생성형 AI 백엔드를 연결해 실제 인터랙션을 만드는 구조를 빠르게 살펴볼 수 있습니다.
    [Source URL](https://blog.flutter.dev/how-we-built-a-flutter-powered-ai-coffee-shop-878c60a11f1a) (Flutter Blog)

*   **국내 기술 블로그, AI 하네스와 Skill 품질 관리 사례 축적**
    우아한형제들은 Cursor Rules와 Skills를 활용한 팀 맞춤형 AI 코딩 환경 구축, RAG 챗봇, LLM 기반 다국어 프로젝트 사례를 연이어 공개했습니다. Toss Tech는 코딩 에이전트용 Skill 품질을 6개 섹션 30개 항목 Rubric으로 관리한 경험을 공유했습니다. 공통적으로 AI 도입의 초점이 모델 선택에서 컨텍스트, 검증, 운영 가능한 하네스 설계로 이동하고 있습니다.
    [Source URL](https://techblog.woowahan.com/) (Woowahan Tech)
    [Source URL](https://toss.tech/article/skill-quality-rubric) (Toss Tech)

*   **Hacker News, AI 개발 스택과 모바일 앱 개발 변화 논의 지속**
    Hacker News에서는 AI 개발 스택/워크플로우와 2026년 앱 개발의 상태를 묻는 토론이 이어지고 있습니다. 공식 발표는 아니지만, 개발자들이 에이전트형 IDE, LLM CLI, 테스트 자동화, 모바일 개발 커리어 변화를 어떻게 체감하는지 확인할 수 있는 커뮤니티 신호입니다.
    [Source URL](https://news.ycombinator.com/item?id=48413629) (Hacker News)
    [Source URL](https://news.ycombinator.com/item?id=48337409) (Hacker News)

---

오늘의 핵심은 AI 에이전트가 코드 작성 도구를 넘어 보안 패치, 로컬 실행, 크로스 언어 오케스트레이션, 운영 가능한 개발 하네스로 확장되고 있다는 점입니다. API 모델 종료와 플랫폼 정책 변경은 실제 배포에 영향을 줄 수 있으니 먼저 점검하는 것이 좋겠습니다.
