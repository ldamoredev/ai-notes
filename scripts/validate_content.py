#!/usr/bin/env python3
"""Validate source structure, editorial contracts, and migration invariants."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import build  # noqa: E402
from scripts.audit_content import parse_frontmatter  # noqa: E402

EN = ROOT / "content" / "en" / "ai"
ES = ROOT / "content" / "es" / "ai"
REQUIRED_FRONTMATTER = {"title", "description", "tags", "order", "updated"}
INDEX_SIGNALS = {
    "mental model": re.compile(r"(?im)^##\s+(?:the\s+)?(?:mental model|modelo mental)\b"),
    "roadmap": re.compile(r"(?im)^##\s+.*(?:roadmap|hoja de ruta)\b"),
    "connections": re.compile(r"(?i)\*\*(?:connects to|conecta con):\*\*"),
    "sources": re.compile(r"(?im)^##\s+(?:core sources|sources|fuentes principales)\b"),
}
FLAGSHIPS = (
    "mathematics-for-ai/vectors-matrices-and-tensors.md",
    "mathematics-for-ai/probability-likelihood-and-uncertainty.md",
    "mathematics-for-ai/gradient-descent-and-optimization.md",
    "computation-and-autodiff/backpropagation-from-first-principles.md",
    "model-architectures/self-attention-from-first-principles.md",
    "llms/from-prompt-to-generated-token.md",
)


def published(path: Path) -> tuple[dict[str, object], str]:
    return parse_frontmatter(path.read_text(encoding="utf-8"))


def validate_index(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing required index: {path.relative_to(ROOT)}")
        return
    fm, body = published(path)
    if str(fm.get("translation", "")).lower() == "stale" or fm.get("draft") is True:
        errors.append(f"{path.relative_to(ROOT)}: phase/index overlays must be current")
    for label, pattern in INDEX_SIGNALS.items():
        if not pattern.search(body):
            errors.append(f"{path.relative_to(ROOT)}: missing {label} section/signal")
    if len(re.findall(r"https?://", body)) < 3:
        errors.append(f"{path.relative_to(ROOT)}: needs at least 3 full source URLs")
    if len(re.findall(r"\[\[[^\]]+\]\]", body)) < 2:
        errors.append(f"{path.relative_to(ROOT)}: needs at least 2 internal wikilinks")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if len(build.BRANCHES) != 24:
        errors.append(f"taxonomy must have 24 branches, found {len(build.BRANCHES)}")
    if len(build.PHASES) != 8:
        errors.append(f"taxonomy must have 8 phases, found {len(build.PHASES)}")
    if set(build.BRANCHES_ES) != set(build.BRANCHES):
        errors.append("BRANCHES_ES keys must exactly match BRANCHES")

    actual_branches = {path.parent.name for path in EN.glob("*/index.md")}
    expected_branches = set(build.BRANCHES)
    if actual_branches != expected_branches:
        errors.append(
            f"branch index drift: missing={sorted(expected_branches - actual_branches)}, "
            f"extra={sorted(actual_branches - expected_branches)}"
        )

    for branch in sorted(expected_branches):
        validate_index(EN / branch / "index.md", errors)
        validate_index(ES / branch / "index.md", errors)

    phase_paths = [Path(str(phase["href"]).replace(".html", ".md")).name for phase in build.PHASES]
    for filename in phase_paths:
        validate_index(EN / filename, errors)
        validate_index(ES / filename, errors)

    canonical_paths = sorted(EN.rglob("*.md"))
    for path in canonical_paths:
        fm, body = published(path)
        missing = REQUIRED_FRONTMATTER - set(fm)
        if missing:
            errors.append(f"{path.relative_to(ROOT)}: missing frontmatter {sorted(missing)}")
        if fm.get("draft") is True:
            continue
        if not re.search(r"(?m)^#\s+\S", body):
            errors.append(f"{path.relative_to(ROOT)}: missing H1")

    for rel in FLAGSHIPS:
        path = EN / rel
        if not path.exists():
            errors.append(f"missing flagship: {path.relative_to(ROOT)}")
            continue
        fm, body = published(path)
        for key in ("kind", "level", "status", "prerequisites", "last_verified"):
            if key not in fm or (key != "prerequisites" and not fm.get(key)):
                errors.append(f"{path.relative_to(ROOT)}: flagship missing {key}")
        words = len(re.findall(r"\b\w+\b", body))
        if words < 700:
            errors.append(f"{path.relative_to(ROOT)}: flagship too thin ({words} words)")
        for signal in (r"(?im)^##\s+Exercises\b", r"(?im)^##\s+Sources\b", r"(?i)failure modes?", r"(?i)production lens"):
            if not re.search(signal, body):
                errors.append(f"{path.relative_to(ROOT)}: missing flagship signal {signal}")
        if "```" not in body or not re.search(r"(?m)^```(?:bash|python|typescript|ts)", body):
            errors.append(f"{path.relative_to(ROOT)}: needs an executable artifact")

    canonical_ids = {path.relative_to(ROOT / "content" / "en").with_suffix("").as_posix() for path in canonical_paths}
    for legacy, target in build.LEGACY_REDIRECTS.items():
        if target not in canonical_ids:
            errors.append(f"redirect target missing: {legacy} -> {target}")
        if (ROOT / "content" / "en" / f"{legacy}.md").exists():
            errors.append(f"legacy source still exists instead of redirect: {legacy}")

    for path in sorted(ES.rglob("*.md")):
        rel = path.relative_to(ES)
        if not (EN / rel).exists():
            errors.append(f"orphan ES overlay: {path.relative_to(ROOT)}")

    residual_scan = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in (ROOT / "build.py", ROOT / "README.md") if path.exists()
    )
    if "Nicolas Bottarini" in residual_scan:
        errors.append("residual incorrect author identity: Nicolas Bottarini")

    atomic = [path for path in canonical_paths if len(path.relative_to(EN).parts) == 2 and path.name != "index.md"]
    source_backed = sum(bool(re.search(r"(?im)^##\s+Sources\s*$", published(path)[1])) for path in atomic)
    if source_backed < len(FLAGSHIPS):
        errors.append("source-backed atomic-note count is lower than the flagship set")
    if source_backed < len(atomic) // 2:
        warnings.append(
            f"deep rewrite debt remains: {source_backed}/{len(atomic)} atomic notes have a Sources section"
        )

    for warning in warnings:
        print(f"[warn] {warning}")
    if errors:
        for error in errors:
            print(f"[error] {error}", file=sys.stderr)
        print(f"Content validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(
        f"Validated {len(canonical_paths)} canonical pages, {len(actual_branches)} bilingual branch indexes, "
        f"{len(phase_paths)} bilingual phases, {len(FLAGSHIPS)} flagships, and {len(build.LEGACY_REDIRECTS)} redirects."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
