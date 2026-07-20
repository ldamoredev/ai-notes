---
title: "Loss functions in deep learning"
description: The loss is the number a network is built to minimize, so it defines the task; cross-entropy's clean combined gradient with softmax is why it dominates classification.
tags: [deep-learning, loss, cross-entropy, contrastive]
order: 10
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/computation-and-autodiff/backpropagation-from-first-principles, ai/mathematics-for-ai/information-theory-entropy-and-divergence]
last_verified: 2026-07-20
translation: stale
---
# Loss functions in deep learning

**Mental model:** the loss is the single number a network is built to minimize, so it
**defines the task**. Same architecture, different loss → a classifier, a regressor,
or an embedding model. The loss and the output layer are a matched pair; choosing them
well matters more than most architecture tweaks.

## Mechanism: why cross-entropy's gradient is so clean

For classification, cross-entropy compares a predicted softmax distribution
\(p\) against a one-hot true label \(y\):

\[
L = -\sum_c y_c \log p_c = -\log p_{\text{true class}}.
\]

The reason this pairs so well with softmax is what happens when you take the
gradient of \(L\) with respect to the pre-softmax logits \(z\) — the softmax
Jacobian and the log in the loss cancel exactly:

\[
\frac{\partial L}{\partial z_i} = p_i - y_i.
\]

The gradient is simply "predicted probability minus true probability" per class — no
vanishing term, regardless of how confident or wrong the prediction is. This is what
"clean gradient" means concretely, and it is the mechanism behind why cross-entropy
trains faster than alternatives that lack this cancellation.

## Worked example

Three-class logits \(z = [2.0, 1.0, 0.1]\), true class = index 1. Softmax gives
\(p \approx [0.659, 0.242, 0.099]\). Loss: \(L = -\log(0.242) \approx 1.417\).
Combined gradient: \(p - y = [0.659,\, -0.758,\, 0.099]\) — the correct class's logit
gets pushed up (negative gradient), the wrong classes get pushed down.

Now the case that matters most: the model is **confidently wrong**. Logits
\(z = [\ln 98,\, 0,\, 0]\) give \(p = [0.98, 0.01, 0.01]\), still with true class = 1.
Loss: \(L = -\log(0.01) \approx 4.605\) — much larger, correctly signaling a bad
mistake. Gradient: \(p - y = [0.98,\, -0.99,\, 0.01]\) — still large and pointed the
right direction, with **no vanishing**. A loss built directly on probabilities (e.g.
MSE on softmax output) would instead multiply this error by the softmax Jacobian's
diagonal term \(p_i(1-p_i)\), which is \(0.98 \times 0.02 = 0.0196\) here — tiny,
precisely because the model is saturated near 0 or 1. That shrinking term is exactly
the vanishing-gradient problem cross-entropy's cancellation avoids.

## Executable artifact

Run with `python3`; expected output is the two `(loss, grad)` pairs above,
`1.417 [0.659, -0.758, 0.099]` and `4.605 [0.98, -0.99, 0.01]`:

```python
import math

def softmax(z):
    m = max(z)
    exps = [math.exp(x - m) for x in z]
    s = sum(exps)
    return [e / s for e in exps]

def cross_entropy_and_grad(z, true_idx):
    p = softmax(z)
    loss = -math.log(p[true_idx])
    grad = [pi - (1.0 if i == true_idx else 0.0) for i, pi in enumerate(p)]
    return loss, grad

for z, true_idx in [([2.0, 1.0, 0.1], 1), ([math.log(98), 0.0, 0.0], 1)]:
    loss, grad = cross_entropy_and_grad(z, true_idx)
    print(round(loss, 3), [round(g, 3) for g in grad])
```

## The common losses

| Loss | Task | Pairs with output |
|---|---|---|
| **MSE / L1** | regression | linear output |
| **Cross-entropy** | classification | softmax (multi-class) or sigmoid (binary) |
| **Contrastive / triplet / InfoNCE** | learning [[ai/deep-learning/embeddings-and-latent-spaces|embeddings]] | normalized vectors |

## Contrastive losses: learning a space, not a label

