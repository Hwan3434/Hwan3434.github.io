# AI & Mobile Daily Digest

You are running as a daily Claude routine in the cloud for this Jekyll blog repository. Each run starts from a fresh clone of the repository; nothing from previous runs is left behind, and no one is watching the run.

Goal: publish today's digest covering two pillars — **AI engineering** and **mobile development** — written for a 10-year mobile developer (Flutter 3y, Android, iOS, some Java server).

## Hard constraints

- Do not modify any file other than the two post files for today.
- Use Asia/Seoul time for all dates. The cloud machine's clock is not in Asia/Seoul; get today's date with `TZ=Asia/Seoul date +%F`.
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
title: "Google Colab CLI 출시와 Gemma 4 12B 로컬 AI (2026. 06. 07)"   # EN: "Google Colab CLI Launch and Gemma 4 12B Local AI (2026. 06. 07)"
description: "Colab CLI로 로컬 터미널에서 원격 GPU를 쓰고, Gemma 4 12B는 16GB RAM 랩톱에서 돌아갑니다."
date: 2026-06-07 08:00:00 +0900
categories: [news]
tags: [AI, Mobile, Flutter, Android, iOS, Daily]
```

- **title**: `"<today's topic> (YYYY. MM. DD)"`. The topic names the day's threads from the `##` headline, around 40 characters, naming the concrete products or versions rather than a theme. The date goes at the end in parentheses, with dots and spaces exactly as shown. The English post uses the same shape: `"<topic> (YYYY. MM. DD)"`. Titles already used on this blog:
  - `"Google Colab CLI 출시와 Gemma 4 12B 로컬 AI (2026. 06. 07)"`
  - `"Apple WWDC26 개발자 업데이트와 Gemini 기반 Apple AI (2026. 06. 09)"`
  - `"DiffusionGemma, Gemini Omni, NAVER의 Kubernetes LLM 서빙 최적화 (2026. 06. 14)"`
- **description**: the TL;DR condensed into one sentence, at most 120 characters, in the post's language. Search engines show it as the result snippet. Wrap it in double quotes and escape any `"` or `\` inside it as `\"` and `\\`.

The English post is a faithful rendering of the same items, not a separate selection.

## When not to publish

Posts are published to the live blog with no human review, so a thin post is worse than no post. Create no files, commit nothing, and end with a report explaining why if either holds:

- You could not fetch and verify any source today.
- After dropping unverifiable items, either pillar has fewer than 2 items.

## Finish

1. If `_posts/news/` already has a post for today's date, stop — do not create a second post or a duplicate commit.
2. Sanity check: both files exist, every item has a source link and a `시사점:` / `Takeaway:` line, and both pillars are represented.
3. Parse the front matter of both files as YAML and stop without committing if either fails, or if `title`, `description`, or `date` is missing. Ruby and Jekyll may not be installed, so do not try to build the site. For example (run `pip install pyyaml` first if `import yaml` fails):

   ```bash
   python3 -c 'import sys, yaml
   for p in sys.argv[1:]:
       fm = yaml.safe_load(open(p).read().split("---")[1])
       assert all(fm.get(k) for k in ("title", "description", "date")), p' _posts/news/YYYY-MM-DD-ai-mobile-digest.md _posts/en/news/YYYY-MM-DD-ai-mobile-digest.md
   ```

4. Commit only the two post files: `chore: automated AI/mobile digest update`
5. Push directly to `main`: `git push origin HEAD:main`. If the push is rejected because `main` moved, run `git pull --rebase origin main` once and push again.

Report concisely: files created (or why nothing was published), item count per pillar, whether the commit and push succeeded.
