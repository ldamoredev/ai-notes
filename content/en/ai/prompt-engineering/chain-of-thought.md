---
title: "Chain-of-thought & when not to use it"
description: Asking the model to reason step by step helps multi-step problems — and wastes latency on simple ones. Why it works and when to skip it.
tags: [prompt-engineering, chain-of-thought, reasoning]
order: 4
updated: 2026-06-07
---
# Chain-of-thought & when not to use it

**Chain-of-thought (CoT)** prompting asks the model to produce intermediate reasoning
before the final answer ("think step by step"). It reliably improves multi-step
tasks — but it's not free, and it's not always appropriate.

## Why it works

Generation is sequential: each token conditions on the ones before it. By writing out
steps, the model creates **its own context to build on**, spreading a hard computation
across many tokens instead of forcing it into a single step. The reasoning tokens are
scratch space.

## When it helps

- Math, logic, multi-step word problems.
- Planning and decomposition.
- Anything where a human would need to "work it out."

## When to skip it

- **Simple lookup/classification/extraction** — CoT adds latency and cost for no gain,
  and can even hurt by overthinking.
- **Latency- or cost-sensitive, high-volume** calls.
- When you only want the answer in a tight [[ai/prompt-engineering/structured-outputs|format]]
  — then separate the reasoning from the final structured output (or use a reasoning
  model that hides it).

## CoT vs reasoning models

Newer [[ai/llms/reasoning-and-test-time-compute|reasoning models]] do CoT natively
(trained to reason before answering), so explicit "think step by step" matters less
with them — but understanding CoT explains *why* those models spend inference compute,
and CoT is still useful on non-reasoning models.

## Pitfall

A confident, well-written chain of thought can still reach a wrong answer — CoT
improves odds, it doesn't guarantee correctness or fix
[[ai/llms/why-llms-hallucinate|hallucination]]. Verify outputs that matter.

**Connects to:** [[ai/llms/reasoning-and-test-time-compute|reasoning & test-time compute]] ·
[[ai/prompt-engineering/self-consistency-and-sampling|self-consistency]] ·
[[ai/prompt-engineering/task-decomposition|decomposition]]
