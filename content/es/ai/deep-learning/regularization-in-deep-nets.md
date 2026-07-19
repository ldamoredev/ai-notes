---
title: "Regularización: dropout, weight decay y augmentation"
description: Las redes grandes overfittean fácil. Las herramientas específicas de deep learning que las mantienen honestas: dropout, weight decay, early stopping y data augmentation.
tags: [deep-learning, regularization, dropout, augmentation]
order: 5
updated: 2026-06-07
---
# Regularización: dropout, weight decay y augmentation

Las deep nets tienen suficiente capacidad para memorizar su training set, así que
controlar [[ai/foundations/generalization-and-overfitting|overfitting]] es central. Es
la misma idea que la [[ai/machine-learning/regularization-l1-l2|regularización L1/L2]]
clásica — penalizar complejidad — con ropa de deep learning.

## El toolkit

- **Dropout** — durante entrenamiento, pone aleatoriamente en cero una fracción de
  activaciones en cada paso. Ninguna neurona puede depender de una compañera específica,
  así que la red aprende features redundantes y robustas (un ensemble implícito). Se
  apaga en **inferencia**.
- **Weight decay** — achica pesos hacia cero en cada paso (L2 con otro nombre;
  incorporado en [[ai/deep-learning/optimizers|AdamW]]). Mantiene la función más suave.
- **Early stopping** — detené cuando el validation loss empieza a subir. Gratis,
  efectivo, siempre vale conectarlo.
- **Data augmentation** — expandí el dataset con transformaciones que preservan labels
  (flip/crop/rotate en imágenes; parafraseo/back-translation en texto). Muchas veces
  es la mayor mejora real porque ataca la causa raíz: datos insuficientes.
- **Batch/Layer norm** también regularizan como efecto secundario.

## Cuánto usar

La regularización intercambia un poco de ajuste en entrenamiento por mejor
generalización. La [[ai/machine-learning/error-analysis|learning curve]] te dice hacia
dónde empujar: una brecha grande train-vs-validación → agregá regularización; error alto
en ambos → estás haciendo *underfitting*, así que aflojá.

> El regularizador más fuerte casi siempre es **más y mejores datos**. Buscá datos y
> augmentation antes de apilar dropout sobre dropout.

## Trampa

Dejar dropout prendido en inferencia, u olvidarte de `model.eval()` en PyTorch, degrada
predicciones silenciosamente. Y demasiado dropout + weight decay juntos puede hacer
underfitting: el síntoma es un training loss que no baja.

**Conecta con:** [[ai/foundations/generalization-and-overfitting|overfitting]] ·
[[ai/machine-learning/regularization-l1-l2|L1/L2]] ·
[[ai/deep-learning/training-dynamics|dinámicas de entrenamiento]]
