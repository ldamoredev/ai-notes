---
title: "Planning & decomposition"
description: For multi-step goals, agents break work into subtasks and sequence them. Plan-and-execute vs reactive looping, and why plans must stay revisable.
tags: [agents, planning, decomposition]
order: 5
updated: 2026-06-07
---
# Planning & decomposition

Hard tasks need structure: an agent that just reacts step-by-step can lose the thread on
a ten-step goal. **Planning** is having the agent break the goal into subtasks and
sequence them — but the plan must stay **revisable**, because reality intervenes.

## Two stances

- **Reactive ([[ai/agents-and-tools/react-loop|ReAct]])** — decide the next step each
  turn from the latest observation. Adaptive, but can wander on long horizons.
- **Plan-and-execute** — draft a plan of subtasks first, then execute them (often
  re-planning after each). Keeps long tasks on track and makes progress legible.

Most robust agents **combine** them: a high-level plan for direction, reactive looping
within each step, and re-planning when steps fail.

## Decomposition techniques

- **Subgoal breakdown** — split the goal into ordered, checkable subtasks
  ([[ai/prompt-engineering/task-decomposition|prompt decomposition]] for agents).
- **Reflection / self-critique** — after acting, the agent reviews progress and adjusts
  the plan (a "generate → critique → revise" loop).
- **Delegation** — hand subtasks to specialized [[ai/agents-and-tools/multi-agent-systems|sub-agents]].

## Keep plans cheap and revisable

> A plan is a hypothesis, not a contract. The value is direction and the ability to
> notice when a step failed — not rigid adherence. Re-plan when observations contradict
> the plan.

## Pitfall

Over-planning burns [[ai/llms/tokenization|tokens]] producing elaborate plans the agent
can't follow, and rigid plans break on the first surprise. Under-planning lets the agent
drift and loop. Match planning depth to task horizon; for short tasks, plain ReAct is
enough.

**Connects to:** [[ai/agents-and-tools/react-loop|ReAct]] ·
[[ai/agents-and-tools/multi-agent-systems|delegation]] ·
[[ai/llms/reasoning-and-test-time-compute|reasoning models]]
