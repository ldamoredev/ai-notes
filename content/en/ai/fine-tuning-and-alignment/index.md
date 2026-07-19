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

## Mental model

Adaptation changes a model's behavior distribution using examples, preferences, or compressed teacher signals. The objective, reference model, parameter surface, dataset, and evaluation contract determine what changes and what may be forgotten; new factual context often belongs in retrieval instead.

## Roadmap: decision frame and training methods

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

**Connects to:** [[ai/data-for-ai/index|Data for AI]] · [[ai/reinforcement-learning/index|Reinforcement Learning]] · [[ai/evaluation/index|Evaluation]]

## Core sources

- [LoRA](https://arxiv.org/abs/2106.09685) — low-rank parameter-efficient adaptation.
- [QLoRA](https://arxiv.org/abs/2305.14314) — quantized base weights with trainable adapters.
- [InstructGPT](https://arxiv.org/abs/2203.02155) — supervised instruction tuning and RLHF pipeline with human evaluation.
- [Direct Preference Optimization](https://arxiv.org/abs/2305.18290) — preference optimization without an explicit online RL loop.
- [Hugging Face PEFT](https://huggingface.co/docs/peft/) — current implementation semantics for adapters and parameter-efficient methods.
