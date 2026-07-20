---
title: "Semantic caching"
description: Semantic caching reuses answers for similar requests, reducing cost and latency while introducing freshness and correctness risks.
tags: [ai-product, caching, cost, retrieval]
order: 5
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/rag-and-retrieval/embeddings-for-retrieval]
last_verified: 2026-07-20
---
# Semantic caching

## Mechanism: scoped request → similarity gate → versioned reuse or miss

```python
similarity, threshold, same_tenant = .94, .92, True
print("reuse" if similarity >= threshold and same_tenant else "compute")
```

Run with `python3`; expected output is `reuse`. Keys must include identity, permissions, model/prompt/retrieval versions, freshness, and evidence; similarity never authorizes cross-user reuse.

## Sources

- [Semantic Cache](https://arxiv.org/abs/2311.04929) — semantic caching methods for LLM applications.
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — privacy and risk controls.

Semantic caching stores responses and reuses them when a new request is meaningfully
similar to an earlier one. It can cut latency and cost, but it must be designed around
freshness, personalization, and correctness.

## Exact vs semantic cache

| Cache type | Match | Good for |
|---|---|---|
| Exact | Same key or same prompt | Deterministic transforms, repeated system tasks |
| Semantic | Embedding similarity | Repeated intents phrased differently |
| Fragment | Retrieved chunks or sub-results | RAG and tool-heavy workflows |

Semantic cache usually uses embeddings and a threshold. If the new request is close
enough to a cached request, reuse the answer or reuse part of the pipeline.

## Cache safely

- Include model, prompt, tool, and retrieval versions in the cache key.
- Avoid caching personalized or permission-sensitive outputs globally.
- Set expiration based on how fast the underlying facts change.
- Store citations and evidence with cached answers.
- Revalidate high-stakes answers instead of blindly replaying them.

## Product use cases

Semantic caching is strongest for repeated support questions, documentation answers,
classification, and expensive retrieval pipelines. It is risky for user-specific,
fresh, or regulated decisions.

## Pitfall

Similarity is not equivalence. Two questions can be semantically close but require
different answers because of time, user, permission, or context.

**Connects to:** [[ai/rag-and-retrieval/embeddings-for-retrieval|embeddings for retrieval]] ·
[[ai/mlops/cost-optimization|cost optimization]] ·
[[ai/rag-and-retrieval/grounding-and-citations|grounding]]
