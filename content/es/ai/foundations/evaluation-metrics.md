---
title: "Métricas de evaluación y qué esconden"
description: Accuracy miente en datos desbalanceados. Precision, recall, F1, ROC-AUC: qué mide cada una y cómo elegir la métrica que coincide con el costo de equivocarse.
tags: [foundations, metrics, evaluation, precision-recall]
order: 12
updated: 2026-06-07
---
# Métricas de evaluación y qué esconden

Una métrica única es un resumen con pérdida del comportamiento de un modelo. Elegir la
equivocada hace que un modelo inútil parezca genial: la trampa clásica es **accuracy en
datos desbalanceados**.

## Por qué accuracy miente

Si 99% de las transacciones son legítimas, un modelo que predice "legítima" siempre
tiene 99% de accuracy y detecta **cero** fraude. Accuracy premia la clase mayoritaria.
En cuanto las clases están desbalanceadas (fraude, enfermedad, defectos), buscá otra cosa.

## La familia de la matriz de confusión

Todo arranca con cuatro conteos: verdaderos/falsos positivos y negativos.

| Métrica | Pregunta que responde | Usala cuando |
|---|---|---|
| **Precision** | de los positivos que marqué, ¿cuántos eran correctos? | los falsos positivos son costosos (filtro de spam) |
| **Recall** | de los positivos reales, ¿cuántos capturé? | los falsos negativos son costosos (screening de cáncer) |
| **F1** | media armónica de precision y recall | necesitás un solo número balanceado |
| **ROC-AUC** | calidad del ranking en todos los thresholds | comparar modelos, independiente del threshold |
| **PR-AUC** | tradeoff precision/recall sobre positivos raros | fuerte desbalance de clases |

## El tradeoff precision-recall

Casi siempre podés intercambiar una por la otra moviendo el **threshold** de decisión.
Bajar el threshold → capturás más positivos (mayor recall) pero más falsas alarmas
(menor precision). El punto "correcto" depende del **costo relativo** de cada tipo de
error: una decisión de producto/ética, no matemática. Por eso un modelo se despliega
con un *threshold elegido*, no solo con una probabilidad.

## Más allá de clasificación

- **Regresión**: MAE (robusta a outliers) vs RMSE (castiga errores grandes). Elegí según
  cuánto duelen los misses grandes.
- **Ranking/retrieval**: Recall@K, MRR, NDCG; ver
  [[ai/rag-and-retrieval/index|evaluación de retrieval]].
- **Outputs generativos/LLM**: métricas de superficie (ROUGE/BLEU) correlacionan pobremente
  con calidad; la práctica moderna se apoya en [[ai/evaluation/index|LLM-as-judge y
  evals de tarea]].

## Trampa

Optimizar una sola métrica offline puede degradar silenciosamente lo que realmente te
importa (ley de Goodhart: una métrica que se vuelve objetivo deja de ser buena métrica).
Siempre acompañá el número principal con [[ai/mathematics-for-ai/probability-likelihood-and-uncertainty|calibración]]
y análisis de errores.

**Conecta con:** [[ai/foundations/how-learning-works|loss vs métrica]] ·
[[ai/evaluation/index|evaluar sistemas de AI]] ·
[[ai/mathematics-for-ai/probability-likelihood-and-uncertainty|calibración]]
