---
title: Vectors, Matrices, and Tensors
description: Shapes, dot products, matrix multiplication, linear transformations, batching, and the array semantics behind AI computation.
tags: [linear-algebra, vectors, matrices, tensors, shapes]
order: 1
updated: 2026-07-19
kind: derivation
level: beginner
status: current
prerequisites: []
last_verified: 2026-07-19
---
# Vectors, Matrices, and Tensors

A tensor is a multidimensional array plus a contract about what each axis means. AI systems use tensors because batches of examples, token sequences, image grids, channels, features, parameters, and logits can all be transformed by regular array operations that hardware executes in parallel.

The mental model is not “a tensor is a box of numbers.” It is **numbers + shape + axis semantics + dtype + device**. A multiplication can be dimensionally valid and still be conceptually wrong if you contract the wrong axes.

## Scalars, vectors, matrices, and higher-order tensors

| Object | Example shape | Possible meaning |
|---|---:|---|
| Scalar | `[]` | one loss, learning rate, or probability |
| Vector | `[D]` | one example with `D` features |
| Matrix | `[N, D]` | `N` examples or tokens with `D` features each |
| Rank-3 tensor | `[B, N, D]` | batch, sequence, embedding |
| Rank-4 tensor | `[B, C, H, W]` | batch, image channels, height, width |

Rank is the number of axes. Shape is the ordered size of those axes. A two-dimensional matrix with shape `[3, 2]` contains six scalar entries, but its two axes require domain meaning before an operation can be interpreted.

Do not use “dimension” without context. It may mean rank, the size of one axis, the feature count `D`, or the dimension of a vector space.

## Vectors as coordinates and features

Write a vector `x ∈ R^D` as an ordered list:

```text
x = [x₁, x₂, …, x_D]
```

The same numbers can encode a position, measured features, token activations, or parameters. Vector algebra does not know the semantics. The model designer supplies them.

For `x = [2, -1]`, the Euclidean norm is:

```text
||x||₂ = sqrt(2² + (-1)²) = sqrt(5)
```

Norms measure size under a chosen geometry. Normalizing `x / ||x||₂` preserves direction and discards magnitude. That is useful for cosine similarity but destructive when magnitude carries information.

## Dot product: weighted sum and similarity primitive

For `x, w ∈ R^D`, the dot product contracts the feature axis:

```text
w · x = Σᵢ wᵢ xᵢ
```

With `w = [1, 3]` and `x = [2, -1]`:

```text
w · x = 1×2 + 3×(-1) = -1
```

Three useful readings coexist:

- A weighted sum: each input feature contributes `wᵢxᵢ`.
- A projection: `w · x = ||w|| ||x|| cos(θ)` measures alignment.
- A linear model score: `z = w · x + b` becomes a logit before a link function.

Attention uses dot products between query and key vectors. Embedding retrieval often ranks normalized vectors by dot product, which then equals cosine similarity. The operation is the same; normalization and semantics differ.

## Matrix-vector multiplication: several weighted sums

Let `W ∈ R^(M×D)` and `x ∈ R^D`. Then:

```text
y = Wx, where y ∈ R^M
yⱼ = Σᵢ Wⱼᵢ xᵢ
```

Every row of `W` is a different weighted sum of the same input. For:

```text
W = [[ 1, 3],
     [-2, 0.5],
     [ 0, 4]]
x = [2, -1]
```

the output is:

```text
Wx = [-1, -4.5, -4]
```

Shape reasoning predicts `[3, 2] @ [2] → [3]`. The contracted inner size `2` must match. The remaining axes form the output.

## Matrix multiplication: compose transformations

For `A ∈ R^(M×K)` and `B ∈ R^(K×N)`:

```text
C = AB ∈ R^(M×N)
Cᵢⱼ = Σₖ Aᵢₖ Bₖⱼ
```

The `K` axis is contracted. A useful shape proof is:

```text
[M, K] @ [K, N] → [M, N]
```

Matrix multiplication is not elementwise multiplication. It composes linear transformations: applying `B` and then `A` gives `A(Bx) = (AB)x`. Order matters; usually `AB ≠ BA`.

In a dense neural layer with a batch `X ∈ R^(B×D)` and weights `W ∈ R^(D×M)`:

```text
Y = XW + b
[B, D] @ [D, M] + [M] → [B, M]
```

The bias broadcasts across the batch axis. Broadcasting is a shape rule, not free copying: the implementation behaves as though the same `[M]` vector were used for every row.

## Linear transformations and why neural networks need nonlinearity

