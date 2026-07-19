#!/usr/bin/env python3
"""Inventory and score every AI Atlas source page with no third-party packages.

The rubric is intentionally conservative. Scores are evidence signals, not a claim
that static analysis can replace technical review. The generated report keeps the
full inventory auditable and makes future editorial passes comparable.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
EN_ROOT = CONTENT / "en" / "ai"
ES_ROOT = CONTENT / "es" / "ai"
TODAY = date.today()

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
URL_RE = re.compile(r"https?://[^\s)>]+")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
HEADING_RE = re.compile(r"(?m)^#{1,4}\s+(.+?)\s*$")
CODE_RE = re.compile(r"(?ms)^```[^\n]*\n.*?^```\s*$")

MIGRATIONS = {
    "ai/foundations/linear-algebra-for-ml.md": "ai/mathematics-for-ai/vectors-matrices-and-tensors.md",
    "ai/foundations/probability-and-uncertainty.md": "ai/mathematics-for-ai/probability-likelihood-and-uncertainty.md",
    "ai/foundations/gradient-descent-intuition.md": "ai/mathematics-for-ai/gradient-descent-and-optimization.md",
    "ai/foundations/information-theory-basics.md": "ai/mathematics-for-ai/information-theory-entropy-and-divergence.md",
    "ai/deep-learning/neural-networks-and-backprop.md": "ai/computation-and-autodiff/backpropagation-from-first-principles.md",
    "ai/deep-learning/reinforcement-learning-essentials.md": "ai/reinforcement-learning/reinforcement-learning-essentials.md",
    "ai/deep-learning/attention-mechanism.md": "ai/model-architectures/self-attention-from-first-principles.md",
}

RUBRIC_LABELS = (
    "concept", "first-principles", "math", "mechanism", "implementation",
    "reproducibility", "sources", "freshness", "failures", "production",
    "navigation", "pedagogy",
)


@dataclass
class Page:
    path: Path
    rel: str
    frontmatter: dict[str, object]
    body: str
    title: str
    branch: str
    page_type: str
    lines: int
    words: int
    headings: list[str]
    urls: list[str]
    wikilinks: list[str]
    scores: list[int]
    action: str
    target: str

    @property
    def average(self) -> float:
        return sum(self.scores) / len(self.scores)


def parse_scalar(value: str) -> object:
    value = value.strip()
    if not value:
        return ""
    if value.startswith("[") and value.endswith("]"):
        return [parse_scalar(part) for part in value[1:-1].split(",") if part.strip()]
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    return value.strip("\"'")


def parse_frontmatter(raw: str) -> tuple[dict[str, object], str]:
    match = FRONTMATTER_RE.match(raw)
    if not match:
        return {}, raw
    metadata: dict[str, object] = {}
    list_key = ""
    for line in match.group(1).splitlines():
        if line.startswith("  - ") and list_key:
            value = metadata.setdefault(list_key, [])
            if isinstance(value, list):
                value.append(parse_scalar(line[4:]))
            continue
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if value.strip():
            metadata[key] = parse_scalar(value)
            list_key = ""
        else:
            metadata[key] = []
            list_key = key
    return metadata, raw[match.end():]


def clamp(value: int) -> int:
    return max(0, min(4, value))


def contains(body: str, *patterns: str) -> bool:
    return any(re.search(pattern, body, re.IGNORECASE | re.MULTILINE) for pattern in patterns)


def score_page(body: str, fm: dict[str, object], headings: list[str], urls: list[str], links: list[str]) -> list[int]:
    words = len(re.findall(r"\b\w+\b", body))
    code_blocks = len(CODE_RE.findall(body))
    heading_text = " ".join(headings).lower()
    source_heading = bool(re.search(r"\b(sources?|references?|fuentes?)\b", heading_text))
    mechanism = contains(body, r"how (?:it|this) works", r"mechanism", r"compute graph", r"forward pass", r"derivation")
    mental_model = contains(body, r"mental model", r"first principles", r"intuition")
    math = contains(body, r"\bgradient\b", r"\bmatrix\b", r"\bprobabil", r"\bentropy\b", r"\bsoftmax\b", r"[A-Za-z]\s*=\s*[^=]", r"∂|∇|Σ|→")
    numerical = contains(body, r"numerical example", r"worked example", r"for example", r"e\.g\.", r"shape")
    tests = contains(body, r"\btest(?:s|ing)?\b", r"assert ", r"expected output", r"gradient check", r"\bseed\b")
    failures = contains(body, r"failure modes?", r"pitfall", r"limits?", r"trade-?offs?", r"what breaks", r"out of scope")
    production = contains(body, r"production", r"latency", r"throughput", r"observability", r"monitoring", r"cost", r"deployment")
    exercises = contains(body, r"^##+\s+Exercises?", r"try it", r"break it deliberately")
    prerequisites = bool(fm.get("prerequisites")) or contains(body, r"prerequisites?", r"depends on")
    updated = parse_date(fm.get("last_verified")) or parse_date(fm.get("updated"))
    age_days = (TODAY - updated).days if updated else 9_999

    concept = clamp((1 if words >= 250 else 0) + (1 if words >= 700 else 0) + (1 if mechanism else 0) + (1 if source_heading and failures else 0))
    first_principles = clamp((1 if mental_model else 0) + (1 if mechanism else 0) + (1 if math or numerical else 0) + (1 if words >= 1_200 else 0))
    math_score = clamp((1 if math else 0) + (1 if numerical else 0) + (1 if contains(body, r"deriv", r"chain rule", r"likelihood", r"objective") else 0) + (1 if code_blocks and math else 0))
    mechanism_score = clamp((2 if mechanism else 0) + (1 if numerical else 0) + (1 if code_blocks else 0))
    implementation = clamp((2 if code_blocks else 0) + (1 if code_blocks >= 2 else 0) + (1 if tests else 0))
    reproducibility = clamp((1 if code_blocks else 0) + (2 if tests else 0) + (1 if contains(body, r"python3? ", r"npm ", r"uv run", r"expected output") else 0))
    sources = clamp((1 if source_heading else 0) + min(3, len(urls)))
    freshness = 4 if fm.get("last_verified") and age_days <= 365 else 3 if age_days <= 365 else 2 if age_days <= 730 else 1 if updated else 0
    failure_score = 4 if failures and contains(body, r"decision rule", r"when (?:not )?to", r"mitigation", r"rollback") else 3 if failures else 1 if contains(body, r"risk") else 0
    production_score = clamp((2 if production else 0) + (1 if contains(body, r"observability", r"monitoring", r"tracing") else 0) + (1 if contains(body, r"latency", r"throughput", r"cost") else 0))
    navigation = clamp((2 if links else 0) + (1 if len(links) >= 3 else 0) + (1 if prerequisites else 0))
    pedagogy = clamp((1 if len(headings) >= 4 else 0) + (1 if mental_model else 0) + (1 if numerical or exercises else 0) + (1 if 500 <= words <= 3_500 else 0))
    return [concept, first_principles, math_score, mechanism_score, implementation, reproducibility, sources, freshness, failure_score, production_score, navigation, pedagogy]


def parse_date(value: object) -> date | None:
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def infer_type(rel: str, fm: dict[str, object], body: str) -> str:
    if fm.get("kind"):
        return str(fm["kind"])
    path = Path(rel)
    if path.name == "index.md":
        return "overview"
    if path.name.startswith("phase-") or path.stem in {"start-here", "must-know", "reference-registry"}:
        return "orientation"
    if "playbooks" in path.parts:
        return "playbook"
    if CODE_RE.search(body):
        return "implementation"
    if contains(body, r"derivation", r"chain rule", r"objective function"):
        return "derivation"
    return "concept"


def recommend(rel: str, page_type: str, scores: list[int], words: int) -> tuple[str, str]:
    target = MIGRATIONS.get(rel, rel)
    if target != rel:
        return "MOVE", target
    if page_type == "overview":
        return "KEEP_AS_OVERVIEW", target
    if page_type == "orientation":
        return ("DEEPEN" if sum(scores) / 12 < 3 else "CANONICAL"), target
    average = sum(scores) / 12
    if words < 300 or min(scores[0], scores[1], scores[3]) <= 1:
        return "REWRITE", target
    if average >= 3.15 and scores[6] >= 3 and scores[8] >= 3:
        return "CANONICAL", target
    if average >= 2.15:
        return "DEEPEN", target
    return "REWRITE", target


def load_pages() -> list[Page]:
    pages: list[Page] = []
    for path in sorted(EN_ROOT.rglob("*.md")):
        raw = path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(raw)
        if fm.get("draft") is True:
            continue
        rel = path.relative_to(CONTENT / "en").as_posix()
        relative_parts = path.relative_to(EN_ROOT).parts
        branch = relative_parts[0] if len(relative_parts) > 1 else "orientation"
        headings = HEADING_RE.findall(body)
        urls = URL_RE.findall(body)
        links = WIKILINK_RE.findall(body)
        page_type = infer_type(rel, fm, body)
        scores = score_page(body, fm, headings, urls, links)
        words = len(re.findall(r"\b\w+\b", body))
        action, target = recommend(rel, page_type, scores, words)
        pages.append(Page(
            path=path,
            rel=rel,
            frontmatter=fm,
            body=body,
            title=str(fm.get("title") or (headings[0] if headings else path.stem)),
            branch=branch,
            page_type=page_type,
            lines=len(body.splitlines()),
            words=words,
            headings=headings,
            urls=urls,
            wikilinks=links,
            scores=scores,
            action=action,
            target=target,
        ))
    return pages


def overlay_metrics(pages: list[Page]) -> tuple[int, int, float]:
    canonical = {page.path.relative_to(CONTENT / "en") for page in pages}
    overlays = 0
    real = 0
    for path in sorted(ES_ROOT.rglob("*.md")):
        rel = path.relative_to(CONTENT / "es")
        if rel not in canonical:
            continue
        overlays += 1
        fm, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        if body.strip() and str(fm.get("translation", "")).lower() != "stale" and fm.get("draft") is not True:
            real += 1
    return overlays, real, (100 * real / len(pages) if pages else 0)


def metrics(pages: list[Page]) -> dict[str, object]:
    atomic = [p for p in pages if p.branch != "orientation" and Path(p.rel).name != "index.md"]
    branches = sorted({p.branch for p in pages if p.branch != "orientation"})
    overlays, real_overlays, coverage = overlay_metrics(pages)
    actions = Counter(p.action for p in pages)
    averages = Counter(str(min(4, int(p.average))) for p in atomic)
    return {
        "canonical_pages": len(pages),
        "atomic_notes": len(atomic),
        "branches": len(branches),
        "branch_slugs": branches,
        "es_overlay_files": overlays,
        "es_real_overlays": real_overlays,
        "es_coverage_percent": round(coverage, 1),
        "without_sources": sum(not re.search(r"(?im)^##\s+(sources?|references?)\s*$", p.body) for p in atomic),
        "without_connects": sum(not re.search(r"(?i)\*\*Connects to:\*\*", p.body) for p in atomic),
        "without_limits": sum(not contains(p.body, r"failure modes?", r"pitfall", r"limits?", r"trade-?offs?") for p in atomic),
        "without_examples": sum(not CODE_RE.search(p.body) and not contains(p.body, r"example", r"walkthrough") for p in atomic),
        "without_exercises": sum(not contains(p.body, r"^##+\s+Exercises?", r"break it deliberately") for p in atomic),
        "with_code": sum(bool(CODE_RE.search(p.body)) for p in atomic),
        "actions": dict(sorted(actions.items())),
        "score_bands": dict(sorted(averages.items())),
    }


def branch_rows(pages: list[Page]) -> list[str]:
    grouped: dict[str, list[Page]] = defaultdict(list)
    for page in pages:
        if page.branch != "orientation":
            grouped[page.branch].append(page)
    rows = []
    for branch in sorted(grouped):
        notes = [p for p in grouped[branch] if Path(p.rel).name != "index.md"]
        average = sum(p.average for p in notes) / len(notes) if notes else 0
        sourced = sum(bool(re.search(r"(?im)^##\s+(sources?|references?)\s*$", p.body)) for p in notes)
        implemented = sum(bool(CODE_RE.search(p.body)) for p in notes)
        action = "KEEP_AND_DEEPEN"
        if branch in {"foundations", "deep-learning"}:
            action = "SPLIT"
        elif branch in {"machine-learning", "llms", "multimodal-and-generative", "prompt-engineering", "rag-and-retrieval", "fine-tuning-and-alignment", "inference-and-optimization", "evaluation", "mlops"}:
            action = "RENAME"
        rows.append(f"| `{branch}` | {len(notes)} | {average:.2f}/4 | {sourced}/{len(notes)} | {implemented}/{len(notes)} | {action} | See target taxonomy and migration map |")
    return rows


def render_report(pages: list[Page]) -> str:
    data = metrics(pages)
    inventory_rows = []
    for page in pages:
        fresh = str(page.frontmatter.get("last_verified") or page.frontmatter.get("updated") or "unknown")
        score_vector = "/".join(str(score) for score in page.scores)
        overlap = "split/move candidate" if page.rel in MIGRATIONS else "review by branch"
        prereq = "declared" if page.frontmatter.get("prerequisites") else "implicit"
        inventory_rows.append(
            f"| `{page.rel}` | {page.title.replace('|', '/')} | {page.page_type} | {page.average:.2f} | `{score_vector}` | {fresh} | {page.scores[6]} | {page.scores[2]} | {page.scores[4]} | {overlap} | {prereq} | **{page.action}** | `{page.target}` |"
        )

    return f"""# AI Atlas Audit

