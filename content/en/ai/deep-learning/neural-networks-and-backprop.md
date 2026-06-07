---
title: "Neural networks & backpropagation"
description: A network is a differentiable compute graph; backprop is just the chain rule run backwards through it. Get this and the rest is detail.
tags: [deep-learning, backpropagation, neural-networks, autograd]
order: 1
updated: 2026-06-07
---
# Neural networks & backpropagation

A neural network is a big differentiable function built from small steps. Training
it means computing how a tiny change in each parameter would change the
[[ai/foundations/how-learning-works|loss]], then nudging every parameter
accordingly. That gradient computation is **backpropagation** — and it's nothing
more than the chain rule applied to a graph.

## Forward pass: a stack of simple steps

Each layer computes `z = W·x + b` (a [[ai/machine-learning/linear-and-logistic-regression|linear
model]]) followed by a nonlinear [[ai/deep-learning/activation-functions|activation]].
Stack them and you get a **compute graph** from input to a scalar loss. Without the
nonlinearities, stacking linear layers would collapse to a single linear layer —
the activations are what give depth its power.

## Backward pass: the chain rule, reversed

To get the gradient of the loss with respect to an early weight, the chain rule
multiplies the local derivatives along the path from that weight to the loss.
Backprop computes this efficiently by walking the graph **backwards once**, reusing
shared sub-results, so the cost is about the same as the forward pass.

> Each node only needs to know: its local derivative, and the gradient flowing in
> from above. Multiply them, pass the result down. That's the whole algorithm.

## Autograd: why you never do this by hand

Frameworks (PyTorch, JAX) record the forward operations as a graph and apply backprop
automatically — **automatic differentiation**. You define the forward computation;
the gradients come free. Karpathy's *micrograd* shows the entire idea in ~100 lines.

## Why gradients misbehave

The chain of multiplications is also the failure mode: many small factors → the
gradient **vanishes** (early layers stop learning); large factors → it **explodes**
(training diverges). Most of [[ai/deep-learning/initialization-and-normalization|init
and normalization]], better [[ai/deep-learning/activation-functions|activations]],
and residual connections exist to keep that gradient flowing.

**Connects to:** [[ai/foundations/gradient-descent-intuition|gradient descent]] ·
[[ai/deep-learning/activation-functions|activations]] ·
[[ai/deep-learning/optimizers|optimizers]]
