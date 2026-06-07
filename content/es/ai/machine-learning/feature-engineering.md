---
title: "Feature engineering"
description: Para ML clásico sobre datos tabulares, las features le ganan a los algoritmos. Encoding, escalado, interacciones y las trampas de leakage que acechan en cada paso.
tags: [machine-learning, feature-engineering, preprocessing]
order: 6
updated: 2026-06-07
---
# Feature engineering

En ML clásico, **las features deciden el techo** y el algoritmo solo se acerca. Deep
learning automatiza esto para texto e imágenes, pero para datos tabulares las features
pensadas todavía le ganan a un modelo más sofisticado. Es donde entra el conocimiento
de dominio.

## El toolkit cotidiano

- **Escalado** — estandarizá/normalizá features numéricas para que modelos basados en
  distancia y gradiente se comporten (kNN, SVM, lineales, redes neuronales). A los
  árboles no les importa.
- **Encoding de categóricas** — one-hot para baja cardinalidad; target/ordinal/hashing
  o embeddings para alta cardinalidad.
- **Manejo de valores faltantes** — imputá (media/mediana/modelo) y muchas veces agregá
  una bandera "was-missing", porque la ausencia en sí puede ser señal.
- **Transformaciones** — log/Box-Cox para valores sesgados; binning; fecha →
  (dayofweek, mes, is_holiday).
- **Interacciones y ratios** — `price_per_sqft`, `clicks/impressions`. Los modelos
  lineales no pueden inventarlos; tenés que agregarlos (una forma de inyectar
  [[ai/foundations/inductive-bias-and-no-free-lunch|sesgo inductivo]] a mano).

## Las buenas features comparten rasgos

- **Relevantes** para el target (llevan señal), no solo disponibles.
- **Disponibles al momento de predicción**: si una feature se conoce solo *después* del
  resultado, es [[ai/foundations/data-splits-and-leakage|target leakage]].
- **Estables**: no propensas a [[ai/foundations/distribution-shift|drift]] que rompa el
  modelo más adelante.

## La trampa de leakage

Cualquier feature aprendida de datos (estadísticas de scaler, target encoding, TF-IDF)
debe ajustarse solo sobre el **training fold**, dentro de un
[[ai/machine-learning/ml-pipelines-and-leakage|pipeline]]. Target encoding es
especialmente peligroso: computar medias por categoría sobre todas las filas filtra la etiqueta.

> Más features no es mejor. Features relevantes, sin leakage y disponibles en serving sí.
> Podá agresivamente; cada feature débil agrega varianza.

**Se conecta con:** [[ai/machine-learning/ml-pipelines-and-leakage|pipelines y leakage]] ·
[[ai/foundations/features-and-dimensionality|representaciones]] ·
[[ai/machine-learning/regularization-l1-l2|regularización para selección]]
