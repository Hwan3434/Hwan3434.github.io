---
layout: post
title: "데일리 테크 뉴스 - 2026-07-04"
date: 2026-07-04 06:02:56 +0900
categories: [news]
tags: [Developer, AI, Daily]
---

## 오늘의 개발자 뉴스: 브라우저 에이전트, Copilot 운영 경계, AI 보안과 데이터 무결성

2026년 7월 4일 기준으로 개발자에게 직접 영향이 있는 browser automation, AI coding 운영 정책, jailbreak 평가, context 비용 실험과 database 검증 소식을 정리했습니다. 주가, 실적, 경영진 중심 뉴스는 제외했습니다.

---

### 브라우저와 AI 개발 도구

*   **WebKit, Safari MCP server를 Technology Preview에 공개**
    Safari Technology Preview 247에는 MCP-compatible coding agent가 Safari window에 직접 연결되는 Safari MCP server가 추가됐습니다. Agent는 DOM과 console log, network request, screenshot을 읽고 JavaScript 실행, viewport 변경, click·type 같은 interaction도 수행할 수 있어 Safari compatibility, performance와 accessibility 검사를 자동화할 수 있습니다. Server 자체는 local에서만 실행되고 별도 network call을 하지 않지만, 수집한 page content와 screenshot은 연결한 agent로 전달됩니다. 현재 stable Safari가 아닌 Technology Preview 기능이므로 CI의 유일한 browser test로 대체하기보다 기존 test suite의 Safari 진단 경로로 평가하는 편이 적절합니다.
    [Source URL](https://webkit.org/blog/18136/introducing-the-safari-mcp-server-for-web-developers/) (WebKit)
    [Source URL](https://news.ycombinator.com/item?id=48769639) (Hacker News)

*   **GitHub Copilot, Gemini 2.5 Pro와 Gemini 3 Flash를 7월 31일 종료**
    GitHub은 Copilot Chat, inline edit, ask·agent mode와 code completion을 포함한 모든 Copilot 경험에서 두 model을 7월 31일 deprecate합니다. 권장 대체 model은 각각 Gemini 3.1 Pro와 Gemini 3.5 Flash이며, Copilot Enterprise에서는 관리자가 새 model policy를 먼저 켜야 할 수 있습니다. Model name을 고정한 workflow와 integration은 종료 전에 대체 model의 output 형식, tool call과 latency를 다시 검증해야 합니다.
    [Source URL](https://github.blog/changelog/2026-07-02-upcoming-deprecation-of-gemini-2-5-pro-and-gemini-3-flash/) (GitHub Changelog)

*   **Copilot CLI의 Actions 인증 단순화와 agent session 감사 기능 확대**
    GitHub Actions에서 Copilot CLI는 장기 PAT 대신 built-in `GITHUB_TOKEN`과 `copilot-requests: write` permission으로 실행할 수 있게 됐습니다. Organization policy를 활성화하면 사용한 AI credit은 organization에 직접 청구되며 user budget은 적용되지 않으므로 cost center나 session limit을 별도로 설정해야 합니다. Enterprise Managed Users를 쓰는 GitHub Enterprise Cloud에는 Copilot client의 prompt, response와 tool call을 SIEM으로 stream하거나 최근 48시간 기록을 REST API로 가져오는 public preview도 추가됐습니다. 자동화 secret은 줄지만 비용과 민감한 session data 보존 정책은 함께 설계해야 합니다.
    [Source URL](https://github.blog/changelog/2026-07-02-copilot-cli-no-longer-needs-a-personal-access-token-in-github-actions/) (GitHub Changelog)
    [Source URL](https://github.blog/changelog/2026-07-02-copilot-agent-session-streaming-is-now-in-public-preview/) (GitHub Changelog)

---

### AI 보안과 context engineering

*   **Anthropic, cyber jailbreak 심각도를 CJS-0부터 CJS-4로 분류하는 초안 공개**
    Anthropic의 Cyber Jailbreak Severity framework는 jailbreak가 공격자에게 추가하는 capability gain, 적용 범위, weaponization 난이도와 discoverability를 합산해 Informational부터 Critical까지 분류합니다. 이미 공개된 scanner가 같은 결과를 내면 capability gain을 0으로 두는 등 model output 자체보다 기존 도구 대비 실제 공격 능력의 증가를 기준으로 삼습니다. 함께 공개한 Fable 5 classifier 정책은 prohibited, high-risk dual use, low-risk dual use와 benign use를 구분하고, 잠재적 false positive를 감수하는 safety margin을 명시합니다. 현재는 초기 초안이며 발견 사례는 새 HackerOne program으로 접수합니다.
    [Source URL](https://www.anthropic.com/news/fable-safeguards-jailbreak-framework) (Anthropic)

*   **pxpipe, 긴 coding-agent context를 PNG로 바꾸는 비용 절감 실험 공개**
    Hacker News에서 주목받은 open-source `pxpipe`는 system prompt, tool documentation과 오래된 history처럼 token-dense한 입력을 local proxy에서 PNG로 바꿔 vision token으로 전달합니다. 공개 benchmark에서는 SWE-bench Pro 19쌍에서 request size가 60% 줄었지만 해결 수는 압축 사용 14건, 미사용 15건이었고, dense image 안의 12자리 hex 정확 재현은 Fable 5에서 13/15, Opus에서 0/15였습니다. 즉 gist 보존에는 유용할 수 있지만 hash, ID, secret과 정확한 숫자를 조용히 잘못 읽을 수 있는 lossy 방식입니다. 비용 최적화로 평가하려면 byte-exact data를 text로 고정하고 자체 workload에서 quality와 실제 청구량을 함께 측정해야 합니다.
    [Source URL](https://github.com/teamchong/pxpipe) (GitHub)
    [Source URL](https://news.ycombinator.com/item?id=48776464) (Hacker News)

---

### 데이터베이스 신뢰성

*   **Canonical, 16년 된 SQLite WAL bug를 TLA+로 재현하고 dqlite 영향 검증**
    SQLite 3.7.0부터 3.51.2까지 존재한 WAL-reset bug는 여러 connection의 checkpoint와 write가 매우 좁은 timing으로 겹칠 때 transaction 일부가 database로 반영되지 않는 data race입니다. SQLite 3.51.3과 backport release에서 수정됐으며 발생 확률은 낮지만 결과는 database corruption입니다. Canonical은 TLA+ model checker로 실패 trace와 salt 비교 fix를 검증했고, dqlite는 append와 checkpoint 모두 write lock을 잡아 동시에 진행되지 않으므로 같은 invariant를 위반하지 않는다고 확인했습니다. Embedded SQLite를 WAL mode와 multi-connection으로 쓰는 제품은 bundled version과 vendor backport 여부를 확인해야 합니다.
    [Source URL](https://ubuntu.com/blog/hunting-a-16-year-old-sqlite-bug-with-tla-is-dqlite-affected) (Ubuntu)
    [Source URL](https://www.sqlite.org/wal.html#the_wal_reset_bug) (SQLite)
    [Source URL](https://news.ycombinator.com/item?id=48730953) (Hacker News)

---

오늘의 핵심은 agent가 browser와 CI, enterprise audit 영역까지 들어오면서 기능뿐 아니라 권한, 비용, data exposure와 model lifecycle이 운영 설계의 일부가 됐다는 점입니다. 동시에 context 압축과 concurrent database처럼 드물게 실패하는 최적화는 평균 절감률보다 silent corruption을 찾는 검증 장치가 더 중요합니다.
