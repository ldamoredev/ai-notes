---
title: Fase 03 — Entrenamiento e Inferencia
description: Sistemas que entrenan, adaptan, cargan, planifican, optimizan y sirven modelos bajo restricciones de hardware y confiabilidad.
tags: [phase, training, inference, systems]
order: 6
updated: 2026-07-19
---
# Fase 03 — Entrenamiento e Inferencia

Entrenamiento e inferencia ejecutan graphs relacionados con restricciones distintas. Training guarda activaciones y gradientes; inferencia optimiza carga, tráfico de memoria, batching, caching y latencia.

## Modelo mental

Entrenamiento es medir y actualizar repetidamente; inferencia es ejecutar un graph de sólo lectura bajo scheduling. Ambos están limitados por shapes, memoria, precisión, paralelismo y confiabilidad.

## Hoja de ruta por ramas

- [[ai/fine-tuning-and-alignment/index|Entrenamiento y Adaptación]]
- [[ai/inference-and-optimization/index|Sistemas de Inferencia]]

**Conecta con:** [[ai/phase-02-learning-and-models|Fase 02 — Aprendizaje y Modelos]] · [[ai/phase-04-context-and-agency|Fase 04 — Contexto y Agencia]]

## Fuentes principales

- [PyTorch Distributed Overview](https://pytorch.org/tutorials/beginner/dist_overview.html) — paralelismo de entrenamiento.
- [QLoRA](https://arxiv.org/abs/2305.14314) — adaptación eficiente en memoria.
- [vLLM](https://arxiv.org/abs/2309.06180) — serving de alto throughput.
