---
title: "El workflow de aprendizaje supervisado, de punta a punta"
description: El loop repetible desde encuadrar el problema hasta desplegar un modelo, y por qué un baseline tonto es el primer modelo más valioso que construís.
tags: [machine-learning, workflow, baseline]
order: 1
updated: 2026-06-07
---
# El workflow de aprendizaje supervisado, de punta a punta

La mayoría de los proyectos de ML fallan en **framing y datos**, no en modelado. El
algoritmo es la parte fácil. Este es el loop que te mantiene honesto.

## El loop

1. **Encuadrá el problema.** ¿Qué decisión impulsa este output? ¿Clasificación o
   regresión? ¿Cuánto cuesta una respuesta equivocada (esto elige tu
   [[ai/foundations/evaluation-metrics|métrica]])?
2. **Conseguí y dividí los datos** *antes* de tocarlos: train/validación/test, por
   tiempo o grupo si hace falta (ver [[ai/foundations/data-splits-and-leakage|leakage]]).
3. **Construí un baseline.** Una constante, una heurística o una regresión logística.
   Esa es la vara que todo modelo más sofisticado debe superar.
4. **Entrená un modelo real** sobre el split de entrenamiento.
5. **Evaluá** sobre validación y hacé [[ai/machine-learning/error-analysis|análisis de
   errores]]: no solo un score, sino *qué* casos fallan.
6. **Iterá** sobre features, datos y modelo. La mayoría de las mejoras vienen de datos,
   no de algoritmos.
7. **Chequeo final** sobre el test set intacto, una sola vez. Después desplegá y monitoreá.

## Por qué un baseline primero

Un baseline es el seguro más barato en ML:

- Te dice si el problema siquiera es aprendible desde tus datos.
- Expone leakage temprano (un baseline "demasiado bueno" es una alerta roja).
- Fija la referencia: un modelo con 92% de accuracy no vale nada si predecir la clase
  mayoritaria da 91%.
- Es un pipeline end-to-end funcionando que podés mejorar incrementalmente.

> Desplegá el modelo más tonto que corra de punta a punta el día uno. Optimizá desde ahí.

## Dónde se va realmente el tiempo

| Fase | Realidad |
|---|---|
| Framing y datos | la mayor parte del proyecto; la mayor parte del riesgo |
| Modelado | muchas veces unos pocos defaults bien elegidos |
| Evaluación y análisis de errores | subestimado; donde se esconden las mejoras reales |
| Productivización | [[ai/mlops/index|su propia disciplina]] |

## Trampa

Saltar a un modelo complejo antes de un baseline significa que no podés saber si tus
mejoras vienen del modelo, de un leak o de ruido.

**Se conecta con:** [[ai/machine-learning/error-analysis|análisis de errores]] ·
[[ai/foundations/how-learning-works|cómo funciona el aprendizaje]] ·
[[ai/machine-learning/ml-pipelines-and-leakage|pipelines]]
