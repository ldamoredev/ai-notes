---
title: "Inicialización y normalización"
description: Cómo arrancás los pesos y mantenés bien escaladas las activaciones decide si una deep net entrena o no. Xavier/He init, BatchNorm vs LayerNorm.
tags: [deep-learning, initialization, batchnorm, layernorm]
order: 3
updated: 2026-06-07
---
# Inicialización y normalización

Las redes profundas son delicadas con la **escala de los números** que fluyen por ellas.
Arrancá mal los pesos o dejá que las activaciones deriven, y los gradientes se desvanecen
o explotan y el entrenamiento se estanca. Dos familias de trucos mantienen la señal en
un rango sano.

## Inicialización: importa dónde empezás

Si los pesos iniciales son demasiado grandes, activaciones y gradientes explotan; si son
demasiado chicos, se encogen hasta la nada a través de muchas capas. Esquemas
principled fijan la escala inicial para preservar varianza de capa a capa:

- **Xavier/Glorot** — para activaciones estilo tanh/sigmoid.
- **He/Kaiming** — para activaciones de la familia [[ai/deep-learning/activation-functions|ReLU]]
  (el default común hoy).

Nunca inicialices todos los pesos con la misma constante: las neuronas quedarían
idénticas para siempre (simetría). La aleatoriedad rompe la simetría para que las
neuronas se especialicen.

## Normalización: mantener activaciones bien comportadas

Las capas de normalización reescalan activaciones durante entrenamiento para que cada
capa vea una distribución estable, lo que permite usar [[ai/deep-learning/optimizers|learning
rates]] más altos y entrenar más profundo.

| Norm | Normaliza sobre | Usada en |
|---|---|---|
| **BatchNorm** | la dimensión del batch (por feature) | CNNs / visión |
| **LayerNorm** | la dimensión de features (por ejemplo) | transformers / [[ai/llms/index|LLMs]], RNNs |

LayerNorm ganó en transformers porque no depende de estadísticas de batch: se comporta
igual con batch size 1 o 1000 y con secuencias de longitud variable, algo clave para lenguaje.

## Por qué funciona (versión corta)

La normalización suaviza el paisaje del loss, reduciendo la chance de que la actualización
de una capa desplace brutalmente los inputs de la siguiente ("internal covariate shift"
es la explicación clásica, aunque discutida). Conexiones residuales + LayerNorm son lo
que hace entrenables a transformers de 100+ capas.

## Trampa

Una red que no aprende (loss plano o NaN) muchas veces es init/normalización o
[[ai/deep-learning/optimizers|learning rate]]: chequeá eso antes que la arquitectura.

**Se conecta con:** [[ai/deep-learning/neural-networks-and-backprop|gradientes que se desvanecen]] ·
[[ai/deep-learning/optimizers|optimizadores]] ·
[[ai/llms/index|LayerNorm en transformers]]
