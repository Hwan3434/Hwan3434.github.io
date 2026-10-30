---
layout: post
title: "Anthropic Scion 소스 컨트롤, App Review 가이드라인 개정, iPhone Duo (2026. 10. 31)"
description: "Anthropic이 git을 대체한 Scion을 공개하고, Apple은 심사 가이드라인을 개정하며 iPhone Duo 스크린샷 요건을 예고했습니다."
date: 2026-10-31 08:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
---

## 오늘의 흐름: 에이전트 규모의 소스 컨트롤, 연구 현장의 Claude, Apple 심사 규정 변화

-   Anthropic, git 대신 자체 VCS Scion 도입
-   Claude로 제약 문서 검토 25시간→3시간 (vendor 측정)
-   App Review Guidelines 개정, 2.5.19 신설
-   iPhone Duo용 스크린샷, 2027년 4월부터 필수
-   Swift 생태계: Vapor 5 beta, SE-0554 리뷰

---

### Agent Infrastructure

*   **Anthropic이 모노레포를 git에서 자체 VCS Scion으로 옮김 — 에이전트 규모의 머지가 병목이었음**
    -   하루 머지가 2026년 5월 약 2,500건에서 9월 3만 건 이상으로 늘었고, CI 체크아웃은 하루 약 2,500만 건입니다.
    -   서버가 history·blame·rebase를 처리하는 3단 캐시 구조로 바꿔 CPU와 메모리를 기존 git 미러 대비 약 200배 줄였습니다 (vendor 측정).
    [Source URL](https://www.anthropic.com/research/redesigning-source-control) (Anthropic)
    > 시사점: 일반 팀에는 필요 없는 규모의 해법이지만, 에이전트가 CI 체크아웃을 늘리면 shallow·sparse clone 한계가 먼저 드러나는지 지켜보세요.

*   **Anthropic이 신약 개발 현장의 Claude 활용 사례를 공개 — 문서 검토와 설계 제안이 중심**
    -   Enveda는 1,061쪽 제조 문서에서 사람이 찾은 11건을 모두 잡고 7건을 더 찾아, 검토 시간이 25시간 이상에서 3시간 미만으로 줄었습니다 (vendor 측정).
    -   대부분 전임상 단계이며 임상시험에서의 역할은 아직 정해지지 않았습니다.
    [Source URL](https://www.anthropic.com/research/early-progress-drug-development) (Anthropic)
    > 시사점: 당장 조치는 불필요합니다.

---

### App Store Policy

*   **Apple이 App Review Guidelines를 개정 — 숨은 기능 조항이 2.5.19로 이동하고 AI 생성 이미지 규정이 명시됨**
    -   2.5.19는 숨겨졌거나 문서화되지 않은 기능을 다루며, 바꿔치기 앱은 삭제되고 개발자 프로그램에서도 제외될 수 있습니다.
    -   1.2는 AI 생성물을 포함한 비동의 성적 이미지를 콘텐츠 모더레이션 대상으로 명시하고, 3.1.1(a)는 Music Streaming Services entitlement를 StoreKit External Purchase Link Entitlement로 합쳤습니다.
    [Source URL](https://developer.apple.com/news/) (Apple Developer News)
    > 시사점: 원격 설정으로 켜지는 기능이나 문서에 없는 디버그 코드가 앱에 남아 있는지 제출 전에 점검하세요.

*   **iPhone Duo가 10월 23일 출시 — 스크린샷은 2027년 4월 제출분부터 필수**
    -   iOS 27.1에서 동작하며 Xcode 27.1이 개발을 지원하고, Device Hub로 자세와 방향별 동작을 미리 볼 수 있습니다.
    [Source URL](https://developer.apple.com/news/) (Apple Developer News)
    > 시사점: 레이아웃이 자세 변화에 대응하는지 Xcode 27.1 Device Hub로 확인해 두세요.

---

### Swift Ecosystem

*   **Swift 6.4 이후 생태계 정리 — Vapor 5 beta와 SE-0554 리뷰가 눈에 띔**
    -   Vapor 5 beta는 `EventLoopFuture`를 없애고 structured concurrency로 전부 다시 썼습니다.
    -   SE-0554는 `#if deploymentTargetAtLeast(...)`로 최소 배포 타깃에 따라 import와 선언을 고르는 안으로, 현재 리뷰 중입니다.
    [Source URL](https://www.swift.org/blog/) (Swift.org)
    > 시사점: Swift 서버 코드를 쓴다면 Vapor 4에서 5로 넘어갈 때 async 전환 범위를 미리 가늠해 보세요.

---

다섯 항목 모두 규모나 규정이 바뀔 때 기존 도구와 관행이 먼저 한계를 드러낸다는 점을 보여 줍니다.
