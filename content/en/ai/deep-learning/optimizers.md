---
title: "Optimizers: from SGD to AdamW"
description: Momentum accumulates gradient history to accelerate consistent directions; Adam's bias-corrected moment ratio provably normalizes step size to the learning rate regardless of gradient magnitude, at every parameter, from the very first step.
tags: [deep-learning, optimizers, adam, sgd, momentum]
order: 4
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/mathematics-for-ai/gradient-descent-and-optimization]
last_verified: 2026-07-20
translation: stale
---
# Optimizers: from SGD to AdamW

**Mental model:** every optimizer builds on plain
[[ai/mathematics-for-ai/gradient-descent-and-optimization|gradient descent]]
(`θ ← θ − η∇L`); the differences are entirely in how much *history* of past gradients
each one keeps and how it uses that history to reshape the step. Momentum keeps a
running direction; Adam keeps a running direction **and** a running per-parameter
scale.

## Mechanism: momentum accumulates a running gradient

Plain SGD: \(\theta_{t+1} = \theta_t - \eta\, g_t\), using only the current gradient
\(g_t\). Momentum instead updates a velocity that blends the new gradient with the
previous velocity, \(v_t = \beta v_{t-1} + g_t\), and steps along \(v_t\). For a
consistent-direction (noisy but same-sign) gradient sequence
\(g = [1.0, 1.2, 0.8, 1.1, 0.9]\) with \(\beta = 0.9\), \(v_0 = 0\):

| Step | \(g_t\) | \(v_t = 0.9v_{t-1}+g_t\) |
|---:|---:|---:|
| 1 | 1.0 | 1.00 |
| 2 | 1.2 | 2.10 |
| 3 | 0.8 | 2.69 |
| 4 | 1.1 | 3.52 |
| 5 | 0.9 | 4.07 |

By step 5 the effective step (\(\eta v_5\)) is over **4x** a single raw gradient
(\(\eta g_5\)) — momentum literally accelerates when the direction stays consistent,
the "ball rolling downhill" picking up speed. On an oscillating gradient the same
mechanism cancels opposite-sign contributions instead, damping zigzag.

## Mechanism: Adam normalizes step size, exactly, from step one

Adam tracks two running estimates per parameter: a first moment (mean) and a second
raw moment (uncentered variance) of the gradient, each with bias correction for the
fact that both start at zero:

\[
m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t, \qquad
v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2,
\]
\[
\hat m_t = \frac{m_t}{1-\beta_1^t}, \qquad
\hat v_t = \frac{v_t}{1-\beta_2^t}, \qquad
\theta_{t+1} = \theta_t - \eta\,\frac{\hat m_t}{\sqrt{\hat v_t} + \epsilon}.
\]

At \(t=1\), the bias correction is **exact**, not approximate: \(m_1 = (1-\beta_1)g_1\)
so \(\hat m_1 = g_1\); \(v_1 = (1-\beta_2)g_1^2\) so \(\hat v_1 = g_1^2\). Therefore
\(\hat m_1/\sqrt{\hat v_1} = g_1/|g_1| = \text{sign}(g_1)\) — the update magnitude at
the very first step is \(\eta\) **regardless of the gradient's magnitude**, for any
nonzero gradient. That is the literal mechanism behind "Adam is forgiving about
learning rate" and "rarely-updated parameters still move."

## Worked example

Two parameters with wildly different gradient scale, \(\eta=0.001\),
\(\beta_1=0.9\), \(\beta_2=0.999\): parameter A has \(g=1.0\); parameter B has
\(g=0.01\) — a **100x** difference in raw gradient. The formula above says both get
essentially the same first step, \(\approx\eta = 0.001\), because each parameter's
own history normalizes its own scale.

## Executable artifact

Run with `python3`; expected output is `1.0 0.001` and `0.01 0.001` — identical
step magnitude despite the 100x gradient difference:

```python
import math

def adam_step_1(g, eta=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
    m = (1 - beta1) * g
    v = (1 - beta2) * g * g
    m_hat = m / (1 - beta1)
    v_hat = v / (1 - beta2)
    return eta * m_hat / (math.sqrt(v_hat) + eps)

for g in (1.0, 0.01):
    print(g, round(adam_step_1(g), 6))
```

## The progression

- **SGD** — steps opposite the mini-batch gradient. Simple, well understood, often
  generalizes best in vision, but sensitive to the learning rate.
