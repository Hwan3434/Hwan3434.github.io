#!/usr/bin/env python3
"""블로그 글이 CLAUDE.md '글 작성 기준'을 지키는지 검사한다.

    python3 tools/check_posts.py        # 레포 루트에서 실행

어긴 글이 있으면 '파일: 무엇을 어겼는지'를 한 줄씩 찍고 1로 끝난다.
GitHub Actions(.github/workflows/post-lint.yml)가 PR·push·매일 새벽 4시에 돌린다.
"""
import datetime as dt
import os
import re
import sys
import urllib.parse

import yaml

ROOT = "_posts"

REQUIRED = ["title", "description", "date", "categories", "tags"]
OPTIONAL = ["series", "series_order", "pin", "noindex", "sitemap", "toc"]
# _config.yml defaults 가 채우는 값. 글에 쓰면 글마다 달라 보이기만 한다.
BY_DEFAULTS = ["layout", "lang", "locale", "permalink", "comments"]

# 한국어 폴더 → 영어판 폴더
SECTIONS = {"Tech": "tech", "Philosophy": "philosophy", "news": "news"}

FILENAME = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
POST_FILE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-(.+)\.md$")

# 본문의 링크 목적지. <...> 꼴은 공백을, 맨 꼴은 괄호 한 겹을 품는다. 목적지 뒤의 "제목" 은 잡지 않는다.
DEST = r"\s*(?:<([^>\n]+)>|((?:[^\s()]|\([^\s()]*\))+))"
QUOTED = r"\s*=\s*(?:\"([^\"]*)\"|'([^']*)')"
MD_IMAGE = re.compile(r"!\[[^\]]*\]\(" + DEST)
MD_DEST = re.compile(r"(?<!\\)\]\(" + DEST)  # 그림과 링크 모두. \] 는 글자 그대로라 뺀다
MD_REF = re.compile(r"^ {0,3}\[(?!\^)[^\]]+\]:" + DEST, re.M)  # [이름]: 목적지 (각주 [^1]: 는 뺀다)
HTML_IMG = re.compile(r"<img\b[^>]*?\ssrc" + QUOTED, re.I)
HTML_A = re.compile(r"<a\b[^>]*?\shref" + QUOTED, re.I)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
INLINE_CODE = re.compile(r"(`+).+?\1")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")


def split(text):
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    return (m.group(1), m.group(2)) if m else (None, None)


def outside_code(body):
    """코드 블록 밖의 줄. 코드 블록은 ``` 나 ~~~ 로 열고, 같은 글자를 그 길이 이상 쓴 줄로 닫는다."""
    fence = None
    for line in body.splitlines():
        m = FENCE.match(line)
        if fence is None:
            # ``` 뒤에 ` 가 또 있으면 펜스가 아니라 인라인 코드다
            if m and not (m.group(1)[0] == "`" and "`" in m.group(2)):
                fence = m.group(1)
            else:
                yield line
        elif m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not m.group(2).strip():
            fence = None


def headings(body):
    for line in outside_code(body):
        m = re.match(r"^(#{1,6}) \S", line)
        if m:
            yield len(m.group(1)), line.strip()


def links(body):
    """코드와 HTML 주석 밖 본문의 링크 목적지마다 그림인지를 단다. {목적지: 그림인가}"""
    # 여러 줄에 걸친 <img> 와 주석을 잡으려고 줄을 다시 잇는다
    text = HTML_COMMENT.sub("", "\n".join(INLINE_CODE.sub("", line) for line in outside_code(body)))
    hits = sorted((m.start(), m.group(m.lastindex), image)
                  for rx, image in ((MD_DEST, False), (MD_REF, False), (HTML_A, False), (MD_IMAGE, True), (HTML_IMG, True))
                  for m in rx.finditer(text))
    found = {}
    for _, dest, image in hits:
        found[dest] = found.get(dest, False) or image
    return found


def post_urls(config):
    """_config.yml defaults 의 permalink 로 만든 글 주소 전부와, 글 주소가 시작하는 접두사들."""
    rules = [(d["scope"].get("path", ""), d["values"]["permalink"])
             for d in config.get("defaults", [])
             if d.get("scope", {}).get("type") == "posts" and "permalink" in d.get("values", {})]
    urls, prefixes = set(), set()
    for root, _, files in os.walk(ROOT):
        for f in files:
            m = POST_FILE.match(f)
            if not m:
                continue
            path = os.path.join(root, f)
            # Jekyll 은 scope path 가 가장 길게 맞는 defaults 를 쓴다
            _, link = max(((s, p) for s, p in rules if not s or path.startswith(s.rstrip("/") + "/")),
                          key=lambda r: len(r[0]))
            # Jekyll 은 frontmatter date 로 주소를 만든다. check() 가 그 날짜를 파일명 날짜와 같게 강제하니 파일명에서 딴다.
            year, month, day, slug = m.groups()
            urls.add(link.replace(":year", year).replace(":month", month).replace(":day", day).replace(":slug", slug))
            prefixes.add(link.split(":")[0])
    return urls, tuple(prefixes)


def repo_file(path):
    """레포에 대소문자까지 같은 파일이 있는가. macOS 는 대소문자를 가리지 않지만 Pages 는 가린다."""
    cur = "."
    for part in path.strip("/").split("/"):
        if not os.path.isdir(cur) or part not in os.listdir(cur):
            return False
        cur = os.path.join(cur, part)
    return os.path.isfile(cur)


