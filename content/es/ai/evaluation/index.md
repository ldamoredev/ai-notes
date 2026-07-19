---
title: Evaluación y Medición
description: Eval sets, métricas, jueces, regresiones, incertidumbre y decisiones de producto.
tags: [evaluation, evals, quality]
order: 0
updated: 2026-07-19
---
# Evaluación y Medición

Una evaluación es un instrumento conectado a una decisión. Muestra casos, aplica mediciones o juicios, agrega incertidumbre y define si un sistema cruza un umbral de producto, seguridad u operación.

## Modelo mental

Diseñá la evaluación desde el contrato real: población, slices, fallas costosas, baseline y regla de decisión. Un score de benchmark sin ese contexto es evidencia incompleta.

## Hoja de ruta

- [[ai/evaluation/designing-eval-sets|Diseñar eval sets]]
- [[ai/evaluation/metrics-for-llm-evals|Métricas para evals LLM]]
- [[ai/evaluation/llm-as-judge|LLM como juez]]
- [[ai/evaluation/systematic-error-analysis|Análisis sistemático de errores]]
- [[ai/evaluation/evaluating-rag-systems|Evaluar RAG]]
- [[ai/evaluation/evaluating-agent-systems|Evaluar agentes]]

**Conecta con:** [[ai/research-and-experimentation/index|Investigación y Experimentación]] · [[ai/ai-product-engineering/evals-inside-the-product|Evals en el Producto]] · [[ai/interpretability/index|Interpretabilidad]]

## Fuentes principales

- [HELM](https://crfm.stanford.edu/helm/) — evaluación transparente y multi-escenario.
- [Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685) — sesgos y límites de jueces automáticos.
- [RAGAS](https://docs.ragas.io/) — métricas por componente para RAG.
- [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/) — vínculo entre evidencia offline y readiness.
