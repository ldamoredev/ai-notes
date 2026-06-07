---
title: "Cómo funciona el aprendizaje: loss, objetivo y ERM"
description: Todo modelo que "aprende" está minimizando una función de pérdida sobre datos. Entendé ese loop y la mayor parte de ML deja de parecer magia.
tags: [foundations, loss, optimization, training]
order: 1
updated: 2026-06-07
---
# Cómo funciona el aprendizaje: loss, objetivo y ERM

Un modelo que "aprende" está haciendo algo mecánico: tiene **parámetros**, una forma
de convertir parámetros + input en una predicción, y una **función de pérdida** que
puntúa qué tan equivocada está cada predicción. El entrenamiento es la búsqueda de
parámetros que hagan chica la pérdida promedio.

## Las tres piezas

1. **Una familia de modelos** — una función parametrizada `f(x; θ)`. Los parámetros
   `θ` son lo que cambia el entrenamiento (pesos de una red, coeficientes de una regresión).
2. **Una función de pérdida** — `L(prediction, target)` devuelve un número grande
   cuando la predicción es mala. Ejemplos: error cuadrático para regresión,
   cross-entropy para clasificación.
3. **Un optimizador** — un procedimiento que empuja `θ` para reducir el loss, casi
   siempre una variante de [[ai/foundations/gradient-descent-intuition|gradient descent]].

## Minimización empírica del riesgo (ERM)

En realidad queremos bajo loss sobre la *distribución verdadera* de datos ("riesgo"),
pero solo tenemos una muestra finita. Entonces minimizamos la **pérdida promedio en el
training set** — el riesgo *empírico* — y esperamos que siga al riesgo verdadero:

> minimizar sobre θ:  (1/N) Σ L( f(xᵢ; θ), yᵢ )

Esa "esperanza" es todo el juego. Cuando el riesgo empírico es bajo pero el riesgo
verdadero es alto, tenés [[ai/foundations/generalization-and-overfitting|overfitting]].
La brecha entre ambos es lo que [[ai/foundations/data-splits-and-leakage|la evaluación
held-out]] existe para estimar.

## El loss codifica lo que realmente querés

El loss es una **declaración de valor**, no una tecnicalidad. Si los falsos negativos
son peores que los falsos positivos, el loss tiene que decirlo (pesos por clase, costos
custom). Un modelo optimiza exactamente lo que medís, no lo que quisiste decir.

- El error cuadrático castiga desproporcionadamente los errores grandes → sensible a outliers.
- Cross-entropy castiga fuerte las respuestas equivocadas con confianza → empuja calibración.
- Un proxy loss (lo diferenciable) suele diferir del objetivo real (lo que le importa
  al negocio). Cuidá esa brecha.

## Trampa

Optimizar el objetivo equivocado es el bug más caro en ML, y es silencioso: la curva de
loss se ve genial mientras el modelo mejora en lo incorrecto.

**Se conecta con:** [[ai/foundations/gradient-descent-intuition|gradient descent]] ·
[[ai/foundations/evaluation-metrics|métricas vs loss]] ·
[[ai/foundations/information-theory-basics|por qué cross-entropy]]
