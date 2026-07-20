---
title: "Onboarding and expectations"
description: AI onboarding should teach the user what the feature is good at, what it cannot do, and how to steer or verify it.
tags: [ai-product, onboarding, ux, expectations]
order: 10
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/ai-product-engineering/handling-errors-and-hallucinations-in-ui]
last_verified: 2026-07-20
---
# Onboarding and expectations

## Mechanism: capability boundary → user mental model → corrective feedback

```python
expectation = {"can": "draft with cited sources", "cannot": "guarantee correctness"}
print(expectation["cannot"])
```

Run with `python3`; expected output names the limit. Onboarding should state role, evidence, authority, privacy, correction, and escalation before a user relies on the feature.

## Production lens and exercises

Measure first-task success, correction use, escalation, abandonment, and overreliance reports. Update onboarding when model, permissions, evidence sources, or fallback behavior changes; stale expectations are a product defect.

1. Write a first-run disclosure for an AI feature that can draft but cannot submit.
2. Test whether a user can find and correct a wrong answer without rereading a help center.

## Sources

- [People + AI Guidebook](https://pair.withgoogle.com/guidebook/) — expectation-setting patterns.
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — transparency context.

AI features fail when users expect magic or when they do not know how to steer the
system. Onboarding should set usable expectations without burying the product in
warnings.

## What onboarding must teach

- What tasks the feature is designed for.
- What inputs produce good results.
- What the model can and cannot access.
- How to verify sources or evidence.
- How to edit, correct, reject, or escalate.
- Which actions are automatic and which require approval.

The best onboarding is often embedded in the workflow: examples, templates, empty
states, constraints, and progressive hints.

## Calibrate trust

Too much hype causes over-trust; too many warnings cause abandonment. Calibrated trust
means the user understands where the feature is strong and where review is needed.

## Use examples

Examples are more useful than abstract capability claims. Show concrete prompts,
before/after outputs, and "good for / not good for" boundaries.

## Pitfall

Do not make users learn prompt engineering to use the product. Good product design
turns common tasks into guided controls and sensible defaults.

**Connects to:** [[ai/prompt-engineering/anatomy-of-a-prompt|prompt anatomy]] ·
[[ai/ai-product-engineering/ux-patterns-for-ai|UX patterns]] ·
[[ai/ai-product-engineering/handling-errors-and-hallucinations-in-ui|error recovery]]
