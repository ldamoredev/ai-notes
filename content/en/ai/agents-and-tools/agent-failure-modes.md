---
title: "Agent failure modes"
description: Loops, wrong-tool calls, error cascades, context rot, and runaway cost. The characteristic ways agents break and how to contain each.
tags: [agents, failure-modes, debugging, reliability]
order: 10
updated: 2026-06-07
---
# Agent failure modes

Agents fail in recognizable ways. Knowing the catalog turns "the agent is flaky" into a
specific, fixable diagnosis — and most fixes are **structural**, not "use a better
model."

## The catalog

| Failure | Looks like | Mitigation |
|---|---|---|
| **Infinite / repetitive loop** | same action over and over, never finishes | hard iteration cap; detect repeats; clearer "done" signal |
| **Wrong-tool / bad-arg calls** | picks the wrong tool or hallucinates args | better [[ai/agents-and-tools/agent-computer-interface|tool descriptions]], fewer tools, arg validation |
| **Error cascade** | one bad observation derails all later steps | actionable error messages; let it retry/recover; checkpoints |
| **Context rot** | quality degrades as history grows | [[ai/agents-and-tools/agent-memory|summarize/trim]]; scope sub-agent context |
| **Goal drift** | wanders off the original task | re-state the goal each turn; [[ai/agents-and-tools/planning-and-decomposition|re-plan]] |
| **Runaway cost** | huge token/$$ bill per run | cap iterations, tokens, and tool calls |
| **Overconfidence** | declares success without verifying | require verification step / [[ai/agents-and-tools/evaluating-agents|eval]] of outcomes |

## Why agents fail more than workflows

Autonomy compounds small error rates: a 95%-reliable step is ~60% reliable over 10
sequential dependent steps. Long loops multiply the chance of *some* misstep — which is
the core argument for [[ai/agents-and-tools/workflows-vs-agents|preferring workflows]]
and keeping agent loops short.

## Debugging: read the trace

> The single most useful agent-debugging habit is **reading the full trace** —
> thought, action, observation per step. The failure stage is almost always obvious once
> you see what the agent actually saw and did.

Then fix the **earliest** broken step (often a tool/observation problem masquerading as
a reasoning problem).

**Connects to:** [[ai/agents-and-tools/react-loop|the loop]] ·
[[ai/agents-and-tools/evaluating-agents|evaluating agents]] ·
[[ai/agents-and-tools/autonomy-and-control|capping blast radius]]
