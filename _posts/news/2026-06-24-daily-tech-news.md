---
layout: post
title: "데일리 테크 뉴스 - 2026-06-24"
date: 2026-06-24 21:26:58 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## 오늘의 개발자 뉴스: 팀 단위 AI 에이전트, Gemini API 변경, 그리고 모바일 개발 업데이트

2026년 6월 24일 기준으로 개발자에게 직접 영향이 있는 AI 에이전트, API, 모바일/프론트엔드, 국내 기술 블로그 소식을 정리했습니다. 주가, 실적, 경영진 중심 뉴스는 제외했습니다.

---

### AI 에이전트와 개발 워크플로우

*   **Anthropic, Slack에서 협업하는 Claude Tag 베타 공개**
    Anthropic은 팀 채널에서 `@Claude`를 태그해 작업을 위임하는 Claude Tag를 공개했습니다. Claude Enterprise와 Team 고객을 대상으로 Slack 베타를 시작하며, 선택된 채널과 도구, 데이터, 코드베이스에 접근 권한을 부여해 공동 작업 맥락을 누적하는 방식입니다. 코딩 에이전트가 개인 도구에서 팀 단위 협업 주체로 이동하고 있다는 점에서 개발 조직의 운영 방식에 의미가 있습니다.
    [Source URL](https://www.anthropic.com/news/introducing-claude-tag) (Anthropic)

*   **OpenAI Codex, 개발자를 넘어 지식 작업 자동화로 확장**
    OpenAI는 Codex가 코드 작성뿐 아니라 리서치, 데이터 분석, 문서/스프레드시트/프레젠테이션 생성, 업무 자동화에 쓰이고 있다고 설명했습니다. 별도 발표에서는 역할별 플러그인, Sites, annotations를 통해 팀 워크플로우에 Codex를 더 깊게 연결하는 방향을 제시했습니다. 개발자 입장에서는 에이전트 결과물을 코드 저장소 밖 산출물까지 검토하고 운영하는 일이 늘어날 수 있습니다.
    [Source URL](https://openai.com/index/codex-for-knowledge-work/) (OpenAI)
    [Source URL](https://openai.com/index/codex-for-every-role-tool-workflow/) (OpenAI)

*   **Google Developers, ADK와 A2A 중심의 멀티 에이전트 개발 흐름 강화**
    Google Developers Blog는 Agent Development Kit와 A2A 프로토콜 기반의 크로스 언어 멀티 에이전트 예제, Jules 측정 방식, agentic UI, resource discovery 등 에이전트 개발 관련 글을 전면에 배치했습니다. Python, Go, Android/Kotlin 등 여러 런타임에서 에이전트 협업을 구성하려는 팀에게 참고할 만한 흐름입니다.
    [Source URL](https://developers.googleblog.com/) (Google Developers Blog)

---

### API와 플랫폼 변경

*   **Gemini API, Interactions API GA와 음성 스트리밍 지원**
    Google AI for Developers 문서에 따르면 Interactions API가 GA가 되었고, 신규 프로젝트에서 최신 모델과 기능을 쓰기 위한 권장 인터페이스로 안내되고 있습니다. 6월 17일에는 `gemini-3.1-flash-tts-preview` 모델의 speech generation streaming 지원도 추가되었습니다. 기존 `generateContent` 기반 통합은 유지되지만, 새 기능을 쓰려는 팀은 Interactions API 전환 계획을 검토할 필요가 있습니다.
    [Source URL](https://ai.google.dev/gemini-api/docs/changelog) (Google AI for Developers)
    [Source URL](https://ai.google.dev/gemini-api/docs/interactions-overview) (Google AI for Developers)

*   **Gemini 이미지/비디오 모델 deprecation 일정 확인 필요**
    Google은 Imagen 4 및 Gemini 3 Image 모델 일부를 2026년 8월 17일 종료 예정으로, Veo 2/3 계열 일부 모델을 2026년 6월 30일 종료 예정으로 공지했습니다. 이미지/비디오 생성 기능을 제품에 연결한 팀은 모델 ID, 대체 모델, 배포 일정을 빠르게 점검해야 합니다.
    [Source URL](https://ai.google.dev/gemini-api/docs/deprecations) (Google AI for Developers)

*   **Apple, iOS/iPadOS/macOS 27 디자인 키트와 최신 베타 릴리스 제공**
    Apple Developer는 iOS, iPadOS, macOS 27용 Figma/Sketch 디자인 키트를 공개했습니다. Liquid Glass 업데이트, 컴포넌트와 상태 확장, 코드와 맞춘 명명 변경, macOS Dark Mode 지원 등이 포함됩니다. 릴리스 페이지에는 Xcode 27 beta 2 및 iOS/iPadOS/macOS/tvOS/visionOS 27 beta 2도 올라와 있어 앱 개발자는 SDK와 UI 리소스를 함께 확인할 시점입니다.
    [Source URL](https://developer.apple.com/news/) (Apple Developer)
    [Source URL](https://developer.apple.com/news/releases/) (Apple Developer Releases)

---

### 앱 개발과 국내 기술 블로그

*   **Flutter 팀, Gemini/Firebase를 결합한 AI 커피숍 데모 공개**
    Flutter 팀은 Flutter, Firebase, Gemini를 사용해 주문 경험을 구성한 AI 커피숍 데모를 소개했습니다. 실제 제품 코드라기보다 참고용 데모지만, 크로스 플랫폼 UI와 생성형 AI 백엔드를 엮어 사용자 경험을 만드는 패턴을 확인할 수 있습니다.
    [Source URL](https://blog.flutter.dev/how-we-built-a-flutter-powered-ai-coffee-shop-878c60a11f1a) (Flutter Blog)

*   **Toss Tech, 코딩 에이전트용 Skill 품질 Rubric 구현 경험 공유**
    토스 AI DX Team은 사내 공용 Skill이 잘 호출되고 실제로 효과를 내도록 6개 섹션, 30개 항목의 품질 Rubric을 설계한 경험을 공개했습니다. LLM이 읽고 호출하는 개발 보조 도구는 컴파일러나 테스트처럼 명확한 게이트가 부족하므로, 에이전트 도구 품질을 관리하려는 팀에 실용적인 참고가 됩니다.
    [Source URL](https://toss.tech/article/skill-quality-rubric) (Toss Tech)

*   **NAVER D2, AI 에이전트 실험/개선과 Playwright E2E 하네스 사례 공개**
    NAVER D2는 사내 기술 교류 행사 발표를 통해 AI 에이전트가 코드를 실험하고 개선하는 방식, 그리고 AI 에이전트를 위한 Playwright E2E 테스트 하네스 구축 사례를 공개했습니다. 에이전트가 만든 변경을 어떻게 실행, 검증, 피드백 루프로 연결할지 고민하는 개발팀에 유용한 주제입니다.
    [Source URL](https://d2.naver.com/helloworld/8061804) (NAVER D2)
    [Source URL](https://d2.naver.com/helloworld/6811215) (NAVER D2)

*   **Hacker News, AI 개발 스택과 워크플로우 논의 지속**
    Hacker News에서는 최신 AI 개발 스택과 워크플로우를 묻는 토론이 이어졌습니다. 특정 제품 발표는 아니지만, 개발자들이 에이전트형 IDE, LLM CLI, 테스트/리뷰 자동화, 로컬 모델을 어떻게 조합하는지 살펴볼 수 있는 커뮤니티 신호입니다.
    [Source URL](https://news.ycombinator.com/item?id=48413629) (Hacker News)

---

오늘의 핵심은 에이전트가 개인 코딩 보조를 넘어 팀 협업, API, 테스트 하네스, 사내 도구 품질 관리까지 넓어지고 있다는 점입니다. API deprecation과 베타 SDK는 실제 제품에 영향을 줄 수 있으니 관련 통합을 먼저 점검하는 것이 좋겠습니다.
