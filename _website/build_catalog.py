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


# --- Study material: surface the research behind each piece on its work page --
NT_BOOKS = {
    "matthew", "mark", "luke", "john", "acts", "romans", "corinthians",
    "galatians", "ephesians", "philippians", "colossians", "thessalonians",
    "timothy", "titus", "philemon", "hebrews", "james", "peter", "jude", "revelation",
}
OT_AUTHOR = {"psalm": "David", "psalms": "David", "isaiah": "Isaiah", "zechariah": "Zechariah"}
OT_WHEN = {
    "psalm": "around a thousand years before the cross",
    "psalms": "around a thousand years before the cross",
    "isaiah": "around seven hundred years before the cross",
    "zechariah": "around five hundred years before the cross",
}
# Hand-written historical setting, keyed by the Old-Testament book in view.
STUDY_SETTING = {
    "psalm": (
        "Psalm 22 is a cry of King David, set down roughly a thousand years before Christ. "
        "It opens in the voice of a man surrounded and abandoned, then bends, line by line, "
        "toward a suffering David himself never endured and a rescue that reaches the ends of the earth."
    ),
    "isaiah": (
        "These lines belong to Isaiah's fourth Servant Song, written some seven hundred years "
        "before the cross. They describe a man wounded for the sins of others, whose suffering "
        "becomes the means of their healing."
    ),
    "zechariah": (
        "Zechariah prophesied in Jerusalem after the return from exile, around five hundred years "
        "before the cross, while the people rebuilt the temple. Chapter 12 looks past their own day "
        "to a deliverance of Jerusalem, where God says its people will look on one they have pierced "
        "and mourn for him as for an only son."
    ),
}
STOP_HEADINGS = ("depth", "voice", "sourcing", "ledger", "footnote", "sources", "notes")


def slopless(s: str) -> str:
    """Normalise authored narration to the site's no-smart-typography house style."""
    if not s:
        return ""
    s = s.replace(" — ", ", ").replace(" – ", ", ").replace("—", ", ").replace("–", "-")
    s = s.replace("…", "...")
    s = s.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"\s+,", ",", s)
    s = re.sub(r",\s*,", ",", s)
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip()


def book_of(ref: str) -> str:
    ref = (ref or "").strip()
    if not ref:
        return ""
    return re.sub(r"^\d+\s*", "", ref).split()[0].lower()


def is_nt(ref: str) -> bool:
    return book_of(ref) in NT_BOOKS


def study_source_for(item: dict) -> str | None:
    ss = item.get("study_source")
    if ss:
        return ss
    ps = item.get("preview_source") or ""
    if "/visual/" in ps:
        return ps.split("/visual/")[0]
    return None


def parse_reading(md_text: str) -> list[dict]:
    """Turn the narration script into ordered blocks: heading / prose / scripture."""
    lines = md_text.splitlines()
    start = 0
    for i, l in enumerate(lines):
        if l.strip() == "---":
            start = i + 1
            break
    blocks: list[dict] = []
    i, n = start, len(lines)
    while i < n:
        raw = lines[i].strip()
        if raw.startswith("## "):
            title = raw[3:].strip()
            if any(w in title.lower() for w in STOP_HEADINGS):
                break
            title = re.sub(r"\*\(.*?\)\*", "", title)
            title = re.sub(r"^MOVEMENT\s+\d+\s*[—–-]\s*", "", title, flags=re.I)
            blocks.append({"type": "heading", "text": slopless(title).title()})
            i += 1
            continue
        m = re.match(r"\*\*\[(.+?)\]\*\*", raw)
        if m:
            tag = m.group(1)
            i += 1
            content = []
            while i < n:
                c = lines[i].strip()
                if not c or c.startswith("**[") or c.startswith("## ") or c == "---":
                    break
                content.append(c)
                i += 1
            text = " ".join(content).strip()
            km = re.search(r"KJV,\s*(.+)", tag)
            if km:
                # narration may put terminal punctuation OUTSIDE the closing quote
                # ("It is finished".) to mark a KJV elision - keep only the quoted words
                qt = re.sub(r'^"', "", text.strip())
                qt = re.sub(r'"\s*[.,;:]?\s*$', "", qt).strip()
                blocks.append({"type": "scripture", "ref": km.group(1).strip(), "text": slopless(qt)})
            elif text:
                blocks.append({"type": "prose", "text": slopless(text)})
            continue
        i += 1
    return blocks


