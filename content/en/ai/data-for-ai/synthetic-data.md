---
title: "Synthetic data"
description: Synthetic data can expand coverage, bootstrap rare cases, and protect privacy, but it can also amplify bias, leak prompts, and cause model collapse.
tags: [data-for-ai, synthetic-data, model-collapse]
order: 6
updated: 2026-06-07
---
# Synthetic data

Synthetic data is generated rather than directly collected from the target process. It
can be useful, but only when the generation process, filtering, and evaluation are
designed deliberately.

## Good uses

- Creating rare but important edge cases.
- Bootstrapping instruction-following examples.
- Generating paraphrases for robustness testing.
- Producing simulation data when real collection is expensive or unsafe.
- Redacting or transforming sensitive examples while preserving task structure.

## Risks

| Risk | What happens |
|---|---|
| Model collapse | repeated training on generated data narrows the distribution |
| Bias amplification | generator reproduces or intensifies source bias |
| False diversity | many examples look different but test the same behavior |
| Leakage | generated examples reveal private seed data |
| Evaluation contamination | synthetic evals become too aligned to the generator |

## Quality controls

- Keep human-reviewed seed examples.
- Mix synthetic data with real data and track ratios.
- Filter for correctness, diversity, and task relevance.
- Evaluate on real holdout cases.
- Record generator, prompt, sampling settings, and filters in dataset documentation.

## Pitfall

Synthetic data is not free ground truth. The generator can be confidently wrong, and a
student model can inherit those errors at scale.

**Connects to:** [[ai/fine-tuning-and-alignment/distillation|distillation]] ·
[[ai/data-for-ai/datasheets-and-data-documentation|dataset documentation]] ·
[[ai/evaluation/designing-eval-sets|eval sets]]
