---
title: "Embeddings & latent spaces"
description: Neural nets turn things into vectors where geometry means something. Embeddings and the latent space are why transfer learning, search, and clustering all work.
tags: [deep-learning, embeddings, latent-space, representation-learning]
order: 9
updated: 2026-06-07
---
# Embeddings & latent spaces

The deepest payoff of deep learning is the **representation** it learns. A trained
network maps inputs into a **latent space** — a vector space where position encodes
meaning. Get a good space and a dozen downstream tasks become easy.

## What an embedding is

An **embedding** is a dense vector that represents an item (word, sentence, image,
user). The network learns to place related items close together and unrelated items
far apart, so [[ai/foundations/linear-algebra-for-ml|distance and direction]] carry
semantics: similar things → small cosine distance; concept directions become
arithmetic ("king − man + woman ≈ queen").

Compared to one-hot/sparse encodings, embeddings are **dense, low-dimensional, and
generalize** — they capture similarity instead of treating every item as unrelated.

## The latent space

Internally, each hidden layer is a latent space; the network progressively reshapes
the input into a representation where the final [[ai/machine-learning/linear-and-logistic-regression|linear
layer]] can do its job. A frontier model's hidden states *are* a giant learned latent
space for language.

## Why this matters everywhere

- **Transfer learning** — features learned on a huge dataset transfer to new tasks
  with little data. Fine-tuning and [[ai/fine-tuning-and-alignment/index|adaptation]]
  exploit this: keep the representation, retarget the head.
- **Semantic search / [[ai/rag-and-retrieval/index|RAG]]** — embed query and
  documents, retrieve by nearest neighbor. This is the engine of modern retrieval.
- **Clustering & visualization** — group or [[ai/machine-learning/clustering-and-pca|project]]
  embeddings to see structure the model learned.
- **Multimodal** — train text and images into a *shared* space (CLIP) so they can be
  compared directly.

## Pitfall

Embeddings are only meaningful **within the model that produced them** — never
compare vectors from two different embedding models, and re-embed everything when you
change models. Also: cosine similarity assumes normalized vectors; normalize before
comparing.

**Connects to:** [[ai/foundations/linear-algebra-for-ml|vectors & similarity]] ·
[[ai/rag-and-retrieval/index|retrieval]] ·
[[ai/foundations/features-and-dimensionality|representations]]