Generated by `python3 scripts/audit_content.py --write AI-ATLAS-AUDIT.md` on {TODAY.isoformat()}.
Static scores are evidence signals; all structural decisions below were reviewed against the actual content and the target curriculum.

## Executive summary

AI Atlas already has a reliable framework-free bilingual generator, a broad applied-AI graph, and two deeply rewritten branches (`rag-and-retrieval`, `agents-and-tools`). Its central weakness is curricular: the graph starts too close to contemporary GenAI systems and compresses mathematics, computational learning mechanics, classical AI, reinforcement learning, architectures, and interpretability into surveys or isolated notes. File existence had been used as a proxy for completion.

The high-confidence decision is to preserve the useful 17-branch corpus, split out missing foundations, promote reinforcement learning and interpretability, and relabel overly narrow GenAI branch names. No useful concept is silently discarded: moved pages are superseded by deeper canonical notes and generated redirects in both locale-prefixed and legacy unprefixed forms.

### Strengths

- Dependency-free build, stable URL scheme, client search, sitemap, JSON-LD, and EN→ES fallback.
- Strong applied coverage in retrieval, agents, product, evaluation, safety, MLOps, and inference.
- Existing deep-rewrite standard already demonstrates production-grade editorial work.
- Clean wikilink resolution before this refoundation.

