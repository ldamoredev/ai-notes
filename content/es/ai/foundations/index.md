---
title: Fundamentos
description: Los modelos mentales agnósticos al modelo detrás de la AI: qué optimiza el aprendizaje, por qué los modelos generalizan o fallan, datos, incertidumbre y evaluación.
tags: [foundations, vocabulary]
order: 0
updated: 2026-06-07
---
# Fundamentos

Fundamentos sostiene los conceptos que hacen más fácil cada rama posterior. Estas notas
son **agnósticas al modelo**: aplican tanto a una regresión logística como a un LLM de
frontera, porque ambos son sistemas que aprenden una función a partir de datos y después
tienen que comportarse sobre datos que nunca vieron.

Si solo internalizás una cosa acá: **machine learning es la disciplina de generalizar
desde ejemplos finitos hacia casos no vistos; todo lo demás es detalle al servicio de
eso.**

## Conceptos centrales

- [[ai/foundations/how-learning-works|Cómo funciona el aprendizaje: loss, objetivo y ERM]]
- [[ai/foundations/generalization-and-overfitting|Generalización, overfitting y el tradeoff sesgo-varianza]]
- [[ai/foundations/inductive-bias-and-no-free-lunch|Sesgo inductivo y la idea de no-free-lunch]]
- [[ai/foundations/types-of-learning|Tipos de aprendizaje: supervisado, no supervisado, self-supervised, RL]]

## Datos e incertidumbre

- [[ai/foundations/data-splits-and-leakage|Splits train/validación/test y data leakage]]
- [[ai/foundations/distribution-shift|La distribución de datos y el distribution shift]]
- [[ai/foundations/probability-and-uncertainty|Probabilidad e incertidumbre para ML]]
- [[ai/foundations/features-and-dimensionality|Features, representaciones y la maldición de la dimensionalidad]]

## La matemática que realmente usás

- [[ai/foundations/linear-algebra-for-ml|Intuición de álgebra lineal: el producto punto como similitud]]
- [[ai/foundations/gradient-descent-intuition|Gradient descent: cómo aprenden realmente los modelos]]
- [[ai/foundations/information-theory-basics|Teoría de la información: entropía, cross-entropy y KL]]

## Juzgar modelos

- [[ai/foundations/evaluation-metrics|Métricas de evaluación y qué esconden]]

## Vista de sistemas

- [[ai/foundations/mental-models-for-ai|Modelos mentales para sistemas de AI]]

## Conocer los límites

- [[ai/foundations/when-not-to-use-ai|Cuándo no usar AI]] reconoce dónde reglas, humanos o software más simple le ganan a un modelo.

## Fuentes principales

- 3Blue1Brown — *Essence of Linear Algebra* y *Neural Networks* (intuición visual).
- StatQuest (Josh Starmer) — sesgo/varianza, cross-validation, métricas.
- James, Witten, Hastie, Tibshirani — *An Introduction to Statistical Learning* (ISLP).
- Aurélien Géron — *Hands-On Machine Learning* (3rd ed.).
- Google — *Machine Learning Crash Course*.
