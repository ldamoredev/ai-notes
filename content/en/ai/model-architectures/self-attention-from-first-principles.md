---
title: "Self-attention from first principles"
description: Derive causal scaled dot-product attention from shapes and numbers, implement it without a tensor library, and understand its systems costs.
tags: [attention, transformers, qkv, causal-masking]
order: 1
updated: 2026-07-19
kind: concept
level: foundational
status: flagship
prerequisites: [vectors-matrices-and-tensors, probability-likelihood-and-uncertainty]
last_verified: 2026-07-19
---
# Self-attention from first principles

Self-attention is a differentiable content-addressed read. Every token creates a
query describing what it seeks, a key describing how it can be found, and a value
containing the information it can contribute. Similarity scores become a probability
distribution, and that distribution mixes the values.

The mechanism is simple enough to calculate by hand. Its power and its costs emerge
from tensor shapes, masking, normalization, and repeated composition.

## The operation and its shapes

Let the token representation matrix be \(X\in\mathbb{R}^{T\times d_{model}}\), where
\(T\) is sequence length. Learned projection matrices produce:

\[
Q=XW_Q,\quad K=XW_K,\quad V=XW_V,
\]

with \(Q,K\in\mathbb{R}^{T\times d_k}\) and
\(V\in\mathbb{R}^{T\times d_v}\). Scaled dot-product attention is:

\[
\operatorname{Attention}(Q,K,V)=
\operatorname{softmax}\left(\frac{QK^T}{\sqrt{d_k}}+M\right)V.
\]

The shape ledger is the shortest reliable explanation:

| Expression | Shape | Meaning |
|---|---|---|
| `Q @ K.T` | `[T, T]` | one score for each query-key pair |
| `scores + M` | `[T, T]` | forbidden positions become unreachable |
| `softmax(..., axis=-1)` | `[T, T]` | every query row sums to one |
| `weights @ V` | `[T, d_v]` | one weighted value vector per query |

Attention does not retrieve a single record. It performs a soft read over all
eligible positions.

## A numerical example

Use two-dimensional queries, keys, and values:

\[
Q=K=\begin{bmatrix}1&0\\0&1\\1&1\end{bmatrix},\qquad
V=\begin{bmatrix}1&0\\0&2\\3&1\end{bmatrix}.
\]

For the final token, the unscaled scores against the three keys are `[1, 1, 2]`.
After division by \(\sqrt{2}\), stable softmax produces approximately
`[0.248, 0.248, 0.503]`. Its output is therefore:

\[
0.248[1,0]+0.248[0,2]+0.503[3,1]\approx[1.758,0.999].
\]

That vector is a content-dependent mixture. Changing a query changes the routing
without changing the network topology.

## Why divide by the square root of the key width?

If query and key coordinates are independent with unit variance, their dot product
has variance proportional to \(d_k\). Wider keys create larger logits, which push
softmax into saturated, low-gradient regions. Dividing by \(\sqrt{d_k}\) keeps the
score scale roughly stable as width changes.

This factor is not decorative. Remove it from a wide head and inspect the entropy of
the attention rows and the gradient magnitudes.

## Causal masking

An autoregressive decoder must not use future tokens to predict the present token.
The causal mask is:

\[
M_{ij}=\begin{cases}
0 & j\le i\\
-\infty & j>i.
\end{cases}
\]

Adding the mask before softmax makes forbidden probabilities exactly zero in exact
arithmetic. Masking after softmax is wrong unless the remaining entries are
renormalized, and even then it wastes probability mass and can complicate kernels.

Padding masks answer a different question: which batch positions are artificial?
Production implementations combine causal, padding, segment, and sometimes local
window constraints without confusing their semantics.

## Executable artifact: dependency-free causal attention

Run the complete implementation:

```bash
python3 labs/glassbox/v4_attention.py
python3 -m unittest labs.glassbox.test_glassbox -v
```

Its core is ordinary loops, which makes every index visible:

```python
def causal_attention(q, k, v):
    width = len(q[0])
    outputs, rows = [], []
    for i, query in enumerate(q):
        scores = []
        for j, key in enumerate(k):
            score = dot(query, key) / math.sqrt(width)
            scores.append(score if j <= i else float("-inf"))
        weights = stable_softmax(scores)
        output = [
            sum(weights[j] * v[j][col] for j in range(len(v)))
            for col in range(len(v[0]))
        ]
        rows.append(weights)
        outputs.append(output)
    return outputs, rows
```

