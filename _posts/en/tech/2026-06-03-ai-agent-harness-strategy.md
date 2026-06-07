---
title: "AI Agent Harness Strategy: Abandoning Universality and Focusing on the Domain"
description: "The overlap issue with custom-built skills experienced from the Claude Code update, and insights into building an effective AI harness"
date: 2026-06-03 11:50:00 +0900
categories: [ai, retrospect]
tags: [Claude Code, AI Agent, Harness, Productivity]
toc: true
---

Recently, while actively using AI coding agents like **Claude Code** in my work, I had been building and using a custom 'Harness' tailored to my own development environment. Here, a harness refers to the **custom rules, skills, sub-agents**, etc., that help the agent better understand and operate within my projects.

Initially, I meticulously defined skills and rules for general workflows, security guidelines, and even coding patterns that the agent couldn't handle perfectly. However, as time passed, I faced an unexpected, yet perhaps inevitable problem.

## The pace of AI advancement is faster than I imagined

The biggest issue was that **as the version of Claude Code went up, the harness rules and skills I had painstakingly implemented began to come built-in to the product itself**.

A prime example is the rule **"Do not casually check or copy the env file"**. In the beginning, I explicitly created a rule to enforce this out of concern that the agent might accidentally read the environment variable file or expose it externally. But at a certain point (since the Opus 4.8 version), Claude Code itself evolved to automatically filter out and avoid reading the security-sensitive `.env` file.

Eventually, the 'general features or rules that could apply to any project (Do not do XX)' that I had worked hard to create, such as "Do not push without permission" and "Do not read environment variables," either overlapped with default features or became legacy code that actually hindered the agent's efficiency. I found myself having to find and manually remove the rules, skills, and sub-agents I had previously created.

## What to entrust, and what to teach?

Going through this process, I gained an important insight into how to work with AI agents.

**"General tasks should be entrusted to the AI's own development and intelligence."**

General security principles, universal GitHub usage, etc., will soon be performed perfectly by the AI through updates without us needing to enforce them with rules. Spending time building a harness for these things only results in increased maintenance costs. General rules should be gradually removed in line with the advancement of AI performance.

Then, what is the knowledge we truly need to inject into the agent through a harness? It is exactly the **unique contexts that exist only in our projects**.

### 1. Collaboration Conventions
- **How to write Commit and PR messages**: Rules for linking to our team's issue tracker, commit convention formats
- **Code Formatting and Linting Rules**: Beyond general lint rules, the specific architectural rules our team adheres to

### 2. Project-Specific Execution Guides
- **Build and Run Methods**: Complex build scripts and app execution methods that are configured differently per environment like `dev`, `stage`, and `prod`

## Conclusion

The true value of a harness lies in elevating the agent from a 'smart coder' to **'a colleague who perfectly understands our team's context'**.

From now on, when writing rules or skills for an AI agent, I plan to ask myself first: "Is this universal knowledge that applies to any project, or is it domain knowledge unique to our team?" The most sustainable way to utilize agents is to boldly leave the general aspects to the advancement of the tools, and focus our remaining energy on **spoon-feeding our unique conventions and domain context to the AI**.
