---
title: "Evaluation metrics & what they hide"
description: Accuracy lies on imbalanced data. Precision, recall, F1, ROC-AUC — what each measures, and how to pick the metric that matches the cost of being wrong.
tags: [foundations, metrics, evaluation, precision-recall]
order: 12
updated: 2026-06-07
---
# Evaluation metrics & what they hide

A single metric is a lossy summary of a model's behavior. Picking the wrong one
makes a useless model look great — the classic trap being **accuracy on imbalanced
data**.

## Why accuracy lies

If 99% of transactions are legitimate, a model that predicts "legit" every time is
99% accurate and catches **zero** fraud. Accuracy rewards the majority class. The
moment classes are imbalanced (fraud, disease, defects), reach for something else.

## The confusion-matrix family

Everything starts from four counts: true/false positives and negatives.

| Metric | Question it answers | Use when |
|---|---|---|
| **Precision** | of the positives I flagged, how many were right? | false positives are costly (spam filter) |
| **Recall** | of the actual positives, how many did I catch? | false negatives are costly (cancer screening) |
| **F1** | harmonic mean of precision & recall | you need one balanced number |
| **ROC-AUC** | ranking quality across all thresholds | comparing models, threshold-independent |
| **PR-AUC** | precision/recall tradeoff on rare positives | heavy class imbalance |

## The precision–recall tradeoff

You can almost always trade one for the other by moving the decision **threshold**.
Lower the threshold → catch more positives (higher recall) but more false alarms
(lower precision). The "right" point depends on the **relative cost** of each error
type — a product/ethics decision, not a math one. This is why a model ships with a
*chosen threshold*, not just a probability output.

## Beyond classification

- **Regression**: MAE (robust to outliers) vs RMSE (punishes large errors). Pick
  per how much big misses hurt.
- **Ranking/retrieval**: Recall@K, MRR, NDCG — see
  [[ai/rag-and-retrieval/index|retrieval evaluation]].
- **Generative/LLM outputs**: surface metrics (ROUGE/BLEU) correlate poorly with
  quality; modern practice leans on [[ai/evaluation/index|LLM-as-judge and task
  evals]].

## Pitfall

Optimizing a single offline metric can quietly degrade the thing you actually care
about (Goodhart's law: a metric that becomes a target stops being a good metric).
Always pair the headline number with [[ai/mathematics-for-ai/probability-likelihood-and-uncertainty|calibration]]
and error analysis.

**Connects to:** [[ai/foundations/how-learning-works|loss vs metric]] ·
[[ai/evaluation/index|evaluating AI systems]] ·
[[ai/mathematics-for-ai/probability-likelihood-and-uncertainty|calibration]]
