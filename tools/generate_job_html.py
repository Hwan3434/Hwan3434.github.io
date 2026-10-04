"""jobs.json 을 읽어 비밀번호로 잠긴 jobs.html 을 만든다.

페이지에는 지금 열린 공고뿐 아니라 지금까지 수집한 공고가 모두 쌓인다.
각 공고에는 그 회사에 지원했던 이력을 붙인다. 지원 이력은 개인 정보라서
레포에 두지 않고 배포 시점에 환경변수(JOBS_APPLIED)로만 받는다.

블로그는 공개 정적 사이트라 서버에서 막을 방법이 없다. 그래서 공고 데이터와
지원 이력을 비밀번호로 암호화해 넣고, 브라우저가 비밀번호를 받아 푼다.
페이지 틀(tools/jobs_page.html)에는 데이터가 들어 있지 않다.

    JOBS_PAGE_PASSWORD  페이지 비밀번호. 없으면 DEFAULT_PASSWORD
    JOBS_APPLIED        지원 이력 JSON. 없으면 tools/applied.local.json, 그것도 없으면 빈 목록
"""

import base64
import datetime
import hashlib
import hmac
import json
import os
import re
import zlib

import job_scraper

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(TOOLS_DIR, 'jobs.json')
TEMPLATE_PATH = os.path.join(TOOLS_DIR, 'jobs_page.html')
LOCAL_APPLIED_PATH = os.path.join(TOOLS_DIR, 'applied.local.json')
# 회사 → 공식 도메인. 페이지가 이 도메인의 파비콘을 로고로 띄운다. 없는 회사는 이니셜로 나온다.
DOMAINS_PATH = os.path.join(TOOLS_DIR, 'company_domains.json')
# 사용자 PC 의 Aside 브라우저로 2026-10-04 하루 모은 공고(단발성). 수집기가 다시 보지
# 못하므로 모은 날을 첫 수집·마지막 확인 시각으로 둔다. 매주 덮어쓰는 jobs.json 과는 따로 둔다.
ASIDE_PATH = os.path.join(TOOLS_DIR, 'jobs_aside.json')
ASIDE_SEEN_AT = '2026-10-04 03:00:00'
ASIDE_YEAR, ASIDE_MONTH = 2026, 10
OUTPUT_PATH = os.path.join(TOOLS_DIR, '..', 'jobs.html')
VAULT_TOKEN = '__JOBS_VAULT__'

# 임시 비밀번호다. 저장소 Secret JOBS_PAGE_PASSWORD 를 넣으면 그 값을 쓴다.
DEFAULT_PASSWORD = '1234'

# 브라우저가 비밀번호를 한 번 확인하는 데 드는 비용이다. 대입 공격을 늦추는 용도다.
KDF_ITERATIONS = 200_000

# 수집은 주 1회(월요일) 돈다. 활성 판정 창을 24시간으로 두면 한 소스가 실패한 주에
# 그 소스의 공고가 통째로 마감으로 바뀐다. 한 주 + 여유로 잡는다.
ACTIVE_WINDOW_DAYS = 8

KST = datetime.timezone(datetime.timedelta(hours=9))

LEGAL_NAME_RE = re.compile(r'\(주\)|㈜|주식회사')
KEY_STRIP_RE = re.compile(r"[\s.\-·,&'’/]")
PAREN_RE = re.compile(r'\((.*?)\)')
TITLE_TAG_RE = re.compile(r'\[(.*?)\]')
LEADING_TAGS_RE = re.compile(r'^\s*(\[[^\]]*\]\s*)+')
DOMAIN_RE = re.compile(r'^[a-z0-9-]+(\.[a-z0-9-]+)+$')
# 지원 결과가 이 말을 담으면 그 회사에서 떨어진 것으로 본다.
REJECTED_RE = re.compile(r'불합격|탈락')
# 경력 표기. 공백을 지운 뒤에 맞춘다. '3년~8년 미만', '5년차 이상', '경력3년↑', '35년 이하'.
CAREER_RANGE_RE = re.compile(r'(\d{1,2})년?차?[~\-](\d{1,2})년차?(미만)?')
CAREER_MIN_RE = re.compile(r'(\d{1,2})년차?(?:↑|이상|~|\+)')
CAREER_MAX_RE = re.compile(r'(\d{1,2})년차?이하')
CAREER_YEARS_RE = re.compile(r'경력(\d{1,2})년')


