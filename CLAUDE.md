# Hwan's Dev Blog

이정환의 개인 기술·철학 블로그다. Jekyll 로 만들고 GitHub Pages 로 배포한다.

- 레포: https://github.com/Hwan3434/Hwan3434.github.io
- 주소: https://hwan3434.github.io
- 이 문서가 블로그 글쓰기 규칙의 유일한 정본이다. 여기서 쓰는 글은 이정환 본인 이름으로 나간다.

# 글 작성 기준 (`_posts/`)

모든 글은 이 기준 하나를 따른다. `python3 tools/check_posts.py`(레포 루트에서 실행, PyYAML 필요)가 검사하고, GitHub Actions `Post Lint`(`.github/workflows/post-lint.yml`)가 PR·main push·매일 새벽 4시(KST)에 돌린다. 위반이 있으면 `파일: 무엇을 어겼는지`를 찍고 실패한다.

## 위치와 파일명

| 구분 | 한국어판 | 영어판 |
|---|---|---|
| 기술 | `_posts/Tech/` | `_posts/en/tech/` |
| 철학 | `_posts/Philosophy/` | `_posts/en/philosophy/` |
| 뉴스 | `_posts/news/` | `_posts/en/news/` |

- 한국어판 폴더는 대소문자가 섞여 있다(`Tech`, `Philosophy`, `news`). 영어판은 모두 소문자다.
- 파일명은 `YYYY-MM-DD-영문-소문자-슬러그.md`다. 영어판도 **같은 파일명**으로 둔다.
- 영어판이 없으면 검사 위반이다. 한국어 글을 쓰면 영어판도 같이 쓴다.
- 한영 전환 버튼은 URL 에서 `/en` 만 떼거나 붙여 짝을 찾는다(`/posts/:year/:month/:day/:slug/` ↔ `/en/posts/...`). 파일명이나 날짜가 다르면 버튼이 없는 주소로 간다.

## frontmatter

필수 키: `title`, `description`, `date`, `categories`, `tags`.

- `description`: 한 문장. 목록과 검색 결과에 보인다. 120자 안팎을 권장한다(길이는 검사하지 않는다).
- `date`: `YYYY-MM-DD HH:MM:SS +0900`. 파일명 날짜와 같아야 한다.
- `categories`
  - 기술·철학은 `[대분류, 세부]` 두 개다. 대분류는 영문 소문자다(예: `[android, compose]`, `[flutter, 트러블슈팅]`).
  - 철학은 대분류가 반드시 `philosophy`다(예: `[philosophy, 에세이]`).
  - 뉴스는 `[news]` 하나다.
- `tags`: 목록.

선택 키:

- `series` + `series_order`(정수): 함께 쓴다. 같은 언어·같은 `series` 글을 모아 글 위에 시리즈 목차를 그린다.
- `pin`: 검사는 허용하지만 지금 레이아웃(`_layouts/`, `_includes/`)은 이 값을 쓰지 않는다.
- `noindex: true` + `sitemap: false`: 함께 쓴다.
- `toc: false`: 목차를 끌 때만 쓴다.

쓰지 않는 키: `layout`, `toc: true`, `lang`, `locale`, `permalink`, `comments`. `_config.yml` 의 `defaults` 가 채운다(`_posts/en` 아래는 `lang: en` 과 `/en/posts/...` 주소가 붙는다). 위에 없는 키도 쓰지 않는다.

영어판은 `title`·`description`·`tags` 를 영어로 옮긴다. `categories` 세부와 `series` 제목도 옮긴다(예: `[philosophy, essay]`, `"Android Through a Flutter Developer's Eyes"`). 대분류와 `date` 는 한국어판과 같다.

## 본문 제목

- `#` 은 쓰지 않는다. 페이지 제목은 `title` 이 그린다.
- `##` 부터 시작하고 한 단계씩 내려간다(`##` → `###` → `####`). 코드 블록 안의 `#` 은 검사하지 않는다.
- 목차는 `##`·`###` 을 모은다. 항목이 2개 미만이면 숨겨진다.

## 글이 어느 목록에 뜨는가

폴더가 아니라 `categories` 가 정한다.

- 철학 목록(`/philosophy/`)은 `categories` 에 `philosophy` 가 있는 글이다.
- 뉴스 목록(`/news/`)은 `news` 가 있는 글이다.
- 기술 목록(`/tech/`)은 둘 다 아닌 글 전부다.
- 각 목록은 페이지 언어와 같은 언어의 글만 보여 준다.

# 글쓰기 원칙

이 블로그의 글은 공부한 기술 내용이나 일하면서 정리한 생각을 설명하는 글이다.

- **판정 말투 금지:** "틀렸다", "맞았다", "틀린 생각이었다", "흔한 실수", "반은 맞고 반은 틀리다"처럼 정답을 판정하는 말투를 쓰지 않는다. 개념이 어떻게 동작하는지, 왜 그런지를 설명한다.
- **지어낸 일화 금지:** 작성자가 겪었다고 확인되지 않은 1인칭 경험("저는 두 번 틀렸습니다" 등)을 만들어 넣지 않는다. 경험은 작성자가 준 자료나 대화에서 직접 말한 것만 쓴다. 철학 글의 사례(즐겨찾기 응답의 `null`, 체크박스 제안 등)도 모두 작성자 본인의 일이다.
- **맥락 유지:** 앞뒤 흐름과 동떨어진 문장을 끼워 넣지 않는다. 강조할 내용은 표나 설명의 흐름 안에 녹인다.
- **사실 확인:** 버전, API 동작, 수치는 확인한 것만 쓴다.
- 흐름·맥락을 같이 다듬을 때는 `.claude/skills/flow-pair` 스킬을, 문장 안의 AI 티를 지울 때는 `.claude/skills/humanize-korean` 스킬을 쓴다.

