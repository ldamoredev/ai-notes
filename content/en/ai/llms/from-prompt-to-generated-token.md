---
title: "From prompt to generated token"
description: Trace one autoregressive step through tokenization, embeddings, transformer blocks, logits, probability shaping, sampling, and the KV cache.
tags: [llms, tokenization, logits, decoding, inference]
order: 2
updated: 2026-07-19
kind: system-walkthrough
level: foundational
status: flagship
prerequisites: [self-attention-from-first-principles, probability-likelihood-and-uncertainty]
last_verified: 2026-07-19
---
# From prompt to generated token

An LLM does not emit a sentence. Given token IDs, it computes one vector of scores
over its vocabulary, converts those scores into a selection rule, appends one token,
and repeats. Streaming prose is the visible result of this discrete autoregressive
loop.

The useful mental model is a trace: **text → token IDs → residual vectors → logits →
probabilities → selected ID → text**. Each arrow has its own invariants and failure
modes.

## The complete one-token path

For a prompt with \(T\) tokens, vocabulary size \(V\), model width \(d\), and
\(L\) transformer blocks:

| Stage | Representative shape | What changes |
|---|---|---|
| Tokenize | text → `[T]` | strings become integer IDs |
| Embed | `[T]` → `[T, d]` | IDs select learned vectors |
| Transformer blocks | `[T, d]` → `[T, d]` | context is mixed and transformed |
| Final norm/head | `[T, d]` → `[T, V]` | hidden states become vocabulary logits |
| Select final row | `[T, V]` → `[V]` | only the next-position scores matter |
| Shape distribution | `[V]` → `[V]` | penalties, temperature, top-k/top-p |
| Sample | `[V]` → scalar ID | a policy chooses one token |
| Decode and append | ID → text fragment | the loop gains one token |

Training evaluates many next-token positions in parallel. Autoregressive inference
must commit to one token before it knows the next input, so the generation loop is
sequential across output positions.

## 1. The tokenizer defines the model's alphabet

A tokenizer maps byte or Unicode sequences to IDs from a fixed vocabulary. Modern
tokenizers commonly operate on subword or byte-level units, not words. Spaces,
capitalization, normalization, and preceding characters can change the split.

Suppose a tiny vocabulary is:

```text
id:     0    1    2    3
token: " "  "a"  "b"  "c"
```

The prompt `ab` becomes `[1, 2]`. A production tokenizer also has special tokens,
chat-template delimiters, and a defined treatment for arbitrary bytes. The model
cannot consume a string that has not passed through exactly the tokenizer associated
with its weights.

Chat APIs add an earlier transformation: role/content messages are serialized by a
model-specific template. Count tokens after templating, not from the visible user
message alone.

## 2. Embeddings turn IDs into vectors

The embedding table is \(E\in\mathbb{R}^{V\times d}\). Token ID \(i\) selects row
\(E_i\). After positional information is added or applied, the residual stream is:

\[
X_0\in\mathbb{R}^{T\times d}.
\]

The model now manipulates continuous vectors. An embedding is learned jointly with
the model; its coordinates do not arrive with human labels.

## 3. Transformer blocks update the residual stream

A decoder block alternates attention and a feed-forward transformation, usually
with normalization and residual addition. A pre-normalization sketch is:

\[
X' = X + \operatorname{Attention}(\operatorname{Norm}(X)),
\]

\[
X_{next} = X' + \operatorname{MLP}(\operatorname{Norm}(X')).
\]

Causal masking prevents position \(t\) from accessing tokens after \(t\). Self-
attention routes information between positions; the MLP transforms each position's
features. Repeating the pair lets the final prompt position summarize information
needed to predict what follows.

The residual stream keeps shape `[T, d]` through all blocks. Heads and intermediate
MLP widths create temporary dimensions, but the skip connections require a common
model width.

## 4. The language-model head produces logits

After the final normalization, a projection maps the last hidden vector
\(h_T\in\mathbb{R}^d\) to vocabulary logits:

\[
z = W_{vocab}h_T+b, \qquad z\in\mathbb{R}^{V}.
\]

Some architectures tie \(W_{vocab}\) to the input embedding table. A logit is an
unnormalized compatibility score, not a probability. Adding the same constant to
every logit does not change softmax.

## 5. The decoding policy shapes the scores

Before sampling, a serving system can apply:

