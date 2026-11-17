---
title: "Write Down Only What Code Cannot Say"
description: "How an old rule about writing fewer comments now carries over to CLAUDE.md, lint, and architecture when working with AI agents"
date: 2026-11-17 22:00:00 +0900
categories: [philosophy, essay]
tags: [AI, agents, comments, lint, architecture, code review]
---

For a long time, I have been telling people to write fewer comments.
Comments that restate what a function does often wore out reviewers.

Lately, that advice sounds a little different to me.
It is no longer only people who read code.
AI agents read code, and they take it as a model for the next code they write.

> "What should be left in prose, and what should be left to the code?"

## Comments cannot keep up with code

The biggest reason I pushed for fewer comments is SSOT.
Single Source of Truth: each fact lives in exactly one place.
Tired reviewers are the visible symptom, and this is the root.

Over time, code changes like a living thing.
Requirements change, bugs get fixed, and the structure gets cleaned up.
But the comments that described that code do not change on their own.

When the same fact lives in both the code and a comment, sooner or later the two say different things.
Then the reader does not know which one to trust.
Code runs, so at least it tells you what it does now, but nobody checks a comment.

That is why I am on the side of keeping only the minimum of comments.
The question is what to keep and what to delete.

## Two rules

Comments are not the only way a codebase ends up saying something untrue.
Code that is left in place but never used causes the same problem.
So there are two rules.
Delete code this version does not use, and write comments only for what the code cannot say.

### Delete unused code

At some point I started deleting code that is not used in this version, even when it will almost certainly be used in the next one.

Leftover code is a claim in itself.
It claims, "This code is in use."
The next reader takes that code as a pattern in current use.
This is also an SSOT problem.
What the codebase says and what actually runs drift apart.

The memory of deleted code lives in git, not in the code.
I used to believe that if deleted code was needed again, tomorrow's me would write something better.
These days, instead of relying on that belief, I have AI bring back the old logic.

1. **Recall**: have AI dig through git commits to remind me how the logic was written back then
2. **Compare**: work with AI to find a better way, or decide whether the changed code and the old code can live together
3. **Rebuild**: build the best approach for the code as it is now

### Comments keep only the business "why"

That does not mean I write no comments at all.
I do not use comments to explain functions.
I write them only about the business, not about the logic.

Say there is code that "shows an event popup on day X from Y to Z in the afternoon."
The logic that compares the day and the time is right there in the code.
But why it is day X in particular cannot be expressed in code.
That belongs to product planning and the business.
That is what is worth leaving as a comment.

Such a comment does not conflict with SSOT either.
Why it is day X is a fact the code does not hold, so the code and the comment never state the same fact twice.

| | Comments to keep | Comments not to write |
|---|---|---|
| Content | A business decision, such as why day X | Restating what a function does |
| Source | Planning and business | The code itself |
| When the code logic changes | Still true if the decision stands | Drifts from the code |

In the end, the two rules come down to one sentence.
**Let the code say what code can express, and leave in prose only what code cannot express.**

## Our teammates became agents

Both rules are for the teammate who will read this code next.
Even when teammates change, the code must stay readable, and structure must prevent errors.
Deleting unused code and narrowing comments to the business "why" both serve to make the code readable on its own.
Going one step further, from being readable to actually preventing mistakes, is the job of static analysis such as lint.

But it seems that teammate is now an agent.

Lauren Tan (poteto)'s talk "[All Code Is Slop (Except Mine)](https://www.youtube.com/watch?v=O_zcc6Xl12g)" makes this point.
It was published on the AI Engineer channel on 2026-11-14.
Slop is a word for low-quality output that AI churns out carelessly.

The speaker compares a codebase to a garden.
If workarounds (code made to run without fixing the problem), anti-patterns, and technical debt are left in place, the next agent takes them as patterns and copies them.
So, the speaker says, if you want to trust agents, you first have to invest in the environment.

The talk also lays out an order of investment.

1. **The code itself**: API design and architecture
2. **Lint, types, tests**: rules that machines check
3. **Runtime and formal verification**: checks that actually run the code or prove it mathematically
4. **Prose**: rules, skills, AGENTS.md and CLAUDE.md (instruction files for agents). Kept thin, at the end

There is also a part about comments.
The speaker's team banned 99% of comments in product code.
Agents had used comments to justify workarounds, and the next agents followed those comments as iron rules.
The speaker's explanation is that comments go stale and cannot be enforced.

This talk may not be the answer for every team, but it points the same way as what I have been saying for a long time.
We differ a little on how to handle comments, and I will come back to that at the end.

What has changed is who reads.
A human reviewer doubts a stale comment and checks the code, but an agent trusts the comment as written and builds code on top of it.

## Block with structure, not prose

The talk's other pillar is checks.
It goes one step beyond code being readable, toward preventing errors through structure.
When an agent gets something wrong, do not add a line to AGENTS.md; turn it into a deterministic check.
A deterministic check is one, like lint or type checking, that always gives the same result for the same code.

