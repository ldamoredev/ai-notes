---
title: "RNNs y sus límites"
description: Las redes recurrentes procesaban secuencias un paso a la vez, hasta que los gradientes que se desvanecen y la imposibilidad de paralelizar hicieron ganar a attention. Vale entenderlas para ver por qué existen los transformers.
tags: [deep-learning, rnn, lstm, sequences]
order: 7
updated: 2026-06-07
---
# RNNs y sus límites

Antes de los transformers, las redes neuronales recurrentes eran la forma de modelar
secuencias. En gran parte perdieron, pero entender *por qué* es la forma más limpia de
entender por qué [[ai/deep-learning/attention-mechanism|attention]] y
[[ai/llms/index|transformers]] tomaron el control.

## Cómo funciona una RNN

Una RNN lee una secuencia elemento por elemento, manteniendo un **hidden state** que
actúa como memoria: en cada paso combina el input nuevo con el estado previo para
producir un nuevo estado. En principio, el estado lleva información de todo el pasado
hacia el presente.

## Límite 1: gradientes que se desvanecen en secuencias largas

Backpropagar a través de muchos pasos temporales multiplica muchos números chicos, así
que el gradiente [[ai/deep-learning/neural-networks-and-backprop|se desvanece]] y la red
tiene problemas para conectar eventos distantes ("el tema mencionado hace 200 palabras").
**LSTMs** y **GRUs** agregaron gates para llevar información más lejos, lo que ayudó
mucho, pero las dependencias de largo alcance siguieron siendo difíciles.

## Límite 2: sin paralelismo

Este fue el fatal. Como el paso *t* necesita el estado del paso *t−1*, una RNN debe
procesar una secuencia **secuencialmente**: no podés computar todas las posiciones a la
vez. En GPUs modernas hechas para [[ai/foundations/linear-algebra-for-ml|matemática
matricial]] masivamente paralela, eso es una sentencia de muerte para escalar.

## Por qué ganó attention

[[ai/deep-learning/attention-mechanism|Attention]] arregla ambos problemas a la vez:

- Cualquier posición puede mirar **directamente** a cualquier otra en un salto: no hay
  una cadena larga por la cual el gradiente se desvanezca, así que las dependencias de
  largo alcance son fáciles.
- Todas las posiciones se computan **en paralelo**: perfecto para GPUs, lo que destrabó
  entrenamiento sobre datos a escala internet.

> "Attention is all you need" no era solo sobre calidad: eliminar recurrencia es lo que
> hizo los modelos *escalables*, y la escala es lo que produjo los [[ai/llms/index|LLMs]].

Las RNNs todavía aparecen en settings diminutos, streaming o de baja latencia, y la
pregunta eficiencia-vs-attention sigue viva en modelos state-space más nuevos (por
ejemplo Mamba).

**Se conecta con:** [[ai/deep-learning/attention-mechanism|attention]] ·
[[ai/deep-learning/neural-networks-and-backprop|gradientes que se desvanecen]] ·
[[ai/llms/index|por qué transformers]]
