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
    .plan-series{{font-size:.68rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#c8a55e;margin:1.1rem 0 .45rem}}
    .strip{{max-width:600px;margin:0 auto;padding:0 12px}}
    .strip figure{{margin:0 0 34px;background:#eceae4;padding:10px 10px 0;border-radius:4px;box-shadow:0 14px 40px rgba(0,0,0,.55);transform:rotate(-.5deg)}}
    .strip figure:nth-child(even){{transform:rotate(.6deg)}}
    .strip img{{width:100%;display:block;border:2px solid #101216;border-radius:0;box-shadow:none}}
    .strip figcaption{{font-size:.92rem;color:#23262c;padding:10px 6px 12px;line-height:1.45;font-weight:600}}
    .strip figcaption .bar{{display:inline-block;background:#c1121f;color:#fff;font-weight:800;font-size:.68rem;letter-spacing:.13em;text-transform:uppercase;padding:.26rem .55rem;border-radius:3px;margin-right:.4rem}}
    .strip figure.splash{{position:relative;background:none;padding:0;border-radius:6px;overflow:hidden;transform:none;box-shadow:0 18px 50px rgba(0,0,0,.65)}}
    .strip figure.splash img{{border:none}}
    .strip figure.splash .roar{{position:absolute;left:0;right:0;bottom:8%;text-align:center;font-family:'Archivo Black',sans-serif;text-transform:uppercase;color:#fff;font-size:clamp(2.6rem,10vw,4.8rem);letter-spacing:.02em;line-height:.9;text-shadow:0 4px 0 #000,0 0 40px rgba(229,48,61,.8);transform:rotate(-2deg)}}
    .depth-track{{display:flex;gap:.5rem;justify-content:center;flex-wrap:wrap;margin:1.2rem 0 0}}
    .depth-track a{{font-size:.72rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;padding:.45rem .85rem;border:1px solid rgba(255,255,255,.14);border-radius:999px;color:#9aa0ab;text-decoration:none;transition:.2s}}
    .depth-track a:hover{{border-color:#e5303d;color:#eceae4}}
    .depth-track a b{{color:#e5303d;margin-right:.35rem}}
    .sect{{max-width:1080px;margin:4rem auto 0;padding:0 16px}}
    .sect-head{{display:flex;align-items:baseline;gap:1rem;margin-bottom:1.3rem}}
    .sect-head .no{{font-family:'Archivo Black',sans-serif;font-size:2.4rem;color:transparent;-webkit-text-stroke:1.5px rgba(236,234,228,.55)}}
    .sect-head h2{{font-family:'Archivo Black',sans-serif;text-transform:uppercase;font-size:clamp(1.15rem,3vw,1.55rem);color:#efe9dc}}
    .sect-head .sub{{color:#9aa0ab;font-size:.88rem}}
    .pattern{{display:grid;gap:14px}}
    .pattern-row{{display:grid;grid-template-columns:1fr 44px 1fr;align-items:stretch}}
    .pcell{{background:#14171d;border:1px solid rgba(255,255,255,.09);border-radius:10px;padding:1rem 1.1rem}}
    .pcell .who{{font-size:.66rem;font-weight:800;letter-spacing:.2em;text-transform:uppercase;margin-bottom:.45rem}}
    .pcell.ot .who{{color:#c8a55e}}
    .pcell.nt .who{{color:#e5303d}}
    .pcell .claim{{font-weight:700;color:#eceae4;line-height:1.35}}
    .pcell .kjv{{margin-top:.55rem;font-size:.86rem;color:#d8b9b9;border-left:3px solid #c1121f;padding:.35rem 0 .35rem .7rem;line-height:1.5}}
    .pcell .kjv b{{color:#e5303d;font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;display:block;margin-bottom:.15rem}}
    .plink{{display:grid;place-items:center;font-family:'Archivo Black',sans-serif;color:#e5303d;font-size:1.1rem}}
    .pattern-note{{color:#9aa0ab;font-size:.92rem;max-width:640px;margin:1.2rem auto 0;text-align:center}}
    @media(max-width:680px){{.pattern-row{{grid-template-columns:1fr}}.plink{{padding:.2rem 0;transform:rotate(90deg)}}}}
    .meat{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}}
    .meat-card{{background:#14171d;border:1px solid rgba(255,255,255,.09);border-radius:12px;padding:1.2rem 1.3rem}}
    .meat-card h3{{font-family:'Archivo Black',sans-serif;text-transform:uppercase;font-size:.92rem;margin:0 0 .55rem;color:#efe9dc}}
    .meat-card h3 span{{color:#e5303d}}
    .meat-card p{{font-size:.92rem;color:#c8ccd4;line-height:1.65}}
    .meat-card .kjv{{margin-top:.7rem;font-size:.86rem;color:#d8b9b9;border-left:3px solid #c1121f;padding:.3rem 0 .3rem .7rem}}
    .meat-card .kjv b{{color:#e5303d;font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;display:block}}
    .today-box{{max-width:680px;margin:0 auto;background:linear-gradient(160deg,#1a1210,#14171d 60%);border:1px solid rgba(200,165,94,.35);border-radius:14px;padding:1.6rem 1.7rem}}
    .today-box p{{color:#d9d4c8;line-height:1.75}}
    .today-box p+p{{margin-top:.8rem}}
    .today-box .q{{font-family:'Archivo Black',sans-serif;text-transform:uppercase;font-size:1.02rem;color:#c8a55e;margin-bottom:.8rem}}
    .journey{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}}
    .j-card{{display:block;background:#14171d;border:1px solid rgba(255,255,255,.09);border-radius:12px;overflow:hidden;text-decoration:none;color:inherit;transition:transform .18s ease,border-color .18s ease}}
    .j-card:hover{{transform:translateY(-4px);border-color:#e5303d}}
    .j-card img{{width:100%;aspect-ratio:16/10;object-fit:cover;opacity:.85}}
    .j-card .pad{{padding:.9rem 1rem 1.1rem}}
    .j-card .k{{font-size:.64rem;font-weight:800;letter-spacing:.2em;text-transform:uppercase;color:#e5303d}}
    .j-card .t{{font-weight:800;color:#eceae4;margin-top:.25rem}}
    .j-card .s{{font-size:.82rem;color:#9aa0ab;margin-top:.2rem}}
    .sub-cta{{margin:2.4rem auto 0;max-width:680px;text-align:center;background:#14171d;border:2px solid #c1121f;border-radius:14px;padding:1.5rem 1.4rem;box-shadow:0 0 40px rgba(193,18,31,.25)}}
    .sub-cta h3{{font-family:'Archivo Black',sans-serif;text-transform:uppercase;font-size:1.15rem;color:#efe9dc;margin:0}}
    .sub-cta p{{color:#9aa0ab;font-size:.92rem;margin:.5rem 0 1rem}}
    .sub-cta a,.sub-cta span.soon{{display:inline-block;background:#c1121f;color:#fff;font-weight:800;letter-spacing:.1em;text-transform:uppercase;font-size:.8rem;padding:.75rem 1.5rem;border-radius:8px;text-decoration:none}}
    .sub-cta a:hover{{background:#e5303d}}
    .sub-cta span.soon{{background:#2a2e36;color:#9aa0ab}}
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
        scored = [h for h in sorted((batch / "visual").glob("*_scored.mp4"))
                  if ".bak" not in h.name]  # never frame a parked backup
    if not scored:
        print(f"  !! no scored mp4 for {item['slug']} - skipping frames")
        return 0
    video = scored[0]
    out_dir.mkdir(parents=True, exist_ok=True)
    n = wrote = 0
    for i, beat in enumerate(spec["beats"], 1):
        dest = out_dir / f"beat_{i:02d}.jpg"
        n += 1
        if dest.exists() and not force:
            continue
        t0, t1 = beat["t"]
        t = min(max(t0 + 0.8 * (t1 - t0), t0 + 0.3), t1 - 0.15)
        dest.unlink(missing_ok=True)  # ffmpeg -ss past EOF exits 0 writing nothing
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(video),
             "-frames:v", "1", "-vf", f"scale={FRAME_W}:-2", "-q:v", str(JPEG_Q), str(dest)],
            check=True)
        if dest.is_file():
            wrote += 1
    if wrote == n:
        # every frame was (re)cut from THIS video in THIS run -> stamp provenance
        # (SYNC-G5 freshness, v2/RELEASE_SYNC.md)
        import hashlib
        h = hashlib.sha256()
        with open(video, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        (out_dir / "_meta.json").write_text(json.dumps(
            {"source_video": video.name, "source_sha": h.hexdigest()}, indent=2),
            encoding="utf-8")
    elif wrote:
        # MIXED provenance (some frames kept from an older video, some new) — a
        # stamp would launder it as fresh (red-team C3). Drop any old stamp so the
        # SYNC gate WARNs until a full --force re-extract.
        (out_dir / "_meta.json").unlink(missing_ok=True)
        print(f"  !! {item['slug']}: {wrote}/{n} frames re-cut - mixed provenance, "
              "_meta dropped; run with --force to re-cut all beats")
    return n


def sect_head(no: str, title: str, sub: str) -> str:
    return (f'<div class="sect-head"><span class="no">{esc(no)}</span>'
            f'<h2>{esc(title)}</h2><span class="sub">{esc(sub)}</span></div>')


def render_pattern(study: dict) -> str:
    rows = study.get("pattern") or []
    if not rows:
        return ""
    parts = ['<section class="sect" id="pattern">',
             sect_head("02", "The pattern",
                       slopless(study.get("pattern_lead", "The Old Testament draws the outline. The New Testament fills it in."))),
             '<div class="pattern">']
    for row in rows:
        cells = []
        for side in ("ot", "nt"):
            c = row.get(side) or {}
            cells.append(
                f'<div class="pcell {side}"><div class="who">{esc(slopless(c.get("who", "")))}</div>'
                f'<div class="claim">{esc(slopless(c.get("claim", "")))}</div>'
                f'<div class="kjv"><b>{esc(c.get("ref", ""))}</b>"{esc(slopless(c.get("kjv", "")))}"</div></div>')
        parts.append(f'<div class="pattern-row">{cells[0]}<div class="plink">&rarr;</div>{cells[1]}</div>')
    parts.append("</div>")
    note = slopless(study.get("pattern_note", ""))
    if note:
        parts.append(f'<p class="pattern-note">{esc(note)}</p>')
    parts.append("</section>")
    return "\n".join(parts)


def render_meat(study: dict) -> str:
    cards = study.get("meat") or []
    if not cards:
        return ""
    parts = ['<section class="sect" id="meat">',
             sect_head("03", "The meat", "for the ones who want to dig"),
             '<div class="meat">']
    for c in cards:
        kjv = ""
        if c.get("kjv"):
            kjv = f'<div class="kjv"><b>{esc(c.get("ref", ""))}</b>{esc(slopless(c["kjv"]))}</div>'
        parts.append(f'<div class="meat-card"><h3>{esc(slopless(c.get("title", "")))}</h3>'
                     f'<p>{esc(slopless(c.get("body", "")))}</p>{kjv}</div>')
    parts.append("</div></section>")
    return "\n".join(parts)


def render_today(study: dict) -> str:
    today = study.get("today") or {}
    if not today.get("paras"):
        return ""
    parts = ['<section class="sect" id="today">',
             sect_head("04", "Today", "why this is in your feed"),
             '<div class="today-box">']
    if today.get("q"):
        parts.append(f'<p class="q">"{esc(slopless(today["q"]))}"</p>')
    for p in today["paras"]:
        parts.append(f"<p>{esc(slopless(p))}</p>")
    parts.append("</div></section>")
    return "\n".join(parts)


def render_journey(slug: str, n_beats: int, nxt: dict | None, yt_url: str) -> str:
    parts = ['<section class="sect">',
             sect_head("&rarr;", "Keep going", "the story does not stop here"),
             '<div class="journey">']
    if nxt:
        parts.append(f'<a class="j-card" href="{esc(nxt["slug"])}.html">'
                     f'<img loading="lazy" src="../assets/study/read/{esc(nxt["slug"])}/beat_01.jpg" alt="{esc(nxt["title"])}">'
                     f'<div class="pad"><span class="k">Next study</span><div class="t">{esc(nxt["title"])}</div>'
                     f'<div class="s">{esc(nxt.get("ref", ""))}</div></div></a>')
    mid = max(1, n_beats // 2)
    parts.append(f'<a class="j-card" href="../catalogue.html">'
                 f'<img loading="lazy" src="../assets/study/read/{slug}/beat_{mid:02d}.jpg" alt="Catalogue">'
                 f'<div class="pad"><span class="k">Explore</span><div class="t">Every study</div>'
                 f'<div class="s">Season by season: the whole Bible, through Jesus.</div></div></a>')
    parts.append(f'<a class="j-card" href="../plan.html">'
                 f'<img loading="lazy" src="../assets/study/read/{slug}/beat_{n_beats:02d}.jpg" alt="The Plan">'
                 f'<div class="pad"><span class="k">The plan</span><div class="t">What is coming</div>'
                 f'<div class="s">We build in the open. See what is next.</div></div></a>')
    parts.append("</div>")
    if yt_url:
        cta = f'<a href="{esc(yt_url)}">Subscribe on YouTube</a>'
    else:
        cta = '<span class="soon">Launching on YouTube soon</span>'
    parts.append('<div class="sub-cta"><h3>New studies every week</h3>'
                 '<p>60-second films on YouTube. The full studies live here.</p>'
                 f'{cta}</div></section>')
    return "\n".join(parts)


def render_read_page(item: dict, spec: dict, slug: str, narration_text: str,
                     study: dict | None = None, nxt: dict | None = None,
                     yt_url: str = "") -> str:
    title = item["title"]
    ref = item.get("ref", "")
    hook = slopless(item.get("public_hook", ""))
    canonical = f"https://awakeden.com/read/{slug}.html"
    og = f"https://awakeden.com/assets/study/read/{slug}/beat_01.jpg"
    parts = [chrome_top(f"Read: {title}", hook or f"{title}, hand-inked and readable panel by panel.",
                        canonical, og)]
    parts.append(f'<div class="page-hero"><h1>{esc(title)}</h1>'
                 f'<p class="hero-lead">{esc(hook)}</p></div>')
    yt = (item.get("youtube_id") or "").strip()
    if yt:
        watch = (
            f'<p><a class="watch-btn" href="#" onclick="document.getElementById(\'yt-modal\').style.display=\'flex\';'
            f'document.getElementById(\'yt-frame\').src=\'https://www.youtube-nocookie.com/embed/{yt}?autoplay=1\';return false;">'
            '&#9654;&nbsp; Watch the film</a></p>'
            '<div id="yt-modal" style="display:none;position:fixed;inset:0;background:rgba(10,8,6,.92);'
            'z-index:99;align-items:center;justify-content:center;flex-direction:column" '
            'onclick="this.style.display=\'none\';document.getElementById(\'yt-frame\').src=\'\';">'
            '<div style="width:min(92vw,960px);aspect-ratio:16/9">'
            '<iframe id="yt-frame" style="width:100%;height:100%;border:0" allow="autoplay; fullscreen" '
            'allowfullscreen></iframe></div>'
            '<p style="color:#f5f0d0;font-size:.85rem;margin-top:.8rem">click anywhere to close</p></div>'
            '<style>.watch-btn{display:inline-block;background:#a8231d;color:#f5f0d0;font-weight:700;'
            'padding:.55em 1.3em;border-radius:6px;text-decoration:none}.watch-btn:hover{background:#c22b24}</style>')
    else:
        watch = '<p>Every panel below is a frame from the finished film, in order. ' \
                'Scripture is in red. The video version is coming to YouTube.</p>'
    parts.append('<div class="read-meta">'
                 f'<p class="verse">{esc(ref)} &middot; KJV</p>'
                 f'{watch}</div>')
    study = study or {}
    if study.get("pattern") or study.get("meat") or (study.get("today") or {}).get("paras"):
        track = ['<a href="#story"><b>1</b> The story</a>']
        if study.get("pattern"):
            track.append('<a href="#pattern"><b>2</b> The pattern</a>')
        if study.get("meat"):
            track.append('<a href="#meat"><b>3</b> The meat</a>')
        if (study.get("today") or {}).get("paras"):
            track.append('<a href="#today"><b>4</b> Today</a>')
        parts.append(f'<nav class="depth-track" aria-label="Depth" style="margin-bottom:2rem">{"".join(track)}</nav>')
    splash_beat = study.get("splash_beat") or 0
    splash_text = slopless(study.get("splash_text", ""))
    parts.append('<div class="strip" id="story">')
    for i, beat in enumerate(spec["beats"], 1):
        img = f"../assets/study/read/{slug}/beat_{i:02d}.jpg"
        alt = esc(slopless((beat.get("cap") or {}).get("text", "")))
        if i == splash_beat:
            roar = f'<span class="roar">{esc(splash_text)}</span>' if splash_text else ""
            parts.append(f'<figure class="splash"><img loading="lazy" src="{img}" alt="{alt}">{roar}</figure>')
        else:
            parts.append(f'<figure><img loading="lazy" src="{img}" alt="Panel {i}: {alt}">'
                         f'<figcaption>{beat_caption(beat)}</figcaption></figure>')
    parts.append("</div>")
    if narration_text:
        parts.append('<div class="read-text"><h2>The narration</h2>'
                     f'<p>{esc(slopless(narration_text))}</p></div>')
    parts.append(render_pattern(study))
    parts.append(render_meat(study))
    parts.append(render_today(study))
    parts.append(render_journey(slug, len(spec["beats"]), nxt, yt_url))
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


def render_plan(items: list[dict], read_slugs: set[str], series: list[dict] | None = None) -> str:
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
    series_order = [s["slug"] for s in (series or [])]
    series_title = {s["slug"]: s["title"] for s in (series or [])}

    def by_series(rows: list[dict]) -> list[dict]:
        return sorted(rows, key=lambda i: (
            series_order.index(i.get("series_id")) if i.get("series_id") in series_order else 99,
            i.get("cluster_order") or 99))

    parts.append('<div class="plan-cols">')
    for label, statuses, note in PLAN_GROUPS:
        rows = by_series([i for i in items if i.get("public_status") in statuses])
        parts.append(f'<div class="plan-col"><h2>{esc(label)}</h2><p class="plan-note">{esc(note)}</p>')
        last_series = None
        for i in rows:
            sid = i.get("series_id")
            if sid != last_series:
                parts.append(f'<p class="plan-series">{esc(series_title.get(sid, sid or ""))}</p>')
                last_series = sid
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

    yt_url = ""
    cfg_p = SITE_DIR / "config.yaml"
    if cfg_p.is_file():
        cfg = yaml.safe_load(cfg_p.read_text(encoding="utf-8")) or {}
        yt_url = (((cfg.get("social") or {}).get("youtube") or {}).get("url") or "").strip()

    entries: list[dict] = []
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
        study = None
        st_p = batch / "study.json"
        if st_p.is_file():
            study = json.loads(st_p.read_text(encoding="utf-8"))
        entries.append({"item": item, "spec": spec, "slug": slug, "narration": narration,
                        "study": study, "title": item["title"], "ref": item.get("ref", "")})

    entries.sort(key=lambda e: e["title"])
    pages: list[dict] = []
    for i, e in enumerate(entries):
        nxt = entries[(i + 1) % len(entries)] if len(entries) > 1 else None
        nxt_page = {"slug": nxt["slug"], "title": nxt["title"], "ref": nxt["ref"]} if nxt else None
        (READ_DIR / f"{e['slug']}.html").write_text(
            render_read_page(e["item"], e["spec"], e["slug"], e["narration"],
                             study=e["study"], nxt=nxt_page, yt_url=yt_url), encoding="utf-8")
        pages.append({"slug": e["slug"], "title": e["title"], "ref": e["ref"]})
        extras = " + study" if e["study"] else ""
        print(f"  read/{e['slug']}.html  ({len(e['spec']['beats'])} panels{extras})")
    (READ_DIR / "index.html").write_text(render_read_index(pages), encoding="utf-8")
    (SITE_DIR / "plan.html").write_text(
        render_plan(items, {p["slug"] for p in pages}, manifest.get("series")), encoding="utf-8")
    print(f"built read/index.html ({len(pages)} strips) + plan.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
