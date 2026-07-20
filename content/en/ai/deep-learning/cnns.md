---
title: "CNNs: convolution & spatial structure"
description: A convolution is a small weight-shared filter slid over an image; that single mechanism produces locality, translation invariance, and a parameter count orders of magnitude below a fully connected layer.
tags: [deep-learning, cnn, convolution, vision]
order: 6
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/computation-and-autodiff/backpropagation-from-first-principles]
last_verified: 2026-07-20
translation: stale
---
# CNNs: convolution & spatial structure

**Mental model:** a CNN's [[ai/foundations/inductive-bias-and-no-free-lunch|inductive
bias]] matches images directly: nearby pixels relate, and a pattern means the same
thing wherever it appears. Baking that into the architecture — instead of hoping a
fully connected layer discovers it from data — is why CNNs dominated vision for a
decade with a fraction of the parameters.

## Mechanism: convolution as a slid dot product

A 2D convolution (implemented as cross-correlation) slides a small filter
\(K \in \mathbb{R}^{k \times k}\) over an input \(X \in \mathbb{R}^{h \times w}\).
Each output position is a dot product between the filter and the patch it currently
covers:

\[
Y_{i,j} = \sum_{di=0}^{k-1}\sum_{dj=0}^{k-1} X_{i+di,\,j+dj}\; K_{di,dj}.
\]

With stride \(s=1\) and no padding, the output size is \(O = (n - k) + 1\) per
dimension. The **same** \(K\) is reused at every position (weight sharing) — this is
what makes the filter translation-invariant: it responds to a pattern the same way
regardless of where in the image that pattern sits.

## Worked example: convolution as edge detection

Take a 5×5 image with a vertical edge (bright on the left, dark on the right) and a
simple edge kernel:

\[
X = \begin{bmatrix}10&10&10&0&0\\10&10&10&0&0\\10&10&10&0&0\\10&10&10&0&0\\10&10&10&0&0\end{bmatrix},
\qquad
K = \begin{bmatrix}1&0&-1\\1&0&-1\\1&0&-1\end{bmatrix}.
\]

Output size is \((5-3)+1 = 3\) per dimension. At the top-left patch (columns 0–2, all
value 10), the dot product is \(1{\cdot}10+0{\cdot}10-1{\cdot}10=0\) per row, summed
over 3 rows = **0** — a uniform region produces no response. At the next patch
(columns 1–3, values `10,10,0`), each row contributes \(1{\cdot}10+0{\cdot}10-1{\cdot}0=10\),
summed over 3 rows = **30** — the filter fires exactly where the edge crosses its
window. Because every image row is identical, all three output rows are the same:
`[0, 30, 30]`.

## Executable artifact

Run with `python3`; expected output is three identical rows, `[0.0, 30.0, 30.0]`:

```python
def conv2d(image, kernel):
    ih, iw = len(image), len(image[0])
    kh, kw = len(kernel), len(kernel[0])
    oh, ow = ih - kh + 1, iw - kw + 1
    out = [[0.0] * ow for _ in range(oh)]
    for i in range(oh):
        for j in range(ow):
            s = 0.0
            for di in range(kh):
                for dj in range(kw):
                    s += image[i + di][j + dj] * kernel[di][dj]
            out[i][j] = s
    return out

image = [[10, 10, 10, 0, 0] for _ in range(5)]
kernel = [[1, 0, -1], [1, 0, -1], [1, 0, -1]]

for row in conv2d(image, kernel):
    print(row)
```

## Why weight sharing crushes the parameter count

A fully connected layer mapping a flattened 32×32×3 image (3072 values) to 10 outputs
needs \(3072 \times 10 + 10 = 30{,}730\) parameters. A convolutional layer with 10
filters of size 5×5 over 3 input channels needs only
\(5 \times 5 \times 3 \times 10 + 10 = 760\) parameters — about **40x fewer** — while
still scanning the entire image, because the same 760 numbers are reused at every
spatial position instead of learning a separate weight per pixel per output.

