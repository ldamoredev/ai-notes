---
title: "Model deprecation & migration"
description: Models you depend on get retired or silently updated. How to insulate your system, detect behavior changes, and migrate without breaking production.
tags: [mlops, deprecation, migration, versioning]
order: 14
updated: 2026-06-07
---
# Model deprecation & migration

A reality of building on someone else's model: it **won't last forever**. Providers
deprecate model versions on a schedule, and even "the same" model can shift behavior
after an update. If your prompts and product are tuned to one model, a migration can
silently break things. Plan for it from day one.

## Why this bites

- **Hard deprecations** — a provider sunsets a model version; your calls start failing
  on a deadline you must meet.
- **Silent updates** — a model alias (e.g. "latest") points to new weights; outputs
  drift even though your code didn't change ([[ai/foundations/distribution-shift|a
  distribution shift]] you didn't cause).
- **Prompt brittleness** — prompts and [[ai/prompt-engineering/zero-and-few-shot|few-shot
  examples]] over-tuned to one model don't transfer cleanly.

## Insulate the system up front

- **Pin explicit versions**, not floating aliases, so updates are a *choice*, not a
  surprise.
- **Abstract the model** behind a thin interface so swapping providers/models is a
  config change, not a rewrite.
- **Keep prompts versioned** in a [[ai/mlops/model-and-prompt-registry|registry]] and
  decoupled from app logic.
- **Track the provider's deprecation calendar** as an operational dependency.

## Migrate with evals, not hope

A model swap is a behavior change — treat it like a deploy:

1. Run the new model against your [[ai/evaluation/designing-eval-sets|eval set]] and
   **diff** against the current model ([[ai/evaluation/prompt-regression-testing|regression
   test]]).
2. Re-tune prompts for the new model where needed (don't assume they transfer).
3. **Canary / shadow** — run new alongside old on real traffic, compare, then ramp.
4. Keep a rollback path until the new model is proven.

## Pitfall

Discovering a deprecation the week it takes effect, with prompts hand-tuned to the old
model and no eval set to validate the replacement — so the migration is a scramble and
ships regressions. The fix is boring and upfront: pin versions, version prompts, keep an
eval set, and migrate behind a canary.

**Connects to:** [[ai/mlops/model-and-prompt-registry|prompt/model registry]] ·
[[ai/evaluation/prompt-regression-testing|regression testing]] ·
[[ai/ai-product-engineering/choosing-a-model|model selection]]
