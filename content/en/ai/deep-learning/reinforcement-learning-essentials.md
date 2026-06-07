---
title: "Reinforcement learning, the essentials"
description: Learning from reward instead of labeled answers — agent, environment, policy, and the exploration problem. The paradigm behind RLHF, reasoning models, and agents.
tags: [reinforcement-learning, rl, policy, reward]
order: 13
updated: 2026-06-07
---
# Reinforcement learning, the essentials

[[ai/foundations/types-of-learning|Supervised learning]] needs labeled answers.
**Reinforcement learning (RL)** learns from a *reward signal* by acting and seeing what
works — no answer key, just better and worse outcomes over time. It's the paradigm
behind [[ai/fine-tuning-and-alignment/rlhf-with-ppo|RLHF]],
[[ai/llms/reasoning-and-test-time-compute|reasoning models]], and learning
[[ai/agents-and-tools/index|agents]], so it's worth the core vocabulary.

## The setup

An **agent** takes **actions** in an **environment**, which returns a new **state** and
a **reward**. The goal: learn a **policy** (a mapping from state to action) that
maximizes cumulative reward over time.

- **Policy** — the strategy: what to do in each state.
- **Reward** — the scalar feedback signal (the thing being maximized).
- **Value** — expected future reward from a state (how good is it to be here?).
- **Return** — total (often discounted) reward over a trajectory.

The framing is a Markov Decision Process; you don't need the math to use the ideas.

## What makes RL hard

- **Delayed reward / credit assignment** — the reward may come long after the action
  that earned it; which move actually mattered?
- **Exploration vs exploitation** — exploit what works, or explore to find something
  better? Too little exploration → stuck in a rut; too much → never converges.
- **Sample efficiency** — RL often needs huge amounts of interaction, which is why it
  shines in simulators/games and is harder in the real world.

## Why it matters for modern AI

- **RLHF / preference alignment** — turn human preferences into a reward and optimize
  the model toward it ([[ai/fine-tuning-and-alignment/direct-preference-optimization|DPO]]
  reframes this without a separate RL loop).
- **Reasoning models** — trained with RL on **verifiable** rewards (did the math/code
  come out right?) to produce long [[ai/prompt-engineering/chain-of-thought|chains of
  thought]].
- **Agents** — sequential decision-making under feedback is exactly the RL frame, even
  when today's agents are mostly prompted rather than RL-trained.

## Pitfall

**Reward hacking** (a Goodhart problem): the agent maximizes the *measured* reward in
unintended ways — the proxy diverges from what you actually wanted. Designing rewards is
as hard and as consequential as designing a [[ai/foundations/how-learning-works|loss]].

**Connects to:** [[ai/foundations/types-of-learning|types of learning]] ·
[[ai/fine-tuning-and-alignment/rlhf-with-ppo|RLHF]] ·
[[ai/llms/reasoning-and-test-time-compute|reasoning & test-time compute]]
