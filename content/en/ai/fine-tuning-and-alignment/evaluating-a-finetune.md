---
title: "Evaluating a fine-tune"
description: A fine-tune is only better if it wins on held-out target behavior without regressing safety, format, latency, or cost.
tags: [fine-tuning, evaluation, regression-testing]
order: 11
updated: 2026-06-07
---
# Evaluating a fine-tune

A fine-tune is not successful because training loss went down. It is successful only
if the adapted model improves the target behavior on held-out cases and does not
regress the behaviors your product depends on.

## Evaluate against baselines

Compare at least three systems:

| System | Why |
|---|---|
| Original model + old prompt | Current production bar |
| Original model + improved prompt/RAG | Cheaper alternative |
| Fine-tuned model | Candidate improvement |

If the fine-tune only beats a weak prompt, the conclusion is premature.

## What to measure

- Target task quality on held-out examples.
- Output format reliability and schema validity.
- Safety/refusal behavior and policy adherence.
- General instruction-following regression.
- Latency, cost, and throughput.
- Human preference when the task is subjective.

## Error analysis

Do not stop at aggregate scores. Cluster failures: wrong facts, bad format, over-refusal,
under-refusal, style drift, missing citations, tool-call errors, or degraded reasoning.
Then decide whether to fix data, method, prompt, or model choice.

## Pitfall

Training loss is an internal signal, not product quality. A model can lower loss by
memorizing dataset quirks that users will never benefit from.

**Connects to:** [[ai/evaluation/index|evaluation]] ·
[[ai/machine-learning/error-analysis|error analysis]] ·
[[ai/fine-tuning-and-alignment/catastrophic-forgetting|forgetting]]
