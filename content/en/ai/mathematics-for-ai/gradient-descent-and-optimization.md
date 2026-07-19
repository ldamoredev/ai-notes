---
title: Gradient Descent and Optimization
description: Objectives, gradients, learning rates, convex intuition, non-convex training, numerical verification, and an executable optimizer from first principles.
tags: [optimization, gradient-descent, objectives, learning-rate]
order: 3
updated: 2026-07-19
kind: implementation
level: beginner
status: current
prerequisites: [ai/mathematics-for-ai/vectors-matrices-and-tensors]
last_verified: 2026-07-19
---
# Gradient Descent and Optimization

Optimization turns a learning objective into parameter changes. A gradient is not “the direction the model should learn”; it is the vector of local partial derivatives of a scalar objective with respect to chosen parameters at the current point.

The mental model is: compute the loss, compute its local slope in every parameter direction, choose an update rule and step size, apply the update, then measure both objective behavior and task behavior. The gradient supplies local information. The optimizer supplies a trajectory.

## Problem and notation

Let parameters be `θ ∈ R^P`, data be `D`, and scalar objective be:

```text
J(θ; D) ∈ R
```

The gradient is:

```text
∇J(θ) = [∂J/∂θ₁, …, ∂J/∂θ_P]
```

For a small displacement `Δθ`, first-order approximation gives:

```text
J(θ + Δθ) ≈ J(θ) + ∇J(θ) · Δθ
```

Under Euclidean geometry and a fixed small step length, the steepest local decrease is opposite the gradient. Gradient descent uses:

```text
θₜ₊₁ = θₜ - η ∇J(θₜ)
```

where `η > 0` is the learning rate.

## One-dimensional numerical example

Minimize:

```text
J(w) = (w - 3)²
dJ/dw = 2(w - 3)
```

Start with `w₀ = 0` and `η = 0.1`:

```text
t=0: w=0.000, gradient=-6.000, loss=9.000
t=1: w=0.600, gradient=-4.800, loss=5.760
t=2: w=1.080, gradient=-3.840, loss=3.6864
t=3: w=1.464, gradient=-3.072, loss=2.3593
```

The update approaches `w=3`. If `η=1`, the update oscillates between `0` and `6`; if `η>1`, it diverges for this objective. A correct gradient does not rescue a bad step size.

## Linear regression from scratch

For examples `(xᵢ, yᵢ)`, prediction `ŷᵢ = wxᵢ + b`, and mean squared error:

```text
J(w,b) = (1/n) Σᵢ (wxᵢ + b - yᵢ)²
∂J/∂w = (2/n) Σᵢ (ŷᵢ - yᵢ)xᵢ
∂J/∂b = (2/n) Σᵢ (ŷᵢ - yᵢ)
```

Minimal executable training loop:

```python
xs = [0.0, 1.0, 2.0, 3.0]
ys = [1.0, 3.0, 5.0, 7.0]  # y = 2x + 1
w, b, learning_rate = 0.0, 0.0, 0.05

for step in range(500):
    errors = [w * x + b - y for x, y in zip(xs, ys)]
    loss = sum(error * error for error in errors) / len(xs)
    dw = 2 * sum(error * x for error, x in zip(errors, xs)) / len(xs)
    db = 2 * sum(errors) / len(xs)
    w -= learning_rate * dw
    b -= learning_rate * db

assert abs(w - 2.0) < 1e-3
assert abs(b - 1.0) < 1e-3
print(round(loss, 8), round(w, 4), round(b, 4))
```

The code implements exactly the derivatives above. A tensor framework would vectorize the same operations and autograd would produce `dw` and `db`.

## Batch, stochastic, and mini-batch gradients

- Batch gradient descent uses all training examples per update: stable estimate, expensive step.
- Stochastic gradient descent uses one example: cheap noisy step.
- Mini-batch SGD uses a subset: hardware-efficient compromise and the standard deep-learning regime.

The mini-batch gradient is an estimator of the full-data gradient. Batch composition, sampling, class imbalance, correlation, and distributed sharding change its noise and bias.

An epoch is one pass through the chosen training set. A step is one parameter update. With `N` examples and batch size `B`, one epoch has approximately `ceil(N/B)` steps.

## Convex intuition

For a differentiable convex objective, every local minimum is global. With suitable step sizes, gradient methods have analyzable convergence behavior. Linear regression with squared loss is a useful convex case.

Convex intuition teaches slope, conditioning, and step size. It does not imply neural-network training has one basin or that the found solution is globally optimal.

