---
title: "Data contamination and benchmark leakage"
description: Contamination happens when training, prompting, or tuning data overlaps with evaluation data, making scores look better than real generalization.
tags: [data-for-ai, contamination, benchmarks, leakage]
order: 7
updated: 2026-06-07
---
# Data contamination and benchmark leakage

Data contamination happens when evaluation examples or their answers appear in training,
fine-tuning, prompts, retrieval corpora, or manual tuning workflows. The result is a
score that measures exposure, not generalization.

## Where leakage enters

- Near-duplicates across train, validation, test, and holdout sets.
- Public benchmark examples inside pretraining corpora.
- Eval answers copied into prompt examples or RAG documents.
- Human tuning that repeatedly inspects holdout failures.
- Synthetic data generated from benchmark-like prompts.
- Production feedback added to training before being removed from eval.

## Detection methods

| Method | Finds |
|---|---|
| Exact matching | copied examples and answers |
| Fuzzy matching | formatting changes and paraphrases |
| Embedding similarity | semantic near-duplicates |
| Entity split checks | same user, document, account, or item across splits |
| Timeline audit | future data leaking into past evaluation |

## Prevention

- Keep holdout sets access-restricted and versioned.
- Deduplicate across all splits and corpora.
- Separate dev evals from release or benchmark evals.
- Track provenance of prompt examples, fine-tuning rows, and RAG documents.
- Rebuild evals when they have been overused.

## Pitfall

High benchmark performance can be real capability, contamination, or both. Treat public
benchmarks as orientation and product evals as acceptance tests.

**Connects to:** [[ai/foundations/data-splits-and-leakage|data splits and leakage]] ·
[[ai/evaluation/public-benchmarks-and-limits|benchmark limits]] ·
[[ai/data-for-ai/data-cleaning-and-deduplication|deduplication]]
