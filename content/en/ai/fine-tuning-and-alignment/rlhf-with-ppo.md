---
title: "RLHF with PPO, conceptually"
description: RLHF trains a model to prefer human-approved outputs using a reward model and policy optimization, but it is complex and easy to destabilize.
tags: [alignment, rlhf, ppo, preference-learning]
order: 5
updated: 2026-06-07
---
# RLHF with PPO, conceptually

Reinforcement Learning from Human Feedback (RLHF) is the classic post-training recipe
behind helpful chat models. It teaches a model which outputs humans prefer, not just
which output appears in a supervised dataset.

## The three-stage shape

1. **SFT model** — start with a model that already follows instructions.
2. **Reward model** — train a model to score responses from human preference comparisons.
3. **PPO optimization** — update the policy model to produce responses that score well.

The reward model becomes a proxy for human judgment. PPO then pushes the model toward
answers the reward model likes while trying not to drift too far from the SFT model.

## Why PPO needs constraints

If you optimize only reward, the policy can exploit reward-model bugs. RLHF usually
adds a KL penalty so the new model stays near the reference model.

| Component | Purpose |
|---|---|
| Reward model | Approximate human preference |
| Policy model | The model being aligned |
| Reference model | Anchor to prevent wild drift |
| KL penalty | Discourage reward hacking |

## Why teams often avoid it

RLHF with PPO is powerful but operationally heavy: preference data, reward-model
training, policy optimization, stability tuning, and careful evaluation. For many
fine-tuning projects, [[ai/fine-tuning-and-alignment/direct-preference-optimization|DPO]]
gets most of the preference-alignment benefit with less machinery.

## Pitfall

The reward model is not truth. It is another learned model with blind spots, and the
policy will learn to exploit those blind spots if evaluation is weak.

**Connects to:** [[ai/fine-tuning-and-alignment/supervised-fine-tuning|SFT]] ·
[[ai/fine-tuning-and-alignment/direct-preference-optimization|DPO]] ·
[[ai/fine-tuning-and-alignment/evaluating-a-finetune|evaluating alignment]]
