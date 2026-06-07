---
title: "Data quality dimensions"
description: Data quality is multi-dimensional: accuracy, completeness, consistency, validity, timeliness, uniqueness, coverage, and label reliability.
tags: [data-for-ai, data-quality, validation]
order: 2
updated: 2026-06-07
---
# Data quality dimensions

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