- **Momentum** — accumulates a velocity, shown above, that powers through noise and
  small bumps instead of zig-zagging.
- **RMSProp / Adagrad** — scale each parameter's step by its own recent gradient
  magnitude (the second-moment half of what Adam does, without the first-moment
  smoothing).
- **Adam** — momentum **and** per-parameter scaling combined, with bias correction —
  the default for most deep nets.
- **AdamW** — Adam with weight decay applied **directly to the parameter**, decoupled
  from the gradient-based moment estimates: \(\theta_{t+1} = \theta_t - \eta\left(
  \frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon} + \lambda\theta_t\right)\), instead of
  folding \(\lambda\theta_t\) into \(g_t\) before computing \(m_t, v_t\). Folding decay
  into the gradient makes its effective strength ride on the same adaptive per-parameter
  scale as the gradient signal, so parameters with small gradient history get decayed
  disproportionately; decoupling removes that unintended coupling. AdamW is the
  standard for training transformers.

## What framework defaults hide

`torch.optim.Adam(params, weight_decay=...)` implements the *coupled* L2 behavior
described above by default — it is not AdamW despite looking similar. Using
`weight_decay` with plain `Adam` and expecting AdamW's decoupled behavior is a common,
silent mistake: both run without error, but they regularize differently, and the
difference is invisible without reading the source or checking documentation.

## Failure modes and a decision rule

- **No optimizer saves a bad learning rate.** Adam reduces sensitivity to \(\eta\) but
  does not remove it — pair it with a
  [[ai/deep-learning/training-dynamics|warmup + decay schedule]]. Too high → loss
  diverges (NaNs); too low → training crawls.
- **Adam/AdamW confusion**, shown above: coupled vs. decoupled weight decay change
  what the regularizer actually does per parameter.
- **Momentum overshoot.** A high \(\beta\) with a high \(\eta\) can overshoot minima
  repeatedly on a sharp loss landscape — the same accumulated velocity that
  accelerates convergence can also accelerate past it.
- **Second-moment underflow at low precision.** \(v_t\) can underflow in fp16 for
  parameters with a long run of tiny gradients, effectively disabling the adaptive
  scaling for that parameter; mixed-precision training typically keeps optimizer
  state in fp32 specifically to avoid this.

**Decision rule:** default to **AdamW + warmup + cosine decay** for transformer and
most deep-net training. Reach for plain SGD + momentum when squeezing the last bit of
generalization out of a well-understood vision model where the extra tuning cost is
worth it.

## Production lens

Log gradient norm, per-parameter update norm, and the ratio of the two (a rough proxy
for effective learning rate per layer) — this catches the coupled-vs-decoupled decay
mistake and momentum overshoot far earlier than watching the loss curve alone. Restart
optimizer state (not just model weights) deliberately when resuming from a checkpoint
after a long gap; stale second-moment estimates from a different data regime can
distort early steps after resumption.

## Exercises

1. Recompute the momentum table with \(\beta = 0.5\) instead of \(0.9\) and explain
   why the accumulated velocity stays much closer to the raw gradient.
2. Extend the Adam artifact to `t=2` with a second gradient value for each parameter
   and check whether the step-normalization property still holds as cleanly as at
   `t=1`.
3. Write out the coupled-Adam update (`weight_decay` folded into `g_t`) for a
   parameter with a large `v̂_t` and show algebraically why its effective decay is
   smaller than for a parameter with small `v̂_t`, given the same `λ`.

**Connects to:** [[ai/mathematics-for-ai/gradient-descent-and-optimization|gradient descent]] · [[ai/deep-learning/training-dynamics|LR schedules]] · [[ai/deep-learning/initialization-and-normalization|initialization & normalization]] · [[ai/computation-and-autodiff/backpropagation-from-first-principles|backpropagation]]

## Sources

- [Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980) — the original Adam derivation, bias correction, and convergence analysis.
- [Decoupled Weight Decay Regularization](https://arxiv.org/abs/1711.05101) — the AdamW paper identifying and fixing the coupled-decay problem.
- [Deep Learning, Chapter 8](https://www.deeplearningbook.org/contents/optimization.html) — optimization algorithms for deep networks in the broader training context.
- [Stanford CS231n](https://cs231n.github.io/) — practical optimizer comparisons and training diagnostics.
