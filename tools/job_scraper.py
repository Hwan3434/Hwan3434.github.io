import sqlite3
import json
import urllib.request
import re
import datetime

def normalize_string(s):
    if not s:
        return ""
    s = re.sub(r'[^a-zA-Z0-9가-힣]', '', s)
    return s.lower()

def is_duplicate(cursor, company, title):
    norm_title = normalize_string(title)
    cursor.execute("SELECT id, title, platform FROM jobs WHERE company = ?", (company,))
    for job_id, existing_title, existing_platform in cursor.fetchall():
        norm_existing = normalize_string(existing_title)
        if norm_title in norm_existing or norm_existing in norm_title:
            return job_id, existing_platform
    return None

def save_jobs(jobs):
    import os
    db_path = os.path.join(os.path.dirname(__file__), 'jobs.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    new_jobs_count = 0
    updated_jobs_count = 0
    
    current_time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    
    for job in jobs:
        # 1. 완전 동일 ID 검사 (생명 연장!)
        cursor.execute("SELECT id FROM jobs WHERE id = ?", (job['id'],))
        if cursor.fetchone():
            cursor.execute("UPDATE jobs SET last_seen_at = ? WHERE id = ?", (current_time, job['id']))
            updated_jobs_count += 1
            continue
            
        # 2. 크로스 플랫폼 유사도 검사 (생명 연장 + 배지 병합!)
        dup_info = is_duplicate(cursor, job['company'], job['title'])
        if dup_info:
            dup_id, existing_platform = dup_info
            new_platform = existing_platform
            if job['platform'] not in existing_platform:
                new_platform = f"{existing_platform}, {job['platform']}"
            cursor.execute("UPDATE jobs SET platform = ?, last_seen_at = ? WHERE id = ?", (new_platform, current_time, dup_id))
            updated_jobs_count += 1
            continue
            
        # 3. 완전 신규 공고!
        cursor.execute('''
        INSERT INTO jobs (id, platform, title, company, job_url, tech_stack, created_at, last_seen_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (job['id'], job['platform'], job['title'], job['company'], job['job_url'], job.get('tech_stack', ''), current_time, current_time))
        new_jobs_count += 1
            
    conn.commit()
    conn.close()
    return new_jobs_count, updated_jobs_count

def scrape_wanted():
    print("Fetching from Wanted API...")
    url = "https://www.wanted.co.kr/api/v4/jobs?country=kr&tag_type_ids=677&tag_type_ids=678&tag_type_ids=10110&job_sort=job.latest_order&locations=all&years=-1&limit=50"
    jobs = []
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            for job in data.get('data', []):
                title = job.get('position', '').lower()
                
                # 블랙리스트 방식: 확실히 모바일이 아닌 직무(백엔드, 서버, 데이터 등)만 걸러냄
                # 이렇게 하면 영어(App Developer 등)나 범용 타이틀(Software Engineer)을 놓치지 않음
                blacklist = ['backend', '백엔드', 'server', '서버', 'data', '데이터', 'ml', 'ai', '머신러닝', 'frontend', '프론트엔드', 'web', '웹', 'devops', '데브옵스', 'infra', '인프라']
                
                is_valid = True
                for bad_word in blacklist:
                    if bad_word in title:
                        is_valid = False
                        break
                        
                if is_valid:
                    jobs.append({
                        'id': f"wanted_{job.get('id')}",
                        'platform': 'Wanted',
                        'title': job.get('position'),
                        'company': job.get('company', {}).get('name'),
                        'job_url': f"https://www.wanted.co.kr/wd/{job.get('id')}",
                        'tech_stack': 'Mobile'
                    })
    except Exception as e:
        print(f"Wanted scraping failed: {e}")
    return jobs

def scrape_coupang():
    url = "https://boards-api.greenhouse.io/v1/boards/coupang/jobs"
    jobs = []
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            for job in data.get('jobs', []):
                title = job.get('title', '').lower()
                if 'android' in title or 'ios' in title or 'flutter' in title or 'mobile' in title:
                    jobs.append({
                        'id': f"coupang_{job.get('id')}",
                        'platform': 'Coupang',
                        'title': job.get('title'),
                        'company': '쿠팡 (Coupang)',
                        'job_url': job.get('absolute_url'),
                        'tech_stack': 'Mobile'
                    })
    except Exception as e:
        pass
    return jobs

if __name__ == '__main__':
    all_jobs = []
    all_jobs.extend(scrape_wanted())
    all_jobs.extend(scrape_coupang())
    
    new_count, update_count = save_jobs(all_jobs)
    print(f"🎉 Inserted {new_count} NEW jobs.")
    print(f"🔄 Updated (Last Seen) {update_count} existing active jobs.")