A linear transformation preserves addition and scalar multiplication:

```text
T(x + y) = T(x) + T(y)
T(cx) = cT(x)
```

Matrix multiplication implements every finite-dimensional linear map after bases are chosen. An affine map adds a bias: `f(x) = Wx + b`.

Stacking affine maps without nonlinear activation collapses into one affine map:

```text
W₂(W₁x + b₁) + b₂ = (W₂W₁)x + (W₂b₁ + b₂)
```

Depth alone does not create nonlinear decision boundaries. Activations, attention softmax, normalization, gating, and other nonlinear operations change the function class.

## Batch and sequence dimensions

For language models, an activation often has shape `[B, N, D]`:

- `B`: independent sequences processed together.
- `N`: positions or tokens in each sequence.
- `D`: feature or embedding width at each position.

A projection `W_Q ∈ R^(D×d_k)` applies at every batch and token position:

```text
Q = XW_Q
[B, N, D] @ [D, d_k] → [B, N, d_k]
```

The matrix multiplication contracts only `D`. `B` and `N` are leading axes carried through. Multi-head attention then reshapes a feature axis into `[H, d_head]`; reshaping is valid only if `H × d_head = D` and the intended storage/order is preserved.

## A minimal executable artifact

Glassbox v0 implements dot product, matrix-vector multiplication, stable softmax, entropy, cross-entropy, and seeded sampling without NumPy:

```bash
python3 -m labs.glassbox.v0_math
python3 -m unittest labs.glassbox.test_glassbox.MathTests -v
```

Expected shape trace:

```text
shape: matrix=[3,2], vector=[2], logits=[3]
logits: [-1.0, -4.5, -4.0]
sum(p): 1.000000
```

The implementation rejects shape mismatch instead of silently truncating. That check is part of correctness.

## What frameworks hide

- Strides and storage: a transpose may create a view whose logical order differs from memory order.
- Broadcasting: compact syntax can accidentally combine axes that happen to be size-compatible.
- Kernel selection: the same `matmul` call may dispatch to different CPU/GPU kernels and precisions.
- Copies and transfers: changing dtype, device, or contiguity can move data and dominate latency.
- Accumulation precision: products and sums may use different formats or reduction orders.

## Failure modes and limits

- A valid shape is not valid semantics. Swapping batch and sequence axes can run and still corrupt learning.
- Cosine similarity ignores magnitude and does not prove semantic equivalence.
- High-dimensional distances can concentrate; retrieval quality must be evaluated on the task.
- Matrix notation hides memory bandwidth, kernel launch, and layout cost.
- Floating-point matrix multiplication is not algebraically exact or perfectly associative.

Decision rule: write axis names beside every important shape until you can derive the output without running code. Use named tensor conventions or assertions at system boundaries.

## Production lens

Log semantic shapes at system boundaries, not every tensor in a hot loop. Track dtype, device, batch/sequence axes, peak memory, and the operation that first produces a non-finite value. Shape assertions belong at ingestion, model interfaces, cache boundaries, and serialization points; a valid but swapped axis often survives much longer than a dimension error.

## Exercises

1. Compute `[[1, 2], [3, 4]] @ [5, 6]` by hand and verify with `matvec`.
2. Show numerically that `(AB)x = A(Bx)` for compatible small matrices.
3. Construct two different tensors with shape `[2, 3]` whose axes mean different things; explain why shape checking alone fails.
4. Remove the shape guard in Glassbox v0 and observe how `zip` silently truncates mismatched vectors.
5. Derive the shapes of `QKᵀ` for `Q, K ∈ R^(B×H×N×d_head)`.

**Connects to:** [[ai/model-architectures/self-attention-from-first-principles|Self-Attention from First Principles]] · [[ai/deep-learning/embeddings-and-latent-spaces|Embeddings and Latent Spaces]] · [[ai/computation-and-autodiff/backpropagation-from-first-principles|Backpropagation from First Principles]]

## Sources

- [Mathematics for Machine Learning, Chapter 2](https://mml-book.github.io/) — linear algebra tied directly to ML applications and notation.
- [Dive into Deep Learning — Data Manipulation](https://d2l.ai/chapter_preliminaries/ndarray.html) — executable tensor creation, indexing, and operations.
- [PyTorch Broadcasting Semantics](https://pytorch.org/docs/stable/notes/broadcasting.html) — the exact rules production tensor code follows.
- [BLAS specification and references](https://www.netlib.org/blas/) — the foundational interface behind dense linear algebra kernels.
