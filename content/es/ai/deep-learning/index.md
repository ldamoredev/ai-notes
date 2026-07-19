---
title: Deep Learning
description: Cómo las redes neuronales aprenden representaciones: backprop, arquitecturas, trucos de entrenamiento que las hacen funcionar y por qué importa la escala.
tags: [deep-learning, neural-networks]
order: 0
updated: 2026-06-07
---
# Deep Learning

Deep learning es lo que pasa cuando apilás muchas capas simples y diferenciables y
dejás que [[ai/mathematics-for-ai/gradient-descent-and-optimization|gradient descent]] descubra las
features en vez de diseñarlas a mano. Ese único cambio — **representaciones aprendidas
por encima de features artesanales** — es la razón por la que tomó visión, habla y
lenguaje, y es el sustrato sobre el que se construye todo [[ai/llms/index|LLM]].

> Una red neuronal es un stack de [[ai/machine-learning/linear-and-logistic-regression|modelos
> lineales]] separados por no linealidades, entrenada end to end con backprop. Todo lo
> demás es hacer que eso entrene establemente a escala.

## Modelo mental

Deep learning compone transformaciones diferenciables para aprender representaciones junto con la tarea. La arquitectura define caminos de información; el objetivo aporta presión; backprop asigna crédito; optimización y sistemas numéricos permiten escalar.

## Hoja de ruta: cómo aprende una red

- [[ai/computation-and-autodiff/backpropagation-from-first-principles|Redes neuronales y backpropagation]]
- [[ai/deep-learning/activation-functions|Funciones de activación y por qué importa la no linealidad]]
- [[ai/deep-learning/loss-functions-in-dl|Funciones de pérdida en deep learning]]

## Hacer que el entrenamiento funcione

- [[ai/deep-learning/initialization-and-normalization|Inicialización y normalización]]
- [[ai/deep-learning/optimizers|Optimizadores: de SGD a AdamW]]
- [[ai/deep-learning/regularization-in-deep-nets|Regularización: dropout, weight decay y augmentation]]
- [[ai/deep-learning/training-dynamics|Dinámicas de entrenamiento: schedules, warmup y debugging]]

## Arquitecturas

- [[ai/deep-learning/cnns|CNNs: convolución y estructura espacial]]
- [[ai/deep-learning/rnns-and-their-limits|RNNs y sus límites]]
- [[ai/model-architectures/self-attention-from-first-principles|El mecanismo de attention]]

## Representaciones y escala

- [[ai/deep-learning/embeddings-and-latent-spaces|Embeddings y espacios latentes]]
- [[ai/deep-learning/scaling-laws|Scaling laws: por qué más grande sigue funcionando]]

## Paradigmas y estrategia

- [[ai/reinforcement-learning/reinforcement-learning-essentials|Reinforcement learning, lo esencial]] cubre reward, policy y el paradigma detrás de RLHF y modelos de razonamiento.
- [[ai/deep-learning/the-bitter-lesson|The bitter lesson]] explica por qué los métodos generales y hambrientos de cómputo siguen venciendo a la estructura hecha a mano.

**Conecta con:** [[ai/computation-and-autodiff/index|Cómputo y Autodiff]] · [[ai/model-architectures/index|Arquitecturas de Modelos]] · [[ai/llms/index|Modelos de Lenguaje]]

## Fuentes principales

- Andrej Karpathy — *Neural Networks: Zero to Hero* (micrograd → makemore → GPT).
- 3Blue1Brown — serie *Neural Networks* (intuición visual para backprop).
- *Dive into Deep Learning* (d2l.ai) — ejecutable, amplio.
- Goodfellow, Bengio, Courville — *Deep Learning* (texto de referencia).
- Stanford CS231n; Distill.pub para explicaciones visuales.
- [Deep Learning](https://www.deeplearningbook.org/) — referencia canónica.
- [Dive into Deep Learning](https://d2l.ai/) — implementaciones ejecutables.
- [Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html) — de autodiff escalar a GPT.
