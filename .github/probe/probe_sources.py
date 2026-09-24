"""임시 판정용. 채용 소스 후보를 러너에서 실측한다. 판정이 끝나면 지운다.

A. 그리팅 — 웹 검색으로 실제 존재가 확인된 보드 + 짐작한 후보
B. Greenhouse / Lever — 검색으로 보인 것 + 짐작한 후보
C. 채용 플랫폼 — 러너 IP 를 막는지, robots.txt 가 허용하는지, 응답 형태
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, 'tools')
import job_scraper as js  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PAUSE = 0.3  # 연달아 두드리지 않는다


def probe(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {'User-Agent': js.USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, ''
    except Exception as e:
        return type(e).__name__, ''
    finally:
        time.sleep(PAUSE)


def existing():
    return (set(js.GREETING_COMPANIES), set(js.GREENHOUSE_BOARDS), set(js.LEVER_ACCOUNTS))


# ------------------------------------------------------------ A. 그리팅

GREETING_GUESSES = """
banksalad kakaobank kakaoent kakaogames kakaohealthcare kakaostyle zigzag 29cm
wconcept ssg lotteon wemakeprice bunjang joongna myrealtrip triple interpark
yanoljacloud nol greencar vcnc watcha wavve tving spoon spoonradio azar class101
taling kmong soomgo brave riiid mathpresso qanda enuma day1company fastcampus
inflearn elice yogiyo ncsoft nexon netmarble smilegate devsisters com2us
pearlabyss shiftup bithumb coinone korbit lambda256 8percent lendit peoplefund
payhere rainist kbank laftel dreamus flo jobkorea saramin dramancompany
wantedlab rocketpunch station3 dabang hogangnono goodoc doctornow bbros
mediwhale lunit vuno ably ablycorp a-bly kream kreamcorp stylenanda hiver zipdoc
frip munto trevari lifegoeson laundrygo catchtable wad tabling weverse
channelcorp flexteam braincommerce teamblind wadiz liner upstage scatterlab
tosslab jandi daangnpay hanatour yeogi aitrics sparklabs musinsa-recruit
socarcorp gangnam-unni oliveyoung cjolive kolonmall hyundaihmall
""".split()


def run_greeting():
    have_g, _, _ = existing()
    found = [s.strip() for s in open(os.path.join(HERE, 'greeting_found.txt')) if s.strip()]
    candidates = []
    for s in found + GREETING_GUESSES:
        if s not in candidates and s not in have_g:
            candidates.append(s)

    print("=" * 72)
    print(f"A. 그리팅 — 후보 {len(candidates)}곳 (검색 확인 {len(found)} + 짐작, 기존 제외)")
    print("=" * 72)
    rows = []
    for sub in candidates:
        url = f"https://{sub}.career.greetinghr.com/"
        status, body = probe(url)
        origin = 'search' if sub in found else 'guess'
        if status != 200:
            rows.append((sub, origin, str(status), 0, 0, []))
            continue
        try:
            openings = js.extract_greetinghr_openings(body, url)
        except js.SourceError as e:
            rows.append((sub, origin, f"파서실패:{str(e)[:40]}", 0, 0, []))
            continue
        titles = [o.get('title') or '' for o in openings]
        mobile = [t for t in titles if js.looks_mobile(t)]
        rows.append((sub, origin, '200', len(titles), len(mobile), mobile))

    ok = [r for r in rows if r[2] == '200']
    print(f"\n200 응답 {len(ok)}곳 / {len(rows)}곳\n")
    for sub, origin, st, total, nm, mobile in sorted(ok, key=lambda r: -r[4]):
        print(f"  {'★' if nm else ' '} {sub:22} [{origin}] 전체 {total:3}건 · 모바일 {nm}건")
        for t in mobile[:6]:
            print(f"        · {t}")
    bad = [r for r in rows if r[2] != '200']
    print(f"\n그 외 {len(bad)}곳:")
    print("  " + ", ".join(f"{r[0]}({r[2]})" for r in bad))
    return rows


# ------------------------------------------------------------ B. Greenhouse / Lever

GREENHOUSE_CANDIDATES = """
dunamu seoulrobotics channelcorp channelio ably wadiz linercorp liner upstage
twelvelabs furiosaai furiosa scatterlab bithumb lunit vuno gentlemonster
hyperconnect toss riiid socar bucketplace kakaostyle ab180 airbridge
""".split()

LEVER_CANDIDATES = "matchgroup sendbird toss riiid krafton nexon hybe musinsa ab180 moloco".split()


def run_ats():
    _, have_gh, have_lv = existing()
    print()
    print("=" * 72)
    print("B-1. Greenhouse")
    print("=" * 72)
    for token in GREENHOUSE_CANDIDATES:
        if token in have_gh:
            continue
        status, body = probe(f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs")
        if status != 200:
            print(f"  -- {token}: {status}")
            continue
        jobs = json.loads(body).get('jobs', [])
        mobile = [j for j in jobs if js.looks_mobile(j.get('title') or '')]
        print(f"  OK {token}: 전체 {len(jobs)} · 모바일 {len(mobile)}")
        for j in mobile[:6]:
            print(f"        · {j.get('title')}  @ {(j.get('location') or {}).get('name')}")

    print()
    print("=" * 72)
    print("B-2. Lever (서울 필터 지원 여부 포함)")
    print("=" * 72)
    for token in LEVER_CANDIDATES:
        if token in have_lv:
            continue
        status, body = probe(f"https://api.lever.co/v0/postings/{token}")
        if status != 200:
            print(f"  -- {token}: {status}")
            continue
        posts = json.loads(body)
        mobile = [p for p in posts if js.looks_mobile(p.get('text') or '')]
        print(f"  OK {token}: 전체 {len(posts)} · 모바일 {len(mobile)}")
        for p in mobile[:6]:
            print(f"        · {p.get('text')}  @ {(p.get('categories') or {}).get('location')}")
        s2, b2 = probe(f"https://api.lever.co/v0/postings/{token}?location=Seoul%2C%20South%20Korea")
        if s2 == 200:
            seoul = json.loads(b2)
            sm = [p for p in seoul if js.looks_mobile(p.get('text') or '')]
            print(f"     └ location=Seoul 필터: 전체 {len(seoul)} · 모바일 {len(sm)}")
            for p in sm[:6]:
                print(f"        · {p.get('text')}  @ {(p.get('categories') or {}).get('location')}")


# ------------------------------------------------------------ C. 채용 플랫폼

BROWSER = {
    'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'),
    'Accept': 'application/json, text/plain, */*',
}

PLATFORMS = [
    ("점핏", "https://jumpit.saramin.co.kr", [
        "https://jumpit-api.saramin.co.kr/api/positions?page=1&sort=reg_dt&keyword=iOS",
        "https://jumpit-api.saramin.co.kr/api/positions?page=1&sort=reg_dt&keyword=%EC%95%88%EB%93%9C%EB%A1%9C%EC%9D%B4%EB%93%9C",
    ]),
    ("랠릿", "https://www.rallit.com", [
        "https://www.rallit.com/positions?jobGroup=DEVELOPER",
        "https://www.rallit.com/api/v1/position?jobGroup=DEVELOPER&pageNumber=1&pageSize=20",
    ]),
    ("프로그래머스", "https://career.programmers.co.kr", [
        "https://career.programmers.co.kr/api/job_positions?page=1",
    ]),
    ("로켓펀치", "https://www.rocketpunch.com", [
        "https://www.rocketpunch.com/api/jobs/template?page=1&q=iOS",
    ]),
    ("직행", "https://zighang.com", [
        "https://zighang.com/",
    ]),
    ("리멤버", "https://career.rememberapp.co.kr", [
        "https://career.rememberapp.co.kr/job/postings",
    ]),
]


def shape(body):
    """응답이 JSON 이면 구조를, HTML 이면 단서만 보여준다."""
    try:
        data = json.loads(body)
    except ValueError:
        hints = []
        if '__NEXT_DATA__' in body:
            hints.append('__NEXT_DATA__')
        if 'window.__NUXT__' in body:
            hints.append('__NUXT__')
        return f"HTML {len(body)}B {' '.join(hints)}"
    if isinstance(data, dict):
        inner = {k: type(v).__name__ for k, v in list(data.items())[:8]}
        out = f"JSON dict keys={inner}"
        for k in ('result', 'data', 'positions', 'jobPositions', 'jobs'):
            v = data.get(k)
            if isinstance(v, dict):
                out += f" | {k}.keys={list(v)[:8]}"
                for kk, vv in v.items():
                    if isinstance(vv, list) and vv and isinstance(vv[0], dict):
                        out += f" | {k}.{kk}[0].keys={list(vv[0])[:14]} (len {len(vv)})"
                        break
            elif isinstance(v, list) and v and isinstance(v[0], dict):
                out += f" | {k}[0].keys={list(v[0])[:14]} (len {len(v)})"
        return out
    if isinstance(data, list):
        return f"JSON list len={len(data)}" + (f" [0].keys={list(data[0])[:14]}" if data and isinstance(data[0], dict) else '')
    return f"JSON {type(data).__name__}"


def robots_rules(base):
    status, body = probe(base + '/robots.txt', BROWSER)
    if status != 200:
        return f"robots.txt {status}"
    lines, active = [], False
    for raw in body.splitlines():
        line = raw.split('#')[0].strip()
        if not line:
            continue
        key, _, val = line.partition(':')
        key, val = key.strip().lower(), val.strip()
        if key == 'user-agent':
            active = (val == '*')
        elif active and key in ('disallow', 'allow'):
            lines.append(f"{key}:{val}")
    return "robots(*): " + (", ".join(lines[:20]) or "제한 없음")


def run_platforms():
    print()
    print("=" * 72)
    print("C. 채용 플랫폼 — 러너 IP 차단 여부 · robots.txt · 응답 형태")
    print("=" * 72)
    for name, base, urls in PLATFORMS:
        print(f"\n[{name}] {base}")
        print(f"  {robots_rules(base)}")
        for url in urls:
            status, body = probe(url, BROWSER)
            print(f"  {status} {url}")
            if status == 200:
                print(f"      {shape(body)}")
                print(f"      앞부분: {body[:240]!r}")


if __name__ == '__main__':
    run_greeting()
    run_ats()
    run_platforms()