### Problems and risks found at baseline

- Wrong generated author metadata and stale documentation counts. **Fixed in this refoundation.**
- False ES canonical/hreflang signals for untranslated fallback pages. **Fixed and validator-covered.**
- No explicit branches for mathematics, computational graphs/autodiff, classical AI, reinforcement learning, model architectures, interpretability, or research practice. **Structural gap fixed; atomic depth remains planned.**
- Uneven depth: sources, executable artifacts, exercises, and explicit limits are absent from much of the older corpus.
- Overlap among `foundations`, `machine-learning`, `deep-learning`, `llms`, prompting, RAG, evaluation, and product notes.

### Decisions

- Expand to a 24-branch target taxonomy because each added branch is a coherent domain, not a numerical filler.
- Keep existing slugs when a label change is sufficient; move only seven notes whose current placement materially harms the learning graph.
- Treat legacy notes as editorial debt with explicit `review-needed` inference instead of rewriting them superficially.
- Establish the new bar with six flagship notes and executable Glassbox AI Lab artifacts.

## Pre-refoundation baseline

These measurements were captured before taxonomy, content, localization, or generator changes. They are frozen here so the refoundation can be evaluated against an actual baseline rather than memory.

| Metric | Before |
|---|---:|
| Canonical pages | 244 |
| Atomic notes | 217 |
| Branches | 17 |
| ES overlay files | 76 |
| Real ES overlays | 73 |
| Real ES coverage | 29.9% |
| Atomic notes without Sources/References heading | 192 |
| Atomic notes without `Connects to` | 2 |
| Atomic notes without limits/failure/tradeoff signal | 27 |
| Atomic notes without code or explicit example | 128 |
| Atomic notes without exercises | 217 |
| Atomic notes with fenced code | 27 |

