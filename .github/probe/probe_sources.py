"""임시 판정용 2차. 1차에서 살아남은 후보의 세부를 확인한다. 판정이 끝나면 지운다.

1. 추가할 그리팅 보드가 정말 그 회사인지 (<title>, 공고 제목)
2. 점핏 API 호스트 robots.txt, 직군 필터(jobCategory) 번호, 페이지 크기
3. 랠릿 직군 필터 파라미터
4. 리멤버 __NEXT_DATA__ 안에서 공고 목록 위치
5. 매치그룹 Lever 서울 공고 목록
"""

import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, 'tools')
import job_scraper as js  # noqa: E402

PAUSE = 0.4
BROWSER = {
    'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'),
    'Accept': 'application/json, text/plain, */*',
}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def probe(url, headers=None, follow=True):
    req = urllib.request.Request(url, headers=headers or {'User-Agent': js.USER_AGENT})
    opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NoRedirect)
    try:
        with opener.open(req, timeout=15) as r:
            return r.status, r.read().decode('utf-8', 'replace'), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, '', dict(e.headers or {})
    except Exception as e:
        return type(e).__name__, '', {}
    finally:
        time.sleep(PAUSE)


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


# ------------------------------------------------------------ 3. 랠릿 샘플

RALLIT_API = "https://www.rallit.com/api/v1/position"


def check_rallit():
    section("3. 랠릿 — 공고 한 건의 전체 필드")
    for job in ("ANDROID_DEVELOPER", "IOS_DEVELOPER", "FLUTTER_DEVELOPER",
                "CROSS_PLATFORM_DEVELOPER", "MOBILE_DEVELOPER", "REACT_NATIVE_DEVELOPER"):
        url = f"{RALLIT_API}?jobGroup=DEVELOPER&job={job}&pageNumber=1&pageSize=20"
        status, body, _ = probe(url, BROWSER)
        if status != 200:
            print(f"  {job}: {status}")
            continue
        payload = json.loads(body)
        data = payload.get('data')
        if not isinstance(data, dict):
            print(f"  {job}: data 가 dict 가 아니다 — {body[:200]!r}")
            continue
        items = data.get('items') or []
        statuses = sorted({json.dumps(i.get('status'), ensure_ascii=False) for i in items})
        print(f"  {job}: total {data.get('totalCount')} · statuses={statuses}")
        for i in items[:12]:
            print(f"      · {i.get('title')} | {i.get('companyName')} | {i.get('startedAt')}~{i.get('endedAt')} | {i.get('url')}")
        if items:
            print("    샘플:", json.dumps(items[0], ensure_ascii=False)[:700])


# ------------------------------------------------------------ 4. 리멤버

NEXT_RE = re.compile(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', re.S)


def tree(node, path='', depth=0, out=None):
    out = [] if out is None else out
    if depth > 7 or len(out) > 80:
        return out
    if isinstance(node, dict):
        for k, v in node.items():
            tree(v, f"{path}.{k}", depth + 1, out)
    elif isinstance(node, list):
        if node and isinstance(node[0], dict):
            out.append(f"{path}[{len(node)}] keys={list(node[0])[:12]}")
            tree(node[0], f"{path}[0]", depth + 1, out)
    return out


def check_remember():
    section("4. 리멤버 — __NEXT_DATA__ 안의 목록")
    status, body, _ = probe("https://career.rememberapp.co.kr/job/postings", BROWSER)
    m = NEXT_RE.search(body)
    if not m:
        print(f"  {status}, __NEXT_DATA__ 없음")
        return
    data = json.loads(m.group(1))
    for line in tree(data):
        print("  " + line)


# ------------------------------------------------------------ 5. 매치그룹

def check_matchgroup():
    section("5. 매치그룹 Lever — 서울 공고")
    status, body, _ = probe("https://api.lever.co/v0/postings/matchgroup?location=Seoul%2C%20South%20Korea")
    if status != 200:
        print(f"  {status}")
        return
    for p in json.loads(body):
        cats = p.get('categories') or {}
        print(f"  · {p.get('text')}  [{cats.get('team')} / {cats.get('location')}]")


if __name__ == '__main__':
    import traceback
    for check in (check_rallit, check_remember, check_matchgroup):
        try:
            check()
        except Exception:
            traceback.print_exc(file=sys.stdout)
