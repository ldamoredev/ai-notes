---
title: "Direct Preference Optimization"
description: DPO aligns a model from chosen/rejected response pairs without training a separate reward model or running PPO.
tags: [alignment, dpo, preference-learning, rlhf]
order: 6
updated: 2026-06-07
---
# Direct Preference Optimization

Direct Preference Optimization (DPO) is a simpler preference-alignment method: given a
prompt, a chosen response, and a rejected response, train the model to prefer the chosen
one directly.

## What DPO replaces

Classic RLHF trains a reward model and then optimizes a policy with PPO. DPO folds that
preference objective into supervised-style training, using pairs like:

| Field | Meaning |
|---|---|
| Prompt | The user request or task context |
| Chosen | The preferred answer |
| Rejected | The worse answer |
| Reference model | Anchor for how far the model should move |

The data still comes from human or high-quality evaluator preferences. DPO just removes
the explicit reward-model and RL loop.

## Why it became popular

- It is easier to implement and debug than PPO-based RLHF.
- It uses ordinary training infrastructure.
- It is stable enough for many instruction and style-alignment jobs.
- It makes preference data directly useful.

## What it is good for

DPO is best when you can express the improvement as "answer A is better than answer B":
tone, helpfulness, refusal quality, concision, formatting preference, or policy
behavior. It is less useful when you lack reliable preference pairs.

## Pitfall

DPO quality is capped by pair quality. If "chosen" responses are only slightly better,
or if annotators reward superficial polish over correctness, the model learns that bias.

**Connects to:** [[ai/fine-tuning-and-alignment/rlhf-with-ppo|RLHF]] ·
[[ai/fine-tuning-and-alignment/data-quality-for-finetuning|data quality]] ·
[[ai/evaluation/index|evaluation]]
