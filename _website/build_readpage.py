#!/usr/bin/env python3
"""Build the READ pages (comic strips) + The Plan tracker for awakeden.com.

Every living-page piece is already a comic: `livingpage_short.spec.json` holds the
beats/captions/red-letter bars and the finished video has them rendered pixel-true.
This script extracts ONE frame per beat from the scored MP4 (local run, needs ffmpeg)
into `assets/study/read/<slug>/beat_NN.jpg`, then writes:

    read/<slug>.html    the scrollable strip (frames + figcaptions + narration text)
    read/index.html     the strip library
    plan.html           the public tracker (Out now / In the studio / Next)

Frames are committed (assets/study/** is git-allowed), so Netlify can rebuild the
HTML without media:  python build_readpage.py --html-only

Run locally after a new piece locks:  python _website/build_readpage.py
"""
from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. pip install -r _website/requirements.txt", file=sys.stderr)
    raise SystemExit(1)

SITE_DIR = Path(__file__).resolve().parent
REPO_ROOT = SITE_DIR.parent
READ_ASSETS = SITE_DIR / "assets" / "study" / "read"
READ_DIR = SITE_DIR / "read"
FRAME_W = 540
JPEG_Q = 4          # ffmpeg -q:v (2 best .. 31 worst)


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def slopless(s: str) -> str:
    if not s:
        return ""
    s = s.replace(" — ", ", ").replace("—", ", ").replace("–", "-")
    s = s.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
    s = s.replace("…", "...")
    return re.sub(r"\s{2,}", " ", s).strip()


