---
layout: post
title: "데일리 테크 뉴스 - 2026-08-04"
date: 2026-08-04 06:03:37 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## 오늘의 개발자 뉴스: 대규모 모델 추론 최적화, 허위 CVE, 장기 코딩 벤치마크, Karpathy의 Pelican 실험

2026년 8월 4일 기준으로 Kimi·GLM을 더 적은 GPU memory로 제공하는 Cloudflare의 production 기법, AI가 만든 것으로 보이는 SQLite CVE를 재현 검증한 JFrog의 분석, 전체 program 재구현 능력을 측정하는 MirrorCode, Andrej Karpathy의 장시간 Three.js 생성 실험을 정리했습니다. 주가, 실적, 경영진 중심 뉴스는 제외했습니다.

---

### AI Inference Infrastructure

*   **Cloudflare, KV cache FP8 양자화·INT4 weight 압축·page integrity 검사로 대형 모델 serving 밀도 개선**
    Cloudflare는 Workers AI에서 Kimi K2.6의 KV cache를 BF16에서 FP8(e4m3)로 바꿔 같은 memory에 담는 context를 약 68.6만 token에서 137만 token으로 늘렸습니다. 단일 request의 token 속도는 BF16이 소폭 빠르지만, FP8은 동시 request를 32개에서 64개까지 수용해 측정상 peak throughput을 약 41% 높이고 token당 비용을 약 30% 낮췄습니다. GLM 5.2는 weight를 FP8에서 INT4로 압축해 checkpoint를 705GB에서 421GB로 줄였습니다. 다만 INT4는 weight를 다시 펼치는 비용 때문에 prefill에는 불리해, compute-bound prefill은 FP8로 두고 memory-bound decode만 INT4로 운영합니다. 공유 KV cache에는 page가 재할당될 때 바뀌는 tag를 붙이고 decode 전에 request가 기대한 page·tag mapping을 검사해, 잘못된 page를 읽을 가능성이 있으면 응답 대신 request를 중단합니다. 핵심은 양자화 정밀도 하나가 아니라 prefill/decode 분리와 cache 격리를 함께 설계한 점입니다.
    [Source URL](https://blog.cloudflare.com/smaller-faster-safer-models/) (Cloudflare Blog)

---

### Software Supply Chain Security

*   **JFrog, SQLite Critical CVE 6건이 source·PoC 검증을 통과하지 못한 허위 advisory라고 분석**
    JFrog은 새 GitHub 계정이 제출한 SQLite 취약점 advisory를 대상 version source와 대조하고, 공식 release를 격리된 Docker에서 AddressSanitizer로 build해 공개 PoC를 실행했습니다. 그 결과 존재하지 않는 함수, 실제 file 길이를 넘는 line number, 변경되지 않은 file에 대한 가짜 patch 주장, parser 단계에서 실패하는 SQL 등이 확인됐고 여섯 PoC 모두 주장한 memory bug를 재현하지 못했습니다. 같은 계정의 advisory 55건을 넓게 감사한 결과 54건은 완전히 조작됐고 한 건만 실제 bug를 검증되지 않은 CVE metadata로 감싼 형태였다고 보고했습니다. CI나 보안 agent가 NVD·GHSA severity만 받아 자동 ticket과 patch를 만들면 허위 입력이 실제 engineering 비용과 불필요한 코드 변경으로 이어질 수 있습니다. 새 CVE는 maintainer advisory와 commit을 교차 확인하고, 영향 version을 checkout한 뒤 안전한 환경에서 PoC를 재현하는 단계가 필요합니다.
    [Source URL](https://research.jfrog.com/post/sqlite-critical-cves-or-llm-slops/) (JFrog Security Research)

---

### Agent Evaluation

*   **Epoch AI와 METR, source 없이 전체 program을 재구현하는 장기 코딩 benchmark MirrorCode 공개**
    MirrorCode는 bug fix나 단일 feature 대신 Unix utility, serialization·query tool, bioinformatics, interpreter, static analysis, cryptography, compression 등 25개 program을 입출력 behavior만 보고 처음부터 다시 구현하게 합니다. agent는 internet과 원본 source에 접근할 수 없는 sandbox에서 작업하고, 보지 못한 end-to-end test까지 정확히 통과해야 합니다. 가장 큰 한 번의 run은 19일 동안 사람 개입 없이 진행돼 $2,600이 들었으며, Claude Opus 4.7은 40개가 넘는 command와 약 1.6만 줄 규모의 Go bioinformatics tool `gotree`를 14시간·$251에 거의 재현했습니다. 다만 2,001개 test 중 niche date-annotation edge case 하나를 실패해 엄격한 의미에서는 완전 해결이 아니고, open-source target이 pretraining에 포함됐을 가능성도 남습니다. 팀은 scaffold와 25개 중 22개 target을 공개했으므로, 모델 순위보다 long-horizon agent의 test discipline·budget·failure mode를 재현하는 기반으로 보는 편이 유용합니다.
    [Source URL](https://epoch.ai/MirrorCode) (Epoch AI / METR)

---

### Generative Coding Experiments

*   **Andrej Karpathy, 100만 token budget으로 문학 한 단락을 5,500줄 Three.js 장면으로 확장한 Pelican 실험 공유**
    Karpathy는 단순한 “자전거를 탄 펠리컨 SVG”류 prompt를 넘어 장시간 코딩 agent를 시험하기 위해, 소설 첫 단락과 100만 token budget(약 $10)을 Claude Opus 5에 주고 Three.js render를 요청했습니다. 모델은 약 2시간 동안 실행되며 polygon asset을 좌표에 배치하고 animation을 조율하는 코드 약 5,500줄을 만들었습니다. 결과를 본인도 다듬어지지 않은 실험으로 표현했으므로 정확성이나 생산성을 입증하는 benchmark로 읽을 수는 없습니다. 대신 짧은 코드 생성에서 벗어난 agent 작업은 결과 화면만 평가하기보다 장시간 실행 trace, asset provenance, browser 성능, 유지보수 가능한 scene abstraction, 예산 상한을 함께 검토해야 한다는 실용적인 test case입니다.
    [Source URL](https://twitter.com/karpathy/status/2083749667410727319) (Andrej Karpathy)

---

오늘의 공통점은 긴 실행과 자동화가 입력 검증의 중요성을 더 키운다는 점입니다. 추론 server는 cache page를 확인하고, 보안 pipeline은 CVE를 재현하며, coding agent 평가는 hidden test와 오염 가능성을 구분해야 합니다.
