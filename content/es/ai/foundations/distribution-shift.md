---
title: "La distribución de datos y el distribution shift"
description: Los modelos asumen que mañana se parece a los datos de entrenamiento. Cuando eso se rompe, y siempre se rompe, el rendimiento decae en silencio.
tags: [foundations, distribution-shift, drift, robustness]
order: 7
updated: 2026-06-07
---
# La distribución de datos y el distribution shift

Todo modelo se entrena sobre una **muestra de alguna distribución** y asume en silencio
que los datos de producción vienen de la misma. Cuando el mundo real se aleja de ese
supuesto, la accuracy cae: muchas veces sin ningún error, solo con outputs silenciosamente peores.

## Vocabulario para qué cambió

- **Covariate shift** — cambian los inputs, no cambia la relación input→output.
  (Nuevas demografías de usuarios; una cámara con otra iluminación.)
- **Label shift** — cambia la mezcla de resultados. (La tasa base de fraude salta
  durante una fecha especial.)
- **Concept drift** — cambia la relación input→output en sí. (Lo que cuenta como
  "spam" evoluciona cuando los spammers se adaptan.) El tipo más difícil.

## Por qué es la norma, no la excepción

- El mundo no es estacionario: comportamiento, lenguaje, precios y adversarios se mueven.
- Tu training set es una *foto*; el despliegue es un *stream*.
- Feedback loops: las propias acciones del modelo cambian la distribución que luego ve
  (un recommender reconfigura lo que clickean los usuarios).

## Detectar y responder

- **Monitoreá inputs**, no solo outputs: trackeá distribuciones de features y marcá
  cuándo los datos de producción se alejan de training (PSI, tests KS, chequeos de
  distancia entre embeddings).
- **Monitoreá un proxy de calidad** cuando las etiquetas llegan tarde (confianza, tasa
  de override humano, métricas downstream).
- Respondé con **retraining**, ponderación por recencia o, para sistemas LLM,
  refrescando el [[ai/rag-and-retrieval/index|contexto recuperado]] para mantener los
  hechos actuales sin tocar los pesos.

## Para LLMs específicamente

El **knowledge cutoff** de un modelo es un distribution shift incorporado el día que se
lanza: el mundo sigue moviéndose, los pesos no. Ese es el argumento central para usar
retrieval sobre fine-tuning cuando los hechos cambian.

**Conecta con:** [[ai/foundations/data-splits-and-leakage|splits realistas]] ·
[[ai/mlops/index|monitoreo y drift]] ·
[[ai/rag-and-retrieval/index|RAG para hechos frescos]]
