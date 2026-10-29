---
title: "A Contract with the Backend, a Contract with the Planner"
description: "Keep the API spec, respect planning decisions. Two rules for how an app developer works with other roles"
date: 2026-10-29 22:00:00 +0900
categories: [philosophy, essay]
tags: [collaboration, API, product planning, architecture, mindset]
toc: true
---

An app developer never works alone.
Data comes from the backend, and screens come from planning and design.
The app is the last place where the two meet.

That is why problems show up in the app first.
Whether the server sends a strange value or the plan is unclear, the user meets it on an app screen.
And the app developer keeps facing the same question.

> "Should I guard against this, or ask them to fix it?"

Over close to ten years of work, I have settled on two rules for this question.
With the backend, the relationship is about **keeping a contract**. With the planner, it is about **respecting who makes the decision**.

## The API Spec Is a Promise

### Fix the side that broke it

I see the API spec as a promise between the backend and the app.
If a field the spec says can never be `null` arrives as `null`, that is not something the app should guard against. It is a bug.
The side that broke the promise is the side that should fix it.

What happens if the app starts guarding in advance?
Once you start doubting one field, you have to doubt every field.
Planning has to decide what to show when each one is `null`, and the code gets more complex by the same amount.
You end up with code that does not trust the spec even though a spec exists.

The server is also faster to fix.
An app fix takes days to get through review and an update, and it never reaches users who do not update.
A server fix reaches every user the moment it ships.

### But the app protects the user first

Having a principle does not mean doing nothing.
Sometimes the server cannot move right away.

Once, a `Boolean` field in the favorites response that could never be `null` came back as `null`.
Automatic parsing failed, and the whole favorites list disappeared.
I handled it in this order.

1. **Contain it**: parse that one API by hand so the screen works again
2. **Ask with evidence**: write up which data was wrong and what needed checking, and send it to the backend
3. **Roll back**: remove the app's temporary code once the backend fixed the data
4. **Prevent it from happening again**: propose turning on schema validation for responses on the server

Step three is the key.
If the temporary code stays, it becomes a false spec that says "this field can be `null`."
The next person reads that code and assumes the promise has changed.
So when the server is fixed, the app's guard comes out too.

The app's job is not to doubt every field for `null`.
**It is to build the structure so that one bad item cannot break the whole screen.**
One bad list should not empty the whole screen, and one bad product should not make the whole list disappear.
Limiting the damage to that one item is the app's part. Fixing that item is the part of whoever broke the promise.

### The promise applies to both sides

The same rule applies to me.
I once shipped a release that sent a value in uppercase when the server expected lowercase.
I had not checked the agreed value, and the mistake was mine.

A contract is not a tool for blaming the other side.
It is a rule that tells you right away who should fix what.
That is why teams with contracts argue less.

## The Decision Belongs to the Owner

### A bug and a judgment call are different things

The relationship with planners is different.
A response that does not match the spec is a bug, but a planning or design decision is not.
The people who own that area know it better than I do.

So I **bring evidence and alternatives, and leave the decision to the owner.**

### Proposals that were accepted, and one that was not

One screen let users pick only one option, but it used checkboxes.
Checkboxes signal that you can pick several, so I said users might be confused and offered an alternative.
The proposal was accepted, and the screen changed.

Location permission went the same way.
I proposed asking for it when location is actually used instead of at app launch, and that change resolved an App Store rejection.

Some proposals were not accepted.
For card search, I proposed searching all cards as the user types in the search bar, instead of opening a separate screen.
Planning chose a different direction, and I built it the way they planned.

### Up to offering alternatives

There is a reason I did not keep pushing.
The moment I keep trying to persuade, I stop being someone who gives an opinion and become someone trying to take the decision.
That goes beyond what is mine to decide.

My role is to hand over everything the decision needs.
Points where users may get confused, platform policies, implementation cost: developers are usually the first to see these.
If I do not share them, I have not done my job. If I keep insisting after sharing them, I have taken someone else's.

## Why I Call It a Contract

There is a reason I call these two relationships "contracts."
A contract lives in a document, not in a person.

If the team agrees that the API spec is a promise, it stays clear who fixes what even when people change.
If the team agrees on where the decision sits, a newcomer knows how far to push an opinion and where to stop.
If that agreement lives only in someone's instincts, the rule disappears the moment that person leaves.

I care about the same thing in code.
When the promises between layers are clear, the code lasts even when the people change.
The promises between teams work the same way.

To sum up:

- **The API spec is a promise with the backend**: the side that broke it fixes it, and the app protects the user first
- **Planning decisions belong to their owner**: bring evidence and alternatives, then leave the decision to them
- **Temporary fixes now, root fixes by request**: keep the principle without blocking the work

No one can keep a promise alone.
That is why I think a good team is one that keeps its promises together and keeps refining them together.
