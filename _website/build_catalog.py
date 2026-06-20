#!/usr/bin/env python3
"""Build www.awakeden.com catalogue from manifest.yaml + config.yaml.

Run from repo root or _website/:
  python _website/build_catalog.py

Outputs:
  data/catalog.json, sitemap.xml, robots.txt, work/*.html, assets/previews/*
"""
from __future__ import annotations

import html
import json
import re
import sys
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. pip install -r _website/requirements.txt", file=sys.stderr)
    raise SystemExit(1)

try:
    from PIL import Image
except ImportError:
    Image = None  # type: ignore

SITE_DIR = Path(__file__).resolve().parent
REPO_ROOT = SITE_DIR.parent
PREVIEW_DIR = SITE_DIR / "assets" / "previews"
WORK_DIR = SITE_DIR / "work"
DATA_DIR = SITE_DIR / "data"

STATUS_LABEL = {
    "planned": "Planned",
    "in_production": "In production",
    "studio_complete": "Studio complete",
    "live": "Live",
}

STATUS_CLASS = {
    "planned": "status-planned",
    "in_production": "status-production",
    "studio_complete": "status-complete",
    "live": "status-live",
}


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


# --- AI-slop guard: ban "smart typography" tells from shipped copy ---------
# Literal characters and their HTML-entity forms that read as AI/auto-typeset
# copy. Straight quotes/apostrophes and plain hyphens are fine; these are not.
SLOP_CHARS = {
    "—": "em-dash",
    "–": "en-dash",
    "‘": "curly-quote",
    "’": "curly-quote",
    "“": "curly-quote",
    "”": "curly-quote",
    "…": "ellipsis",
}
SLOP_ENTITY = re.compile(
    r"&(?:mdash|ndash|lsquo|rsquo|ldquo|rdquo|hellip"
    r"|#8211|#8212|#8216|#8217|#8220|#8221|#8230"
    r"|#x201[34cd]|#x2018|#x2019|#x2026);",
    re.IGNORECASE,
)


def check_ai_slop(warnings: list[str]) -> None:
    """Fail the build if shipped copy contains smart-typography 'AI slop'.

    Scans the hand-edited copy sources (config/manifest) and every shipped
    .html page (incl. generated work/* pages). Dev docs (*.md) are exempt.
    Raises SystemExit on any hit so Netlify won't deploy it.
    """
    targets = [SITE_DIR / "config.yaml", SITE_DIR / "manifest.yaml"]
    targets += sorted(SITE_DIR.glob("*.html"))
    targets += sorted((SITE_DIR / "series").glob("*.html"))
    targets += sorted(WORK_DIR.glob("*.html"))

    hits: list[str] = []
    for path in targets:
        if not path.is_file():
            continue
        rel = path.relative_to(SITE_DIR)
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            found = {SLOP_CHARS[c] for c in line if c in SLOP_CHARS}
            if SLOP_ENTITY.search(line):
                found.add("html-entity")
            if found:
                kinds = ", ".join(sorted(found))
                hits.append(f"  {rel}:{lineno}  [{kinds}]  {line.strip()[:80]}")

    if hits:
        print("\nAI-SLOP GUARD FAILED — banned typography in shipped copy:", file=sys.stderr)
        print("\n".join(hits), file=sys.stderr)
        print(
            "\nReplace em/en-dashes with comma/colon/period, curly quotes with "
            "straight quotes, ellipsis with three periods. Then rebuild.",
            file=sys.stderr,
        )
        raise SystemExit(3)


def resolve_source(path_str: str) -> Path | None:
    if not path_str:
        return None
    p = (SITE_DIR / path_str).resolve()
    if p.is_file():
        return p
    if p.name == "scene_plan.json" and p.is_file():
        return p
    # scene_plan path → try hero PNG in same tree
    if path_str.endswith("scene_plan.json"):
        base = p.parent
        for provider in ("nbp", "hf"):
            d = base / provider
            if d.is_dir():
                pngs = sorted(d.glob("*.png"))
                if pngs:
                    return pngs[0]
        return None
    return None if not p.exists() else p


def find_hero_png_from_scene_plan(plan_path: Path) -> Path | None:
    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    hero = plan.get("hero_candidate")
    scenes = plan.get("scenes") or []
    slug = None
    for sc in scenes:
        if sc.get("index") == hero:
            slug = sc.get("slug") or sc.get("stem")
            break
    if not slug and scenes:
        slug = scenes[0].get("slug") or scenes[0].get("stem")
    if not slug:
        return None
    base = plan_path.parent
    for provider in ("nbp", "hf"):
        d = base / provider
        if not d.is_dir():
            continue
        for pat in (f"*_{slug}.png", f"{hero:02d}_{slug}.png", f"*{slug}*.png"):
            hits = list(d.glob(pat))
            if hits:
                return hits[0]
    return None


