#!/usr/bin/env python
"""POC only — lives under _poc_comic_elevate/. Does NOT modify production code.

Elevate Pierced (Zech 12:10) into a harder graphic-comic animated strip:
  1) HF Seedream stills (bold ink)
  2) HF Kling camera-only clips
  3) ffmpeg comic-page assembly (borders, gutters, caption bands)
  4) COMPARE.html current vs elevated

Usage:
  .venv\\Scripts\\python.exe _poc_comic_elevate\\run_poc.py --stage stills
  .venv\\Scripts\\python.exe _poc_comic_elevate\\run_poc.py --stage animate
  .venv\\Scripts\\python.exe _poc_comic_elevate\\run_poc.py --stage assemble
  .venv\\Scripts\\python.exe _poc_comic_elevate\\run_poc.py --stage all
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POC = Path(__file__).resolve().parent / "pierced"
STILLS = POC / "stills"
CLIPS = POC / "clips"
CURRENT = POC / "current"
WORK = POC / "work"
HF = Path.home() / "bin" / "hf.exe"
PY = ROOT / ".venv" / "Scripts" / "python.exe"
SRC = ROOT / "batches" / "cluster_01_cross" / "pierced_zech1210"

# Harder comic look than production STYLE — POSITIVES ONLY (seedream no-negative channel)
INK = (
    " Prestige biblical GRAPHIC-NOVEL splash illustration: ultra-bold black ink outlines, "
    "thick hand-inked contours, flat cel-shaded limited comic palette of deep indigo, "
    "warm ochre, ivory, and crimson blood only where wounded, heavy ink cross-hatching "
    "in the shadows, high-contrast poster composition, matte printed paper texture, "
    "dramatic comic framing, sacred and reverent mature tone, single full-bleed image "
    "filling the frame."
)

# Six elevated panels — more extreme comic composition than the production stills
PANELS = [
    {
        "slug": "p01_spear_raised",
        "caption": "A Roman soldier raised his spear",
        "kw": "SPEAR",
        "move": (
            "ONE slow steady continuous crane ascent along the raised spear shaft, "
            "rising with gentle sideways parallax until the crucified figure above fills more of frame"
        ),
        "prompt": (
            "extreme low-angle looking steeply UP at a 1st-century Roman soldier from behind, "
            "both arms thrusting a long iron-tipped spear almost vertically into a black storm sky, "
            "his bronze helmet and red cloak silhouette against lightning-rimmed clouds, "
            "far above at the tip of the spear the tiny silhouette of three rough crosses on a hill, "
            "worm's-eye comic splash composition, the spear shaft a bold black diagonal ruling the page, "
            "vertical 9:16, 1st-century Judea"
        ),
    },
    {
        "slug": "p02_the_word",
        "caption": "The LORD himself claims the wound",
        "kw": "LORD",
        "move": (
            "ONE slow steady continuous push-in toward the aged prophet's lifted face and the scroll"
        ),
        "prompt": (
            "an aged Hebrew prophet on a flat rooftop at night, face lifted to a dense field of sharp stars, "
            "one open hand pressed to his own chest as if claiming a wound, a rolled parchment scroll "
            "held tight under his other arm, moonlit stone city of Jerusalem sleeping below, "
            "bold silhouette against the star field, dramatic comic night palette of indigo and silver, "
            "vertical 9:16, 5th-century-BC Judea"
        ),
    },
    {
        "slug": "p03_pierced",
        "caption": "They shall look upon me whom they have pierced",
        "kw": "PIERCED",
        "move": (
            "ONE slow steady continuous push-in toward the wound where spear meets side, "
            "keeping the shaft and the wound centred"
        ),
        "prompt": (
            "close dramatic comic panel of the crucified Christ in a plain linen loincloth, "
            "a long Roman spear driven upward into his side under the ribs, iron spearhead sunk deep, "
            "a stream of dark blood and clear water running down the wood grain of the cross, "
            "his head bowed, thorn crown, storm-black sky, high-contrast ink shadows on the ribs and arm, "
            "the wound is the clear focal point, reverent not horror, vertical 9:16, 1st-century Judea"
        ),
    },
    {
        "slug": "p04_mourn",
        "caption": "Look upon ME. Mourn for HIM.",
        "kw": "MOURN",
        "move": (
            "ONE slow steady continuous push-in toward the three upturned tearful faces"
        ),
        "prompt": (
            "extreme close comic crop of three different 1st-century Judean faces stacked tight in frame, "
            "men and women, eyes lifted upward toward a warm light above the frame, tears catching the light, "
            "grief and sudden recognition breaking on each face, bold ink linework on brows and eyes, "
            "deep indigo shadow, warm rim light, vertical 9:16, 1st-century Judea"
        ),
    },
    {
        "slug": "p05_grace_pour",
        "caption": "I will pour… the spirit of grace",
        "kw": "POUR",
        "move": (
            "ONE slow steady continuous upward crane through the poured light, "
            "gentle lateral drift, lifting toward the radiant break in the sky"
        ),
        "prompt": (
            "comic splash of warm golden light pouring like a waterfall of liquid gold from a single "
            "violent tear in heavy black storm clouds, the poured light is the subject, "
            "small silhouette of three crosses on a hill receiving the pour, "
            "the city of Jerusalem tiny below, extreme graphic contrast of black cloud vs molten gold light, "
            "vertical 9:16, ancient Judea"
        ),
    },
    {
        "slug": "p06_look_live",
        "caption": "Look, and live.",
        "kw": "LIVE",
        "move": (
            "ONE slow steady continuous push-in toward the kneeling figure under the long cross shadow"
        ),
        "prompt": (
            "dawn comic landing panel: a single small kneeling figure in a rough cloak, head lifted, "
            "looking up the long sharp black shadow of a cross stretched across pale gold dust, "
            "soft low morning light breaking over the ridge, wide negative space of empty sky above, "
            "hope and stillness, bold simple shapes, vertical 9:16, 1st-century Judea"
        ),
    },
]

INK_ANIM_BASE = (
    "A finished inked graphic-novel comic panel — flat printed art with bold black ink outlines, "
    "cel-flat color and cross-hatching. Animate it as {move}. The drawing itself never moves, "
    "redraws, repaints, breathes or changes; the ink lines and flat colors stay exactly as printed; "
    "only the camera moves. No hard cuts, no dissolves, no morphing, no subject motion, no limbs "
    "moving, no new lines drawn. INVENT NOTHING: show ONLY what is already inked in this exact panel. "
    "Keep the subject whole in frame."
)


def _run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    print(">>", " ".join(str(c) for c in cmd[:8]), "..." if len(cmd) > 8 else "")
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)


def _download(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    # prefer curl; fall back to urllib
    r = _run(["curl", "-sL", url, "-o", str(dest)])
    if dest.exists() and dest.stat().st_size > 1000:
        return True
    try:
        import urllib.request
        urllib.request.urlretrieve(url, dest)
        return dest.exists() and dest.stat().st_size > 1000
    except Exception as e:
        print(f"download fail: {e}")
        return False


def stage_copy_current():
    """Copy production stills + final for side-by-side."""
    CURRENT.mkdir(parents=True, exist_ok=True)
    map_ = {
        "p01_spear_raised": "spear_thrust_up",
        "p02_the_word": "zechariah_night_scroll",
        "p03_pierced": "blood_water_wood",
        "p04_mourn": "look_up_faces",
        "p05_grace_pour": "grace_poured_sky",
        "p06_look_live": "us_under_cross_shadow",
    }
    vis = SRC / "visual"
    for new, old in map_.items():
        for ext in (".png",):
            src = vis / f"{old}{ext}"
            if src.exists():
                shutil.copy2(src, CURRENT / f"{new}_current.png")
        clip = vis / "clips" / f"{old}.mp4"
        if clip.exists():
            shutil.copy2(clip, CURRENT / f"{new}_current.mp4")
    final = vis / "pierced_zech1210_sfx.mp4"
    if not final.exists():
        final = vis / "pierced_zech1210_scored.mp4"
    if final.exists():
        shutil.copy2(final, CURRENT / "current_final.mp4")
    print(f"copied current assets → {CURRENT}")


def stage_stills(*, only: set[str] | None = None, force: bool = False):
    STILLS.mkdir(parents=True, exist_ok=True)
    for p in PANELS:
        slug = p["slug"]
        if only and slug not in only:
            continue
        out = STILLS / f"{slug}.png"
        if out.exists() and not force:
            print(f"[skip] {slug} exists")
            continue
        prompt = p["prompt"] + INK
        cmd = [
            str(HF), "generate", "create", "seedream_v4_5",
            "--prompt", prompt,
            "--aspect_ratio", "9:16",
            "--quality", "high",
            "--wait",
            "--json",
        ]
        print(f"\n=== STILL {slug} (1 credit) ===")
        r = _run(cmd, timeout=300)
        blob = (r.stdout or "") + (r.stderr or "")
        print(blob[-800:] if len(blob) > 800 else blob)
        url = None
        # try JSON parse
        try:
            data = json.loads(r.stdout or "{}")
            # various HF shapes
            if isinstance(data, dict):
                for key in ("url", "image_url", "result_url"):
                    if data.get(key):
                        url = data[key]
                raw = json.dumps(data)
                m = re.search(r'https?://[^\s"]+\.(?:png|jpg|jpeg|webp)', raw, re.I)
                if m:
                    url = m.group(0)
        except json.JSONDecodeError:
            pass
        if not url:
            m = re.search(r'https?://[^\s"]+\.(?:png|jpg|jpeg|webp)', blob, re.I)
            if m:
                url = m.group(0).rstrip(")',\"")
        if not url:
            m = re.search(r'https?://[^\s"]+', blob)
            if m and "http" in m.group(0):
                url = m.group(0).rstrip(")',\"")
        if not url:
            print(f"FAIL no url for {slug}")
            continue
        if _download(url, out):
            print(f"SAVED {out} ({out.stat().st_size} bytes)")
        else:
            print(f"FAIL download {slug}")


def stage_animate(*, only: set[str] | None = None, force: bool = False):
    CLIPS.mkdir(parents=True, exist_ok=True)
    os.environ["JITB_SKIP_STILL_GATE"] = "1"
    sys.path.insert(0, str(ROOT))
    from _hf_animate_short import hf_animate

    for p in PANELS:
        slug = p["slug"]
        if only and slug not in only:
            continue
        still = STILLS / f"{slug}.png"
        out = CLIPS / f"{slug}.mp4"
        if not still.exists():
            print(f"[skip] no still for {slug}")
            continue
        if out.exists() and not force:
            print(f"[skip] clip {slug} exists")
            continue
        prompt = INK_ANIM_BASE.format(move=p["move"])
        print(f"\n=== ANIMATE {slug} (~12.5 credits) ===")
        ok = hf_animate(still, out, prompt, duration=5, aspect_ratio="9:16")
        print(f"{'OK' if ok else 'FAIL'} {out if ok else slug}")


def _make_paper(w: int, h: int, path: Path):
    from PIL import Image, ImageDraw, ImageFilter
    import random
    img = Image.new("RGB", (w, h), (242, 232, 210))
    px = img.load()
    rnd = random.Random(42)
    # fine grain / halftone-ish
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            n = rnd.randint(-12, 8)
            r, g, b = px[x, y]
            px[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n - 2)), max(0, min(255, b + n - 4)))
    # subtle vignette
    draw = ImageDraw.Draw(img, "RGBA")
    for i in range(40):
        a = int(4 + i * 0.8)
        draw.rectangle([i, i, w - 1 - i, h - 1 - i], outline=(60, 40, 20, a))
    img.save(path)


def _wobbled_border(draw, box, width=10, color=(12, 10, 8), seed=0):
    """Hand-inked-ish rectangle (slight wobble)."""
    import random
    x0, y0, x1, y1 = box
    rnd = random.Random(seed)
    pts_top = []
    pts_bot = []
    pts_left = []
    pts_right = []
    steps = 24
    for i in range(steps + 1):
        t = i / steps
        jx = rnd.randint(-2, 2)
        jy = rnd.randint(-2, 2)
        pts_top.append((int(x0 + (x1 - x0) * t) + jx, y0 + jy))
        pts_bot.append((int(x0 + (x1 - x0) * t) + jx, y1 + jy))
        pts_left.append((x0 + jx, int(y0 + (y1 - y0) * t) + jy))
        pts_right.append((x1 + jx, int(y0 + (y1 - y0) * t) + jy))
    for pts in (pts_top, pts_bot, pts_left, pts_right):
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i + 1]], fill=color, width=width)


def _caption_band(img, text: str, kw: str, y_bottom: int):
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(img)
    w, h = img.size
    band_h = 110
    y0 = y_bottom - band_h - 24
    # torn parchment band
    draw.rectangle([40, y0, w - 40, y0 + band_h], fill=(236, 220, 185), outline=(20, 14, 10), width=4)
    # jagged top edge marks
    for x in range(50, w - 50, 18):
        draw.line([(x, y0 - 3), (x + 6, y0 + 2), (x + 12, y0 - 2)], fill=(20, 14, 10), width=2)
    try:
        font = ImageFont.truetype("arial.ttf", 36)
        font_kw = ImageFont.truetype("arialbd.ttf", 40)
    except Exception:
        font = ImageFont.load_default()
        font_kw = font
    # word wrap
    words = text.split()
    lines, cur = [], ""
    for word in words:
        test = (cur + " " + word).strip()
        if draw.textlength(test, font=font) < w - 100:
            cur = test
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    ty = y0 + 22
    for line in lines[:2]:
        # word-by-word so keyword is red WITHOUT double-drawing (no garbled overlap)
        x = 56
        low_kw = (kw or "").lower()
        for word in line.split(" "):
            clean = word.strip(".,;:!?…")
            is_kw = bool(low_kw) and clean.lower() == low_kw
            f = font_kw if is_kw else font
            color = (160, 20, 20) if is_kw else (25, 18, 12)
            draw.text((x, ty), word + " ", fill=color, font=f)
            x += int(draw.textlength(word + " ", font=f))
        ty += 42


def _frame_panel(clip_or_png: Path, caption: str, kw: str, out_png: Path, *, border_break: bool = False):
    """Composite one comic page frame (static) from first frame of clip or still."""
    from PIL import Image, ImageDraw, ImageEnhance
    WORK.mkdir(parents=True, exist_ok=True)
    W, H = 1080, 1920
    paper = WORK / "_paper.png"
    if not paper.exists():
        _make_paper(W, H, paper)
    page = Image.open(paper).convert("RGB")

    # extract art
    art_path = WORK / f"_art_{out_png.stem}.png"
    if clip_or_png.suffix.lower() == ".mp4":
        _run([
            "ffmpeg", "-y", "-ss", "0.3", "-i", str(clip_or_png),
            "-frames:v", "1", str(art_path),
        ])
    else:
        shutil.copy2(clip_or_png, art_path)
    art = Image.open(art_path).convert("RGB")
    # slight contrast punch for comic print
    art = ImageEnhance.Contrast(art).enhance(1.15)
    art = ImageEnhance.Color(art).enhance(0.95)
    art = ImageEnhance.Sharpness(art).enhance(1.2)

    margin = 28 if border_break else 48
    box_w = W - 2 * margin
    box_h = int(H * 0.78) if not border_break else int(H * 0.84)
    art = art.resize((box_w, box_h), Image.Resampling.LANCZOS)
    x0, y0 = margin, margin + (20 if not border_break else 8)
    page.paste(art, (x0, y0))
    draw = ImageDraw.Draw(page)
    # outer page ink edge
    _wobbled_border(draw, (18, 18, W - 18, H - 18), width=6, color=(18, 12, 8), seed=1)
    # panel border
    bw = 14 if not border_break else 18
    _wobbled_border(draw, (x0 - 6, y0 - 6, x0 + box_w + 6, y0 + box_h + 6), width=bw, color=(8, 6, 4), seed=7)
    # soft drop shadow under panel
    # caption band
    _caption_band(page, caption, kw, H)
    page.save(out_png)
    return out_png


def _clip_with_border(clip: Path, caption: str, kw: str, out: Path, *, border_break: bool = False, dur: float = 4.0):
    """Take 5s clip → comic-bordered page video of `dur` seconds with mild zoom."""
    from PIL import Image
    WORK.mkdir(parents=True, exist_ok=True)
    # sample mid frame for layout metrics, but actually overlay borders via filter is hard —
    # approach: pre-render bordered still frames at start/mid/end? Better: scale clip into
    # a page template video via ffmpeg overlay.

    # Build static page chrome (paper + border hole) and overlay scaled clip
    W, H = 1080, 1920
    paper = WORK / "_paper.png"
    if not paper.exists():
        _make_paper(W, H, paper)

    margin = 28 if border_break else 48
    box_w = W - 2 * margin
    box_h = int(H * 0.78) if not border_break else int(H * 0.84)
    x0, y0 = margin, margin + (20 if not border_break else 8)

    # chrome: paper with transparent hole for video — use black rect as mask region, overlay video
    chrome_path = WORK / f"chrome_{out.stem}.png"
    cap_path = WORK / f"cap_{out.stem}.png"
    from PIL import ImageDraw
    chrome = Image.open(paper).convert("RGBA")
    draw = ImageDraw.Draw(chrome)
    # dark panel well
    draw.rectangle([x0 - 8, y0 - 8, x0 + box_w + 8, y0 + box_h + 8], fill=(8, 6, 4, 255))
    _wobbled_border(draw, (18, 18, W - 18, H - 18), width=6, color=(18, 12, 8, 255), seed=1)
    _wobbled_border(draw, (x0 - 6, y0 - 6, x0 + box_w + 6, y0 + box_h + 6), width=14 if not border_break else 18,
                    color=(8, 6, 4, 255), seed=hash(out.stem) % 999)
    chrome_rgb = chrome.convert("RGB")
    chrome_rgb.save(chrome_path)

    # caption layer
    cap_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # draw band on RGB then convert
    band = Image.new("RGB", (W, H), (0, 0, 0))
    # actually draw caption on transparent by using the helper on a blank and keying — simpler:
    page_cap = Image.open(paper).convert("RGB")
    # clear most of page to a key color? Easier path: burn caption into chrome bottom only
    full = chrome_rgb.copy()
    _caption_band(full, caption, kw, H)
    full.save(chrome_path)

    # zoompan mild push on the source clip, scale into panel rect
    # ffmpeg: [0:v] scale+crop to box, [1:v] chrome; overlay
    vf = (
        f"[0:v]scale={box_w}:{box_h}:force_original_aspect_ratio=increase,"
        f"crop={box_w}:{box_h},fps=30,"
        f"zoompan=z='min(1.08,1+0.016*on/30)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d=1:s={box_w}x{box_h}:fps=30,trim=duration={dur},setpts=PTS-STARTPTS[v];"
        f"[1:v]scale={W}:{H},fps=30,trim=duration={dur},setpts=PTS-STARTPTS[bg];"
        f"[bg][v]overlay={x0}:{y0}:shortest=1,format=yuv420p"
    )
    cmd = [
        "ffmpeg", "-y",
        "-i", str(clip),
        "-loop", "1", "-i", str(chrome_path),
        "-filter_complex", vf,
        "-t", str(dur),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an",
        str(out),
    ]
    r = _run(cmd, timeout=120)
    if not out.exists():
        print((r.stderr or "")[-600:])
        return False
    # slam flash first 3 frames — mild white flash at start
    flashed = out.with_name(out.stem + "_flash.mp4")
    flash_vf = (
        "fade=t=in:st=0:d=0.12:color=white,"
        "eq=contrast=1.05:saturation=0.95"
    )
    r2 = _run([
        "ffmpeg", "-y", "-i", str(out), "-vf", flash_vf,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an", str(flashed),
    ], timeout=60)
    if flashed.exists():
        flashed.replace(out)
    return out.exists()


def stage_assemble():
    WORK.mkdir(parents=True, exist_ok=True)
    segs = []
    for i, p in enumerate(PANELS):
        slug = p["slug"]
        clip = CLIPS / f"{slug}.mp4"
        still = STILLS / f"{slug}.png"
        src = clip if clip.exists() else still
        if not src.exists():
            print(f"missing {slug}")
            continue
        seg = WORK / f"seg_{i+1:02d}_{slug}.mp4"
        # impact panel shorter punch; grace + landing a bit longer
        dur = 3.6 if i in (0, 2) else (4.2 if i in (4, 5) else 3.8)
        border_break = (i == 4)  # grace pour breaks the frame energy
        if src.suffix.lower() == ".mp4":
            ok = _clip_with_border(src, p["caption"], p["kw"], seg, border_break=border_break, dur=dur)
        else:
            # still → bordered page → short ken burns via zoompan
            page = WORK / f"page_{slug}.png"
            _frame_panel(src, p["caption"], p["kw"], page, border_break=border_break)
            _run([
                "ffmpeg", "-y", "-loop", "1", "-i", str(page),
                "-vf", f"fps=30,zoompan=z='min(1.06,1+0.012*on/30)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,trim=duration={dur}",
                "-t", str(dur), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an", str(seg),
            ], timeout=60)
            ok = seg.exists()
        if ok:
            segs.append(seg)
            print(f"seg ok {seg.name}")
        else:
            print(f"seg FAIL {slug}")

    if not segs:
        print("no segments")
        return

    # hard-cut concat (comic strip turns the page with a cut, not a dissolve)
    lst = WORK / "concat.txt"
    lst.write_text("\n".join(f"file '{s.as_posix()}'" for s in segs), encoding="utf-8")
    silent = POC / "elevated_strip_silent.mp4"
    _run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", str(silent),
    ], timeout=120)

    # mux narration excerpt if available (first ~25s of audio) — optional
    audio = SRC / "audio" / "narration.mp3"
    final = POC / "elevated_strip.mp4"
    if audio.exists() and silent.exists():
        # pad/trim audio to video length
        _run([
            "ffmpeg", "-y", "-i", str(silent), "-i", str(audio),
            "-filter_complex",
            "[1:a]atrim=0:26,apad=whole_dur=26[a];[0:v]tpad=stop_mode=clone:stop_duration=0.5[v]",
            "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-c:a", "aac", "-shortest",
            str(final),
        ], timeout=120)
        if not final.exists():
            # simpler mux
            _run([
                "ffmpeg", "-y", "-i", str(silent), "-i", str(audio),
                "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
                "-shortest", str(final),
            ], timeout=60)
    else:
        if silent.exists():
            shutil.copy2(silent, final)

    print(f"FINAL {final} exists={final.exists()}")
    stage_compare_html()


def stage_compare_html():
    """Build clickable COMPARE.html — current stills/clips vs elevated."""
    rows = []
    for p in PANELS:
        slug = p["slug"]
        cur_png = CURRENT / f"{slug}_current.png"
        new_png = STILLS / f"{slug}.png"
        cur_mp4 = CURRENT / f"{slug}_current.mp4"
        new_mp4 = CLIPS / f"{slug}.mp4"

        def rel(path: Path) -> str:
            try:
                return path.relative_to(POC).as_posix()
            except ValueError:
                return path.as_posix()

        rows.append(f"""
        <section class="row">
          <h2>{slug} — {p['caption']}</h2>
          <div class="pair">
            <figure>
              <figcaption>CURRENT production</figcaption>
              {"<img src='" + rel(cur_png) + "'/>" if cur_png.exists() else "<p>missing</p>"}
              {"<video controls loop muted src='" + rel(cur_mp4) + "'></video>" if cur_mp4.exists() else ""}
            </figure>
            <figure>
              <figcaption>ELEVATED comic POC</figcaption>
              {"<img src='" + rel(new_png) + "'/>" if new_png.exists() else "<p>missing</p>"}
              {"<video controls loop muted src='" + rel(new_mp4) + "'></video>" if new_mp4.exists() else ""}
            </figure>
          </div>
        </section>
        """)

    cur_final = CURRENT / "current_final.mp4"
    elev = POC / "elevated_strip.mp4"
    html = f"""<!doctype html>
