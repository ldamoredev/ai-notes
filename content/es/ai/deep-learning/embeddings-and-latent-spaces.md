---
title: "Embeddings y espacios latentes"
description: Las redes neuronales convierten cosas en vectores donde la geometría significa algo. Embeddings y el espacio latente son por qué funcionan transfer learning, búsqueda y clustering.
tags: [deep-learning, embeddings, latent-space, representation-learning]
order: 9
updated: 2026-06-07
---
# Embeddings y espacios latentes

La ganancia más profunda de deep learning es la **representación** que aprende. Una red
entrenada mapea inputs a un **espacio latente**: un espacio vectorial donde la posición
codifica significado. Conseguí un buen espacio y una docena de tareas downstream se
vuelven fáciles.

## Qué es un embedding

Un **embedding** es un vector denso que representa un ítem (palabra, oración, imagen,
usuario). La red aprende a ubicar ítems relacionados cerca e ítems no relacionados lejos,
así que [[ai/mathematics-for-ai/vectors-matrices-and-tensors|distancia y dirección]] cargan semántica:
cosas similares → baja distancia coseno; direcciones conceptuales se vuelven aritmética
("rey − hombre + mujer ≈ reina").

Comparados con codificaciones one-hot/sparse, los embeddings son **densos, de baja
dimensionalidad y generalizan**: capturan similitud en vez de tratar cada ítem como no relacionado.

## El espacio latente

Internamente, cada hidden layer es un espacio latente; la red reconfigura progresivamente
el input en una representación donde la [[ai/machine-learning/linear-and-logistic-regression|capa
lineal]] final puede hacer su trabajo. Los hidden states de un modelo de frontera *son*
un enorme espacio latente aprendido para lenguaje.

## Por qué esto importa en todas partes

- **Transfer learning** — features aprendidas sobre un dataset enorme transfieren a
  tareas nuevas con pocos datos. Fine-tuning y [[ai/fine-tuning-and-alignment/index|adaptation]]
  explotan esto: conservá la representación, redirigí la head.
- **Búsqueda semántica / [[ai/rag-and-retrieval/index|RAG]]** — embeddeá query y
  documentos, recuperá por nearest neighbor. Este es el motor del retrieval moderno.
- **Clustering y visualización** — agrupá o [[ai/machine-learning/clustering-and-pca|proyectá]]
  embeddings para ver la estructura que aprendió el modelo.
- **Multimodal** — entrená texto e imágenes en un espacio *compartido* (CLIP) para que
  puedan compararse directamente.

## Trampa

Los embeddings solo tienen significado **dentro del modelo que los produjo**: nunca
compares vectores de dos modelos de embeddings distintos, y re-embeddeá todo cuando
cambiás de modelo. Además: cosine similarity asume vectores normalizados; normalizá
antes de comparar.

**Conecta con:** [[ai/mathematics-for-ai/vectors-matrices-and-tensors|vectores y similitud]] ·
[[ai/rag-and-retrieval/index|retrieval]] ·
[[ai/foundations/features-and-dimensionality|representaciones]]
