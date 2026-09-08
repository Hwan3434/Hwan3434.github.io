"""jobs.json 을 읽어 jobs.html 을 만든다.

트랙(Flutter / React Native / Android / iOS)을 나눠서 보여준다.
네이티브와 크로스플랫폼은 요구 스택도 채용 채널도 다른 시장이라
한 덩어리로 묶어두면 읽히지 않는다.
"""

import datetime
import html
import json
import os

# 수집은 주 1회(월요일) 돈다. 활성 판정 창을 24시간으로 두면 한 소스가 실패한 주에
# 그 소스의 공고가 통째로 페이지에서 사라진다. 한 주 + 여유로 잡는다.
ACTIVE_WINDOW_DAYS = 8

# 이번 실행에서 처음 발견한 공고에만 NEW를 붙인다.
NEW_WINDOW_HOURS = 24

TRACK_ORDER = ['Flutter', 'React Native', 'Android', 'iOS', '기타 모바일']
TRACK_ICONS = {
    'Flutter': '💙',
    'React Native': '⚛️',
    'Android': '💚',
    'iOS': '🍎',
    '기타 모바일': '📱',
}


def categorize_job(title):
    """track 필드가 없는 과거 데이터를 위한 폴백."""
    t = (title or '').lower()
    if 'flutter' in t or '플러터' in t:
        return 'Flutter'
    if 'react native' in t or '리액트 네이티브' in t:
        return 'React Native'
    if 'ios' in t or '아이폰' in t or 'mac' in t:
        return 'iOS'
    if 'android' in t or '안드로이드' in t:
        return 'Android'
    return '기타 모바일'


def parse_stamp(value):
    if not value:
        return None
    try:
        return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return None


