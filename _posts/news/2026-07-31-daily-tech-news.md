---
layout: post
title: "데일리 테크 뉴스 - 2026-07-31"
date: 2026-07-31 06:00:54 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## 오늘의 개발자 뉴스: GPT-5.6 가격 조정, Gemini Robotics 2, GitHub Stacked PR, Agent 코드 리팩터링 비용

2026년 7월 31일 기준으로 GPT-5.6 API의 새 가격·처리 모드, Gemini Robotics 2의 embodied reasoning 개발자 프리뷰, GitHub의 stacked pull request 공개 프리뷰, agent가 작성한 코드에서 리팩터링이 이후 작업의 token 비용에 미치는 실험 결과를 정리했습니다. 주가, 실적, 경영진 중심 뉴스는 제외했습니다.

---

### AI API

*   **OpenAI, GPT-5.6 Luna·Terra 가격을 낮추고 Sol용 Fast mode 도입**
    OpenAI는 7월 30일부터 GPT-5.6 Luna의 API 가격을 input 100만 token당 0.20달러, output 100만 token당 1.20달러로, Terra는 각각 2달러와 12달러로 조정했습니다. 회사 설명 기준으로 기존보다 Luna는 80%, Terra는 20% 낮아진 가격입니다. GPT-5.6 Sol에는 Standard 대비 최대 2.5배 빠른 대신 가격이 두 배인 Fast mode가 추가되며, 기존 Priority Processing 요청은 별도 변경 없이 Fast mode로 연결됩니다. Codex와 ChatGPT Work의 구독 가격·quota budget 자체는 유지되지만 Terra와 Luna의 credit 소비량은 줄어듭니다. 개발팀은 단일 모델을 기본값으로 고정하기보다, 계획·불확실성 해소에는 Sol을 쓰고 명세가 분명한 구현·테스트에는 Luna를 쓰는 식으로 단계별 품질과 비용을 eval해야 합니다. 가격 인하율과 속도는 공급자 발표치이며 workload별 실제 latency와 성공률은 별도 검증이 필요합니다.
    [Source URL](https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/) (OpenAI)

---

### Physical AI

*   **Google DeepMind, whole-body 제어와 multi-robot 협업을 지원하는 Gemini Robotics 2 공개**
    Gemini Robotics 2는 시각·언어 입력을 motor control로 바꾸는 VLA 모델, 여러 분 동안 이어지는 작업을 계획하는 `Gemini Robotics ER 2`, 로봇 장치에서 로컬 실행되는 `Gemini Robotics On-Device 2`로 구성됩니다. ER 2는 Google AI Studio에서 사용할 수 있고 Gemini Enterprise Agent Platform에서는 private preview이며, VLA와 On-Device 모델은 early-access partner에게 제공됩니다. On-Device 2는 일반적으로 200개 미만의 example과 몇 시간의 data로 새로운 bi-arm embodiment에 적응할 수 있다는 것이 회사 설명입니다. 새 `ASIMOV-Agentic` benchmark는 위험한 VLA tool call 거부, 작업 가능성 판단, 불확실할 때 사람에게 개입을 요청하는 능력을 평가합니다. 다만 공개 자료에서도 multi-finger 조작은 여전히 어렵다고 밝히며, 전체 VLA checkpoint가 일반 API로 공개된 것은 아니므로 현재 일반 개발자가 직접 시험할 수 있는 범위는 ER 2 중심입니다.
    [Source URL](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/) (Google DeepMind)

---

### Developer Workflow

*   **GitHub, 의존 관계가 있는 작은 변경을 한 번에 관리하는 stacked pull request 공개 프리뷰 시작**
    GitHub의 stacked pull request는 큰 변경을 순서가 있는 여러 PR로 나누고, 각 PR이 바로 아래 layer를 target하도록 구성합니다. Reviewer는 layer별 diff와 stack map을 보며 독립적으로 검토할 수 있고, 준비된 최상위 PR을 merge하면 아직 합쳐지지 않은 하위 layer까지 한 번에 반영할 수 있습니다. stack 일부만 merge하면 위쪽 PR은 열린 상태로 자동 rebase·retarget되며, 기존 branch protection, required check, review requirement는 그대로 적용됩니다. `gh extension install github/gh-stack`으로 CLI extension을 설치할 수 있고 웹, GitHub Mobile, `gh-stack` skill을 사용하는 coding agent에서도 stack을 만들 수 있습니다. 모든 repository에 며칠에 걸쳐 공개 프리뷰가 배포되며 merge queue 지원은 이후 수 주 동안 순차 적용되므로, CI automation은 rollout 상태와 자동 retarget 뒤의 base branch를 확인해야 합니다.
    [Source URL](https://github.blog/changelog/2026-07-30-stacked-pull-requests-are-now-in-public-preview/) (GitHub)

---

### Agentic Engineering

*   **MartinFowler.com 실험, 구조적 리팩터링 후 같은 agent 작업의 input token이 83% 감소**
    Giles Edwards-Alexander는 agent가 작성한 약 15만 줄 규모 application에서 17,155줄짜리 Rust data-access file을 단계적으로 리팩터링하고, 매 단계마다 fresh sub-agent에게 동일한 변경을 수행시켰습니다. 가장 큰 file이 3,695줄로 줄어든 마지막 단계에서 같은 작업의 추정 input token은 159,564개에서 27,360개로 83% 감소했고, output token은 큰 변화가 없었습니다. 전체 data-access layer의 코드량은 거의 그대로였으므로 효과는 단순한 줄 수 삭제보다 agent가 읽어야 할 관련 범위를 작은 file 집합으로 식별할 수 있게 된 데서 나왔다는 해석입니다. 반대로 중간 단계에서는 token이 오르기도 했고, live token 계측 대신 문자 수를 4로 나눈 추정치를 사용했으며, 단일 codebase와 대표 작업 한 건의 결과입니다. 따라서 “file을 작게 쪼개면 항상 절약된다”는 결론보다, 명확한 module boundary가 agent의 context 탐색 비용을 줄일 수 있다는 실험적 신호로 보는 편이 안전합니다.
    [Source URL](https://martinfowler.com/articles/exploring-gen-ai/refactoring-economic-benefit.html) (Giles Edwards-Alexander / MartinFowler.com)

---

오늘의 공통점은 AI 개발 비용이 model 가격만으로 결정되지 않는다는 점입니다. Workflow 단계에 맞는 model과 처리 모드를 고르고, agent가 읽을 code boundary를 선명하게 만들며, 큰 변경은 검토 가능한 PR layer로 나누는 운영 설계가 token 비용과 review 병목을 함께 줄입니다.
