---
title: "RNNs & their limits"
description: Recurrent nets processed sequences one step at a time — until vanishing gradients and an inability to parallelize made attention win. Worth understanding to see why transformers exist.
tags: [deep-learning, rnn, lstm, sequences]
order: 7
updated: 2026-06-07
---
# RNNs & their limits

Before transformers, recurrent neural networks were how you modeled sequences. They
mostly lost — but understanding *why* is the cleanest way to understand why
[[ai/model-architectures/self-attention-from-first-principles|attention]] and [[ai/llms/index|transformers]]
took over.

## How an RNN works

An RNN reads a sequence one element at a time, maintaining a **hidden state** that
acts as memory: at each step it combines the new input with the previous state to
produce a new state. In principle the state carries information from the whole past
into the present.

## Limit 1: vanishing gradients over long sequences

Backpropagating through many time steps multiplies many small numbers, so the
gradient [[ai/computation-and-autodiff/backpropagation-from-first-principles|vanishes]] and the network
struggles to connect distant events ("the topic mentioned 200 words ago"). **LSTMs**
and **GRUs** added gating to carry information further, which helped a lot — but
long-range dependencies stayed hard.

## Limit 2: no parallelism

This was the fatal one. Because step *t* needs the state from step *t−1*, an RNN must
process a sequence **sequentially** — you can't compute all positions at once. On
modern GPUs built for massive parallel [[ai/mathematics-for-ai/vectors-matrices-and-tensors|matrix
math]], that's a death sentence for scale.

## Why attention won

[[ai/model-architectures/self-attention-from-first-principles|Attention]] fixes both at once:

- Any position can look **directly** at any other in one step — no long chain to
  vanish through, so long-range dependencies are easy.
- All positions are computed **in parallel** — perfect for GPUs, which unlocked
  training on internet-scale data.

> "Attention is all you need" wasn't only about quality — removing recurrence is what
> made models *scalable*, and scale is what produced [[ai/llms/index|LLMs]].

RNNs still appear in tiny, streaming, or low-latency settings, and the
efficiency-vs-attention question lives on in newer state-space models (e.g. Mamba).

**Connects to:** [[ai/model-architectures/self-attention-from-first-principles|attention]] ·
[[ai/computation-and-autodiff/backpropagation-from-first-principles|vanishing gradients]] ·
[[ai/llms/index|why transformers]]
