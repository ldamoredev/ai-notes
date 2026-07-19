---
title: "kNN y SVM: distancia y márgenes"
description: Dos ideas clásicas con sombras largas: nearest-neighbor como ancestro de vector search, y la intuición de margen detrás de SVMs.
tags: [machine-learning, knn, svm, kernels]
order: 5
updated: 2026-06-07
---
# kNN y SVM: distancia y márgenes

Dos algoritmos más viejos que conviene conservar porque sus ideas centrales reaparecen
por todos lados en AI moderna: kNN es el ancestro conceptual de vector search, y el
margen de SVM es una lente limpia sobre generalización.

## k-Nearest Neighbors: "sos tus vecinos"

Para clasificar un punto, encontrá los `k` puntos de entrenamiento más cercanos y tomá
voto mayoritario (o promedio, para regresión). No hay "entrenamiento" real: solo guarda
los datos y computa distancias al momento de la consulta.

- **Fortaleza**: muerto de simple; un baseline no paramétrico decente.
- **Debilidad**: lento en predicción (compara contra todo), y sufre la
  [[ai/foundations/features-and-dimensionality|maldición de la dimensionalidad]]: las
  distancias pierden significado en dimensiones altas.
- **Por qué importa hoy**: [[ai/rag-and-retrieval/index|RAG y búsqueda semántica]] son
  kNN sobre [[ai/mathematics-for-ai/vectors-matrices-and-tensors|embeddings]], acelerados con índices
  approximate nearest-neighbor (HNSW). La idea escaló; la fuerza bruta no.

## Support Vector Machines: la calle más ancha

Un SVM encuentra la frontera de decisión con el **margen más grande**: la brecha más
ancha entre clases. Maximizar ese margen es un
[[ai/foundations/inductive-bias-and-no-free-lunch|sesgo inductivo]] incorporado hacia
generalización. Solo importan los puntos que definen la frontera (los *support vectors*).

El **kernel trick** permite que un SVM dibuje fronteras no lineales mapeando
implícitamente los datos a un espacio de mayor dimensión sin computar las coordenadas:
elegante y fuerte en datasets chicos/medianos con márgenes claros.

## Cuándo usar cada uno

| | Bueno para | Cuidado con |
|---|---|---|
| **kNN** | pocos datos, baseline rápido, lookups estilo recomendación | dimensiones altas, datasets grandes (lento) |
| **SVM** | problemas chicos/medianos con margen limpio | requiere escalado; tunear C/kernel; datos grandes son lentos |

En datos tabulares grandes, los [[ai/machine-learning/decision-trees-and-ensembles|árboles
con gradient boosting]] suelen ganarles a ambos, pero las intuiciones de distancia/margen
siguen siendo útiles.

**Conecta con:** [[ai/rag-and-retrieval/index|vector search]] ·
[[ai/foundations/features-and-dimensionality|dimensiones altas]] ·
[[ai/mathematics-for-ai/vectors-matrices-and-tensors|distancia y similitud]]
