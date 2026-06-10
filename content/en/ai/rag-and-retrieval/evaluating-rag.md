---
title: "Evaluating RAG: retriever vs generator"
description: RAG fails in two distinct places — retrieval and generation. Evaluate them separately, or you'll tune the wrong half.
tags: [rag, evaluation, ragas, metrics]
order: 9
updated: 2026-06-10
---
# Evaluating RAG: retriever vs generator

**Mental model:** a bad RAG answer has two possible causes with *opposite* fixes — the
right chunk was never retrieved (fix chunking/recall), or it was retrieved and the
model ignored or mangled it (fix grounding/prompt). One end-to-end score cannot
distinguish them, so the cardinal rule is: **measure the retriever and the generator
separately.** Everything else in RAG eval is detail on top of that split.

## Retriever metrics (classic IR, on (query → relevant chunks) pairs)

- **Recall@k** — fraction of queries whose needed chunk(s) appear in the top k. The
  metric that matters most: a recall miss is unrecoverable downstream.
- **Precision@k** — fraction of the top k that is relevant; proxies context noise.
- **MRR** — `mean(1/rank of first relevant)`; rewards putting the answer first.
- **nDCG@k** — rank-position-discounted gain; the right metric when relevance is
  graded rather than binary (the BEIR standard, Thakur et al. 2021,
  [arXiv:2104.08663](https://arxiv.org/abs/2104.08663)).

Practical split: track **recall@50** (did stage one find it?) and **recall@5 /
precision@5** (did [[ai/rag-and-retrieval/reranking|reranking]] surface it into the
prompt?). The pair tells you which stage to fix.

```typescript
type Example = { query: string; relevantChunkIds: string[] };

export async function evalRetriever(examples: Example[], k = 5) {
  let recallSum = 0, mrrSum = 0;
  for (const ex of examples) {
    const got = (await retrieve(ex.query, k)).map((c) => c.id);
    const hitRank = got.findIndex((id) => ex.relevantChunkIds.includes(id));
    recallSum += ex.relevantChunkIds.some((id) => got.includes(id)) ? 1 : 0;
    mrrSum += hitRank >= 0 ? 1 / (hitRank + 1) : 0;
  }
  return { recallAtK: recallSum / examples.length, mrr: mrrSum / examples.length };
}
```

Thirty lines of code, no framework — run it in CI on every chunking/embedding/index
change, exactly like a test suite
([[ai/evaluation/prompt-regression-testing|regression testing]]).

## Generator metrics (hold context fixed, judge the answer)

The RAGAS framework (Es et al. 2023,
[arXiv:2309.15217](https://arxiv.org/abs/2309.15217)) named the axes everyone now
uses, each scored by an [[ai/evaluation/llm-as-judge|LLM judge]]:

| Metric | Question it answers | Diagnoses |
|---|---|---|
| **Faithfulness** | is every claim in the answer entailed by the context? | hallucination / parametric bleed |
| **Answer relevance** | does the answer address the question? | evasion, padding |
| **Context precision** | is what was retrieved actually relevant? | noisy retrieval |
| **Context recall** | does the context cover the ground-truth answer? | retrieval misses (needs ground truth) |

Faithfulness is the load-bearing one. The mechanism: decompose the answer into atomic
claims, then ask the judge per claim whether the context supports it — far more
reliable than one holistic 1–10 score (judges are poorly calibrated on scalar scales;
binary per-claim verdicts aggregate better). Use a strong model as judge, and check
the judge against ~30 human-labeled examples before trusting it
([[ai/evaluation/llm-as-judge|judge validation]]).

## Building the eval set

You need 30–100 examples of `(query, ground-truth answer, relevant chunk ids)`:

- **Mine real queries** from logs (or pilot users) — invented queries systematically
  miss real phrasing, typos, and follow-ups.
- **Label relevant chunks** by searching the corpus manually — tedious, one-time, and
  the only way to compute recall.
- **Include hard negatives**: unanswerable questions (tests refusal), conflicting-doc
  questions, exact-identifier lookups, conversational follow-ups.
- **Synthetic generation** (LLM writes Q from each chunk) bootstraps cheaply but
  overfits to chunk phrasing — real recall will look better than it is. Blend, don't
  rely on it alone.

This is the same discipline as [[ai/evaluation/designing-eval-sets|any eval set]];
without it you are tuning by vibes.

## Tooling (2026)

[RAGAS](https://docs.ragas.io/) (Python) implements the metrics above;
[promptfoo](https://promptfoo.dev/) runs YAML-configured eval suites in CI (TS-native,
fits your stack); Langfuse/Braintrust attach evals to
[[ai/mlops/llm-observability-and-tracing|production traces]] so you can score live
traffic samples, not just offline sets. The order of value: **logged traces → manual
30-example set → automated retriever metrics → LLM-judged generator metrics.** Teams
that jump straight to a framework without the labeled set automate the measurement of
nothing.

## Decision rules from the numbers

| Reading | Diagnosis | Fix |
|---|---|---|
| recall@50 low | stage-1 retrieval misses | [[ai/rag-and-retrieval/chunking|chunking]], [[ai/rag-and-retrieval/hybrid-search|hybrid]], [[ai/rag-and-retrieval/query-transformations|transforms]] |
| recall@50 high, recall@5 low | ranking | add/tune [[ai/rag-and-retrieval/reranking|reranker]] |
| context precision low | noisy top-k | smaller k, reranker, better filters |
| faithfulness low | generation ignores context | [[ai/rag-and-retrieval/grounding-and-citations|grounding]] prompt, fewer/better chunks |
| everything high, users unhappy | eval set unrepresentative | re-mine real queries |

## Failure modes

- **Judge grading its own homework** — using the same model family for generation and
  judging inflates scores; known self-preference bias. Use a different model or
  validate the judge against humans.
- **Eval set rot** — corpus and users evolve; an eval set frozen in Q1 measures a
  product that no longer exists. Refresh quarterly from logs.
- **Optimizing one number** — chasing faithfulness alone produces timid,
  refusal-heavy systems; track refusal rate on *answerable* questions alongside it.
- **No per-stage logging** — if you can't replay what was retrieved for a failing
  query, you can't attribute the failure; [[ai/rag-and-retrieval/rag-first-pass-design|log
  everything]] is a prerequisite, not an optimization.

**Connects to:** [[ai/evaluation/evaluating-rag-systems|evaluation branch view]] ·
[[ai/rag-and-retrieval/rag-failure-modes|failure modes]] ·
[[ai/foundations/evaluation-metrics|ranking metrics]] ·
[[ai/ai-playbooks/evaluate-rag-answer-quality|step-by-step playbook]]

## Sources

- [Es et al. 2023 — RAGAS (arXiv:2309.15217)](https://arxiv.org/abs/2309.15217) — the reference decomposition of RAG quality into faithfulness/relevance/context metrics.
- [RAGAS documentation](https://docs.ragas.io/) — current metric definitions and implementations (they've evolved past the paper).
- [Thakur et al. 2021 — BEIR (arXiv:2104.08663)](https://arxiv.org/abs/2104.08663) — how serious retrieval benchmarking is done; the nDCG@10 convention.
- [Hamel Husain — Your AI Product Needs Evals (2024)](https://hamel.dev/blog/posts/evals/) — the strongest practitioner case for log-mined eval sets and judge validation before automation.
- [Eugene Yan — Evaluating RAG and LLM-judges (2024)](https://eugeneyan.com/writing/llm-evaluators/) — survey of judge biases (self-preference, position, verbosity) with mitigations.
- [promptfoo docs](https://www.promptfoo.dev/docs/intro/) — CI-native eval harness that fits a TypeScript stack.
