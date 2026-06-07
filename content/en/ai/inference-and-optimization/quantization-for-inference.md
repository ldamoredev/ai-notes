---
title: "Quantization for inference"
description: Inference quantization stores weights or activations in lower precision to reduce memory, bandwidth, and cost, with possible quality tradeoffs.
tags: [inference, quantization, optimization]
order: 4
updated: 2026-06-07
---
# Quantization for inference

Quantization represents model values with fewer bits. For inference, the main prize is
smaller memory footprint and lower memory bandwidth, which can make a larger model fit
or let more requests share the same hardware.

## Common forms

| Approach | Typical use |
|---|---|
| FP16/BF16 | standard high-quality inference |
| INT8 | faster or smaller serving with modest quality impact |
| 4-bit weights | fit larger models on limited VRAM |
| GPTQ | post-training weight quantization with calibration |
| AWQ | activation-aware weight quantization |
| KV-cache quantization | reduce memory for long contexts |

## What can degrade

- Rare-token behavior and multilingual quality.
- Math, coding, and precise reasoning.
- Tool argument reliability and structured output.
- Long-context recall.
- Safety and refusal behavior on edge cases.

Quantization changes error patterns, so test the product task, not only a public
benchmark.

## Practical workflow

1. Establish a full-precision baseline.
2. Quantize one candidate.
3. Run product evals and safety evals.
4. Measure latency, memory, throughput, and cost.
5. Inspect failed slices before accepting savings.

## Pitfall

Quantization that passes average evals can still break high-value slices. Check
structured outputs, tool calls, and safety behavior explicitly.

**Connects to:** [[ai/llms/quantization-and-inference|LLM quantization]] ·
[[ai/evaluation/model-vs-product-evals|product evals]] ·
[[ai/inference-and-optimization/right-sizing-models|right-sizing models]]
