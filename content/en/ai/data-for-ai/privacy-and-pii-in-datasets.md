---
title: "Privacy and PII in datasets"
description: A dataset's privacy risk lives in quasi-identifier combinations and every derived copy, not just in fields tagged PII; k-anonymity and differential privacy make that measurable.
tags: [data-for-ai, privacy, pii, governance]
order: 10
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/data-for-ai/data-quality-dimensions]
last_verified: 2026-07-20
---
# Privacy and PII in datasets

**Mental model:** a dataset is a leakage surface, and the surface is larger than the
fields you labeled "PII." Direct identifiers are the obvious part; quasi-identifiers —
attributes that are individually harmless but jointly unique — and every derived copy
(embeddings, caches, fine-tuning exports, eval logs) extend the surface. Privacy
engineering bounds that whole surface, not one file.

## Mechanism: quasi-identifiers and k-anonymity

Split attributes into three classes: **direct identifiers** (name, email, SSN — remove
or hash these), **quasi-identifiers** (zip code, birth date, gender — individually
common, jointly rare), and **sensitive attributes** (diagnosis, salary, behavior — what
an attacker wants to learn). Latanya Sweeney's classic result: zip code, birth date, and
gender alone uniquely identify the large majority of the US population, even with no
direct identifier present.

A release is **k-anonymous** on a set of quasi-identifier columns if every combination
of values in that release is shared by at least \(k\) records. Formally, group records
by their quasi-identifier tuple; \(k\) is the size of the smallest group:

\[
k = \min_{g \in \text{groups}} |g|.
\]

\(k = 1\) means at least one record is uniquely identifiable by its quasi-identifiers
alone — an attacker with any one external record sharing that combination
(a voter roll, a hospital discharge list) re-identifies it directly, without ever
touching a direct identifier.

## Worked example

Eight records with quasi-identifiers `(zip3, age_bucket, gender)`:

| id | zip3 | age | gender |
|---:|---|---|---|
| 1 | 100 | 20s | M |
| 2 | 100 | 20s | M |
| 3 | 100 | 30s | F |
| 4 | 200 | 20s | F |
| 5 | 200 | 20s | F |
| 6 | 200 | 20s | F |
| 7 | 300 | 40s | M |
| 8 | 100 | 20s | M |

Grouping by `(zip3, age, gender)`: `(100,20s,M)` has 3 members `{1,2,8}`;
`(200,20s,F)` has 3 members `{4,5,6}`; but `(100,30s,F)` has only `{3}` and
`(300,40s,M)` has only `{7}`. So \(k = 1\): records 3 and 7 are uniquely identifiable
even though no name or email ever appeared in the table.

## Mechanism: differential privacy as a budget

