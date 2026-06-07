---
title: "Supervised fine-tuning / instruction tuning"
description: SFT teaches the model the desired prompt-response behavior using curated examples, but it only works when the examples are clean and representative.
tags: [fine-tuning, sft, instruction-tuning]
order: 2
updated: 2026-06-07
---
# Supervised fine-tuning / instruction tuning

Supervised fine-tuning (SFT) trains a pretrained model on curated prompt-response
pairs. For LLMs, instruction tuning is SFT that teaches the model how to behave as an
assistant: follow requests, use the right format, and prefer useful response patterns.

## What SFT changes

SFT does not create a new foundation model. It nudges an existing
[[ai/llms/base-vs-instruct|base or instruct model]] toward examples you provide.

| Training signal | Learns |
|---|---|
| Prompt and ideal response | How the task should be answered |
| Chat template | How roles and messages are formatted |
| Repeated style patterns | Tone, structure, refusal style, verbosity |
| Domain procedures | Stable workflows that should become default |

## Dataset shape

Each row should be a clean demonstration of desired behavior:

- The input resembles real production prompts.
- The response is something you would be happy to ship.
- The format is consistent across examples.
- Edge cases and refusals are included, not only happy paths.
- Train, validation, and test examples are split before iteration.

## What it does not solve

SFT does not reliably optimize preferences between two plausible answers; that is
where [[ai/fine-tuning-and-alignment/direct-preference-optimization|DPO]] or RLHF-like
methods fit. It also does not make missing knowledge appear unless that knowledge was
already latent in the model or present in the prompt.

## Pitfall

SFT faithfully learns your mess. Inconsistent labels, mixed formats, or mediocre
answers teach the model to be inconsistent, mixed, and mediocre.

**Connects to:** [[ai/llms/base-vs-instruct|base vs instruct]] ·
[[ai/fine-tuning-and-alignment/building-the-finetuning-dataset|dataset construction]] ·
[[ai/fine-tuning-and-alignment/direct-preference-optimization|DPO]]
