---
title: Reinforcement Learning
description: Decisión secuencial desde MDPs y ecuaciones de Bellman hasta policy optimization, offline RL y fallas de recompensa.
tags: [reinforcement-learning, decision-making, policies, rewards]
order: 0
updated: 2026-07-19
status: planned
level: intermediate
---
# Reinforcement Learning

Reinforcement learning es aprender de consecuencias a lo largo del tiempo. El objeto aprendido no es un predictor de etiquetas sino una policy o una estimación de valor para decisiones secuenciales bajo incertidumbre.

## Modelo mental

Un agente observa un estado, elige una acción, recibe recompensa y transiciona. El return agrega recompensas futuras; una policy mapea estados a distribuciones de acciones; las value functions resumen retorno esperado. Las ecuaciones de Bellman exponen la recursión que aproximan los algoritmos.

## Overview actual

- [[ai/reinforcement-learning/reinforcement-learning-essentials|Fundamentos de Reinforcement Learning]]

## Roadmap

MDPs · Bellman y dynamic programming · Monte Carlo y TD · Q-learning/DQN · policy gradients · actor-critic · exploración · offline RL · model-based RL/world models · reward hacking y RLHF.

**Conecta con:** [[ai/classical-ai-and-reasoning/index|IA Clásica y Razonamiento]] · [[ai/fine-tuning-and-alignment/rlhf-with-ppo|RLHF con PPO]] · [[ai/agents-and-tools/autonomy-and-control|Autonomía y control]]

## Fuentes principales

- [Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book-2nd.html) — texto canónico de Sutton y Barto.
- [David Silver RL course](https://www.davidsilver.uk/teaching/) — recorrido riguroso desde MDPs a policy gradients.
- [OpenAI Spinning Up](https://spinningup.openai.com/) — ecuaciones e implementaciones mínimas.