def load_study(study_source: str | None) -> dict | None:
    """Read the narration and return clean, audience-ready study data."""
    if not study_source:
        return None
    base = (SITE_DIR / study_source).resolve()
    md = base / "narration.md"
    creation = base / "narration.creation.json"
    if not md.is_file():
        return None
    reading = parse_reading(md.read_text(encoding="utf-8"))
    if not reading:
        return None
    scriptures = [b for b in reading if b["type"] == "scripture"]

    gospel, primary_book = "", ""
    if creation.is_file():
        c = json.loads(creation.read_text(encoding="utf-8"))
        gospel = slopless((c.get("thread") or {}).get("gospel_landing", ""))
        primary_book = book_of((c.get("episode") or {}).get("primary_ref", ""))

    ot = next((s for s in scriptures if not is_nt(s["ref"])), None)
    nt = next((s for s in scriptures if is_nt(s["ref"])), None)
    if not primary_book and ot:
        primary_book = book_of(ot["ref"])

    prophecy = None
    if ot and nt:
        b = book_of(ot["ref"])
        prophecy = {
            "who": OT_AUTHOR.get(b, ""),
            "when": OT_WHEN.get(b, ""),
            "ot": ot,
            "nt": nt,
        }

    return {
        "setting": STUDY_SETTING.get(primary_book, ""),
        "prophecy": prophecy,
        "reading": reading,
        "gospel": gospel,
        "is_long": sum(1 for b in reading if b["type"] == "heading") >= 2,
    }


STUDY_STOP = {
    "the", "and", "that", "with", "from", "this", "what", "who", "whom", "not", "but",
    "for", "his", "her", "him", "she", "they", "them", "you", "your", "our", "its",
    "into", "out", "over", "shall", "will", "thou", "thee", "thy", "hath", "unto",
    "upon", "then", "when", "there", "here", "all", "was", "were", "are", "has", "have",
    "had", "did", "does", "would", "could", "should", "one", "two", "yet", "far", "off",
    "let", "saw", "see", "seen", "made", "make", "own", "his", "where", "why",
}


def _words(t: str) -> set:
    return {w for w in re.findall(r"[a-z]{3,}", (t or "").lower())} - STUDY_STOP


def gather_scene_pngs(base: Path) -> list[dict]:
    own = base / "visual" / "nbp"
    pngs = sorted(own.glob("*.png")) if own.is_dir() else []
    if not pngs:  # long-form: pool stills from the sibling shorts
        pngs = sorted(base.glob("shorts/*/visual/nbp/*.png"))
    out = []
    for png in pngs:
        m = re.match(r"\d+_(.+)\.png$", png.name)
        slug = m.group(1) if m else png.stem
        out.append({"slug": slug, "png": png, "words": _words(slug.replace("-", " "))})
    return out


def select_study_figures(study_source, slug, reading, is_long, exclude_slug="") -> dict:
    """Choose which scene painting illustrates each narration moment (keyword match).

    Returns {block_index: candidate}. Deterministic, so the cloud build (which has
    only the committed webps, not the source media) reproduces the same placement.
    """
    if not study_source:
        return {}
    base = (SITE_DIR / study_source).resolve()
    out_dir = SITE_DIR / "assets" / "study" / slug
    cands = [c for c in gather_scene_pngs(base) if c["slug"] != exclude_slug]
    if not cands and out_dir.is_dir():  # Netlify: rebuild candidates from committed assets
        webps = list(out_dir.glob("*.webp")) + list((out_dir / "cut").glob("*.webp"))
        cands = [
            {"slug": s, "png": None, "words": _words(s.replace("-", " "))}
            for s in sorted({w.stem for w in webps})
        ]
    if not cands:
        return {}

    # one painting per unique scene (the pooled shorts share recurring motifs)
    seen, uniq = set(), []
    for c in cands:
        if c["slug"] in seen:
            continue
        seen.add(c["slug"])
        uniq.append(c)

    anchorable = [i for i, b in enumerate(reading) if b["type"] in ("prose", "scripture")]
    if not anchorable:
        return {}

    scored = []
    for c in uniq:
        best_i, best_s = None, 0
        for i in anchorable:
            sc = len(c["words"] & _words(reading[i].get("text", "")))
            if sc > best_s:
                best_s, best_i = sc, i
        if best_i is not None:
            scored.append((best_s, c["slug"], c, best_i))
    scored.sort(key=lambda x: (-x[0], x[1]))

    cap = 8 if is_long else 4
    placement = {}
    for sc, _sl, c, bi in scored:
        if len(placement) >= cap or sc <= 0:
            break
        if bi in placement:
            free = [i for i in anchorable if i not in placement]
            if not free:
                break
            bi = min(free, key=lambda i: (abs(i - bi), i))
        placement[bi] = c
    return placement


# All existing study stills are Baroque oil paintings - archived off the site
# (archive/website_baroque/). Flip back on when inked plates exist per piece.
STUDY_FIGURES_ENABLED = False


