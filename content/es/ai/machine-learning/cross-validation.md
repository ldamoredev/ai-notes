---
title: "Cross-validation bien hecha"
description: Cómo estimar rendimiento sin desperdiciar datos ni engañarte: k-fold, stratified, grouped, time-series y la nested CV que requiere el tuning.
tags: [machine-learning, cross-validation, evaluation, model-selection]
order: 7
updated: 2026-06-07
---
# Cross-validation bien hecha

Un solo [[ai/foundations/data-splits-and-leakage|split]] train/validación da una
estimación ruidosa: tené mala suerte y sacás la conclusión equivocada. Cross-validation
(CV) rota el rol de validación por los datos para una estimación más estable, y usa
eficientemente datos escasos.

## k-fold CV

Dividí los datos en `k` folds. Entrená en `k−1`, validá en el fold held-out, rotá para
que cada fold sea validado una vez y promediá. Obtenés `k` scores: su **media** estima
rendimiento y su **dispersión** estima qué tan confiable es ese número. `k = 5` o `10`
son estándar.

## Elegí la variante que coincide con tus datos

| Variante | Usala cuando |
|---|---|
| **Stratified k-fold** | clasificación: preserva balance de clases en cada fold (esencial para datos [[ai/machine-learning/class-imbalance|desbalanceados]]) |
| **Grouped k-fold** | entidades repetidas (usuario, paciente): mantené un grupo entero en un solo fold para evitar [[ai/foundations/data-splits-and-leakage|group leakage]] |
| **Time-series split** | datos temporales: entrená siempre sobre el pasado, validá sobre el futuro; nunca shuffle |
| **Leave-one-out** | datasets muy chicos (caro, alta varianza) |

## Nested CV: la parte que la gente saltea

Si tuneás [[ai/machine-learning/hyperparameter-tuning|hiperparámetros]] usando tu score
de CV y después *reportás* ese mismo score, es optimista: ajustaste a los folds de
validación. **Nested CV** usa un loop interno para tunear y uno externo para estimar
honestamente. Como mínimo, mantené un [[ai/foundations/data-splits-and-leakage|test set]]
final que nunca tocás durante tuning.

## Trampa

Todo preprocesamiento debe pasar **dentro** del loop de CV (mediante un
[[ai/machine-learning/ml-pipelines-and-leakage|pipeline]]). Ajustá un scaler o hacé
resampling antes de dividir y cada fold queda contaminado: la forma más común en que CV
te miente.

**Se conecta con:** [[ai/foundations/data-splits-and-leakage|splits y leakage]] ·
[[ai/machine-learning/hyperparameter-tuning|tuning]] ·
[[ai/machine-learning/ml-pipelines-and-leakage|pipelines]]
