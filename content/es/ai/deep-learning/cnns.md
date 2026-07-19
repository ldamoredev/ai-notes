---
title: "CNNs: convolución y estructura espacial"
description: Las redes convolucionales incorporan la estructura de las imágenes en la arquitectura — localidad e invariancia a traslación — y ese sesgo inductivo es por lo que ganaron en visión.
tags: [deep-learning, cnn, convolution, vision]
order: 6
updated: 2026-06-07
---
# CNNs: convolución y estructura espacial

Una convolutional neural network es una red cuyo [[ai/foundations/inductive-bias-and-no-free-lunch|sesgo
inductivo]] matchea imágenes: los píxeles cercanos se relacionan y un patrón significa
lo mismo donde sea que aparezca. Codificar eso en la arquitectura es por lo que las CNNs
dominaron visión durante una década.

## Convolución: un filtro chico, deslizado por todos lados

En vez de conectar cada píxel con cada neurona, una CNN desliza **filtros** pequeños
(por ejemplo 3×3) por la imagen. Cada filtro aprende a detectar un patrón local — un
borde, una textura — y aplica los **mismos pesos en todos lados** (weight sharing). Dos
grandes ganancias:

- **Localidad** — las neuronas miran vecindarios chicos, matcheando cómo funciona la
  estructura visual.
- **Invariancia a traslación** — un detector de gatos se activa esté el gato arriba a
  la izquierda o en el centro, porque el filtro se comparte entre posiciones.

Weight sharing también significa **muchísimos menos parámetros** que una red fully-connected
sobre la misma imagen: menos [[ai/foundations/generalization-and-overfitting|overfitting]],
menos cómputo.

## La jerarquía de features

Convoluciones apiladas construyen una jerarquía de features: capas tempranas detectan
bordes y colores, capas medias detectan texturas y partes, capas profundas detectan
objetos. **Pooling** (downsampling) achica el tamaño espacial y agranda el receptive
field, así neuronas más profundas "ven" más de la imagen. Esto es
[[ai/foundations/features-and-dimensionality|representation learning]] hecho espacial.

## Dónde están hoy las CNNs

Las CNNs todavía impulsan mucha visión en producción (clasificación, detección,
segmentación) y son baratas y rápidas. Vision Transformers (ViT) ahora las igualan o
superan a gran escala, pero los ViTs necesitan más datos justamente porque *carecen* del
sesgo convolucional y deben aprender localidad desde cero. El tradeoff es el mismo de
siempre: prior más fuerte vs más datos (y la historia de [[ai/model-architectures/self-attention-from-first-principles|attention]]
sigue directo hacia [[ai/llms/index|LLMs]]).

## Trampa

Las CNNs asumen datos con estructura de grilla y correlación local. Forzarlas sobre datos
tabulares (sin estructura espacial) desperdicia su sesgo:
[[ai/machine-learning/decision-trees-and-ensembles|los árboles]] suelen ganar ahí.

**Conecta con:** [[ai/foundations/inductive-bias-and-no-free-lunch|sesgo inductivo]] ·
[[ai/model-architectures/self-attention-from-first-principles|attention vs convolución]] ·
[[ai/foundations/features-and-dimensionality|jerarquía de features]]
