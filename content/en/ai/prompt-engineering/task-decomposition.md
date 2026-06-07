---
title: "Task decomposition & prompt chaining"
description: One giant prompt that does everything is brittle. Splitting work into focused, chained steps improves reliability and makes failures debuggable.
tags: [prompt-engineering, decomposition, prompt-chaining, workflows]
order: 7
updated: 2026-06-07
---
# Task decomposition & prompt chaining

Cramming a multi-part job into a single mega-prompt tends to fail: the model drops
requirements, blends steps, and gives you no way to see *where* it went wrong.
**Decomposition** — break the task into focused steps and chain them — is usually the
biggest reliability win.

## Why smaller steps win

- Each call has **one clear objective**, so it's easier to get right and to
  [[ai/prompt-engineering/evaluating-and-iterating-prompts|evaluate]].
- Failures are **localized** — you can see which step broke and fix just that prompt.
- Intermediate outputs can be **validated** or transformed in code between steps
  ([[ai/prompt-engineering/structured-outputs|structured output]] makes this clean).

## Prompt chaining

Feed the output of one step as input to the next: e.g. *extract → classify → draft →
critique → revise*. This is the predictable, debuggable middle ground between a single
prompt and a fully autonomous [[ai/agents-and-tools/index|agent]] — a fixed workflow
you control.

> Workflow vs agent: if you can hard-code the steps, **do** — a chain is cheaper,
> faster, and more reliable than letting a model decide the control flow. Reserve
> agents for when the steps genuinely can't be predetermined.

## Patterns

- **Sequential chain** — steps in a fixed order.
- **Routing** — a classifier step sends the input to the right specialized prompt.
- **Generate-then-critique** — one call produces, another reviews/repairs.
- **Map-reduce** — process chunks independently, then combine (great for long docs).

## Pitfall

More steps = more [[ai/llms/tokenization|token]] cost and latency, and errors can
compound down the chain. Decompose enough to be reliable and debuggable, not so much
that you build a fragile Rube Goldberg pipeline.

**Connects to:** [[ai/agents-and-tools/index|workflows vs agents]] ·
[[ai/prompt-engineering/structured-outputs|passing data between steps]] ·
[[ai/prompt-engineering/chain-of-thought|reasoning within a step]]
