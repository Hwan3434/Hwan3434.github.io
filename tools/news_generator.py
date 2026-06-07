import urllib.request
import urllib.parse
import datetime
import os
import feedparser
from google import genai
import datetime
import os
from google import genai
from google.genai import types

def fetch_tech_feeds():
    feeds = [
        "https://developer.apple.com/news/rss/news.rss",  # Apple Developer
        "https://developers.googleblog.com/feeds/posts/default?alt=rss", # Google Developers
        "https://hnrss.org/frontpage?points=100", # Hacker News Top
        "https://openai.com/news/rss.xml", # OpenAI News
        "https://medium.com/feed/flutter" # Flutter
    ]
    
    items = []
    now = datetime.datetime.now(datetime.timezone.utc)
    
    for url in feeds:
        try:
            parsed = feedparser.parse(url)
            for entry in parsed.entries[:3]: # Top 3 per source
                pub_date = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    pub_date = datetime.datetime(*entry.published_parsed[:6], tzinfo=datetime.timezone.utc)
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    pub_date = datetime.datetime(*entry.updated_parsed[:6], tzinfo=datetime.timezone.utc)
                    
                if pub_date and (now - pub_date).total_seconds() > 86400 * 3:
                    continue # Skip items older than 3 days
                
                title = entry.title if hasattr(entry, 'title') else ''
                link = entry.link if hasattr(entry, 'link') else ''
                desc = entry.description if hasattr(entry, 'description') else (entry.summary if hasattr(entry, 'summary') else '')
                items.append({'title': title, 'link': link, 'description': desc})
        except Exception as e:
            print(f"Failed to fetch feed {url}: {e}")
            
    return items

def generate_markdown(news_items):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY is not set.")
        return None
        
    client = genai.Client(api_key=api_key)
    
    now_date = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y년 %m월 %d일")
    prompt = f"다음은 오늘({now_date}) 수집된 주요 최신 테크 뉴스 기사들입니다. 일반적인 경제/기업 주가 관련 뉴스는 철저히 제외하고, **오직 순수 개발자 관점(Google I/O, WWDC, Flutter, 오픈소스, AI 기술 및 모델 연구 등)**에서 흥미로울 만한 핵심 뉴스들만 엄선하여 마크다운 포맷의 블로그 포스트를 작성해주세요.\n"
    prompt += "수집된 각 뉴스 항목의 끝에는 반드시 원본 기사의 링크(Source URL)를 달아주세요. (형식: `[Source URL](링크) (언론사)`)\n"
    prompt += "제목 크기는 h3(###)을 권장하며, 기술적 깊이가 있는 요약을 제공해주세요.\n\n"
    
    for idx, item in enumerate(news_items):
        prompt += f"기사 {idx+1}. 제목: {item['title']}\n링크: {item['link']}\n내용: {item['description'][:500]}...\n\n"
        
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"Gemini API generation failed: {e}")
        return None

def translate_to_english(client, korean_markdown):
    prompt = "Translate the following Korean markdown blog post into professional, natural English. Keep the markdown formatting, headers, and links exactly the same.\n\n" + korean_markdown
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"Gemini API translation failed: {e}")
        return None

def main():
    items = fetch_tech_feeds()
    if not items:
        print("No news items found.")
        return
        
    content_ko = generate_markdown(items)
    if not content_ko:
        print("Failed to generate markdown content.")
        return
        
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    content_en = translate_to_english(client, content_ko)
        
    KST = datetime.timezone(datetime.timedelta(hours=9))
    now = datetime.datetime.now(KST)
    date_str = now.strftime("%Y-%m-%d")
    
    frontmatter_ko = f"""---
layout: post
title: "데일리 테크 뉴스 - {date_str}"
date: {now.strftime("%Y-%m-%d %H:%M:%S")} +0900
categories: [news]
tags: [Developer, AI, Daily]
---

"""

    frontmatter_en = f"""---
layout: post
title: "Daily Tech News - {date_str}"
date: {now.strftime("%Y-%m-%d %H:%M:%S")} +0900
categories: [news]
tags: [Developer, AI, Daily]
---

"""
    
    # Save Korean Version
    out_dir_ko = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '_posts', 'news'))
    os.makedirs(out_dir_ko, exist_ok=True)
    out_path_ko = os.path.join(out_dir_ko, f"{date_str}-daily-tech-news.md")
    
    with open(out_path_ko, 'w', encoding='utf-8') as f:
        f.write(frontmatter_ko + content_ko)
    print(f"Successfully wrote {out_path_ko}")

    # Save English Version
    if content_en:
        out_dir_en = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '_posts', 'en', 'news'))
        os.makedirs(out_dir_en, exist_ok=True)
        out_path_en = os.path.join(out_dir_en, f"{date_str}-daily-tech-news.md")
        
        with open(out_path_en, 'w', encoding='utf-8') as f:
            f.write(frontmatter_en + content_en)
        print(f"Successfully wrote {out_path_en}")

if __name__ == "__main__":
    main()
