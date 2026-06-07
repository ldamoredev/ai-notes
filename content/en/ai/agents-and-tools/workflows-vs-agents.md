---
title: "Workflows vs agents: when to use which"
description: The most important agent decision is whether to build one at all. Predetermined workflows beat autonomous agents whenever the steps are knowable.
tags: [agents, workflows, architecture]
order: 1
updated: 2026-06-07
---
# Workflows vs agents: when to use which

Before "how do I build an agent," ask "**should** this be an agent?" The distinction
(from Anthropic) is about who controls the steps:

- **Workflow** — LLM calls orchestrated through **predefined code paths**. You decide
  the steps; the model fills them in.
- **Agent** — the **model decides** its own steps and tool use dynamically, looping
  until done.

## Prefer the workflow

Workflows are more **predictable, cheaper, faster, and easier to
[[ai/agents-and-tools/evaluating-agents|debug]]**. Most "agent" use cases are really
workflows: [[ai/prompt-engineering/task-decomposition|prompt chaining]], routing,
parallelization, generate-then-critique. If you can draw the flowchart, code the
flowchart.

> Agentic autonomy trades reliability and cost for flexibility. Buy it only when the
> path genuinely can't be predetermined.

## When an agent earns its keep

- The number/order of steps is **unknown ahead of time** (open-ended research,
  debugging, "do whatever it takes to X").
- The task needs **dynamic tool selection** based on intermediate results.
- A fixed flow would be a giant brittle decision tree.

## The spectrum

| | Predictability | Cost/latency | Use for |
|---|---|---|---|
| Single prompt | highest | lowest | one well-scoped task |
| Workflow (chain/route) | high | low–medium | known multi-step pipelines |
| Agent (loop) | lower | higher | open-ended, dynamic tasks |

## Pitfall

"Agent" is a hype magnet; teams reach for autonomy and inherit
[[ai/agents-and-tools/agent-failure-modes|loops, runaway cost, and flaky behavior]] to
solve a problem a [[ai/prompt-engineering/task-decomposition|chain]] handled. Start at
the simplest point on the spectrum that works.

**Connects to:** [[ai/prompt-engineering/task-decomposition|prompt chaining]] ·
[[ai/agents-and-tools/react-loop|the agent loop]] ·
[[ai/agents-and-tools/autonomy-and-control|autonomy limits]]
