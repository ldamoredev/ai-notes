---
title: "Regresión lineal y logística"
description: Los dos caballos de batalla que vale entender de verdad: un baseline fuerte, un modelo interpretable y el bloque de construcción dentro de toda red neuronal.
tags: [machine-learning, regression, classification, baseline]
order: 2
updated: 2026-06-07
---
# Regresión lineal y logística

Estos son los primeros modelos a probar y los últimos en jubilar por completo. Son
rápidos, interpretables, difíciles de overfittear y, crucialmente, una sola neurona en
una red neuronal *es* uno de ellos. Entendé estos y deep learning se vuelve menos misterioso.

## Regresión lineal: predecir un número

Ajustá una suma ponderada de features para predecir un valor continuo:
`ŷ = w·x + b`. Entrená minimizando error cuadrático mediante
[[ai/mathematics-for-ai/gradient-descent-and-optimization|gradient descent]] (o una solución cerrada).
Cada peso es legible: "manteniendo lo demás fijo, +1 acá mueve la predicción en wᵢ".

Supuestos que conviene conocer: relación más o menos lineal, errores no brutalmente
heteroscedásticos, features no perfectamente colineales. Rompelos fuerte y los
coeficientes se vuelven inestables o engañosos.

## Regresión logística: predecir una probabilidad

Para clasificación, envolvé el mismo score lineal en una **sigmoid** para comprimirlo
a [0, 1]: una probabilidad más o menos calibrada. Entrená con loss de
[[ai/mathematics-for-ai/information-theory-entropy-and-divergence|cross-entropy]]. A pesar del nombre, es un
*clasificador*. Un threshold (default 0.5, pero tunealo; ver
[[ai/foundations/evaluation-metrics|métricas]]) convierte la probabilidad en una decisión.

> Una regresión logística es exactamente la capa de salida de una red neuronal de
> clasificación. La parte "deep" solo aprende mejores features para alimentarla.

## Por qué siguen siendo el baseline default

- **Rápidos** para entrenar y predecir, incluso con muchos datos.
- **Interpretables**: los coeficientes se pueden inspeccionar, algo clave para confianza y debugging.
- **Difíciles de overfittear** con [[ai/machine-learning/regularization-l1-l2|regularización]],
  excelentes cuando los datos son limitados.
- Un buen score acá significa que un modelo complejo debe *ganarse* el riesgo adicional.

## Trampa

Los modelos lineales necesitan [[ai/machine-learning/feature-engineering|features]]
razonables: escalalas, codificá categóricas y agregá términos de interacción/no lineales
a mano, porque el modelo no puede descubrirlos por sí solo (ese es el
[[ai/foundations/inductive-bias-and-no-free-lunch|sesgo inductivo lineal]]).

**Conecta con:** [[ai/machine-learning/regularization-l1-l2|regularización]] ·
[[ai/mathematics-for-ai/gradient-descent-and-optimization|gradient descent]] ·
[[ai/deep-learning/index|la neurona dentro de una red]]
