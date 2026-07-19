---
title: Probability, Likelihood, and Uncertainty
description: Random variables, distributions, conditioning, Bayes' rule, likelihood, calibration, and the uncertainty claims AI systems can and cannot make.
tags: [probability, likelihood, uncertainty, bayes, calibration]
order: 2
updated: 2026-07-19
kind: derivation
level: beginner
status: current
prerequisites: [ai/mathematics-for-ai/vectors-matrices-and-tensors]
last_verified: 2026-07-19
---
# Probability, Likelihood, and Uncertainty

Probability is a language for uncertain events under a model. Likelihood reuses the same mathematical function while treating observed data as fixed and parameters as variable. Neither is automatically truth, confidence, causality, or safety.

The mental model is a pipeline: define a sample space and random variables, choose or learn a distribution, condition on evidence, make a decision, then test whether predicted uncertainty matches observed frequencies on the deployment population.

## Events, random variables, and distributions

A sample space `Ω` contains possible outcomes. An event is a subset of `Ω`. A random variable `X` maps outcomes to values. A probability distribution assigns mass or density under explicit assumptions.

For a categorical classifier with classes `cat`, `dog`, and `fox`:

```text
p(Y) = [0.60, 0.30, 0.10]
Σᵧ p(Y=y) = 1
```

These numbers are a model's distribution over a defined label variable. They do not express uncertainty about whether the labels are valid, whether the input is in distribution, or whether the decision is safe.

## Joint, marginal, and conditional probability

A joint distribution `p(X, Y)` describes two variables together. Marginalization removes a variable by summing or integrating:

```text
p(X=x) = Σᵧ p(X=x, Y=y)
```

Conditional probability restricts to evidence with nonzero probability:

```text
p(Y=y | X=x) = p(X=x, Y=y) / p(X=x)
```

The product rule follows:

```text
p(X, Y) = p(Y | X)p(X) = p(X | Y)p(Y)
```

Autoregressive language models repeatedly apply the chain rule of probability:

```text
p(x₁, …, x_N) = Πₜ p(xₜ | x₁, …, xₜ₋₁)
```

The model does not generate a sentence in one atomic act. It represents and samples successive conditional distributions.

## Bayes' rule

Rearranging the product rule gives:

```text
p(H | D) = p(D | H)p(H) / p(D)
```

- `H`: hypothesis or parameter value.
- `D`: observed data.
- `p(H)`: prior.
- `p(D | H)`: likelihood.
- `p(H | D)`: posterior.
- `p(D)`: evidence or marginal likelihood.

### Numerical example

Suppose a condition has prevalence `p(H)=0.01`. A test is positive with sensitivity `p(+|H)=0.95` and false-positive rate `p(+|¬H)=0.05`.

```text
p(+) = 0.95×0.01 + 0.05×0.99 = 0.059
p(H|+) = 0.95×0.01 / 0.059 ≈ 0.161
```

A positive result implies about 16.1% posterior probability under these assumptions, not 95%. Base rates matter.

## Probability versus likelihood

Let observations `D = {x₁, …, x_n}` come from a model with parameter `θ`.

- Probability asks about possible data with `θ` fixed: `p(D | θ)`.
- Likelihood treats observed `D` as fixed and compares parameter values: `L(θ; D) = p(D | θ)`.

Likelihood is not a probability distribution over `θ` unless it is combined with a prior and normalized. Its values need not sum to one across parameter choices.

Maximum likelihood chooses:

```text
θ_hat = argmax_θ Πᵢ p(xᵢ | θ)
```

Products of many small probabilities underflow, so computation uses log-likelihood:

```text
log L(θ; D) = Σᵢ log p(xᵢ | θ)
```

Maximizing likelihood is equivalent to minimizing negative log-likelihood. For a one-hot categorical target, this becomes cross-entropy.

## Aleatoric and epistemic uncertainty

- Aleatoric uncertainty belongs to outcome variability under the data-generating process: sensor noise or inherently ambiguous labels.
- Epistemic uncertainty belongs to limited knowledge: sparse coverage, unknown parameters, or model misspecification.

