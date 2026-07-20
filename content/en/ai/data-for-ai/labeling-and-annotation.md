---
title: "Labeling and annotation"
description: Labels are a measurement process with instrument error; Cohen's kappa separates real agreement from chance, and guidelines are the measurement protocol.
tags: [data-for-ai, labeling, annotation, agreement]
order: 3
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/data-for-ai/data-quality-dimensions]
last_verified: 2026-07-20
---
# Labeling and annotation

**Mental model:** a label is a measurement, an annotator is an instrument, and a
guideline is the measurement protocol. Like any instrument, annotators have bias
(systematic drift from ground truth) and variance (disagreement with each other on the
same item). Improving labels means improving the protocol and calibrating the
instrument — not just hiring more annotators.

## Mechanism: agreement corrected for chance

Raw percent agreement is misleading because two annotators can agree often purely by
guessing the majority class. Cohen's kappa corrects for that:

\[
\kappa = \frac{p_o - p_e}{1 - p_e}
\]

where \(p_o\) is observed agreement (fraction of items where both annotators gave the
same label) and \(p_e\) is the agreement expected if each annotator labeled
independently according to their own marginal rate. For two annotators on a binary
task with marginal "yes" rates \(y_1, y_2\):

\[
p_e = y_1 y_2 + (1-y_1)(1-y_2).
\]

\(\kappa = 0\) means agreement is no better than chance; \(\kappa = 1\) is perfect
agreement. The common (if debated) interpretation bands are: \(<0.2\) slight,
\(0.2\text{–}0.4\) fair, \(0.4\text{–}0.6\) moderate, \(0.6\text{–}0.8\) substantial,
\(>0.8\) almost perfect.

## Worked example: the base-rate trap

**Balanced task** (roughly 50/50 spam vs not-spam), 100 items, two annotators:

| | Ann. 2: yes | Ann. 2: no | Total |
|---|---:|---:|---:|
| **Ann. 1: yes** | 45 | 5 | 50 |
| **Ann. 1: no** | 8 | 42 | 50 |
| Total | 53 | 47 | 100 |

\(p_o = (45+42)/100 = 0.87\). Marginals: \(y_1 = 0.50\), \(y_2 = 0.53\), so
\(p_e = 0.50 \cdot 0.53 + 0.50 \cdot 0.47 = 0.50\). \(\kappa = (0.87-0.50)/(1-0.50) =
0.74\) — substantial agreement, and it tracks the 87% raw number reasonably well.

**Skewed task** (95% of items are the negative class — the common case for abuse or
defect detection), also 100 items:

| | Ann. 2: yes | Ann. 2: no | Total |
|---|---:|---:|---:|
| **Ann. 1: yes** | 3 | 2 | 5 |
| **Ann. 1: no** | 2 | 93 | 95 |
| Total | 5 | 95 | 100 |

\(p_o = (3+93)/100 = 0.96\) — looks *better* than the balanced case. But
\(y_1=y_2=0.05\), so \(p_e = 0.05^2 + 0.95^2 = 0.905\): both annotators agree on "no"
almost automatically because "no" is 95% of items. \(\kappa = (0.96-0.905)/(1-0.905) =
0.58\) — only moderate. The 96% raw number was mostly chance, not signal. Skewed
classes always need kappa (or a class-conditional metric), never raw agreement alone.

## Executable artifact

Run with `python3`; expected output is `0.74` then `0.58`, confirming the two cases
above and printing the interpretation band:

```python
def cohens_kappa(both_yes, ann1_yes_ann2_no, ann1_no_ann2_yes, both_no):
    n = both_yes + ann1_yes_ann2_no + ann1_no_ann2_yes + both_no
    po = (both_yes + both_no) / n
    y1 = (both_yes + ann1_yes_ann2_no) / n
    y2 = (both_yes + ann1_no_ann2_yes) / n
    pe = y1 * y2 + (1 - y1) * (1 - y2)
    return (po - pe) / (1 - pe)

def band(k):
    if k < 0.2: return "slight"
    if k < 0.4: return "fair"
    if k < 0.6: return "moderate"
    if k < 0.8: return "substantial"
    return "almost perfect"

balanced = cohens_kappa(45, 5, 8, 42)
skewed = cohens_kappa(3, 2, 2, 93)
print(round(balanced, 2), band(balanced))
print(round(skewed, 2), band(skewed))
```

