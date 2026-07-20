---
title: "Data quality dimensions"
description: Data quality is multi-dimensional: accuracy, completeness, consistency, validity, timeliness, uniqueness, coverage, and label reliability.
tags: [data-for-ai, data-quality, validation]
order: 2
updated: 2026-07-20
kind: concept
level: foundational
status: current
prerequisites: [ai/data-for-ai/dataset-design-and-sampling]
last_verified: 2026-07-20
---
# Data quality dimensions

## Mechanism: intended use → quality dimension → acceptance test

```python
quality = {"completeness": .98, "timeliness_days": 1}
print("pass" if quality["completeness"] >= .95 and quality["timeliness_days"] <= 2 else "hold")
```

Run with `python3`; expected output is `pass`. Define accuracy, completeness, consistency, timeliness, coverage, provenance, and representativeness against the decision they support—not as universal scores.

## Sources

- [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) — data quality and lifecycle questions.
- [Data Cascades in High-Stakes AI](https://research.google/pubs/data-cascades-in-high-stakes-ai/) — operational data failures.

"Bad data" is too vague to fix. Data quality improves when you name the dimension that
is broken and attach a validation check, owner, or review loop to it.

## Core dimensions

| Dimension | Question | Typical check |
|---|---|---|
| Accuracy | is the value or label correct? | manual audit, gold labels |
| Completeness | is required information present? | missing-field rate |
| Consistency | do fields agree across sources? | cross-table constraints |
| Validity | does the value fit the schema? | type, range, enum checks |
| Timeliness | is the data fresh enough? | age, update lag |
| Uniqueness | are records duplicated? | exact and fuzzy duplicate detection |
| Coverage | are important slices represented? | slice counts and performance |
| Reliability | do labels agree? | inter-annotator agreement |

## AI-specific quality signals

- Ambiguous examples that even experts cannot label consistently.
- Distribution shift between training, evaluation, and production.
- Shortcuts or spurious features that models can exploit.
- Benchmark contamination or duplicate examples across splits.
- Data provenance that is unknown or legally risky.

## Validation belongs in the pipeline

Data quality checks should run before training, eval, fine-tuning, retrieval indexing,
and production ingestion. Great Expectations-style assertions are useful because they
make quality expectations executable.

## Pitfall

Do not optimize only for clean-looking rows. A dataset can pass schema validation while
still missing the users, edge cases, and failure modes that matter.

**Connects to:** [[ai/foundations/distribution-shift|distribution shift]] ·
[[ai/machine-learning/ml-pipelines-and-leakage|pipeline leakage]] ·
[[ai/data-for-ai/dataset-design-and-sampling|dataset design]]
