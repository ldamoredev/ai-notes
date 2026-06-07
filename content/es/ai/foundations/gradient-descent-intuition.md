---
title: "Gradient descent: cómo aprenden realmente los modelos"
description: El loop de optimización detrás de casi todo modelo: caminar cuesta abajo sobre una superficie de loss, y por qué learning rate es la perilla más importante.
tags: [foundations, optimization, gradient-descent, training]
order: 10
updated: 2026-06-07
---
# Gradient descent: cómo aprenden realmente los modelos

El entrenamiento se reduce a un loop: medir qué tan equivocado estás, descubrir en qué
dirección empujar cada parámetro para estar *menos* equivocado, dar un paso chico,
repetir. Eso es gradient descent, y alimenta todo desde regresión lineal hasta LLMs de frontera.

## La imagen mental

Imaginá el [[ai/foundations/how-learning-works|loss]] como un paisaje con colinas donde
altura = error y tu posición = los parámetros actuales. El **gradiente** es la dirección
de subida más empinada; das un paso en la dirección **opuesta** para bajar.

> new_params = old_params − learning_rate × gradient

Repetís hasta que el loss deja de mejorar. Estás caminando cuesta abajo en un espacio
con millones o miles de millones de dimensiones.

## Learning rate: la perilla que define todo

- **Demasiado grande** → te pasás del valle, el loss rebota o diverge (NaNs).
- **Demasiado chico** → el entrenamiento avanza lentísimo y puede estancarse en un mal lugar.
- En la práctica usás un **schedule**: warm up y después decay. Este único
  hiperparámetro muchas veces importa más que cambios de modelo.

## Por qué "stochastic" (SGD)

Calcular el gradiente sobre el dataset *entero* en cada paso es demasiado caro, así que
lo estimamos sobre un **mini-batch**. La estimación es ruidosa, pero el ruido es una
feature: ayuda a escapar de malos lugares y generaliza mejor. Batch size intercambia
calidad del gradiente contra velocidad y memoria.

## Lo que realmente usás

SGD puro rara vez se usa crudo. **Adam / AdamW** adaptan el tamaño de paso por parámetro
usando promedios móviles de gradientes pasados: defaults robustos para deep nets.

| Término | Significado en una línea |
|---|---|
| Gradiente | dirección de mayor aumento del loss |
| Backpropagation | la regla de la cadena computando gradientes capa por capa |
| Learning rate | tamaño de paso: el hiperparámetro más importante |
| Mini-batch | una muestra usada para estimar el gradiente barato |
| Adam/AdamW | optimizador adaptativo; el default común |

## Trampa

Un loss que explota a NaN casi siempre es learning rate (o inputs sin escalar, o falta
de normalización). Bajá el LR antes de culpar al modelo.

**Se conecta con:** [[ai/foundations/how-learning-works|loss y objetivo]] ·
[[ai/deep-learning/index|backprop y optimizadores]] ·
[[ai/foundations/linear-algebra-for-ml|la matemática por debajo]]
