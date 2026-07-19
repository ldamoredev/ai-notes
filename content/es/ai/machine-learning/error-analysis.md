---
title: "Análisis de errores: leer los errores de tu modelo"
description: Un único score agregado esconde dónde falla un modelo. Slices, learning curves y patrones de confusión convierten errores en un roadmap.
tags: [machine-learning, error-analysis, debugging, evaluation]
order: 11
updated: 2026-06-07
---
# Análisis de errores: leer los errores de tu modelo

La forma más rápida de mejorar un modelo es **mirar en qué se equivoca**, no cambiar
algoritmos. Un F1 de 0.87 no te dice nada sobre *cómo* llegar a 0.90. El análisis de
errores sí.

## Leé primero los errores a mano

Sacá una muestra de predicciones equivocadas y categorizalas. Los patrones aparecen rápido:

- "La mitad de los errores son una categoría mal etiquetada" → corregí las etiquetas.
- "Falla en inputs cortos" → brecha de feature o cobertura de datos.
- "Confiado y equivocado en un subgrupo" → sesgo o [[ai/foundations/distribution-shift|shift]].

Contar tipos de error te dice el *valor esperado* de cada arreglo: corregí primero el
bucket que es grande y barato.

## Sliceá, no promedies

Una métrica agregada puede estar bien mientras un slice crítico está roto. Evaluá
siempre por segmento (región, dispositivo, clase, largo de input, tier de cliente). El
modelo que tiene 95% de accuracy global pero 60% en tus usuarios de mayor valor es un
fracaso vestido de éxito.

## Las learning curves diagnostican el cuello de botella

Graficá error de entrenamiento vs validación a medida que crece data/tamaño:

| Patrón | Diagnóstico | Arreglo |
|---|---|---|
| Ambos altos, cerca entre sí | underfitting (alto sesgo) | modelo más grande, mejores features |
| Train bajo, val alto (brecha grande) | overfitting (alta varianza) | más datos, [[ai/machine-learning/regularization-l1-l2|regularización]] |
| Val todavía cae al final | todavía no hay datos suficientes | conseguir más datos |

Esto mapea directamente al [[ai/foundations/generalization-and-overfitting|tradeoff sesgo-varianza]].

## Trampa

Tunear contra un solo número invita a la [[ai/foundations/evaluation-metrics|ley de
Goodhart]]. Acompañá el score con slices y una matriz de confusión, o vas a optimizar
la métrica mientras el producto empeora.

**Conecta con:** [[ai/machine-learning/supervised-learning-workflow|el workflow]] ·
[[ai/foundations/evaluation-metrics|métricas]] ·
[[ai/evaluation/index|evaluar sistemas]]