The speaker gives two examples.

- Banning React's `useEffect` in product code
- Splitting an Electron app's main (the process running in the background) and renderer (the process that draws the screen) into top-level folders, and blocking imports between them with lint

The second example matches what I consider important in app architecture.
The core of app architecture is keeping modules from tangling, with dependencies as the boundary.
That boundary becomes a barricade against AI's import mistakes.
An agent can miss a sentence saying "do not call that layer from this one."
It cannot miss an import that crosses the boundary if the build catches it.
That is why I see **architecture, in the big picture, as one more lint**.

| | Blocking with prose | Blocking with structure |
|---|---|---|
| Form | Instruction files, comments | Lint, types, dependency boundaries |
| When violated | Nothing happens | The check fails |
| Over time | Drifts from the code | A check flags drift first |

The speaker's team also invests heavily in verification.
They spend most of their tokens on verification, and they review through verification artifacts such as videos, screenshots, and formal verification.
As a result, the speaker says, they shipped 11,000 PRs in a month, with about 0.5% reverted.
The speaker also says the app's performance actually improved.
These are the speaker's own claims, and I have not verified the numbers.

That does not mean that once the structure is in place, agents stop producing slop.
But they get less room to produce it, and when they do, a check is more likely to catch it first.

## CLAUDE.md is a comment too

Following this thought, one more thing comes into view.
Instruction files like CLAUDE.md and AGENTS.md are comments for agents.
They are the same in that they are prose outside the code, talking about the code.
Earlier the talk said not to add lines to the instructions; here it is about removing lines that are already there.

The reason to cut comments was that they drift from the code.
Instruction files get one more reason.
The model, which is the reader, knows more and more on its own.
So as I work with agents, I feel that instructions explaining what the model already does on its own lose meaning over time.

On 2026-11-16, I cut the AGENTS.md in my personal knowledge repository from 164 lines to 43.
The model I use now (Anthropic's Opus 5.5) does everything without such detailed writing.
I removed the lines explaining what the model does on its own and kept only the facts the model cannot know by itself.

Among the lines I deleted was one that went like this.
"When you leave a document, commit and push. Otherwise sessions on other machines read stale rules."
This line also has a "why" in it, but it is different from the "why" of day X.
The reason for day X is a fact that is neither in the code nor in the model.
If you do not push, others cannot see what changed.
That is how git works, and it is common knowledge the model already has.
When I saw this reason, I wondered why anyone had put in something so obvious.
So I kept the rule to commit and push, and deleted only the "otherwise…" reason.
The rule is something decided for this repository, so the model cannot know it by itself.

It is the same as deleting a comment that restates a function.
The code already says what the function does, and the model already knows why to push.
The principle is the same.
Do not write again what the reader can already know.
What changed is that, with the model as the reader, the range of "what the reader can already know" has grown.

An agent follows what is written as is, whether stale or redundant, and at the same time knows a lot that is not written.
Both traits point toward less prose.

### Skills and plugins go the same way

Prose about how to do things is not only in instruction files.
Skills that teach an agent the order of work, and plugins that add how to use a particular technology, are the same kind.

I used to build skills myself, such as for opening PRs and merging.
I also built a skill that hands work to sub-sessions (separately launched agent sessions).
These days, skills like that seem less and less necessary.

So from now on, skills seem likely to be used not to organize patterns of work, but only for a person's own workflow.
Something like "after this task is done, send a notification to Slack."
The model cannot know this however well it reads the code.
I am heading in that direction too.

Plugins are similar.
Plugins that teach how to use Flutter, React, or Swift seem likely to become unnecessary once AI uses those technologies best.
Plugins that connect to things outside the model, such as controlling a simulator or looking up the latest documentation, are different.
They are not about what the model knows, but about places the model cannot reach.

## A standard, not a ban

Where the talk and I part ways is comments.
That is because we start from different places.

| | The talk's rule | My rule |
|---|---|---|
| Starting point | The agent | The business |
| How comments are seen | An escape hatch for agents to justify workarounds | The only place where the planning "why" stays next to the code |
| Shape of the rule | Ban 99% | Keep only reasons that come from planning and the business |

Rather than a ban, I filter with the standard "keep only reasons that come from planning and the business."
Comments that excuse workarounds do not pass this standard.

Earlier I said an agent trusts comments as written.
If the only comments left are planning decisions, then even when an agent follows them, all it follows is what should be followed.
That is why this standard does not change whether the reader is a person or an agent.

To sum up:

- **Comments**: no restating functions; keep only the business "why"
- **Unused code**: delete if not used in this version; git keeps the memory
- **How to prevent mistakes**: lint and dependency boundaries over prose; architecture is one more lint
- **Instruction files, skills, plugins**: shrink toward facts the model cannot know, a person's own workflow, and connections to the outside

The principle is the same as long ago.
Leave to the code what code can say, and write down only what code cannot say.
What changed is that the readers of that writing now include agents as well as people, and the readers already know that much more.
