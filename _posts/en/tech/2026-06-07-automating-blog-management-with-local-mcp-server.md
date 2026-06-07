---
layout: post
title: "Automating Blog Management with a Local MCP Server"
date: 2026-06-07 08:47:19 +0900
categories: [tech]
tags: [MCP, AI Agent, Automation]
---

Today, I would like to share my experience of building a **pure local MCP server** so that an AI can control the Jekyll blog running on my local Mac environment.

## Why MCP instead of REST API or CLI?

Generally, when thinking about system automation, the first thing that comes to mind is spinning up a `REST API` server or creating a `CLI` tool.

Of course, both REST APIs and CLIs are excellent technologies, and they are essential when external integration is needed or when a user needs to interact directly with the terminal. That is, they are not technologies in opposition to MCP, but independent ones used as needed depending on the situation.

However, looking closely at my blog management environment, the story is a bit different. The sole purpose is "to have my own AI agent directly manage my blog on my local PC."

I didn't need to force open a REST API for external communication, nor did I need to separately develop a CLI for a human to type. Therefore, I judged that running a **single MCP server** that internally controls the GitHub CLI (`gh` or `git`) and communicates directly with the AI without external intervention was the most appropriate and elegant solution for the current situation.

## Architecture and Implementation

I easily built the server in a Node.js environment using the official `@modelcontextprotocol/sdk`.

### 1. `list_blog_categories` Tool
To allow the AI to grasp the existing category structure when writing a post, it reads the `_posts/` directory and returns a list of existing folders such as `news, tech, philosophy, etc`. This prevents the phenomenon of the AI arbitrarily creating categories that do not exist.

### 2. `create_blog_post` Tool
If the AI provides just the title and content, the backend automatically handles all the necessary tasks.
- Using regular expressions, it removes special characters from the title and automatically generates a clean URL slug.
- It applies KST (Korea Standard Time) to accurately calculate the publish date without time zone issues.
- It formats the markdown text to fit Jekyll's Frontmatter (`layout`, `title`, `date`, `category`) format.
- Through `child_process.execFileSync`, it sequentially executes `git add`, `commit`, and `push` to perfectly automate the deployment to GitHub.
