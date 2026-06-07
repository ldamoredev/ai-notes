---
title: "Task-specific evals"
description: Generic quality rubrics are weak; strong evals encode the exact task, output contract, risks, and acceptable tradeoffs.
tags: [evaluation, rubrics, task-design]
order: 5
updated: 2026-06-07
---
# Task-specific evals

The best evals are specific to the job the system performs. "Good answer" is too
vague; "extract the renewal date, cite the clause, and return valid JSON" is testable.

## Start from the task contract

- What input does the system receive?
- What output format is promised?
- What information must be correct?
- What evidence or citation is required?
- What should the system do when information is missing?
- What errors are cheap, expensive, or unacceptable?

This turns product expectations into grading criteria.

## Common task patterns

| Task | Primary checks | Extra checks |
|---|---|---|
| Classification | label accuracy, confusion matrix | calibration, class imbalance |
| Extraction | exact fields, schema validity | citation, missing-field behavior |
| Summarization | coverage, faithfulness | no unsupported claims |
| RAG Q&A | answer correctness, groundedness | retrieval recall, citation quality |
| Tool use | valid arguments, correct tool | side effects, permission boundary |
| Creative assistance | usefulness, fit to brief | tone, originality, safety |

## Rubric shape

- Define pass/fail criteria before comparing model outputs.
- Include examples of pass, partial pass, and fail.
- Separate correctness from style so a polished wrong answer does not pass.
- Keep the rubric stable across model comparisons.

## Pitfall

Generic judges usually reward fluency. Task-specific rubrics reward the behavior that
matters, even when the best answer is short, cautious, or says "I do not know".

**Connects to:** [[ai/evaluation/llm-as-judge|LLM-as-judge]] ·
[[ai/prompt-engineering/anatomy-of-a-prompt|prompt anatomy]] ·
[[ai/ai-product-engineering/onboarding-and-expectations|expectations]]
