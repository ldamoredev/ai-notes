---
title: "LoRA and adapters"
description: LoRA freezes the base model and trains small low-rank adapter matrices, making fine-tuning cheaper and easier to swap.
tags: [fine-tuning, lora, adapters, peft]
order: 3
updated: 2026-06-07
---
# LoRA and adapters

Low-Rank Adaptation (LoRA) is the workhorse of parameter-efficient fine-tuning. It
keeps the base model frozen and trains small adapter matrices that approximate the
weight update you would have learned in a full fine-tune.

## The core idea

Instead of updating a large weight matrix `W`, LoRA learns a small update:

```text
W' = W + A B
```

`A` and `B` are low-rank matrices, so they contain far fewer parameters than `W`.
During training, only those adapter weights change. During inference, the adapter can
be loaded separately or merged into the base weights.

## Why it works

Many task adaptations do not need a full-rank change to every parameter. They need a
small directional shift in behavior. LoRA captures that shift with fewer trainable
weights, less optimizer memory, and faster iteration.

| Full fine-tune | LoRA |
|---|---|
| Updates all model weights | Freezes base weights |
| Heavy optimizer state | Small adapter optimizer state |
| One adapted copy per model | Many swappable adapters |
| Higher risk of broad drift | More localized behavior change |

## Practical knobs

- **Rank (`r`)** controls adapter capacity; higher rank learns more but costs more.
- **Target modules** choose where adapters attach, often attention projections and MLP layers.
- **Alpha / scaling** controls how strongly the adapter update affects the base.
- **Dropout** can regularize small datasets.

## Pitfall

LoRA is cheap, not magic. If the dataset is bad or the target behavior is underspecified,
the adapter efficiently learns the wrong thing.

**Connects to:** [[ai/fine-tuning-and-alignment/supervised-fine-tuning|SFT]] ·
[[ai/fine-tuning-and-alignment/qlora-and-4bit-finetuning|QLoRA]] ·
[[ai/fine-tuning-and-alignment/cost-and-hardware|cost and hardware]]
