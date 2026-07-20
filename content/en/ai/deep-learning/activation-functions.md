---
title: "Activation functions & why nonlinearity matters"
description: A stack of linear layers collapses algebraically into one matrix; the activation is what makes depth buy anything, and it is also where neurons can die permanently.
tags: [deep-learning, activations, relu, gelu]
order: 2
updated: 2026-07-20
kind: concept
level: foundational
status: current
prerequisites: [ai/computation-and-autodiff/backpropagation-from-first-principles]
last_verified: 2026-07-20
translation: stale
---
# Activation functions & why nonlinearity matters

**Mental model:** an activation is the only nonlinear step between linear layers.
Remove it and a hundred stacked layers collapse algebraically into a single linear
map — depth buys nothing without it. The nonlinearity is what lets a network bend
space so a later linear boundary can separate things the input space could not.

## Mechanism: why linear layers collapse

A layer without an activation computes \(h = Wx + b\). Stack two such layers:

\[
y = W_2(W_1 x + b_1) + b_2 = (W_2 W_1)\,x + (W_2 b_1 + b_2).
\]

That is exactly the form of a *single* linear layer with combined weight
\(W' = W_2 W_1\) and bias \(b' = W_2 b_1 + b_2\). No matter how many layers you stack,
composing linear maps only ever produces another linear map — a matrix product is
still a matrix.

**Numeric example.** Let \(W_1 = \begin{bmatrix}2&0\\1&1\end{bmatrix}\),
\(W_2 = \begin{bmatrix}1&1\\0&2\end{bmatrix}\), no bias. Multiplying them:

\[
W_2 W_1 = \begin{bmatrix}1&1\\0&2\end{bmatrix}\begin{bmatrix}2&0\\1&1\end{bmatrix}
= \begin{bmatrix}3&1\\2&2\end{bmatrix}.
\]

For any input \(x\), the two-layer "network" \(y = W_2(W_1 x)\) produces exactly the
same output as the single layer \(y = \begin{bmatrix}3&1\\2&2\end{bmatrix}x\). Add a
nonlinearity between the layers and this collapse is no longer possible — each layer
can now reshape space in a way the next layer's linear map cannot undo.

## The usual suspects

| Activation | Shape | Notes |
|---|---|---|
| **Sigmoid / tanh** | squashing | saturate for large-magnitude inputs, gradient → 0 |
| **ReLU** | \(\max(0, x)\) | default workhorse — cheap, sparse, gradient exactly 1 for positive inputs |
| **Leaky ReLU / ELU** | ReLU with a small negative slope | fixes dead neurons at the cost of exact sparsity |
| **GELU / SiLU** | smooth, ReLU-like | standard inside transformers |

Sigmoids saturate: their gradient approaches 0 for large-magnitude inputs, so a deep
stack of them suffers [[ai/computation-and-autodiff/backpropagation-from-first-principles|vanishing
gradients]] and barely trains. ReLU's gradient is exactly 1 for any positive
pre-activation, so signal passes through arbitrarily deep networks unattenuated — the
main reason very deep nets became trainable.

## Worked example: how one outlier permanently kills a ReLU neuron

A ReLU neuron's gradient is \(\text{relu}'(z) = 1\) if \(z>0\), else \(0\), where
\(z = wx+b\). If a single large update pushes \(z \le 0\) for the entire input
domain, the gradient is 0 forever after — the neuron cannot recover because updating
requires a nonzero gradient it no longer has. Train `y = relu(wx+b)` toward the
target `y = 2x` with SGD, learning rate 0.1, starting `w=1.0, b=0.0`:

| Step | Input `x`, target `y` | `w` after | `b` after |
|---|---|---:|---:|
| 1 | `x=1, y=2` | 1.100 | 0.100 |
| 2 | `x=2, y=4` | 1.440 | 0.270 |
| 3 | `x=3, y=6` | 1.863 | 0.411 |
| outlier | `x=50, y=0` | **-465.942** | **-8.945** |

The outlier's huge pre-activation (`93.561`) produces a huge gradient
(`dw = 4678.05`), and the update overshoots so far that `w` flips sign. For every
subsequent non-negative `x`, `z = wx+b ≤ b < 0`, so the neuron outputs 0 and its
gradient is exactly 0 — it is dead for the rest of training, regardless of target.

