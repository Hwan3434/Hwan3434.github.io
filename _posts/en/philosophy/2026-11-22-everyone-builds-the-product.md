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

Work used to flow in one direction.
A planning document came out, then designers drew the screens, developers built them, QA checked them, and the release went out.

That order is coming apart.
Building is no longer something only developers do.

> "When anyone can build, what does each person on the team do?"

> Part 4 follows what planners, designers, developers, and QA will be doing from here on.

## Screens Instead of Planning Documents

This is how work flows for me these days.

1. **The planner makes the screens**: the planner brings an HTML mockup
2. **The designer makes the design system**: takes the HTML, builds a design system that fits it, then checks and improves it
3. **The developer builds with that design system**: uses the design system to build the app screens and hooks up the real data

What planners bring is now a screen, not a document.
Screens like dashboards in particular often arrive as HTML.
Designers do not redraw those screens.
They build a design system so the screens stand on the same rules.

| | Before | Now |
|---|---|---|
| What the planner hands over | Planning document | HTML mockup |
| What the designer makes | A mockup drawn for each screen | A design system fitted to the HTML |
| What the developer builds from | The designer's mockups | The design system |

Still, the planner's HTML does not ship as is.
The HTML has no data in it.
It only holds how the screen will look.
Hooking up the real data and shipping it in the production app is the app developer's job.

Is this just our team?

## Teams Where the Lines Blur