This distinction is useful but not perfectly observable. A single softmax output generally mixes neither source in a complete, identifiable way. Ensembles, Bayesian approximations, and predictive intervals can estimate aspects of uncertainty only under their assumptions.

## Calibration

A predictor is calibrated for an event on a population if cases assigned probability near `q` realize the event about fraction `q` of the time. Calibration is a group-frequency property, not a guarantee for one case.

For 100 predictions near 0.8 confidence, roughly 80 should be correct for that bin under the evaluated distribution. Reliability diagrams, expected calibration error, Brier score, and log loss reveal different aspects and all require sufficient data.

Important boundaries:

- Token probability is probability of a token under the model, not calibrated factual confidence.
- Calibration can hold overall and fail in an important subgroup.
- A calibrated model can be inaccurate; it may honestly assign low confidence.
- Calibration can break under distribution shift.

## Decision theory: uncertainty is not the action

Predictions become decisions through costs or utilities. If false negatives cost much more than false positives, the optimal threshold is not necessarily 0.5.

For actions `a` and outcomes `y`, choose an action that minimizes expected loss:

```text
a* = argmin_a Σᵧ p(y | x) C(a, y)
```

This makes the product decision explicit. The model estimates a distribution; the application supplies consequences, constraints, abstention, and human escalation.

## Executable artifact

Glassbox v0 turns logits into stable probabilities, computes entropy and cross-entropy, and performs seeded categorical sampling:

```bash
python3 -m labs.glassbox.v0_math
python3 -m unittest labs.glassbox.test_glassbox.MathTests -v
```

The critical softmax step subtracts the maximum logit before exponentiation:

```python
offset = max(logits)
exponentials = [math.exp(value - offset) for value in logits]
probabilities = [value / sum(exponentials) for value in exponentials]
```

Subtracting a constant does not change softmax ratios, but prevents overflow near large logits.

## What frameworks hide

- Distribution parameter constraints and transforms.
- Stable `log_softmax`/cross-entropy fusion.
- Independence assumptions inside factored likelihoods.
- Whether uncertainty is over labels, parameters, samples, sequences, or decisions.
- Calibration population and binning choices.
- Random-number-generator state and sampling policy.

## Failure modes and limits

- Assigning probabilities without defining the event.
- Reading a likelihood value as posterior probability.
- Ignoring base rates when interpreting evidence.
- Assuming softmax confidence is factual confidence.
- Reporting entropy as uncertainty without naming the represented distribution.
- Using point estimates when tail risk or coverage matters.
- Applying a calibration result after the population has shifted.

Decision rule: state `p(what | what)` in words. If you cannot name the event, conditioning evidence, population, and estimation protocol, do not make a calibrated probability claim.

## Production lens

Store the model and calibration revisions, decision threshold, population slice, and outcome window with every uncertainty report. Monitor reliability curves and expected calibration error by consequential slice, but retain raw counts and intervals: aggregate calibration can hide a small group that is confidently wrong. Define abstention and escalation as product actions rather than treating probability alone as a policy.

## Exercises

1. Recompute the test example with prevalence 10%; explain why the posterior changes.
2. Derive negative log-likelihood for a Bernoulli observation.
3. Pass logits `[1000, 1001, 999]` through naive and stable softmax.
4. Create ten predictions and compute a two-bin reliability table by hand.
5. Define a cost matrix where a 0.2 threshold is optimal.

**Connects to:** [[ai/mathematics-for-ai/information-theory-entropy-and-divergence|Information Theory, Entropy, and Divergence]] · [[ai/evaluation/metrics-for-llm-evals|Metrics for LLM Evals]] · [[ai/foundations/distribution-shift|Distribution Shift]]

## Sources

- [Probabilistic Machine Learning: An Introduction](https://probml.github.io/pml-book/book1.html) — probability, inference, decision theory, and modern ML in one coherent notation.
- [Mathematics for Machine Learning, Chapter 6](https://mml-book.github.io/) — probability foundations with ML applications.
- [On Calibration of Modern Neural Networks](https://arxiv.org/abs/1706.04599) — empirical calibration study and temperature scaling.
- [scikit-learn calibration guide](https://scikit-learn.org/stable/modules/calibration.html) — reliability diagrams and calibrated-classifier behavior.
