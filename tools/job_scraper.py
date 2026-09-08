"""모바일 채용 공고 수집기.

소스를 추가할 때는 SOURCES 리스트에 (이름, 호출가능한 것) 한 줄만 넣으면 된다.
각 수집 함수는 성공하면 공고 리스트를, 실패하면 SourceError를 올린다.
예외를 삼키지 않는 이유: 2026년 8월 내내 0건을 수집하고도 워크플로가
14회 연속 success로 끝났던 적이 있다. 조용한 실패는 없는 것보다 나쁘다.
"""

import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.request

USER_AGENT = 'Mozilla/5.0 (compatible; Hwan3434-jobs-digest/2.0)'
TIMEOUT = 15

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'jobs.json'))


class SourceError(Exception):
    """한 소스의 수집이 실패했음을 알린다. 나머지 소스는 계속 돈다."""


# ---------------------------------------------------------------- 공통 유틸

def fetch_text(url):
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            return response.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        raise SourceError(f"HTTP {e.code} — {url}")
    except Exception as e:
        raise SourceError(f"{type(e).__name__}: {e} — {url}")


def fetch_json(url):
    body = fetch_text(url)
    try:
        return json.loads(body)
    except json.JSONDecodeError as e:
        raise SourceError(f"JSON 파싱 실패 ({e}) — {url}")


def normalize_string(s):
    if not s:
        return ""
    return re.sub(r'[^a-zA-Z0-9가-힣]', '', s).lower()


# 네이티브 / 크로스플랫폼 트랙은 시장이 다르다. 페이지에서 나눠 보여주려고 분류한다.
def classify_track(title):
    t = (title or '').lower()
    if 'flutter' in t or '플러터' in t or 'dart' in t:
        return 'Flutter'
    if 'react native' in t or 'react-native' in t or '리액트 네이티브' in t:
        return 'React Native'
    if 'android' in t or '안드로이드' in t:
        return 'Android'
    if 'ios' in t or '아이폰' in t or 'swift' in t:
        return 'iOS'
    return '기타 모바일'


# 모바일 직군만 남기기 위한 판별. 화이트리스트 우선, 그다음 블랙리스트.
MOBILE_KEYWORDS = (
    'android', '안드로이드', 'ios', '아이폰', 'flutter', '플러터', 'dart',
    'mobile', '모바일', 'react native', 'kotlin', 'swift', 'app', '앱',
)

NON_MOBILE_KEYWORDS = (
    'backend', '백엔드', 'back-end', 'server', '서버', 'data', '데이터',
    'ml', '머신러닝', 'machine learning', 'frontend', '프론트엔드', 'front-end',
    'web', '웹', 'devops', '데브옵스', 'infra', '인프라', 'sre', 'qa',
    'security', '보안', 'designer', '디자이너', 'pm', '기획',
)


def looks_mobile(title):
    t = (title or '').lower()
    if not any(k in t for k in MOBILE_KEYWORDS):
        return False
    # "웹 프론트엔드 (React Native 우대)" 같은 건 걸러낸다.
    # 단 모바일 키워드가 제목 앞쪽에 있으면 모바일 직군으로 본다.
    for bad in NON_MOBILE_KEYWORDS:
        if bad in t:
            first_mobile = min(
                (t.index(k) for k in MOBILE_KEYWORDS if k in t), default=len(t)
            )
            if t.index(bad) < first_mobile:
                return False
    return True


def iso_to_stamp(value):
    """ATS가 주는 ISO8601을 jobs.json이 쓰는 문자열 포맷으로 바꾼다."""
    if not value:
        return None
    try:
        cleaned = str(value).replace('Z', '+00:00')
        dt = datetime.datetime.fromisoformat(cleaned)
        if dt.tzinfo is not None:
            dt = dt.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return None


def epoch_ms_to_stamp(value):
    """Lever가 주는 epoch 밀리초를 같은 문자열 포맷으로 바꾼다."""
    if not isinstance(value, (int, float)) or value <= 0:
        return None
    try:
        dt = datetime.datetime.utcfromtimestamp(value / 1000.0)
    except (ValueError, OverflowError, OSError):
        return None
    return dt.strftime('%Y-%m-%d %H:%M:%S')


# ---------------------------------------------------------------- 소스: Greenhouse

