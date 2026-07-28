---
layout: post
title: "데일리 테크 뉴스 - 2026-07-29"
date: 2026-07-29 06:01:57 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## 오늘의 개발자 뉴스: Claude 암호분석, 과학 소프트웨어와 Coding Agent, Zig 증분 컴파일, Orchestrator의 Context 비용

2026년 7월 29일 기준으로 Claude Mythos Preview가 찾아낸 HAWK·축소형 AES 공격, coding agent를 과학 소프트웨어 유지보수에 적용한 8개 사례, Zig compiler의 함수 단위 증분 빌드 구조, multi-agent workflow에서 orchestrator의 working memory를 보호하는 방법을 정리했습니다. 주가, 실적, 경영진 중심 뉴스는 제외했습니다.

---

### AI와 암호분석

*   **Claude Mythos Preview, HAWK와 7-round AES의 기존 최선 공격 개선**
    Anthropic은 Claude Mythos Preview가 NIST post-quantum signature 후보 HAWK의 lattice에서 기존에 활용되지 않은 automorphism을 찾아 더 빠른 key-recovery attack을 구성했다고 발표했습니다. 회사가 제시한 HAWK-256 예시에서 예상 공격 비용은 `2^64`에서 `2^38`로 낮아졌으며, 60시간가량의 agent 작업과 약 10만 달러의 API 비용이 들었습니다. 별도의 autonomous scaffold는 AES-128의 10 round 전체가 아닌 7-round 변형에서 Möbius Bridge라는 fingerprinting 기법을 찾아 기존 meet-in-the-middle attack을 200~800배 개선했습니다. 두 결과 모두 현재 production system에는 직접 영향이 없습니다. HAWK는 아직 후보이고, AES 결과는 막대한 chosen plaintext를 요구하는 축소형 cipher 대상입니다. 특히 AES 아이디어는 model이 약 1주 만에 찾았지만 두 연구자가 정확성을 확신하는 데 거의 한 달과 수백 시간이 필요했습니다. AI security research에서도 생성 비용보다 독립 검증, responsible disclosure, 재현 가능한 proof가 병목이 된다는 사례입니다.
    [Source URL](https://www.anthropic.com/research/discovering-cryptographic-weaknesses) (Anthropic)

---

### Agentic Scientific Computing

*   **OpenAI 현장 보고서, 과학 소프트웨어 8개 project에서 구현보다 검증과 stewardship이 새 병목**
    OpenAI는 genomics를 중심으로 한 8개 agent-assisted scientific computing 사례를 공개했습니다. 5개는 Codex만, 3개는 Codex와 Claude Code를 함께 사용했으며, legacy packaging 교체부터 성능 최적화, language migration, GPU-native redesign까지 범위가 다양합니다. 참여 팀은 agent가 작은 팀의 구현·유지보수 속도를 높였다고 보고했지만, scientific validity를 스스로 안정적으로 판단하지 못하고 명확한 오류에도 자신감을 보이는 문제가 반복됐습니다. 효과적인 workflow는 기존 tool과의 exact output parity, simulated data의 정답, 통계적 동작, benchmark 같은 외부 acceptance target을 두고 작업을 작은 단계로 나눴습니다. 초기 구현보다 edge case와 수치 차이를 해결하는 마지막 구간이 더 오래 걸렸고, 별도 rewrite가 난립하면 maintainer의 관심과 사용자 기반이 분산될 수 있습니다. 이는 8개 팀의 회고를 모은 exploratory report이지 통제 실험은 아니므로 생산성 수치를 일반화하기보다 upstream 조율, 검증 기준, 장기 owner를 먼저 정하는 근거로 읽어야 합니다.
    [Source URL](https://openai.com/index/scientific-computing-agentic-ai/) (OpenAI)

---

### Compiler Engineering

*   **Zig, source hash·dependency graph·통합 linker로 함수 단위 증분 컴파일 구현**
    Zig core team의 Matthew Lugg는 compiler가 변경된 declaration과 function만 다시 분석하고 결과 machine code를 기존 binary에 직접 덮어쓰는 증분 컴파일 내부 구조를 설명했습니다. Source file별 ZIR cache와 declaration 영역 hash가 최초 변경점을 찾고, type·value·layout·function body를 analysis unit으로 나눈 dependency graph가 재분석 범위를 전파합니다. AIR-to-MIR code generation은 function 단위로 다시 실행하며, compiler와 밀접하게 통합된 linker가 새 code를 기존 allocation에 쓰거나 공간이 부족할 때만 다른 위치로 옮깁니다. Fizzy pixel editor 시연에서는 초기 build 약 5초 뒤 update가 50~70ms였고 한 profile에서는 전체 update가 37ms, 그중 semantic analysis·codegen·linking이 약 1.6ms였습니다. 현재는 `zig build --watch -fincremental`로 사용할 수 있지만 Zig 0.16.0에는 필요한 linker 기능 일부가 없어 `master`가 필요하며, 작성자는 false-positive error와 miscompilation 가능성을 포함해 아직 안정 기능이 아니라고 경고합니다. 성능 수치는 한 project의 warm incremental workload이므로 자체 codebase에서 correctness test와 rebuild latency를 함께 측정해야 합니다.
    [Source URL](https://mlugg.co.uk/posts/incremental-compilation-internals/) (Matthew Lugg / Zig Core Team)

---

### Multi-Agent Engineering

*   **The Orchestrator's Tax, subagent의 핵심 가치를 병렬성보다 context 격리로 재정의**
    Thoughtworks의 Rahul Garg는 네 subagent가 병렬로 .NET refactoring을 수행한 실제 session을 분석해, worker 수보다 orchestrator가 무엇을 main context에 가져오는지가 장기 작업 품질을 좌우한다고 주장했습니다. 가벼운 status 확인 과정에서 worker의 raw JSONL transcript 수만 token이 두 차례 main thread로 들어왔고, 이 정보는 이후 모든 turn에서 attention을 계속 차지했습니다. 제안된 원칙은 같은 mental model이 필요한 일을 함께 묶는 `cognitive locality`, full transcript 대신 필요한 결과만 반환하는 격리, concurrent writer가 있을 때 repository-wide `git stash` 같은 동작 금지, 겹치는 file ownership을 agent 추가가 아닌 작업 통합 신호로 보는 것입니다. 글의 2~4개 agent 권고와 5개 이상일 때 재검토한다는 threshold는 Claude Sonnet 5와 한 workflow에서 얻은 heuristic이며 보편적 수치가 아닙니다. 실제로 계측된 것은 transcript 유입과 wall-clock time뿐이고 그것이 최대 비용이라는 평가는 orchestrator의 self-critique이므로, 팀은 context 유입량·중복 탐색·handoff 품질을 직접 계측해 규칙을 조정해야 합니다.
    [Source URL](https://martinfowler.com/articles/orchestrator-tax.html) (Rahul Garg / MartinFowler.com)

---

오늘의 공통점은 AI나 compiler가 빠르게 후보 결과를 만들수록 검증 가능한 경계가 더 중요해진다는 점입니다. 암호분석과 과학 software는 외부 proof와 장기 owner가, 증분 compiler는 correctness test가, multi-agent workflow는 main context로 돌아오는 정보의 품질이 실제 생산성을 결정합니다.
