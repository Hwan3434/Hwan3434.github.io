---
title: "Thoughts on the Boundary Between PMs and Developers, and Entropy in the AI Era"
description: "Starting from screen-dependent APIs and DDD, a reflection on what the friction between PMs and developers, and entropy, mean when the cost of code nears zero."
date: 2026-06-04 08:00:00 +0900
categories: [philosophy, essay]
tags: [AI, DDD, Product Engineering, essay]
---

## From Screen-Dependent APIs to DDD

I was organizing the retrospective agenda for our product organization for the first half of 2026. Among numerous inefficiencies, one particularly painful issue stood out. It was the problem of "screen-dependent API design," where the backend had to create a new API every time the frontend's screen layout changed.

To resolve this maintenance nightmare, where we had to overhaul the server whenever a screen changed, we concluded that we should "provide pure APIs solely based on domain (business) units." Suddenly, a thought crossed my mind.

> Is this perhaps the DDD (Domain-Driven Design) I've only heard about?

I had never studied DDD deeply. But after rolling around in the field and living through the pain, I had naturally ended up heading in that direction. The struggle to discard the superficial shell of object-oriented programming and move toward "true object-oriented programming," where objects themselves fully take responsibility for business rules and data. That was the essence of DDD.

## When the Cost of Code Nears Zero

However, a strange sense of futility and a chilling question followed this realization.

> What is the meaning of this kind of architectural agonizing in an AI era like today?

Now, the cost of coding is infinitely converging to zero. For a mere ten or twenty dollars in API costs, AI perfectly refactors terribly written procedural code into a DDD pattern. We are in an era where even an OS can be whipped up for around a thousand dollars. Isn't the "craftsmanship" of a developer dividing object dependencies and designing domains destined to be pushed aside by AI?

If AI even handles the mechanical work of dividing dependencies, the essence of software boils down to **who holds the business policies (Rules)**. From this, the conclusion emerges that it is best for Product Managers (PMs) to learn development.

In the past, someone who knew a bit of planning and a bit of development was disparaged as a "jack-of-all-trades" lacking expertise. However, in a world where I have dozens of extreme-specialist AI assistants under me capable of catching 0.01% of errors, the story changes.

Now, the people who hold the reins of those AIs and navigate the compromise between business practicality and technical perfection, those once "mediocre" people, will become the master conductors of the orchestra and dominate the field.

## The PM's Chaos, the Developer's Obsession

What makes a great PM is a "free imagination" that boldly pursues only business value, ignoring the constraints and rules of reality. In contrast, the driving force that made developers great for decades was a "perverted persistence" to control every variable without tolerating even a 0.01% edge case.

| | PM | Developer |
|---|---|---|
| Temperament | Chaos (disorder) | Obsession (order) |
| Driving force | Free imagination | Perverted persistence |
| Aims at | Business value beyond the constraints of reality | Control down to the 0.01% edge case |

The two temperaments mostly collided at the point of implementation. When a PM's novel request multiplied queries and drove up API costs or weighed down the database, or when it meant touching an architecture that was already built, the PM's imagination and the developer's persistence stood against each other. The fight was always over "How do we implement this requirement?"

The massive frictional heat that erupts when these two extreme temperaments violently collide is what gave birth to great products.

## Where the Friction Disappears

But AI is breaking down the tension between the two.

The PM writes a meticulous plan together with AI, has AI review it and give feedback, and then hands it to the developer. In this process, the PM's creativity is, if anything, worn down by AI's persuasion. AI refines the plan while already accounting for development resources such as API costs and database load. The parts that would once have been shaved off by clashing with the developer are now shaved off in advance by AI.

The developer, in turn, gives that plan to AI as it is and has AI build it. The architecture and the API calls have already been considered in the plan, so there is nothing in particular to touch. The gaps that the developer's persistence would have dug into are already filled at the planning stage.

With AI filling both sides of the spot where the two temperaments used to clash, the very point of contact where friction happened disappears.

And so planning and development connect smoothly. Without conflict, results will emerge quickly, but they will somehow lack vitality, remaining ordinary and standardized.

When every company develops in this pattern, the tendencies of AI rub off on the products. The styles of models like OpenAI's, Claude, and Gemini seep into both the plans and the code, and even though the companies differ, their products come to resemble one another. In this phenomenon, I felt a foreboding that the world's pendulum was shifting in the direction of **decreasing entropy (diversity and degree of disorder)**.

**In a frictionless world, there is no innovation.**

It's just an era of downward leveling where safe, ordinary outputs regurgitated by AI are mass-produced. The foreboding I felt was precisely this instinctive sense of crisis regarding the loss of creative frictional heat.

> Is this shift of the pendulum truly right?

No. If we are not to fall into this swamp of standardization, we must elevate the "Battlefield" where friction occurs to a higher dimension.

## Raising the Battlefield

Once AI can rework an architecture, or rewrite queries and storage structures, in a single day, friction no longer happens at that point.

> Then where does the collision happen?

Facing what a PM or designer has made, the developer asks: "Is that really good UX?" "Can we afford the cost of storing even that?" The planning side answers: "Users will find this UI/UX fresh and engaging." "We have to store this to have the data we can offer our customers." Through this exchange, the developer also starts asking whether it is the core of the business.

If in the past the developer held on to "How do we implement this requirement?", now the PM and the developer begin to wrestle with the same territory: "Is this really the core of the business?" The battlefield where friction happens moves to "What to build for humanity, and Why."

| | The old battlefield | The new battlefield |
|---|---|---|
| Where friction happens | API costs and database load driven up by requests, changes that touch an existing architecture | Is that good UX? Is it worth storing even that? |
| The central question | How do we implement this requirement? | Is this really the core of the business? (What, Why) |
| PM and developer | Face off holding different questions | Clash over the same question |

Standing on the same battlefield does not mean their temperaments have to become the same. As coding costs converge to zero, PMs must explode their imagination to maximize the chaos of the business, and developers must possess an even greater obsession to macroscopically control the complexity that massive systems intertwined with hundreds of AI agents can produce. When chaos and obsession collide over the same question, the frictional heat comes back to life.

The moment we become intoxicated by the convenience provided by AI and settle for "adequate answers," the creative disorder (entropy) that evolved the product drops to its lowest, and its vitality will wither away.

In this era of transformation where the boundaries between planning and development are blurring, only those who guard against the loss of friction and maintain the fierce human tension to the end will be able to carve a true edge in a standardized world.

---

A small fragment of code called a screen-dependent API eventually brought me back to the massive question of the essence of a product maker in the AI era.

In a world where everything becomes ordinary, the intense frictional heat created by the chaos of planning and the obsession of development might be the most powerful weapon we must protect.
