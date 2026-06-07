---
title: "Splits train/validación/test y data leakage"
description: Cómo estimar honestamente el rendimiento real, y las formas sutiles en que se filtra información e infla tus scores.
tags: [foundations, evaluation, data-leakage, validation]
order: 5
updated: 2026-06-07
---
# Splits train/validación/test y data leakage

No podés juzgar generalización sobre datos con los que el modelo entrenó. Por eso
particionás tus datos y mantenés una parte oculta: ese rendimiento held-out es tu
estimación de cómo se comporta el modelo en la calle.

## Los tres splits y sus trabajos

- **Training set** — el modelo ajusta sus parámetros acá.
- **Validation set** — se usa para tomar *decisiones*: hiperparámetros, selección de
  modelo, early stopping. Lo mirás muchas veces.
- **Test set** — se toca **una vez**, al final, para reportar un número honesto. Si lo
  usás para ajustar, deja de ser una estimación justa.

Cross-validation rota el rol de validación entre folds para obtener una estimación más
estable cuando los datos escasean.

## Data leakage: el inflador silencioso de scores

**Leakage** es cualquier momento en que información de afuera del training set se mete
en el modelo, haciendo que los scores de validación parezcan mejores que la realidad.
Es la causa más común de "genial en el notebook, terrible en producción".

Leaks comunes:

- **Preprocesamiento antes de dividir** — ajustar un scaler/imputer/vectorizer sobre el
  dataset *entero* filtra estadísticas de test hacia train. Ajustá solo sobre train y
  después aplicá a validación/test (usá un pipeline).
- **Target leakage** — una feature que codifica la respuesta (por ejemplo, un campo que
  solo se completa después de conocer el resultado).
- **Temporal leakage** — entrenar con datos futuros para predecir el pasado. Las series
  temporales deben dividirse por **tiempo**, nunca al azar.
- **Group leakage** — la misma entidad (usuario, paciente, documento) aparece tanto en
  train como en test, entonces el modelo "reconoce" en vez de generalizar. Dividí por grupo.
- **Filas duplicadas / casi duplicadas** cruzando el split — común en corpus de texto
  scrapeados y una preocupación real para benchmarks de LLMs (contaminación).

## Regla práctica

> Si un resultado se ve demasiado bueno, sospechá leakage antes de celebrar.

Un split realista que espeja cómo se va a usar realmente el modelo vale más que un
split aleatorio limpio que filtra en silencio.

**Se conecta con:** [[ai/foundations/generalization-and-overfitting|overfitting]] ·
[[ai/foundations/distribution-shift|distribution shift]] ·
[[ai/evaluation/index|evaluación]]
