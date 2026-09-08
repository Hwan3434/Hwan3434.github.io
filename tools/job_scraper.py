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

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            body = response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        raise SourceError(f"HTTP {e.code} — {url}")
    except Exception as e:
        raise SourceError(f"{type(e).__name__}: {e} — {url}")

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


# ---------------------------------------------------------------- 소스: Greenhouse

# 공개 Job Board API를 쓰는 곳. 회사마다 함수를 새로 짤 필요가 없다.
# 여기 있는 토큰은 실제 채용 URL에서 확인된 것만 넣는다.
# 확인되지 않은 후보(당근, 토스, 오늘의집 등)는 job_id 포맷상 Greenhouse로
# 보이지만 board token을 확인하지 못해 넣지 않았다. 토큰을 확인하면 한 줄 추가하면 된다.
GREENHOUSE_BOARDS = {
    'coupang': '쿠팡',
    'dunamu': '두나무',
    'moloco': '몰로코',
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
    sources.append(("Wanted", scrape_wanted))
    return sources


# TODO(그리팅): 무신사·카카오모빌리티·11번가·야놀자·버즈빌·직방·메디블록·쏘카·
# 강남언니·브랜디·핀다 등이 모두 *.career.greetinghr.com 을 쓴다. 국내 표준 ATS라
# 파서 하나로 커버리지가 가장 크게 늘어난다. 다만 공개 API 스펙을 확인하지 못해
# 넣지 않았다. 추측으로 엔드포인트를 넣으면 조용히 0건을 수집하게 되므로,
# 채용 페이지를 열고 DevTools Network 탭에서 공고 목록 XHR을 확인한 뒤
# scrape_greenhouse 와 같은 형태로 추가할 것.


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
