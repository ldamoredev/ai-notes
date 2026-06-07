---
title: "Catastrophic forgetting"
description: Fine-tuning can improve the target behavior while damaging general abilities. Know why it happens and how to detect it.
tags: [fine-tuning, catastrophic-forgetting, regression]
order: 9
updated: 2026-06-07
---
# Catastrophic forgetting

Catastrophic forgetting happens when fine-tuning improves a narrow target behavior but
damages capabilities the model already had. The model did not "forget" like a person;
its weights shifted away from useful general behavior.

## Why it happens

Fine-tuning data is usually much narrower than pretraining data. If training pushes too
hard on that narrow distribution, the model over-specializes.

| Cause | Effect |
|---|---|
| High learning rate | Large, destructive weight updates |
| Too many epochs | Memorization and drift |
| Narrow dataset | Loss of general behavior outside the target task |
| Bad formatting | Chat/template behavior regresses |

## How to detect it

Evaluate both the target task and preserved behaviors:

- Held-out task examples from the fine-tuning domain.
- General instruction-following prompts.
- Safety/refusal tests if policy behavior matters.
- Format and tool-call tests if the model is used in a system.
- A small benchmark or smoke suite for broad capability regression.

## Mitigations

Use lower learning rates, early stopping, smaller LoRA rank, regularization, and a
mixed dataset that includes examples of behavior you must preserve. Keep a reference
model and compare outputs during evaluation.

## Pitfall

If you only evaluate the target task, forgetting looks like success. Always measure
what must not get worse.

**Connects to:** [[ai/fine-tuning-and-alignment/lora-and-adapters|LoRA]] ·
[[ai/fine-tuning-and-alignment/evaluating-a-finetune|eval suite]] ·
[[ai/foundations/generalization-and-overfitting|overfitting]]
