---
title: "The data flywheel"
description: A data flywheel is a coupled feedback loop between quality and usage; closing it turns a fixed growth rate into a compounding one, and the gap widens every cycle.
tags: [data, data-flywheel, feedback, moat]
order: 13
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/data-for-ai/feedback-data-and-active-learning]
last_verified: 2026-07-20
---
# The data flywheel

**Mental model:** two quantities, product quality and usage, are coupled instead of
independent. Usage produces signal, signal (when actually mined and fed back) raises
quality, and higher quality raises usage beyond what marketing alone would produce.
"Flywheel" is not a metaphor for effort — it names a specific feedback loop, and
whether that loop is closed or open changes the shape of growth from linear to
compounding.

## Mechanism: a coupled recurrence

Let \(Q_t \in [0,1]\) be quality at cycle \(t\) (e.g. task success rate) and \(U_t\) be
usage. A minimal model of the loop:

\[
Q_{t+1} = Q_t + k\,(1 - Q_t), \qquad
U_{t+1} = U_t \left(1 + g + e\,(Q_t - Q_{\text{base}})\right)
\]

\(k\) is how efficiently captured signal closes the remaining gap to perfect quality
(mining, labeling, and retraining efficiency); \(g\) is baseline usage growth with no
quality edge at all (marketing, organic reach); \(e\) is how elastic usage is to a
quality edge over a static baseline competitor \(Q_{\text{base}}\). **If the loop is
open** (`k = 0`, captured signal never feeds back), quality is frozen at \(Q_0\) and
usage grows at the flat rate \(g\) forever — no compounding.

## Worked example

\(Q_0 = Q_{\text{base}} = 0.70\), \(U_0 = 1000\), \(g = 0.05\), \(e = 0.8\),
\(k = 0.15\):

| Cycle | Quality (loop closed) | Usage, loop closed | Usage, loop open |
|---:|---:|---:|---:|
| 0 | 0.700 | 1000.0 | 1000.0 |
| 1 | 0.745 | 1050.0 | 1050.0 |
| 2 | 0.783 | 1140.3 | 1102.5 |
| 3 | 0.816 | 1273.3 | 1157.6 |
| 4 | 0.843 | 1454.8 | 1215.5 |

Both start identically because at \(t=0\) quality has no edge yet. By cycle 4, closing
the loop produces **~20% more usage** than the identical system with the loop left
open — same starting product, same baseline growth rate, only the feedback path
differs. The gap keeps widening every cycle because the usage growth *rate* itself
rises as quality rises, while the open-loop rate stays flat at \(g\) forever.

## Executable artifact

Run with `python3`; expected output matches the table above (`t`, quality, usage with
the loop closed, usage with the loop open):

```python
def simulate(cycles, g, e, k, q0, qbase, u0, feedback):
    q, u = q0, u0
    rows = [(0, round(q, 3), round(u, 1))]
    for t in range(1, cycles + 1):
        r = g + e * (q - qbase) if feedback else g
        u = u * (1 + r)
        if feedback:
            q = q + k * (1 - q)
        rows.append((t, round(q, 3), round(u, 1)))
    return rows

g, e, k, q0, qbase, u0 = 0.05, 0.8, 0.15, 0.70, 0.70, 1000.0
closed = simulate(4, g, e, k, q0, qbase, u0, feedback=True)
open_loop = simulate(4, g, e, k, q0, qbase, u0, feedback=False)
for (t, q, u_closed), (_, _, u_open) in zip(closed, open_loop):
    print(t, q, u_closed, u_open)
```

## Why it's the real moat

Frontier models are available to everyone; the proprietary feedback loop is not. This
is the mechanism behind "ship early and learn" beating "polish in secret": \(k\) and
the signal that feeds it cannot exist until real users hit the system, so the team that
closes the loop first has a head start that the recurrence itself keeps widening.

## What "flywheel" pitches hide

A roadmap slide that says "flywheel" is describing an intent, not a measured \(k\).
Most systems that call themselves a flywheel have `k` close to zero in practice: usage
data is logged but never mined into new eval cases or training signal, so the loop is
open even though the pitch describes it as closed. The gap in the table above only
appears when \(k > 0\) is real, not aspirational.

## Failure modes and a decision rule

- **Logging without mining.** Usage data accumulates in a warehouse but nothing turns
  it into [[ai/evaluation/systematic-error-analysis|failure clusters]],
  [[ai/evaluation/designing-eval-sets|eval cases]], or training examples — `k = 0` in
  practice regardless of data volume.
- **Uninstrumented outcomes.** Capturing clicks and completions but not whether the
  result actually helped means the mined signal correlates poorly with true quality,
  which weakens the effective \(k\) even when a pipeline exists.
- **Cheap feedback ignored.** High-friction feedback (surveys, support tickets) yields
  too little volume to move \(Q_t\) meaningfully; cheap in-flow feedback (accept/edit/
  reject in the UI) yields far more signal per user interaction.
- **Elasticity assumed, not measured.** Treating \(e\) as large when the market is
  actually quality-insensitive (e.g. a captive or habitual user base) overstates the
  flywheel's payoff and misdirects investment away from the actual growth lever.

**Decision rule:** before calling something a flywheel, measure `k` — the fraction of
captured signal that actually reaches a retrain or eval update within a fixed cycle
(a week, a sprint). If that fraction is at or near zero, invest in the mining and
feedback pipeline before investing further in raw usage growth; growth without a
closed loop just produces logs, not compounding.

## Production lens

Instrument outcomes, not just outputs — [[ai/ai-product-engineering/product-metrics-for-ai|product
metrics]] should distinguish "the system responded" from "the response actually
helped." Track `k` operationally as a pipeline metric: signal captured per cycle vs.
signal that reached a shipped eval case or retrain, the same way a CI pipeline tracks
build-to-deploy lead time. [[ai/data-for-ai/privacy-and-pii-in-datasets|Privacy and
consent]] boundaries determine what feedback may be retained and reused at all, and
must be part of the pipeline design, not a later patch.

## Exercises

1. Re-run the simulation with `k = 0.05` (slow mining) and `k = 0.30` (fast mining);
   report the usage gap at cycle 4 for each and explain why it is nonlinear in `k`.
2. Set `e = 0` (usage indifferent to quality) and confirm the closed- and open-loop
   usage columns become identical even though quality still improves — showing quality
   improvement alone is not a flywheel without elastic demand.
3. For a real product you know, estimate `k` (fraction of usage signal that reaches a
   shipped eval case or retrain in one release cycle) and identify the single biggest
   leak between "signal captured" and "signal used."

**Connects to:** [[ai/data-for-ai/feedback-data-and-active-learning|feedback & active learning]] · [[ai/evaluation/eval-driven-development|eval-driven development]] · [[ai/mlops/feedback-loops|production feedback loops]] · [[ai/ai-product-engineering/product-metrics-for-ai|product metrics for AI]]

## Sources

- [Hidden Technical Debt in Machine Learning Systems](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems) — feedback loops as a distinct, compounding category of ML systems debt.
- [Data Cascades in High-Stakes AI](https://research.google/pubs/data-cascades-in-high-stakes-ai/) — how upstream data and feedback shortcuts compound downstream, the mirror image of a healthy flywheel.
- [Continuous Delivery for Machine Learning](https://martinfowler.com/articles/cd4ml.html) — the pipeline discipline (versioning, testing, feedback) a real closed loop requires operationally.
- [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/) — production-readiness signals, including monitoring the feedback path itself.