<html><head><meta charset="utf-8"/>
<title>POC — Pierced comic elevation</title>
<style>
  body {{ font-family: Georgia, serif; background:#1a1510; color:#f2e6d0; margin:0; padding:24px; }}
  h1 {{ color:#f5d7a1; }}
  h2 {{ color:#e8c27a; border-bottom:1px solid #5a4030; padding-bottom:6px; }}
  .pair {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; }}
  figure {{ background:#2a2118; padding:12px; border:2px solid #3d2e20; border-radius:6px; margin:0; }}
  figcaption {{ font-weight:bold; margin-bottom:8px; letter-spacing:.04em; }}
  img, video {{ width:100%; max-height:640px; object-fit:contain; background:#000; }}
  .films {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:32px; }}
  .note {{ background:#2a2118; padding:16px; border-left:4px solid #c44; margin:16px 0 32px; }}
  a {{ color:#8ec8ff; }}
</style></head><body>
<h1>POC — Pierced elevated to graphic comic strip</h1>
<div class="note">
  <p><b>Source:</b> production short <code>pierced_zech1210</code></p>
  <p><b>What changed:</b> harder ink stills · camera-only Kling · always-on comic page chrome
  (paper gutters, thick hand-wobbled borders, parchment caption bands, slam flash) ·
  splash → strip → impact → grace border-break → landing.</p>
  <p><b>Temp folder only</b> — no production code or assets modified.</p>
</div>
<section class="films">
  <figure>
    <figcaption>CURRENT full short</figcaption>
    {"<video controls src='" + cur_final.relative_to(POC).as_posix() + "'></video>" if cur_final.exists() else "<p>missing final</p>"}
  </figure>
  <figure>
    <figcaption>ELEVATED strip (~24s showcase)</figcaption>
    {"<video controls src='" + elev.relative_to(POC).as_posix() + "'></video>" if elev.exists() else "<p>not built yet</p>"}
  </figure>
</section>
{''.join(rows)}
</body></html>
"""
    out = POC / "COMPARE.html"
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["copy", "stills", "animate", "assemble", "compare", "all"],
                    default="all")
    ap.add_argument("--only", default="", help="comma slugs")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    only = {x.strip() for x in a.only.split(",") if x.strip()} or None

    POC.mkdir(parents=True, exist_ok=True)
    if a.stage in ("copy", "all"):
        stage_copy_current()
    if a.stage in ("stills", "all"):
        stage_stills(only=only, force=a.force)
    if a.stage in ("animate", "all"):
        stage_animate(only=only, force=a.force)
    if a.stage in ("assemble", "all"):
        stage_assemble()
    if a.stage == "compare":
        stage_compare_html()


if __name__ == "__main__":
    main()
