---
title: "Initialization & normalization"
description: Initialization sets a per-layer variance-scaling factor; compounded across depth, being off by even 10% explodes or vanishes activations exponentially. Normalization is what keeps that factor near 1 during training.
tags: [deep-learning, initialization, batchnorm, layernorm]
order: 3
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/computation-and-autodiff/backpropagation-from-first-principles]
last_verified: 2026-07-20
translation: stale
---
# Initialization & normalization

**Mental model:** every layer multiplies the variance of its input by some factor
close to (but rarely exactly) 1. Across many layers, that factor compounds
*exponentially* — a per-layer error of a few percent becomes a difference of orders of
magnitude by layer 50. Initialization picks the starting scale so that factor starts
near 1; normalization keeps it near 1 as training moves the weights away from their
initial values.

## Mechanism: solving for the variance-preserving scale

For a linear layer \(y = Wx\) with \(n\) inputs, weights drawn i.i.d. with mean 0 and
variance \(\sigma_w^2\), and inputs with variance \(\sigma_x^2\):

\[
\mathrm{Var}(y_j) = \sum_{i=1}^{n} \mathrm{Var}(W_{ji} x_i) = n\,\sigma_w^2\,\sigma_x^2.
\]

To keep \(\mathrm{Var}(y) = \mathrm{Var}(x)\) — the signal neither grows nor shrinks
passing through the layer — solve for \(\sigma_w^2 = 1/n\). That is **Xavier/Glorot**
initialization, derived for linear or tanh-like activations. ReLU zeros out roughly
half its inputs (everything negative), which halves the variance that survives the
nonlinearity; compensating requires \(\sigma_w^2 = 2/n\) — **He/Kaiming**
initialization, the default for ReLU-family activations today.

## Worked example: why "close to 1" still isn't good enough

Suppose the per-layer variance-scaling factor is off by a constant \(c\) instead of
being exactly 1 (e.g. \(\sigma_w^2\) set 10% too large or too small). After \(L\)
layers, variance is \(c^L\):

| \(c\) | after 10 layers | after 50 layers | after 100 layers |
|---:|---:|---:|---:|
| 0.9 (10% too small) | 0.349 | 0.0052 | 0.0000266 |
| 1.1 (10% too large) | 2.594 | 117.4 | 13,780.6 |

A 10% per-layer error — well within normal floating-point and hyperparameter noise —
leaves activations at roughly **1/38,000th** of their starting scale after 100 layers
in the shrinking case, or explodes past **13,000x** in the growing case. This is why
initialization is exponentially sensitive to depth even though the formula itself is
simple algebra.

## Executable artifact

Run with `python3`; expected output is `0.1` (Xavier std for fan-in 100), `0.1414`
(He std), then the six variance values from the table above:

```python
import math

def required_std(fan_in, mode):
    if mode == "xavier":
        return math.sqrt(1.0 / fan_in)
    if mode == "he":
        return math.sqrt(2.0 / fan_in)
    raise ValueError(mode)

def variance_after_layers(c, layers):
    return c ** layers

print(round(required_std(100, "xavier"), 4))
print(round(required_std(100, "he"), 4))

for c in (0.9, 1.1):
    for L in (10, 50, 100):
        print(c, L, round(variance_after_layers(c, L), 8))
```

Never initialize all weights to the same constant, including 0 — every neuron in a
layer would then compute the identical gradient and stay identical forever
(a symmetry the network can never break on its own). Randomness is what lets neurons
specialize; the variance-scaling formula only fixes the *scale* of that randomness.

## Mechanism: normalization keeps the factor near 1 during training

Initialization only sets the *starting* scale. As weights update, layer output
distributions can drift again — normalization layers rescale activations mid-training
to counter that drift, which is what lets you use higher
[[ai/deep-learning/optimizers|learning rates]] and train deeper.

| Norm | Normalizes over | Used in |
|---|---|---|
| **BatchNorm** | the batch dimension, per feature | CNNs / vision |
| **LayerNorm** | the feature dimension, per example | transformers / [[ai/llms/index|LLMs]], RNNs |

LayerNorm won in transformers because it does not depend on batch statistics — it
behaves identically at batch size 1 or 1000 and for variable-length sequences, which
matters for language where sequence length varies per example and inference often
happens one sequence at a time. BatchNorm's statistics are computed across the batch,
so a small or unrepresentative batch produces noisy normalization — fine for large,
fixed-size image batches, brittle for language.

## What framework defaults hide

`nn.Linear` in PyTorch does not leave weights at zero or at a naive scale — it applies
its own default initialization automatically, which may not match the activation you
attach afterward. Nothing errors if you pair a tanh layer with a ReLU-tuned default or
vice versa; the network still runs, just trains slower or less reliably, with no
signal pointing back to initialization as the cause.

## Failure modes and a decision rule

- **Flat or NaN loss at the very start of training** is very often initialization,
  normalization, or [[ai/deep-learning/optimizers|learning rate]] — check those three
  before touching architecture.
- **Symmetry from constant initialization**, shown above: identical neurons stay
  identical forever.
- **BatchNorm train/eval mismatch.** BatchNorm uses live batch statistics during
  training but running averages at inference; a large gap between training and
  serving batch sizes or distributions produces a train/eval discrepancy that looks
  like a bug elsewhere.
- **Normalization epsilon too small in low precision.** An epsilon tuned for fp32 can
  underflow in fp16/bf16 training, producing instability that looks like a learning-rate
  problem.

**Decision rule:** use He initialization by default for ReLU-family activations, Xavier
for tanh/sigmoid; use LayerNorm for variable-length or small-batch sequence models,
BatchNorm for large, fixed-batch vision pipelines where batch statistics are stable.
Residual connections plus LayerNorm are what make 100+ layer transformers trainable at
all — do not remove either without a specific reason.

## Production lens

Instrument per-layer activation and gradient-norm histograms during the first few
hundred training steps — a bad initialization shows up there immediately, long before
it shows up as a plateaued loss curve hours into a run. When moving to mixed precision,
re-verify normalization epsilon and initial loss scale together; they interact, and a
config that was stable in fp32 is not guaranteed stable in fp16 without adjustment.

## Exercises

1. Recompute the variance table for \(c = 0.99\) and \(c = 1.01\) at \(L=100\) and
   \(L=1000\); at what depth does a 1% per-layer error become a 10x deviation?
2. Derive the He-init variance requirement from scratch: given \(\mathrm{Var}(\text{relu}(y))
   \approx \tfrac{1}{2}\mathrm{Var}(y)\) for zero-mean symmetric \(y\), solve for
   \(\sigma_w^2\) that keeps variance constant across a ReLU layer.
3. Explain, using the BatchNorm train/eval mechanism, why a model that trains well with
   batch size 256 can degrade when served with batch size 1.

**Connects to:** [[ai/computation-and-autodiff/backpropagation-from-first-principles|vanishing gradients]] · [[ai/deep-learning/optimizers|optimizers]] · [[ai/deep-learning/activation-functions|activation functions]] · [[ai/llms/index|LayerNorm in transformers]]

## Sources

- [Delving Deep into Rectifiers](https://arxiv.org/abs/1502.01852) — the He/Kaiming initialization derivation for ReLU-family networks.
- [Understanding the difficulty of training deep feedforward neural networks](http://proceedings.mlr.press/v9/glorot10a.html) — the original Xavier/Glorot initialization analysis.
- [Batch Normalization](https://arxiv.org/abs/1502.03167) — the original method and its effect on training dynamics.
- [Layer Normalization](https://arxiv.org/abs/1607.06450) — the batch-independent alternative standard in transformers.
