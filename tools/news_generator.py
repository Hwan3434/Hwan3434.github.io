import urllib.request
import xml.etree.ElementTree as ET
import datetime
import os
from google import genai
from google.genai import types

def fetch_geeknews_rss():
    url = "https://news.hada.io/rss"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read()
            root = ET.fromstring(data)
            items = []
            for item in root.findall('.//item')[:10]:
                title = item.find('title').text if item.find('title') is not None else ''
                link = item.find('link').text if item.find('link') is not None else ''
                desc = item.find('description').text if item.find('description') is not None else ''
                items.append({'title': title, 'link': link, 'description': desc})
            return items
    except Exception as e:
        print(f"Failed to fetch RSS: {e}")
        return []

def generate_markdown(news_items):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY is not set.")
        return None
        
    client = genai.Client(api_key=api_key)
    
    prompt = "다음은 오늘 수집된 주요 최신 테크 뉴스 기사들입니다. 중복되는 내용을 정리하고, 핵심 내용을 쉽게 요약하여 마크다운 포맷의 블로그 포스트를 작성해주세요.\n"
    prompt += "수집된 각 뉴스 항목의 끝에는 반드시 원본 기사의 링크(Source URL)를 달아주세요. 제목 크기는 h3(###)을 권장합니다.\n\n"
    
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

def main():
    items = fetch_geeknews_rss()
    if not items:
        print("No news items found.")
        return
        
    content = generate_markdown(items)
    if not content:
        print("Failed to generate markdown content.")
        return
        
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    
    frontmatter = f"""---
layout: post
title: "데일리 테크 뉴스 - {date_str}"
date: {now.strftime("%Y-%m-%d %H:%M:%S")} +0900
categories: [news]
tags: [AI, Tech, Daily]
---

"""
    final_content = frontmatter + content
    
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '_posts', 'news'))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{date_str}-daily-tech-news.md")
    
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
        
    print(f"Successfully wrote {out_path}")

if __name__ == "__main__":
    main()
