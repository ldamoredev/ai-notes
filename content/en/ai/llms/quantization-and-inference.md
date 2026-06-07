---
title: "Quantization & inference"
description: Quantization shrinks a model by lowering numeric precision, trading a little quality for big memory and speed wins. The basics, and the inference knobs that shape cost.
tags: [llms, quantization, inference, serving]
order: 11
updated: 2026-06-07
---
# Quantization & inference

A trained model is a pile of weights stored as numbers. **Quantization** stores them
at lower precision (fewer bits), shrinking memory and speeding up inference — the main
reason capable models can run on a single GPU or even a laptop.

## What quantization does

Weights are typically trained in 16-bit (fp16/bf16). Quantization converts them to
lower precision:

| Precision | Rough size vs fp16 | Typical quality |
|---|---|---|
| fp16 / bf16 | baseline | full |
| int8 / 8-bit | ~½ | near-full |
| 4-bit (e.g. NF4, GPTQ, AWQ) | ~¼ | small, often acceptable loss |

The tradeoff: lower precision = less memory and faster compute, at some accuracy cost.
4-bit is a popular sweet spot for running large models on modest hardware; quality
loss is usually modest but task-dependent — **measure it**. (4-bit also underpins
[[ai/fine-tuning-and-alignment/index|QLoRA]] fine-tuning.)

## The inference cost levers

Serving is dominated by GPU **memory bandwidth and capacity**, not just FLOPs. The
knobs that shape latency and cost:

- **Quantization** — smaller weights, less memory traffic, faster.
- **[[ai/llms/context-window-and-kv-cache|KV cache]] size** — grows with context and
  batch; often the binding memory constraint.
- **Batching** — serving many requests together raises throughput (good for cost) but
  can raise per-request latency.
- **Prefill vs decode** — the prompt is processed in parallel (prefill); generation is
  one token at a time (decode), which is the slow part.

## Practical takeaways

- For self-hosting, quantize and use a serving engine (vLLM, TGI) that does paged KV
  cache + continuous batching.
- "Latency" splits into **time-to-first-token** (prefill) and **tokens/second**
  (decode) — optimize the one your [[ai/ai-product-engineering/index|product]] feels.
- Quality after quantization is empirical — benchmark on *your* task before trusting
  it ([[ai/evaluation/index|eval]]).

**Connects to:** [[ai/llms/context-window-and-kv-cache|KV cache]] ·
[[ai/mlops/index|serving]] ·
[[ai/ai-product-engineering/index|latency & cost]]
