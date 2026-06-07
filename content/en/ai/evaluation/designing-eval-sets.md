---
title: "Designing eval sets"
description: A useful eval set is representative, sliceable, versioned, and protected from leakage into prompts, training, or tuning.
tags: [evaluation, datasets, golden-set, leakage]
order: 2
updated: 2026-06-07
---
# Designing eval sets

An eval set is a curated sample of tasks that represents the behavior you care
about. The goal is not size alone; the goal is decision quality when comparing
prompts, models, retrieval strategies, fine-tunes, or product releases.

## What goes into a golden set

- Real user cases from traces, support tickets, sales calls, QA, and internal dogfooding.
- Known edge cases that have broken the system before.
- High-value or high-risk workflows, not only average traffic.
- Negative cases where the system should refuse, ask for clarification, or escalate.
- Expected answers, references, rubrics, or deterministic checks for grading.
- Metadata for slices: intent, difficulty, domain, language, customer tier, document type.

## Keep splits and versions clean

| Set | Purpose | Rule |
|---|---|---|
| Dev set | fast iteration | okay to inspect often |
| Regression set | release gates | change deliberately and review diffs |
| Holdout set | honest comparison | do not tune on it |
| Production sample | drift and freshness | sampled continuously |

This mirrors [[ai/foundations/data-splits-and-leakage|data split discipline]]: once a
case guides tuning, it is no longer a pure test of generalization.

## Size and coverage

- Start with 30-100 cases that match the main workflow.
- Add slices before adding random volume.
- Track every case with an owner, source, expected behavior, and last reviewed date.
- Prefer small high-signal suites in CI and larger suites for nightly or release runs.

## In practice

Each production incident should either become an eval case or be explicitly rejected
as not worth guarding. That turns failures into durable regression protection.

**Connects to:** [[ai/evaluation/prompt-regression-testing|prompt regression testing]] ·
[[ai/mlops/feedback-loops|feedback loops]] ·
[[ai/fine-tuning-and-alignment/building-the-finetuning-dataset|dataset building]]