def write_svg_preview(slug: str, title: str, ref: str, out: Path) -> None:
    t = html.escape(title[:48])
    r = html.escape(ref)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="540" height="960" viewBox="0 0 540 960">
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#141018"/>
      <stop offset="50%" stop-color="#0a0a0c"/>
      <stop offset="100%" stop-color="#1c1208"/>
    </linearGradient>
    <radialGradient id="glow" cx="50%" cy="28%" r="55%">
      <stop offset="0%" stop-color="#c9a227" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#c9a227" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="bar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#c9a227" stop-opacity="0"/>
      <stop offset="100%" stop-color="#c9a227" stop-opacity="0.5"/>
    </linearGradient>
  </defs>
  <rect width="540" height="960" fill="url(#g)"/>
  <rect width="540" height="960" fill="url(#glow)"/>
  <rect x="0" y="0" width="4" height="960" fill="url(#bar)"/>
  <circle cx="420" cy="180" r="120" fill="none" stroke="#c9a227" stroke-opacity="0.08" stroke-width="1"/>
  <circle cx="420" cy="180" r="80" fill="none" stroke="#c9a227" stroke-opacity="0.12" stroke-width="1"/>
  <text x="36" y="780" fill="#c9a227" font-family="Georgia, serif" font-size="11" letter-spacing="0.28em">AWAKEDEN SERIES</text>
  <text x="36" y="830" fill="#f4efe6" font-family="Georgia, serif" font-size="26" font-weight="600">{t}</text>
  <text x="36" y="868" fill="#a89880" font-family="Georgia, serif" font-size="15">{r}</text>
</svg>"""
    out.write_text(svg, encoding="utf-8")


def build_preview(item: dict, warnings: list[str]) -> str | None:
    slug = item["slug"]
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    webp = PREVIEW_DIR / f"{slug}.webp"
    svg = PREVIEW_DIR / f"{slug}.svg"

    if not item.get("preview_approved"):
        write_svg_preview(slug, item["title"], item.get("ref", ""), svg)
        return f"assets/previews/{slug}.svg"

    src_str = item.get("preview_source") or ""
    src = resolve_source(src_str)
    if src and src.name == "scene_plan.json":
        src = find_hero_png_from_scene_plan(src) or src

    if src and src.suffix.lower() == ".png" and src.is_file() and Image:
        try:
            im = Image.open(src).convert("RGB")
            im.thumbnail((540, 960), Image.Resampling.LANCZOS)
            im.save(webp, "WEBP", quality=82, method=6)
            return f"assets/previews/{slug}.webp"
        except OSError as e:
            warnings.append(f"{slug}: preview copy failed ({e})")

    # PNG source unavailable (e.g. Netlify CI has no local media tree): reuse a
    # previously committed .webp if one exists, rather than downgrading to SVG.
    if webp.is_file():
        return f"assets/previews/{slug}.webp"

    if src and src.suffix.lower() == ".png" and not src.is_file():
        warnings.append(f"{slug}: preview_source missing on disk ({src_str}); SVG fallback")

    write_svg_preview(slug, item["title"], item.get("ref", ""), svg)
    return f"assets/previews/{slug}.svg"


def enrich_item(raw: dict, config: dict, warnings: list[str]) -> dict:
    item = dict(raw)
    item["status_label"] = STATUS_LABEL.get(item["public_status"], item["public_status"])
    item["status_class"] = STATUS_CLASS.get(item["public_status"], "")
    item["preview"] = build_preview(item, warnings)
    item["show_video"] = (
        config["site"].get("mode") == "live"
        and item.get("youtube_id")
    )
    item["kind_label"] = "Long-form" if item.get("kind") == "long" else "Short"
    return item


def render_work_page(item: dict, config: dict) -> str:
    site = config["site"]
    brand = config["brand"]
    preview = item.get("preview") or ""
    video_block = ""
    if item.get("show_video") and item.get("youtube_id"):
        yid = html.escape(item["youtube_id"])
        video_block = f"""
        <div class="work-video">
          <iframe src="https://www.youtube.com/embed/{yid}" title="{html.escape(item['title'])}"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen loading="lazy"></iframe>
        </div>"""
    elif site.get("mode") != "live" or not item.get("youtube_id"):
        video_block = """
        <div class="work-video work-video--soon">
          <p>Video will be on YouTube when the series launches.</p>
        </div>"""

    blurb = html.escape(item.get("public_blurb", "").strip())
    hook = html.escape(item.get("public_hook", "").strip())
    cluster_link = ""
    if item.get("cluster") == "psalm-22":
        cluster_link = '<p class="work-cluster"><a href="../series/psalm-22.html">Part of Psalm 22: From the Cross</a></p>'

    site_url = site["url"].rstrip("/")
    page_url = f"{site_url}/work/{item['slug']}.html"
    og_img = f"{site_url}/assets/og-cover.jpg"
    title_full = f"{item['title']} | {brand['wordmark']} {brand['series']}"
    ld_json = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "CreativeWork",
            "name": item["title"],
            "description": item.get("public_hook", "").strip(),
            "url": page_url,
            "image": og_img,
            "isPartOf": {"@type": "WebSite", "name": "Awakeden Series", "url": f"{site_url}/"},
        },
        ensure_ascii=False,
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(item['title'])} | {html.escape(brand['wordmark'])} {html.escape(brand['series'])}</title>
  <meta name="description" content="{hook}">
  <link rel="canonical" href="{page_url}">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <meta name="theme-color" content="#f4eee1">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Awakeden Series">
  <meta property="og:title" content="{html.escape(title_full)}">
  <meta property="og:description" content="{hook}">
  <meta property="og:url" content="{page_url}">
  <meta property="og:image" content="{og_img}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title_full)}">
  <meta name="twitter:description" content="{hook}">
  <meta name="twitter:image" content="{og_img}">
  <script type="application/ld+json">{ld_json}</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/css/site.css">
</head>
<body>
  <div class="grain" aria-hidden="true"></div>
  <header class="site-header">
    <a class="wordmark" href="../index.html"><span class="wordmark-main">{html.escape(brand['wordmark'])}</span> <span class="wordmark-sub">{html.escape(brand['series'])}</span></a>
    <nav class="site-nav">
      <a href="../catalogue.html">Catalogue</a>
      <a href="../series/psalm-22.html">Psalm 22</a>
      <a href="../roadmap.html">Roadmap</a>
      <a href="../about.html">About</a>
    </nav>
  </header>
  <main class="work-page">
    <div class="work-hero">
      <div class="work-poster{" ken-burns" if preview else ""}">
        {"<img src='../" + preview.lstrip("/") + "' alt=''>" if preview else "<div class='work-poster-fallback'></div>"}
      </div>
      <div class="work-meta">
        <span class="badge {item['status_class']}">{html.escape(item['status_label'])}</span>
        <span class="work-kind">{html.escape(item['kind_label'])}</span>
        <h1>{html.escape(item['title'])}</h1>
        <p class="work-ref">{html.escape(item.get('ref', ''))}</p>
        <p class="work-hook">{hook}</p>
        {cluster_link}
      </div>
    </div>
    {video_block}
    <div class="prose">
      <p>{blurb}</p>
    </div>
    <p><a class="text-link" href="../catalogue.html">Back to catalogue</a></p>
  </main>
  <footer class="site-footer">
    <p>{html.escape(site.get('scripture_note', ''))}</p>
    <p class="footer-url">{html.escape(site['url'])}</p>
  </footer>
  <script src="../assets/js/motion.js" defer></script>
</body>
</html>"""


