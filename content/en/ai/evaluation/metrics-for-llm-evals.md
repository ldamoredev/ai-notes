---
title: "Metrics for LLM evals"
description: LLM systems need a mix of exact, semantic, groundedness, operational, and safety metrics instead of one universal score.
tags: [evaluation, metrics, groundedness]
order: 4
updated: 2026-06-07
---
# Metrics for LLM evals

LLM evaluation needs multiple metrics because LLM products have multiple failure
modes. A response can be correct but too slow, fluent but ungrounded, safe but
unhelpful, or well written but impossible to parse.

## Metric families

| Metric family | Measures | Best for |
|---|---|---|
| Exact checks | string match, regex, JSON schema, unit tests | structured output, extraction, tool args |
| Semantic checks | meaning similarity, rubric score, pairwise preference | open-ended answers |
| Groundedness | claims supported by provided context | RAG, summarization, support answers |
| Retrieval metrics | recall@k, MRR, NDCG | search and RAG context selection |
| Operational metrics | latency, cost, tokens, retries, error rate | production quality |
| Safety metrics | refusal quality, policy compliance, leakage | risky or regulated workflows |

No single metric represents "good AI". Choose metrics from the product contract.

## Exact vs semantic

- Use exact checks when the output has a contract: JSON shape, labels, numbers, SQL, tool arguments, citations.
- Use semantic checks when many correct phrasings exist.
- Use groundedness checks when the answer must be supported by retrieved or supplied evidence.
- Use operational checks when a better answer is not better if it is too slow or expensive.

## Thresholds and tradeoffs

Metrics become release gates only after you choose thresholds. A support answer might
require high groundedness and medium completeness; a brainstorming tool might tolerate
lower groundedness but require helpfulness and low latency.

## Pitfall

Surface overlap metrics can reward wording similarity while missing factual failure.
They are useful for narrow tasks, but poor substitutes for groundedness, task success,
or human judgment.

**Connects to:** [[ai/foundations/evaluation-metrics|classic metrics]] ·
[[ai/evaluation/llm-as-judge|LLM-as-judge]] ·
[[ai/evaluation/model-vs-product-evals|product evals]]