The tests verify that every row sums to one and every future position has zero
weight. Replace the causal comparison with `j < i` to see why a token sometimes
needs access to its own representation.

## Multi-head attention

A transformer normally divides the representation into \(H\) heads:

\[
\operatorname{MHA}(X)=
\operatorname{Concat}(head_1,\ldots,head_H)W_O.
\]

Each head owns different projection parameters and can learn a different similarity
space. Heads do not come with predefined linguistic roles, and observed patterns are
not proof of causal importance. Head dimension, rotary or absolute position
encoding, grouped-query attention, and the output projection all affect behavior.

## Where position enters

Plain attention is permutation equivariant: reorder the input rows and the output
reorders the same way. Sequence models inject order through positional embeddings or
position-dependent transformations such as rotary position embeddings (RoPE).
The causal mask provides directionality but does not by itself encode distance.

## What optimized kernels change

The mathematical result can be computed without storing the full \(T\times T\)
attention matrix. FlashAttention tiles queries, keys, and values through fast on-chip
memory and performs an online softmax. It reduces memory traffic and changes the
practical bottleneck while preserving exact attention up to floating-point order.

This distinction matters: an optimized kernel improves execution, but it does not
turn global attention's pairwise work into a linear-time algorithm.

## Inference and the KV cache

During autoregressive generation, earlier keys and values do not change. Cache them
instead of recomputing them at every token. For each layer, KV-cache memory grows
approximately with:

\[
2\times L\times T\times H_{kv}\times d_{head}\times bytes.
\]

Grouped-query and multi-query attention reduce \(H_{kv}\), trading some modeling
capacity for lower memory bandwidth and larger serving batches. Prefix sharing,
paged caches, quantized caches, and eviction policies are systems-level extensions
of the same shape equation.

## Failure modes and limits

- **Quadratic training footprint.** Global pairwise scores grow as \(T^2\), although
  optimized kernels can avoid materializing the full matrix.
- **Softmax overflow.** Subtract the maximum finite logit before exponentiation.
- **All-masked rows.** Softmax over only negative infinity is undefined; validate
  masks or define an explicit empty-row policy.
- **Mask leakage.** A one-position error lets evaluation targets enter their own
  context and produces deceptively good metrics.
- **Attention is not explanation.** A large weight is an internal routing value, not
  automatically a faithful account of model reasoning.
- **Long context is not perfect recall.** Position effects, distractors, training
  distribution, and retrieval quality can dominate the nominal context window.

## Production lens

Record prompt length, generated length, prefill latency, per-token decode latency,
KV-cache bytes, cache hit/eviction rates, and attention-kernel selection. Throughput
should be stratified by sequence length; an average hides nonlinear cost.

Test masks with tiny deterministic matrices before benchmarking optimized kernels.
At serving time, monitor time-to-first-token separately from inter-token latency:
prefill is highly parallel and compute-heavy, while decode is commonly constrained
by memory bandwidth and cache movement.

## Exercises

1. Reproduce the final-token numerical example by hand and with `v4_attention.py`.
2. Remove the \(\sqrt{d_k}\) scale, multiply every vector width by 16, and compare
   row entropy.
3. Add a padding mask and a test where an entire padded column must receive zero
   probability.
4. Estimate KV-cache memory for 32 layers, 32 KV heads, head width 128, context
   8192, and two-byte elements. Repeat for 8 KV heads.

**Connects to:** [[ai/mathematics-for-ai/vectors-matrices-and-tensors|vectors, matrices, and tensors]] · [[ai/mathematics-for-ai/probability-likelihood-and-uncertainty|probability and uncertainty]] · [[ai/computation-and-autodiff/backpropagation-from-first-principles|backpropagation]] · [[ai/llms/from-prompt-to-generated-token|from prompt to generated token]] · [[ai/inference-and-optimization/kv-cache-and-memory|KV cache and memory]]

## Sources

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — the transformer architecture and scaled dot-product attention definition.
- [FlashAttention](https://arxiv.org/abs/2205.14135) — an IO-aware exact-attention algorithm and memory analysis.
- [RoFormer](https://arxiv.org/abs/2104.09864) — rotary position embeddings and their relative-position properties.
- [Fast Transformer Decoding](https://arxiv.org/abs/1911.02150) — multi-query attention as an inference-memory trade-off.
- [Hugging Face KV cache strategies](https://huggingface.co/docs/transformers/kv_cache) — concrete cache implementations, offloading, quantization, and sliding windows.
