---
title: "Dinámicas de entrenamiento: schedules, warmup y debugging"
description: Las perillas prácticas que deciden si un modelo grande entrena suavemente: learning-rate schedules, warmup, gradient clipping, batch size y leer la curva de loss.
tags: [deep-learning, training, learning-rate, debugging]
order: 11
updated: 2026-06-07
---
# Dinámicas de entrenamiento: schedules, warmup y debugging

Dos redes con arquitectura idéntica pueden tener éxito o fracasar puramente por **cómo**
fueron entrenadas. Estas son las palancas prácticas, y la habilidad de leer una curva de loss.

## Learning-rate schedules

Un [[ai/deep-learning/optimizers|learning rate]] fijo rara vez es lo mejor. Receta estándar:

- **Warmup** — arrancá minúsculo y subí durante los primeros cientos/miles de pasos.
  Al principio los pesos son aleatorios y un paso grande puede explotar; warmup evita
  la divergencia temprana que persigue a los transformers.
- **Decay** — bajá gradualmente la tasa (cosine o linear) para que el modelo dé pasos
  grandes al principio y pasos finos y cuidadosos después, al acercarse a un buen mínimo.

## Las otras perillas clave

- **Gradient clipping** — limitá la norma del gradiente para que un gradiente enorme
  raro no tire los pesos por un precipicio. Casi obligatorio para RNNs y transformers.
- **Batch size** — batches más grandes dan gradientes más suaves y mejor throughput de
  hardware, pero usan más memoria y pueden generalizar un poco peor; suele escalarse
  junto con el learning rate.
- **Mixed precision (fp16/bf16)** — entrená en menor precisión para velocidad y memoria,
  manteniendo algunas cosas en fp32 para estabilidad. Estándar en modelos grandes.

## Leer la curva de loss

| Síntoma | Causa probable |
|---|---|
| Loss → NaN / explota | LR demasiado alto, sin warmup, sin grad clipping, inputs sin escalar |
| Loss plano desde el paso 0 | LR demasiado bajo, mala [[ai/deep-learning/initialization-and-normalization|init]], data pipeline roto |
| Train ↓ pero val ↑ | [[ai/foundations/generalization-and-overfitting|overfitting]] → regularizar / más datos |
| Spikes de loss y después recupera | suele estar bien; spikes persistentes → bajar LR o clipear más fuerte |

## Orden de operaciones para debugging

1. **Overfitteá un solo batch** hasta ~cero loss: prueba que modelo + loss + cableado de backprop funcionan.
2. Después escalá datos y tuneá el LR (el hiperparámetro de mayor leverage).
3. Solo después tocá arquitectura.

> Si un modelo no aprende, sospechá del data pipeline y del learning rate mucho antes
> que de la arquitectura.

**Conecta con:** [[ai/deep-learning/optimizers|optimizadores]] ·
[[ai/deep-learning/initialization-and-normalization|init y norm]] ·
[[ai/machine-learning/error-analysis|learning curves]]
