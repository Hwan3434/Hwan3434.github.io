---
title: "What Each Person Does on a Team Where Anyone Can Build"
description: "Now that planners bring screens and AI writes the code, a look at what remains for planners, designers, developers, and QA on a team with a well-built harness"
date: 2026-11-22 14:00:00 +0900
categories: [philosophy, essay]
tags: [AI, agents, harness, planners, designers, developers, roles]
series: "Developers in the AI Era"
series_order: 4
---

The last post ended with the idea that developers build the harness instead of the code.
A harness is a setup that blocks the AI when it heads the wrong way and shows it the way back when it gets blocked.

A planning document used to come first, then designers drew the screens, developers built them, and QA checked them.
That order is coming apart.
Building is no longer something only developers do.

> "When anyone can build, what does each person on the team do?"

> Part 4 follows what planners, designers, developers, and QA will be doing from here on.

## Screens Instead of Planning Documents

This is how work flows for me these days.

1. **The planner makes the screens**: brings screens such as dashboards as HTML mockups
2. **The designer makes the design system**: builds and improves a design system that fits the HTML
3. **The developer builds with that design system**: builds the app screens and hooks up the real data

| | Before | Now |
|---|---|---|
| What the planner hands over | Planning document | HTML mockup |
| What the designer makes | A mockup drawn for each screen | A design system fitted to the HTML |
| What the developer builds from | The designer's mockups | The design system |

Still, the planner's HTML does not ship as is.
The HTML has no data in it.
Hooking up the real data and shipping it in the production app is the app developer's job.

## Teams Where the Lines Blur

This is not just our team.
Fiona Fung, who leads engineering for Claude Code at Anthropic, says "Our PMs code a lot now" ([article](https://claude.com/resources/articles/running-an-ai-native-engineering-org), 2026-06-03).

| | Before | After |
|---|---|---|
| Team makeup | Fixed roles: engineers write code, PMs plan, designers design | Roles blur: PMs prototype, engineers take on design and context |

Jess Yan, a PM at the same company, writes that once the job to be done is clear, the PM uses Claude Code to build and ship an agent for it directly ([article](https://claude.com/resources/articles/product-management-on-the-ai-exponential), 2026-04-29).

In Part 1, I wrote that it would be best for planners to learn development.
Back then it was a forecast; now, on some teams, what a PM builds ships as is.

So why, on our team, is that last step still the developer's job?

## With a Harness, It Does Not Matter Who Builds

My answer is the harness.

These days, when I hand the AI what I want, the AI does all of it.
What I check now and then is jank (frames dropped while the screen stutters), memory, and unnecessary functions or logic.
The harness already holds the architecture patterns.

The harness blocks the same way no matter who gave the AI the task.
An import that crosses a boundary fails the same check whether a developer asked or a planner asked.

**In a project with a well-built harness, planners and developers produce code of the same quality.**

I think this is possible even now.
But I have never actually had a planner try it.
No planner asked to, and the planners I have worked with did not know much about development.
So this part is a forecast that comes from my own experience.

## What the Harness Cannot Catch

If code quality is the same, does the product end up the same too?

| | Examples | What makes it the same |
|---|---|---|
| Code quality | Structure, dependency boundaries | The harness |
| Visual look | Color, fonts, spacing, components | The design system |
| UX | Layout, screen flow | Nothing |

How to arrange a screen and which flow to lead the user through cannot be guarded by a check.
I think that when planners arrange the layout, the UX will feel quite stiff.
Fiona Fung also says PMs and designers are still needed for product sense and taste.

So today's flow, where the planner goes as far as the wireframe (the skeleton of what goes where on a screen), will not last long.
It is more natural for the planner to design the features and hand over a list, and for the designer to lay out the screens on top of the design system.
Today's flow is what the transition looks like.

## What Is Left for Each Role

As AI and the harness improve, people will step into each other's areas more often.
Still, I do not think the roles merge into one.
Building gets mixed, while each role's area of responsibility actually gets sharper.

| Role | Transition (now) | After |
|---|---|---|
| Planner | Builds HTML mockups and wireframes | Designs features and hands over the feature list |
| Designer | Builds a design system to match the planner's HTML | Owns UI/UX, layout, wireframes, and the design system |
| Developer | Builds with the design system and hooks up the data | Builds the harness |
| QA | Checks by hand | Decides what gets checked automatically |

The developer row needs a little more.
The jank and memory issues I check now and then can actually be caught by a harness in CI (a setup that builds and checks the code automatically every time it is pushed).
But building that kind of harness is still hard without knowing development.
Once AI gets better it will do this on its own too, but not yet.
Shipping to a production app means performance and structure have to hold.
**For now, only developers can build the harness that holds them, and that is why the last step is still theirs.**

## The Transition Is 2 to 5 Years

I see the next 2 to 5 years as the transition.
I predict that within that time, more than 90% of companies will have changed this way.
This is about building commercial apps, and it is a guess, not a certainty.

The evidence is my own experience.
A year ago, the IDE was the default for development.
In the last three months, I can barely remember opening one.

If everyone produces code of the same quality with the same tools, code is no longer what sets products apart.
What decides success is how decisively the product solves the customer's problem.
And that comes down, in the end, to how much vision the business goal has.

So who decides what to build?
Right now, the planner does.
If the app's business value is clear, things will move toward growing and refining that value.
But if everyone has to agree together on how, that becomes another bottleneck.
Honestly, I do not know yet where that line will end up.

To sum up:

- **The harness**: when it is well built, code of the same quality comes out no matter who builds. For now, developers build it
- **Outside the harness**: UX such as layout and screen flow stays with designers
- **The transition**: today's flow, where planners go as far as the screens. The next 2 to 5 years
- **The measure of success**: how decisively the product solves the customer's problem. In the end, the vision of the business goal
- **The open question**: who decides what to build

Building is open to everyone.
What is left for each person is deciding what to build and what to let through.

In the next post, I want to look at the shadow of this flow.
The worry is that once harnesses and guides harden into standards, products built on the same structure will start to look alike.
