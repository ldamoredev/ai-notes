---
title: "Tuning de hiperparámetros"
description: Los parámetros se aprenden; los hiperparámetros se eligen. Cómo buscarlos sin quemar cómputo ni overfittear tu validation set.
tags: [machine-learning, hyperparameters, tuning, model-selection]
order: 9
updated: 2026-06-07
---
# Tuning de hiperparámetros

Los **parámetros** se aprenden de los datos (pesos). Los **hiperparámetros** son las
perillas que configurás *antes* de entrenar: learning rate, profundidad de árbol,
cantidad de estimators, [[ai/machine-learning/regularization-l1-l2|regularización λ]],
`k` en kNN. Los valores correctos pueden mover un modelo de mediocre a fuerte, pero la
búsqueda puede desperdiciar cómputo y overfittear en silencio si se hace sin cuidado.

## Estrategias de búsqueda

| Método | Cómo | Cuándo |
|---|---|---|
| **Grid search** | prueba cada combinación en una grilla | pocos hiperparámetros, modelos baratos |
| **Random search** | samplea combinaciones al azar | más eficiente; mejor con muchos params (la mayoría no importa) |
| **Bayesian / Optuna / Hyperband** | modela qué configuraciones parecen prometedoras y enfoca ahí | modelos caros, presupuestos más grandes |

Random search suele ganarle a grid con el mismo presupuesto: solo un par de
hiperparámetros tienden a importar, y el muestreo aleatorio explora esas dimensiones
mejor que una grilla rígida.

## Hacelo sin engañarte

- Tuneá contra un **validation set o [[ai/machine-learning/cross-validation|cross-validation]]**,
  nunca contra el test set.
- Cada trial de tuning que mira datos de validación gasta algo de su confiabilidad:
  cuantos más trials, más riesgo de overfittear *al validation set*. Usá **nested CV**
  o un test set held-out para el número final honesto.
- Poné esfuerzo donde rinde: para gradient boosting, learning rate + cantidad de árboles
  + profundidad dominan; para redes neuronales, el [[ai/mathematics-for-ai/gradient-descent-and-optimization|learning
  rate]] es rey.

## Orden práctico de operaciones

1. Conseguí un baseline con defaults razonables.
2. Tuneá los 2-3 hiperparámetros que más importan (random search).
3. Refiná alrededor de la mejor región.
4. Bloquealo y reportá sobre el test set intacto.

## Trampa

Perseguir una mejora de 0.2% en CV a través de cientos de trials suele ser minería de
ruido, no mejora, y además infla tu estimación. Mejores features o más datos le ganan
casi siempre a la obsesión por hiperparámetros.

**Conecta con:** [[ai/machine-learning/cross-validation|cross-validation]] ·
[[ai/machine-learning/regularization-l1-l2|regularización]] ·
[[ai/machine-learning/decision-trees-and-ensembles|tunear boosting]]
