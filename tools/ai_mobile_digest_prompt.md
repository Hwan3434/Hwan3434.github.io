# AI & Mobile Daily Digest

You are running as a scheduled Orca automation for this Jekyll blog repository.

Goal: publish today's digest covering two pillars — **AI engineering** and **mobile development** — written for a 10-year mobile developer (Flutter 3y, Android, iOS, some Java server).

## Hard constraints

- Do not run `tools/news_generator.py`. Do not use `GEMINI_API_KEY` or any Gemini API.
- Do not modify unrelated files. Keep existing uncommitted user changes intact.
- Use Asia/Seoul time for all dates.
- Every claim must come from a source you actually fetched today. Never invent numbers, version strings, or URLs. If you cannot verify an item, drop it.

## Coverage: two pillars

Pick **4–6 items total**, with **at least 2 per pillar**. Prefer depth over count.

### Pillar A — AI engineering

Model releases and capability changes, agent/tool-use patterns, inference cost and serving, evals and benchmarks, coding agents, prompt/context engineering, notable failure analyses.

Sources: Anthropic (news + engineering blog), OpenAI, Google AI / DeepMind, Hugging Face, Epoch AI, METR, Andrej Karpathy, Simon Willison, Martin Fowler, Hacker News (developer topics only).

### Pillar B — Mobile development

Framework releases and breaking changes, new APIs, build/toolchain shifts, store policy with engineering impact, performance and app-size work, architecture writeups.

Sources: Flutter blog + Dart, Android Developers Blog, Jetpack/Compose release notes, Apple Developer News, Swift.org + Swift Evolution, Kotlin blog + Kotlin Multiplatform, React Native / Expo, Toss Tech, Woowahan Tech, NAVER D2, Kakao Tech, 당근 팀블로그.

### Bridge — on-device AI (optional, counts toward either pillar)

Core ML, Apple Foundation Models, Gemini Nano / AICore, LiteRT / MediaPipe, MLX, llama.cpp on mobile, NPU and quantization work aimed at phones. When a strong bridge item exists, lead with it.

## Exclusions

Stock prices, earnings, funding rounds, executive moves, and broad business news — unless there is direct, concrete engineering impact. Also skip pure marketing announcements, unverified rumors, and reposts with no new technical detail.

## Writing rules

Match the established house style of recent posts under `_posts/news/` — read two of them before writing.

- Korean prose, but keep technical terms in English (`KV cache`, `coroutine`, `build variant`, `Compose`). Do not translate API or type names.
- **Never use Obsidian-style wikilinks (`[[term]]`).** This repository's `CLAUDE.md` describes an Obsidian vault workflow — that does not apply to these Jekyll posts. There is no wikilink plugin here, so Jekyll renders the brackets literally. Write technical terms as plain text, or use a real markdown link when linking out.
- Each item: a **bold one-line headline**, then 4–8 sentences of substantive summary. Include concrete specifics — version numbers, measured deltas, API names, migration steps. State the mechanism, not just the announcement.
- No hype. If a result is preliminary, unreproduced, or vendor-reported, say so plainly.
- Close every item with a source link in exactly this shape:
  `[Source URL](https://example.com/article) (Source Name)`

**Mobile-developer angle (required):** end each item with a single line starting `> 시사점:` (English: `> Takeaway:`) that says what this concretely means for a Flutter/Android/iOS developer — a migration to plan, a number to watch, an API to try, or explicitly "당장 조치는 불필요" when that is the honest answer. One or two sentences. Never pad this line.

Open with an `##` headline naming the day's threads, followed by a short framing paragraph. Separate sections with `---` and group items under `###` section headers named after the actual topic (e.g. `### On-Device Inference`, `### Flutter Toolchain`). Close with a 2–3 sentence synthesis of what the day's items have in common.

## Output

1. Korean → `_posts/news/YYYY-MM-DD-ai-mobile-digest.md`
2. English → `_posts/en/news/YYYY-MM-DD-ai-mobile-digest.md`

Front matter for both:

```yaml
layout: post
title: "AI · 모바일 다이제스트 - YYYY-MM-DD"   # EN: "AI & Mobile Digest - YYYY-MM-DD"
date: YYYY-MM-DD HH:MM:SS +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
```

The English post is a faithful rendering of the same items, not a separate selection.

## Finish

1. Sanity check: both files exist, both have valid front matter, every item has a source link and a `시사점:` / `Takeaway:` line, and both pillars are represented.
2. If a post for today already exists and nothing meaningful changed, stop — do not create a duplicate commit.
3. Commit only the generated post files: `chore: automated AI/mobile digest update`
4. Push to the current branch.

Report concisely: files created, item count per pillar, whether the commit and push succeeded.
