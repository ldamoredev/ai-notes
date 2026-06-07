---
title: "Handling class imbalance"
description: When positives are rare, accuracy lies and naive training ignores the minority. Resampling, class weights, threshold tuning — and what actually helps.
tags: [machine-learning, class-imbalance, metrics, resampling]
order: 8
updated: 2026-06-07
---
# Handling class imbalance

Fraud, disease, defects, churn — the cases you care about are often rare. With a
99:1 split, a model that always predicts the majority is 99% accurate and useless.
Imbalance touches metrics, training, and the decision threshold.

## Step 1: fix the metric first

This is the biggest lever and it's free. Drop accuracy; use metrics that focus on
the minority class — **precision, recall, F1, PR-AUC** (see
[[ai/foundations/evaluation-metrics|metrics & what they hide]]). You can't manage
what you mismeasure.

## Step 2: decide whether to rebalance

Often a good model + metric + threshold is enough. If the minority is genuinely
under-learned, rebalance — but carefully:

| Technique | What it does | Watch out |
|---|---|---|
| **Class weights** | tell the loss to penalize minority errors more | simplest; try this first |
| **Random oversampling** | duplicate minority rows | can overfit the duplicates |
| **SMOTE** | synthesize new minority points between neighbors | risky in high dimensions; can blur boundaries |
| **Undersampling** | drop majority rows | throws away data; use when majority is huge |

## Step 3: tune the threshold

A classifier outputs a probability; the **decision threshold** is yours to set. For
rare-but-costly positives, lower it to raise recall (accepting more false alarms).
This is a [[ai/foundations/evaluation-metrics|precision–recall tradeoff]] driven by
the relative cost of each error — a product decision, not a default.

## The cardinal rule

> **Resample inside the cross-validation fold, never before splitting.** Oversampling
> the whole dataset first leaks minority points into both train and validation,
> inflating scores. Do it in a [[ai/machine-learning/ml-pipelines-and-leakage|pipeline]].

Also keep the **test set at the real-world ratio** — evaluating on artificially
balanced data hides how the model behaves in production.

**Connects to:** [[ai/foundations/evaluation-metrics|precision/recall]] ·
[[ai/machine-learning/cross-validation|stratified CV]] ·
[[ai/machine-learning/ml-pipelines-and-leakage|resample in-fold]]
