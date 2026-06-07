---
title: "Cost and hardware"
description: Fine-tuning cost is dominated by model size, precision, sequence length, batch size, optimizer state, and iteration count.
tags: [fine-tuning, hardware, cost, gpu]
order: 12
updated: 2026-06-07
---
# Cost and hardware

Fine-tuning cost is not just "how big is the model?" It is model size, precision,
sequence length, batch size, optimizer state, activation memory, and how many bad runs
you need before the dataset is fixed.

## What consumes memory

| Memory item | Why it matters |
|---|---|
| Model weights | The base model must fit on device |
| Gradients | Needed for trainable parameters |
| Optimizer state | Adam can multiply trainable memory |
| Activations | Grow with batch size and sequence length |
| KV/context tensors | Matter for long chat examples |

Full fine-tuning pays most of these costs for every parameter. [[ai/fine-tuning-and-alignment/lora-and-adapters|LoRA]]
and [[ai/fine-tuning-and-alignment/qlora-and-4bit-finetuning|QLoRA]] reduce the trainable
and stored footprint.

## Cost levers

- Smaller base model if the task is narrow.
- LoRA/QLoRA instead of full fine-tuning.
- Shorter examples and trimmed context.
- Gradient checkpointing when memory is tight.
- Fewer epochs with early stopping.
- Better data review before expensive runs.

## Hardware planning

The practical question is whether you can fit the model, batch, and context length
with stable throughput. If not, reduce precision, use adapters, lower batch size, or
move to a smaller model. Training slowly but reproducibly is better than running a
large unstable job.

## Pitfall

The cheapest fine-tune is usually the one you do *after* cleaning the dataset and
building the eval. Otherwise you pay GPU time to discover obvious label problems.

**Connects to:** [[ai/fine-tuning-and-alignment/qlora-and-4bit-finetuning|QLoRA]] ·
[[ai/llms/quantization-and-inference|quantization]] ·
[[ai/fine-tuning-and-alignment/data-quality-for-finetuning|data quality]]
