---
title: "Multi-agent systems & handoffs"
description: Splitting work across specialized agents (orchestrator + sub-agents) buys parallelism and focus — at the cost of coordination, tokens, and new failure modes.
tags: [agents, multi-agent, orchestration, handoffs]
order: 7
updated: 2026-06-07
---
# Multi-agent systems & handoffs

Instead of one agent doing everything, split work across **multiple specialized agents**
that coordinate. It can dramatically help — Anthropic's research system uses an
orchestrator spawning parallel sub-agents — but it multiplies cost and complexity, so it
needs justification.

## Common shapes

- **Orchestrator–worker** — a lead agent decomposes the task and delegates subtasks to
  sub-agents, then synthesizes their results. The dominant pattern.
- **Handoff** — one agent transfers control (and context) to a more specialized agent
  ("route billing questions to the billing agent").
- **Parallel sub-agents** — independent subtasks run concurrently (e.g. research several
  sub-questions at once), then results are merged.

## Why split at all

- **Separation of concerns** — each agent has a focused role, fewer tools, and a clean
  [[ai/agents-and-tools/agent-memory|context]] — which improves reliability.
- **Parallelism** — independent subtasks finish faster.
- **Specialization** — different prompts/tools/models per role.

## The costs (don't ignore them)

- **Token blowup** — multi-agent systems can burn many times the tokens of a single
  agent; reserve them for high-value tasks where breadth/parallelism pays.
- **Coordination is hard** — passing the *right* context at a handoff is the crux; too
  little and the sub-agent flails, too much and you lose the focus benefit.
- **Compounding errors** — one bad sub-result can poison the synthesis.

## Guidance

> Start with **one** agent + good tools. Go multi-agent when the task has clearly
> separable, parallelizable subtasks — and design handoffs as deliberate context
> transfers, not full-history dumps.

**Connects to:** [[ai/agents-and-tools/planning-and-decomposition|delegation]] ·
[[ai/agents-and-tools/agent-memory|context per agent]] ·
[[ai/agents-and-tools/evaluating-agents|evaluating multi-agent]]
