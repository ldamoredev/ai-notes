---
title: "El decoder transformer"
description: Cómo la arquitectura estilo GPT ensambla attention, capas feed-forward, residuales y norms en un predictor causal del próximo token.
tags: [llms, transformers, architecture, gpt]
order: 1
updated: 2026-06-07
---
# El decoder transformer

Todo LLM estilo GPT tiene la misma forma: convertir tokens en vectores, pasarlos por
una pila de bloques idénticos y leer una distribución de probabilidad sobre el próximo
token. Entender ese pipeline desmitifica a toda la familia.

## El pipeline, de punta a punta

1. **Tokenizá** el texto en IDs enteros ([[ai/llms/tokenization|tokenization]]).
2. **Embeddeá** cada token en un vector y agregá un
   [[ai/llms/positional-encodings|positional encoding]] para representar el orden.
3. **N bloques transformer**, cada uno haciendo dos cosas:
   - **Masked self-attention**: cada token mezcla información de tokens anteriores
     (ver [[ai/model-architectures/self-attention-from-first-principles|attention]]).
   - **Feed-forward network (FFN/MLP)**: una transformación no lineal por token donde
     se almacena buena parte del "conocimiento" del modelo.
   Ambos están envueltos en **conexiones residuales** + **[[ai/deep-learning/initialization-and-normalization|LayerNorm]]**,
   que es lo que permite entrenar decenas de bloques apilados.
4. **Unembeddeá** el vector final hacia logits sobre el vocabulario; softmax →
   probabilidades del próximo token ([[ai/llms/decoding-and-sampling|decoding]] elige uno).

## "Decoder-only" y enmascaramiento causal

La propiedad clave: un token solo puede atender a tokens **anteriores** (una máscara
causal). Esto hace que el modelo sea **autoregresivo**: predice cada próximo token a
partir del contexto izquierdo, que es exactamente lo que requieren el
[[ai/llms/pretraining-next-token|pretraining]] de próximo token y la generación. (El
transformer original también tenía un encoder; los LLMs generativos modernos lo
eliminan y se quedan con el decoder.)

## Dónde viven los parámetros

- **Attention** rutea información entre posiciones (relaciones, sintaxis,
  correferencia).
- **Capas FFN** contienen aproximadamente dos tercios de los parámetros y actúan como
  la memoria asociativa del modelo para hechos y patrones.
- Profundidad (más bloques) y ancho (vectores más grandes) son las perillas principales
  de [[ai/deep-learning/scaling-laws|scaling]].

## Trampa

La arquitectura es pequeña y repetitiva: unos pocos cientos de líneas de código. La
capacidad viene de **escala y datos**, no de una genialidad arquitectónica. No busques
la magia en el diagrama; está en los billones de tokens de entrenamiento.

**Conecta con:** [[ai/model-architectures/self-attention-from-first-principles|attention]] ·
[[ai/llms/pretraining-next-token|pretraining]] ·
[[ai/llms/tokenization|tokenization]]