k-anonymity describes a static release; **differential privacy** (DP) bounds what an
*algorithm* can reveal. A mechanism \(M\) is \(\varepsilon\)-differentially private if
for any two datasets \(D, D'\) differing in exactly one record, and any output set
\(S\):

\[
\Pr[M(D) \in S] \le e^{\varepsilon} \cdot \Pr[M(D') \in S].
\]

Smaller \(\varepsilon\) means the output distribution barely changes whether or not any
one individual's record is included — stronger privacy, more noise. The **Laplace
mechanism** answers a numeric query \(f\) by adding noise drawn from a Laplace
distribution scaled to the query's sensitivity \(\Delta f\) (how much one record can
change the true answer):

\[
M(D) = f(D) + \text{Laplace}\left(0, \frac{\Delta f}{\varepsilon}\right).
\]

For a count query, \(\Delta f = 1\) (one record can change a count by at most 1), so
the noise scale is simply \(1/\varepsilon\) — and the expected absolute noise equals
that scale exactly, which is what makes the epsilon-to-noise tradeoff so direct.

## Executable artifact

Run with `python3`; expected output is `1 [3, 7]` then the three scale rows
`0.1 10.0`, `1.0 1.0`, `2.0 0.5`:

```python
def min_k_anonymity(records, quasi_id_cols):
    groups = {}
    for r in records:
        key = tuple(r[c] for c in quasi_id_cols)
        groups.setdefault(key, []).append(r["id"])
    k = min(len(ids) for ids in groups.values())
    singletons = [ids[0] for ids in groups.values() if len(ids) == 1]
    return k, singletons

def laplace_scale(sensitivity, epsilon):
    return sensitivity / epsilon

records = [
    {"id": 1, "zip3": "100", "age": "20s", "gender": "M"},
    {"id": 2, "zip3": "100", "age": "20s", "gender": "M"},
    {"id": 3, "zip3": "100", "age": "30s", "gender": "F"},
    {"id": 4, "zip3": "200", "age": "20s", "gender": "F"},
    {"id": 5, "zip3": "200", "age": "20s", "gender": "F"},
    {"id": 6, "zip3": "200", "age": "20s", "gender": "F"},
    {"id": 7, "zip3": "300", "age": "40s", "gender": "M"},
    {"id": 8, "zip3": "100", "age": "20s", "gender": "M"},
]

k, singletons = min_k_anonymity(records, ["zip3", "age", "gender"])
print(k, singletons)
for eps in (0.1, 1.0, 2.0):
    print(eps, laplace_scale(1.0, eps))
```

Records 3 and 7 are exactly the two the analysis above found by hand. The scale row
shows the tradeoff mechanically: tightening \(\varepsilon\) from 2.0 to 0.1 multiplies
expected noise by 20x.

## What "PII scrubbers" hide

NER-based redaction tools (Presidio and similar) find direct identifiers reliably but
have no notion of quasi-identifier combinations — a scrubbed table can still be
1-anonymous. They also stop at the source file: embeddings, vector-index caches,
fine-tuning exports, and eval logs derived from that table inherit its risk but are
rarely covered by the same scrubbing pass, and a raw record can be partially recovered
from an embedding through inversion or [[ai/ai-safety-and-security/data-and-pii-leakage|membership
inference]].

## Failure modes and a decision rule

- **Linkage attacks.** "Anonymized" release + one public auxiliary dataset sharing
  quasi-identifiers re-identifies records — this is exactly how the Netflix Prize
  dataset and AOL search logs were de-anonymized despite having no names attached.
- **Aggregation hides minority slices.** Aggregating to protect privacy can erase the
  exact minority group a fairness or safety audit needed to see.
- **Synthetic data as a false escape hatch.** Generating synthetic records from a
  private seed set does not remove risk if the generator memorized and can reproduce
  seed examples — see [[ai/data-for-ai/synthetic-data|synthetic data]].
- **Derived-artifact blind spot.** Treating "we only store embeddings" as automatically
  safe, when the embedding model can be inverted or probed for membership.

**Decision rule:** if any quasi-identifier group has \(k < 5\) (a common regulatory
floor), the release needs generalization, suppression, or a DP mechanism before it
leaves the source system — and every derived artifact (embedding index, fine-tuning
export, eval cache) inherits the access tier of the source data unless it has its own
verified k-anonymity or DP guarantee.

## Production lens

Track retention windows and who can access raw (non-aggregated) records with audit
logging. Treat a differential-privacy epsilon as a spendable budget across queries —
each released statistic consumes some of it, and composition means many small queries
can add up to a large effective epsilon. Classify PII appearing in model *outputs* as
an incident distinct from PII appearing in training *inputs*; see
[[ai/ai-safety-and-security/data-and-pii-leakage|data and PII leakage]] for the
output-side taxonomy.

## Exercises

1. Add a ninth record to the table above that raises `k` to 2 for every group, and
   verify with the script.
2. For a sum query with sensitivity 50 (e.g., total dollars in a transaction table
   where one record can be at most $50), compute the Laplace scale at
   \(\varepsilon = 0.5\) and at \(\varepsilon = 5\).
3. List every place a single customer record could still exist 30 days after a
   "delete my data" request in a system with embeddings, a fine-tuning export, and a
   nightly analytics warehouse copy.

**Connects to:** [[ai/ai-safety-and-security/privacy-and-data-governance|privacy governance]] · [[ai/ai-safety-and-security/data-and-pii-leakage|data and PII leakage]] · [[ai/rag-and-retrieval/vector-databases-and-indexes|vector indexes]] · [[ai/data-for-ai/synthetic-data|synthetic data]]

## Sources

- [k-Anonymity: A Model for Protecting Privacy](https://www.hks.harvard.edu/publications/k-anonymity-model-protecting-privacy) — Sweeney's original formulation and the zip+birthdate+gender re-identification result.
- [The Algorithmic Foundations of Differential Privacy](https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf) — Dwork & Roth's complete formal treatment of DP, mechanisms, and composition.
- [Robust De-anonymization of Large Sparse Datasets](https://www.cs.cornell.edu/~shmat/shmat_oak08netflix.pdf) — Narayanan & Shmatikov's de-anonymization of the Netflix Prize dataset via linkage.
- [Membership Inference Attacks against Machine Learning Models](https://arxiv.org/abs/1610.05820) — shows trained models leak whether a specific record was in the training set.
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) — governance vocabulary for data risk across the AI lifecycle.
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) — sensitive information disclosure as an application-level risk category.
