---
title: "Building the fine-tuning dataset"
description: A fine-tuning dataset is a product specification in examples: schema, sampling, splits, quality checks, and held-out evals.
tags: [fine-tuning, dataset, data-pipeline]
order: 8
updated: 2026-06-07
---
# Building the fine-tuning dataset

A fine-tuning dataset is not a dump of chats. It is a product specification expressed
as examples: what the model should see, how it should respond, and which edge cases
matter.

## Start from the behavior spec

Before writing examples, define:

- The task boundary: what the model should and should not do.
- The expected input shape: user message, context, tool results, system prompt.
- The output contract: prose, JSON, citations, refusal, or tool call.
- The policy behavior: what to do with unsafe, ambiguous, or unsupported requests.
- The evaluation criteria: what counts as better.

## Build the rows

Each row should be complete enough to train the behavior without hidden assumptions.

| Dataset field | Why it matters |
|---|---|
| Messages / prompt | Recreates production context |
| Ideal response | Demonstrates the target behavior |
| Metadata | Tracks source, reviewer, scenario, difficulty |
| Split | Prevents train/eval leakage |
| Version | Makes experiments reproducible |

## Split before iteration

Create train, validation, and test splits early. Keep near-duplicates in the same split
so the model cannot see a memorized variant during training and appear good on eval.
For time-sensitive data, split by time.

## In practice

Start with 100 to 500 excellent examples before scaling. Train a small adapter, inspect
failures, fix the dataset, and only then grow the corpus.

**Connects to:** [[ai/fine-tuning-and-alignment/data-quality-for-finetuning|data quality]] ·
[[ai/foundations/data-splits-and-leakage|leakage]] ·
[[ai/fine-tuning-and-alignment/evaluating-a-finetune|evaluation]]
