---
title: MLOps
description: Operating ML and LLM systems in production — experiments, registries, pipelines, monitoring, observability, serving, cost, HITL, and feedback loops.
tags: [mlops, llmops, production, monitoring]
order: 0
updated: 2026-06-07
---
# MLOps

MLOps is the discipline of making model systems reproducible, observable, deployable,
and improvable after they leave the notebook. For LLM apps, the same discipline extends
to prompts, retrieval, tools, traces, and product feedback.

> The model is only one artifact. Production quality comes from the system around it:
> data, prompts, evals, releases, monitoring, rollback, and learning loops.

## Operating model

- [[ai/mlops/mlops-to-llmops|MLOps to LLMOps]]
- [[ai/mlops/experiment-tracking|Experiment tracking]]
- [[ai/mlops/model-and-prompt-registry|Model and prompt registry]]
- [[ai/mlops/reproducible-pipelines|Reproducible pipelines]]

## Production controls

- [[ai/mlops/monitoring-and-drift|Monitoring and drift]]
- [[ai/mlops/llm-observability-and-tracing|LLM observability and tracing]]
- [[ai/mlops/ci-cd-for-ml|CI/CD for ML systems]]
- [[ai/mlops/feature-stores|Feature stores]]

## Serving and improvement

- [[ai/mlops/serving-and-inference|Serving and inference]]
- [[ai/mlops/cost-optimization|Cost optimization]]
- [[ai/mlops/human-in-the-loop-production|Human-in-the-loop in production]]
- [[ai/mlops/feedback-loops|Feedback loops]]

## Core sources

- Chip Huyen — *Designing Machine Learning Systems* and *AI Engineering*.
- Made With ML by Goku Mohandas — practical production ML workflows.
- Google Cloud — *MLOps: Continuous delivery and automation pipelines in machine learning*.
- MLflow and Weights & Biases docs for experiment tracking and model registries.
- LangSmith, Langfuse, and Arize Phoenix docs for LLM tracing and observability patterns.
- Eugene Yan — production ML and LLM system writing.
