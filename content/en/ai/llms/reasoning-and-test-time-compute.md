---
title: "Reasoning & test-time compute"
description: Chain-of-thought and reasoning models trade inference compute for accuracy — the model "thinks" before answering. What changed, when it helps, and what it costs.
tags: [llms, reasoning, chain-of-thought, test-time-compute]
order: 12
updated: 2026-06-07
---
# Reasoning & test-time compute

A major recent shift: instead of only scaling *training*, you can scale **inference** —
let the model generate intermediate reasoning before its final answer. Spending more
tokens (more compute) at answer time measurably improves hard tasks.

## From chain-of-thought to reasoning models

- **Chain-of-thought (CoT)** prompting — asking the model to "think step by step"
  produces intermediate steps and improves multi-step problems. It works because
  generation is sequential: written-out steps become context the later tokens can
  build on (the model can't do unlimited hidden computation in one step).
- **Reasoning models** — newer models are *trained* (often with RL on verifiable
  problems) to produce long internal reasoning before answering. They effectively do
  CoT natively and spend a variable amount of "thinking" per problem.

## Test-time compute as a new scaling axis

The insight: for a fixed model, **letting it think longer** (more reasoning tokens,
sampling multiple attempts and selecting the best) raises accuracy on math, code, and
logic — a different lever than making the model bigger. Compute moved partly from
pretraining to inference.

## When it helps — and when it doesn't

| Use reasoning for | Skip it for |
|---|---|
| math, code, logic, multi-step planning | simple lookup, classification, extraction |
| problems with verifiable steps | latency-sensitive, high-volume calls |

The costs are real: reasoning tokens mean **higher latency and price**, and on easy
tasks the extra thinking adds cost with little gain (sometimes overthinking hurts).
It also doesn't fix [[ai/llms/why-llms-hallucinate|hallucination]] — a confident wrong
chain is still wrong.

> Reasoning trades [[ai/ai-product-engineering/index|latency and cost]] for accuracy.
> Spend it where the problem is genuinely hard; default to fast models elsewhere.

**Connects to:** [[ai/llms/emergent-abilities-and-scale|in-context learning]] ·
[[ai/prompt-engineering/index|chain-of-thought prompting]] ·
[[ai/ai-product-engineering/index|latency vs quality]]
