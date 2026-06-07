---
title: "Tipos de aprendizaje: supervisado, no supervisado, self-supervised, RL"
description: Las cuatro grandes formas en que aprenden los modelos, qué señal usa cada una y por qué self-supervision hizo posibles los LLMs.
tags: [foundations, supervised, self-supervised, reinforcement-learning]
order: 4
updated: 2026-06-07
---
# Tipos de aprendizaje: supervisado, no supervisado, self-supervised, RL

Las categorías difieren en **qué señal de supervisión** recibe el modelo: de dónde sale
la "respuesta correcta" durante el entrenamiento.

## Las cuatro familias

- **Supervisado** — aprende de pares `(input, label)`. La etiqueta es la respuesta.
  Clasificación y regresión. Potente, pero limitado por el costo de etiquetar.
- **No supervisado** — sin etiquetas; encuentra estructura. Clustering, reducción de
  dimensionalidad, estimación de densidad. Responde "¿qué hay en estos datos?"
- **Self-supervised** — las etiquetas se *generan desde los datos mismos*. Ocultá parte
  del input y predecila. No requiere anotación humana.
- **Reinforcement learning (RL)** — aprende de una señal de **recompensa** actuando en
  un entorno. No hay respuesta etiquetada, solo resultados mejores/peores a lo largo
  del tiempo.

## Por qué self-supervision cambió todo

Los LLMs se entrenan self-supervised: la "etiqueta" de cada token es simplemente **el
siguiente token** en el texto. Eso convierte todo internet en datos de entrenamiento
sin una sola anotación humana, por eso el pretraining pudo escalar como escaló. El
modelo aprende lenguaje, hechos y patrones de razonamiento como efecto secundario de
volverse bueno en "predecir el siguiente token".

> Self-supervision = datos no supervisados, entrenamiento de estilo supervisado. Es el
> puente que hizo económicamente posibles los foundation models.

## Dónde aparece cada uno en AI moderna

| Etapa | Tipo de aprendizaje |
|---|---|
| Pretraining de LLMs | self-supervised (next-token) |
| Instruction tuning / SFT | supervisado (prompt → respuesta ideal) |
| Alineación por preferencias (RLHF/DPO) | reinforcement / preference learning |
| Embeddings, clustering | no supervisado / self-supervised |

Un modelo de frontera es un *stack* de estos, no uno solo. Mirá
[[ai/fine-tuning-and-alignment/index|fine-tuning y alignment]] para ver cómo funcionan
las etapas posteriores.

**Se conecta con:** [[ai/llms/index|LLMs]] ·
[[ai/foundations/how-learning-works|cómo funciona el aprendizaje]] ·
[[ai/fine-tuning-and-alignment/index|fine-tuning y alignment]]