- Invalid-token masks and grammar or JSON-schema constraints.
- Repetition, presence, or frequency penalties.
- Temperature \(\tau\): \(z'_i=z_i/\tau\).
- Top-k filtering to retain only the largest `k` scores.
- Top-p filtering to retain the smallest sorted set with cumulative mass at least
  `p`.

Temperature below one sharpens the distribution; above one flattens it. Temperature
zero is normally implemented as greedy argmax, not literal division by zero.

## 6. Stable softmax makes probabilities

For the retained logits:

\[
p_i = \frac{\exp(z'_i-m)}{\sum_j\exp(z'_j-m)},
\qquad m=\max_j z'_j.
\]

Subtracting the maximum preserves the probabilities while avoiding overflow. Use
the log-sum-exp form when computing log probabilities. Low-precision kernels require
care with accumulation and masked values.

## 7. Selection commits the next input

Greedy decoding chooses `argmax(p)`. Sampling draws one ID from the categorical
distribution. Beam search retains multiple partial sequences and scores them, but
it is not the default solution for open-ended assistant text.

A random seed helps reproduce a local demonstration, but bit-for-bit production
determinism can still be affected by batching, kernel choice, floating-point order,
hardware, and server implementation.

The selected token ID is appended to the context. Its text fragment may be an
incomplete Unicode byte sequence; robust streamers buffer until decoded output is
valid rather than assuming one token equals one displayable character.

## Executable artifact: inspect every intermediate value

The Glassbox lab implements the whole discrete loop for a tiny bigram model:

```bash
python3 -m labs.glassbox.v4_token_trace
python3 -m unittest labs.glassbox.test_glassbox -v
```

The model is deliberately small enough to print its state:

```python
def generate_one(text: str, temperature: float, seed: int) -> dict[str, object]:
    token_ids = encode(text)
    logits = BIGRAM_LOGITS[token_ids[-1]]
    probabilities = stable_softmax(logits, temperature)
    selected_id = sample_categorical(probabilities, random.Random(seed))
    return {
        "token_ids": token_ids,
        "logits": logits,
        "probabilities": probabilities,
        "selected_id": selected_id,
        "selected_token": decode([selected_id]),
    }
```

For prompt `ab`, temperature `0.8`, and seed `7`, the trace selects `c`. Change one
input at a time and inspect which stages change. This model has no embeddings or
attention—the bigram row stands in for the neural network's logits—so it isolates
the tokenizer/score/probability/selection boundary.

## The KV cache changes execution, not semantics

Without caching, generating token \(T+1\) would recompute keys and values for tokens
`1..T` in every layer. Because those tensors are unchanged, a serving engine stores
them. The new query attends to cached keys and values, then one new key/value pair is
appended per layer.

The cache lowers repeated compute but consumes memory proportional to sequence
length, batch size, layers, KV heads, head width, and element bytes. It also turns
allocation, paging, prefix reuse, and eviction into core serving concerns.

## Stop conditions

Generation ends when one of these policies fires:

- An end-of-sequence token is selected.
- The configured maximum new-token count is reached.
- A stop-token or stop-string matcher accepts the suffix.
- A grammar has completed a valid object.
- The client cancels or a time/budget limit expires.

String stops can span token boundaries. Applying them only to individually decoded
tokens misses valid matches.

## Failure modes and diagnostic rules

- **Wrong chat template.** Capability appears degraded because the weight-specific
  role markers are absent or duplicated.
- **Tokenizer mismatch.** IDs no longer correspond to the embeddings learned during
  training; output becomes meaningless.
- **Off-by-one logits.** Training labels must align token `t+1` with the hidden state
  at `t`.
- **Unstable softmax.** Exponentiating raw large logits produces infinities or NaNs.
- **Filter-order ambiguity.** Penalties, temperature, top-k, and top-p need a defined,
  tested order because operations do not all commute.
- **False confidence from greedy decoding.** Deterministic output is not evidence of
  correctness or calibration.
- **Context overflow.** Truncation can remove system instructions or critical early
  evidence; log the actual post-template token sequence policy.
- **Cache corruption.** Reusing KV state across incompatible prompts, adapters, or
  positions produces plausible but wrong output.

## Production lens

Trace prompt-template version, tokenizer/model revision, input and output token
counts, decoding parameters, stop reason, and request seed where supported. Record
time-to-first-token separately from inter-token latency. Prefill cost scales with
prompt processing; decode cost repeats once per generated token and often becomes
memory-bandwidth bound.

For quality analysis, retain log probabilities only under a deliberate privacy and
storage policy. Compare requests using the same model revision and sampling config.
For cost analysis, distinguish cached input, uncached input, and generated tokens if
the provider bills them differently.

## Exercises

1. Run the Glassbox trace for seeds `0..9`; tabulate selected IDs and compare their
   frequency with the printed probabilities.
2. Add greedy decoding and top-k filtering to the lab, with tests for `k=1` and
   `k=V`.
3. Write a stop-string matcher that handles a match spanning two decoded tokens.
4. For vocabulary `V=50,000` and model width `d=4096`, calculate the parameter count
   of an untied vocabulary projection, excluding bias.

**Connects to:** [[ai/llms/tokenization|tokenization]] · [[ai/model-architectures/self-attention-from-first-principles|self-attention from first principles]] · [[ai/llms/decoding-and-sampling|decoding and sampling]] · [[ai/inference-and-optimization/kv-cache-and-memory|KV cache and memory]] · [[ai/llms/pretraining-next-token|next-token pretraining]]

## Sources

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — the decoder stack and autoregressive transformer architecture.
- [Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) — a concrete next-token language-modeling formulation and byte-pair vocabulary.
- [SentencePiece](https://arxiv.org/abs/1808.06226) — a language-independent tokenizer trained directly from raw sentences.
- [PyTorch softmax](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.softmax.html) — the framework definition and dimensional semantics of softmax.
- [Hugging Face generation strategies](https://huggingface.co/docs/transformers/generation_strategies) — current decoding, sampling, constraints, and cache-facing controls.
- [Hugging Face KV cache strategies](https://huggingface.co/docs/transformers/kv_cache) — cache types and the memory/latency trade-offs used in inference.
