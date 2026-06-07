---
title: "Clustering y PCA: aprender sin etiquetas"
description: Las dos herramientas no supervisadas más útiles: encontrar grupos con k-means y comprimir/visualizar datos con PCA (y cuándo usar UMAP).
tags: [machine-learning, clustering, pca, unsupervised, dimensionality-reduction]
order: 10
updated: 2026-06-07
---
# Clustering y PCA: aprender sin etiquetas

[[ai/foundations/types-of-learning|El aprendizaje no supervisado]] encuentra estructura
sin una clave de respuestas. Dos herramientas cubren la mayor parte de la necesidad
práctica: clustering (agrupar puntos similares) y reducción de dimensionalidad
(comprimir y visualizar).

## Clustering: descubrir grupos

- **k-means**: elegí `k`, asigná puntos al centroide más cercano, mové centroides a la
  media, repetí. Rápido y ubicuo. Salvedades: tenés que elegir `k` (usá el método
  elbow/silhouette), asume clusters redondos y de tamaño similar, y es sensible al
  escalado y a la inicialización (usá k-means++).
- **Hierarchical / DBSCAN**: construye un árbol de clusters, o encuentra regiones
  densas y etiqueta puntos dispersos como ruido (DBSCAN encuentra `k` por sí mismo y
  formas arbitrarias).

Usos: segmentación de clientes, deduplicación, análisis exploratorio, agrupar
[[ai/foundations/linear-algebra-for-ml|embeddings]] para ver qué "piensa" un modelo que
es similar.

## PCA: comprimir en las direcciones que importan

Principal Component Analysis encuentra las direcciones ortogonales de **máxima
varianza** y reexpresa los datos en esas coordenadas. Conservá los primeros componentes
y reducís dimensiones preservando la mayor parte de la señal.

- Combate la [[ai/foundations/features-and-dimensionality|maldición de la dimensionalidad]]
  y decorrelaciona features.
- Acelera modelos downstream y habilita visualización 2-D/3-D.
- Es **lineal**: no puede desplegar estructura curva.

## PCA vs UMAP/t-SNE para visualizar

| Herramienta | Mejor para | Nota |
|---|---|---|
| **PCA** | reducción rápida, preprocesamiento, estructura global | lineal; los componentes son interpretables |
| **UMAP / t-SNE** | visualización 2-D de clusters | no lineal; gran visual, pero distancias/tamaños de clusters pueden engañar |

> Usá PCA para *reducir y decorrelacionar*; usá UMAP/t-SNE para *mirar*; y nunca leas
> distancias exactas desde un plot t-SNE.

## Trampa

Siempre escalá features antes de k-means y PCA: ambos se basan en distancia/varianza,
así que una feature no escalada de rango grande domina todo.

**Se conecta con:** [[ai/foundations/features-and-dimensionality|dimensionalidad]] ·
[[ai/foundations/types-of-learning|aprendizaje no supervisado]] ·
[[ai/deep-learning/index|representaciones aprendidas]]
