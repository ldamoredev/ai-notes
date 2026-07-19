---
title: "Clustering & PCA: learning without labels"
description: The two most useful unsupervised tools — finding groups with k-means, and compressing/visualizing data with PCA (and when to reach for UMAP).
tags: [machine-learning, clustering, pca, unsupervised, dimensionality-reduction]
order: 10
updated: 2026-06-07
---
# Clustering & PCA: learning without labels

[[ai/foundations/types-of-learning|Unsupervised learning]] finds structure with no
answer key. Two tools cover most of the practical need: clustering (group similar
points) and dimensionality reduction (compress and visualize).

## Clustering — discover groups

- **k-means**: pick `k`, assign points to the nearest centroid, move centroids to
  the mean, repeat. Fast and ubiquitous. Caveats: you must choose `k` (use the
  elbow/silhouette method), it assumes round, similar-size clusters, and it's
  sensitive to scaling and initialization (use k-means++).
- **Hierarchical / DBSCAN**: build a tree of clusters, or find dense regions and
  label sparse points as noise (DBSCAN finds `k` itself and arbitrary shapes).

Uses: customer segmentation, deduplication, exploratory analysis, grouping
[[ai/mathematics-for-ai/vectors-matrices-and-tensors|embeddings]] to see what a model "thinks" is
similar.

## PCA — compress along the directions that matter

Principal Component Analysis finds the orthogonal directions of **maximum variance**
and re-expresses the data in those coordinates. Keep the top few components and you
shrink dimensions while preserving most of the signal.

- Fights the [[ai/foundations/features-and-dimensionality|curse of dimensionality]]
  and decorrelates features.
- Speeds up downstream models and enables 2-D/3-D visualization.
- It's **linear** — it can't unfold curved structure.

## PCA vs UMAP/t-SNE for visualization

| Tool | Best for | Note |
|---|---|---|
| **PCA** | fast reduction, preprocessing, global structure | linear; components are interpretable |
| **UMAP / t-SNE** | 2-D visualization of clusters | nonlinear; great visuals but distances/cluster sizes can mislead |

> Use PCA to *reduce and decorrelate*; use UMAP/t-SNE to *look* — and never read
> exact distances off a t-SNE plot.

## Pitfall

Always scale features before k-means and PCA — both are distance/variance based, so
an unscaled large-range feature dominates everything.

**Connects to:** [[ai/foundations/features-and-dimensionality|dimensionality]] ·
[[ai/foundations/types-of-learning|unsupervised learning]] ·
[[ai/deep-learning/index|learned representations]]