def build_study_figures(study_source, slug, reading, is_long, warnings, exclude_slug="") -> dict:
    """Render each placed painting: a floated cutout (text-wrap) if one exists, else a plate."""
    if not STUDY_FIGURES_ENABLED:
        return {}
    placement = select_study_figures(study_source, slug, reading, is_long, exclude_slug)
    if not placement:
        return {}
    out_dir = SITE_DIR / "assets" / "study" / slug
    figs, cut_side = {}, 0
    for bi, c in placement.items():
        cut_rel = f"assets/study/{slug}/cut/{c['slug']}.webp"
        if (SITE_DIR / cut_rel).is_file():
            # a cut-out only wraps cleanly when prose follows it; retarget if needed
            tgt = bi if reading[bi]["type"] == "prose" else None
            if tgt is None:
                tgt = next(
                    (j for j in range(bi, len(reading))
                     if reading[j]["type"] == "prose" and j not in figs),
                    None,
                )
            if tgt is not None and tgt not in figs:
                side = "left" if cut_side % 2 == 0 else "right"
                cut_side += 1
                figs[tgt] = (
                    f'<figure class="study-cutout cut-{side}" '
                    f'style="shape-outside:url(../{cut_rel})">'
                    f'<img src="../{cut_rel}" alt="" loading="lazy"></figure>'
                )
                continue
            # no prose to wrap: fall through and show it as a framed plate
        web_rel = f"assets/study/{slug}/{c['slug']}.webp"
        webp = SITE_DIR / web_rel
        if not webp.is_file():
            if Image is None or not c.get("png") or not c["png"].is_file():
                continue
            try:
                out_dir.mkdir(parents=True, exist_ok=True)
                im = Image.open(c["png"]).convert("RGB")
                im.thumbnail((620, 1040), Image.Resampling.LANCZOS)
                im.save(webp, "WEBP", quality=82, method=6)
            except OSError as ex:
                warnings.append(f"{slug}: study figure {c['slug']} failed ({ex})")
                continue
        caption = c["slug"].replace("-", " ").title()
        figs[bi] = (
            f'<figure class="study-figure"><img src="../{web_rel}" '
            f'alt="{html.escape(caption)}" loading="lazy">'
            f"<figcaption>{html.escape(caption)}</figcaption></figure>"
        )
    return figs


def render_study_html(s: dict | None, figs: dict | None = None) -> str:
    if not s:
        return ""
    figs = figs or {}
    e = html.escape
    p = ['<section class="study">', "      <h2>The study behind this</h2>"]
    if s["setting"]:
        p.append(f'      <p class="study-setting">{e(s["setting"])}</p>')

    if s["prophecy"]:
        pr = s["prophecy"]
        meta = f"Written by {pr['who']}, {pr['when']}." if pr["who"] else ""
        p.append('      <div class="prophecy">')
        p.append('        <div class="prophecy-col">')
        p.append('          <span class="prophecy-tag">The prophecy</span>')
        p.append(f'          <blockquote class="scripture"><p>{e(pr["ot"]["text"])}</p><cite>{e(pr["ot"]["ref"])}</cite></blockquote>')
        if meta:
            p.append(f'          <p class="prophecy-meta">{e(meta)}</p>')
        p.append("        </div>")
        p.append('        <div class="prophecy-arrow" aria-hidden="true"></div>')
        p.append('        <div class="prophecy-col">')
        p.append('          <span class="prophecy-tag">The fulfilment</span>')
        p.append(f'          <blockquote class="scripture"><p>{e(pr["nt"]["text"])}</p><cite>{e(pr["nt"]["ref"])}</cite></blockquote>')
        p.append('          <p class="prophecy-meta">Fulfilled in Jesus Christ.</p>')
        p.append("        </div>")
        p.append("      </div>")

    p.append(f'      <h3>{"Movement by movement" if s["is_long"] else "The reading"}</h3>')
    p.append('      <div class="reading">')
    first_prose = True
    for bi, b in enumerate(s["reading"]):
        if bi in figs:
            p.append("        " + figs[bi])
        if b["type"] == "heading":
            p.append(f'        <h4 class="movement">{e(b["text"])}</h4>')
        elif b["type"] == "scripture":
            p.append(f'        <blockquote class="scripture verse"><p>{e(b["text"])}</p><cite>{e(b["ref"])}</cite></blockquote>')
        else:
            cls = ' class="lead-para"' if first_prose else ""
            first_prose = False
            prose = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", e(b["text"]))
            p.append(f"        <p{cls}>{prose}</p>")
    p.append("      </div>")

    if s["gospel"]:
        p.append(f'      <aside class="study-close"><span>Where it lands</span><p>{e(s["gospel"])}</p></aside>')
    p.append(
        '      <p class="study-note">Every quotation is the King James Version, '
        "verified word for word against the text.</p>"
    )
    p.append("    </section>")
    return "\n".join(p)


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

    if src and src.suffix.lower() in (".png", ".jpg", ".jpeg") and src.is_file() and Image:
        try:
            im = Image.open(src).convert("RGB")
            im.thumbnail((540, 960), Image.Resampling.LANCZOS)
            im.save(webp, "WEBP", quality=82, method=6)
            return f"assets/previews/{slug}.webp"
        except OSError as e:
            warnings.append(f"{slug}: preview copy failed ({e})")

    # Source unavailable (e.g. Netlify CI has no local media tree): reuse a
    # previously committed .webp if one exists, rather than downgrading to SVG.
    if webp.is_file():
        return f"assets/previews/{slug}.webp"

    if src and src.suffix.lower() in (".png", ".jpg", ".jpeg") and not src.is_file():
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


