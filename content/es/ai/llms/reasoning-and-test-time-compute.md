---
title: "Reasoning y test-time compute"
description: Chain-of-thought y reasoning models intercambian compute de inferencia por accuracy: el modelo "piensa" antes de responder. Qué cambió, cuándo ayuda y qué cuesta.
tags: [llms, reasoning, chain-of-thought, test-time-compute]
order: 12
updated: 2026-06-07
---
# Reasoning y test-time compute

Un cambio reciente importante: en vez de escalar solo el *entrenamiento*, podés escalar
la **inferencia**: dejar que el modelo genere razonamiento intermedio antes de su
respuesta final. Gastar más tokens (más compute) al responder mejora de forma medible
las tareas difíciles.

## De chain-of-thought a reasoning models

- **Prompting chain-of-thought (CoT)**: pedirle al modelo que "piense paso a paso"
  produce pasos intermedios y mejora problemas multi-step. Funciona porque la
  generación es secuencial: los pasos escritos se vuelven contexto sobre el que los
  tokens posteriores pueden construir (el modelo no puede hacer compute oculto
  ilimitado en un solo paso).
- **Reasoning models**: modelos más nuevos están *entrenados* (a menudo con RL sobre
  problemas verificables) para producir razonamiento interno largo antes de responder.
  En efecto hacen CoT nativamente y gastan una cantidad variable de "pensamiento" por
  problema.

## Test-time compute como nuevo eje de scaling

La idea: para un modelo fijo, **dejarlo pensar más tiempo** (más tokens de reasoning,
muestrear varios intentos y elegir el mejor) sube la accuracy en matemática, código y
lógica: una palanca distinta a hacer el modelo más grande. El compute se movió en
parte desde pretraining hacia inferencia.

## Cuándo ayuda, y cuándo no

| Usá reasoning para | Saltealo para |
|---|---|
| matemática, código, lógica, planificación multi-step | lookup simple, clasificación, extracción |
| problemas con pasos verificables | llamadas sensibles a latencia y de alto volumen |

Los costos son reales: los tokens de reasoning implican **mayor latencia y precio**, y
en tareas fáciles el pensamiento extra suma costo con poca ganancia (a veces pensar de
más empeora). Tampoco arregla la [[ai/llms/why-llms-hallucinate|alucinación]]: una
cadena confiada e incorrecta sigue siendo incorrecta.

> Reasoning intercambia [[ai/ai-product-engineering/index|latencia y costo]] por
> accuracy. Gastalo donde el problema sea genuinamente difícil; usá modelos rápidos
> por default en el resto.

**Se conecta con:** [[ai/llms/emergent-abilities-and-scale|in-context learning]] ·
[[ai/prompt-engineering/index|prompting chain-of-thought]] ·
[[ai/ai-product-engineering/index|latencia vs calidad]]
