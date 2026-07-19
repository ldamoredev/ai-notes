---
title: "Manejar class imbalance"
description: Cuando los positivos son raros, accuracy miente y el entrenamiento naive ignora la minoría. Resampling, pesos de clase, tuning de threshold y qué ayuda de verdad.
tags: [machine-learning, class-imbalance, metrics, resampling]
order: 8
updated: 2026-06-07
---
# Manejar class imbalance

Fraude, enfermedad, defectos, churn: los casos que te importan suelen ser raros. Con
un split 99:1, un modelo que siempre predice la mayoría tiene 99% de accuracy y es
inútil. El imbalance toca métricas, entrenamiento y el threshold de decisión.

## Paso 1: arreglá primero la métrica

Esta es la palanca más grande y es gratis. Soltá accuracy; usá métricas enfocadas en
la clase minoritaria: **precision, recall, F1, PR-AUC** (ver
[[ai/foundations/evaluation-metrics|métricas y qué esconden]]). No podés gestionar lo
que medís mal.

## Paso 2: decidí si rebalancear

Muchas veces un buen modelo + métrica + threshold alcanza. Si la minoría realmente está
subaprendida, rebalanceá, pero con cuidado:

| Técnica | Qué hace | Cuidado con |
|---|---|---|
| **Pesos de clase** | le dice al loss que penalice más los errores de la minoría | lo más simple; probá esto primero |
| **Random oversampling** | duplica filas de la minoría | puede overfittear los duplicados |
| **SMOTE** | sintetiza nuevos puntos minoritarios entre vecinos | riesgoso en dimensiones altas; puede difuminar fronteras |
| **Undersampling** | descarta filas de la mayoría | tira datos; usalo cuando la mayoría es enorme |

## Paso 3: tuneá el threshold

Un clasificador devuelve una probabilidad; el **threshold de decisión** lo elegís vos.
Para positivos raros pero costosos, bajalo para subir recall (aceptando más falsas
alarmas). Este es un [[ai/foundations/evaluation-metrics|tradeoff precision-recall]]
empujado por el costo relativo de cada error: una decisión de producto, no un default.

## La regla cardinal

> **Hacé resampling dentro del fold de cross-validation, nunca antes de dividir.**
> Oversamplear todo el dataset primero filtra puntos de la minoría tanto en train como
> en validación, inflando scores. Hacelo en un [[ai/machine-learning/ml-pipelines-and-leakage|pipeline]].

Además mantené el **test set con la proporción del mundo real**: evaluar sobre datos
artificialmente balanceados esconde cómo se comporta el modelo en producción.

**Conecta con:** [[ai/foundations/evaluation-metrics|precision/recall]] ·
[[ai/machine-learning/cross-validation|CV estratificada]] ·
[[ai/machine-learning/ml-pipelines-and-leakage|resample in-fold]]
