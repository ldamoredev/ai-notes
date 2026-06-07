---
title: "Teoría de la información: entropía, cross-entropy y KL"
description: Por qué los clasificadores y LLMs se entrenan con cross-entropy, qué mide realmente perplexity y cómo KL mantiene a raya a los modelos fine-tuned.
tags: [foundations, information-theory, cross-entropy, kl-divergence]
order: 11
updated: 2026-06-07
---
# Teoría de la información: entropía, cross-entropy y KL

La teoría de la información da el vocabulario para "sorpresa" y "distancia entre
distribuciones". Vale conocerla porque el loss que entrena casi todo clasificador y
cada LLM — **cross-entropy** — sale directamente de ahí.

## Entropía = sorpresa promedio

**Entropía** mide qué tan impredecible es una distribución. Una moneda justa tiene
entropía alta (no podés predecirla); una moneda cargada tiene entropía baja. Los eventos
raros cargan más información ("sorpresa") que los comunes. La entropía es la sorpresa
promedio que esperás de una fuente.

## Cross-entropy = el loss de entrenamiento

**Cross-entropy** mide el costo de usar la distribución predicha por tu modelo cuando
la distribución *verdadera* es otra. Minimizarla empuja las probabilidades predichas
por el modelo hacia las etiquetas reales:

- Para un LLM, la distribución target pone toda la masa en el token siguiente real, así
  que cross-entropy se reduce a "maximizar la probabilidad que el modelo asignó al
  token correcto". Ese único objetivo, sobre billones de tokens, es cómo aprenden los
  LLMs. (Ver [[ai/foundations/types-of-learning|aprendizaje self-supervised]].)
- Encaja naturalmente con outputs softmax y castiga fuerte respuestas **confiadas y
  equivocadas**, que es exactamente la presión que querés.

## Perplexity = cross-entropy legible

**Perplexity** es simplemente `exp(cross-entropy)`. Intuitivamente: "entre cuántas
opciones está eligiendo efectivamente el modelo en cada paso". Más bajo es mejor; una
perplexity de 1 significa predicción perfecta. Es la métrica intrínseca clásica para
modelos de lenguaje.

## Divergencia KL = distancia entre distribuciones

La **divergencia KL** mide qué tan lejos está una distribución de otra (no es simétrica).
Dos lugares donde aparece constantemente:

- **Alineación por preferencias** — [[ai/fine-tuning-and-alignment/index|RLHF y DPO]]
  agregan una penalización KL para que el modelo tuneado no se aleje demasiado del
  modelo base, preservando fluidez mientras cambia comportamiento.
- **Distillation** — un modelo student se entrena para matchear la distribución de
  salida completa de un teacher mediante un loss estilo KL.

## El resumen de un párrafo

> Entropía = impredecibilidad. Cross-entropy = el loss que entrena clasificadores y
> LLMs. Perplexity = cross-entropy hecha legible. KL = qué tan lejos están dos
> distribuciones, la correa que mantiene anclados los fine-tunes.

**Se conecta con:** [[ai/foundations/how-learning-works|loss y objetivo]] ·
[[ai/foundations/probability-and-uncertainty|probabilidad]] ·
[[ai/llms/index|entrenamiento de LLMs]]