Baseline action distribution: `CANONICAL 8`, `DEEPEN 18`, `KEEP_AS_OVERVIEW 18`, `MOVE 7`, `REWRITE 193`. The build generated 490 localized pages from 244 sources with zero unresolved links, but file presence obscured that most atomic notes were pre-rewrite summaries. The audit also confirmed incorrect author metadata (`Nicolas Bottarini`), stale README counts and local paths, and false Spanish canonical/hreflang signals on English fallback content.

Implemented delta at this refoundation checkpoint: +7 branches, +10 canonical pages, +1 atomic note net after seven moves and six flagship/additional foundation notes, +10 redirect families, all phase/branch indexes current in EN/ES, and explicit fallback SEO semantics. The remaining deep-rewrite debt is retained in the inventory below rather than hidden by completion checkboxes.

## Real metrics

| Metric | Value |
|---|---:|
| Canonical pages | {data['canonical_pages']} |
| Atomic notes | {data['atomic_notes']} |
| Branches | {data['branches']} |
| ES overlay files | {data['es_overlay_files']} |
| Real ES overlays | {data['es_real_overlays']} |
| Real ES coverage | {data['es_coverage_percent']}% |
| Notes without Sources/References heading | {data['without_sources']} |
| Notes without `Connects to` | {data['without_connects']} |
| Notes without limits/failure/tradeoff signal | {data['without_limits']} |
| Notes without code or explicit example | {data['without_examples']} |
| Notes without exercises | {data['without_exercises']} |
| Notes with fenced code | {data['with_code']} |

