---
title: Fine-tuning & Alignment
description: When and how to adapt a base model — SFT, LoRA/QLoRA, RLHF, DPO, distillation — and how to know it worked.
tags: [fine-tuning, alignment, lora, rlhf, dpo]
order: 0
updated: 2026-06-07
---
# Fine-tuning & Alignment

Fine-tuning changes a model's **weights** to shape its behavior. The single most
important idea in this branch: **fine-tuning is for form, not facts.** Use it to
change style, format, tone, refusal patterns, and task-specific behavior — not to
inject knowledge that changes weekly (that is what retrieval is for).

The pragmatic adaptation ladder, cheapest first:

> **Prompt → RAG → Fine-tune → Distill**

Climb only when the cheaper rung stops working. Most teams over-reach for
fine-tuning when a better prompt or a retrieval pass would have solved it.

## What this branch covers

- **When** to fine-tune versus prompt or retrieve, and how to tell the difference.
- **Parameter-efficient** methods (LoRA, QLoRA) that make adaptation cheap.
- **Preference alignment** (RLHF, DPO) for shaping *which* answers a model prefers.
- **Data and evaluation** — the parts that actually decide whether a fine-tune helps.

## Core sources

- Sebastian Raschka — *Build a Large Language Model (From Scratch)* and his fine-tuning articles.
- Hugging Face **PEFT** documentation (LoRA/QLoRA in practice).
- **Unsloth** docs — practical, low-VRAM fine-tuning guide.
- Foundational papers: *LoRA*, *QLoRA*, *Direct Preference Optimization (DPO)*.

> Notes are being written. This branch index will link them as they land.
