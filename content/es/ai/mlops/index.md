---
title: MLOps y Operaciones
description: Versionado, pipelines, releases, observabilidad, rollback y feedback loops de sistemas de IA.
tags: [mlops, llmops, production]
order: 0
updated: 2026-07-19
---
# MLOps y Operaciones

MLOps hace que cada cambio con modelos sea identificable, reproducible, observable, reversible y mejorable. La unidad desplegada incluye código, datos, pesos, prompts, retrieval, configuración y políticas.

## Modelo mental

No operás un modelo aislado: operás un sistema versionado con señales, SLOs, gates de release, detección de drift, rollback y aprendizaje desde producción.

## Hoja de ruta

- [[ai/mlops/experiment-tracking|Tracking de experimentos]]
- [[ai/mlops/model-and-prompt-registry|Registro de modelos y prompts]]
- [[ai/mlops/reproducible-pipelines|Pipelines reproducibles]]
- [[ai/mlops/monitoring-and-drift|Monitoreo y drift]]
- [[ai/mlops/llm-observability-and-tracing|Observabilidad y tracing LLM]]
- [[ai/mlops/ci-cd-for-ml|CI/CD para ML]]

**Conecta con:** [[ai/research-and-experimentation/index|Investigación]] · [[ai/evaluation/index|Evaluación]] · [[ai/inference-and-optimization/index|Sistemas de Inferencia]]

## Fuentes principales

- [Continuous Delivery for Machine Learning](https://martinfowler.com/articles/cd4ml.html) — versionado, testing, deployment y feedback.
- [Google MLOps](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning) — niveles de madurez y pipelines.
- [Hidden Technical Debt in ML Systems](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems) — acoplamiento y deuda sistémica.
- [OpenTelemetry](https://opentelemetry.io/docs/specs/otel/) — contrato de traces, métricas y logs.
