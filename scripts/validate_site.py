#!/usr/bin/env python3
"""Validate generated HTML, local links, localization SEO, assets, and redirects."""
from __future__ import annotations

import json
import re
import struct
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import build  # noqa: E402
from scripts.audit_content import parse_frontmatter  # noqa: E402

SITE = ROOT / "site"
CONTENT = ROOT / "content"
LOCALES = build.LOCALES


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.html_lang = ""
        self.body: dict[str, str] = {}
        self.ids: set[str] = set()
        self.refs: list[str] = []
        self.canonicals: list[str] = []
        self.alternates: dict[str, str] = {}
        self.meta: dict[str, list[str]] = {}
        self.classes: set[str] = set()
        self.title_parts: list[str] = []
        self._in_title = False

    def handle_starttag(self, tag: str, attrs_raw: list[tuple[str, str | None]]) -> None:
        attrs = {key: value or "" for key, value in attrs_raw}
        if tag == "html":
            self.html_lang = attrs.get("lang", "")
        if tag == "body":
            self.body = attrs
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        self.classes.update(attrs.get("class", "").split())
        for attr in ("href", "src"):
            if attrs.get(attr):
                self.refs.append(attrs[attr])
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonicals.append(attrs.get("href", ""))
        if tag == "link" and attrs.get("rel") == "alternate" and attrs.get("hreflang"):
            self.alternates[attrs["hreflang"]] = attrs.get("href", "")
        if tag == "meta":
            key = attrs.get("name") or attrs.get("property")
            if key:
                self.meta.setdefault(key, []).append(attrs.get("content", ""))
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)

    @property
    def title(self) -> str:
        return "".join(self.title_parts).strip()


def real_overlay(path: Path) -> bool:
    fm, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    return bool(body.strip()) and fm.get("draft") is not True and str(fm.get("translation", "")).lower() != "stale"


def parse_html(path: Path) -> DocumentParser:
    parser = DocumentParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def local_target(source: Path, value: str) -> tuple[Path | None, str]:
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or value.startswith(("mailto:", "data:", "javascript:")):
        return None, ""
    raw_path = unquote(parsed.path)
    if not raw_path:
        return source, unquote(parsed.fragment)
    target = SITE / raw_path.lstrip("/") if raw_path.startswith("/") else source.parent / raw_path
    target = target.resolve()
    try:
        target.relative_to(SITE.resolve())
    except ValueError:
        return Path("/__outside_site__"), ""
    if raw_path.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target, unquote(parsed.fragment)


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    if len(data) != 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return 0, 0
    return struct.unpack(">II", data[16:24])


