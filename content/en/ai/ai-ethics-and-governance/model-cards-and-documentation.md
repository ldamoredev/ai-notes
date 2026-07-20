---
title: "Model cards and documentation"
description: Documentation is a versioned evidence chain from data and model to deployed system, release decision, and incident response.
tags: [model-cards, documentation, governance]
order: 6
updated: 2026-07-20
kind: implementation
level: intermediate
status: current
prerequisites: [ai/data-for-ai/datasheets-and-data-documentation, ai/mlops/model-and-prompt-registry]
last_verified: 2026-07-20
---
# Model cards and documentation

**Mental model:** a card is an interface contract for a decision maker. It answers
what version exists, what it was evaluated to do, what it must not do, what evidence
supports that claim, and who can respond when production contradicts it. A static PDF
cannot document a changing prompt, retrieval corpus, tool set, and model release.

## Mechanism: evidence chain to release gate

Connect a data card (provenance and rights), model card (capabilities and limits),
system card (assembly and controls), eval report (release evidence), and incident
record (what failed). Each artifact references immutable versions and a responsible
owner. A changed dependency invalidates the relevant evidence and triggers review.

```python
release = {"model":"v3", "prompt":"p19", "corpus":"c42", "eval":"e12",
           "owner":"ml-platform", "rollback":"v2"}
required = ["model", "prompt", "corpus", "eval", "owner", "rollback"]
assert all(release[k] for k in required)
print("documentation gate passed")
```

Run with `python3`; expected output is `documentation gate passed`. In a production
pipeline, resolve these identifiers to signed artifacts and reject a missing result.

## Minimum useful fields

| Artifact | Must make inspectable |
|---|---|
| Data card | collection, consent/rights, composition, gaps, retention |
| Model card | intended/out-of-scope use, eval slices, limitations, cost/latency |
| System card | prompts, retrieval, tools, access controls, user journey |
| Eval report | fixtures, oracle/rubric, baseline, failures, thresholds |
| Incident report | timeline, impact, versions, mitigation, follow-up |

Documentation is not a claim of safety. It exposes what was and was not tested, so a
consumer can reject an unsupported use. Keep it close to code and release metadata;
review it after fine-tuning, model change, prompt/tool/corpus change, or incident.

## Failure modes and decision rule

Vendor documentation omits application context; a model card without evaluated scope
is marketing; a card copied across versions creates false assurance. Require a current
evidence chain before release and publish a user-appropriate summary where transparency
or recourse requires it. Preserve historical cards rather than overwriting them.

## Exercises

1. Add an `evaluation_date` and fail the artifact when it predates a model change.
2. Draft the system-card entry for one retrieval source and its permission boundary.

**Connects to:** [[ai/data-for-ai/datasheets-and-data-documentation|datasheets]] · [[ai/evaluation/model-vs-product-evals|product evals]] · [[ai/mlops/model-and-prompt-registry|registry]] · [[ai/ai-ethics-and-governance/accountability-and-human-oversight|ownership]]

## Sources

- [Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993) — original model-card proposal and sections.
- [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) — dataset documentation questions.
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — lifecycle governance and evidence expectations.
