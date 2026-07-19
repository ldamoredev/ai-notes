---
title: "Árboles de decisión y ensembles (RF, gradient boosting)"
description: Por qué los árboles con gradient boosting siguen siendo el ganador default en datos tabulares, y cómo bagging y boosting doman la inestabilidad de un solo árbol.
tags: [machine-learning, trees, random-forest, gradient-boosting, xgboost]
order: 4
updated: 2026-06-07
---
# Árboles de decisión y ensembles (RF, gradient boosting)

Para datos tabulares, un ensemble de árboles suele ser el modelo a vencer: muchas veces
supera a redes neuronales, entrena en segundos y necesita poco escalado de features.
Saber cómo funcionan te dice cuándo confiar en ellos.

## Un solo árbol de decisión

Un árbol divide los datos con una serie de preguntas sí/no ("¿edad > 30?"), eligiendo
cada split para que los grupos resultantes sean más puros. Captura no linealidades e
interacciones automáticamente y es fácil de leer, pero un árbol profundo solo **overfittea
fuerte**: tiene alta [[ai/foundations/generalization-and-overfitting|varianza]],
memorizando ruido. La solución es combinar muchos árboles.

## Dos formas de combinar árboles

| Método | Idea | Los árboles son | Efecto |
|---|---|---|---|
| **Bagging / Random Forest** | entrenar muchos árboles sobre muestras bootstrap + subconjuntos aleatorios de features, promediarlos | independientes, paralelos | principalmente reduce **varianza** |
| **Boosting** (GBM, XGBoost, LightGBM) | cada árbol nuevo corrige los errores del ensemble previo | secuenciales, dependientes | reduce **sesgo** *y* varianza |

- **Random Forest**: robusto, difícil de configurar mal, un gran baseline fuerte.
- **Gradient boosting**: suele tener el mejor score en datos tabulares, pero es más
  sensible a hiperparámetros (learning rate, profundidad del árbol, cantidad de árboles,
  regularización) y puede overfittear si lo empujás: [[ai/machine-learning/cross-validation|validá]]
  y usá early stopping.

## Por qué los árboles aman los datos tabulares

- No hace falta escalar features; manejan mezclas numéricas/categóricas naturalmente.
- Capturan interacciones y no linealidades sin
  [[ai/machine-learning/feature-engineering|feature crosses]] manuales.
- Dan **feature importances** para interpretabilidad (con salvedades).

## Trampa

Los defaults de boosting pueden overfittear en silencio. Mirá la curva de validación,
limitá profundidad de árboles y usá early stopping. Y acordate de que feature importances
puede engañar con features correlacionadas: corroborá con permutation importance o SHAP.

**Conecta con:** [[ai/machine-learning/hyperparameter-tuning|tuning]] ·
[[ai/foundations/generalization-and-overfitting|varianza y overfitting]] ·
[[ai/machine-learning/feature-engineering|features]]