def parse_stamp(value):
    if not value:
        return None
    try:
        return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return None


def load_jobs(db_path=DB_PATH):
    if not os.path.exists(db_path):
        return []
    with open(db_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_applied():
    raw = os.environ.get('JOBS_APPLIED', '').strip()
    if not raw and os.path.exists(LOCAL_APPLIED_PATH):
        with open(LOCAL_APPLIED_PATH, 'r', encoding='utf-8') as f:
            raw = f.read()
    if not raw:
        return []
    # 형식이 깨졌으면 조용히 빈 목록으로 넘어가지 않는다. 표시가 통째로 사라진다.
    entries = json.loads(raw)
    if not isinstance(entries, list):
        raise ValueError('지원 이력은 JSON 배열이어야 한다')
    return entries


# ---------------------------------------------------------------- 회사명 매칭

def display_company(name):
    return LEGAL_NAME_RE.sub('', name or '').strip()


def company_keys(name):
    """회사명을 비교용 키 집합으로 바꾼다.

    법인 표기와 공백·구두점을 지우고, 괄호 안 브랜드명은 따로 키로 본다.
    '넛지헬스케어(캐시워크)' → {'넛지헬스케어', '캐시워크'}
    부분 문자열로는 비교하지 않는다. '카카오'가 '카카오모빌리티'에 붙으면 안 된다.
    """
    text = LEGAL_NAME_RE.sub('', name or '')
    parts = [PAREN_RE.sub('', text)] + PAREN_RE.findall(text)
    keys = set()
    for part in parts:
        key = KEY_STRIP_RE.sub('', part).lower()
        if key:
            keys.add(key)
    return keys


def posting_keys(job):
    """회사명에 더해 제목 앞의 [브랜드] 표기도 키로 쓴다. '[TADA] Android Engineer'."""
    keys = company_keys(job.get('company'))
    for tag in TITLE_TAG_RE.findall(job.get('title') or ''):
        keys |= company_keys(tag)
    return keys


def entry_keys(entry):
    keys = company_keys(entry.get('company'))
    for alias in entry.get('aliases') or []:
        keys |= company_keys(alias)
    return keys


def match_history(job, applied):
    keys = posting_keys(job)
    return [entry for entry in applied if keys & entry_keys(entry)]


def history_label(company, entries):
    """'2025 · 2022 불합격'처럼 짧게 쓴다. 결과가 서로 다르면 연도마다 붙인다.

    공고 회사명이 아니라 브랜드로 맞은 이력은 어느 이름으로 지원했는지 괄호로 남긴다.
    """
    own = company_keys(company)
    entries = sorted(entries, key=lambda e: str(e.get('date', '')), reverse=True)

    def when(entry):
        year = str(entry.get('date', ''))[:4]
        if not company_keys(entry.get('company')) & own:
            year += f"({PAREN_RE.sub('', display_company(entry.get('company')))})"
        return year

    def joined(labels):
        # 같은 해에 여러 번 냈으면 '2024×3'으로 묶는다.
        counts = {}
        for label in labels:
            counts[label] = counts.get(label, 0) + 1
        return ' · '.join(label if n == 1 else f'{label}×{n}' for label, n in counts.items())

    results = [str(entry.get('result', '')) for entry in entries]
    if len(set(results)) == 1:
        return joined(when(e) for e in entries) + ' ' + results[0]
    return joined(f'{when(e)} {r}' for e, r in zip(entries, results))


def is_rejected(entries):
    return any(REJECTED_RE.search(str(entry.get('result', ''))) for entry in entries)


# ---------------------------------------------------------------- 경력

def parse_career(text):
    """경력 표기를 [최소, 최대] 연차로 바꾼다. 최대가 없으면 None. 읽을 수 없으면 None.

    '경력 3-7년' → [3, 7], '경력5년↑' → [5, None], '신입' → [0, 0], '경력무관' → [0, None].
    '미들', '경력'처럼 연차가 없는 표기는 모른다고 본다.
    """
    t = re.sub(r'\s', '', str(text or ''))
    found = CAREER_RANGE_RE.search(t)
    if found:
        low, high = int(found.group(1)), int(found.group(2))
        return [low, high - 1 if found.group(3) else high]
    found = CAREER_MIN_RE.search(t)
    if found:
        return [int(found.group(1)), None]
    found = CAREER_MAX_RE.search(t)
    if found:
        return [0, int(found.group(1))]
    if '무관' in t or '경력전체' in t or ('신입' in t and '경력' in t and not CAREER_YEARS_RE.search(t)):
        return [0, None]
    if '신입' in t or '인턴' in t:
        found = CAREER_YEARS_RE.search(t)
        return [0, int(found.group(1)) if found else 0]
    found = CAREER_YEARS_RE.search(t)
    if found:
        return [int(found.group(1)), None]
    return None


def career_range(career, title):
    """경력 칸을 먼저 보고, 없거나 읽을 수 없으면 제목의 '(5년 이상)' 같은 표기를 본다."""
    return parse_career(career) or parse_career(title)


def history_detail(entries):
    lines = []
    for entry in sorted(entries, key=lambda e: str(e.get('date', '')), reverse=True):
        line = f"{entry.get('date', '')} {entry.get('company', '')} {entry.get('result', '')}"
        if entry.get('position'):
            line += f" — {entry['position']}"
        lines.append(line.strip())
    return '\n'.join(lines)


def load_domains(path=DOMAINS_PATH):
    """회사명 키 → 도메인. 표기가 달라도('쿠팡 (Coupang)') 같은 키로 찾는다."""
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        raw = json.load(f)
    domains = {}
    for name, domain in raw.items():
        domain = (domain or '').strip().lower()
        if not DOMAIN_RE.match(domain):
            raise ValueError(f'{path}: {name} 의 도메인 형식이 이상하다: {domain!r}')
        for key in company_keys(name):
            domains[key] = domain
    return domains


def company_domain(company, domains):
    for key in sorted(company_keys(company)):
        if key in domains:
            return domains[key]
    return ''


# ---------------------------------------------------------------- 행 만들기

# 같은 플랫폼이 소스마다 다른 이름으로 들어온다. 화면에는 한 이름으로 쓴다.
PLATFORM_NAMES = {'Wanted': '원티드', 'Coupang': '쿠팡', '직행(Zighang)': '직행', '고용24(워크넷)': '고용24'}


def split_platforms(value):
    """중복 병합된 공고는 platform 이 '그리팅, 점핏'처럼 합쳐져 있다."""
    seen = []
    for part in (value or '').split(','):
        part = PLATFORM_NAMES.get(part.strip(), part.strip())
        if part and part not in seen:
            seen.append(part)
    return seen


def safe_url(url):
    url = (url or '').strip()
    return url if url.startswith(('https://', 'http://')) else ''


def latest_run(jobs):
    stamps = [parse_stamp(j.get('last_seen_at')) for j in jobs]
    stamps = [s for s in stamps if s]
    return max(stamps) if stamps else None


def aside_deadline(value):
    """Aside 수집분의 마감일. '2026-10-15', '10/09(금)' 을 읽는다. '상시'·'채용시마감'·'없음'은 상시."""
    text = str(value or '').strip()
    found = re.match(r'^(\d{1,2})/(\d{1,2})', text)
    if found:
        month, day = int(found.group(1)), int(found.group(2))
        # 2026-10-04 에 모은 목록이라 그보다 앞선 달은 해를 넘긴 마감이다.
        year = ASIDE_YEAR if month >= ASIDE_MONTH else ASIDE_YEAR + 1
        try:
            return datetime.date(year, month, day).strftime('%Y-%m-%d')
        except ValueError:
            return None
    return job_scraper.deadline_date(text) if re.match(r'^\d{4}-\d{2}-\d{2}', text) else None


def from_aside(record):
    """Aside 레코드를 jobs.json 레코드 모양으로 맞춘다."""
    job = dict(record)
    job['created_at'] = job['last_seen_at'] = ASIDE_SEEN_AT
    job['posted_at'] = f"{record['posted_at']} 00:00:00" if record.get('posted_at') else None
    job['deadline_at'] = aside_deadline(record.get('deadline'))
    return job


def title_keys(title):
    """중복 판정용 제목 키. 앞의 [브랜드] 꼬리표만 다른 것은 같은 공고로 본다.

    포함 관계로는 묶지 않는다. 'Software Engineer, Android' 와 그 '(인턴)' 공고,
    스쿨버스 경력/신입 공고처럼 서로 다른 공고가 한데 묶인다.
    """
    full = job_scraper.normalize_string(title)
    bare = job_scraper.normalize_string(LEADING_TAGS_RE.sub('', title or ''))
    return {key for key in (full, bare) if key}


def dedupe(rows):
    """회사가 같고 제목 키가 겹치는 공고를 하나로 합친다. 여러 플랫폼에 올라온 같은 공고다."""
    parent = list(range(len(rows)))

    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    by_company = {}
    for i, row in enumerate(rows):
        for key in row['_ck']:
            by_company.setdefault(key, []).append(i)
    for members in by_company.values():
        for x, i in enumerate(members):
            for k in members[x + 1:]:
                if rows[i]['_tk'] & rows[k]['_tk']:
                    parent[root(i)] = root(k)

    groups = {}
    for i, row in enumerate(rows):
        groups.setdefault(root(i), []).append(row)

    merged = []
    for group in groups.values():
        # 열린 것, 수집기가 매주 확인하는 것, 먼저 본 것 순으로 대표를 고른다.
        group.sort(key=lambda r: (not r['a'], r['_aside'], r['c']))
        row = dict(group[0])
        platforms = []
        for other in group:
            for name in other['p'].split(' · '):
                if name and name not in platforms:
                    platforms.append(name)
        row['p'] = ' · '.join(platforms)
        row['a'] = any(r['a'] for r in group)
        row['c'] = min(r['c'] for r in group)
        row['ls'] = max(r['ls'] for r in group)
        for field in ('dl', 'po', 'cr', 'lo', 'u'):
            row[field] = next((r[field] for r in group if r[field]), '')
        merged.append(row)
    return merged


def build_rows(jobs, applied, now, domains=None, extra=()):
    """페이지에 실을 공고 행을 만든다. 열린 공고가 먼저, 그다음 마감된 공고.

    extra 는 Aside 로 따로 모은 공고다. 사람이 골라 모은 것이라 모바일 판별을 다시 하지 않는다.
    """
    active_cutoff = now - datetime.timedelta(days=ACTIVE_WINDOW_DAYS)
    domains = domains or {}

    rows = []
    for job, curated in [(j, False) for j in jobs] + [(from_aside(j), True) for j in extra]:
        title = (job.get('title') or '').strip()
        # 예전 규칙으로 들어온 비모바일 공고가 jobs.json 에 남아 있다. 지금 규칙으로 다시 거른다.
        if not curated and not job_scraper.looks_mobile(title):
            continue
        if not job_scraper.in_capital_area(job.get('location'), title):
            continue
        last_seen = parse_stamp(job.get('last_seen_at'))
        created = parse_stamp(job.get('created_at'))
        posted = parse_stamp(job.get('posted_at'))
        if not last_seen or not created:
            continue

        history = match_history(job, applied)
        rows.append({
            't': title,
            'co': display_company(job.get('company')),
            'd': company_domain(job.get('company'), domains),
            'tr': job.get('track') or job_scraper.classify_track(title),
            'p': ' · '.join(split_platforms(job.get('platform'))),
            'u': safe_url(job.get('job_url')),
            'po': posted.strftime('%Y-%m-%d') if posted else '',
            'c': created.strftime('%Y-%m-%d'),
            'ls': last_seen.strftime('%Y-%m-%d'),
            'a': last_seen > active_cutoff,
            'dl': job.get('deadline_at') or '',
            'cr': clean_text(job.get('career')),
            'lo': clean_text(job.get('location')),
            'h': history_label(job.get('company'), history) if history else '',
            'hd': history_detail(history) if history else '',
            'rj': is_rejected(history),
            '_ck': company_keys(job.get('company')),
            '_tk': title_keys(title),
            '_aside': curated,
        })

    rows = dedupe(rows)
    for row in rows:
        for key in ('_ck', '_tk', '_aside'):
            del row[key]
        # 합친 뒤에 계산한다. 경력 칸은 묶인 공고 중 처음 채워진 것을 쓴다.
        row['cy'] = career_range(row['cr'], row['t'])

    active = [r for r in rows if r['a']]
    closed = [r for r in rows if not r['a']]
    active.sort(key=lambda r: (r['c'], r['po']), reverse=True)
    closed.sort(key=lambda r: (r['ls'], r['c']), reverse=True)
    return active + closed


def clean_text(value):
    text = str(value or '').strip()
    return '' if text in ('', '없음', 'None') else text


def load_aside(path=ASIDE_PATH):
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def build_payload(jobs, applied, now, extra=()):
    run = latest_run(jobs)
    updated = (run.replace(tzinfo=datetime.timezone.utc).astimezone(KST)
               if run else None)
    return {
        'updated': updated.strftime('%Y-%m-%d %H:%M') if updated else '',
        'week': updated.isocalendar()[1] if updated else 0,
        'rows': build_rows(jobs, applied, now, load_domains(), extra),
    }


# ---------------------------------------------------------------- 잠금

def _derive_keys(password, salt, iterations):
    keys = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations, dklen=64)
    return keys[:32], keys[32:]


