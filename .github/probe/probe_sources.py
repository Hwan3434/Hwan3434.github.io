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


# ------------------------------------------------------------ 1. 그리팅 신원 확인

CHOSEN = """
pfct scatterlab oliveyoung kidsnote kurly nrise apartmentary medistream danbiedu
kakaopay gripcorp gccompany estfamily myrealtrip soomgo catchtable wadiz goodoc
kmong hybe travel-wallet spoonradio wconcept gravitylabs
""".split()

TITLE_RE = re.compile(r'<title[^>]*>(.*?)</title>', re.S)


def check_greeting():
    section("1. 그리팅 — 추가 후보의 신원")
    for sub in CHOSEN:
        url = f"https://{sub}.career.greetinghr.com/"
        status, body, _ = probe(url)
        if status != 200:
            print(f"  -- {sub}: {status}")
            continue
        m = TITLE_RE.search(body)
        page_title = (m.group(1).strip() if m else '?')[:60]
        try:
            titles = [o.get('title') or '' for o in js.extract_greetinghr_openings(body, url)]
        except js.SourceError as e:
            print(f"  !! {sub}: {e}")
            continue
        print(f"  {sub:14} <title>{page_title}</title>  공고 {len(titles)}건")
        for t in titles[:8]:
            print(f"        · {t}")


# ------------------------------------------------------------ 2. 점핏

JUMPIT_API = "https://jumpit-api.saramin.co.kr/api/positions"


def check_jumpit():
    section("2. 점핏 — API 호스트 robots.txt · jobCategory 번호")
    status, body, _ = probe("https://jumpit-api.saramin.co.kr/robots.txt", BROWSER)
    print(f"  api 호스트 robots.txt: {status} {body[:300]!r}")

    for cat in range(1, 26):
        status, body, _ = probe(f"{JUMPIT_API}?page=1&sort=reg_dt&jobCategory={cat}", BROWSER)
        if status != 200:
            print(f"  jobCategory={cat}: {status}")
            continue
        result = json.loads(body).get('result') or {}
        positions = result.get('positions') or []
        cats = sorted({p.get('jobCategory') for p in positions[:6]})
        print(f"  jobCategory={cat:2}: total {result.get('totalCount')} · 페이지당 {len(positions)} · 예: {cats[:3]}")

    # 페이지 크기를 키울 수 있는지
    for extra in ('&size=100', '&pageSize=100', '&limit=100'):
        status, body, _ = probe(f"{JUMPIT_API}?page=1&sort=reg_dt&jobCategory=4{extra}", BROWSER)
        n = len((json.loads(body).get('result') or {}).get('positions') or []) if status == 200 else status
        print(f"  jobCategory=4{extra}: 한 페이지 {n}")

    # 한 건의 전체 필드
    status, body, _ = probe(f"{JUMPIT_API}?page=1&sort=reg_dt&jobCategory=4", BROWSER)
    if status == 200:
        positions = (json.loads(body).get('result') or {}).get('positions') or []
        if positions:
            print("  샘플 한 건:", json.dumps(positions[0], ensure_ascii=False)[:600])


# ------------------------------------------------------------ 3. 랠릿

RALLIT_API = "https://www.rallit.com/api/v1/position"


def check_rallit():
    section("3. 랠릿 — 리다이렉트 · 필터 파라미터")
    status, _, headers = probe("https://www.rallit.com/positions?jobGroup=DEVELOPER", BROWSER, follow=False)
    loc = headers.get('Location') or headers.get('location')
    print(f"  /positions → {status} Location={loc}")
    if loc:
        target = urllib.parse.urljoin("https://www.rallit.com/", loc)
        status, body, _ = probe(target, BROWSER)
        print(f"  {target} → {status}, {len(body)}B")
        found = sorted(set(re.findall(r'[?&](job[A-Za-z]*|skill[A-Za-z]*|keyword|q)=([A-Z_]{3,40})', body)))
        print(f"  페이지 안의 필터 파라미터 흔적: {found[:30]}")

    base = f"{RALLIT_API}?jobGroup=DEVELOPER&pageNumber=1&pageSize=20"
    status, body, _ = probe(base, BROWSER)
    total = (json.loads(body).get('data') or {}).get('totalCount') if status == 200 else status
    print(f"  기준 DEVELOPER 전체: {total}")
    items = []
    for extra in ('&job=ANDROID_DEVELOPER', '&jobs=ANDROID_DEVELOPER', '&job=ANDROID',
                  '&jobs=ANDROID', '&keyword=Android', '&q=Android',
                  '&job=IOS_DEVELOPER', '&jobs=IOS_DEVELOPER', '&pageSize=100'):
        status, body, _ = probe(base + extra, BROWSER)
        if status != 200:
            print(f"  {extra}: {status}")
            continue
        data = json.loads(body).get('data') or {}
        items = data.get('items') or []
        print(f"  {extra}: total {data.get('totalCount')} · 이번 페이지 {len(items)} · "
              f"예: {[i.get('title') for i in items[:3]]}")
    if items:
        print("  샘플 한 건:", json.dumps(items[0], ensure_ascii=False)[:600])


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
    check_greeting()
    check_jumpit()
    check_rallit()
    check_remember()
    check_matchgroup()