## Mechanism: receptive field grows faster than filter size

Stacking small filters grows the receptive field (the input region a deep neuron
depends on) recursively: \(RF_l = RF_{l-1} + (k_l - 1) \cdot \prod_{i<l} s_i\). Two
stacked 3×3 convolutions (stride 1) give \(RF = 3 + (3-1){\cdot}1 = 5\) — the same
receptive field as one 5×5 convolution — but with \(2 \times 3 \times 3 = 18\)
weights per channel pair instead of \(5\times5=25\), plus an extra nonlinearity
between them. This is the standard argument (VGG-style) for stacking small filters
instead of using one large one: same coverage, fewer parameters, more nonlinearity.

## Where CNNs stand now

CNNs still power most production vision (classification, detection, segmentation) and
are cheap and fast. Vision Transformers match or beat them at large data scale — but
ViTs need more data precisely because they *lack* the convolutional locality bias and
must learn it from examples instead of getting it for free from the architecture. The
trade is the same one everywhere: a stronger prior needs less data; a weaker prior
needs more.

## What framework layers hide

`nn.Conv2d(in_channels, out_channels, kernel_size)` hides that the operation performed
is cross-correlation, not the sign-flipped convolution from signal processing — the
distinction is irrelevant once weights are learned, but it matters if you ever port a
hand-designed kernel from a signal-processing reference. It also hides the actual
receptive field of a deep neuron unless you compute it layer by layer with the formula
above; a debugger showing activation maps will not tell you that on its own.

## Failure modes and a decision rule

- **Wrong domain.** CNNs assume grid-structured, locally correlated data. Forcing them
  onto tabular data with no spatial structure wastes the bias entirely —
  [[ai/machine-learning/decision-trees-and-ensembles|trees]] usually win there.
- **Receptive field too small for the task.** A network whose deepest receptive field
  is smaller than the object or context it needs to recognize cannot succeed no matter
  how much data it sees; check the formula above before adding data or depth blindly.
- **Stride/padding off-by-one errors.** Mismatched output sizes between layers are a
  purely mechanical bug from the size formula above, not a learning problem — verify
  shapes before debugging training.

**Decision rule:** reach for a CNN (or a hybrid) whenever the input is naturally
grid-structured and local context dominates; reach for attention when long-range,
data-dependent interactions matter more than locality and enough data is available to
learn that structure from scratch.

## Exercises

1. Change the kernel to `[[1,1,1],[0,0,0],[-1,-1,-1]]` (a horizontal edge detector) and
   predict the output before running it on the same image — should it detect anything
   given the image only has a vertical edge?
2. Compute the receptive field of three stacked 3×3 convolutions (stride 1) using the
   recursive formula, and compare its parameter count to a single convolution with the
   equivalent receptive field.
3. For a 224×224×3 input and a first layer of 64 filters at 7×7 (stride 2, ResNet's
   stem), compute the output spatial size and the parameter count.

**Connects to:** [[ai/foundations/inductive-bias-and-no-free-lunch|inductive bias]] · [[ai/model-architectures/self-attention-from-first-principles|attention vs convolution]] · [[ai/foundations/features-and-dimensionality|feature hierarchy]] · [[ai/deep-learning/initialization-and-normalization|initialization & normalization]]

## Sources

- [Deep Learning, Chapter 9](https://www.deeplearningbook.org/contents/convnets.html) — convolution, pooling, and the CNN training mechanism in full.
- [Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385) — residual CNNs and the stem/stage design used in most production vision backbones.
- [An Image is Worth 16x16 Words](https://arxiv.org/abs/2010.11929) — the Vision Transformer and the data-scale tradeoff against convolutional locality bias.
- [Stanford CS231n](https://cs231n.github.io/) — receptive field arithmetic and practical CNN training diagnostics.
