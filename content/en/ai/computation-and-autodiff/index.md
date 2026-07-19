---
title: Computation and Autodiff
description: How arrays, compute graphs, derivatives, memory, precision, and parallel hardware turn mathematical models into executable learning systems.
tags: [computation, tensors, autodiff, systems]
order: 0
updated: 2026-07-19
status: current
level: intermediate
---
# Computation and Autodiff

A mathematical function does not train itself. It must be represented as array operations, executed in a defined order, differentiated, scheduled on hardware, and observed under finite precision.

## Mental model

The forward pass creates values and dependencies. Reverse-mode automatic differentiation traverses those dependencies backward, multiplying local derivatives and accumulating every path into shared parameters. Tensor libraries add shape rules, vectorized kernels, device placement, memory management, and synchronization around that mechanism.

## Current foundation notes

- [[ai/computation-and-autodiff/backpropagation-from-first-principles|Backpropagation from First Principles]]

## Candidate note roadmap

- `arrays-tensors-shapes-and-strides` — storage, views, broadcasting, strides, and contiguity.
- `vectorization-and-batched-computation` — replace scalar loops with array programs and reason about batch axes.
- `compute-graphs-and-execution-models` — eager, traced, compiled, static, and dynamic execution.
- `reverse-mode-autodiff-engine` — nodes, local derivatives, topology, accumulation, and lifecycle.
- `forward-mode-jacobians-and-jvps` — when forward mode is the cheaper derivative program.
- `floating-point-and-mixed-precision` — formats, rounding, loss scaling, and numerical failure.
- `randomness-seeds-and-reproducibility` — RNG state, nondeterministic kernels, and environment capture.
- `gpus-kernels-and-parallel-computation` — threads, warps, memory hierarchy, launch overhead, and arithmetic intensity.

## What frameworks hide

Autograd frameworks correctly automate derivative bookkeeping, but they cannot decide whether an objective is meaningful, a tensor shape is semantically correct, an in-place mutation invalidates a graph, or a nondeterministic kernel undermines an experiment. This branch makes those boundaries explicit.

**Connects to:** [[ai/mathematics-for-ai/index|Mathematics for AI]] · [[ai/deep-learning/index|Deep Learning]] · [[ai/inference-and-optimization/index|Inference Systems]]

## Core sources

- [PyTorch Autograd mechanics](https://pytorch.org/docs/stable/notes/autograd.html) — precise behavior of the production reverse-mode engine.
- [JAX automatic differentiation](https://docs.jax.dev/en/latest/automatic-differentiation.html) — transformations, Jacobian-vector products, and composable autodiff.
- [micrograd](https://github.com/karpathy/micrograd) — compact reference implementation to study, not copy blindly.
- [What Every Computer Scientist Should Know About Floating-Point Arithmetic](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html) — foundational analysis of finite-precision behavior.
