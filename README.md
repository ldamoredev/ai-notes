# AI Atlas

Static personal knowledge atlas for Artificial Intelligence notes.

This project mirrors the architectural idea of the existing CyberSec Atlas: a
small Python build script, local Markdown sources, bilingual output, sticky
sidebar/topbar, client-side search, SEO metadata, sitemap, robots, and static
assets. It uses a different visual identity: sober AI-console styling with
cyan, indigo, violet, and neutral knowledge-tool surfaces.

## Structure

```text
build.py                       # Static site generator
content/en/ai/                 # Canonical English Markdown notes
content/es/ai/                 # Spanish overlays with matching paths
static/favicon.svg             # Shared favicon (SVG source)
static/apple-touch-icon.png    # iOS home-screen icon (generated)
static/assets/atlas.css        # Design system and responsive layout
static/assets/search.js        # Theme, drawer, language memory, client search
static/assets/og-image.svg     # Social card source
static/assets/og-image.png     # Social card raster (generated, 1200x630)
static/assets/icon-192.png     # PWA icon (generated)
static/assets/icon-512.png     # PWA icon (generated, also maskable)
scripts/rasterize-brand-assets.sh   # SVG -> PNG generator
.github/workflows/deploy.yml   # GitHub Pages CI (build + deploy)
site/                          # Generated output
```

Generated pages are written to:

```text
site/en/
site/es/
```

The root `site/index.html` is a small language chooser that redirects to the
stored or browser-preferred locale.

## Build

No framework is required. The build works with the Python standard library.
If the optional `markdown` package is installed, `build.py` will use it;
otherwise it falls back to a compact Markdown renderer that supports the
current atlas skeleton.

```bash
cd /Users/nicolasbottarini/projects/ai-notes
python3 build.py
```

The build refuses to clear `site/` if it loads zero notes.

## Serve Locally

Search uses `fetch`, so serve the generated folder for full functionality:

```bash
cd /Users/nicolasbottarini/projects/ai-notes
python3 -m http.server 8001 --directory site
```

Open:

```text
http://127.0.0.1:8001/en/
http://127.0.0.1:8001/es/
```

## Add a Note

Create a Markdown file under `content/en/ai/<branch>/`.

```markdown
---
title: My New Note
description: Short SEO/search description.
tags: [llms, evaluation]
order: 2
updated: 2026-06-07
# featured: true   # optional — promotes this note to the home "Featured" card
# draft: true      # optional — keeps the note out of the build until removed
---
# My New Note

Atomic note body.
```

Frontmatter flags:

- `order` sorts notes inside a branch (lower first; index is always pinned on top).
- `featured: true` selects the single note shown in the home "Featured note" card.
  If none is set, the first concept/playbook note is used.
- `draft: true` excludes the note from the build (and from search/sitemap), so you
  can write in-tree without publishing. The build logs how many drafts it skipped.

Use wikilinks for internal references:

```markdown
[[ai/llms/transformer-attention-map|Transformer Attention Map]]
```

Then rebuild:

```bash
python3 build.py
```

## Add a Branch

1. Add the branch metadata in `BRANCHES` inside `build.py`.
2. Add an optional Spanish label/summary in `BRANCHES_ES`.
3. Create `content/en/ai/<branch>/index.md`.
4. Create `content/es/ai/<branch>/index.md` if you want a translated overlay.
5. Rebuild.

The home branch cards, sidebar grouping, search metadata, and page URLs are
derived from that structure.

## Add a Translation

Spanish is an overlay, not a separate source tree. Create the same path under
`content/es/`:

```text
content/en/ai/llms/example.md
content/es/ai/llms/example.md
```

If a translation is missing, the ES page still exists and shows the English
source with a translation-pending banner.

## SEO and Deployment

The build emits:

- Canonical URLs
- `hreflang` alternates for EN/ES and `x-default`
- OpenGraph and Twitter metadata with a **PNG** social image (1200x630)
- `apple-touch-icon` + PWA icons (192/512, including a maskable variant)
- JSON-LD breadcrumbs/articles
- `site/sitemap.xml`
- `site/robots.txt`
- `.nojekyll` for GitHub Pages

Set `SITE_URL` and `GITHUB_URL` when building if the final repository URL
differs from the defaults:

```bash
SITE_URL="https://example.com/ai-notes" \
GITHUB_URL="https://github.com/your-user/ai-notes" \
python3 build.py
```

### Brand assets (SVG -> PNG)

Social/share platforms do not render SVG, so the PNG icons and the OG image are
committed to `static/`. Regenerate them after editing `static/favicon.svg` or
`static/assets/og-image.svg`:

```bash
./scripts/rasterize-brand-assets.sh
```

The script uses `rsvg-convert`, `magick`, or `inkscape` if installed, and falls
back to the macOS built-in `qlmanage`/`sips` (no install required).

### Continuous deployment

`.github/workflows/deploy.yml` builds the site and publishes it to GitHub Pages
on every push to `main`. It runs `python build.py` with `SITE_URL` set to the
Pages base URL, then uploads `site/` as the Pages artifact — the generated
`site/` folder does not need to be committed once CI is enabled.

## Initial Content

The skeleton includes:

- Main AI index
- Start Here and Must Know
- Six phase pages
- Thirteen branch index placeholders
- Three short example notes
- One AI playbook
- One reference registry

It is intentionally small so the atlas can grow from real notes instead of a
large invented knowledge base.