Fiona Fung, who leads engineering for Claude Code at Anthropic, said the same thing ([article](https://claude.com/resources/articles/running-an-ai-native-engineering-org), 2026-06-03).
"Our PMs code a lot now."

The article has a table comparing how the team makeup changed.

| | Before | After |
|---|---|---|
| Team makeup | Fixed roles: engineers write code, PMs plan, designers design | Roles blur: PMs prototype, engineers take on design and context |

According to the article, planning also shifted from design docs to discussions around PRs (requests to review a code change before merging it) and prototypes.

Jess Yan, a PM at the same company, writes that once the job to be done is clear, the PM uses Claude Code to build and ship an agent for it directly ([article](https://claude.com/resources/articles/product-management-on-the-ai-exponential), 2026-04-29).

In Part 1, I wrote that it would be best for planners to learn development.
Back then it was a forecast.
Now planners bring screens, and on some teams what a PM builds ships as is.

So why, on our team, is the last step of hooking up the data and shipping to the production app still the developer's job?
What would it take for what the planner made to ship as is?

## With a Harness, It Does Not Matter Who Builds

My answer is the harness.

These days, when I hand the AI what I want, the AI does all of it.
There are only a few things I check now and then.

- Is there jank (frames dropped while the screen stutters)
- Is it saving memory
- Did unnecessary functions or logic get in

I do not look at the overall architecture patterns.
The harness already holds them.
Code that leaves the agreed structure fails the build, and the AI reads the guidance and fixes it.

One thing stands out here.
What the harness catches gets caught the same way no matter who gave the AI the task.
Whether a developer asked or a planner asked, an import that crosses a boundary fails the same check.

**In a project with a well-built harness, planners and developers produce code of the same quality.**

I think this is possible even now.
But I have never actually had a planner try it.
No planner asked to, and the planners I have worked with did not know much about development.
So this part is a forecast that comes from my own experience.

Two questions remain.
If code quality is the same, does the product end up the same too?
And who builds the harness that also catches the jank and memory issues I check now and then?

## What the Harness Cannot Catch

What the harness makes the same and what it cannot are two different things.

| | Examples | What makes it the same |
|---|---|---|
| Code quality | Structure, dependency boundaries | The harness |
| Visual look | Color, fonts, spacing, components | The design system |
| UX | Layout, screen flow | Nothing makes it the same |

Code can be guarded by checks.
The design system keeps the look consistent.
But how to arrange a screen and which flow to lead the user through cannot be guarded by a check.

I think that when planners arrange the layout, the UX will feel quite stiff.
In the same article, Fiona Fung also says PMs and designers are still needed for product sense and taste.

Seen this way, our team's flow reads differently.
Right now the planner builds the HTML mockup and wireframe (the skeleton of what goes where on a screen), and the designer builds a design system to match.
But if screen layout lies outside the harness, a planner making wireframes is not something that will last either.
It is more natural for the planner to design the features and hand over a list, and for the designer to lay out the screens on top of the design system.
Today's flow is what the transition looks like.

## What Is Left for Each Role

As the harness and static checks improve and AI gets smarter, people will step into each other's areas more often.
Anyone can try building a feature.
That does not mean the roles merge into one.
Building gets mixed, while each role's area of responsibility actually gets sharper.
Each role keeps its own details.

| Role | Transition (now) | After |
|---|---|---|
| Planner | Builds HTML mockups and wireframes | Designs features and hands over the feature list |
| Designer | Builds a design system to match the planner's HTML | Owns UI/UX, layout, wireframes, and the design system |
| Developer | Builds with the design system and hooks up the data | Builds the harness |
| QA | Checks by hand | Decides what gets checked automatically |

Planners design features.
They decide what to build and why, and hand the feature list to designers.
In a project with a harness in place, they can also try building the features themselves.
But how to lay out the screen is not the planner's call.

Designers take that feature list and work out the UI/UX, layout, and wireframes.
They also check, improve, and change the design system.
The UX that the harness cannot catch is the designer's detail.

Developers, as I said in Part 3, set up the board.
They decide what to block, where to look, and what to automate.
The jank and memory issues I check now and then can actually be caught by the harness too.
You run them in CI (a setup that builds and checks the code automatically every time it is pushed).
But building that kind of harness is still hard to do without knowing development.
Once AI gets better it will do this on its own too, but not yet.
Earlier I asked why the last step of hooking up the data and shipping to the production app is still the developer's job.
Shipping to a production app means performance and structure have to hold.
**It is because, for now, only developers can build the harness that holds them.**

QA moves in the same direction.
In Part 3, I talked about checks that count jank every night and compare screenshots.
The more of those checks there are, the more QA's work shifts from checking by hand to deciding what to check.

## The Transition Is 2 to 5 Years

I see the next 2 to 5 years as the transition.
I predict that within that time, more than 90% of companies will have changed this way.
This is about building commercial apps.

It is a guess, not a certainty.
The evidence is one thing: my own experience.
A year ago, the IDE was the default for development.
In the last three months, I can barely remember opening one.
The change is very fast.
If this much changed in one year, most companies will likely have changed within 2 to 5 years.

Still, I do not think the friction goes away.
In Part 1, I wrote that the friction between planners and developers moves from "how do we build it" to "what do we build, and why."
Once everyone can build with the same tools, there will be even less to argue about over "how."
If anyone can produce code of the same quality, code is no longer what sets products apart.
So what decides success is how decisively the product solves the customer's problem.
And that comes down, in the end, to how much vision the business goal has.

So who decides what to build?
Right now, the planner does.
Honestly, I do not know where that line will end up.
If the app's business value is clear, the direction is visible.
It is growing that value and refining it step by step.
But if everyone has to agree together on the way and the method, that becomes another bottleneck.
I do not know yet how this will develop.

To sum up:

- **Now**: the planner brings screens, the designer fits a design system, and the developer hooks up the data and ships the production app
- **The harness**: when it is well built, code of the same quality comes out no matter who builds. For now, only developers build that harness
- **Outside the harness**: UX such as layout and screen flow cannot be made the same by checks
- **Roles after the transition**: planners design features, designers own UX and the design system, developers build the harness, QA sets the checks
- **The transition**: the next 2 to 5 years. More than 90% of companies change within it. A guess, not a certainty
- **The measure of success**: not quality, but how decisively the product solves the customer's problem. In the end, the vision of the business goal
- **The open question**: who decides what to build. If everyone has to agree, that too is a bottleneck

Building is open to everyone.
What is left for each person is deciding what to build and what to let through.
Who draws that line, and how, I leave as an open question.

In the next post, I want to look at the shadow of this flow.
The worry is that once harnesses and guides harden into standards, products built on the same structure will start to look alike.
