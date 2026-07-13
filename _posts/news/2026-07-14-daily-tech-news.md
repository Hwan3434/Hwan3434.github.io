---
layout: post
title: "데일리 테크 뉴스 - 2026-07-14"
date: 2026-07-14 06:00:15 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## 오늘의 개발자 뉴스: AI 보안 분석, 에이전트 하네스, 오픈소스 도구

2026년 7월 14일 기준으로 개발자에게 직접 영향이 있는 App Store 제출 요건, 정적 분석 보안 규칙, AI 코딩 에이전트 운영 방식, 오픈소스 생산성 도구 소식을 정리했습니다. 주가, 실적, 경영진 중심 뉴스는 제외했습니다.

---

### 플랫폼과 애플리케이션 보안

*   **Apple, App Store Connect 연령 등급 설문에 소셜 미디어 항목 추가**
    Apple은 사용자 제작 콘텐츠를 소셜 피드 등으로 재배포·확산하거나 상호작용할 수 있는지를 묻는 항목을 연령 등급 설문에 추가했습니다. 해당 기능이 있으면 제품 페이지에 새로운 Social Media 콘텐츠 설명이 표시되며, 13세 미만에게 기능을 비활성화한 경우에는 그 연령대의 Social Media Time Allowance 분류에서 제외됩니다. 개발자는 지금부터 답변할 수 있고 2026년 9월부터 새 앱·업데이트 제출과 대체 배포용 notarization에 응답이 필수이므로, 제출 자동화 문서와 심사 체크리스트를 미리 갱신해야 합니다.
    [Source URL](https://developer.apple.com/news/?id=tlur8uvi) (Apple Developer)

*   **CodeQL 2.26.0, JavaScript·TypeScript system prompt injection 탐지 추가**
    GitHub는 신뢰할 수 없는 사용자 입력이 AI 모델의 system prompt로 흐르는 경로를 찾는 `js/system-prompt-injection` query를 CodeQL 2.26.0에 추가했습니다. OpenAI, Anthropic, Google GenAI SDK의 prompt sink 모델이 확장됐고 Kotlin 2.4.0, C# Razor Pages, Go `log/slog`, Swift CryptoKit 분석도 개선됐습니다. github.com의 code scanning에는 자동 배포되지만 구형 GitHub Enterprise Server는 CodeQL을 수동 업그레이드해야 새 탐지를 적용할 수 있습니다.
    [Source URL](https://github.blog/changelog/2026-07-10-codeql-2-26-0-adds-kotlin-2-4-0-support-and-ai-prompt-injection-detection/) (GitHub Changelog)

---

### AI 코딩 에이전트 운영

*   **Martin Fowler, agent harness의 핵심을 context 집중과 검증 sensor로 정리**
    Martin Fowler는 Future of Software Development Retreat 논의를 바탕으로 큰 context window 자체보다 모델이 올바른 정보에 집중하도록 작은 `AGENTS.md`와 context를 관리하는 일이 중요하다고 전했습니다. 검증 측면에서는 property-based testing과 formal method 같은 computational sensor가 주목받았고, 이런 harness가 token 사용량을 낮추면서 비교적 약한 모델과 self-hosted model도 실용적으로 만든다는 관찰을 공유했습니다. 팀이 에이전트에 넘기는 작업 범위를 키울수록 지침의 양보다 명시적 acceptance criteria와 자동 검증 경계를 먼저 설계할 필요가 있습니다.
    [Source URL](https://martinfowler.com/fragments/2026-07-13.html) (Martin Fowler)

---

### 오픈소스 개발 도구

*   **Logseq 2.0.1 DB 버전, 첫 공개 beta 배포**
    Logseq가 오랫동안 개발해 온 DB 버전의 첫 2.0 beta를 데스크톱과 Android용으로 공개했습니다. 프로젝트는 이를 초기 beta로 명시하고 중요한 데이터를 백업한 뒤 시험할 것을 권고하며, 기존 버전과 DB 버전을 분리해 운영하는 roadmap도 함께 안내합니다. plugin이나 자동화 workflow를 유지하는 개발자는 운영 graph를 바로 이전하기보다 별도 백업에서 데이터 호환성과 확장 기능 동작을 먼저 확인하는 편이 안전합니다.
    [Source URL](https://github.com/logseq/logseq/releases/tag/2.0.1) (Logseq)

*   **`dom-docx`, semantic HTML을 편집 가능한 OOXML 문서로 변환**
    Hacker News에서 주목받은 MIT 라이선스 TypeScript 프로젝트 `dom-docx`는 HTML fragment를 screenshot이나 1×1 layout table이 아닌 Word의 native paragraph, list, table, image 구조로 변환합니다. 기본 inline-style 경로는 Node.js와 browser에서 pure JavaScript로 실행되고, computed style이나 복잡한 chart 변환이 필요할 때만 Playwright와 rasterization을 선택적으로 사용합니다. 현재 v0.1.x는 CSS grid, web font, 복잡한 SVG와 완전한 multi-page layout fidelity를 지원하지 않으므로 문서 export 도입 전 지원 범위와 regression score harness를 함께 검토해야 합니다.
    [Source URL](https://github.com/floodtide/dom-docx) (GitHub Repository)

---

오늘의 흐름은 AI 기능을 제품에 붙이는 단계에서 그 동작을 통제하고 검증하는 단계로 관심이 이동하고 있다는 점입니다. system prompt로 들어가는 data flow, agent context와 acceptance criteria, beta data migration, 문서 구조 보존처럼 배포 후 되돌리기 어려운 경계를 자동 검사하는 일이 중요해지고 있습니다.