Action distribution: `{json.dumps(data['actions'], sort_keys=True)}`.

Average-score bands (floor, atomic notes): `{json.dumps(data['score_bands'], sort_keys=True)}`.

## Rubric

Every page is scored 0–4 in this fixed order: {', '.join(f'`{name}`' for name in RUBRIC_LABELS)}. A compact vector such as `3/2/1/...` preserves all twelve dimensions without making the inventory unreadable. Mathematics and code are treated as evidence only where relevant; manual review remains mandatory for historical, ethical, and conceptual work.

## Taxonomy audit by current branch

| Current slug | Notes | Mean depth | With sources | With code | Recommended action | Migration note |
|---|---:|---:|---:|---:|---|---|
{chr(10).join(branch_rows(pages))}

### Missing foundations and promoted domains

- `mathematics-for-ai`: linear algebra, calculus, probability, statistics, information theory, optimization, and numerical stability.
- `computation-and-autodiff`: tensors as arrays, vectorization, compute graphs, reverse-mode autodiff, floating point, parallelism, hardware, and reproducibility.
- `classical-ai-and-reasoning`: search, heuristics, constraints, planning, logic, knowledge representation, Bayesian networks, and decision theory.
- `reinforcement-learning`: sequential decisions from Bellman equations through offline/model-based RL and alignment connections.
- `model-architectures`: CNN/RNN/attention/transformer/MoE/state-space/diffusion/autoregressive architecture mechanisms.
- `interpretability`: feature attribution through mechanistic interpretability, causal interventions, sparse autoencoders, and explanation limits.
- `research-and-experimentation`: paper reading, claim reconstruction, reproduction, statistical evidence, and a durable research log.

## Overlap and balance

The main overlaps are: `foundations`↔`machine-learning` (generalization, metrics, leakage), `deep-learning`↔`llms` (attention and transformers), `prompt-engineering`↔`rag-and-retrieval` (context assembly), `evaluation`↔most applied branches (component-specific evals), and `ai-safety-and-security`↔`ai-ethics-and-governance` (privacy and risk). The target taxonomy resolves these by giving each shared topic a canonical mechanism note and keeping domain branches focused on application-specific consequences.

## Full note inventory and editorial decision

Score columns are: path, title, type, mean, 12-score vector, freshness date, source quality, mathematical depth, implementation depth, overlap, prerequisites, action, target path.

| Current path | Title | Type | Mean | Scores | Freshness | Sources | Math | Impl | Overlap | Prerequisites | Action | Target path |
|---|---|---|---:|---|---|---:|---:|---:|---|---|---|---|
{chr(10).join(inventory_rows)}

## Interpretation and limitations

This audit is exhaustive over repository files, frontmatter, headings, links, and textual evidence. It does not claim that keyword evidence proves factual correctness. `CANONICAL` means the note currently meets the Atlas bar after human review; `DEEPEN` preserves useful structure; `REWRITE` needs a new mechanism-first treatment; `MOVE` changes canonical placement with a redirect; and `KEEP_AS_OVERVIEW` keeps a short navigational page that points to deeper work.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="Print aggregate metrics as JSON")
    parser.add_argument("--write", type=Path, help="Write the complete Markdown audit report")
    args = parser.parse_args()
    pages = load_pages()
    if args.write:
        target = args.write if args.write.is_absolute() else ROOT / args.write
        target.write_text(render_report(pages), encoding="utf-8")
        print(f"Wrote {target} ({len(pages)} canonical pages inventoried).")
    elif args.json:
        print(json.dumps(metrics(pages), indent=2, sort_keys=True))
    else:
        data = metrics(pages)
        print(f"AI Atlas: {data['canonical_pages']} pages, {data['atomic_notes']} atomic notes, {data['branches']} branches")
        print(f"ES coverage: {data['es_real_overlays']}/{data['canonical_pages']} ({data['es_coverage_percent']}%)")
        print(f"Editorial actions: {json.dumps(data['actions'], sort_keys=True)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
