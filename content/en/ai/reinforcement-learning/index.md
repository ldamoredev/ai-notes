---
title: Reinforcement Learning
description: Sequential decision making from Markov decision processes and Bellman equations to policy optimization, offline RL, and reward failure.
tags: [reinforcement-learning, decision-making, policies, rewards]
order: 0
updated: 2026-07-19
status: planned
level: intermediate
---
# Reinforcement Learning

Reinforcement learning is learning from consequences over time. The object being learned is not a label predictor but a policy or value estimate for sequential decisions under uncertainty.

## Mental model

An agent observes a state, chooses an action, receives a reward, and transitions. Return aggregates future rewards; a policy maps states to action distributions; value functions summarize expected return. Bellman equations expose the recursive structure that most RL algorithms approximate.

## Current overview

- [[ai/reinforcement-learning/reinforcement-learning-essentials|Reinforcement Learning Essentials]]

## Candidate note roadmap

- `mdps-returns-policies-and-values` — formal problem definition and assumptions.
- `bellman-equations-and-dynamic-programming` — policy evaluation, improvement, and value iteration.
- `monte-carlo-and-temporal-difference-learning` — sampled returns, bootstrapping, bias, and variance.
- `q-learning-and-deep-q-networks` — off-policy control, replay, target networks, and instability.
- `policy-gradients-from-first-principles` — score-function estimator, baselines, and variance reduction.
- `actor-critic-methods` — learned critics, advantage estimation, and implementation tradeoffs.
- `exploration-and-credit-assignment` — uncertainty, sparse rewards, and long horizons.
- `offline-rl-and-dataset-coverage` — distribution shift, conservatism, and evaluation without deployment.
- `model-based-rl-and-world-models` — learned dynamics, planning, model error, and compounding bias.
- `reward-hacking-rlhf-and-rlaif` — specification gaming and connections to model alignment.

## Scope

This branch separates RL as a field from RLHF as one adaptation technique. Examples start in tabular environments before neural approximators hide the mechanism.

**Connects to:** [[ai/classical-ai-and-reasoning/index|Classical AI and Reasoning]] · [[ai/fine-tuning-and-alignment/rlhf-with-ppo|RLHF with PPO]] · [[ai/agents-and-tools/autonomy-and-control|Autonomy and Control]]

## Core sources

- [Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book-2nd.html) — canonical free text by Sutton and Barto.
- [David Silver's Reinforcement Learning course](https://www.davidsilver.uk/teaching/) — rigorous lectures from MDPs through policy gradients.
- [OpenAI Spinning Up](https://spinningup.openai.com/) — equations and minimal implementations for deep RL.
- [Offline Reinforcement Learning: Tutorial, Review, and Perspectives](https://arxiv.org/abs/2005.01643) — map of the offline setting and its distribution-shift problem.
