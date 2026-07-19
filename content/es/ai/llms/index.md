---
title: LLMs
description: Cómo funcionan realmente los large language models: el decoder transformer, tokenization, pretraining, decoding, contexto y los comportamientos (y modos de falla) que se desprenden.
tags: [llms, transformers]
order: 0
updated: 2026-06-07
---
# LLMs

Un large language model es un [[ai/model-architectures/self-attention-from-first-principles|transformer]]
entrenado con un objetivo engañosamente simple: **predecir el próximo token**, a una
escala enorme. Todo lo que resulta mágico o irritante de los LLMs (in-context
learning, alucinación, sensibilidad al wording) sale de ese objetivo y de la
arquitectura que lo rodea. Esta rama construye el modelo mental desde adentro hacia
afuera.

> Un LLM es un predictor del próximo token. Es asombrosamente capaz *y* no tiene una
> noción incorporada de verdad: ambas cosas vienen del mismo objetivo de entrenamiento.

## Modelo mental

Un modelo de lenguaje factoriza la probabilidad de una secuencia en predicciones repetidas del próximo token. El transformer produce logits, decoding compromete un token y ese prefijo vuelve a ser el próximo input.

## Hoja de ruta: arquitectura a comportamiento

- [[ai/llms/from-prompt-to-generated-token|Del prompt al token generado]]

- [[ai/llms/the-decoder-transformer|El decoder transformer]]
- [[ai/llms/transformer-attention-map|Mapa de attention del transformer]]
- [[ai/llms/tokenization|Tokenization: por qué los modelos ven tokens, no palabras]]
- [[ai/llms/positional-encodings|Positional encodings y RoPE]]

## Entrenamiento y adaptación

- [[ai/llms/pretraining-next-token|Pretraining: predicción del próximo token]]
- [[ai/llms/base-vs-instruct|Modelos base vs instruct vs chat]]
- [[ai/llms/emergent-abilities-and-scale|Emergent abilities e in-context learning]]

## Generación y contexto

- [[ai/llms/decoding-and-sampling|Decoding y sampling]]
- [[ai/llms/context-window-and-kv-cache|Ventana de contexto y KV cache]]
- [[ai/llms/long-context-and-lost-in-the-middle|Long context y lost in the middle]]
- [[ai/llms/reasoning-and-test-time-compute|Reasoning y test-time compute]]

## Comportamiento y despliegue

- [[ai/llms/why-llms-hallucinate|Por qué alucinan los LLMs]]
- [[ai/llms/quantization-and-inference|Quantization e inferencia]]

**Conecta con:** [[ai/model-architectures/index|Arquitecturas]] · [[ai/fine-tuning-and-alignment/index|Entrenamiento y Adaptación]] · [[ai/inference-and-optimization/index|Sistemas de Inferencia]]

## Fuentes principales

- Andrej Karpathy — *Let's build GPT*, *Intro to LLMs*, *Deep Dive into LLMs*.
- Sebastian Raschka — *Build a Large Language Model (From Scratch)*.
- Jay Alammar — *The Illustrated Transformer* / *Illustrated GPT-2*.
- Hugging Face — *LLM Course*; Jurafsky & Martin — *Speech and Language Processing* (SLP3).
- Lilian Weng — blog (attention, hallucination, agents).
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — arquitectura transformer.
- [Speech and Language Processing](https://web.stanford.edu/~jurafsky/slp3/) — referencia actual de NLP y LLMs.
- [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/) — material ejecutable.
