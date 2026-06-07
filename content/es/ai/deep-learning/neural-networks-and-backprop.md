---
title: "Redes neuronales y backpropagation"
description: Una red es un grafo de cómputo diferenciable; backprop es solo la regla de la cadena corriendo hacia atrás por ese grafo. Entendé esto y el resto es detalle.
tags: [deep-learning, backpropagation, neural-networks, autograd]
order: 1
updated: 2026-06-07
---
# Redes neuronales y backpropagation

Una red neuronal es una gran función diferenciable construida con pasos pequeños.
Entrenarla significa calcular cómo un cambio diminuto en cada parámetro cambiaría el
[[ai/foundations/how-learning-works|loss]], y después empujar cada parámetro en
consecuencia. Ese cálculo de gradientes es **backpropagation**, y no es más que la regla
de la cadena aplicada a un grafo.

## Forward pass: un stack de pasos simples

Cada capa calcula `z = W·x + b` (un [[ai/machine-learning/linear-and-logistic-regression|modelo
lineal]]) seguido de una [[ai/deep-learning/activation-functions|activación]] no lineal.
Apilalas y obtenés un **grafo de cómputo** desde el input hasta un loss escalar. Sin las
no linealidades, apilar capas lineales colapsaría a una sola capa lineal: las
activaciones son lo que le da poder a la profundidad.

## Backward pass: la regla de la cadena, invertida

Para obtener el gradiente del loss respecto de un peso temprano, la regla de la cadena
multiplica las derivadas locales a lo largo del camino desde ese peso hasta el loss.
Backprop computa esto eficientemente recorriendo el grafo **una vez hacia atrás**,
reutilizando sub-resultados compartidos, así que el costo es parecido al forward pass.

> Cada nodo solo necesita saber: su derivada local y el gradiente que le llega desde
> arriba. Los multiplicás y pasás el resultado hacia abajo. Ese es todo el algoritmo.

## Autograd: por qué nunca hacés esto a mano

Frameworks (PyTorch, JAX) registran las operaciones forward como un grafo y aplican
backprop automáticamente: **diferenciación automática**. Definís el cómputo forward;
los gradientes vienen gratis. *micrograd* de Karpathy muestra toda la idea en ~100 líneas.

## Por qué los gradientes se portan mal

La cadena de multiplicaciones también es el modo de falla: muchos factores chicos → el
gradiente **se desvanece** (las capas tempranas dejan de aprender); factores grandes →
**explota** (el entrenamiento diverge). Buena parte de [[ai/deep-learning/initialization-and-normalization|init
y normalización]], mejores [[ai/deep-learning/activation-functions|activaciones]] y
conexiones residuales existen para mantener ese gradiente fluyendo.

**Se conecta con:** [[ai/foundations/gradient-descent-intuition|gradient descent]] ·
[[ai/deep-learning/activation-functions|activaciones]] ·
[[ai/deep-learning/optimizers|optimizadores]]