def link_errors(body, posts):
    urls, prefixes = posts
    errs = []
    for dest, image in links(body).items():
        if not dest.startswith("/") or dest.startswith("//"):
            continue  # 바깥 주소
        path = urllib.parse.unquote(re.split(r"[?#]", dest)[0])
        if path.startswith(prefixes):
            if not {path, path + "/", path.removesuffix("index.html")} & urls:
                errs.append(f"링크한 글이 없다: {dest}")
        elif image and not repo_file(path):
            errs.append(f"이미지 파일이 없다: {dest}")
    return errs


def check(path, section, is_en, posts):
    errs = []
    name = os.path.basename(path)
    with open(path, encoding="utf-8") as f:
        fm_text, body = split(f.read())
    if fm_text is None:
        return ["frontmatter(---)가 없다"]
    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError as e:
        return [f"frontmatter가 YAML로 읽히지 않는다: {e}".splitlines()[0]]

    fname = FILENAME.match(name)
    if not fname:
        errs.append("파일명은 YYYY-MM-DD-영문-소문자-슬러그.md 형식이어야 한다")
    file_date = dt.date(*map(int, fname.groups())) if fname else None

    news = section == "news"

    for k in REQUIRED:
        if not fm.get(k):
            errs.append(f"{k}: 빠졌다")
    for k in fm:
        if k in BY_DEFAULTS:
            errs.append(f"{k}: _config.yml 기본값이 채운다. 글에서 지운다")
        elif k not in REQUIRED + OPTIONAL:
            errs.append(f"{k}: 기준에 없는 키다")

    if "toc" in fm and fm["toc"] is not False:
        errs.append("toc: 기본이 켜짐이다. 끌 때만 'toc: false'로 쓴다")
    if ("series" in fm) != ("series_order" in fm):
        errs.append("series와 series_order는 함께 쓴다")
    if "series_order" in fm and not isinstance(fm["series_order"], int):
        errs.append("series_order는 정수다")
    if ("noindex" in fm) != ("sitemap" in fm):
        errs.append("noindex: true와 sitemap: false는 함께 쓴다")

    # PyYAML 은 '+0900' 시간대를 못 읽어 문자열로 넘긴다. Jekyll 은 읽는다. 그래서 글자로 본다.
    date = fm.get("date")
    if date:
        m = re.match(r"^(\d{4})-(\d{2})-(\d{2}) \d{2}:\d{2}(?::\d{2})? \+0900$", str(date))
        if not m:
            errs.append(f"date는 'YYYY-MM-DD HH:MM:SS +0900' 형식이다: {date}")
        elif file_date and dt.date(*map(int, m.groups())) != file_date:
            errs.append(f"date가 파일명 날짜({file_date})와 다르다: {date}")

    cats = fm.get("categories")
    if cats is not None:
        if not isinstance(cats, list):
            errs.append("categories는 [대분류, 세부] 목록이다")
        elif news and cats != ["news"]:
            errs.append("뉴스의 categories는 [news] 하나다")
        elif not news and len(cats) != 2:
            errs.append("categories는 [대분류, 세부] 두 개다")
        elif section == "Philosophy" and cats[0] != "philosophy":
            errs.append("철학 글의 categories는 [philosophy, 세부]다")
        elif not news and cats[0] != str(cats[0]).lower():
            errs.append("categories 대분류는 영문 소문자다")
    if fm.get("tags") is not None and not isinstance(fm["tags"], list):
        errs.append("tags는 목록이다")

    prev = 1
    for level, line in headings(body):
        if level == 1:
            errs.append(f"본문에 # 제목이 있다(제목은 title이 그린다): {line[:40]}")
        elif level > prev + 1:
            where = "첫 제목" if prev == 1 else f"h{prev} 다음"
            errs.append(f"제목 단계를 건너뛴다({where}에 h{level}, ##부터 한 단계씩): {line[:40]}")
        prev = max(level, 2)

    errs += link_errors(body, posts)

    if not is_en:
        pair = os.path.join(ROOT, "en", SECTIONS[section], name)
        if not os.path.exists(pair):
            errs.append(f"영어판이 없다: {pair}")
    return errs


def main():
    if not os.path.isdir(ROOT):
        sys.exit("레포 루트에서 실행한다")
    with open("_config.yml", encoding="utf-8") as f:
        posts = post_urls(yaml.safe_load(f))
    bad = 0
    total = 0
    for root, dirs, files in sorted(os.walk(ROOT)):
        rel = os.path.relpath(root, ROOT).split(os.sep)
        is_en = rel[0] == "en"
        sec = rel[1] if is_en and len(rel) > 1 else rel[0]
        if is_en:
            sec = {v: k for k, v in SECTIONS.items()}.get(sec, sec)
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            if sec not in SECTIONS:
                print(f"{path}: _posts/{{Tech,Philosophy,news}} 또는 _posts/en/{{tech,philosophy,news}} 아래에 둔다")
                bad += 1
                continue
            total += 1
            for e in check(path, sec, is_en, posts):
                print(f"{path}: {e}")
                bad += 1
    print(f"\n글 {total}편 검사, 위반 {bad}건")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
