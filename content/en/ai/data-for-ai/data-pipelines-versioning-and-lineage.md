---
title: "Data pipelines, versioning, and lineage"
description: Data pipelines need versioning and lineage so training, evaluation, retrieval, and monitoring datasets can be reproduced and audited.
tags: [data-for-ai, pipelines, lineage, versioning]
order: 9
updated: 2026-07-20
kind: implementation
level: intermediate
status: current
prerequisites: [ai/data-for-ai/datasheets-and-data-documentation]
last_verified: 2026-07-20
---
# Data pipelines, versioning, and lineage

## Mechanism: immutable input → transformation version → output manifest

```python
manifest = {"raw":"sha256:a", "transform":"clean:v3", "output":"sha256:b"}
assert len(manifest) == 3
print("lineage is reproducible")
```

Run with `python3`; expected output is `lineage is reproducible`. Record code, configuration, environment, source snapshot, validation result, and consumer; rollback by restoring the manifest, not guessing from a mutable table.

## Sources

- [ML Metadata](https://www.tensorflow.org/tfx/guide/mlmd) — lineage metadata concepts.
- [Google Rules of ML](https://developers.google.com/machine-learning/guides/rules-of-ml) — data-pipeline discipline.

AI teams need to know exactly which data produced a model, eval score, vector index, or
product behavior. Versioning and lineage turn datasets from loose files into auditable
artifacts.

## What to version

- Raw source snapshots.
- Cleaning and filtering rules.
- Labeling guidelines and label batches.
- Train, validation, test, and holdout splits.
- Feature definitions and transformations.
- Retrieval indexes and embedding model versions.
- Eval cases, rubrics, judge prompts, and expected outputs.

## Lineage questions

| Question | Why it matters |
|---|---|
| Which source produced this example? | provenance and licensing |
| Which pipeline transformed it? | reproducibility |
| Which split contains it? | leakage control |
| Which model or index used it? | impact analysis |
| Which user or tenant can access it? | authorization |

## Operational pattern

1. Treat datasets as build artifacts with IDs.
2. Store code, config, source snapshot, and output manifest together.
3. Run validation checks before publishing a dataset version.
4. Attach dataset versions to model, prompt, and index versions.
5. Keep changelogs for additions, removals, relabeling, and filtering.

## Pitfall

If a dataset cannot be rebuilt, a model cannot really be reproduced. A CSV in a shared
folder is not lineage.

**Connects to:** [[ai/mlops/reproducible-pipelines|reproducible pipelines]] ·
[[ai/mlops/feature-stores|feature stores]] ·
[[ai/mlops/model-and-prompt-registry|model and prompt registry]]
