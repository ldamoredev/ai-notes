---
title: "Backpropagation from first principles"
description: Reverse-mode automatic differentiation as graph bookkeeping: local derivatives, adjoints, accumulation, and a complete scalar engine.
tags: [autodiff, backpropagation, gradients, computation-graphs]
order: 1
updated: 2026-07-19
kind: concept
level: foundational
status: flagship
prerequisites: [vectors-matrices-and-tensors, gradient-descent-and-optimization]
last_verified: 2026-07-19
---
# Backpropagation from first principles

Backpropagation is not a neural-network trick. It is an efficient way to evaluate
the chain rule on a directed acyclic computation graph when one scalar output
depends on many inputs. The forward pass records values and dependencies; the
reverse pass propagates each node's contribution to the final output.

Once that mechanism is visible, framework calls such as `loss.backward()` become a
convenient implementation of graph traversal, local derivatives, and gradient
accumulation—not magic.

## The derivative question training actually asks

Let a model with parameters \(\theta\) produce a scalar loss \(L\). Training needs
one number per parameter:

\[
\nabla_\theta L =
\left[\frac{\partial L}{\partial \theta_1}, \ldots,
\frac{\partial L}{\partial \theta_P}\right].
\]

Finite differences could perturb every parameter and rerun the model. That takes
roughly one forward evaluation per parameter. Reverse-mode autodiff obtains all
those derivatives with one forward traversal and one reverse traversal, usually
within a small constant factor of the forward cost.

## A graph, not a stack of layers

Consider:

\[
a = xw, \qquad b = a + c, \qquad L = b^2.
\]

For `x = 2`, `w = -3`, and `c = 10`:

| Node | Expression | Forward value |
|---|---|---:|
| `a` | `x * w` | -6 |
| `b` | `a + c` | 4 |
| `L` | `b ** 2` | 16 |

The graph stores edges from each input to the operation that consumes it. A reverse
topological traversal visits every consumer before its inputs.

## Local derivatives and adjoints

Define the adjoint of node \(v\) as:

\[
\bar{v} = \frac{\partial L}{\partial v}.
\]

Seed the output with \(\bar{L} = 1\). Every operation receives an upstream adjoint,
multiplies it by a local derivative, and contributes the result to its parents.

For the example:

\[
\bar{b}=\bar{L}\frac{\partial L}{\partial b}=1\cdot2b=8,
\]

\[
\bar{a}=\bar{b}\frac{\partial b}{\partial a}=8,
\qquad
\bar{c}=\bar{b}\frac{\partial b}{\partial c}=8,
\]

\[
\bar{x}=\bar{a}\frac{\partial a}{\partial x}=8w=-24,
\qquad
\bar{w}=\bar{a}\frac{\partial a}{\partial w}=8x=16.
\]

The global derivative is assembled from local facts: multiplication knows the
other operand; addition contributes one; squaring contributes twice its input.

## Why gradients must accumulate

If a value reaches the loss through several paths, its derivative is the sum of
every path contribution. For `y = x*x + x`, the same `x` is used three times:

\[
\frac{dy}{dx} = x + x + 1 = 2x + 1.
\]

An engine that assigns `parent.grad = contribution` silently loses paths. Correct
reverse mode uses `parent.grad += contribution`. This small detail explains many
hand-written autodiff bugs.

## Executable artifact: a scalar reverse-mode engine

The repository contains a complete dependency-free implementation:

```bash
python3 labs/glassbox/v1_autodiff.py
python3 -m unittest labs.glassbox.test_glassbox -v
```

The irreducible core is:

```python
def backward(self) -> None:
    topo: list[Value] = []
    visited: set[int] = set()

    def build(node: Value) -> None:
        if id(node) in visited:
            return
        visited.add(id(node))
        for parent in node.parents:
            build(parent)
        topo.append(node)

    build(self)
    self.grad = 1.0
    for node in reversed(topo):
        node._backward()
```

Each overloaded operation creates a result value and closes over the local rule.
For multiplication:

```python
def __mul__(self, other: "Value | float") -> "Value":
    rhs = other if isinstance(other, Value) else Value(float(other))
    out = Value(self.data * rhs.data, (self, rhs), "*")

    def _backward() -> None:
        self.grad += rhs.data * out.grad
        rhs.grad += self.data * out.grad

    out._backward = _backward
    return out
```

