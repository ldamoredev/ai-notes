---
title: Arquitecturas de Modelos
description: Mecanismos que enrutan información y cómputo a través de espacio, tiempo, tokens, experts y trayectorias de denoising.
tags: [architectures, attention, transformers, diffusion]
order: 0
updated: 2026-07-19
status: current
level: intermediate
---
# Arquitecturas de Modelos

Una arquitectura especifica un cómputo parametrizado y sus sesgos inductivos: qué interacciones son baratas, qué caminos de información existen, qué simetrías codifica y cómo escala el costo.

## Modelo mental

Las CNN reutilizan filtros locales; las RNN comprimen historia en estado; attention crea interacciones dependientes del contenido; transformers combinan attention y transformaciones por token con caminos residuales; state-space models propagan estado estructurado; diffusion aprende denoising iterativo.

## Nota fundacional actual

- [[ai/model-architectures/self-attention-from-first-principles|Self-attention desde primeros principios]]

## Roadmap

CNNs · RNN/LSTM · transformer block · encoder/decoder · mixture of experts · state-space models · perspectivas autoregresivas y energy-based · diffusion · foundation models.

**Conecta con:** [[ai/deep-learning/index|Deep Learning]] · [[ai/llms/the-decoder-transformer|El decoder transformer]] · [[ai/multimodal-and-generative/index|Visión, Audio e IA Multimodal]]

## Fuentes principales

- [Deep Learning](https://www.deeplearningbook.org/) — fundamentos de arquitecturas neuronales.
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — arquitectura Transformer original.
- [An Image is Worth 16x16 Words](https://arxiv.org/abs/2010.11929) — Vision Transformer.