def chrome_top(title: str, desc: str, canonical: str, og_image: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)} | Awakeden</title>
  <link rel="stylesheet" href="../assets/css/site.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <meta name="description" content="{esc(desc)}">
  <link rel="canonical" href="{esc(canonical)}">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <meta name="theme-color" content="#0c0e12">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Awakeden">
  <meta property="og:title" content="{esc(title)} | Awakeden">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{esc(canonical)}">
  <meta property="og:image" content="{esc(og_image)}">
  <meta name="twitter:card" content="summary_large_image">
  <style>
    main.page{{padding-top:5.5rem}}
    .strip{{max-width:560px;margin:0 auto;padding:0 12px}}
    .strip figure{{margin:0 0 30px}}
    .strip img{{width:100%;border-radius:8px;display:block;border:1px solid rgba(255,255,255,.07);box-shadow:0 10px 34px rgba(0,0,0,.5)}}
    .strip figcaption{{font-size:.95rem;color:#9aa3b2;padding:10px 4px 0;line-height:1.5}}
    .strip figcaption .bar{{display:inline-block;background:#c1121f;color:#fff;font-weight:700;font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;padding:.28rem .6rem;border-radius:3px;margin-right:.35rem}}
    .read-meta{{text-align:center;max-width:640px;margin:0 auto 34px;padding:0 14px;color:#9aa3b2}}
    .read-meta .verse{{display:inline-block;background:#c1121f;color:#fff;font-weight:700;letter-spacing:.18em;font-size:.78rem;padding:.35rem .8rem;border-radius:4px;text-transform:uppercase}}
    .read-text{{max-width:640px;margin:44px auto 0;padding:0 14px;line-height:1.75;color:#c8ccd4}}
    .read-text h2{{font-family:'Archivo Black',sans-serif;text-transform:uppercase;font-size:1.15rem;letter-spacing:.02em;color:#efe9dc}}
    .plan-cols{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:22px;max-width:1080px;margin:0 auto;padding:0 14px}}
    .plan-col h2{{font-family:'Archivo Black',sans-serif;font-size:1rem;letter-spacing:.06em;text-transform:uppercase;color:#efe9dc}}
    .plan-item{{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:8px;padding:12px 15px;margin:0 0 10px}}
    .plan-item .t{{font-weight:600;color:#e6e9ee}}
    .plan-item .r{{font-size:.82rem;color:#e5303d;font-weight:600;letter-spacing:.08em}}
    .plan-item a{{text-decoration:none;color:inherit}}
    .plan-note{{color:#9aa3b2;font-size:.9rem}}
    .read-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:20px;max-width:1080px;margin:0 auto;padding:0 14px}}
    .read-card img{{width:100%;border-radius:8px;display:block;border:1px solid rgba(255,255,255,.07)}}
    .read-card{{text-decoration:none;color:inherit;transition:transform .18s ease}}
    .read-card:hover{{transform:translateY(-3px)}}
    .read-card .t{{font-weight:700;padding-top:8px;color:#e6e9ee}}
    .read-card .r{{font-size:.8rem;color:#e5303d;font-weight:600;letter-spacing:.08em}}
  </style>
</head>
<body>
  <nav class="nav" aria-label="Main">
    <a class="wordmark" href="../index.html">AWAK<em>EDEN</em></a>
    <div class="nav-links">
      <a href="../catalogue.html">Catalogue</a>
      <a href="index.html">Read</a>
      <a href="../plan.html">The Plan</a>
      <a href="../about.html">About</a>
    </div>
    <a class="nav-cta" href="index.html">Start reading</a>
  </nav>
  <main class="page">
"""


CHROME_BOTTOM = """  </main>
  <footer class="site-footer"><p><span class="wordmark" style="font-size:.85rem">AWAK<em>EDEN</em></span></p>
  <p>Scripture quoted from the King James Version (KJV), public domain. The ink is ours. The words are His.</p></footer>
</body>
</html>
"""


def beat_caption(beat: dict) -> str:
    cap = beat.get("cap") or {}
    text = slopless(cap.get("text", ""))
    if cap.get("type") == "redletter":
        speaker = cap.get("speaker", "")
        ref = cap.get("ref", "")
        tag = " - ".join(x for x in (speaker, ref) if x)
        return f'<span class="bar">{esc(tag)}</span> &nbsp;"{esc(text)}"'
    return esc(text)


def extract_frames(item: dict, batch: Path, out_dir: Path, *, force: bool) -> int:
    spec_p = batch / item.get("read_spec", "visual/livingpage_short.spec.json")
    spec = json.loads(spec_p.read_text(encoding="utf-8"))
    if item.get("read_video"):
        scored = [batch / item["read_video"]]
        if not scored[0].is_file():
            scored = []
    else:
        scored = sorted((batch / "visual").glob("*_scored.mp4"))
    if not scored:
        print(f"  !! no scored mp4 for {item['slug']} - skipping frames")
        return 0
    video = scored[0]
    out_dir.mkdir(parents=True, exist_ok=True)
    n = 0
    for i, beat in enumerate(spec["beats"], 1):
        dest = out_dir / f"beat_{i:02d}.jpg"
        n += 1
        if dest.exists() and not force:
            continue
        t0, t1 = beat["t"]
        t = min(max(t0 + 0.8 * (t1 - t0), t0 + 0.3), t1 - 0.15)
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(video),
             "-frames:v", "1", "-vf", f"scale={FRAME_W}:-2", "-q:v", str(JPEG_Q), str(dest)],
            check=True)
    return n


def render_read_page(item: dict, spec: dict, slug: str, narration_text: str) -> str:
    title = item["title"]
    ref = item.get("ref", "")
    hook = slopless(item.get("public_hook", ""))
    canonical = f"https://awakeden.com/read/{slug}.html"
    og = f"https://awakeden.com/assets/study/read/{slug}/beat_01.jpg"
    parts = [chrome_top(f"Read: {title}", hook or f"{title}, hand-inked and readable panel by panel.",
                        canonical, og)]
    parts.append(f'<div class="page-hero"><h1>{esc(title)}</h1>'
                 f'<p class="hero-lead">{esc(hook)}</p></div>')
    parts.append('<div class="read-meta">'
                 f'<p class="verse">{esc(ref)} &middot; KJV</p>'
                 '<p>Every panel below is a frame from the finished film, in order. '
                 'Scripture is in red. The video version is coming to YouTube.</p></div>')
    parts.append('<div class="strip">')
    for i, beat in enumerate(spec["beats"], 1):
        img = f"../assets/study/read/{slug}/beat_{i:02d}.jpg"
        parts.append(f'<figure><img loading="lazy" src="{img}" '
                     f'alt="Panel {i}: {esc(slopless((beat.get("cap") or {}).get("text", "")))}">'
                     f'<figcaption>{beat_caption(beat)}</figcaption></figure>')
    parts.append("</div>")
    if narration_text:
        parts.append('<div class="read-text"><h2>The narration</h2>'
                     f'<p>{esc(slopless(narration_text))}</p></div>')
    parts.append(CHROME_BOTTOM)
    return "\n".join(parts)


def render_read_index(pages: list[dict]) -> str:
    parts = [chrome_top("Read", "Every Awakeden short, hand-inked and readable panel by panel.",
                        "https://awakeden.com/read/index.html",
                        "https://awakeden.com/assets/og-cover.jpg")]
    parts.append('<div class="page-hero"><h1>Read</h1>'
                 '<p class="hero-lead">Every short is drawn before it is filmed. '
                 'Read each one panel by panel, Scripture in red.</p></div>')
    parts.append('<div class="read-grid">')
    for p in pages:
        parts.append(f'<a class="read-card" href="{p["slug"]}.html">'
                     f'<img loading="lazy" src="../assets/study/read/{p["slug"]}/beat_01.jpg" alt="{esc(p["title"])}">'
                     f'<div class="t">{esc(p["title"])}</div>'
                     f'<div class="r">{esc(p["ref"])}</div></a>')
    parts.append("</div>")
    parts.append(CHROME_BOTTOM)
    return "\n".join(parts)


PLAN_GROUPS = [
    ("Out now", ["live"], "Live on YouTube. Launch is next; published pieces will appear here."),
    ("In the studio", ["studio_complete", "in_production"],
     "Built or being built - finished pieces wait in the release bank."),
    ("Next", ["planned"], "On the slate."),
]


def render_plan(items: list[dict], read_slugs: set[str]) -> str:
    parts = [chrome_top("The Plan", "What is out, what is in the studio, and what is next on Awakeden.",
                        "https://awakeden.com/plan.html",
                        "https://awakeden.com/assets/og-cover.jpg")]
    # plan.html sits at site root: fix relative nav/css from the read/ chrome
    parts[0] = parts[0].replace('href="../', 'href="').replace('src="../', 'src="')
    parts[0] = parts[0].replace('href="index.html">Read', 'href="read/index.html">Read')
    parts[0] = parts[0].replace('href="index.html">Start reading', 'href="read/index.html">Start reading')
    parts.append('<div class="page-hero"><h1>The Plan</h1>'
                 '<p class="hero-lead">We build in the open. Finished pieces bank up before '
                 'release; the schedule slips before a quality gate ever does.</p></div>')
    parts.append('<div class="plan-cols">')
    for label, statuses, note in PLAN_GROUPS:
        rows = [i for i in items if i.get("public_status") in statuses]
        parts.append(f'<div class="plan-col"><h2>{esc(label)}</h2><p class="plan-note">{esc(note)}</p>')
        for i in rows:
            t = esc(i["title"])
            body = f'<div class="t">{t}</div><div class="r">{esc(i.get("ref", ""))}</div>'
            slug = i["slug"]
            if slug in read_slugs:
                body = f'<a href="read/{slug}.html">{body}<div class="plan-note" style="font-size:.8rem">Read the whole study &rarr;</div></a>'
            parts.append(f'<div class="plan-item">{body}</div>')
        parts.append("</div>")
    parts.append("</div>")
    parts.append(CHROME_BOTTOM.replace('href="../', 'href="'))
    return "\n".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--html-only", action="store_true", help="no ffmpeg; rebuild HTML from committed frames")
    ap.add_argument("--force", action="store_true", help="re-extract frames even if present")
    args = ap.parse_args()

    manifest = yaml.safe_load((SITE_DIR / "manifest.yaml").read_text(encoding="utf-8"))
    items = manifest["items"]
    READ_DIR.mkdir(exist_ok=True)

    pages: list[dict] = []
    for item in items:
        rs = item.get("read_source")
        if not rs:
            continue
        batch = (SITE_DIR / rs).resolve()
        spec_p = batch / item.get("read_spec", "visual/livingpage_short.spec.json")
        if not spec_p.is_file():
            continue
        slug = item["slug"]
        out_dir = READ_ASSETS / slug
        if not args.html_only:
            extract_frames(item, batch, out_dir, force=args.force)
        if not (out_dir / "beat_01.jpg").is_file():
            print(f"  !! no frames on disk for {slug} - skipping page")
            continue
        spec = json.loads(spec_p.read_text(encoding="utf-8"))
        narration = ""
        sp = batch / "audio" / "narration.spoken.txt"
        if sp.is_file():
            narration = sp.read_text(encoding="utf-8")
        (READ_DIR / f"{slug}.html").write_text(
            render_read_page(item, spec, slug, narration), encoding="utf-8")
        pages.append({"slug": slug, "title": item["title"], "ref": item.get("ref", "")})
        print(f"  read/{slug}.html  ({len(spec['beats'])} panels)")

    pages.sort(key=lambda p: p["title"])
    (READ_DIR / "index.html").write_text(render_read_index(pages), encoding="utf-8")
    (SITE_DIR / "plan.html").write_text(
        render_plan(items, {p["slug"] for p in pages}), encoding="utf-8")
    print(f"built read/index.html ({len(pages)} strips) + plan.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
