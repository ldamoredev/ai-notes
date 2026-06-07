---
title: "Pipelines y prevención de leakage en preprocesamiento"
description: Por qué el preprocesamiento debe ajustarse solo sobre datos de entrenamiento, y cómo un pipeline vuelve eso el default en vez de algo que tenés que recordar.
tags: [machine-learning, pipelines, data-leakage, scikit-learn]
order: 12
updated: 2026-06-07
---
# Pipelines y prevención de leakage en preprocesamiento

El bug silencioso más común en ML es **ajustar preprocesamiento sobre todo el dataset**.
Escalado, imputación, encoding y selección de features todos *aprenden* estadísticas;
si aprenden de filas de test, tu evaluación queda contaminada. Un pipeline vuelve
automático el comportamiento correcto.

## El leak, concretamente

Supongamos que estandarizás features usando media y desviación estándar. Si las calculás
sobre todo el dataset *antes* de dividir, la distribución del test set se filtró hacia
training. Tu score de validación se ve mejor de lo que producción jamás verá. Esto es
una forma de [[ai/foundations/data-splits-and-leakage|data leakage]].

Otros pasos propensos a leak: imputar valores faltantes, target/mean encoding,
vectorizers TF-IDF, selección de features, oversampling para
[[ai/machine-learning/class-imbalance|imbalance]] (hacé resampling **dentro** de los
folds de cross-validation, nunca antes).

## El arreglo: fit en train, transform en el resto

> Cada paso que *aprende* de datos debe ver **solo el training fold**, y después aplicar
> lo que aprendió a validación/test.

Un **pipeline** encadena preprocesamiento + modelo en un objeto para que:

- `fit()` aprenda los parámetros de cada paso solo desde datos de entrenamiento.
- `transform/predict()` los reutilice sobre datos nuevos.
- Cross-validation reajuste el *pipeline entero* por fold, así ninguna estadística cruza
  la frontera del fold.

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipe = Pipeline([
    ("scale", StandardScaler()),
    ("clf", LogisticRegression()),
])
pipe.fit(X_train, y_train)      # scaler learns from train only
pipe.predict(X_test)            # reuses train statistics
```

## Bonus: paridad train/serve

Un pipeline también es el artifact que desplegás, así que el preprocesamiento exacto
usado en entrenamiento corre en producción, eliminando "training/serving skew", una
causa principal de modelos que testean bien y fallan en vivo.

## Trampa

Llamar `scaler.fit_transform(X)` sobre todo el dataset en un notebook es el leak
canónico. Si el preprocesamiento pasa fuera del loop de cross-validation, asumí leakage.

**Se conecta con:** [[ai/foundations/data-splits-and-leakage|leakage]] ·
[[ai/machine-learning/cross-validation|cross-validation]] ·
[[ai/mlops/index|paridad train/serve]]
