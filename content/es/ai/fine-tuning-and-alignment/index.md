---
title: Entrenamiento y Adaptación
description: Training loops, infraestructura distribuida, SFT, adapters, preferencias, distillation y aprendizaje continuo.
tags: [training, fine-tuning, alignment, adaptation]
order: 0
updated: 2026-07-19
---
# Entrenamiento y Adaptación

Adaptar un modelo cambia sus parámetros y por lo tanto su distribución de comportamiento. La técnica importa menos que la calidad de datos, el baseline, el objetivo, la infraestructura, las evals y la capacidad de revertir.

## Modelo mental

La adaptación cambia comportamiento con ejemplos, preferencias o señales de un teacher. Objetivo, reference model, superficie de parámetros y dataset determinan qué mejora y qué puede olvidarse.

## Hoja de ruta actual

- [[ai/fine-tuning-and-alignment/when-to-fine-tune|Cuándo fine-tunear]]
- [[ai/fine-tuning-and-alignment/supervised-fine-tuning|Supervised fine-tuning]]
- [[ai/fine-tuning-and-alignment/lora-and-adapters|LoRA y adapters]]
- [[ai/fine-tuning-and-alignment/qlora-and-4bit-finetuning|QLoRA]]
- [[ai/fine-tuning-and-alignment/rlhf-with-ppo|RLHF con PPO]]
- [[ai/fine-tuning-and-alignment/direct-preference-optimization|DPO]]
- [[ai/fine-tuning-and-alignment/building-the-finetuning-dataset|Dataset de fine-tuning]]
- [[ai/fine-tuning-and-alignment/data-quality-for-finetuning|Calidad de datos]]
- [[ai/fine-tuning-and-alignment/catastrophic-forgetting|Catastrophic forgetting]]
- [[ai/fine-tuning-and-alignment/distillation|Distillation]]
- [[ai/fine-tuning-and-alignment/evaluating-a-finetune|Evaluar un fine-tune]]
- [[ai/fine-tuning-and-alignment/cost-and-hardware|Costo y hardware]]

**Conecta con:** [[ai/data-for-ai/index|Datos para IA]] · [[ai/reinforcement-learning/index|Reinforcement Learning]] · [[ai/inference-and-optimization/index|Sistemas de Inferencia]]

## Fuentes principales

- [LoRA](https://arxiv.org/abs/2106.09685) · [QLoRA](https://arxiv.org/abs/2305.14314) · [DPO](https://arxiv.org/abs/2305.18290) — papers primarios.
- [PyTorch Distributed](https://pytorch.org/tutorials/beginner/dist_overview.html) — infraestructura de entrenamiento distribuido.