# 공개 Job Board API를 쓰는 곳. 회사마다 함수를 새로 짤 필요가 없다.
# 여기 있는 토큰은 전부 실제로 200 + jobs 배열이 오는 것만 확인해서 넣었다.
#
# 확인해보고 뺀 것 (전부 404):
#   dunamu  — 두나무는 Greenhouse를 쓰지 않는다. dunamu.com/careers/jobs 자체 Next.js 사이트다.
#   karrotmarket, toss, tossbank, bucketplace, hyperconnect, banksalad
#           — 토큰이 존재하지 않는다. 토스는 자체 채용 사이트를 쓴다.
GREENHOUSE_BOARDS = {
    'coupang': '쿠팡',
    'daangn': '당근',
    'krafton': '크래프톤',
    'moloco': '몰로코',
    'sendbird': '센드버드',
}


def scrape_greenhouse(token, company):
    url = f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs"
    data = fetch_json(url)

    if 'jobs' not in data:
        raise SourceError(f"예상과 다른 응답 형태 (jobs 키 없음) — {url}")

    jobs = []
    for job in data['jobs']:
        title = job.get('title') or ''
        if not looks_mobile(title):
            continue
        jobs.append({
            'id': f"greenhouse_{token}_{job.get('id')}",
            'platform': 'Greenhouse',
            'title': title,
            'company': company,
            'job_url': job.get('absolute_url'),
            'tech_stack': 'Mobile',
            'track': classify_track(title),
            # ATS가 주는 실제 게시/갱신 시각. 이게 있어야 "우리가 처음 본 날"이 아닌
            # 진짜 신선도로 판정할 수 있다.
            'posted_at': iso_to_stamp(job.get('updated_at')),
        })
    return jobs


def greenhouse_sources():
    for token, company in GREENHOUSE_BOARDS.items():
        yield (
            f"Greenhouse:{token}",
            lambda t=token, c=company: scrape_greenhouse(t, c),
        )


# ---------------------------------------------------------------- 소스: Lever

# Lever도 키 없이 열려 있다. 응답은 dict 가 아니라 공고 배열이다.
# 국내 사용사를 훑어봤는데 실제로 200이 오는 곳은 네오위즈뿐이었다.
# (클래스101은 jobs.lever.co/class101 이 지금 404다. Lever에서 빠진 것으로 보인다.)
LEVER_ACCOUNTS = {
    'neowiz': '네오위즈',
}


def scrape_lever(token, company):
    url = f"https://api.lever.co/v0/postings/{token}?mode=json"
    data = fetch_json(url)

    # 계정이 사라지면 200이 아니라 {"ok": false} 가 오지만, 형태가 바뀌는 경우도
    # 여기서 걸러야 한다. 배열이 아니면 우리가 아는 응답이 아니다.
    if not isinstance(data, list):
        raise SourceError(f"예상과 다른 응답 형태 (배열이 아님) — {url}")

    jobs = []
    for posting in data:
        if not isinstance(posting, dict) or 'text' not in posting:
            raise SourceError(f"예상과 다른 공고 형태 (text 키 없음) — {url}")
        title = posting.get('text') or ''
        if not looks_mobile(title):
            continue
        jobs.append({
            'id': f"lever_{token}_{posting.get('id')}",
            'platform': 'Lever',
            'title': title,
            'company': company,
            'job_url': posting.get('hostedUrl'),
            'tech_stack': 'Mobile',
            'track': classify_track(title),
            # Lever의 createdAt 은 ISO8601이 아니라 epoch 밀리초다.
            'posted_at': epoch_ms_to_stamp(posting.get('createdAt')),
        })
    return jobs


def lever_sources():
    for token, company in LEVER_ACCOUNTS.items():
        yield (
            f"Lever:{token}",
            lambda t=token, c=company: scrape_lever(t, c),
        )


# ---------------------------------------------------------------- 소스: 그리팅

