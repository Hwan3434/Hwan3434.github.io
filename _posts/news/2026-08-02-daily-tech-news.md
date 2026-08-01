---
layout: post
title: "데일리 테크 뉴스 - 2026-08-02"
date: 2026-08-02 06:02:49 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## 오늘의 개발자 뉴스: Astra의 Lean 인증 수학 결과, Google Agent Eval GA, Lean 커널 결함 사후 분석, NetBSD 11.0

2026년 8월 2일 기준으로 OpenAI가 공개한 수학·이론 전산학 결과 10건, Gemini Enterprise Agent Platform의 agent·model 평가 기능 GA, AI 보조로 발견된 Lean 커널 soundness 결함의 사후 분석, RISC-V와 microVM 지원을 확대한 NetBSD 11.0을 정리했습니다. 주가, 실적, 경영진 중심 뉴스는 제외했습니다.

---

### AI for Formal Research

*   **OpenAI, Astra가 만든 수학·이론 전산학 결과 10건과 Lean certificate 공개**
    OpenAI는 최소 10년간 핵심 결과에 진전이 없었다고 설명한 문제 중 고차원 sphere packing, code bound, non-sofic group, arithmetic circuit complexity, quantum parallel repetition, lattice의 closest vector problem 등 10건에 대한 새 결과를 공개했습니다. 수학적 argument는 차기 주요 model인 Astra의 내부 버전이 생성했고, 사람이 같은 model과 함께 manuscript로 정리한 뒤 각 argument를 Lean certificate로 formalize했다는 것이 회사 설명입니다. 탐색에 사용된 전체 token 비용은 Sol API 요율로 약 2,000달러라고 추산했지만 Astra 자체는 공개 API가 아니며, 비용 수치도 재현 가능한 공개 benchmark가 아니라 해당 탐색 run의 환산값입니다. Lean certificate는 type checker가 형식적 정합성을 검사할 수 있게 하지만 결과의 중요성, 기존 문헌과의 관계, formalization에 들어간 statement가 의도한 theorem과 정확히 같은지는 분야 전문가의 검토가 별도로 필요합니다. 연구용 agent를 평가하는 팀에는 최종 답뿐 아니라 machine-checkable artifact, 인간의 편집 범위, model과 compute 비용을 함께 공개하는 사례라는 점이 중요합니다.
    [Source URL](https://openai.com/index/ten-advances-in-mathematics/) (OpenAI)

---

### Agent Evaluation

*   **Google, 개발 실험과 production traffic에 같은 metric을 쓰는 Agent Platform 평가 기능 GA**
    Gemini Enterprise Agent Platform의 agent·model evaluation은 quality, safety, grounding, tool use와 trajectory 등을 다루는 20개 이상의 기본 metric, custom code metric, LLM-as-a-judge metric을 제공합니다. 개발 단계에서는 local·server-side experiment와 case generator, multi-turn user simulator, 실패·지연 응답을 대신 만드는 environment simulator를 사용할 수 있고, 배포 뒤에는 Cloud Trace의 session과 trace를 sampling해 같은 metric으로 continuous evaluation과 drift alert를 실행할 수 있습니다. Server-side artifact는 Cloud Storage에 남아 run을 versioning·감사할 수 있으며, 실패를 팀 taxonomy에 맞춰 묶는 issue clustering도 지원합니다. Local evaluation은 provider에 관계없이 model을 쓸 수 있고 server-side는 Model Garden의 Gemini·Anthropic model을 지원합니다. 다만 model 기반 metric에는 해당 model 호출료와 artifact storage 비용이 들고 LLM judge는 그 자체로 오판할 수 있으므로, deterministic check와 사람이 검수한 calibration set을 함께 유지하는 편이 안전합니다.
    [Source URL](https://developers.googleblog.com/agent-and-model-evaluations-in-gemini-enterprise-agent-platform-are-now-ga/) (Google Developers Blog)

---

### Formal Verification Security

*   **Lean, AI 보조 Collatz ‘반증’이 악용한 커널 soundness 버그를 신고 한 시간 뒤 수정**
    7월 25일 공개된 `sorry` 없는 Collatz conjecture 반증은 실제 증명이 아니라 nested inductive type의 phantom parameter가 생성된 auxiliary type에서 사라져 type checking을 피하는 Lean 커널 버그를 악용한 것이었습니다. 이 경로는 일반 frontend가 잘못된 argument를 막기 때문에 metaprogramming으로 declaration을 커널에 직접 보낼 때만 도달하지만, elaborator는 신뢰 경계 밖에 있으므로 커널이 스스로 거부해야 합니다. 최소 `False` 증명이 7월 28일 issue `#14576`으로 보고된 뒤 한 시간 만에 수정이 올라왔고 patch release와 regression test가 배포됐습니다. 당시 독립 Rust checker인 nanoda도 별개의 projection type-name 검증 버그 때문에 proof를 받아들였지만 그 결함은 Lean 신고 일주일 전에 이미 수정됐습니다. 사후 조치로 관련 parameter 검사를 강화하고 AI 보안 분석이 찾은 추가 programming mistake들을 고쳤으며, `comparator.live`가 최신 nanoda를 기본 실행하도록 바꿨습니다. 독립 checker 전략이 무효라는 뜻은 아니지만, 두 구현을 최신으로 유지하고 같은 reference code를 옮긴 checker가 동일 결함을 공유할 가능성까지 threat model에 넣어야 합니다.
    [Source URL](https://leodemoura.github.io/blog/2026-8-1-postmortem-for-kernel-soundness-bug-14576/) (Leonardo de Moura / Lean FRO)

---

### Operating Systems

*   **NetBSD 11.0, 64-bit RISC-V 정식 지원과 약 10ms 부팅용 x86 MICROVM kernel 추가**
    NetBSD 11.0은 VisionFive 2, PINE64 STAR64와 QEMU를 포함한 64-bit RISC-V를 stable release에서 처음 지원하고, Snapdragon X Elite 초기 지원도 추가했습니다. x86의 새 `MICROVM` kernel은 PVH boot, VirtIO MMIO와 kernel 최적화를 이용해 2020년대 CPU에서 약 10ms 부팅을 목표로 합니다. Linux compatibility layer에는 `epoll`, `statx`, `close_range`, `clone3`, `inotify` 등이 들어갔고 POSIX.1-2024·C23 호환성, NPF의 layer 2·user/group filtering도 확장됐습니다. 업그레이드 시 kernel과 module을 먼저 갱신해 reboot한 뒤 userspace와 third-party package를 올려야 하며, OpenSSH의 DSA key 제거와 `ctype(3)` 오용을 segfault로 드러내는 guard page 등 incompatible change를 확인해야 합니다. 프로젝트는 release 시점에 hdaudio privilege check, IPFilter null dereference, deprecated PF의 use-after-free 등 미해결 pullup 세 건도 공개했으며 stable branch 반영 뒤 약 두 달 내 11.1을 목표로 한다고 밝혔습니다. Internet-facing host는 각 기능의 기본 활성화 여부만 보고 넘기지 말고 workaround와 11.1 반영 상태를 추적해야 합니다.
    [Source URL](https://blog.netbsd.org/tnf/entry/netbsd_11_0_released) (NetBSD Project)

---

오늘의 공통점은 신뢰할 수 있는 결과가 한 번의 성공 판정이 아니라 서로 다른 검증 layer에서 나온다는 점입니다. AI 연구 결과에는 machine-checkable artifact와 전문가 검토가, agent에는 offline·online eval의 일관성이, proof kernel과 OS에는 독립 checker·regression test·공개된 잔여 위험의 추적이 필요합니다.
