---
title: "Intuición de álgebra lineal: el producto punto como similitud"
description: El mínimo de álgebra lineal que realmente aparece en ML: vectores como significado, matrices como transformaciones y el producto punto como similitud.
tags: [foundations, linear-algebra, embeddings, math]
order: 9
updated: 2026-06-07
---
# Intuición de álgebra lineal: el producto punto como similitud

No necesitás calcular eigenvalues a mano para hacer ML, pero unas pocas intuiciones
geométricas pagan para siempre. La grande: **casi toda "similitud" en AI moderna es un
producto punto.**

## Los vectores cargan significado

Un vector es una lista de números, pero pensalo como un **punto/flecha en el espacio**.
En ML, un [[ai/deep-learning/index|embedding]] ubica cada ítem (palabra, imagen,
usuario) en un punto tal que *los ítems relacionados caen cerca entre sí*. El
significado se vuelve geometría: "rey − hombre + mujer ≈ reina" funciona porque las
direcciones en el espacio codifican conceptos.

## Producto punto = alineación

Para dos vectores, el producto punto mide cuánto apuntan en la misma dirección:

- Grande positivo → dirección similar (significado similar).
- Cerca de cero → ortogonal (no relacionado).
- Negativo → opuesto.

**Cosine similarity** es simplemente el producto punto después de normalizar la
longitud, así que mide *solo dirección*: el caballo de batalla de búsqueda semántica y
[[ai/rag-and-retrieval/index|retrieval]]. Cuando una vector database "encuentra chunks
similares", está rankeando por producto punto / coseno.

## Las matrices transforman el espacio

Una matriz multiplicada por un vector lo **transforma**: rota, escala, proyecta hacia un
espacio nuevo. Una capa de red neuronal es exactamente esto:
`output = activation(W·x + b)`. Apilar capas apila transformaciones, reconfigurando la
representación paso a paso.

- La multiplicación de matrices es la operación que más se ejecuta en deep learning:
  por eso importan las GPUs (matemática matricial masivamente paralela).
- La atención en un transformer es una secuencia de productos matriciales que convierte
  queries, keys y values en combinaciones ponderadas.

## La shortlist que vale internalizar

| Concepto | Por qué importa en ML |
|---|---|
| Vector | un embedding: significado como coordenadas |
| Producto punto / coseno | similitud, la base de búsqueda y atención |
| Producto matriz-vector | una capa de red neuronal |
| Norma (longitud) | magnitud; normalizá antes de comparar direcciones |
| Proyección | reducción de dimensionalidad, descomponer señales |

**Se conecta con:** [[ai/foundations/features-and-dimensionality|representaciones]] ·
[[ai/deep-learning/index|redes neuronales]] ·
[[ai/rag-and-retrieval/index|embeddings y búsqueda]]
