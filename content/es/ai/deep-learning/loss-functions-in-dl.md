---
title: "Funciones de pérdida en deep learning"
description: El loss es el objetivo que realmente optimizás. MSE vs cross-entropy vs contrastive, y cómo el loss decide silenciosamente en qué se convierte tu red.
tags: [deep-learning, loss, cross-entropy, contrastive]
order: 10
updated: 2026-06-07
---
# Funciones de pérdida en deep learning

El loss es el único número que una red está construida para minimizar, así que **define
la tarea**. Misma arquitectura, distinto loss → un clasificador, un regresor o un modelo
de embeddings. Elegirlo bien importa más que la mayoría de los cambios de arquitectura.

## Los losses comunes

| Loss | Tarea | Va con output |
|---|---|---|
| **MSE / L1** | regresión | output lineal |
| **Cross-entropy** | clasificación | softmax (multi-clase) o sigmoid (binaria) |
| **Contrastive / triplet / InfoNCE** | aprender [[ai/deep-learning/embeddings-and-latent-spaces|embeddings]] | vectores normalizados |

## Por qué cross-entropy domina clasificación

Cross-entropy viene directo de la [[ai/mathematics-for-ai/information-theory-entropy-and-divergence|teoría de la
información]]: mide la brecha entre distribuciones predichas y verdaderas y castiga
fuerte respuestas **confiadas y equivocadas**. Emparejada con softmax, su gradiente es
limpio y fuerte incluso cuando el modelo está muy equivocado, justo cuando querés una
señal de aprendizaje grande. El entrenamiento next-token de cada [[ai/llms/index|LLM]]
es simplemente cross-entropy sobre el vocabulario.

## Contrastive losses: aprender un espacio, no una etiqueta

Cuando el objetivo es una *representación* útil en vez de una clase, los contrastive
losses acercan ítems similares y alejan disimilares en el espacio vectorial. Así se
entrenan modelos de embeddings de texto/imagen (y CLIP), y por eso funciona la
[[ai/rag-and-retrieval/index|búsqueda semántica]].

## La brecha de proxy loss

El loss que podés diferenciar suele ser un **proxy** de lo que realmente te importa (no
podés hacer backprop a través de "satisfacción del usuario" o "accuracy@threshold").
Tené presente la brecha: un loss que baja es necesario, no suficiente; chequeá siempre
también la [[ai/foundations/evaluation-metrics|métrica]] real.

## Trampa

Desalinear loss y capa de salida (por ejemplo, softmax + MSE) entrena lento o no
entrena. Matcheá el loss con la tarea y la activación final.

**Conecta con:** [[ai/mathematics-for-ai/information-theory-entropy-and-divergence|cross-entropy]] ·
[[ai/foundations/how-learning-works|objetivo vs métrica]] ·
[[ai/deep-learning/embeddings-and-latent-spaces|contrastive learning]]