## Executable artifact

Run with `python3`; expected output is the four `(w, b)` pairs above, then three more
lines each showing `dw=0.0 db=0.0` — the dead-neuron confirmation:

```python
def relu(z):
    return z if z > 0 else 0.0

def relu_grad(z):
    return 1.0 if z > 0 else 0.0

def step(w, b, x, y_true, lr):
    z = w * x + b
    pred = relu(z)
    dloss_dpred = pred - y_true
    g = relu_grad(z)
    dw, db = dloss_dpred * g * x, dloss_dpred * g
    return w - lr * dw, b - lr * db, dw, db

w, b, lr = 1.0, 0.0, 0.1
for x, y in [(1, 2), (2, 4), (3, 6)]:
    w, b, dw, db = step(w, b, x, y, lr)
    print(round(w, 3), round(b, 3))

w, b, dw, db = step(w, b, 50, 0, lr)          # the outlier
print("outlier ->", round(w, 3), round(b, 3))

for x, y in [(1, 2), (2, 4), (3, 6)]:          # neuron is dead: no more movement
    w, b, dw, db = step(w, b, x, y, lr)
    print("dw=", round(dw, 3) + 0, "db=", round(db, 3) + 0)
```

## What framework defaults hide

`torch.nn.ReLU()` or `nn.functional.gelu` is one line, but the choice encodes an
assumption about the input distribution the layer normally sees. A framework does not
warn you when a learning-rate spike, a bad batch, or bad initialization pushes a whole
layer into the dead regime — you only see it as a plateaued loss with no obvious
architectural cause, unless you specifically instrument the fraction of zero
activations per layer.

## Failure modes and a decision rule

- **Dead ReLU.** Demonstrated above: too-high learning rate or an outlier gradient
  buries the pre-activation in the negative region permanently.
  [[ai/deep-learning/initialization-and-normalization|Initialization]] and gradient
  clipping reduce the odds this happens early in training.
- **Saturation in sigmoid/tanh stacks.** Deep stacks of squashing activations vanish
  gradients even without any single bad update — it is a property of depth, not an
  outlier event.
- **Wrong output-layer activation.** The output layer is not "just another
  activation" — it pairs with the [[ai/deep-learning/loss-functions-in-dl|loss]]
  (softmax with cross-entropy, linear with MSE); mismatching the two trains slowly or
  not at all.

**Decision rule:** default to ReLU inside the network for cost and simplicity; switch
to GELU/SiLU specifically inside transformer blocks, where the smooth gradient near
zero measurably helps optimization at scale. If more than a small fraction of a
layer's units report zero activation across a representative batch, treat it as a
dead-neuron incident, not normal sparsity, and check learning rate and initialization
before touching architecture.

## Exercises

1. Rerun the worked example with `lr=0.01` instead of `0.1` and confirm the outlier no
   longer kills the neuron; report the resulting `w, b`.
2. Compute \(W_3 W_2 W_1\) for a third \(2\times2\) matrix of your choice and confirm a
   three-layer linear "network" still collapses to one matrix.
3. Instrument the artifact to report the fraction of zero activations across the
   normal-input batch before and after the outlier step.

**Connects to:** [[ai/computation-and-autodiff/backpropagation-from-first-principles|backpropagation]] · [[ai/deep-learning/initialization-and-normalization|initialization & normalization]] · [[ai/deep-learning/loss-functions-in-dl|loss functions]] · [[ai/llms/index|GELU in transformers]]

## Sources

- [Deep Learning, Chapter 6](https://www.deeplearningbook.org/contents/mlp.html) — activation functions in the broader feed-forward network context.
- [Gaussian Error Linear Units (GELUs)](https://arxiv.org/abs/1606.08415) — the smooth activation standard in modern transformers.
- [Deep Sparse Rectifier Neural Networks](http://proceedings.mlr.press/v15/glorot11a/glorot11a.pdf) — the original argument for ReLU's sparsity and gradient-flow advantages.
- [Stanford CS231n](https://cs231n.github.io/) — practical activation-function tradeoffs and training diagnostics.
