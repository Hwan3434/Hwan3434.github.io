---
title: "Developers Build the Harness, Not the Code"
description: "Picturing a flow where AI fixes errors overnight and merges the fix, and asking what is left for developers when no one reads the code line by line"
date: 2026-11-21 20:00:00 +0900
categories: [philosophy, essay]
tags: [AI, agents, harness, lint, architecture, developers]
series: "Developers in the AI Era"
series_order: 3
---

Lately I have been reading and watching a lot about how to build software together with AI.
Lauren Tan's talk from the last post, Matt Pocock's writing, and a number of talks on YouTube.
The more I saw, the more it overlapped with what I had been thinking.

The last post ended on the idea that once the structure is in place, there is less room to produce slop.
Slop means low-quality output that AI churns out carelessly.
But who builds that structure?
And does it still hold when no one is watching?

> "What has to be in place for AI to do the right thing when no one is watching?"

> This post follows the answer I have reached for now.

By "from now on" I mean the next two or three years, five at most.
This is about building commercial apps.
Embedded work or building programming languages may be a different story.

## Errors fixed overnight

This is how I picture development.

1. **An error happens**: an error occurs in the app or the server
2. **It goes to an agent**: a hook hands the error to an agent. A hook is a mechanism that automatically runs a preset action when something happens
3. **The agent fixes it**: the agent reads the error, finds the cause, and fixes it
4. **Checked in the morning**: the developer comes in, looks at screenshots, and merges. Simple ones are already merged

This is not only my imagination.
The team behind the talk from the last post says it already does something similar.
Every time they cut a new release, an agent uses the app like a real user and looks for bugs.
Then it opens a fix PR for each bug and merges it automatically.
According to the speaker, the codebase is good enough that those PRs are mostly fine.

One thing stands out in this flow.
No person looks at the code.
While the agent fixes things the developer is asleep, and what they see in the morning is a result, not code.

So who stops the agent when it fixes something the wrong way?

## No one can read every line

Code written by AI is sometimes structured differently from what you expect.

You open it thinking that in this codebase it would surely be built a certain way, and it is built in a completely different way.
It works.
It is just not the structure you expected.

To prevent this, it seems someone would have to read the code line by line.
There is a lot to check.

- Is performance fine?
- Is there a security hole?
- Does the screen update when it should?
- Is the data getting tangled?
- Did something other than what was fixed change along with it (side effects)?

If a person has to check all of this, the flow above does not work.
Someone would have to reread, line by line in the morning, everything the agent fixed overnight.
Then the person becomes the bottleneck.

So I look at it the other way around.
A person does not check one by one whether AI's code is slop.
Instead of checking, they do something else.

## Don't say it; make it get stuck

In the last post I suggested blocking what must not happen with structure instead of sentences.
Lint or dependency boundaries: whatever the rule, breaking it makes a check fail.
Lint is a tool that automatically checks whether code follows the rules you set.
Dependency boundaries define which modules are allowed to call which.
In a flow no one is watching, this structure stops being nice to have and becomes something you cannot do without.

**Don't tell AI what not to do. Make it get stuck when it tries.**

I want to add one more thing.
When you block it, show the way too.
Don't stop at "you are blocked here"; also show "fix it like this."
Then AI reads that guidance and tries again.
Without anyone stepping in, AI finds its way back on its own.

This actually happened to me.
I blocked AI from running `git commit` directly.
The message it gets when blocked is "commit with `/commit`."
`/commit` is a skill, a work manual the agent can call.
It describes how to write commit messages.

At first AI tried to commit with a message written however it liked, as usual.
And it got blocked.
After reading the message, AI went back to `/commit` and committed again following the rules.
I said nothing in between.

I would like to call this kind of mechanism a harness.
A harness is the gear you put on a horse.
It sets the direction the horse's strength goes.
The horse supplies the strength and the person decides where it goes.

A commit message is a small rule.
But the same principle applies to the overnight flow.
When the agent heads the wrong way it gets stuck, and when it gets stuck it reads the guidance and comes back.

Of course, looking only at results misses some things.
Code whose screen looks fine but whose structure is not what you expected, for example.
That is why we catch as much as we can with lint.
Like the dependency boundaries from the last post, code that strays from the agreed structure fails the build.
The less something shows up in results, the more it should be stopped by a check rather than a human eye.

The performance and screen updates listed earlier can be blocked the same way.
It is not only lint.
There are more ways than you might think.
For example:

- Building the main branch every night and counting jank (frames dropped while the screen stutters)
- Running the tests
- Taking screenshots and comparing them with the previous version or yesterday's, to find screens that changed

What to block, and how, differs from codebase to codebase.

## Where people look

Still, some changes need a person.
At least for the next few years.
Earlier I said simple ones are already merged; there needs to be a rule for what counts as "simple."

Anthropic's Claude Code team has explained that it sorts changes by risk ([post](https://claude.dev/blog/solving-code-review-at-anthropic/)).
Low-risk changes such as docs or copy are merged without human approval.
Ordinary changes need one person, and the riskiest code needs two.

But this is just that team's example.
Which changes are risky differs from codebase to codebase.
What matters is that each team builds its own way to measure risk.
And that it sets up a mechanism to sort changes by that measure.
This is also part of the harness that developers build.

The point is that deciding what to block and where to look stays with developers.
AI writes the code and the developer builds the board AI writes on.

## Agreements between people, as structure too

Some things cannot be known no matter how well you read the code.
Agreements made between people.

For example, an agreement to post an announcement in Slack after a deploy.
This is not in the code, and the model cannot know it.

In the last post I wrote that this kind of flow would remain as a skill.
My thinking has moved one step further.
These agreements become scripts too, not skills.

AI is only told the fact that "an announcement goes to Slack when something is merged."
Sending the announcement is done by automation attached to the merge.
Then AI cannot forget the announcement or get its format wrong.

What must not happen gets stuck when tried, and what must happen happens automatically.
Either way, we do not hope that AI reads a sentence and remembers it.
This is a harness too.

So I think the developer's job changes.

| | Developers until now | Developers from now on |
|---|---|---|
| What they build | Source code | Harness (blocking structure, automation) |
| What they look at in the morning | The code of every change | Results; code only for risky changes |
| Center of the day | Implementing features | Deciding what to block, where to look, and what to automate |

## What has to be done now

With AI writing code today, my answer is that developers build the harness.
But this answer will not last forever.
In 10 or 20 years, or in the extreme case 100, no one will put lint or static analysis on AI.
Static analysis is a check that finds problems by reading code without running it.
The day AI writes well on its own will come, but it is still far off.
What we do now may mean nothing by then.
Still, it has to be done now.

So I leave this post not as a conclusion but as a record of where I stand now.

In the next post I want to widen the view.
Who will do what on a team that builds software this way.
