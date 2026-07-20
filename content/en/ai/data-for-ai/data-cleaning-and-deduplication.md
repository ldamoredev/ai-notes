---
title: "Data cleaning and deduplication"
description: Cleaning and deduplication remove invalid, stale, duplicated, contradictory, and low-value examples before they distort training or evaluation.
tags: [data-for-ai, cleaning, deduplication]
order: 5
updated: 2026-07-20
kind: implementation
level: intermediate
status: current
prerequisites: [ai/data-for-ai/data-pipelines-versioning-and-lineage]
last_verified: 2026-07-20
---
# Data cleaning and deduplication

## Mechanism: raw record → quality rule → versioned accepted/rejected set

```python
rows = ["a", "a", "b", ""]
print(sorted({r.strip() for r in rows if r.strip()}))
```

Run with `python3`; expected output is `['a', 'b']`. Preserve raw data, rules, rejected records, and versions; deduplication can erase rare but legitimate examples or hide train/test leakage.

## Sources

- [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) — collection and maintenance documentation.
- [Data Cleaning: Problems and Current Approaches](https://dl.acm.org/doi/10.1145/2776241) — data-quality mechanisms.

Data cleaning is not cosmetic. Invalid rows, duplicated examples, contradictory labels,
and stale records can dominate training gradients, inflate eval scores, or make failures
impossible to diagnose.

## Cleaning checks

- Schema validity: types, enums, ranges, required fields.
- Text quality: encoding problems, boilerplate, broken markup, language mismatch.
- Label integrity: impossible labels, contradictory labels, missing adjudication.
- Entity consistency: IDs, timestamps, joins, and references agree.
- Freshness: examples are within the intended time window.
- Authorization: examples can legally and ethically be used for the purpose.

## Deduplication levels

| Level | Example |
|---|---|
| Exact duplicate | identical row or document |
| Near duplicate | same article with minor formatting changes |
| Semantic duplicate | same question or answer phrased differently |
| Entity duplicate | same user/account/item appears across splits |
| Benchmark duplicate | eval item appears in training or prompt examples |

## Practical workflow

1. Run automatic validation before manual review.
2. Remove exact duplicates and obvious invalid records.
3. Cluster near-duplicates for review.
4. Check duplicates across training, validation, test, and holdout.
5. Record every cleaning rule in the dataset version.

## Pitfall

Over-cleaning can erase hard cases. Do not remove examples merely because they are
messy if messy inputs are part of the real product distribution.

**Connects to:** [[ai/data-for-ai/data-quality-dimensions|data quality]] ·
[[ai/foundations/data-splits-and-leakage|split leakage]] ·
[[ai/data-for-ai/data-contamination-and-benchmark-leakage|benchmark leakage]]