def render_work_page(item: dict, config: dict, warnings: list) -> str:
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

    ss = study_source_for(item)
    study = load_study(ss)
    poster_m = re.search(r"\d+_([a-z0-9-]+)\.png", item.get("preview_source") or "")
    poster_slug = poster_m.group(1) if poster_m else ""
    figs = (
        build_study_figures(
            ss, item["slug"], study["reading"], study["is_long"], warnings, poster_slug
        )
        if study
        else {}
    )
    study_html = render_study_html(study, figs)
    site_url = site["url"].rstrip("/")
    page_url = f"{site_url}/work/{item['slug']}.html"
    og_card = SITE_DIR / "assets" / "og" / f"{item['slug']}.jpg"
    og_img = (
        f"{site_url}/assets/og/{item['slug']}.jpg"
        if og_card.is_file()
        else f"{site_url}/assets/og-cover.jpg"
    )
    title_full = f"{item['title']} | {brand['wordmark']}"
    ld_json = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "CreativeWork",
            "name": item["title"],
            "description": item.get("public_hook", "").strip(),
            "url": page_url,
            "image": og_img,
            "isPartOf": {"@type": "WebSite", "name": "Awakeden", "url": f"{site_url}/"},
        },
        ensure_ascii=False,
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(item['title'])} | {html.escape(brand['wordmark'])}</title>
  <meta name="description" content="{hook}">
  <link rel="canonical" href="{page_url}">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <meta name="theme-color" content="#0c0e12">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Awakeden">
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
  <link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/css/site.css">
</head>
<body>
  <nav class="nav" aria-label="Main">
    <a class="wordmark" href="../index.html">AWAK<em>EDEN</em></a>
    <div class="nav-links">
      <a href="../catalogue.html">Catalogue</a>
      <a href="../read/index.html">Read</a>
      <a href="../plan.html">The Plan</a>
      <a href="../about.html">About</a>
    </div>
    <a class="nav-cta" href="../read/index.html">Start reading</a>
  </nav>
  <main class="work-page" style="padding-top:5.5rem">
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
    {study_html}
    <p><a class="text-link" href="../catalogue.html">Back to catalogue</a></p>
  </main>
  <footer class="site-footer">
    <p><span class="wordmark" style="font-size:.85rem">AWAK<em>EDEN</em></span></p>
    <p>{html.escape(site.get('scripture_note', ''))} The ink is ours. The words are His.</p>
    <p class="footer-url">{html.escape(site['url'])}</p>
  </footer>
  <script src="../assets/js/motion.js" defer></script>
</body>
</html>"""


def write_sitemap(config: dict, items: list[dict]) -> None:
    base = config["site"]["url"].rstrip("/")
    urls = ["/", "/catalogue.html", "/about.html", "/plan.html", "/series/psalm-22.html",
            "/read/index.html"]
    # read pages: any manifest item wired to a read_source with frames on disk
    urls += [f"/read/{i['slug']}.html" for i in items
             if i.get("read_source")
             and (SITE_DIR / "assets" / "study" / "read" / i["slug"] / "beat_01.jpg").is_file()]
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
    # catalog.json is publicly fetchable: strip build-internal source pointers there
    INTERNAL_FIELDS = ("read_source", "read_spec", "read_video", "study_source", "preview_source")
    public_items = [{k: v for k, v in it.items() if k not in INTERNAL_FIELDS} for it in items]

    catalog = {
        "generated": date.today().isoformat(),
        "site": config["site"],
        "brand": config["brand"],
        "social": config.get("social", {}),
        "launch": config.get("launch", {}),
        "clusters": manifest.get("clusters", {}),
        "roadmap": manifest.get("roadmap", []),
        "items": public_items,
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
            render_work_page(item, config, warnings), encoding="utf-8"
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
