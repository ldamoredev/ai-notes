---
title: "Embeddings & latent spaces"
description: An embedding is a dense vector where geometry encodes meaning; cosine similarity is the mechanism, and it only means anything within the model that produced the space.
tags: [deep-learning, embeddings, latent-space, representation-learning]
order: 9
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/mathematics-for-ai/vectors-matrices-and-tensors]
last_verified: 2026-07-20
translation: stale
---
# Embeddings & latent spaces

**Mental model:** a trained network maps inputs into a **latent space** — a vector
space where position encodes meaning. Get a good space and a dozen downstream tasks
(search, clustering, transfer, analogy) become geometry problems instead of learning
problems. The space is arbitrary — it only means something relative to itself, never
across two different models.

## Mechanism: similarity is a dot product

An **embedding** is a dense vector \(v \in \mathbb{R}^d\) that represents an item. The
network is trained so related items land close together and unrelated items land far
apart, measured by cosine similarity:

\[
\cos(u, v) = \frac{u \cdot v}{\lVert u \rVert \lVert v \rVert}.
\]

This ranges from \(-1\) (opposite direction) to \(1\) (identical direction),
independent of vector magnitude — which is exactly why it is normalized before
comparison: two vectors pointing the same way but with different lengths should still
be judged as maximally similar.

## Worked example: analogy as vector arithmetic

Toy 2D embeddings chosen to make the arithmetic exact:
\(\text{king}=(4,3)\), \(\text{man}=(3,1)\), \(\text{woman}=(2,3)\). Compute the
analogy vector:

\[
r = \text{king} - \text{man} + \text{woman} = (4{-}3{+}2,\; 3{-}1{+}3) = (3, 5).
\]

Compare \(r\) against three candidates using cosine similarity: `queen=(3,5)`,
`prince=(5,2)`, `dog=(-1,-4)`.

| Candidate | Cosine similarity to `r` |
|---|---:|
| `queen` | **1.000** |
| `prince` | 0.796 |
| `dog` | -0.957 |

`r` matches `queen` exactly and is clearly more similar to `prince` than to the
unrelated `dog` — this is the entire mechanism behind "king − man + woman ≈ queen"
and behind semantic search: encode a query, compute similarity against a set of
candidate vectors, return the nearest ones.

## Executable artifact

Run with `python3`; expected output is `queen 1.0`, `prince 0.796`, `dog -0.957`:

```python
import math

def cosine(u, v):
    dot = sum(a * b for a, b in zip(u, v))
    nu = math.sqrt(sum(a * a for a in u))
    nv = math.sqrt(sum(a * a for a in v))
    return dot / (nu * nv)

king, man, woman = (4, 3), (3, 1), (2, 3)
r = tuple(k - m + w for k, m, w in zip(king, man, woman))

candidates = {"queen": (3, 5), "prince": (5, 2), "dog": (-1, -4)}
for name, vec in candidates.items():
    print(name, round(cosine(r, vec), 3))
```

## Why this matters everywhere

- **Transfer learning** — features learned on a large dataset transfer to new tasks
  with little data; [[ai/fine-tuning-and-alignment/index|fine-tuning]] keeps the
  representation and retargets only the head.
- **Semantic search / [[ai/rag-and-retrieval/index|RAG]]** — embed query and
  documents, retrieve by nearest neighbor in the same space.
- **Clustering & visualization** — group or project embeddings to see structure the
  model learned, using [[ai/machine-learning/clustering-and-pca|clustering or
  dimensionality reduction]].
- **Multimodal** — train text and images into a *shared* space (CLIP) so vectors from
  either modality can be compared directly by the same cosine mechanism.

## What vector-database defaults hide

A vector index (HNSW, IVF) reports a ranked list of nearest neighbors as if distance
were an absolute, portable quantity. It is not: the same two documents embedded by two
different model versions produce two different, incomparable spaces — an index
silently mixing vectors from an old and a new model returns results that are
geometrically meaningless, with no error raised anywhere in the stack.

## Failure modes and a decision rule

- **Cross-model comparison.** Comparing a vector from model A against a vector from
  model B is meaningless even if both are 768-dimensional — the axes carry unrelated
  meaning. Re-embed the entire corpus whenever the embedding model or its version
  changes.
- **Skipping normalization.** Cosine similarity assumes the comparison is
  direction-only; feeding un-normalized vectors into a dot-product-only index silently
  turns "similarity" into "similarity times magnitude," which is a different ranking.
- **Curse of dimensionality.** In very high dimensions, distances between random
  points concentrate and lose discriminative power; retrieval quality depends on the
  embedding model actually structuring that space well, not just on raw dimension
  count.
- **Anisotropy.** Raw transformer hidden states are not uniformly distributed in all
  directions; comparing them directly without a dedicated similarity-trained embedding
  head or whitening step underperforms a model actually trained for retrieval.

**Decision rule:** store the exact embedding model name and version alongside every
vector in an index, and treat a model upgrade as a full re-embedding job, not a
config change. Use a model specifically trained for retrieval/similarity (not raw
hidden states from a generative model) whenever ranking quality matters.

## Exercises

1. Compute `king − man + woman` for embeddings of your own choosing (any 3D vectors)
   and find which of two candidate vectors it is closer to by cosine similarity.
2. Add un-normalized magnitude to the `dog` vector (multiply it by 10) and show that
   cosine similarity to `r` is unchanged while raw dot product is not.
3. Explain, using the mechanism above, why re-indexing an entire vector database is
   required after switching embedding providers — not just re-embedding new documents.

**Connects to:** [[ai/mathematics-for-ai/vectors-matrices-and-tensors|vectors & similarity]] · [[ai/rag-and-retrieval/vector-databases-and-indexes|vector indexes]] · [[ai/foundations/features-and-dimensionality|representations]] · [[ai/deep-learning/loss-functions-in-dl|contrastive loss]]

## Sources

- [Distributed Representations of Words and Phrases and their Compositionality](https://arxiv.org/abs/1310.4546) — the word2vec paper and the original analogy-arithmetic result.
- [Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/abs/2103.00020) — CLIP, a shared text-image latent space trained by contrastive similarity.
- [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401) — nearest-neighbor retrieval over an embedding space used to ground generation.
- [pgvector](https://github.com/pgvector/pgvector) — practical ANN indexing and distance-metric controls for embedding search.
