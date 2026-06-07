---
title: "Funciones de activación y por qué importa la no linealidad"
description: Sin una no linealidad, una deep net es solo un modelo lineal. Por qué ganó ReLU, qué son las neuronas muertas y dónde encaja GELU en transformers modernos.
tags: [deep-learning, activations, relu, gelu]
order: 2
updated: 2026-06-07
---
# Funciones de activación y por qué importa la no linealidad

La activación es el paso **no lineal** entre capas lineales. Sacala y cien capas apiladas
colapsan algebraicamente en una sola capa lineal: no hay poder extra. La no linealidad
es lo que permite que una red doble, pliegue y talle fronteras de decisión complejas.

## Por qué la no linealidad no es negociable

Una composición de funciones lineales sigue siendo lineal. Las activaciones no lineales
permiten que cada capa reconfigure el espacio para que la
[[ai/machine-learning/linear-and-logistic-regression|frontera lineal]] de la capa
siguiente separe cosas que antes no eran linealmente separables. La profundidad solo
compra algo *porque* existen activaciones.

## Los sospechosos habituales

| Activación | Forma | Notas |
|---|---|---|
| **Sigmoid / tanh** | compresión | clásicas; saturan y matan gradientes en deep nets |
| **ReLU** | `max(0, x)` | el caballo de batalla default: barata, sparse, evita saturación para inputs positivos |
| **Leaky ReLU / ELU** | ReLU con una pequeña pendiente negativa | arregla neuronas muertas |
| **GELU / SiLU** | suave, parecida a ReLU | estándar dentro de transformers y redes modernas |

## Por qué ReLU cambió deep learning

Las sigmoids saturan: su gradiente va a ~0 para inputs de gran magnitud, así que stacks
profundos sufren [[ai/deep-learning/neural-networks-and-backprop|gradientes que se
desvanecen]] y casi no entrenan. ReLU mantiene un gradiente de 1 para inputs positivos,
así que la señal fluye por redes profundas: una gran razón por la que entrenar deep nets
se volvió práctico.

## La trampa de dead ReLU

Una neurona ReLU que solo ve inputs negativos devuelve 0 para siempre y su gradiente es
0: está **muerta** y no se recupera. Causas: [[ai/deep-learning/optimizers|learning rate]]
demasiado alto o mala [[ai/deep-learning/initialization-and-normalization|inicialización]].
Variantes leaky o init cuidadosa lo previenen.

> Default a ReLU; usá GELU/SiLU en transformers. La capa de salida va aparte: usa
> softmax (clasificación) o nada (regresión), matcheada con el
> [[ai/deep-learning/loss-functions-in-dl|loss]].

**Se conecta con:** [[ai/deep-learning/neural-networks-and-backprop|backprop]] ·
[[ai/deep-learning/initialization-and-normalization|init y norm]] ·
[[ai/llms/index|GELU en transformers]]
