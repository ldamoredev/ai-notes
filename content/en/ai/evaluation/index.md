---
title: Evaluation
description: Evaluation patterns for LLM products, RAG systems, agents, judges, datasets, metrics, and regression checks.
tags: [evaluation, evals, quality]
order: 0
updated: 2026-06-07
---
# Evaluation

Evaluation is the control system for AI work. It turns product behavior, model
quality, safety, cost, latency, and user trust into things that can be measured,
compared, and improved without tuning by vibes.

## Mental model

An evaluation is an instrument tied to a decision. It samples cases, applies measurements or judgments, aggregates uncertainty, and determines whether a candidate system clears a product, safety, or operational threshold. A benchmark score without that decision context is incomplete evidence.

## Roadmap: evaluation foundations

- [[ai/evaluation/model-vs-product-evals|Model vs product evals]] separates benchmark quality from the product contract users experience.
- [[ai/evaluation/designing-eval-sets|Designing eval sets]] explains golden datasets, slices, and leakage control.
- [[ai/evaluation/metrics-for-llm-evals|Metrics for LLM evals]] maps exact, semantic, groundedness, and cost metrics.
- [[ai/evaluation/task-specific-evals|Task-specific evals]] turns "good output" into a rubric for each workflow.

## Judges, humans, and benchmarks

- [[ai/evaluation/llm-as-judge|LLM-as-judge]] covers rubric-based grading and judge bias.
- [[ai/evaluation/human-evaluation|Human evaluation]] designs review workflows that are consistent and useful.
- [[ai/evaluation/public-benchmarks-and-limits|Public benchmarks and limits]] explains when external benchmarks help and when they mislead.

## Regression and failure analysis

- [[ai/evaluation/prompt-regression-testing|Prompt regression testing]] treats prompts as versioned product logic.
- [[ai/evaluation/systematic-error-analysis|Systematic error analysis]] turns failures into an improvement backlog.
- [[ai/evaluation/hallucination-detection|Hallucination detection]] separates unsupported claims from merely imperfect wording.

## System evals

- [[ai/evaluation/evaluating-rag-systems|Evaluating RAG systems]] decomposes retriever, context, generator, and citation quality.
- [[ai/evaluation/evaluating-agent-systems|Evaluating agent systems]] scores outcomes, trajectories, tool use, and autonomy control.
- [[ai/ai-product-engineering/evals-inside-the-product|Evals inside the product]] shows where these checks live in delivery.

## Practice & process

- [[ai/evaluation/eval-driven-development|Eval-driven development]] makes the eval set the spec you build against, like unit tests for AI.
- [[ai/evaluation/nondeterminism-and-reproducibility|Nondeterminism & reproducibility]] explains why the same input varies and how to test for distributions.

**Connects to:** [[ai/research-and-experimentation/index|Research and Experimentation]] · [[ai/ai-product-engineering/evals-inside-the-product|Evals Inside the Product]] · [[ai/interpretability/index|Interpretability]]

## Core sources

- [HELM](https://crfm.stanford.edu/helm/) — transparent multi-scenario evaluation with explicit metrics and limitations.
- [Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685) — empirical analysis of model judges and their biases.
- [RAGAS](https://docs.ragas.io/) — component metrics for retrieval-augmented systems.
- [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/) — connects offline evidence to production readiness.
- [Statistical Comparisons of Classifiers over Multiple Data Sets](https://jmlr.org/papers/v7/demsar06a.html) — practical statistical guidance for comparing models.
