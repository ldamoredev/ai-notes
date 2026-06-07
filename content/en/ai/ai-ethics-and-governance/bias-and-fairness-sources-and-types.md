---
title: "Bias and fairness: sources and types"
description: Bias can enter through problem framing, sampling, labels, features, objectives, deployment context, and feedback loops.
tags: [fairness, bias, responsible-ai]
order: 2
updated: 2026-06-07
---
# Bias and fairness: sources and types

Bias is not only a model defect. It can come from the world being measured, the data
collection process, the labels, the objective, the deployment context, or the way users
react to the system.

## Sources of bias

| Source | Example |
|---|---|
| Historical bias | past decisions encode discrimination |
| Representation bias | some groups are under-sampled or missing |
| Measurement bias | proxies measure different things across groups |
| Label bias | annotators or institutions apply labels inconsistently |
| Aggregation bias | one model is forced across groups with different patterns |
| Deployment bias | model is used in a context it was not designed for |
| Feedback bias | model outputs shape future data collection |

## Fairness questions

- Are outcomes different across protected or meaningful groups?
- Are errors different across groups?
- Are users equally able to contest or correct outputs?
- Does the model rely on proxies for sensitive attributes?
- Does the product increase or reduce existing inequities?

## AI-specific patterns

LLMs can reproduce stereotypes in generated text, image models can underrepresent
groups, retrieval systems can surface biased sources, and agents can automate biased
decisions at scale if the workflow gives them authority.

## Pitfall

Removing sensitive attributes does not remove bias. Proxies such as location, language,
education, device, or history can still recreate group differences.

**Connects to:** [[ai/data-for-ai/dataset-design-and-sampling|dataset design]] ·
[[ai/foundations/distribution-shift|distribution shift]] ·
[[ai/evaluation/systematic-error-analysis|error analysis]]
