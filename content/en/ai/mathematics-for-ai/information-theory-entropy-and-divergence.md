---
title: "Information theory: entropy and divergence"
description: Surprise, entropy, cross-entropy, perplexity, and KL divergence with explicit units, directionality, and numerical checks.
tags: [information-theory, entropy, cross-entropy, kl-divergence]
order: 4
updated: 2026-07-19
kind: concept
level: foundational
status: current
prerequisites: [probability-likelihood-and-uncertainty]
last_verified: 2026-07-19
---
# Information theory: entropy and divergence

Information theory measures the cost of not knowing which event will occur. A rare
event is surprising, entropy is average surprise under the data distribution,
cross-entropy is the average coding cost when a model distribution is used instead,
and KL divergence is the extra cost created by that mismatch.

These quantities connect probabilistic prediction to the objectives used by
classifiers, language models, distillation, variational inference, and alignment.

## Surprise and units

For an event with probability \(p(x)\), self-information is:

\[
I(x)=-\log p(x).
\]

The log base determines the unit: base two gives bits; the natural logarithm gives
nats. A probability-one event carries zero surprise. An event assigned probability
zero has infinite surprise if it occurs.

## Entropy

For a discrete distribution \(P\):

\[
H(P)=-\sum_x p(x)\log p(x)=\mathbb{E}_{x\sim P}[-\log p(x)].
\]

A fair binary distribution has one bit of entropy. A deterministic binary
distribution has zero. Entropy belongs to a distribution, not to one sampled event.

## Cross-entropy and negative log-likelihood

If data come from \(P\) but predictions use \(Q\):

\[
H(P,Q)=-\sum_x p(x)\log q(x).
\]

For one-hot classification targets, this becomes `-log q(correct_class)`. Averaging
that term over examples is both categorical cross-entropy and negative log-
likelihood. Minimizing it is maximum-likelihood estimation under the model family.

## KL divergence

The excess coding cost is:

\[
D_{KL}(P\Vert Q)=\sum_x p(x)\log\frac{p(x)}{q(x)}
=H(P,Q)-H(P).
\]

KL divergence is non-negative but not a metric: it is asymmetric and has no triangle
inequality. Direction matters. `KL(P || Q)` heavily penalizes a model that assigns
near-zero probability where data have mass; `KL(Q || P)` behaves differently when
the model can concentrate on one of several modes.

## Numerical check

```python
import math

p = [0.5, 0.5]
q = [0.9, 0.1]
entropy = -sum(px * math.log(px, 2) for px in p)
cross_entropy = -sum(px * math.log(qx, 2) for px, qx in zip(p, q))
kl = sum(px * math.log(px / qx, 2) for px, qx in zip(p, q))

print(round(entropy, 6))        # 1.0 bit
print(round(cross_entropy, 6))  # 1.736966 bits
print(round(kl, 6))             # 0.736966 bits
assert abs(cross_entropy - entropy - kl) < 1e-12
```

The mismatch does not change the source entropy; it adds avoidable coding cost.

## Perplexity

If cross-entropy is measured in nats, perplexity is:

\[
\operatorname{PPL}=\exp(H(P,Q)).
\]

It is an effective branching factor, not a calibrated measure of truth or downstream
utility. Perplexities are comparable only under the same tokenizer, data, masking,
and aggregation convention. A tokenizer that uses fewer, larger tokens changes the
unit of prediction.

## What frameworks hide

Production loss functions normally accept logits and combine log-softmax with the
negative-log-likelihood reduction. This is more stable than computing softmax and
then taking a logarithm. They may also apply label smoothing, class weights, ignored
indices, or mean/sum reductions; each changes the objective or its scale.

## Failure modes and decision rules

- Never evaluate `log(softmax(logits))` naively when a fused log-softmax exists.
- Do not call KL a distance without stating its direction and support assumptions.
- A single zero in `Q` where `P` has positive mass makes `KL(P || Q)` infinite.
- Cross-entropy can improve while calibration or task utility gets worse; evaluate
  the property the product needs.
- Token-average and sequence-average loss weight examples differently.
- Label smoothing may improve generalization but weakens the interpretation as the
  exact negative log-likelihood of hard labels.

## Production lens

Log loss by dataset slice and token position, not only as a global average. Record
the tokenizer revision, reduction convention, ignored-token rules, and evaluation
corpus hash. Monitor non-finite logits and the fraction of targets receiving very
small probability. For deployed predictions, pair log loss with calibration and
decision-specific metrics.

## Exercises

1. Compute both KL directions for `P=[0.5, 0.5]` and `Q=[0.9, 0.1]`.
2. Show numerically that adding a constant to every logit leaves softmax unchanged.
3. Compare per-token and per-sequence loss for one two-token and one twenty-token
   example.

**Connects to:** [[ai/mathematics-for-ai/probability-likelihood-and-uncertainty|probability, likelihood, and uncertainty]] · [[ai/llms/pretraining-next-token|next-token pretraining]] · [[ai/evaluation/metrics-for-llm-evals|metrics for LLM evaluations]] · [[ai/fine-tuning-and-alignment/direct-preference-optimization|direct preference optimization]]

## Sources

- [Elements of Information Theory](https://onlinelibrary.wiley.com/doi/book/10.1002/047174882X) — the standard reference for entropy, coding, and divergence.
- [Information Theory, Inference, and Learning Algorithms](https://www.inference.org.uk/mackay/itila/) — a free text connecting coding and probabilistic learning.
- [PyTorch CrossEntropyLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html) — precise production semantics for logits, targets, weights, and reductions.
- [On Calibration of Modern Neural Networks](https://arxiv.org/abs/1706.04599) — shows why predictive accuracy and probability calibration must be evaluated separately.
