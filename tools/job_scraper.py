import json
import urllib.request
import re
import datetime
import os

def normalize_string(s):
    if not s:
        return ""
    s = re.sub(r'[^a-zA-Z0-9가-힣]', '', s)
    return s.lower()

def is_duplicate(jobs, company, title):
    norm_title = normalize_string(title)
    for job in jobs:
        if job['company'] == company:
            norm_existing = normalize_string(job['title'])
            if norm_title in norm_existing or norm_existing in norm_title:
                return job['id'], job['platform']
    return None

def save_jobs(new_jobs_list):
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'jobs.json'))
    
    if os.path.exists(db_path):
        with open(db_path, 'r', encoding='utf-8') as f:
            jobs = json.load(f)
    else:
        jobs = []

    new_jobs_count = 0
    updated_jobs_count = 0
    current_time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    for new_job in new_jobs_list:
        # 1. Check exact ID
        existing = next((j for j in jobs if j['id'] == new_job['id']), None)
        if existing:
            existing['last_seen_at'] = current_time
            updated_jobs_count += 1
            continue
            
        # 2. Cross platform similarity
        dup_info = is_duplicate(jobs, new_job['company'], new_job['title'])
        if dup_info:
            dup_id, existing_platform = dup_info
            
            existing = next((j for j in jobs if j['id'] == dup_id), None)
            if existing:
                if new_job['platform'] not in existing_platform:
                    existing['platform'] = f"{existing_platform}, {new_job['platform']}"
                existing['last_seen_at'] = current_time
                updated_jobs_count += 1
            continue
            
        # 3. New Job
        new_job['created_at'] = current_time
        new_job['last_seen_at'] = current_time
        if 'tech_stack' not in new_job:
            new_job['tech_stack'] = ''
        jobs.append(new_job)
        new_jobs_count += 1
            
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)

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
                
                # 블랙리스트 방식
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
