---
title: "Feature stores"
description: Feature stores manage reusable, versioned features with consistent offline training and online serving semantics.
tags: [mlops, feature-store, data-pipelines]
order: 8
updated: 2026-06-07
---
# Feature stores

A feature store manages reusable model inputs so training and serving use the same
definitions. It is most useful when many models share features or when online/offline
consistency is hard.

## The core problem

In classic ML, a feature might be computed one way in a training notebook and a
slightly different way in production. That training-serving skew silently damages
model quality.

Feature stores address this by keeping:

- Feature definitions.
- Offline historical values for training.
- Online low-latency values for serving.
- Metadata, ownership, and freshness checks.

## When it helps

| Situation | Feature store value |
|---|---|
| Many models reuse the same features | Consistency and reuse |
| Low-latency predictions need fresh signals | Online serving layer |
| Point-in-time training matters | Avoids leakage |
| Teams share data transformations | Governance and ownership |

## LLM-era fit

LLM apps often rely more on retrieval/context than tabular features, but the pattern
still matters: versioned transformations, freshness, ownership, and online/offline
consistency also apply to embeddings, user context, and retrieval metadata.

## Pitfall

Do not add a feature store just because it sounds mature. If you have one model, simple
batch features, and no online reuse, a well-tested pipeline may be enough.

**Connects to:** [[ai/machine-learning/feature-engineering|feature engineering]] ·
[[ai/foundations/data-splits-and-leakage|point-in-time leakage]] ·
[[ai/rag-and-retrieval/embeddings-for-retrieval|embeddings]]
