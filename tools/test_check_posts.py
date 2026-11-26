"""글 검사(check_posts.py) 중 본문의 이미지·글 링크 검사 테스트.

임시 폴더에 레포 모양(_config.yml, _posts, assets)을 만들고 그 안에서 check_posts.main() 을 돌린다.
_config.yml 은 레포의 것을 그대로 복사해서, 실제 permalink 설정으로 글 주소를 맞추는지 본다.

    python3 tools/test_check_posts.py      # PyYAML 필요
"""

import contextlib
import io
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import check_posts as cp

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

POST = """---
title: 제목
description: 설명.
date: {date} 10:00:00 +0900
categories: [android, compose]
tags: [a]
---

{body}
"""

# 검사하는 글. 한국어판에 본문을 넣고, 영어판은 비워 둔다.
SRC = "_posts/Tech/2026-01-10-src.md"
# 검사하지 않는 것만 있는 글에 같이 넣는 깨진 이미지. 위반이 이것 하나만 찍혀야 한다.
SENTINEL = "![x](/assets/img/missing.png)"
SENTINEL_ERR = f"{SRC}: 이미지 파일이 없다: /assets/img/missing.png"


class LinkCheckTest(unittest.TestCase):

    def setUp(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp)
        shutil.copy(os.path.join(REPO, "_config.yml"), tmp)
        cwd = os.getcwd()
        os.chdir(tmp)
        self.addCleanup(os.chdir, cwd)
        self.write("assets/img/posts/a/one.png", "")
        # 링크 대상: 한국어·영어판이 다 있는 글과 영어판만 있는 글
        self.post("Tech/2026-01-02-target.md")
        self.post("en/tech/2026-01-02-target.md")
        self.post("en/tech/2026-01-03-en-only.md")

    def write(self, rel, text):
        os.makedirs(os.path.dirname(rel) or ".", exist_ok=True)
        with open(rel, "w", encoding="utf-8") as f:
            f.write(text)

    def post(self, rel, body="본문."):
        date = os.path.basename(rel)[:10]
        self.write(os.path.join("_posts", rel), POST.format(date=date, body=body))

    def check(self, body):
        """SRC 에 body 를 넣고 검사한다. (종료 코드, 위반 줄 목록)"""
        self.post("Tech/2026-01-10-src.md", body)
        self.post("en/tech/2026-01-10-src.md")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = cp.main()
        return code, [line for line in out.getvalue().splitlines() if line.startswith("_posts/")]

    def test_existing_images_and_posts_pass(self):
        code, errs = self.check("\n".join([
            "![a](/assets/img/posts/a/one.png)",
            '![a](/assets/img/posts/a/one.png "제목")',
            "![a](/assets/img/posts/a/one.png?v=1)",
            '<img alt="a" src="/assets/img/posts/a/one.png">',
            "[글](/posts/2026/01/02/target/)",
            "[글](/posts/2026/01/02/target/#section)",
            "[글](/posts/2026/01/02/target)",
            "[post](/en/posts/2026/01/02/target/)",
            '<a href="/en/posts/2026/01/02/target/">post</a>',
        ]))
        self.assertEqual(errs, [])
        self.assertEqual(code, 0)

    def test_missing_image_fails(self):
        code, errs = self.check("\n".join([
            "![a](/assets/img/posts/a/two.png)",
            "<img alt='b' src='/assets/img/posts/a/three.png'>",
        ]))
        self.assertEqual(errs, [
            f"{SRC}: 이미지 파일이 없다: /assets/img/posts/a/two.png",
            f"{SRC}: 이미지 파일이 없다: /assets/img/posts/a/three.png",
        ])
        self.assertEqual(code, 1)

    def test_image_path_case_must_match(self):
        # macOS 는 대소문자를 가리지 않아 파일이 있다고 답하지만 Pages 는 404 다
        code, errs = self.check("![a](/assets/img/posts/A/one.png)")
        self.assertEqual(errs, [f"{SRC}: 이미지 파일이 없다: /assets/img/posts/A/one.png"])

    def test_missing_post_fails(self):
        code, errs = self.check("\n".join([
            "[없는 글](/posts/2026/01/02/nope/)",
            '<a href="/posts/2026/01/09/target/">날짜가 다른 글</a>',
            "[형식이 다른 주소](/posts/target/)",
            "[참조][ref]",
            "",
            "[ref]: /posts/2026/01/02/nope-ref/",
        ]))
        self.assertEqual(errs, [
            f"{SRC}: 링크한 글이 없다: /posts/2026/01/02/nope/",
            f"{SRC}: 링크한 글이 없다: /posts/2026/01/09/target/",
            f"{SRC}: 링크한 글이 없다: /posts/target/",
            f"{SRC}: 링크한 글이 없다: /posts/2026/01/02/nope-ref/",
        ])
        self.assertEqual(code, 1)

    def test_korean_and_english_urls_are_told_apart(self):
        # 영어판만 있는 글은 /en/posts/ 주소로만 있다
        code, errs = self.check("\n".join([
            "[post](/en/posts/2026/01/03/en-only/)",
            "[글](/posts/2026/01/03/en-only/)",
        ]))
        self.assertEqual(errs, [f"{SRC}: 링크한 글이 없다: /posts/2026/01/03/en-only/"])

    def test_paths_in_code_are_not_checked(self):
        code, errs = self.check("\n".join([
            "```markdown",
            "![a](/assets/img/no1.png)",
            "```",
            "~~~",
            "[글](/posts/2026/01/01/no2/)",
            "~~~",
            "인라인 `![a](/assets/img/no3.png)` 와 `` <img src=\"/assets/img/no4.png\"> `` 는 코드다.",
            SENTINEL,
        ]))
        self.assertEqual(errs, [SENTINEL_ERR])

    def test_external_urls_are_not_checked(self):
        code, errs = self.check("\n".join([
            "![a](https://example.com/x.png)",
            "![a](http://example.com/x.png)",
            "![a](//cdn.example.com/x.png)",
            '<img src="https://example.com/y.png">',
            "[글](https://hwan3434.github.io/posts/2026/01/01/nope/)",
            SENTINEL,
        ]))
        self.assertEqual(errs, [SENTINEL_ERR])

    def test_site_pages_are_not_checked(self):
        code, errs = self.check("\n".join([
            "[기술](/tech/)",
            "[Philosophy](/en/philosophy/)",
            "[태그](/tags/flutter/)",
            "[홈](/)",
            SENTINEL,
        ]))
        self.assertEqual(errs, [SENTINEL_ERR])

    def test_post_urls_follow_config_permalink(self):
        with open("_config.yml", encoding="utf-8") as f:
            text = f.read()
        self.assertEqual(text.count("posts/:year/:month/:day/:slug/"), 2)
        self.write("_config.yml", text.replace("posts/:year/:month/:day/:slug/", "blog/:year/:slug/"))
        code, errs = self.check("\n".join([
            "[글](/blog/2026/target/)",
            "[post](/en/blog/2026/en-only/)",
            "[없는 글](/blog/2026/nope/)",
            "[post](/en/blog/2026/nope/)",
        ]))
        self.assertEqual(errs, [
            f"{SRC}: 링크한 글이 없다: /blog/2026/nope/",
            f"{SRC}: 링크한 글이 없다: /en/blog/2026/nope/",
        ])


if __name__ == "__main__":
    unittest.main(verbosity=2)