def _xor_keystream(key, nonce, data):
    """HMAC-SHA256 을 카운터 모드로 돌린 키스트림과 XOR 한다.

    표준 라이브러리에 AES 가 없어서 쓰는 구성이다. 브라우저는 WebCrypto 의 HMAC 으로
    같은 키스트림을 만든다. 무결성은 별도 MAC 키로 따로 확인한다(encrypt-then-MAC).
    """
    out = bytearray(len(data))
    for offset in range(0, len(data), 32):
        counter = (offset // 32).to_bytes(4, 'big')
        stream = hmac.new(key, nonce + counter, hashlib.sha256).digest()
        chunk = data[offset:offset + 32]
        out[offset:offset + len(chunk)] = bytes(a ^ b for a, b in zip(chunk, stream))
    return bytes(out)


def lock(plaintext, password, iterations=KDF_ITERATIONS):
    salt = os.urandom(16)
    nonce = os.urandom(16)
    enc_key, mac_key = _derive_keys(password, salt, iterations)
    ciphertext = _xor_keystream(enc_key, nonce, zlib.compress(plaintext, 9))
    tag = hmac.new(mac_key, salt + nonce + ciphertext, hashlib.sha256).digest()
    b64 = lambda b: base64.b64encode(b).decode('ascii')
    return {'v': 1, 'iter': iterations, 'salt': b64(salt), 'nonce': b64(nonce),
            'ct': b64(ciphertext), 'tag': b64(tag)}


def unlock(vault, password):
    """lock 의 역. 브라우저 쪽 구현과 같은 일을 한다. 테스트에서 쓴다."""
    raw = {k: base64.b64decode(vault[k]) for k in ('salt', 'nonce', 'ct', 'tag')}
    enc_key, mac_key = _derive_keys(password, raw['salt'], vault['iter'])
    expected = hmac.new(mac_key, raw['salt'] + raw['nonce'] + raw['ct'], hashlib.sha256).digest()
    if not hmac.compare_digest(expected, raw['tag']):
        raise ValueError('비밀번호가 맞지 않는다')
    return zlib.decompress(_xor_keystream(enc_key, raw['nonce'], raw['ct']))


def render_page(vault):
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = f.read()
    if VAULT_TOKEN not in template:
        raise ValueError(f'{TEMPLATE_PATH} 에 {VAULT_TOKEN} 자리가 없다')
    return template.replace(VAULT_TOKEN, json.dumps(vault).replace('</', '<\\/'))


def generate_html(output_path=OUTPUT_PATH, password=None, applied=None, now=None,
                  db_path=DB_PATH, aside_path=ASIDE_PATH):
    password = password or os.environ.get('JOBS_PAGE_PASSWORD', '').strip() or DEFAULT_PASSWORD
    applied = load_applied() if applied is None else applied
    now = now or datetime.datetime.utcnow()

    payload = build_payload(load_jobs(db_path), applied, now, load_aside(aside_path))
    plaintext = json.dumps(payload, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    html = render_page(lock(plaintext, password))

    with open(os.path.abspath(output_path), 'w', encoding='utf-8') as f:
        f.write(html)

    rows = payload['rows']
    print(f"jobs.html 생성 완료 — 공고 {len(rows)}건 "
          f"(열림 {sum(r['a'] for r in rows)} · 지원이력 {sum(bool(r['h']) for r in rows)})")
    if password == DEFAULT_PASSWORD:
        print('경고: 임시 비밀번호로 잠갔다. Secret JOBS_PAGE_PASSWORD 를 넣을 것.')


if __name__ == "__main__":
    generate_html()
