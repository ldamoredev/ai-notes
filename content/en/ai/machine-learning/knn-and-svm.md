---
title: "kNN & SVM: distance and margins"
description: Two classic ideas with long shadows — nearest-neighbor as the ancestor of vector search, and the margin intuition behind SVMs.
tags: [machine-learning, knn, svm, kernels]
order: 5
updated: 2026-06-07
---
# kNN & SVM: distance and margins

Two older algorithms worth keeping because their core ideas reappear everywhere in
modern AI — kNN is the conceptual ancestor of vector search, and the SVM margin is
a clean lens on generalization.

## k-Nearest Neighbors — "you are your neighbors"

To classify a point, find the `k` closest training points and take a majority vote
(or average, for regression). There's no real "training" — it just stores the data
and computes distances at query time.

- **Strength**: dead simple; a decent nonparametric baseline.
- **Weakness**: slow at prediction (compares to everything), and it suffers from the
  [[ai/foundations/features-and-dimensionality|curse of dimensionality]] — distances
  lose meaning in high dimensions.
- **Why it matters today**: [[ai/rag-and-retrieval/index|RAG and semantic search]]
  are kNN over [[ai/mathematics-for-ai/vectors-matrices-and-tensors|embeddings]], made fast with
  approximate nearest-neighbor indexes (HNSW). The idea scaled; the brute force
  didn't.

## Support Vector Machines — the widest street

An SVM finds the decision boundary with the **largest margin** — the widest gap
between classes. Maximizing that margin is a built-in
[[ai/foundations/inductive-bias-and-no-free-lunch|inductive bias]] toward
generalization. Only the boundary-defining points (the *support vectors*) matter.

The **kernel trick** lets an SVM draw nonlinear boundaries by implicitly mapping
data into a higher-dimensional space without computing the coordinates — elegant,
and strong on small/medium datasets with clear margins.

## When to use which

| | Good for | Watch out |
|---|---|---|
| **kNN** | small data, a quick baseline, recommendation-style lookups | high dimensions, large datasets (slow) |
| **SVM** | small/medium, clean-margin problems | scaling required; tuning C/kernel; large data is slow |

On large tabular data, [[ai/machine-learning/decision-trees-and-ensembles|gradient-boosted
trees]] usually beat both — but the distance/margin intuitions stay useful.

**Connects to:** [[ai/rag-and-retrieval/index|vector search]] ·
[[ai/foundations/features-and-dimensionality|high dimensions]] ·
[[ai/mathematics-for-ai/vectors-matrices-and-tensors|distance & similarity]]