## Non-convex reality

Deep networks create non-convex objectives with symmetries, flat regions, saddle points, sharp directions, and many parameter configurations representing similar functions. Practical success depends on architecture, initialization, normalization, data order, batch noise, schedules, and regularization.

The optimization target is training loss plus explicit penalties. The product target is something else. A lower training objective can worsen validation performance, calibration, subgroup behavior, robustness, or downstream utility.

## Learning rate and conditioning

If contours are elongated, one direction changes loss much faster than another. A single scalar learning rate may bounce across steep directions while moving slowly along flat ones. Feature scaling, normalization, momentum, and adaptive preconditioning change this geometry or the update.

Useful symptoms:

- Loss explodes or becomes NaN: step too large, unstable computation, or bad data.
- Loss decreases extremely slowly: step too small, poor conditioning, saturation, or gradient scale issue.
- Training improves but validation worsens: generalization/overfitting issue, not necessarily optimizer failure.
- Gradient norm is zero or enormous: inspect activations, loss scaling, clipping, and graph connectivity.

## Momentum and adaptive methods

Momentum maintains a velocity-like exponential accumulation:

```text
vₜ = βvₜ₋₁ + gₜ
θₜ₊₁ = θₜ - ηvₜ
```

Adam additionally tracks first and second gradient moments and applies bias correction. These methods change per-parameter updates; they do not change the data, objective, or meaning of the gradient. Optimizer choice can affect training speed and the solution reached, so it is part of the experiment specification.

## Gradient checking

Centered finite differences approximate one derivative:

```text
∂J/∂θᵢ ≈ [J(θᵢ + ε) - J(θᵢ - ε)] / (2ε)
```

Use it on tiny deterministic functions to verify analytical or autodiff gradients. It costs two forward evaluations per checked parameter and suffers from floating-point cancellation if `ε` is too small, so it is a test—not a training algorithm.

Glassbox v1 performs this check:

```bash
python3 -m labs.glassbox.v1_autodiff
python3 -m unittest labs.glassbox.test_glassbox.AutodiffTests -v
```

Expected result includes `gradient_check: True`.

## What frameworks hide

- Which scalar loss is differentiated when outputs are batched.
- Gradient accumulation versus overwrite.
- Parameter groups, weight-decay semantics, and schedule timing.
- Mixed-precision scaling and skipped updates.
- Distributed gradient reduction and effective batch size.
- Graph detachment, zeroing lifecycle, and in-place mutation.

## Failure modes and decision rules

- Optimize the wrong objective: fix formulation before tuning the optimizer.
- Leak validation data into selection: rebuild the experimental boundary.
- Compare optimizers with different schedules or effective batch sizes: normalize the protocol.
- Clip gradients without measuring frequency: clipping can hide instability.
- Treat training loss as product quality: add task and system evals.
- Change several knobs at once: preserve an interpretable baseline.

Decision rule: first make a tiny batch overfit, then verify gradients and loss scale, then expand data and measure validation behavior. Only after the mechanism is healthy should you tune optimizer families.

## Production lens

Record objective components, learning rate, gradient norm, parameter/update norm ratio, throughput, skipped steps, non-finite counts, seed, data revision, and optimizer state. Compare runs at equal examples or tokens processed, not only equal wall time. Checkpoints must include the optimizer and scheduler if a resumed trajectory is expected to match the original one.

## Exercises

1. Run the linear-regression loop with learning rates `0.005`, `0.05`, `0.5`, and `1.0`.
2. Derive the gradients for one example by hand.
3. Add L2 regularization `λw²` and derive its contribution.
4. Compare analytical and centered-difference gradients for `w` and `b`.
5. Log loss, parameter norm, gradient norm, and validation error; diagnose four distinct failure patterns.

**Connects to:** [[ai/computation-and-autodiff/backpropagation-from-first-principles|Backpropagation from First Principles]] · [[ai/deep-learning/optimizers|Optimizers]] · [[ai/foundations/generalization-and-overfitting|Generalization and Overfitting]]

## Sources

- [Mathematics for Machine Learning, Chapter 7](https://mml-book.github.io/) — continuous optimization foundations for ML.
- [Convex Optimization](https://web.stanford.edu/~boyd/cvxbook/) — canonical treatment of convexity, gradients, conditioning, and duality.
- [An Overview of Gradient Descent Optimization Algorithms](https://arxiv.org/abs/1609.04747) — concise map of SGD, momentum, and adaptive methods.
- [Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980) — original Adam algorithm and assumptions.
