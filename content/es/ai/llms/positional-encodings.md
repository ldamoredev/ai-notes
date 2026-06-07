---
title: "Positional encodings y RoPE"
description: Attention no ve orden por defecto, así que la posición debe inyectarse. Encodings absolutos vs rotary (RoPE), y por qué RoPE sostiene los modelos de long context.
tags: [llms, positional-encoding, rope, context]
order: 4
updated: 2026-06-07
---
# Positional encodings y RoPE

[[ai/deep-learning/attention-mechanism|Self-attention]] trata sus inputs como un
**conjunto**: no tiene una noción inherente de orden. Pero "perro muerde hombre" ≠
"hombre muerde perro", así que la posición debe agregarse explícitamente. Cómo se
hace eso determina en silencio hasta dónde puede extender su contexto un modelo.

## El problema

Attention calcula relevancia comparando cada token con todos los demás, ignorando
dónde están ubicados. Sin información posicional, el modelo no podría distinguir el
primero del último. Entonces inyectamos posición en las representaciones de tokens.

## De absoluto a rotary

- **Absolute positional encodings** (transformer original): agregan un vector
  dependiente de la posición a cada token embedding. Simple, pero ata el modelo a las
  posiciones que vio durante entrenamiento, así que extender más allá de la longitud
  entrenada funciona mal.
- **RoPE (Rotary Position Embedding)**: el default moderno. En vez de *agregar*
  posición, **rota** los vectores query/key por un ángulo proporcional a la posición.
  La consecuencia elegante: attention termina dependiendo de la distancia
  **relativa** entre tokens, no del índice absoluto.

## Por qué RoPE importa para long context

Como RoPE codifica posición *relativa*, se degrada con más gracia más allá de la
longitud de entrenamiento y puede **interpolarse/extenderse** (scaling NTK/YaRN) para
estirar la [[ai/llms/context-window-and-kv-cache|ventana de contexto]] de un modelo sin
reentrenamiento completo. Eso explica buena parte del salto de contextos de 2K a
128K+ tokens. Igual no vuelve *gratis* al long context: mirá
[[ai/llms/long-context-and-lost-in-the-middle|lost in the middle]].

## La idea en una línea

> Attention no ve orden; los positional encodings restauran el orden. RoPE codifica
> posición *relativa* mediante rotación, por eso los modelos long-context actuales se
> apoyan en él.

**Se conecta con:** [[ai/deep-learning/attention-mechanism|attention no ve orden]] ·
[[ai/llms/context-window-and-kv-cache|ventana de contexto]] ·
[[ai/llms/long-context-and-lost-in-the-middle|long context]]
