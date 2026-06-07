---
title: "Dataset design and sampling"
description: Dataset design decides which distribution, slices, negatives, and splits a model learns from and is evaluated against.
tags: [data-for-ai, sampling, splits]
order: 4
updated: 2026-06-07
---
# Dataset design and sampling

A dataset is not a random pile of examples. It is an engineered sample of a task,
distribution, user population, time period, and risk surface.

## Design questions

- What real-world distribution should the dataset represent?
- Which slices are high-value, high-risk, rare, or historically underserved?
- Which negative examples should the model learn to reject?
- Which examples belong in training, evaluation, holdout, or production monitoring?
- What metadata is needed for slice-level analysis?

## Sampling strategies

| Strategy | Use when | Watch for |
|---|---|---|
| Random sample | estimating average performance | rare failures disappear |
| Stratified sample | important slices need representation | slice weights must be tracked |
| Hard-negative sample | model confuses similar cases | overfitting to edge cases |
| Time-based split | production changes over time | less data for training |
| User or entity split | leakage across related records is possible | smaller effective sample |

## Split design

Use splits that match the leakage risk. For users, accounts, documents, products, or
time-series data, random row splits can leak near-duplicates or future information into
evaluation.

## Pitfall

Balancing a dataset can improve learning but distort product expectations. Keep both
the sampling policy and the real production base rates visible.

**Connects to:** [[ai/foundations/data-splits-and-leakage|data splits and leakage]] ·
[[ai/machine-learning/class-imbalance|class imbalance]] ·
[[ai/evaluation/designing-eval-sets|eval set design]]
