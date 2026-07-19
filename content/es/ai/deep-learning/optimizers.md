---
title: "Optimizadores: de SGD a AdamW"
description: SGD camina cuesta abajo; momentum y Adam hacen la caminata más rápida y estable. Qué agrega cada uno y por qué AdamW es el default en transformers.
tags: [deep-learning, optimizers, adam, sgd, momentum]
order: 4
updated: 2026-06-07
---
# Optimizadores: de SGD a AdamW

El optimizador convierte gradientes en actualizaciones de pesos. Todos se apoyan en
[[ai/mathematics-for-ai/gradient-descent-and-optimization|gradient descent]]; las diferencias están en
cómo usan la *historia* de gradientes para dar pasos más inteligentes.

## La progresión

- **SGD** — paso opuesto al gradiente del mini-batch. Simple, bien entendido, muchas
  veces generaliza mejor en visión, pero es lento y sensible al learning rate.
- **Momentum** — acumula una velocidad que promedia gradientes recientes, así el
  optimizador atraviesa ruido y baches chicos en vez de zigzaguear. Pensalo como una
  pelota rodando cuesta abajo.
- **RMSProp / Adagrad** — escala el paso de cada parámetro según la magnitud reciente
  de su propio gradiente, así los parámetros poco actualizados todavía se mueven.
- **Adam** — momentum **+** escalado por parámetro combinados. Robusto, converge rápido,
  perdonador con learning rate: el default para la mayoría de deep nets.
- **AdamW** — Adam con **weight decay desacoplado**, lo que hace que la
  [[ai/deep-learning/regularization-in-deep-nets|regularización L2]] se comporte
  correctamente. El estándar para entrenar transformers.

## Qué compra lo "adaptativo"

Adam adapta el tamaño de paso efectivo por parámetro usando promedios móviles del
gradiente (primer momento) y su cuadrado (segundo momento). En la práctica: funciona
con menos tuning, por eso domina. SGD con momentum + un buen schedule puede generalizar
un poco mejor, pero necesita más cuidado.

## La perilla que todavía importa más

Ningún optimizador te salva de un mal [[ai/mathematics-for-ai/gradient-descent-and-optimization|learning
rate]]. Adam reduce la sensibilidad pero no la elimina: combinalo con un
[[ai/deep-learning/training-dynamics|schedule de warmup + decay]]. Demasiado alto → el
loss diverge (NaNs); demasiado bajo → avanza a paso de tortuga.

> Default razonable: **AdamW + warmup + cosine decay.** Usá SGD+momentum puro cuando
> estés exprimiendo el último poco de generalización de un modelo de visión.

**Conecta con:** [[ai/mathematics-for-ai/gradient-descent-and-optimization|gradient descent]] ·
[[ai/deep-learning/training-dynamics|schedules de LR]] ·
[[ai/deep-learning/regularization-in-deep-nets|weight decay]]
