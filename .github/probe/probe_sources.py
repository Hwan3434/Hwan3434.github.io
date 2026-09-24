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


# ------------------------------------------------------------ 4. 리멤버

NEXT_RE = re.compile(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', re.S)


def shape(node, depth=0):
    if depth > 3:
        return '…'
    if isinstance(node, dict):
        return '{' + ', '.join(f"{k}: {shape(v, depth + 1)}" for k, v in list(node.items())[:10]) + '}'
    if isinstance(node, list):
        return f"[{len(node)}× {shape(node[0], depth + 1) if node else ''}]"
    return type(node).__name__


def remember_queries(url):
    status, body, _ = probe(url, BROWSER)
    m = NEXT_RE.search(body or '')
    if not m:
        print(f"  {url} → {status}, __NEXT_DATA__ 없음")
        return
    data = json.loads(m.group(1))
    print(f"  {url} → {status}")
    print(f"    query: {json.dumps(data.get('query'), ensure_ascii=False)[:200]}")
    for q in data['props']['pageProps'].get('dehydratedState', {}).get('queries', []):
        print(f"    queryKey={json.dumps(q.get('queryKey'), ensure_ascii=False)[:300]}")
        print(f"      data={shape((q.get('state') or {}).get('data'))[:600]}")


def check_remember():
    section("4. 리멤버 — react-query 캐시의 queryKey 와 모양")
    remember_queries("https://career.rememberapp.co.kr/job/postings")
    remember_queries("https://career.rememberapp.co.kr/job/postings?search=%7B%22keywords%22%3A%5B%22iOS%22%5D%7D")
    status, body, _ = probe("https://career.rememberapp.co.kr/robots.txt", BROWSER)
    print(f"  robots.txt 전문:\n{body[:1500]}")


if __name__ == '__main__':
    import traceback
    try:
        check_remember()
    except Exception:
        traceback.print_exc(file=sys.stdout)