def write_sitemap(config: dict, items: list[dict]) -> None:
    base = config["site"]["url"].rstrip("/")
    urls = ["/", "/catalogue.html", "/about.html", "/roadmap.html", "/series/psalm-22.html"]
    urls += [f"/work/{i['slug']}.html" for i in items]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lines.append(f"  <url><loc>{base}{u}</loc></url>")
    lines.append("</urlset>")
    (SITE_DIR / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_robots(config: dict) -> None:
    site = config["site"]
    if site.get("noindex"):
        body = "User-agent: *\nDisallow: /\n"
    else:
        body = f"User-agent: *\nAllow: /\nSitemap: {site['url']}/sitemap.xml\n"
    (SITE_DIR / "robots.txt").write_text(body, encoding="utf-8")


def main() -> int:
    warnings: list[str] = []
    config = load_yaml(SITE_DIR / "config.yaml")
    manifest = load_yaml(SITE_DIR / "manifest.yaml")

    items = [enrich_item(raw, config, warnings) for raw in manifest.get("items", [])]
    items.sort(key=lambda x: (not x.get("featured"), x.get("featured_order") or 99, x.get("cluster_order") or 99))

    catalog = {
        "generated": date.today().isoformat(),
        "site": config["site"],
        "brand": config["brand"],
        "social": config.get("social", {}),
        "launch": config.get("launch", {}),
        "clusters": manifest.get("clusters", {}),
        "roadmap": manifest.get("roadmap", []),
        "items": items,
        "stats": {
            "total": len(items),
            "live": sum(1 for i in items if i["public_status"] == "live"),
            "studio_complete": sum(1 for i in items if i["public_status"] == "studio_complete"),
            "in_production": sum(1 for i in items if i["public_status"] == "in_production"),
            "planned": sum(1 for i in items if i["public_status"] == "planned"),
        },
    }

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "catalog.json").write_text(
        json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    WORK_DIR.mkdir(parents=True, exist_ok=True)
    for item in items:
        (WORK_DIR / f"{item['slug']}.html").write_text(
            render_work_page(item, config), encoding="utf-8"
        )

    write_sitemap(config, items)
    write_robots(config)

    check_ai_slop(warnings)

    print(f"Built catalog: {len(items)} items -> {DATA_DIR / 'catalog.json'}")
    print(f"Work pages: {WORK_DIR} ({len(items)} files)")
    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  - {w}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
