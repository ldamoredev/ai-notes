---
title: "QLoRA and 4-bit fine-tuning"
description: QLoRA combines a quantized frozen base model with trainable LoRA adapters, enabling large-model adaptation on modest hardware.
tags: [fine-tuning, qlora, quantization, lora]
order: 4
updated: 2026-06-07
---
# QLoRA and 4-bit fine-tuning

QLoRA makes large-model fine-tuning practical on smaller GPUs by loading the frozen
base model in 4-bit precision while training LoRA adapters in higher precision.

## The stack

- The base model is quantized to 4-bit, which reduces memory dramatically.
- Base weights stay frozen, so quantization noise does not accumulate through updates.
- LoRA adapters are trained on top of the quantized model.
- Gradients and adapter weights use higher precision where it matters.

This is different from simply training a low-quality 4-bit model. The quantized base
is a memory-saving representation; the learned behavior lives in the adapters.

## Why 4-bit matters

Training memory is not just model weights. It includes gradients, optimizer state,
activations, and batch/context length. Quantizing the frozen base frees enough memory
for longer contexts, larger batches, or models that would otherwise not fit.

| Lever | Effect |
|---|---|
| 4-bit base weights | Large memory reduction |
| LoRA adapters | Small trainable parameter count |
| Gradient checkpointing | Trades compute for activation memory |
| Smaller batch / shorter sequence | Reduces memory but may hurt throughput |

## What can go wrong

QLoRA still depends on the same fundamentals: clean data, correct chat template, good
validation set, and evaluation that matches production. Quantization can also make
training more sensitive to hyperparameters.

## In practice

Use QLoRA when you need to adapt a model that is too large for ordinary fine-tuning
but still want a local, reproducible training loop.

**Connects to:** [[ai/llms/quantization-and-inference|quantization]] ·
[[ai/fine-tuning-and-alignment/lora-and-adapters|LoRA]] ·
[[ai/fine-tuning-and-alignment/cost-and-hardware|hardware planning]]
