---
title: "Regularización: L1, L2 y cómo difieren"
description: La palanca principal contra overfitting: penalizar complejidad. Por qué L1 lleva features a cero, L2 las achica y qué comparten dropout y early stopping con ambas.
tags: [machine-learning, regularization, overfitting, l1, l2]
order: 3
updated: 2026-06-07
---
# Regularización: L1, L2 y cómo difieren

La regularización es la perilla principal para el [[ai/foundations/generalization-and-overfitting|tradeoff
sesgo-varianza]]: agregá una penalización por complejidad para que el modelo no pueda
ajustar ruido. Cambiás un poco de accuracy de entrenamiento por mejor generalización.

## La idea

En vez de minimizar solo el [[ai/foundations/how-learning-works|loss]], minimizá
`loss + λ × penalty(weights)`. Pesos grandes implican una función más flexible y
ondulante; penalizarlos mantiene el modelo más simple. **λ (lambda)** controla la fuerza:
un [[ai/machine-learning/hyperparameter-tuning|hiperparámetro]] clave que tuneás con
[[ai/machine-learning/cross-validation|cross-validation]].

## L1 vs L2

| | Penalización | Efecto sobre los pesos | Usala cuando |
|---|---|---|---|
| **L2** (Ridge) | suma de cuadrados | achica todos los pesos hacia cero, suavemente | default; features correlacionadas |
| **L1** (Lasso) | suma de valores absolutos | lleva algunos pesos a **exactamente cero** | querés selección automática de features / sparsity |
| **Elastic Net** | mezcla de ambas | achica *y* selecciona | muchas features correlacionadas |

La intuición clave: **L1 produce modelos sparse** (selección de features incorporada),
porque la geometría de su penalización tiene esquinas que empujan pesos a cero. **L2
mantiene todas las features pero chicas**, lo que es más estable cuando las features
están correlacionadas.

## Misma idea, otros nombres

La regularización está en todas partes; cambia la forma:

- **Early stopping** — detener el entrenamiento cuando sube el validation loss (limita
  la capacidad efectiva).
- **Dropout** — poner activaciones aleatoriamente en cero durante entrenamiento (un
  regularizador de [[ai/deep-learning/index|deep learning]]).
- **Weight decay** — L2 con otro nombre, incorporado en optimizadores como AdamW.
- **Más datos / augmentation** — el "regularizador" más fuerte de todos.

## Trampa

Escalá tus features antes de L1/L2: la penalización trata todos los pesos por igual, así
que una feature no escalada de rango grande queda injustamente penalizada (o perdonada).
Y λ demasiado fuerte hace underfitting: el síntoma es error alto en train y validación.

**Conecta con:** [[ai/foundations/generalization-and-overfitting|sesgo-varianza]] ·
[[ai/machine-learning/hyperparameter-tuning|tunear λ]] ·
[[ai/machine-learning/feature-engineering|selección de features]]
