---
title: Computación y Autodiff
description: Cómo arrays, compute graphs, derivadas, memoria, precisión y hardware paralelo convierten modelos matemáticos en sistemas ejecutables.
tags: [computation, tensors, autodiff, systems]
order: 0
updated: 2026-07-19
status: current
level: intermediate
---
# Computación y Autodiff

Una función matemática no se entrena sola: hay que representarla como operaciones sobre arrays, ejecutarla en un orden definido, diferenciarla, planificarla sobre hardware y observarla bajo precisión finita.

## Modelo mental

El forward pass crea valores y dependencias. El autodiff reverso recorre esas dependencias hacia atrás, multiplica derivadas locales y acumula cada camino que llega a un parámetro compartido. Las librerías de tensores agregan shapes, kernels vectorizados, devices, memoria y sincronización.

## Nota fundacional actual

- [[ai/computation-and-autodiff/backpropagation-from-first-principles|Backpropagation desde primeros principios]]

## Roadmap

Shapes y strides · vectorización · compute graphs · motor de autodiff reverso · forward mode · floating point y mixed precision · randomness y reproducibilidad · GPUs y kernels.

**Conecta con:** [[ai/mathematics-for-ai/index|Matemática para IA]] · [[ai/deep-learning/index|Deep Learning]] · [[ai/inference-and-optimization/index|Sistemas de Inferencia]]

## Fuentes principales

- [PyTorch Autograd mechanics](https://pytorch.org/docs/stable/notes/autograd.html) — comportamiento del motor de producción.
- [JAX automatic differentiation](https://docs.jax.dev/en/latest/automatic-differentiation.html) — transformaciones y productos Jacobiano-vector.
- [micrograd](https://github.com/karpathy/micrograd) — implementación compacta para estudiar el mecanismo.
