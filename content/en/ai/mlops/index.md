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

## Mental model

MLOps makes every model-bearing change identifiable, reproducible, observable, reversible, and improvable. The deployed unit is a versioned system of code, data, model, prompts, retrieval, configuration, and policy—not a weights file in isolation.

## Roadmap: operating model

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

## Platform decisions

- [[ai/mlops/build-vs-buy-api-vs-self-hosting|Build vs buy: API vs self-hosting]] weighs hosted APIs against running your own models.
- [[ai/mlops/model-deprecation-and-migration|Model deprecation and migration]] insulates production from retired or silently updated models.

**Connects to:** [[ai/research-and-experimentation/index|Research and Experimentation]] · [[ai/evaluation/index|Evaluation]] · [[ai/inference-and-optimization/index|Inference Systems]]

## Core sources

- [Continuous Delivery for Machine Learning](https://martinfowler.com/articles/cd4ml.html) — versioning, testing, deployment, and feedback as one delivery system.
- [MLOps: Continuous delivery and automation pipelines](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning) — maturity levels and production pipeline architecture.
- [Hidden Technical Debt in Machine Learning Systems](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems) — system-level coupling and maintenance risks.
- [OpenTelemetry specification](https://opentelemetry.io/docs/specs/otel/) — vendor-neutral traces, metrics, and logs for model-serving systems.
- [MLflow documentation](https://mlflow.org/docs/latest/) — experiment, model, and deployment lifecycle primitives.
