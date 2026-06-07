---
title: "Features, representations & the curse of dimensionality"
description: Models don't see the world — they see features. How representation quality decides everything, and why high dimensions are weird.
tags: [foundations, features, representations, embeddings]
order: 8
updated: 2026-06-07
---
# Features, representations & the curse of dimensionality

A model never sees raw reality; it sees a **representation** — the numeric features
you feed it. The quality of that representation usually matters more than the choice
of algorithm. "Garbage in, garbage out" is really a statement about features.

## Features vs learned representations

- **Hand-engineered features** — humans decide what's relevant (word counts, ratios,
  domain signals). Classical ML lives or dies here.
- **Learned representations** — the model discovers useful features itself. This is
  what "deep" in deep learning means: each layer builds a richer representation than
  the last. [[ai/deep-learning/index|Embeddings]] are the canonical example — dense
  vectors where geometric closeness encodes semantic similarity.

The shift from hand-engineered to learned features is the central story of modern
AI, and it's why [[ai/rag-and-retrieval/index|embeddings power retrieval]].

## The curse of dimensionality

As the number of features grows, intuition built in 2-D and 3-D breaks down:

- **Sparsity** — data points become isolated; volume grows exponentially, so any
  fixed dataset becomes vanishingly sparse. You need exponentially more data to
  cover the space.
- **Distance concentration** — in very high dimensions, the distance between the
  nearest and farthest points becomes nearly equal, so "nearest neighbor" loses
  meaning. (This is why naive distance metrics struggle, and why embeddings and
  approximate nearest-neighbor indexes are engineered carefully.)
- **Overfitting risk** rises with more features relative to samples.

## The blessing on the other side

Real high-dimensional data usually lives near a **lower-dimensional manifold** —
images of faces don't fill all of pixel space, they cluster on a thin sheet within
it. Representation learning works by finding that manifold. Dimensionality
reduction (PCA, UMAP) exploits the same fact.

## Practical takeaways

- More features is not better; **relevant** features are. Prune, select, or learn.
- When distances misbehave, suspect dimensionality before the algorithm.
- A good representation makes a simple model strong; a bad one defeats a complex one.

**Connects to:** [[ai/foundations/inductive-bias-and-no-free-lunch|inductive bias]] ·
[[ai/deep-learning/index|representation learning]] ·
[[ai/rag-and-retrieval/index|embeddings & retrieval]]
