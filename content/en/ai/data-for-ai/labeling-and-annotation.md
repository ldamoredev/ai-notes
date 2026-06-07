---
title: "Labeling and annotation"
description: Reliable labels require clear guidelines, calibrated annotators, disagreement handling, audits, and sometimes weak supervision.
tags: [data-for-ai, labeling, annotation]
order: 3
updated: 2026-06-07
---
# Labeling and annotation

Labels are product decisions encoded as data. If annotators do not share the same task
definition, the model learns inconsistency and the eval suite becomes unreliable.

## Build labeling guidelines

- Define each label with inclusion and exclusion rules.
- Include positive, negative, borderline, and confusing examples.
- Explain what to do when evidence is missing.
- Specify whether annotators should infer intent or use only visible evidence.
- Version guidelines and record which version produced each label batch.

## Measure agreement

| Signal | Meaning |
|---|---|
| Inter-annotator agreement | whether humans interpret the task consistently |
| Adjudication rate | how often expert review is needed |
| Gold-question accuracy | whether annotators remain calibrated |
| Drift over time | whether label behavior changes between batches |

Disagreement is not always annotator error. It can reveal an ambiguous taxonomy or a
task that needs more context.

## Weak supervision and model-assisted labeling

- Use heuristic rules for obvious cases.
- Use model pre-labels to speed up humans, not to remove review blindly.
- Track whether model-assisted labels introduce systematic bias.
- Keep a high-quality hand-labeled set for calibration and evaluation.

## Pitfall

Cheap labels can be expensive if they train the model toward the wrong behavior. Audit
labels by slice, not only by aggregate agreement.

**Connects to:** [[ai/evaluation/human-evaluation|human evaluation]] ·
[[ai/fine-tuning-and-alignment/building-the-finetuning-dataset|fine-tuning datasets]] ·
[[ai/data-for-ai/datasheets-and-data-documentation|data documentation]]