# 국내 표준 ATS(도입사 3,000곳 이상)라 파서 하나로 커버리지가 가장 크게 는다.
#
# 공식 Open API(oapi.greetinghr.com)는 쓸 수 없다. 채용하는 회사가 자기 워크스페이스에서
# 발급받는 키가 필수라, 남의 회사 공고를 모으는 용도로는 발급 자체가 불가능하다.
#
# 대신 공개 채용 홈은 Next.js SSR이고, 전체 공고 목록이 이미 응답 HTML의
# __NEXT_DATA__ 안에 react-query 캐시(queryKey ["openings"])로 직렬화되어 들어온다.
# 그래서 XHR을 흉내낼 필요 없이 홈 HTML 한 번만 받으면 된다.
#
# 다만 이건 비공식 내부 구조라 예고 없이 바뀔 수 있다. 그래서 아래 파서는
# __NEXT_DATA__ 가 없거나 openings 쿼리가 사라지면 반드시 SourceError 를 올린다.
# 조용히 빈 리스트를 돌려주면 안 된다.
GREETING_COMPANIES = {
    'musinsa': '무신사',
    'kakaomobility': '카카오모빌리티',
    '11st': '11번가',
    'buzzvil': '버즈빌',
    'cashwalk12': '넛지헬스케어(캐시워크)',
    'zigbang': '직방',
    'finda': '핀다',
    'megastudyedu': '메가스터디교육',
    'kstd-lezhin': '키다리스튜디오/레진',
    'xyz': '엑스와이지',
}

# 확인해보고 뺀 서브도메인 (전부 404): medibloc, socar, brandi-recruit, thesleepfactory.

NEXT_DATA_RE = re.compile(
    r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', re.S)


def extract_greetinghr_openings(html, url):
    """채용 홈 HTML에서 공고 목록을 꺼낸다. 형태가 다르면 SourceError."""
    match = NEXT_DATA_RE.search(html)
    if not match:
        raise SourceError(f"__NEXT_DATA__ 스크립트를 찾지 못했다 — {url}")

    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError as e:
        raise SourceError(f"__NEXT_DATA__ JSON 파싱 실패 ({e}) — {url}")

    queries = (data.get('props', {}).get('pageProps', {})
                   .get('dehydratedState', {}).get('queries'))
    if not isinstance(queries, list):
        raise SourceError(f"dehydratedState.queries 가 없다 — {url}")

    for query in queries:
        if query.get('queryKey') == ['openings']:
            openings = query.get('state', {}).get('data')
            # 공고가 0건인 회사는 정상이다. 리스트가 아닌 것만 실패로 본다.
            if not isinstance(openings, list):
                raise SourceError(f"openings 데이터가 배열이 아니다 — {url}")
            return openings

    raise SourceError(f'queryKey ["openings"] 쿼리가 사라졌다 — {url}')


def scrape_greetinghr(subdomain, company):
    url = f"https://{subdomain}.career.greetinghr.com/"
    openings = extract_greetinghr_openings(fetch_text(url), url)

    jobs = []
    for opening in openings:
        title = opening.get('title') or ''
        if not looks_mobile(title):
            continue
        opening_id = opening.get('openingId')
        if opening_id is None:
            raise SourceError(f"공고에 openingId 가 없다 — {url}")
        jobs.append({
            'id': f"greeting_{subdomain}_{opening_id}",
            'platform': '그리팅',
            'title': title,
            'company': company,
            'job_url': (f"https://{subdomain}.career.greetinghr.com"
                        f"/o/{opening_id}"),
            'tech_stack': 'Mobile',
            'track': classify_track(title),
            'posted_at': iso_to_stamp(opening.get('openDate')),
        })
    return jobs


def greetinghr_sources():
    for subdomain, company in GREETING_COMPANIES.items():
        yield (
            f"그리팅:{subdomain}",
            lambda s=subdomain, c=company: scrape_greetinghr(s, c),
        )


# ---------------------------------------------------------------- 소스: 원티드

WANTED_URL = (
    "https://www.wanted.co.kr/api/v4/jobs"
    "?country=kr&tag_type_ids=677&tag_type_ids=678&tag_type_ids=10110"
    "&job_sort=job.latest_order&locations=all&years=-1&limit=100"
)


def scrape_wanted():
    data = fetch_json(WANTED_URL)

    if 'data' not in data:
        raise SourceError("예상과 다른 응답 형태 (data 키 없음) — Wanted")

    jobs = []
    for job in data['data']:
        title = job.get('position') or ''
        if not looks_mobile(title):
            continue
        jobs.append({
            'id': f"wanted_{job.get('id')}",
            'platform': 'Wanted',
            'title': title,
            'company': (job.get('company') or {}).get('name'),
            'job_url': f"https://www.wanted.co.kr/wd/{job.get('id')}",
            'tech_stack': 'Mobile',
            'track': classify_track(title),
            'posted_at': None,  # 원티드 목록 API는 게시일을 주지 않는다
        })
    return jobs


# ---------------------------------------------------------------- 소스 등록

def build_sources():
    sources = list(greenhouse_sources())
    sources.extend(lever_sources())
    sources.extend(greetinghr_sources())
    sources.append(("Wanted", scrape_wanted))
    return sources


# ---------------------------------------------------------------- 저장

def is_duplicate(jobs, company, title):
    """같은 공고가 다른 플랫폼에 올라온 경우를 찾는다."""
    norm_title = normalize_string(title)
    if not norm_title:
        return None
    for job in jobs:
        if job.get('company') != company:
            continue
        norm_existing = normalize_string(job.get('title'))
        if not norm_existing:
            continue
        if norm_title in norm_existing or norm_existing in norm_title:
            return job['id'], job.get('platform', '')
    return None


def load_jobs():
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_jobs(new_jobs_list):
    jobs = load_jobs()
    by_id = {job['id']: job for job in jobs}

    new_count = 0
    updated_count = 0
    now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    for new_job in new_jobs_list:
        existing = by_id.get(new_job['id'])

        if existing is None:
            dup = is_duplicate(jobs, new_job.get('company'), new_job.get('title'))
            if dup:
                dup_id, existing_platform = dup
                existing = by_id.get(dup_id)
                if existing and new_job['platform'] not in existing_platform:
                    existing['platform'] = f"{existing_platform}, {new_job['platform']}"

        if existing is not None:
            existing['last_seen_at'] = now
            # 뒤늦게 게시일을 알게 된 경우 채워 넣는다.
            if new_job.get('posted_at') and not existing.get('posted_at'):
                existing['posted_at'] = new_job['posted_at']
            if new_job.get('track') and not existing.get('track'):
                existing['track'] = new_job['track']
            updated_count += 1
            continue

        new_job['created_at'] = now
        new_job['last_seen_at'] = now
        new_job.setdefault('tech_stack', 'Mobile')
        jobs.append(new_job)
        by_id[new_job['id']] = new_job
        new_count += 1

    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)

    return new_count, updated_count