## Build labeling guidelines

- Define each label with inclusion and exclusion rules, plus positive, negative, and
  borderline examples.
- State explicitly whether annotators should infer intent or use only visible evidence.
- Version guidelines and record which version produced each label batch — a guideline
  change invisibly changes the label distribution.
- Track gold-question accuracy (known-answer items mixed into the queue) to catch
  annotator drift over time, not just disagreement between annotators at one point.

## What labeling platforms hide

Turnkey annotation tools report a single "agreement" number, often raw percent
agreement, without exposing the marginal rates that make it interpretable. They also
average agreement across the whole dataset, hiding that agreement is usually much
worse on the rare, ambiguous, or high-value slice than on the easy majority slice —
exactly the slice that matters most for a hard product decision.

## Failure modes and a decision rule

- **Disagreement mistaken for annotator error.** Low kappa can mean the taxonomy is
  ambiguous or the task needs more context, not that annotators are careless.
- **Anchoring on model pre-labels.** Model-assisted labeling speeds up humans but
  annotators tend to rubber-stamp a plausible-looking pre-label instead of
  independently verifying it, silently importing the model's own bias.
  [[ai/data-for-ai/synthetic-data|Synthetic data]] has the same anchoring risk in
  reverse: a model trained on its own outputs.
- **Aggregate-only audits.** A dataset can have healthy overall kappa while one
  minority slice is near chance; audit by slice, not just in aggregate.
- **Majority-vote flattening.** Taking the majority label from 3+ annotators discards
  the disagreement signal entirely; keep raw per-annotator labels alongside the
  resolved one.

**Decision rule:** \(\kappa < 0.4\) on a slice → stop labeling and fix the taxonomy or
guideline before scaling; \(0.4\text{–}0.75\) → refine guidelines, add adjudication for
disagreements, and keep monitoring; \(>0.75\) → scale with periodic gold-question and
slice audits rather than re-reviewing every item.

## Production lens

Compute kappa (or a multi-annotator variant such as Krippendorff's alpha) per batch and
per slice, not once at project kickoff — guidelines drift as edge cases accumulate. Pin
the guideline version and annotator agreement stats to the dataset version that trains
or evaluates a model, so a later regression can be traced to a labeling change instead
of a model change.

## Exercises

1. Compute \(\kappa\) for a 3-annotator majority-vote table of your choosing and
   compare it to pairwise kappa between each pair of annotators.
2. Take the skewed example above and find the raw agreement at which \(\kappa\) crosses
   from "moderate" to "substantial" while keeping the 95/5 base rate fixed.
3. Design a one-page guideline for a genuinely ambiguous label (e.g. "toxic") including
   at least two borderline examples and the rule for missing evidence.

**Connects to:** [[ai/evaluation/human-evaluation|human evaluation]] · [[ai/fine-tuning-and-alignment/building-the-finetuning-dataset|fine-tuning datasets]] · [[ai/data-for-ai/datasheets-and-data-documentation|data documentation]] · [[ai/data-for-ai/data-quality-dimensions|data quality dimensions]]

## Sources

- [Inter-Coder Agreement for Computational Linguistics](https://aclanthology.org/J08-4004/) — Artstein & Poesio's survey of agreement coefficients, their assumptions, and misuse.
- [Snorkel: Rapid Training Data Creation with Weak Supervision](https://arxiv.org/abs/1711.10160) — programmatic labeling functions as an alternative to pure hand-labeling.
- [Data Cascades in High-Stakes AI](https://research.google/pubs/data-cascades-in-high-stakes-ai/) — how upstream labeling shortcuts compound into downstream failures.
- [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) — documenting collection and annotation process alongside the data itself.