Run the script and it compares the analytical gradient with a centered finite
difference. The expected output includes `gradient_check=True`.

## Gradient checking

For a scalar parameter \(x\), a centered difference is:

\[
\frac{\partial L}{\partial x} \approx
\frac{L(x+\epsilon)-L(x-\epsilon)}{2\epsilon}.
\]

It is a debugging oracle, not a training algorithm. Use double precision, several
random coordinates, and a relative-error comparison. An epsilon that is too large
measures curvature; one that is too small loses the difference to floating-point
rounding.

## What tensor frameworks add

The scalar engine exposes the algorithm, but production autodiff systems also need:

- Vector-Jacobian products instead of materializing full Jacobian matrices.
- Broadcasting rules and reduction gradients that restore the original shape.
- Saved tensors needed by backward kernels, plus a policy for freeing them.
- Device-specific kernels, streams, mixed precision, and distributed collectives.
- Mutation/version tracking so in-place updates cannot invalidate saved values.
- Higher-order derivatives, graph retention, and checkpoint recomputation.

If \(f:\mathbb{R}^n\rightarrow\mathbb{R}^m\), the full Jacobian has \(mn\)
entries. Reverse mode instead propagates \(v^T J_f\), a vector-Jacobian product.
For training, \(m=1\), so one reverse pass is the natural direction. Forward mode
is preferable when there are few inputs and many outputs.

## Failure modes

- **Vanishing or exploding gradients.** Long products of Jacobians shrink toward
  zero or grow without bound. Initialization, normalization, residual paths, and
  gradient clipping alter that signal geometry.
- **Disconnected parameters.** A parameter absent from the loss graph gets no
  gradient. Treat `None` and numerical zero as different diagnostic states.
- **Stale accumulation.** Many frameworks accumulate into `.grad`; forgetting to
  clear gradients mixes optimization steps.
- **Non-differentiable control.** Index choices, sampling, and hard thresholds do
  not provide ordinary gradients through the decision.
- **In-place mutation.** Changing a value saved for backward can make the computed
  derivative inconsistent with the forward pass.
- **Memory pressure.** Activations retained for backward often dominate training
  memory. Checkpointing trades extra forward compute for fewer saved tensors.

## Production lens

Instrument the forward and backward phases separately. Track step time, peak memory,
gradient norm by layer, the fraction of non-finite values, and optimizer-skipped
steps. A loss curve alone cannot distinguish an unhealthy gradient graph from bad
data or a poor learning rate.

For large models, backward is also a communication schedule. Distributed training
overlaps gradient all-reduce with remaining computation, and the bucket order can
materially change utilization. Precision policy matters: loss scaling protects
small gradients in low precision, but master weights and selected reductions often
remain in higher precision.

## Exercises

1. Add subtraction, division, `tanh`, and `exp` to `v1_autodiff.py` and gradient-check
   every operation.
2. Evaluate `y = x*x + x` at `x = 3`; confirm that the engine returns `7`, then
   replace `+=` with `=` and explain the failure.
3. Build a two-neuron multilayer perceptron from scalar `Value` objects and train it
   on four binary examples.
4. Estimate the memory saved by checkpointing half of a 24-layer model when each
   layer retains 200 MB of activations.

**Connects to:** [[ai/mathematics-for-ai/gradient-descent-and-optimization|gradient descent and optimization]] · [[ai/mathematics-for-ai/vectors-matrices-and-tensors|vectors, matrices, and tensors]] · [[ai/deep-learning/initialization-and-normalization|initialization and normalization]] · [[ai/model-architectures/self-attention-from-first-principles|self-attention from first principles]]

## Sources

- [Automatic Differentiation in Machine Learning: a Survey](https://jmlr.org/papers/v18/17-468.html) — a precise taxonomy of forward and reverse modes and their complexity.
- [PyTorch autograd mechanics](https://docs.pytorch.org/docs/stable/notes/autograd.html) — framework-level graph, saved-tensor, and non-differentiability behavior.
- [JAX automatic differentiation](https://docs.jax.dev/en/latest/automatic-differentiation.html) — executable examples of transformations, higher-order derivatives, and Jacobian products.
- [micrograd](https://github.com/karpathy/micrograd) — a compact scalar engine that makes reverse-mode bookkeeping inspectable.
- [Deep Learning, Chapter 6](https://www.deeplearningbook.org/contents/mlp.html) — computation graphs and back-propagation in the broader neural-network context.
