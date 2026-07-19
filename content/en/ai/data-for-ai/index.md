---
title: Data for AI
description: Data-centric AI - the quality, labeling, design, and documentation of datasets that quietly decide whether any model works.
tags: [data, data-centric-ai, datasets]
order: 0
updated: 2026-06-07
---
# Data for AI

[[ai/foundations/index|Foundations]] covers the concepts and
[[ai/machine-learning/index|Machine Learning]] covers the methods, but in practice the
**data** is where projects are won or lost. This branch is the data-centric view:
treating the dataset, not the model, as the primary thing you iterate on.

## Mental model

Data is a sampled, transformed, and governed measurement of the world—not the world itself. Dataset quality is therefore coverage plus provenance: what was observed, what was omitted, how labels were produced, which transformations ran, and whether deployment inputs still match those assumptions.

## Roadmap: data quality and design

- [[ai/data-for-ai/data-centric-ai|Data-centric AI]] explains why improving data often beats changing the model.
- [[ai/data-for-ai/data-quality-dimensions|Data quality dimensions]] defines accuracy, completeness, consistency, freshness, coverage, and validity.
- [[ai/data-for-ai/dataset-design-and-sampling|Dataset design and sampling]] covers representativeness, splits, balance, and slice coverage.
- [[ai/data-for-ai/data-cleaning-and-deduplication|Data cleaning and deduplication]] shows how messy examples become training and evaluation failures.

## Labels, documentation, and feedback

- [[ai/data-for-ai/labeling-and-annotation|Labeling and annotation]] covers guidelines, inter-annotator agreement, weak supervision, and review loops.
- [[ai/data-for-ai/datasheets-and-data-documentation|Datasheets and data documentation]] records provenance, collection, limits, and intended use.
- [[ai/data-for-ai/feedback-data-and-active-learning|Feedback data and active learning]] turns production mistakes into better datasets.

## LLM-era data

- [[ai/data-for-ai/synthetic-data|Synthetic data]] explains where generated examples help and where they collapse quality.
- [[ai/data-for-ai/data-contamination-and-benchmark-leakage|Data contamination and benchmark leakage]] protects evaluation from hidden training exposure.
- [[ai/data-for-ai/data-for-llms|Data for LLMs]] covers pretraining corpora, filtering, mixture design, and deduplication at scale.

## Data operations and governance

- [[ai/data-for-ai/data-pipelines-versioning-and-lineage|Data pipelines, versioning, and lineage]] keeps datasets reproducible and auditable.
- [[ai/data-for-ai/privacy-and-pii-in-datasets|Privacy and PII in datasets]] handles consent, minimization, anonymization, and access boundaries.

## Data strategy

- [[ai/data-for-ai/the-data-flywheel|The data flywheel]] turns usage into a compounding loop of better data and a better product.

**Connects to:** [[ai/foundations/data-splits-and-leakage|Data Splits and Leakage]] · [[ai/machine-learning/index|Statistical Machine Learning]] · [[ai/ai-ethics-and-governance/index|AI Ethics and Governance]]

## Core sources

- [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) — provenance and lifecycle documentation for datasets.
- [Data Cards](https://research.google/pubs/data-cards-purposeful-and-transparent-dataset-documentation-for-responsible-ai/) — structured communication of dataset context and limitations.
- [Hidden Technical Debt in Machine Learning Systems](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems) — data dependencies and feedback loops as systems debt.
- [The Curse of Recursion](https://arxiv.org/abs/2305.17493) — synthetic-data feedback and model-collapse analysis.
- [Hugging Face Datasets](https://huggingface.co/docs/datasets/) — reproducible loading, processing, streaming, and dataset metadata.
