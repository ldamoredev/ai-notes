---
title: "Scaling laws: por qué más grande sigue funcionando"
description: El rendimiento mejora de forma predecible con cómputo, datos y parámetros. Scaling laws, y la lección de datos de Chinchilla, explican toda la estrategia de frontier models.
tags: [deep-learning, scaling-laws, chinchilla, compute]
order: 12
updated: 2026-06-07
---
# Scaling laws: por qué más grande sigue funcionando

El hecho empírico definitorio de la AI moderna: cuando aumentás **cómputo, datos y
parámetros juntos**, el loss cae de forma suave y predecible, muchas veces como una ley
de potencia a través de muchos órdenes de magnitud. Esa previsibilidad es *por qué* los
labs apuestan miles de millones a modelos más grandes: el payoff puede pronosticarse
antes de entrenar.

## Las tres perillas

El test loss está impulsado conjuntamente por:

- **Parámetros** (N) — tamaño del modelo.
- **Datos** (D) — cantidad de tokens de entrenamiento.
- **Cómputo** (C) — aproximadamente `C ≈ 6 · N · D` para transformers.

Escalá una sola y llegás a rendimientos decrecientes; las ganancias vienen de escalarlas
**juntas** en la proporción correcta.

## La corrección Chinchilla

Los primeros modelos grandes estaban **undertrained**: demasiados parámetros para muy
pocos datos. El resultado *Chinchilla* mostró que, para un presupuesto fijo de cómputo,
parámetros y tokens deberían escalar **más o menos por igual**, y que un modelo más chico
entrenado con más datos vence a un modelo más grande entrenado con menos. Esto reencuadró
el campo desde "modelo más grande" hacia "modelo correcto, más (y mejores) datos", y por
eso calidad y cantidad de datos se volvieron el cuello de botella.

## Emergencia (leer con cuidado)

Algunas capacidades parecen "encenderse" después de cierto umbral de escala:
*emergent abilities*. El efecto es real pero en parte es un artefacto de métricas
pass/fail duras; con métricas más suaves, el progreso es más continuo. Tomá los claims
dramáticos de "emergence" con sano escepticismo. (Más en [[ai/llms/index|LLMs]].)

## Por qué importa en la práctica

- **Forecasting** — podés predecir el loss de modelos grandes desde corridas chicas y
  elegir el tamaño compute-optimal antes de comprometerte.
- **El techo** — los datos de alta calidad son finitos, así que el scaling está chocando
  con una pared de datos, empujando interés hacia calidad de datos, datos sintéticos y
  [[ai/foundations/types-of-learning|mejores señales de entrenamiento]].
- **Costo de inferencia** — un modelo más grande también es más caro de *servir*, lo que
  vuelve a los tradeoffs de [[ai/mlops/index|serving]] y [[ai/ai-product-engineering/index|costo
  de producto]].

> Scaling laws explican la estrategia; no prometen que sea gratis ni para siempre. Datos
> y costo de serving son los techos del mundo real.

**Conecta con:** [[ai/llms/index|pretraining de LLMs]] ·
[[ai/deep-learning/training-dynamics|entrenamiento a escala]] ·
[[ai/foundations/how-learning-works|loss como objetivo]]
