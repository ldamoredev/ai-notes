---
title: "Prefix and semantic caching"
description: Prefix caching reuses repeated prompt computation, while semantic caching reuses answers for meaningfully similar requests.
tags: [inference, caching, prefix-cache, semantic-cache]
order: 10
updated: 2026-06-07
---
# Prefix and semantic caching

Caching avoids repeated inference work. In LLM systems, the two most common forms are
prefix caching at the model-serving layer and semantic caching at the product layer.

## Cache types

| Cache | Reuses | Best for |
|---|---|---|
| Prefix cache | KV cache for shared prompt prefix | repeated system prompt, few-shot examples, static context |
| Prompt/result cache | exact input-output pair | deterministic or low-variance tasks |
| Semantic cache | answer for similar meaning | repeated support, search, or FAQ-style tasks |
| Retrieval cache | retrieved chunks or reranked results | stable corpora and repeated queries |

## Prefix caching

If many requests share the same system prompt, tools, examples, or document prefix, the
serving engine can reuse prefill computation. This reduces TTFT and compute for
repeated prefixes.

## Semantic caching

Semantic caching stores responses keyed by embedding similarity or canonicalized intent.
It can save cost, but it must respect freshness, permissions, tenant isolation, and
answer correctness.

## Pitfall

Caching can leak data or serve stale answers. Always include authorization, freshness,
model version, prompt version, and context version in the cache design.

**Connects to:** [[ai/ai-product-engineering/semantic-caching|semantic caching]] ·
[[ai/rag-and-retrieval/embeddings-for-retrieval|embeddings for retrieval]] ·
[[ai/ai-safety-and-security/data-and-pii-leakage|data leakage]]
