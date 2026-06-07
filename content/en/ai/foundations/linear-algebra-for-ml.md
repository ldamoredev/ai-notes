---
title: "Linear algebra intuition: the dot product as similarity"
description: The minimum linear algebra that actually shows up in ML — vectors as meaning, matrices as transforms, and the dot product as similarity.
tags: [foundations, linear-algebra, embeddings, math]
order: 9
updated: 2026-06-07
---
# Linear algebra intuition: the dot product as similarity

You don't need to compute eigenvalues by hand to do ML, but a few geometric
intuitions pay off forever. The big one: **almost every "similarity" in modern AI
is a dot product.**

## Vectors carry meaning

A vector is a list of numbers, but think of it as a **point/arrow in space**. In
ML, an [[ai/deep-learning/index|embedding]] places each item (word, image, user)
at a point such that *related items land near each other*. Meaning becomes
geometry: "king − man + woman ≈ queen" works because directions in the space
encode concepts.

## The dot product = alignment

For two vectors, the dot product measures how much they point the same way:

- Large positive → similar direction (similar meaning).
- Near zero → orthogonal (unrelated).
- Negative → opposing.

**Cosine similarity** is just the dot product after normalizing length, so it
measures *direction only* — the workhorse of semantic search and
[[ai/rag-and-retrieval/index|retrieval]]. When a vector database "finds similar
chunks," it is ranking by dot product / cosine.

## Matrices transform space

A matrix multiplied by a vector **transforms** it — rotate, scale, project into a
new space. A neural network layer is exactly this: `output = activation(W·x + b)`.
Stacking layers stacks transformations, reshaping the representation step by step.

- Matrix multiplication is the single most-run operation in deep learning — it's
  why GPUs (massively parallel matrix math) matter.
- Attention in a transformer is a sequence of matrix products turning queries,
  keys, and values into weighted combinations.

## The shortlist worth internalizing

| Concept | Why it matters in ML |
|---|---|
| Vector | an embedding — meaning as coordinates |
| Dot product / cosine | similarity, the basis of search & attention |
| Matrix–vector product | one neural network layer |
| Norm (length) | magnitude; normalize before comparing directions |
| Projection | dimensionality reduction, decomposing signals |

**Connects to:** [[ai/foundations/features-and-dimensionality|representations]] ·
[[ai/deep-learning/index|neural networks]] ·
[[ai/rag-and-retrieval/index|embeddings & search]]
