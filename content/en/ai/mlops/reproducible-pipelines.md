---
title: "Reproducible pipelines"
description: Reproducible ML pipelines make data, transforms, training, evals, and artifacts rerunnable with controlled inputs.
tags: [mlops, pipelines, reproducibility]
order: 4
updated: 2026-06-07
---
# Reproducible pipelines

A reproducible pipeline lets you rerun the same data transformations, training job,
evals, and artifact packaging with known inputs. Without it, every model is a one-off
experiment that cannot be trusted or debugged.

## Pipeline stages

- Ingest raw data and record source versions.
- Validate schema, ranges, and missingness.
- Transform features or build retrieval indexes.
- Train or adapt the model.
- Run evaluation and regression checks.
- Package artifacts and register release candidates.

Each stage should have explicit inputs and outputs. Hidden notebooks and manual copy
steps are where production bugs hide.

## Determinism where it matters

Perfect determinism is not always possible with GPU training, but reproducibility is
still practical: fixed code version, frozen data snapshot, recorded seeds, pinned
dependencies, and stable config.

## LLM pipeline additions

LLM pipelines often include prompt compilation, eval-set generation, retrieval-index
builds, judge prompts, and trace replay. Treat these as first-class stages, not side
scripts.

## Pitfall

If you cannot rebuild the artifact, you cannot safely patch it. Reproducibility is not
academic neatness; it is incident response.

**Connects to:** [[ai/machine-learning/ml-pipelines-and-leakage|ML pipelines and leakage]] ·
[[ai/rag-and-retrieval/chunking|chunking]] ·
[[ai/mlops/experiment-tracking|experiment tracking]]
