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

import yaml

ROOT = "_posts"

REQUIRED = ["title", "description", "date", "categories", "tags"]
OPTIONAL = ["series", "series_order", "pin", "noindex", "sitemap", "toc"]
# _config.yml defaults 가 채우는 값. 글에 쓰면 글마다 달라 보이기만 한다.
BY_DEFAULTS = ["layout", "lang", "locale", "permalink", "comments"]

# 루틴이 description·영어판을 쓰기 전에 올라간 뉴스. 소급해 채우지 않고 검사에서 뺀다.
NEWS_LEGACY_BEFORE = dt.date(2026, 10, 30)

# 한국어 폴더 → 영어판 폴더
SECTIONS = {"Tech": "tech", "Philosophy": "philosophy", "news": "news"}

FILENAME = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")


def split(text):
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    return (m.group(1), m.group(2)) if m else (None, None)


def headings(body):
    fenced = False
    for line in body.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
            continue
        m = None if fenced else re.match(r"^(#{1,6}) \S", line)
        if m:
            yield len(m.group(1)), line.strip()


def check(path, section, is_en):
    errs = []
    name = os.path.basename(path)
    fm_text, body = split(open(path, encoding="utf-8").read())
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
    legacy = news and file_date and file_date < NEWS_LEGACY_BEFORE

    for k in REQUIRED:
        if k == "description" and legacy:
            continue
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

    if not is_en and not legacy:
        pair = os.path.join(ROOT, "en", SECTIONS[section], name)
        if not os.path.exists(pair):
            errs.append(f"영어판이 없다: {pair}")
    return errs


def main():
    if not os.path.isdir(ROOT):
        sys.exit("레포 루트에서 실행한다")
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
            for e in check(path, sec, is_en):
                print(f"{path}: {e}")
                bad += 1
    print(f"\n글 {total}편 검사, 위반 {bad}건")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
