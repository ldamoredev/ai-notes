# Glassbox AI Lab

Glassbox AI Lab is the executable spine of AI Atlas. Each milestone exposes a mechanism that a larger framework normally hides, keeps inputs tiny enough to inspect, and names the invariant the tests enforce.

## Run

Python 3.11+ is sufficient for the initial artifacts; there are no third-party dependencies.

```bash
python3 -m unittest labs.glassbox.test_glassbox -v
python3 -m labs.glassbox.v0_math
python3 -m labs.glassbox.v1_autodiff
python3 -m labs.glassbox.v4_attention
python3 -m labs.glassbox.v4_token_trace
```

## Implemented artifacts

| Milestone | Artifact | Learning question | Invariant |
|---|---|---|---|
| v0 | `v0_math.py` | How do vector operations, stable softmax, entropy, and sampling behave numerically? | Probabilities are finite, non-negative, and sum to one. |
| v1 | `v1_autodiff.py` | How does reverse-mode autodiff traverse a graph and accumulate gradients? | Analytical gradients match centered finite differences. |
| v4 experiment | `v4_attention.py` | What do Q, K, V, scaling, masking, softmax, and weighted aggregation compute? | Each visible attention row sums to one; future positions receive zero probability. |
| v4 experiment | `v4_token_trace.py` | What stages turn text into a sampled token? | Token IDs, logits, probabilities, selected ID, and decoded token are all observable. |

## Expected output

The scripts print deterministic traces. Floating-point values may differ in their final printed digit across Python builds, but tests use explicit tolerances.

## Break it deliberately

1. Remove the maximum subtraction from `stable_softmax` and pass logits near `1000`.
2. Replace `+=` with `=` in a local gradient update and run the shared-subexpression test.
3. Remove the `1 / sqrt(d_k)` attention scaling and compare how peaked the weights become as dimensions grow.
4. Remove the causal mask and observe the first token attending to future tokens.
5. Change the seed in the token trace and distinguish stochastic output from a changed probability distribution.

## Planned v2→v10

Neural network from scratch → tensor framework and vision → tokenizer and mini-transformer → training/adaptation → inference runtime → retrieval → tool-using agent → multimodal pipeline → production AI system. The specification lives in `content/en/ai/research-and-experimentation/index.md` and `CONTENT-PLAN.md`.
