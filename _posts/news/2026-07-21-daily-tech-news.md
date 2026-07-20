---
layout: post
title: "데일리 테크 뉴스 - 2026-07-21"
date: 2026-07-21 06:02:36 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## 오늘의 개발자 뉴스: WordPress 긴급 패치, Codex 컨텍스트 변경, 로봇 기반 모델, Headless 게임 스트리밍

2026년 7월 21일 기준으로 즉시 대응이 필요한 WordPress Core 취약점, AI coding agent의 context budget 변경, 대규모 manipulation data로 학습한 robot foundation model, 격리된 Linux game-streaming session을 정리했습니다. 주가, 실적, 경영진 중심 뉴스는 제외했습니다.

---

### Web Security와 AI-assisted 취약점 연구

*   **WordPress Core의 pre-auth RCE `wp2shell`이 실제 공격에 사용되기 시작해 즉시 업데이트 필요**
    `CVE-2026-63030`과 `CVE-2026-60137`을 연결하면 인증되지 않은 공격자가 REST API batch route의 validation·execution index 불일치를 이용해 parameter validation을 우회하고, `WP_Query`의 SQL injection을 거쳐 remote code execution에 도달할 수 있습니다. 연구자는 GPT-5.6 Sol Ultra에 4개 agent와 최소 6시간의 source audit를 지시해 초기 SQLi와 복잡한 privilege-escalation chain을 찾았고, 사람이 stock installation에서 재현한 뒤 책임 있게 보고했습니다. WordPress는 7.0.2, 6.9.5, 6.8.6에 수정 사항을 배포하고 영향 버전에 forced auto-update를 활성화했습니다. Wiz는 7월 20일 vulnerable cloud instance에서 webshell 설치를 포함한 실제 악용을 관찰했으므로, 운영자는 자동 업데이트 여부를 확인하고 즉시 patched release로 올려야 합니다.
    [Source URL](https://slcyber.io/research-center/exploit-brokers-pay-500000-for-a-wordpress-rce-i-found-one-with-gpt5-6/) (Searchlight Cyber)
    [Source URL](https://wordpress.org/news/2026/07/wordpress-7-0-2-release/) (WordPress.org)
    [Source URL](https://www.wiz.io/blog/wp2shell-cve-2026-63030-cve-2026-60137) (Wiz Research)

---

### AI Coding Agent의 Context Budget

*   **Codex 0.144 backport, bundled model metadata에서 GPT-5.6 Sol context window를 372K에서 272K로 축소**
    OpenAI의 `codex` repository에 merge된 pull request #33972는 release/0.144 branch의 bundled `models.json`을 갱신하면서 GPT-5.6 Sol의 `context_window`와 `max_context_window` 값을 372,000에서 272,000 token으로 변경했습니다. 이는 공개 repository에서 확인되는 해당 CLI release metadata 변경이며 API model 전체의 사양 변경으로 일반화할 수는 없습니다. 긴 작업에서 많은 파일과 tool output을 한 context에 유지하던 사용자는 자동 compaction이 더 일찍 일어날 수 있다고 보고, task 분할과 concise context 관리가 필요한지 점검할 만합니다.
    [Source URL](https://github.com/openai/codex/pull/33972/files) (OpenAI Codex / GitHub)

---

### Robot Foundation Model

*   **Xiaomi-Robotics-1, 10만 시간 이상의 embodiment-free manipulation trajectory로 robot policy scaling 시도**
    Xiaomi Robotics는 1,700개 이상의 scenario에서 수집한 UMI trajectory 10만 시간을 VLM으로 자동 annotation해 pre-training하고, 7,200시간 이상의 in-house real-robot data 등을 이용해 embodiment와 instruction을 post-training한 Vision-Language-Action model을 공개했습니다. 공식 결과에 따르면 새로운 작업마다 평균 10시간 미만의 demonstration으로 75% overall success rate를 기록해 비교 대상인 `π 0.5`의 40%를 앞섰고, 네 개 simulation benchmark에서도 최고 결과를 냈습니다. 핵심은 특정 robot에서 비싼 데이터를 대량 수집하는 대신 embodiment-free data로 넓게 학습한 뒤 실제 hardware에 정렬하는 data pipeline이며, code와 model weight도 함께 공개됐습니다. 다만 성능 수치는 연구팀 평가이므로 독립적인 재현이 필요합니다.
    [Source URL](https://robotics.xiaomi.com/xiaomi-robotics-1.html) (Xiaomi Robotics)

---

### Linux와 Remote Rendering

*   **Moonshine, desktop과 분리된 compositor에서 실행되는 Rust 기반 headless Moonlight server 제공**
    Moonshine은 각 stream을 별도 Wayland compositor에서 실행해 host desktop을 계속 사용할 수 있게 하고, monitor나 HDMI dummy plug 없이 Moonlight client로 game을 전송하는 open-source Linux server입니다. Vulkan video encoding으로 H.264, H.265, 실험적 AV1을 지원하고, 10-bit HDR, Opus audio, keyboard·mouse·gamepad 입력도 처리합니다. NVIDIA RTX, AMD RDNA2+, Intel Arc 계열 GPU와 systemd가 필요하며 현재 Arch Linux에서 주로 검증됐습니다. GameStream traffic이 application level에서 완전히 암호화되지 않으므로 port를 인터넷에 직접 노출하지 말고 WireGuard나 Tailscale 같은 VPN 뒤에서 사용해야 한다는 제한도 명확합니다.
    [Source URL](https://github.com/hgaiser/moonshine) (Moonshine / GitHub)

---

오늘의 공통점은 AI와 system software의 성능보다 경계 조건을 먼저 확인해야 한다는 것입니다. AI가 찾은 취약점도 human reproduction과 patch 배포가 필요하고, coding agent의 context 값은 특정 client metadata 범위를 구분해야 하며, robot benchmark는 독립 검증이 남아 있습니다. 공개된 수치와 demo를 출발점으로 삼되 version, threat model, evaluation boundary를 함께 읽는 습관이 중요합니다.
