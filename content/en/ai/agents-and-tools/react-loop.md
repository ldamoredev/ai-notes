---
title: "The ReAct loop: reason + act"
description: The core agent pattern — think, call a tool, observe the result, repeat until done. Why interleaving reasoning and action works.
tags: [agents, react, agent-loop, reasoning]
order: 4
updated: 2026-06-07
---
# The ReAct loop: reason + act

Strip an agent to its essence and it's a loop: **reason about what to do, take an action
(a [[ai/agents-and-tools/tool-calling|tool call]]), observe the result, repeat** until
the task is solved. This is **ReAct** (Reasoning + Acting), the backbone pattern.

## The loop

1. **Thought** — the model reasons about the goal and current state
   ([[ai/prompt-engineering/chain-of-thought|chain-of-thought]] applied to action).
2. **Action** — it calls a tool with arguments.
3. **Observation** — your code runs the tool and feeds the result back into the
   [[ai/llms/context-window-and-kv-cache|context]].
4. **Repeat** — until the model decides it's done and returns a final answer.

## Why interleaving beats planning alone

Pure upfront planning is brittle — the world rarely matches the plan. Pure acting is
blind. ReAct **interleaves** them: each action is informed by the latest observation, so
the agent adapts (a search returned nothing → try different terms). Reasoning grounds the
actions; observations ground the reasoning.

## What makes the loop work or fail

- **Good [[ai/agents-and-tools/agent-computer-interface|tools + observations]]** — clear
  results let the model decide the next step; noisy/huge results derail it.
- **A stopping condition** — a max-iteration cap and a clear "done" signal, or the loop
  [[ai/agents-and-tools/agent-failure-modes|runs forever]].
- **Context management** — each turn appends thought+action+observation, so the context
  grows fast; [[ai/agents-and-tools/agent-memory|summarize/trim]] to stay in budget.

## Pitfall

The loop's open-endedness is exactly what makes agents risky: unbounded iterations =
unbounded cost and the classic stuck-in-a-loop behavior. Always cap iterations and watch
the trace ([[ai/agents-and-tools/evaluating-agents|evaluation]]).

**Connects to:** [[ai/agents-and-tools/tool-calling|tool calling]] ·
[[ai/agents-and-tools/planning-and-decomposition|planning]] ·
[[ai/agents-and-tools/agent-failure-modes|loops]]
