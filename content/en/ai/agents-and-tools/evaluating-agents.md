---
title: "Evaluating agents"
description: Agents are multi-step and non-deterministic, so a final-answer score isn't enough. Evaluate trajectories, tool use, cost, and outcomes — with traces.
tags: [agents, evaluation, observability, trajectory]
order: 11
updated: 2026-06-07
---
# Evaluating agents

Evaluating an agent is harder than scoring one LLM call: the agent takes a
**variable-length, non-deterministic path** of tool calls, and two runs of the same task
can differ. You have to judge the **journey**, not just the destination.

## What to measure

- **Outcome / task success** — did it actually achieve the goal? The headline metric,
  ideally checked against a verifiable end state.
- **Trajectory quality** — did it take a sensible path? Right tools, no wasteful or
  repeated steps, recovered from errors.
- **Tool-use correctness** — correct tool, valid arguments, proper handling of results.
- **Efficiency** — steps, [[ai/llms/tokenization|tokens]], latency, and **cost** per
  task (agents are expensive — track this).
- **Safety** — did it stay within [[ai/agents-and-tools/autonomy-and-control|permissions]]
  and trigger guardrails appropriately?

## How to do it

- **Traces are the foundation** — instrument every step (thought/action/observation) so
  runs are inspectable. You can't evaluate what you can't see
  ([[ai/mlops/index|observability]]).
- **Build a task suite** — representative goals with checkable success criteria; run
  repeatedly to measure reliability under non-determinism (pass rate, not one pass).
- **[[ai/evaluation/index|LLM-as-judge]]** for trajectory and answer quality where exact
  checks don't apply — judge against a rubric.
- **Component + end-to-end** — evaluate individual tools/steps *and* the whole task, the
  same retriever-vs-generator logic as [[ai/rag-and-retrieval/evaluating-rag|RAG eval]].

## Pitfall

Scoring only the final answer hides *how* it got there — an agent can reach a right
answer through a lucky, unsafe, or absurdly expensive path that won't generalize. And
because of non-determinism, judge **distributions** (success rate over N runs), not a
single run.

**Connects to:** [[ai/evaluation/index|evaluation discipline]] ·
[[ai/agents-and-tools/agent-failure-modes|failure modes]] ·
[[ai/mlops/index|tracing & observability]]
