# Daily Tech News Digest

You are running as a scheduled local Codex CLI job for this Jekyll blog repository.

Goal: create today's developer-focused daily tech news posts without using Gemini or `tools/news_generator.py`.

Hard constraints:
- Do not run `tools/news_generator.py`.
- Do not use `GEMINI_API_KEY` or any Gemini API.
- Do not modify unrelated files.
- Keep existing uncommitted user changes intact. If unrelated local changes exist, do not overwrite them.
- Use Asia/Seoul time for dates.

Task:
1. Inspect recent posts under `_posts/news/` and `_posts/en/news/` to match front matter and style.
2. Collect current developer-focused technology news from official RSS/news sources and reputable technical sources. Prioritize:
   - Apple Developer
   - Google Developers / Google AI Developers
   - Hacker News developer topics
   - OpenAI
   - Flutter
   - Woowahan Tech
   - Toss Tech
   - NAVER D2
   - Kakao Tech
   - Martin Fowler
   - Andrej Karpathy
   - Claude / Anthropic developer or research news
   - Gemini / Google DeepMind developer or research news
3. Exclude general stock-market, earnings, executive, and broad business news unless it has direct developer impact.
4. Write a Korean post to `_posts/news/YYYY-MM-DD-daily-tech-news.md`.
5. Write an English post to `_posts/en/news/YYYY-MM-DD-daily-tech-news.md`.
6. Each post must include Jekyll front matter:
   - `layout: post`
   - `title: "데일리 테크 뉴스 - YYYY-MM-DD"` for Korean
   - `title: "Daily Tech News - YYYY-MM-DD"` for English
   - `date: YYYY-MM-DD HH:MM:SS +0900`
   - `categories: [news]`
   - `tags: [Developer, AI, Daily]`
7. Include source links in this exact markdown shape whenever possible:
   - `[Source URL](https://example.com/article) (Source Name)`
8. After writing files, run a quick sanity check:
   - both files exist
   - both files have front matter
   - source links are present
9. Commit only the generated news post files if there are changes:
   - commit message: `chore: automated daily tech news update`
10. Push the commit to the current branch.
11. If there is already a post for today and no meaningful update is needed, do not create a duplicate commit.

Be concise in your final report. Mention created files, whether a commit was made, and whether push succeeded.
