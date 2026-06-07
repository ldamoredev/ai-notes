---
title: Fine-tuning & Alignment
description: When and how to adapt a model — SFT, LoRA/QLoRA, RLHF, DPO, distillation, dataset quality, evaluation, cost, and hardware.
tags: [fine-tuning, alignment, lora, rlhf, dpo]
order: 0
updated: 2026-06-07
---
# Fine-tuning & Alignment

Fine-tuning changes a model's weights. Use it when you need to reshape behavior,
format, style, or task skill — not when you merely need fresher facts.

> The adaptation ladder is **prompt → RAG → fine-tune → distill**. Climb only when
> the cheaper rung cannot deliver the behavior you need.

## Decision frame

- [[ai/fine-tuning-and-alignment/when-to-fine-tune|When to fine-tune vs prompt vs RAG]]
- [[ai/fine-tuning-and-alignment/data-quality-for-finetuning|Data quality > quantity]]
- [[ai/fine-tuning-and-alignment/building-the-finetuning-dataset|Building the fine-tuning dataset]]
- [[ai/fine-tuning-and-alignment/evaluating-a-finetune|Evaluating a fine-tune]]

## Training methods

- [[ai/fine-tuning-and-alignment/supervised-fine-tuning|Supervised fine-tuning / instruction tuning]]
- [[ai/fine-tuning-and-alignment/lora-and-adapters|LoRA and adapters]]
- [[ai/fine-tuning-and-alignment/qlora-and-4bit-finetuning|QLoRA and 4-bit fine-tuning]]
- [[ai/fine-tuning-and-alignment/rlhf-with-ppo|RLHF with PPO, conceptually]]
- [[ai/fine-tuning-and-alignment/direct-preference-optimization|Direct Preference Optimization]]

## Failure modes and deployment economics

- [[ai/fine-tuning-and-alignment/catastrophic-forgetting|Catastrophic forgetting]]
- [[ai/fine-tuning-and-alignment/distillation|Distillation]]
- [[ai/fine-tuning-and-alignment/cost-and-hardware|Cost and hardware]]

## Core sources

- Hugging Face — **PEFT** documentation for LoRA, QLoRA, adapters, and trainer patterns.
- Unsloth docs — practical low-VRAM fine-tuning workflows and quantized training.
- Hu et al. — *LoRA: Low-Rank Adaptation of Large Language Models*.
- Dettmers et al. — *QLoRA: Efficient Finetuning of Quantized LLMs*.
- Ouyang et al. — *Training language models to follow instructions with human feedback*; Rafailov et al. — *Direct Preference Optimization*.
- Sebastian Raschka — fine-tuning articles, LoRA experiments, and *Build a Large Language Model (From Scratch)*.
