---
layout: post
title: "Thoughts on the Boundary Between PMs and Developers, and Entropy in the AI Era"
date: 2026-06-04 08:00:00 +0900
categories: [philosophy, essay]
tags: [AI, DDD, Product Engineering, essay]
---

# Thoughts on the Boundary Between PMs and Developers, and Entropy in the AI Era, Starting from Screen-Dependent APIs

I was organizing the retrospective agenda for our product organization for the first half of 2026. Among numerous inefficiencies, one particularly painful issue stood out. It was the problem of "screen-dependent API design," where the backend had to create a new API every time the frontend's screen layout changed. To resolve this maintenance nightmare—where we had to overhaul the server whenever a screen changed—we concluded that we should "provide pure APIs solely based on domain (business) units."

Suddenly, a thought crossed my mind. *"Is this perhaps the DDD (Domain-Driven Design) I've only heard about?"* I had never studied DDD deeply. However, rolling around in the field and experiencing the pain naturally led me in that direction. The struggle to discard the superficial shell of object-oriented programming and move toward "true object-oriented programming," where objects themselves fully take responsibility for business rules and data. That was the essence of DDD.

However, a strange sense of futility and a chilling question followed this realization. 
*"What is the meaning of this kind of architectural agonizing in an AI era like today?"*

Now, the cost of coding is infinitely converging to zero. For a mere ten or twenty dollars in API costs, AI perfectly refactors terribly written procedural code into a DDD pattern. We are in an era where even an OS can be whipped up for around a thousand dollars. Isn't the "craftsmanship" of a developer dividing object dependencies and designing domains ultimately destined to be rendered obsolete by AI?

If AI even handles the mechanical work of dividing dependencies, the essence of software ultimately boils down to "who holds the business policies (Rules)." From this, the conclusion emerges that it is best for Product Managers (PMs) to learn development. 
In the past, someone who knew a bit of planning and a bit of development was disparaged as a "jack-of-all-trades" lacking expertise. However, in a world where I have dozens of "extreme specialist" AI assistants under me capable of catching 0.01% of errors, the story changes. Now, those "mediocre" people will hold the reins of those AIs and become the master conductors of the orchestra, dominating the field by navigating the compromise between business practicality and technical perfection.

As my thoughts reached this point, a strange sense of unease crept over me as I sat in front of the terminal without looking at a single line of code, just running the system. Everything is working fine, so why do I feel so anxious and unable to trust it? Is it because I am a developer accustomed to the old ways?

The true nature of this anxiety was clear. It was an **"instinctive repulsion toward uncontrolled magic."** 
The driving force that made developers great for decades was a "perverted persistence" to control every variable without tolerating even a 0.01% edge case. In contrast, what makes a great Product Manager is a "free imagination" that boldly pursues only business value, ignoring the constraints and rules of reality. 

The PM's "chaos (disorder)" and the developer's "obsession (order)." The massive frictional heat that erupts when these two extreme temperaments violently collide is what gave birth to great products. 

But AI is breaking down the tension between the two. 
The friction between planning and development disappears, and everything connects smoothly. Without conflict, results will emerge quickly, but those results will somehow lack vitality, remaining ordinary and standardized. In this phenomenon, I felt a foreboding that the world's pendulum was shifting in the direction of **"decreasing entropy (diversity and degree of disorder)."** In a frictionless world, there is no innovation. It's just an era of downward leveling where safe, ordinary outputs regurgitated by AI are mass-produced. The unease I couldn't shake off was precisely this instinctive sense of crisis regarding the "loss of creative frictional heat."

Is this shift of the pendulum truly right?
No. If we are not to fall into this swamp of standardization, we must elevate the "Battlefield" where friction occurs to a higher dimension.

In the past, we fought over "How to implement this technically (How)." Now, however, we must generate even greater friction over "What to build for humanity, and Why." As coding costs converge to zero, PMs must explode their crazy imagination to maximize the chaos of the business, while developers must possess an even greater obsession to macroscopically control the complexity born from massive systems intertwined with hundreds of AI agents.

The moment we become intoxicated by the convenience provided by AI and settle for "adequate answers," the creative disorder (entropy) that evolved the product drops to its lowest, and its vitality will wither away. In this era of transformation where the boundaries between planning and development are blurring, only those who guard against the loss of friction and maintain the fierce human tension to the end will be able to carve a true edge in a standardized world.

A small fragment of code called a screen-dependent API eventually brought me back to the massive question of the essence of a product maker in the AI era. In a world where everything becomes ordinary, the intense frictional heat created by the chaos of planning and the obsession of development might be the most powerful weapon we must protect.