## 문체

기존 글의 문체는 두 갈래다. 새 글을 어느 쪽으로 쓸지 정해지지 않았으면 작성자에게 묻는다.

| | 합니다체 | 해라체 |
|---|---|---|
| 글 | 철학 「백엔드와의 계약, 기획자와의 계약」(2026-10), 기술 「Flutter 개발자가 본 Android」 시리즈(2026-06~07) | 철학 「Flutter 철학, 나의 언어로」(2026-03), 「AI 시대, 기획자와 개발자의 경계…」(2026-06) |
| 화자 | "저" | "나", 때로 "우리" |
| 줄바꿈 | 한 문장마다 줄을 바꾸고, 생각 단위로 빈 줄을 둔다 | 문단 단위로 쓴다 |

## 글의 구성 (기존 글에서 보이는 것)

- **도입:** 제목 없이 몇 줄로 상황을 깔고, 글이 답할 질문을 인용 블록으로 세운다(예: `> "이건 내가 막아야 하나, 고쳐 달라고 해야 하나."`). 해라체 글은 첫 `##` 아래에서 같은 일을 한다.
- **시리즈 글:** 도입 끝에 이 편이 다루는 범위를 인용 블록으로 적는다(예: `> 4편은 …를 따라갑니다.`). 끝에서 다음 편을 한 줄로 예고한다.
- **강조:** 핵심 문장 한두 개를 굵게 쓴다. 굵은 글씨를 문단마다 뿌리지 않는다.
- **대비는 표로:** 두 대상의 차이(기획자와 개발자, 과거와 지금, Flutter 와 Compose)는 표로 보여 준다.
- **사례는 구체적으로:** 원칙을 말한 뒤 실제 사례를 붙인다. 순서가 있는 대응은 번호 목록에 굵은 동사로 쓴다(`1. **막는다**: …`).
- **맺음:** "정리하면 이렇습니다." 뒤에 요약 목록을 두거나(합니다체 철학·기술 글), 짧은 맺음 문단을 둔다(해라체 철학 글). 해라체 글은 `---` 가로줄로 큰 구간을 나누기도 한다.
- **기술 글:** Flutter 개발자의 눈으로 다른 플랫폼을 비교하는 관점이 자주 나온다. 대응표에 "Flutter로 치면" 열을 두고, 코드 블록에는 언어(`kotlin`, `dart` 등)를 적는다.

# 서비스 구조

글을 쓰거나 고칠 때 알아야 할 것만 적는다.

## 페이지

| 주소 | 파일 | 내용 |
|---|---|---|
| `/` | `about.md` | 소개(프로필). 예전 주소 `/about/` 은 `about-redirect.html` 이 넘겨 준다 |
| `/tech/` | `tech.html` | 기술 목록 |
| `/philosophy/` | `philosophy.html` | 철학 목록 |
| `/news/` | `news.html` | 뉴스 목록 |
| `/en/...` | `en/` | 위 페이지들의 영어판 |
| `/jobs.html` | (생성물) | 비밀번호로 잠근 채용 페이지 |

- 레이아웃은 `_layouts/`(`default`, `home`, `page`, `post`), 공통 조각은 `_includes/`(내비게이션, SEO, 시리즈 목차, 글 목록 한 줄 등)에 있다.
- 화면 문구는 `_data/ko.yml`, `_data/en.yml` 에 있다. 카테고리 표시 이름은 `_data/category_labels.yml` 이 정하고, 없으면 첫 글자만 대문자로 보인다.
- `_plugins/` 는 git 마지막 수정 시각을 글·페이지의 `last_modified_at`(사이트맵 lastmod)으로 단다. 글을 고치면 커밋 시각이 곧 수정일이 된다.
- `llms.txt` 는 AI 크롤러용 작성자·블로그 소개다.
- `research/` 는 조사 노트다. `_config.yml` 의 `exclude` 로 사이트에는 나가지 않는다. `tools/` 도 마찬가지다.

## 자동으로 만들어지는 것 (손으로 고치지 않는다)

- **채용 페이지 `jobs.html`:** 레포에 없다(`.gitignore`). 배포 때 `tools/generate_job_html.py` 가 `tools/jobs.json` 과 틀 `tools/jobs_page.html` 로 만들고, 지원 이력은 Secret 으로만 받아 암호화해 넣는다. 자동 수집은 없다.
- **뉴스(`_posts/news/`, `_posts/en/news/`):** 매일 클라우드 Claude 루틴이 `tools/ai_mobile_digest_prompt.md` 지침대로 한국어·영어판을 써서 main 에 바로 커밋한다. 뉴스 형식을 바꾸려면 그 지침 파일을 고친다.

## GitHub Actions (`.github/workflows/`)

| 파일 | 하는 일 |
|---|---|
| `pages-deploy.yml` | main push 마다 채용 페이지를 만들고 Jekyll 로 빌드해 Pages 에 배포한다 |
| `post-lint.yml` | `Post Lint`. `tools/check_posts.py` 를 돌린다 |
| `jobs-test.yml` | `tools/*.py` 를 바꾸면 `tools/test_job_scraper.py` 를 돌린다 |

## 그 밖의 `tools/`

- `tools/blog_mcp.js`: 글을 만드는 로컬 MCP 서버. 한국어판 파일만 만들고 바로 커밋·push 한다. 영어판은 따로 써야 한다.
