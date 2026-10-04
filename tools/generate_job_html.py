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
OUTPUT_PATH = os.path.join(TOOLS_DIR, '..', 'jobs.html')
VAULT_TOKEN = '__JOBS_VAULT__'

# 임시 비밀번호다. 저장소 Secret JOBS_PAGE_PASSWORD 를 넣으면 그 값을 쓴다.
DEFAULT_PASSWORD = '1234'

# 브라우저가 비밀번호를 한 번 확인하는 데 드는 비용이다. 대입 공격을 늦추는 용도다.
KDF_ITERATIONS = 200_000

# 수집은 주 1회(월요일) 돈다. 활성 판정 창을 24시간으로 두면 한 소스가 실패한 주에
# 그 소스의 공고가 통째로 마감으로 바뀐다. 한 주 + 여유로 잡는다.
ACTIVE_WINDOW_DAYS = 8

# 마지막 수집에서 처음 발견한 공고에만 신규 표시를 한다. 페이지는 배포 때마다
# 다시 만들어지므로 현재 시각이 아니라 마지막 수집 시각을 기준으로 잡는다.
NEW_WINDOW_HOURS = 6

KST = datetime.timezone(datetime.timedelta(hours=9))

LEGAL_NAME_RE = re.compile(r'\(주\)|㈜|주식회사')
KEY_STRIP_RE = re.compile(r"[\s.\-·,&'’/]")
PAREN_RE = re.compile(r'\((.*?)\)')
TITLE_TAG_RE = re.compile(r'\[(.*?)\]')


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


def history_detail(entries):
    lines = []
    for entry in sorted(entries, key=lambda e: str(e.get('date', '')), reverse=True):
        line = f"{entry.get('date', '')} {entry.get('company', '')} {entry.get('result', '')}"
        if entry.get('position'):
            line += f" — {entry['position']}"
        lines.append(line.strip())
    return '\n'.join(lines)


# ---------------------------------------------------------------- 행 만들기

def split_platforms(value):
    """중복 병합된 공고는 platform 이 '그리팅, 점핏'처럼 합쳐져 있다."""
    seen = []
    for part in (value or '').split(','):
        part = part.strip()
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


def build_rows(jobs, applied, now):
    """페이지에 실을 공고 행을 만든다. 열린 공고가 먼저, 그다음 마감된 공고."""
    run = latest_run(jobs)
    active_cutoff = now - datetime.timedelta(days=ACTIVE_WINDOW_DAYS)
    new_cutoff = run - datetime.timedelta(hours=NEW_WINDOW_HOURS) if run else None

    rows = []
    for job in jobs:
        title = (job.get('title') or '').strip()
        # 예전 규칙으로 들어온 비모바일 공고가 jobs.json 에 남아 있다. 지금 규칙으로 다시 거른다.
        if not job_scraper.looks_mobile(title):
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
            'tr': job.get('track') or job_scraper.classify_track(title),
            'p': ' · '.join(split_platforms(job.get('platform'))),
            'u': safe_url(job.get('job_url')),
            'po': posted.strftime('%Y-%m-%d') if posted else '',
            'c': created.strftime('%Y-%m-%d'),
            'ls': last_seen.strftime('%Y-%m-%d'),
            'a': last_seen > active_cutoff,
            'n': bool(new_cutoff and created >= new_cutoff),
            'h': history_label(job.get('company'), history) if history else '',
            'hd': history_detail(history) if history else '',
        })

    active = [r for r in rows if r['a']]
    closed = [r for r in rows if not r['a']]
    active.sort(key=lambda r: (r['c'], r['po']), reverse=True)
    closed.sort(key=lambda r: (r['ls'], r['c']), reverse=True)
    return active + closed


def build_payload(jobs, applied, now):
    run = latest_run(jobs)
    updated = (run.replace(tzinfo=datetime.timezone.utc).astimezone(KST)
               if run else None)
    return {
        'updated': updated.strftime('%Y-%m-%d %H:%M') if updated else '',
        'week': updated.isocalendar()[1] if updated else 0,
        'rows': build_rows(jobs, applied, now),
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
                  db_path=DB_PATH):
    password = password or os.environ.get('JOBS_PAGE_PASSWORD', '').strip() or DEFAULT_PASSWORD
    applied = load_applied() if applied is None else applied
    now = now or datetime.datetime.utcnow()

    payload = build_payload(load_jobs(db_path), applied, now)
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
