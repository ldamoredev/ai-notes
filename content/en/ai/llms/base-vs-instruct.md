---
title: "Base vs instruct vs chat models"
description: A base model completes text; an instruct/chat model follows requests. The post-training stack (SFT + preference alignment) that turns one into the other.
tags: [llms, instruction-tuning, rlhf, post-training]
order: 7
updated: 2026-06-07
---
# Base vs instruct vs chat models

The model you actually use is not the raw [[ai/llms/pretraining-next-token|pretrained]]
one. A second stage — **post-training** — reshapes a text-completer into an assistant
that follows instructions and behaves. Knowing the difference clears up a lot.

## Three flavors

| Type | Behaves like | Good for |
|---|---|---|
| **Base** | autocomplete of the internet | raw generation, research, your own fine-tuning base |
| **Instruct** | follows a single instruction | one-shot tasks (summarize, classify, extract) |
| **Chat** | multi-turn conversation with roles | assistants, agents, anything stateful |

Ask a *base* model "What is the capital of France?" and it might reply with a list of
similar quiz questions — it's completing a document, not answering you.

## The post-training stack

1. **SFT (supervised fine-tuning / instruction tuning)** — train on curated
   `(prompt → ideal response)` pairs so the model learns the *format* of being
   helpful and following instructions.
2. **Preference alignment** — [[ai/fine-tuning-and-alignment/index|RLHF or DPO]] tunes
   *which* of several valid answers the model prefers, using human preference data,
   to make it more helpful, honest, and harmless.

This is where chat templates, system prompts, and refusal behavior come from. The
[[ai/llms/pretraining-next-token|base model]] supplies the knowledge; post-training
supplies the manners.

## Why it matters in practice

- **Prompting differs** — base models want few-shot examples/continuation; chat models
  want instructions and a system prompt ([[ai/prompt-engineering/index|prompting]]).
- **Chat templates are real** — the special tokens that delimit roles must match the
  model, or quality drops.
- **Alignment is a tax and a gift** — it adds safety and usability but can cause
  over-refusal and a slight capability "alignment tax."

**Connects to:** [[ai/llms/pretraining-next-token|pretraining]] ·
[[ai/fine-tuning-and-alignment/index|SFT, RLHF & DPO]] ·
[[ai/prompt-engineering/index|prompting base vs chat]]
