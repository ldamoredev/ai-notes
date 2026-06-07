---
title: "Eval-driven development"
description: Evals are the unit tests of AI. Writing them first turns prompt/model tuning from guesswork into a measurable loop — the core working discipline for shipping AI.
tags: [evaluation, methodology, eval-driven, workflow]
order: 13
updated: 2026-06-07
---
# Eval-driven development

The defining methodology of serious AI engineering: **build the eval first, then
iterate against it.** Because LLM systems are non-deterministic and "looks good" doesn't
scale, an [[ai/evaluation/designing-eval-sets|eval set]] is the only honest signal that a
change helped. Evals are to AI what unit tests are to software.

## Why "try it and see" fails

A single good output says nothing about the distribution of inputs. Tuning a
[[ai/prompt-engineering/index|prompt]], swapping a [[ai/ai-product-engineering/choosing-a-model|model]],
or changing [[ai/rag-and-retrieval/index|retrieval]] by eyeballing one example means you
fix one case and silently break others. Without a measurement, "better" is a feeling.

## The loop

1. **Collect real examples** — from logs, users, and known failure cases.
2. **Define success** — exact checks where possible, a rubric +
   [[ai/evaluation/llm-as-judge|LLM-as-judge]] where not,
   [[ai/evaluation/human-evaluation|human review]] for the rest.
3. **Establish a baseline** — score the current system.
4. **Change one thing**, run the **whole** eval set, compare to baseline.
5. **Error-analyze** the failures ([[ai/evaluation/systematic-error-analysis|systematically]]),
   which feeds the next change *and* new eval cases.
6. **Gate releases** on the eval in [[ai/mlops/index|CI]] — no regressions ship.

## It compounds

Every production failure becomes a new eval case, so the suite keeps getting stricter as
the system meets reality — the [[ai/data-for-ai/the-data-flywheel|flywheel]] applied to
quality. The eval set becomes your most valuable, hardest-to-copy asset.

## Where it plugs into the stack

Eval-driven development is the practice; the targeted notes are the techniques:
[[ai/evaluation/designing-eval-sets|building eval sets]],
[[ai/evaluation/llm-as-judge|LLM-as-judge]],
[[ai/evaluation/prompt-regression-testing|regression testing]],
[[ai/rag-and-retrieval/evaluating-rag|RAG eval]],
[[ai/agents-and-tools/evaluating-agents|agent eval]].

## Pitfall

Building the product first and bolting on evals "later" — by then you have no baseline,
no regression safety net, and changes are pure guesswork. Start the eval set on day one,
even tiny; a 20-example eval beats zero by an enormous margin.

**Connects to:** [[ai/evaluation/designing-eval-sets|designing eval sets]] ·
[[ai/prompt-engineering/evaluating-and-iterating-prompts|iterating prompts]] ·
[[ai/data-for-ai/the-data-flywheel|the data flywheel]]
