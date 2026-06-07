---
title: "Public benchmarks and their limits"
description: Public benchmarks help compare broad capabilities, but they are weak proxies for your product, data, users, and operating constraints.
tags: [evaluation, benchmarks, model-selection]
order: 9
updated: 2026-06-07
---
# Public benchmarks and their limits

Public benchmarks are useful for orientation, not final product decisions. They
compress broad capability into comparable numbers, but they rarely match your task,
data distribution, latency budget, safety bar, or user interface.

## What benchmarks are good for

- Shortlisting model families before deeper testing.
- Tracking broad capability trends across releases.
- Finding capability ceilings for reasoning, coding, math, language, or safety.
- Explaining why a model is not a plausible candidate for a task.

## What they miss

- Your private data, tools, prompts, retrieval pipeline, and UX.
- Domain-specific terminology and failure costs.
- Long-tail user behavior and adversarial inputs.
- Production constraints: cost, latency, rate limits, uptime, and observability.
- Contamination risk when benchmark examples leak into training.

## Interpreting benchmark numbers

| Benchmark signal | How to use it |
|---|---|
| Large model gap | investigate the stronger model in your own evals |
| Small model gap | prioritize cost, latency, and product evals |
| Benchmark improvement | check whether your task improves too |
| Arena preference | useful for general chat feel, weak for specialized workflows |

## Pitfall

A benchmark leaderboard can make model selection feel objective while hiding the real
decision. Your eval set is the acceptance test; public benchmarks are scouting notes.

**Connects to:** [[ai/evaluation/model-vs-product-evals|model vs product evals]] ·
[[ai/llms/emergent-abilities-and-scale|scale]] ·
[[ai/fine-tuning-and-alignment/evaluating-a-finetune|fine-tune eval]]
