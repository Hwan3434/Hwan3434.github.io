---
layout: post
title: "데일리 테크 뉴스 - 2026-08-03"
date: 2026-08-03 06:01:32 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## 오늘의 개발자 뉴스: Genkit Agent Skills, Go 1.27 미리보기, Rust All Hands, Linux의 Darwin CLI 호환 계층

2026년 8월 3일 기준으로 Genkit의 on-demand Agent Skills, 곧 나올 Go 1.27의 주요 언어·런타임 변화, Rust 프로젝트가 공유한 All Hands 기술 논의, Linux ARM64에서 macOS ARM64 CLI binary를 실행하는 실험적 Kakehashi를 정리했습니다. 주가, 실적, 경영진 중심 뉴스는 제외했습니다.

---

### Agent Development

*   **Google, Genkit 전 언어 SDK에 progressive-disclosure 방식 Agent Skills 지원 추가**
    Genkit은 TypeScript, Go, Dart, Python에서 Agent Skills 표준을 지원합니다. `SKILL.md`의 description 등 metadata만 처음 system prompt에 노출하고, 요청이 맞을 때 `use_skill` tool로 본문과 `scripts`, `references`, `assets`를 불러오는 방식이라 모든 절차서를 상시 context에 넣는 비용과 집중도 저하를 줄입니다. Go 구현은 middleware의 `WrapModel`, `WrapTool`, `WrapGenerate` hook 위에서 동작하며 `ai.WithUse(&middleware.Skills{SkillPaths: []string{"./skills"}})`로 flow에 연결합니다. 배포 관점에서는 skill이 실행 파일을 포함할 수 있다는 점이 중요합니다. 신뢰하지 않는 bundle을 단순 prompt 자료로 취급하지 말고 code dependency처럼 review·version pinning·sandbox 정책을 적용해야 합니다.
    [Source URL](https://developers.googleblog.com/enable-on-demand-expertise-with-agent-skills-in-genkit-go/) (Google Developers Blog)

---

### Programming Languages

*   **Go 1.27 사전 tour, generic method와 표준 UUID·ML-DSA, 기본 JSON v2 구현을 예제로 점검**
    VictoriaMetrics가 공식 release note와 Go source를 바탕으로 아직 출시 전인 Go 1.27의 변화를 실행 가능한 예제로 정리했습니다. method가 receiver와 독립적인 type parameter를 선언할 수 있지만 interface에는 type-parameterized method를 둘 수 없고, generic method로 interface를 구현할 수도 없습니다. runtime은 80 byte 미만 일부 allocation 비용을 최대 30% 줄이며 실제 allocation-heavy program의 전체 개선은 약 1%로 예상됩니다. `goroutineleak` profile은 experiment flag 없이 사용할 수 있고, 표준 라이브러리에는 RFC 9562 UUID와 FIPS 204 ML-DSA가 들어갑니다. `encoding/json/v2`도 experiment에서 벗어나며 기존 `encoding/json`은 v2 구현을 내부에서 사용하되 호환 문제가 있으면 `GOEXPERIMENT=nojsonv2`로 되돌릴 수 있습니다. 정식 release 전 내용이므로 최종 release note와 migration test를 기준으로 채택해야 합니다.
    [Source URL](https://victoriametrics.com/blog/go-1-27/index.html) (VictoriaMetrics)

---

### Rust Ecosystem

*   **Rust All Hands, const 기능·in-place initialization·`rustc` library화와 C++ interop의 blocker 논의**
    Rust 프로젝트는 5월 Utrecht에서 166명이 진행한 3일간 73개 session의 회고와 session note를 공개했습니다. 언어·compiler 쪽에서는 const generics와 const traits, field projection과 reborrowing, in-place initialization, SIMD, allocator, custom lint, library stability attribute, `rustc` as a library, Sized hierarchy와 auto trait이 다뤄졌습니다. interop에서는 Rust/C++ 전체 문제 공간, Crubit, LLVM IR과 Rust MIR을 결합한 더 안전한 접근을 논의했고 Rust for Linux와 Rust for CPython 팀도 통합 blocker를 함께 풀었습니다. `cargo-semver-checks`는 올바른 feature로 rustdoc JSON을 만들어 cross-crate analysis를 여는 경로와 standard library PR에서의 실행 방향을 정리했습니다. 다만 All Hands는 최종 결정을 내리는 자리가 아니므로 이 목록을 확정 roadmap으로 읽기보다 후속 RFC와 project goal을 추적해야 합니다.
    [Source URL](https://blog.rust-lang.org/inside-rust/2026/07/31/all-hands-2026-retrospective/) (Inside Rust Blog)

---

### Compatibility Layers

*   **Kakehashi, JIT 없이 Linux aarch64에서 Darwin Mach-O CLI를 실행하는 초기 userspace 계층 공개**
    Rust로 작성된 Kakehashi는 Linux aarch64에서 macOS ARM64 Mach-O를 load하고 freestanding `libSystem`을 map한 뒤 BSD syscall을 번역해 guest code를 CPU에서 native로 실행합니다. 현재 Docker·Colima와 UTM에서 clang probe, multi-thread 7-Zip, HTTP·HTTPS curl, thread 동작을 검증했고 `cargo install kakehashi`로 설치할 수 있습니다. 목표는 GUI나 완전한 macOS 호환이 아니라 비싼 macOS CI runner 대신 순수 Darwin CLI tool을 Linux ARM64 runner에서 돌리는 것입니다. 약 8천 file을 압축한 공개 측정에서는 syscall boundary 비용으로 native Linux 대비 약 5.2배 느렸습니다. POST·proxy·HTTP/3 전체, Apple framework, `git`, codesign, notarization, GUI는 아직 지원 claim에 포함되지 않으므로 production CI에 넣기 전 필요한 syscall·framework와 licensing 조건을 별도로 검증해야 합니다.
    [Source URL](https://github.com/wie-project/kakehashi) (Kakehashi / GitHub)

---

오늘의 공통점은 더 많은 기능을 한꺼번에 제공하기보다 경계를 명시하는 설계입니다. Agent skill은 필요한 context만 열고, Go와 Rust는 새 기능의 호환 조건과 결정 단계를 드러내며, Kakehashi는 지원하는 CLI surface와 아직 지원하지 않는 macOS 기능을 분리합니다.