When the goal is a useful *representation* rather than a class, contrastive losses
(InfoNCE and relatives) pull [[ai/deep-learning/embeddings-and-latent-spaces|cosine-similar]]
items together and push dissimilar ones apart in vector space, typically by treating
one positive pair against many negative pairs in a batch as a classification problem
over "which of these is the true match." This is how text/image embedding models and
CLIP are trained, and why [[ai/rag-and-retrieval/index|semantic search]] works.

## What framework losses hide

`nn.CrossEntropyLoss` in PyTorch silently applies `log_softmax` internally — passing
already-softmaxed probabilities into it double-applies the nonlinearity and silently
produces a wrong, still-differentiable loss with no error raised. The clean `p - y`
gradient only exists because the framework fuses softmax and cross-entropy into one
numerically stable operation; splitting them apart manually reintroduces both the
Jacobian-shrinkage problem above and float-precision instability from computing
`log(softmax(z))` as two separate steps.

## Failure modes and a decision rule

- **Loss/output mismatch.** Softmax output with MSE loss, or linear output with
  cross-entropy, trains slowly or not at all — always match the pair from the table
  above.
- **Class imbalance swamping the gradient.** With extreme imbalance, cross-entropy's
  aggregate gradient is dominated by the majority class; focal loss down-weights
  easy, well-classified examples specifically to counter this.
- **The proxy-loss gap.** The loss you can differentiate is a *proxy* for what you
  actually care about — you cannot backprop through "user satisfaction" or
  "accuracy@threshold" directly. A falling loss is necessary, not sufficient; always
  check the real [[ai/foundations/evaluation-metrics|metric]] too, and note that a
  well-calibrated loss value does not guarantee well-calibrated *probabilities* — see
  the calibration source below.
- **Double-applying softmax**, shown above, silently trains a wrong objective.

**Decision rule:** use the framework's fused loss (`CrossEntropyLoss`,
`BCEWithLogitsLoss`) rather than composing softmax/sigmoid and a separate loss by
hand, unless you have a specific numerical reason not to. Reach for a contrastive loss
only when the deliverable is a reusable embedding space, not a fixed label set.

## Production lens

Track the loss curve alongside the real evaluation metric, not instead of it — they
can diverge, especially under distribution shift or when the eval metric is
threshold-based while the loss is continuous. For deployed classifiers whose output
probability is shown to a user or used in a downstream decision, evaluate calibration
separately from loss and accuracy; a model can have low loss and still be
systematically overconfident.

## Exercises

1. Recompute loss and gradient for `z=[0.5, 0.5, 0.5]` (a maximally uncertain
   prediction) with true class 0, and compare the gradient magnitude to the two cases
   above.
2. Derive `∂L/∂z_i = p_i - y_i` from the chain rule, using
   `∂p_i/∂z_j = p_i(δ_ij - p_j)` (the softmax Jacobian) and `L = -log(p_true)`.
3. Implement `nn.functional.mse_loss` applied to softmax output for the
   confidently-wrong example above and confirm its gradient magnitude is far smaller
   than cross-entropy's `0.98`.

**Connects to:** [[ai/mathematics-for-ai/information-theory-entropy-and-divergence|cross-entropy]] · [[ai/foundations/how-learning-works|objective vs metric]] · [[ai/deep-learning/embeddings-and-latent-spaces|contrastive learning]] · [[ai/computation-and-autodiff/backpropagation-from-first-principles|backpropagation]]

## Sources

- [Deep Learning, Chapter 6](https://www.deeplearningbook.org/contents/mlp.html) — output units and cost functions, including the softmax/cross-entropy pairing.
- [Focal Loss for Dense Object Detection](https://arxiv.org/abs/1708.02002) — reweighting cross-entropy to counter extreme class imbalance.
- [Representation Learning with Contrastive Predictive Coding](https://arxiv.org/abs/1807.03748) — the InfoNCE contrastive objective used to train embedding spaces.
- [On Calibration of Modern Neural Networks](https://arxiv.org/abs/1706.04599) — why low loss and high accuracy do not guarantee well-calibrated probabilities.
