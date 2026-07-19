---
title: "Decoding y sampling"
description: Un modelo emite una distribución de probabilidad; decoding la convierte en texto. Temperature, top-p/top-k, greedy vs sampling: las perillas que controlan creatividad vs confiabilidad.
tags: [llms, decoding, sampling, temperature]
order: 6
updated: 2026-06-07
---
# Decoding y sampling

En cada paso, el [[ai/llms/the-decoder-transformer|modelo]] emite una probabilidad
sobre todo el vocabulario. **Decoding** es la estrategia para elegir el próximo token
desde esa distribución, y controla cuán creativa, repetitiva o confiable se siente la
salida, *sin cambiar el modelo en absoluto*.

## Greedy vs sampling

- **Greedy**: tomar siempre el token de mayor probabilidad. Determinístico, pero
  plano y propenso a loops.
- **Sampling**: muestrear desde la distribución, así la salida varía. Necesita
  shaping, o cada tanto elige algo incoherente.

## Las perillas

| Perilla | Efecto | Más bajo → / Más alto → |
|---|---|---|
| **Temperature** | escala la nitidez de la distribución | bajo = enfocado/determinístico; alto = creativo/aleatorio |
| **Top-k** | samplea solo desde los k tokens más probables | más chico = más seguro; más grande = más diverso |
| **Top-p (nucleus)** | samplea desde el conjunto más chico que cubre probabilidad p | adapta el pool candidato a la confianza |
| **Repetition / frequency penalty** | desalienta repetir tokens | reduce loops y repeticiones literales |

**Temperature** es la perilla principal: ~0 para extracción, clasificación, código y
cualquier cosa que necesite reproducibilidad; más alta (~0.7-1.0) para brainstorming y
prosa.

## Guía práctica

- ¿Necesitás **estructura o hechos** (JSON, clasificación, tool calls)? Usá temperature ≈ 0.
- ¿Necesitás **variedad** (ideación, escritura creativa)? Subí temperature y/o top-p.
- "El modelo es inconsistente entre corridas" suele ser temperature > 0, no un bug.
- Decoding no agrega conocimiento ni arregla la [[ai/llms/why-llms-hallucinate|alucinación]];
  temperature 0 vuelve una respuesta incorrecta *consistente*, no *correcta*.

> Mismos pesos, distinto decoding = distinto comportamiento de producto. Setealo
> deliberadamente por tarea; no dejes los defaults librados al azar.

**Conecta con:** [[ai/llms/the-decoder-transformer|logits → tokens]] ·
[[ai/prompt-engineering/index|salida estructurada]] ·
[[ai/llms/why-llms-hallucinate|alucinación]]
