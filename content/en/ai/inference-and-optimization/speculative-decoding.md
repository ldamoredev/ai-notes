---
title: "Speculative decoding"
description: Speculative decoding accelerates generation by having a small draft model propose tokens that a larger model verifies in parallel.
tags: [inference, speculative-decoding, decoding]
order: 6
updated: 2026-06-07
---
# Speculative decoding

Speculative decoding uses a cheaper draft model to propose several next tokens, then
asks the larger target model to verify them. If the draft is often right, the system
gets multiple accepted tokens per target-model step.

## Basic flow

1. The draft model generates a short candidate continuation.
2. The target model evaluates those candidate tokens.
3. Accepted tokens are emitted.
4. Rejected tokens are corrected by the target model.
5. The loop repeats until completion.

The output distribution can remain equivalent to the target model when implemented
with the right acceptance rule.

## When it helps

| Helps when | Hurts when |
|---|---|
| draft model is much faster | draft is too inaccurate |
| target model is expensive | verification overhead dominates |
| output is predictable | task requires surprising or high-entropy tokens |
| serving stack supports it | implementation increases complexity |

## Design choices

- Draft model size and quality.
- Number of speculative tokens per step.
- Whether draft and target share tokenizer.
- Hardware placement for draft and target.
- Monitoring accepted-token rate by task.

## Pitfall

Speculative decoding is not magic compression. If the draft model predicts poorly for
your workload, you add complexity without reducing latency or cost.

**Connects to:** [[ai/llms/decoding-and-sampling|decoding and sampling]] ·
[[ai/inference-and-optimization/latency-vs-throughput|latency]] ·
[[ai/inference-and-optimization/serving-engines|serving engines]]