def load_jobs(db_path):
    if not os.path.exists(db_path):
        return []
    with open(db_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def select_active(jobs, now):
    cutoff = now - datetime.timedelta(days=ACTIVE_WINDOW_DAYS)
    active = []
    for job in jobs:
        last_seen = parse_stamp(job.get('last_seen_at'))
        if last_seen and last_seen > cutoff:
            active.append(job)
    return active


def group_by_track(active, now):
    new_cutoff = now - datetime.timedelta(hours=NEW_WINDOW_HOURS)
    grouped = {track: [] for track in TRACK_ORDER}

    for job in active:
        track = job.get('track') or categorize_job(job.get('title'))
        if track not in grouped:
            track = '기타 모바일'

        created = parse_stamp(job.get('created_at'))
        posted = parse_stamp(job.get('posted_at'))

        grouped[track].append({
            'title': job.get('title') or '',
            'company': job.get('company') or '',
            'platform': job.get('platform') or '',
            'url': job.get('job_url') or '',
            'is_new': bool(created and created > new_cutoff),
            # ATS가 게시일을 준 경우에만 표시한다. 없으면 아무것도 쓰지 않는다.
            'posted': posted.strftime('%Y-%m-%d') if posted else None,
            'sort_key': posted or created or datetime.datetime.min,
        })

    for track in grouped:
        grouped[track].sort(key=lambda j: j['sort_key'], reverse=True)
    return grouped


def render_card(job):
    new_tag = '<span class="new-badge">NEW</span>' if job['is_new'] else ''
    posted = (f'<span class="posted">{job["posted"]} 게시</span>'
              if job['posted'] else '')
    title = html.escape(job['title'])
    company = html.escape(job['company'])
    platform = html.escape(job['platform'])
    url = html.escape(job['url'], quote=True)
    return f"""
            <div class="job-card">
                {new_tag}
                <h3 class="job-title" title="{title}">{title}</h3>
                <div class="company-name">{company}</div>
                <div class="job-footer">
                    <span class="platform-badge">{platform}</span>
                    {posted}
                    <a href="{url}" class="apply-btn" target="_blank" rel="noopener">지원하기 →</a>
                </div>
            </div>"""


def generate_html():
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'jobs.json'))
    jobs = load_jobs(db_path)

    now = datetime.datetime.utcnow()
    active = select_active(jobs, now)
    grouped = group_by_track(active, now)

    kst = datetime.timezone(datetime.timedelta(hours=9))
    now_kst = datetime.datetime.now(kst)
    today = now_kst.strftime('%Y-%m-%d')
    now_time = now_kst.strftime('%Y-%m-%d %H:%M')

    total = len(active)
    platforms = sorted({j.get('platform', '') for j in active if j.get('platform')})
    source_line = ' · '.join(platforms) if platforms else '수집 소스 없음'

    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>주간 모바일 채용 다이제스트 - {today}</title>
    <style>
        :root {{ --bg-color: #0d1117; --card-bg: #161b22; --text-main: #c9d1d9; --text-muted: #8b949e; --border: #30363d; }}
        body {{ background-color: var(--bg-color); color: var(--text-main); font-family: 'Inter', -apple-system, sans-serif; margin: 0; padding: 20px; line-height: 1.4; }}
        .container {{ width: 96%; max-width: 1800px; margin: 0 auto; }}
        .header {{ position: relative; text-align: left; margin-bottom: 30px; padding-bottom: 15px; border-bottom: 1px solid var(--border); }}
        .header h1 {{ font-size: 1.8rem; margin: 0; color: #ffffff; }}
        .last-updated {{ position: absolute; bottom: 15px; right: 0; color: var(--text-muted); font-size: 0.95rem; font-weight: 500; background: rgba(139, 148, 158, 0.1); padding: 6px 12px; border-radius: 6px; }}
        .section-title {{ font-size: 1.3rem; color: #58a6ff; margin: 40px 0 15px 0; display: flex; align-items: center; gap: 10px; border-bottom: 1px solid rgba(48, 54, 61, 0.5); padding-bottom: 8px; }}
        .job-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 12px; }}
        .job-card {{ background-color: var(--card-bg); border: 1px solid var(--border); border-radius: 6px; padding: 14px; display: flex; flex-direction: column; transition: border-color 0.2s; position: relative; }}
        .job-card:hover {{ border-color: #58a6ff; }}
        .job-title {{ font-size: 1rem; font-weight: 600; margin: 0 0 6px 0; color: #ffffff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; padding-right: 40px; }}
        .company-name {{ font-size: 0.85rem; color: #8b949e; margin-bottom: 12px; }}
        .job-footer {{ display: flex; justify-content: space-between; align-items: center; gap: 8px; margin-top: auto; flex-wrap: wrap; }}
        .platform-badge {{ background-color: rgba(139, 148, 158, 0.15); color: #c9d1d9; padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; }}
        .posted {{ color: var(--text-muted); font-size: 0.7rem; }}
        .apply-btn {{ color: #58a6ff; text-decoration: none; font-size: 0.8rem; font-weight: 600; margin-left: auto; }}
        .apply-btn:hover {{ text-decoration: underline; }}
        .new-badge {{ position: absolute; top: 12px; right: 14px; background: linear-gradient(90deg, #ff4d4f, #ff7875); color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.65rem; font-weight: bold; }}
        .empty {{ color: var(--text-muted); padding: 40px 0; }}
        .sources {{ color: var(--text-muted); font-size: 0.8rem; margin-top: 6px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>주간 모바일 채용 다이제스트 🚀</h1>
            <p style="color: var(--text-muted); margin-top: 5px; font-size: 0.95rem;">최근 {ACTIVE_WINDOW_DAYS}일 내 확인된 활성 공고 {total}건</p>
            <p class="sources">수집 소스: {html.escape(source_line)}</p>
            <div class="last-updated">⏱️ 최근 갱신: {now_time}</div>
        </div>
"""

    if not total:
        html_content += ('<p class="empty">활성 공고가 없습니다. '
                         '수집 파이프라인 로그를 확인하세요.</p>')

    for track in TRACK_ORDER:
        track_jobs = grouped[track]
        if not track_jobs:
            continue
        html_content += (
            f'<h2 class="section-title">{TRACK_ICONS[track]} {track} '
            f'<span style="color:var(--text-muted); font-size:0.9rem; margin-left:8px;">'
            f'{len(track_jobs)}건</span></h2><div class="job-grid">'
        )
        for job in track_jobs:
            html_content += render_card(job)
        html_content += "</div>"

    html_content += "</div></body></html>"

    output_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'jobs.html'))
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"jobs.html 생성 완료 — 활성 {total}건")
    for track in TRACK_ORDER:
        if grouped[track]:
            print(f"  {track}: {len(grouped[track])}건")


if __name__ == "__main__":
    generate_html()
