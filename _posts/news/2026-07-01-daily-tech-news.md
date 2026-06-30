---
layout: post
title: "데일리 테크 뉴스 - 2026-07-01"
date: 2026-07-01 06:03:30 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## 오늘의 개발자 뉴스: 에이전트 모델, 평가 루프, 시스템 디버깅

2026년 7월 1일 기준으로 개발자에게 직접 영향이 있는 AI 모델과 API, agent workflow, 평가 자동화, 인프라 디버깅 소식을 정리했습니다. 주가, 실적, 경영진 중심 뉴스는 제외했습니다.

---

### AI 모델과 API

*   **Anthropic, Claude Sonnet 5 출시**
    Anthropic은 reasoning, tool use, coding, knowledge work를 강화한 `claude-sonnet-5`를 Claude API와 Claude Code에 출시했습니다. 8월 31일까지의 API 가격은 입력 100만 token당 2달러, 출력 100만 token당 10달러이며, 이후 각각 3달러와 15달러로 전환됩니다. 새 tokenizer 때문에 같은 입력이 Sonnet 4.6보다 약 1.0~1.35배 많은 token으로 계산될 수 있어, 마이그레이션 전 실제 prompt corpus로 품질뿐 아니라 token 사용량과 지연 시간도 다시 측정해야 합니다. 성능 수치는 Anthropic 자체 평가라는 점도 함께 고려할 필요가 있습니다.
    [Source URL](https://www.anthropic.com/news/claude-sonnet-5) (Anthropic)
    [Source URL](https://news.ycombinator.com/item?id=48736605) (Hacker News)

*   **Google, Nano Banana 2 Lite를 Gemini API에 추가**
    Google은 저지연·대량 이미지 생성과 편집을 위한 Gemini 3.1 Flash-Lite Image를 공개했습니다. 개발자는 stable model code `gemini-3.1-flash-lite-image`로 호출할 수 있고, 1K 이미지와 14개 aspect ratio, text/image 입력, multi-turn 편집, function calling, Batch API를 지원합니다. Google은 end-to-end latency 목표를 2초 미만으로 제시하지만 2K·4K 출력, caching, Live API는 지원하지 않으므로 실시간 UI prototype이나 대량 asset 생성처럼 속도와 비용이 우선인 경로에 맞습니다.
    [Source URL](https://deepmind.google/models/gemini-image/flash-lite/) (Google DeepMind)
    [Source URL](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-lite-image) (Google AI for Developers)

---

### 에이전트 개발과 평가

*   **Google, graph workflow 중심의 ADK Go 2.0 출시**
    ADK Go 2.0은 multi-agent application을 node와 edge의 graph로 구성하고, scheduler가 병렬 실행, 상태 저장, 중단과 재개를 맡는 workflow engine을 추가했습니다. Human-in-the-loop가 durable primitive로 들어가 process restart 뒤에도 승인을 이어갈 수 있고, per-node retry·timeout과 graph-wide concurrency 제한도 제공합니다. 1.0에서 올릴 때 `ToolContext`와 `CallbackContext`가 `agent.Context`로 통합되고 event field가 늘어나는 breaking change가 있으므로, custom context와 exact event equality를 쓰는 테스트는 migration guide에 맞춰 수정해야 합니다.
    [Source URL](https://developers.googleblog.com/announcing-adk-go-20/) (Google Developers Blog)

*   **Google, coding agent가 실행하는 agent 평가 skill 공개**
    Google의 quality-flywheel skill은 평가 data 준비, inference, AutoRater grading, failure 분석, 수정과 재평가의 5단계를 coding agent가 orchestration하도록 만듭니다. ADK 전용 package와 framework-independent package가 있으며, synthetic scenario나 OpenTelemetry production trace를 입력으로 사용할 수 있습니다. 특히 수정안을 제안하는 optimizer와 점수를 매기는 evaluation service를 분리해 self-grading을 막고, model-based judge의 절대 점수보다 반복 실행 사이의 delta를 보라는 설계 원칙이 실무적으로 중요합니다.
    [Source URL](https://developers.googleblog.com/driving-the-agent-quality-flywheel-from-your-coding-agent/) (Google Developers Blog)

*   **OpenAI, 판단 중심 과학 agent benchmark GeneBench-Pro 공개**
    GeneBench-Pro는 계산 생물학 10개 domain의 129개 문제에서 agent가 불완전한 data를 탐색하고, 분석 경로를 고치며, 결과가 의사결정에 충분한지 판단하는 능력을 측정합니다. 합성 data의 인과 구조와 정답을 알고 있어 rubric model 대신 결정적으로 채점할 수 있으며, 대표 문제 10개는 공개됩니다. OpenAI가 보고한 최고 pass rate도 31.5%에 그쳐, 긴 scientific workflow에서 tool 실행 성공과 분석 판단의 신뢰성을 별도로 평가해야 한다는 자료입니다.
    [Source URL](https://openai.com/index/introducing-genebench-pro/) (OpenAI)

---

### 인프라와 운영 사례

*   **OpenAI, crash 전체 집단 분석으로 18년 된 GNU libunwind race 수정**
    OpenAI는 Rockset 기반 C++ data infrastructure에서 발생한 return-to-null crash를 개별 core dump가 아니라 전체 crash dataset으로 분류해 조사했습니다. 그 결과 하나로 보였던 현상이 Azure host의 silent hardware corruption과 GNU libunwind의 one-instruction race라는 두 문제였음을 밝혔습니다. 즉시 libgcc unwinder로 전환한 뒤 reproducer와 fix를 upstream에 제출했으며, 희귀 장애에서는 stack trace 몇 개의 정밀 분석보다 population-level telemetry와 정확한 clustering이 먼저라는 사례를 남겼습니다.
    [Source URL](https://openai.com/index/core-dump-epidemiology-data-infrastructure-bug/) (OpenAI)

*   **NAVER D2, 여러 기기에서 동기화되는 AI agent 조직 운영 세션 공개**
    NAVER D2는 Claude Code를 매번 초기 상태로 쓰는 문제에서 출발해, 비서실장과 10개 부서 형태의 agent 조직을 구성한 NaverMadCat 사례를 공개했습니다. 세션은 lifecycle hook, slash command, dashboard, agent의 채용·해고·병합, 여러 환경에서 같은 구성원과 목표를 유지하는 sync 방식을 다룹니다. 개인 prompt 모음보다 지속 가능한 agent 운영 환경을 만들려는 팀이 조직 구조와 상태 동기화 경계를 검토할 때 참고할 수 있습니다.
    [Source URL](https://d2.naver.com/helloworld/3897377) (NAVER D2)

---

오늘의 핵심은 더 강한 모델을 연결하는 것만큼 workflow의 재개 가능성, 독립 평가, token 비용 측정, 장애 data 품질이 중요해졌다는 점입니다. Agent를 production에 넣을수록 모델 교체와 prompt 수정은 일반 software change처럼 baseline, regression test, telemetry를 갖춘 상태에서 진행해야 합니다.
