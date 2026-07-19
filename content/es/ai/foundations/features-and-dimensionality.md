---
title: "Features, representaciones y la maldición de la dimensionalidad"
description: Los modelos no ven el mundo: ven features. Cómo la calidad de la representación decide todo y por qué las dimensiones altas son raras.
tags: [foundations, features, representations, embeddings]
order: 8
updated: 2026-06-07
---
# Features, representaciones y la maldición de la dimensionalidad

Un modelo nunca ve la realidad cruda; ve una **representación**: las features numéricas
que le das. La calidad de esa representación suele importar más que la elección del
algoritmo. "Garbage in, garbage out" es en realidad una afirmación sobre features.

## Features a mano vs representaciones aprendidas

- **Features hechas a mano** — humanos deciden qué es relevante (conteos de palabras,
  ratios, señales de dominio). El ML clásico vive o muere acá.
- **Representaciones aprendidas** — el modelo descubre features útiles por sí mismo.
  Eso significa "deep" en deep learning: cada capa construye una representación más
  rica que la anterior. Los [[ai/deep-learning/index|embeddings]] son el ejemplo
  canónico: vectores densos donde la cercanía geométrica codifica similitud semántica.

El paso de features hechas a mano a features aprendidas es la historia central de la
AI moderna, y por eso [[ai/rag-and-retrieval/index|los embeddings potencian retrieval]].

## La maldición de la dimensionalidad

Cuando crece la cantidad de features, la intuición construida en 2-D y 3-D se rompe:

- **Sparsity** — los puntos de datos quedan aislados; el volumen crece exponencialmente,
  así que cualquier dataset fijo se vuelve casi vacío. Necesitás exponencialmente más
  datos para cubrir el espacio.
- **Concentración de distancias** — en dimensiones muy altas, la distancia entre los
  puntos más cercanos y más lejanos se vuelve casi igual, así que "nearest neighbor"
  pierde significado. (Por eso las métricas de distancia naive sufren, y por eso los
  embeddings e índices approximate nearest-neighbor se diseñan con cuidado.)
- **Riesgo de overfitting** sube con más features en relación con las muestras.

## La bendición del otro lado

Los datos reales de alta dimensión suelen vivir cerca de una **manifold de menor
dimensión**: las imágenes de caras no llenan todo el espacio de píxeles; se agrupan
sobre una lámina fina dentro de él. Representation learning funciona encontrando esa
manifold. La reducción de dimensionalidad (PCA, UMAP) explota el mismo hecho.

## Takeaways prácticos

- Más features no es mejor; features **relevantes** sí. Podá, seleccioná o aprendé.
- Cuando las distancias se comportan raro, sospechá de la dimensionalidad antes que del algoritmo.
- Una buena representación vuelve fuerte a un modelo simple; una mala derrota a uno complejo.

**Conecta con:** [[ai/foundations/inductive-bias-and-no-free-lunch|sesgo inductivo]] ·
[[ai/deep-learning/index|representation learning]] ·
[[ai/rag-and-retrieval/index|embeddings y retrieval]]
