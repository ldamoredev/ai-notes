---
title: "The Model Context Protocol (MCP)"
description: MCP is an open standard for connecting models to tools and data — "USB-C for AI". What it standardizes and why it matters for agent ecosystems.
tags: [agents, mcp, tools, integration]
order: 8
updated: 2026-06-07
---
# The Model Context Protocol (MCP)

Before MCP, every app wired up [[ai/agents-and-tools/tool-calling|tools]] its own way —
an N×M mess of custom integrations. **MCP** (introduced by Anthropic, now broadly
adopted) is an open protocol that standardizes how applications expose tools, data, and
prompts to LLMs. The common analogy: **"USB-C for AI"** — one connector instead of many.

## What it standardizes

An MCP **server** exposes capabilities; an MCP **client** (the host app / agent)
consumes them. The protocol defines a few primitives:

- **Tools** — actions the model can call ([[ai/agents-and-tools/tool-calling|function
  calling]], standardized).
- **Resources** — data/context the server can provide (files, records).
- **Prompts** — reusable prompt templates the server offers.

## Why it matters

- **Write once, reuse everywhere** — build an MCP server for your system (GitHub, a DB,
  Slack) and any MCP-compatible host can use it. No per-app glue.
- **An ecosystem** — a growing library of servers means agents gain capabilities by
  *connecting*, not coding.
- **Separation of concerns** — tool/data providers and agent builders evolve
  independently against a stable contract.

## The same risks, now at the boundary

MCP doesn't remove [[ai/agents-and-tools/autonomy-and-control|security]] concerns — it
concentrates them. A connected server can read data and take actions, so the
[[ai/ai-safety-and-security/index|injection]] and **excessive-agency** questions apply:
vet servers, scope permissions, and don't auto-trust a third-party server's tools or the
content they return.

## The takeaway

> MCP turns "integrate this tool with this model" from bespoke code into plugging into a
> standard port. Great for reuse — and a new trust boundary to guard.

**Connects to:** [[ai/agents-and-tools/tool-calling|tool calling]] ·
[[ai/agents-and-tools/agent-computer-interface|tool design]] ·
[[ai/ai-safety-and-security/index|tool security]]
