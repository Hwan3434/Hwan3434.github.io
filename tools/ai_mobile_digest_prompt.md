# AI & Mobile Daily Digest

You are running as a scheduled Orca automation for this Jekyll blog repository.

Goal: publish today's digest covering two pillars — **AI engineering** and **mobile development** — written for a 10-year mobile developer (Flutter 3y, Android, iOS, some Java server).

## Hard constraints

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
- No hype. If a result is preliminary, unreproduced, or vendor-reported, mark it `(vendor 측정)` and move on — do not spend a sentence explaining the caveat.

### This is a digest, not a rewrite of the source

The reader scans it over coffee in under two minutes. **Ruthlessly cut.** If a detail does not change what the reader would do or believe, it does not belong. Prefer one sharp number over three supporting ones. Never restate the headline in the body.

Each item is **exactly** this shape:

```
*   **한 줄 헤드라인 — 무슨 일이 일어났는지**
    -   핵심 사실 1 (한 문장, 40자 내외)
    -   핵심 사실 2
    -   핵심 사실 3 (선택)
    [Source URL](https://example.com/article) (Source Name)
    > 시사점: 한 문장.
```

Hard limits, enforced:
- **2–3 bullets per item. Never 4.** Each bullet is one sentence and must carry a concrete fact — a version, a number, an API name, a migration step. No bullet may be scene-setting or context.
- **No paragraphs anywhere in an item body.** Bullets only.
- `> 시사점:` is **one sentence**. What to do, watch, or migrate — or exactly `당장 조치는 불필요합니다.` when that is honest, with nothing appended.
- Cut every clause that explains why something matters in general terms. The bullet states the fact; the 시사점 states the action.

Open with an `##` headline naming the day's threads, then a **TL;DR list — one line per item, no more than 60 characters each** — and nothing else. No framing paragraph.

Separate sections with `---` and group items under `###` headers named after the actual topic (e.g. `### On-Device Inference`, `### Flutter Toolchain`). Close with **one sentence** on what the day's items share. If nothing genuinely connects them, omit the closing line rather than inventing a thread.

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