def main() -> int:
    errors: list[str] = []
    required = (
        "index.html", "robots.txt", "sitemap.xml", "site.webmanifest", ".nojekyll",
        "favicon.svg", "apple-touch-icon.png", "assets/atlas.css", "assets/search.js",
        "assets/icon-192.png", "assets/icon-512.png", "assets/og-image.svg",
        "assets/og-image.png", "en/index.html", "es/index.html", "en/search.json", "es/search.json",
    )
    for rel in required:
        if not (SITE / rel).exists():
            errors.append(f"missing generated artifact: site/{rel}")
    if errors:
        for error in errors:
            print(f"[error] {error}", file=sys.stderr)
        return 1

    canonical = []
    for path in sorted((CONTENT / "en" / build.SECTION).rglob("*.md")):
        fm, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        if fm.get("draft") is not True:
            canonical.append(path)
    canonical_rel = {path.relative_to(CONTENT / "en") for path in canonical}
    overlay_rel = {
        path.relative_to(CONTENT / "es")
        for path in sorted((CONTENT / "es" / build.SECTION).rglob("*.md"))
        if real_overlay(path) and path.relative_to(CONTENT / "es") in canonical_rel
    }

    html_paths = sorted(SITE.rglob("*.html"))
    docs = {path.resolve(): parse_html(path) for path in html_paths}
    for path, doc in docs.items():
        rel = path.relative_to(SITE.resolve()).as_posix()
        if not doc.html_lang:
            errors.append(f"{rel}: missing html lang")
        if not doc.title:
            errors.append(f"{rel}: missing title")
        if "unresolved-link" in doc.classes:
            errors.append(f"{rel}: contains unresolved-link")
        if len(doc.canonicals) != 1:
            errors.append(f"{rel}: expected one canonical, found {len(doc.canonicals)}")
        for value in doc.refs:
            if ".md" in urlsplit(value).path and not urlsplit(value).scheme:
                errors.append(f"{rel}: generated link still targets Markdown: {value}")
            target, fragment = local_target(path, value)
            if target is None:
                continue
            if not target.exists():
                errors.append(f"{rel}: missing local target for {value}")
            elif fragment and target.suffix == ".html":
                target_doc = docs.get(target.resolve())
                if target_doc and fragment not in target_doc.ids:
                    errors.append(f"{rel}: missing fragment #{fragment} in {target.relative_to(SITE)}")

        parts = Path(rel).parts
        if not parts or parts[0] not in LOCALES or not rel.endswith(".html"):
            continue
        locale = parts[0]
        is_home = rel == f"{locale}/index.html"
        content_rel = Path(*parts[1:]).with_suffix(".md") if not is_home else None
        is_content = is_home or content_rel in canonical_rel
        if not is_content:  # locale-prefixed legacy redirect
            continue
        translated = is_home or locale == "en" or content_rel in overlay_rel
        if locale == "es" and not translated:
            if doc.html_lang != "en" or doc.body.get("data-content-locale") != "en":
                errors.append(f"{rel}: fallback must declare English content")
            if doc.body.get("data-locale") != "es":
                errors.append(f"{rel}: fallback must preserve Spanish UI locale")
            if doc.meta.get("robots") != ["noindex, follow"]:
                errors.append(f"{rel}: fallback must be noindex, follow")
            if "translation-pending" not in doc.classes:
                errors.append(f"{rel}: fallback notice is missing")
            if "es" in doc.alternates:
                errors.append(f"{rel}: fallback must not advertise false ES hreflang")
            expected = f"{build.SITE_URL}/en/{'/'.join(parts[1:])}"
        else:
            if doc.html_lang != locale or doc.body.get("data-content-locale") != locale:
                errors.append(f"{rel}: native locale metadata is inconsistent")
            if doc.meta.get("robots", [""])[0].startswith("noindex"):
                errors.append(f"{rel}: native page must be indexable")
            expected = f"{build.SITE_URL}/{locale}/" if is_home else f"{build.SITE_URL}/{rel}"
        if doc.canonicals and doc.canonicals[0] != expected:
            errors.append(f"{rel}: canonical mismatch ({doc.canonicals[0]} != {expected})")

    for locale in LOCALES:
        entries = json.loads((SITE / locale / "search.json").read_text(encoding="utf-8"))
        if len(entries) != len(canonical):
            errors.append(f"{locale}/search.json: expected {len(canonical)} entries, found {len(entries)}")
        required_fields = {"title", "url", "branch", "group", "kind", "description", "text", "content_language", "translation_status", "level", "status"}
        for index, entry in enumerate(entries):
            missing = required_fields - set(entry)
            if missing:
                errors.append(f"{locale}/search.json[{index}]: missing {sorted(missing)}")
        fallback_count = sum(entry.get("translation_status") == "fallback" for entry in entries)
        expected_fallback = 0 if locale == "en" else len(canonical) - len(overlay_rel)
        if fallback_count != expected_fallback:
            errors.append(f"{locale}/search.json: expected {expected_fallback} fallbacks, found {fallback_count}")

    for locale in LOCALES:
        home = docs[(SITE / locale / "index.html").resolve()]
        if "glassbox-computation-map" not in home.classes:
            errors.append(f"{locale}/index.html: missing Glassbox computation map")

    for legacy, canonical_id in build.LEGACY_REDIRECTS.items():
        for locale in LOCALES:
            path = SITE / locale / f"{legacy}.html"
            expected = f"{build.SITE_URL}/{locale}/{canonical_id}.html"
            if not path.exists() or parse_html(path).canonicals != [expected]:
                errors.append(f"missing or incorrect redirect: {locale}/{legacy}.html")

    manifest = json.loads((SITE / "site.webmanifest").read_text(encoding="utf-8"))
    if manifest.get("theme_color") != build.THEME_COLOR:
        errors.append("site.webmanifest: theme color mismatch")
    if any("maskable" in icon.get("purpose", "") for icon in manifest.get("icons", [])):
        errors.append("site.webmanifest: maskable purpose claimed without a dedicated safe-area asset")
    for rel, expected in {
        "apple-touch-icon.png": (180, 180),
        "assets/icon-192.png": (192, 192),
        "assets/icon-512.png": (512, 512),
        "assets/og-image.png": (1200, 630),
    }.items():
        if png_dimensions(SITE / rel) != expected:
            errors.append(f"site/{rel}: invalid PNG dimensions")

    sitemap_root = ET.parse(SITE / "sitemap.xml").getroot()
    urls = [node.text or "" for node in sitemap_root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    expected_urls = 1 + len(LOCALES) + len(canonical) + len(overlay_rel)
    if len(urls) != expected_urls or len(urls) != len(set(urls)):
        errors.append(f"sitemap.xml: expected {expected_urls} unique URLs, found {len(urls)}")

    css = (SITE / "assets" / "atlas.css").read_text(encoding="utf-8")
    for color in ("#08111D", "#101B2A", "#172438", "#E8EEF7", "#94A3B8", "#31C7D9", "#6878FF", "#A678FF", "#4FA7FF", "#F2B84B", "#3DDC97", "#EF7896", "#F0646E", "#F4F7FB", "#182232", "#627084"):
        if color.lower() not in css.lower():
            errors.append(f"atlas.css: required palette color absent: {color}")

    generated = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in html_paths)
    if "Nicolas Bottarini" in generated:
        errors.append("generated HTML contains incorrect author identity")

    if errors:
        for error in errors:
            print(f"[error] {error}", file=sys.stderr)
        print(f"Site validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(
        f"Validated {len(html_paths)} HTML files, {len(canonical)} canonical pages, "
        f"{len(overlay_rel)} ES overlays, {len(canonical) - len(overlay_rel)} explicit fallbacks, "
        f"{len(build.LEGACY_REDIRECTS)} redirect families, all local links, SEO, and assets."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
