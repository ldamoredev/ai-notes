---
title: "Right-sizing models"
description: Right-sizing chooses the smallest, fastest, cheapest model strategy that clears product quality, safety, latency, and reliability gates.
tags: [inference, model-routing, distillation, cost]
order: 12
updated: 2026-06-07
---
# Right-sizing models

Right-sizing is the discipline of matching model capability to task difficulty. A
single largest model is simple, but often too slow and expensive for production unit
economics.

## Strategy options

| Strategy | Use when |
|---|---|
| Smaller model | task is easy, structured, or narrow |
| Distillation | large model behavior can be transferred to a cheaper model |
| Fine-tune | smaller model needs domain behavior or format reliability |
| Routing | tasks vary in difficulty and risk |
| Cascade | cheap model tries first, stronger model handles failures |
| Tooling | computation or lookup is better done outside the model |

## Routing signals

- User tier or workflow type.
- Prompt length and retrieval complexity.
- Confidence, judge score, or validation failure.
- Required safety level.
- Structured-output parse success.
- Historical difficulty of similar tasks.

## Evaluation approach

Run candidate routing policies against the product eval set. Measure quality, safety,
latency, cost per successful task, escalation rate, and failure concentration by slice.

## Pitfall

Routing can create inconsistent UX if users cannot predict quality. Keep product
contracts stable: route behind the scenes, but maintain the same reliability bar.

**Connects to:** [[ai/fine-tuning-and-alignment/distillation|distillation]] ·
[[ai/evaluation/model-vs-product-evals|product evals]] ·
[[ai/ai-product-engineering/latency-cost-quality-triangle|latency-cost-quality triangle]]