# ---------------------------------------------------------------- 실행

def collect(sources):
    """모든 소스를 돌리고 (공고, 소스별 건수, 실패목록)을 돌려준다."""
    all_jobs = []
    per_source = {}
    failures = []

    for name, fn in sources:
        try:
            jobs = fn()
        except SourceError as e:
            failures.append((name, str(e)))
            print(f"  ✗ {name}: {e}", file=sys.stderr)
            continue
        per_source[name] = len(jobs)
        all_jobs.extend(jobs)
        print(f"  ✓ {name}: {len(jobs)}건")

    return all_jobs, per_source, failures


def main():
    sources = build_sources()
    print(f"소스 {len(sources)}개에서 수집 시작")

    all_jobs, per_source, failures = collect(sources)

    print(f"\n수집 {len(all_jobs)}건 "
          f"(소스 {len(per_source)}/{len(sources)} 성공)")

    if failures:
        print(f"실패한 소스 {len(failures)}개:", file=sys.stderr)
        for name, err in failures:
            print(f"  - {name}: {err}", file=sys.stderr)

    # 여기가 핵심이다. 0건이면 성공으로 끝내지 않는다.
    if not all_jobs:
        print("\n수집 결과가 0건이다. 모든 소스가 실패했거나 응답 형태가 바뀌었다.",
              file=sys.stderr)
        return 1

    new_count, updated_count = save_jobs(all_jobs)
    print(f"신규 {new_count}건 · 기존 갱신 {updated_count}건")

    # 일부만 실패한 경우도 알린다. 나머지 소스로 페이지는 갱신되지만
    # 실패를 눈에 띄게 남겨야 다음 주에 또 조용히 넘어가지 않는다.
    if failures:
        print(f"\n{len(failures)}개 소스가 실패한 채로 완료됐다.", file=sys.stderr)
        return 2

    return 0


if __name__ == '__main__':
    sys.exit(main())
