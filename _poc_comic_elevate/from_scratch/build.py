#!/usr/bin/env python
"""FROM SCRATCH comic short — The Sentence (Pierced).
Temp-only. Does not touch production code or assets.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
STILLS = HERE / "stills"
CLIPS = HERE / "clips"
PAGES = HERE / "pages"
WORK = HERE / "work"
HF = Path.home() / "bin" / "hf.exe"
AUDIO = ROOT / "batches" / "cluster_01_cross" / "pierced_zech1210" / "audio" / "narration.mp3"

# Hard comic ink — positives only
INK = (
    " Prestige biblical GRAPHIC-NOVEL illustration: ultra-bold black ink outlines, "
    "thick hand-inked contours, flat cel-shaded limited palette, heavy cross-hatching "
    "in shadows, high-contrast printed-comic paper texture, sacred mature tone, "
    "single full-bleed image filling the frame, no lettering, no speech bubbles, no watermark."
)

# ORIGINAL stills — not production remakes
PANELS = [
    {
        "slug": "ink_drop",
        "caption": "Five hundred years earlier, God started a sentence.",
        "kw": "sentence",
        "move": (
            "ONE slow steady continuous push-in toward the falling ink drop "
            "and the tiny cross forming inside the splash on the parchment"
        ),
        "prompt": (
            "extreme macro of a single heavy drop of black ink falling onto aged ivory parchment, "
            "the splash-shape of the drop already spreading into the rough silhouette of a tiny cross, "
            "deep black ink on cream paper, one warm oil-lamp glow at the edge of frame, "
            "nothing else in the world exists, pure graphic-novel splash of a beginning, "
            "vertical 9:16"
        ),
    },
    {
        "slug": "century_thread",
        "caption": "One unbroken line of ink across the centuries.",
        "kw": "line",
        "move": (
            "ONE slow steady continuous lateral camera drift from left to right "
            "along the ink thread, from the prophet toward the distant hill of crosses"
        ),
        "prompt": (
            "epic wide graphic-novel landscape read left-to-right: on the far left a tiny aged prophet "
            "stands on a night rooftop under stars holding a scroll, from his quill a single continuous "
            "thick black ink thread snakes across empty moonlit desert dunes and years of blank space, "
            "and on the far right the thread ends at a small rocky hill with three rough crosses under a dark sky, "
            "the ink line is the subject that joins the two ages, bold simple shapes, vertical 9:16"
        ),
    },
    {
        "slug": "spear_tunnel",
        "caption": "A Roman spear finished the sentence.",
        "kw": "finished",
        "move": (
            "ONE slow steady continuous push forward INTO the dark tunnel of the spear shaft, "
            "traveling toward the small bright cross at the far end, never leaving the shaft"
        ),
        "prompt": (
            "FIRST-PERSON point of view looking straight down the length of a long Roman iron spear "
            "held out ahead like a dark circular tunnel, the wooden shaft and iron socket filling the edges "
            "of frame in bold black ink, at the far tiny end of the tunnel a rough wooden cross stands "
            "on a hill against a storm-lit sky, we are inside the act of piercing, claustrophobic comic composition, "
            "vertical 9:16, 1st-century"
        ),
    },
    {
        "slug": "me_him",
        "caption": "Look upon ME. Mourn for HIM.",
        "kw": "ME",
        "move": (
            "ONE extremely slow steady continuous push-in toward the centre of the split face, "
            "where the white gutter meets the two halves, almost a held breath"
        ),
        "prompt": (
            "one Near-Eastern man's face filling the frame, split cleanly down the middle by a pure white "
            "vertical gutter like a comic panel divide: the LEFT half of the face is lit with soft divine radiance "
            "and calm open eyes looking out, the RIGHT half wears a crown of thorns with a tear and a wound-shadow, "
            "same bone structure both sides, the mystery that ME and HIM are one person, "
            "bold ink linework, high contrast, vertical 9:16, reverent"
        ),
    },
    {
        "slug": "double_sight",
        "caption": "John saw a dying man — and the old sentence kept.",
        "kw": "saw",
        "move": (
            "ONE slow steady continuous push-in toward the reflection in the puddle, "
            "where the older prophetic face lives"
        ),
        "prompt": (
            "a young bearded 1st-century disciple kneels at the foot of a cross looking down into a small "
            "puddle of dark blood mixed with clear water on the stone, his real face is young and stricken, "
            "but the reflection in the puddle shows the SAME man aged into a prophet with a scroll of light "
            "behind the reflected eyes, double sight in one frame, storm dusk, bold ink, vertical 9:16"
        ),
    },
    {
        "slug": "sky_opens",
        "caption": "Not wrath. The spirit of grace.",
        "kw": "grace",
        "move": (
            "ONE slow steady continuous gentle crane upward into the open hand of light "
            "tearing the storm clouds"
        ),
        "prompt": (
            "after a biblical storm: heavy black ink clouds tearing open, the tear itself forms the soft "
            "silhouette of a vast open hand of warm light reaching down over a tiny hill with three crosses, "
            "the hand-of-light is the subject not a waterfall, gold and ivory light against indigo cloud, "
            "no liquid stream, grace as an opened hand, vertical 9:16, sacred"
        ),
    },
    {
        "slug": "eyes_live",
        "caption": "Look, and live.",
        "kw": "live",
        "move": (
            "ONE extremely slow steady continuous push-in into the eyes, "
            "until the warm light in the irises nearly fills the frame"
        ),
        "prompt": (
            "extreme close graphic-novel crop of a pair of human eyes just opening, "
            "warm dawn light catching in the brown irises, one fresh tear track on the cheek below, "
            "no other face features needed beyond brow and upper cheek, the look that becomes life, "
            "bold black ink lashes and brows, soft gold light, vertical 9:16, intimate sacred"
        ),
    },
]

INK_ANIM = (
    "A finished inked graphic-novel comic panel — flat printed art with bold black ink outlines "
    "and cel-flat color. Animate it as {move}. The drawing itself never moves, redraws, repaints, "
    "breathes or changes; only the camera moves. No hard cuts, no dissolves, no morphing, "
    "no subject motion, no new lines. INVENT NOTHING. Keep the subject whole in frame."
)


def _run(cmd, **kw):
    print(">>", " ".join(str(c) for c in cmd[:6]), "...")
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)


def stage_stills(*, only=None, force=False):
    STILLS.mkdir(parents=True, exist_ok=True)
    for p in PANELS:
        slug = p["slug"]
        if only and slug not in only:
            continue
        out = STILLS / f"{slug}.png"
        if out.exists() and not force:
            print(f"[skip] {slug}")
            continue
        prompt = p["prompt"] + INK
        cmd = [
            str(HF), "generate", "create", "seedream_v4_5",
            "--prompt", prompt, "--aspect_ratio", "9:16", "--quality", "high",
            "--wait", "--json",
        ]
        print(f"\n=== STILL {slug} ===")
        r = _run(cmd, timeout=360)
        blob = (r.stdout or "") + (r.stderr or "")
        url = None
        try:
            data = json.loads(r.stdout or "null")
            if isinstance(data, list) and data:
                url = data[0].get("result_url")
            elif isinstance(data, dict):
                url = data.get("result_url")
        except json.JSONDecodeError:
            pass
        if not url:
            m = re.search(r'https?://[^\s"]+\.png', blob)
            url = m.group(0) if m else None
        if not url:
            print("FAIL no url", blob[-400:])
            continue
        urllib.request.urlretrieve(url, out)
        print(f"SAVED {out} ({out.stat().st_size})")


def stage_redownload():
    """Pull full-res from HF list by prompt needle."""
    r = _run([str(HF), "generate", "list", "--json"], timeout=60)
    jobs = json.loads(r.stdout)
    needles = {
        "ink_drop": "falling onto aged ivory parchment",
        "century_thread": "continuous thick black ink thread",
        "spear_tunnel": "FIRST-PERSON point of view looking straight down",
        "me_him": "split cleanly down the middle by a pure white",
        "double_sight": "reflection in the puddle shows the SAME man aged",
        "sky_opens": "silhouette of a vast open hand of warm light",
        "eyes_live": "pair of human eyes just opening",
    }
    for slug, needle in needles.items():
        match = next(
            (j for j in jobs
             if j.get("job_type") == "seedream_v4_5"
             and needle.lower() in ((j.get("params") or {}).get("prompt") or "").lower()),
            None,
        )
        if not match:
            print("no job", slug)
            continue
        url = match.get("result_url")
        dest = STILLS / f"{slug}.png"
        urllib.request.urlretrieve(url, dest)
        print(slug, dest.stat().st_size)


def stage_animate(*, only=None, force=False):
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
            print("no still", slug)
            continue
        if out.exists() and not force:
            print("[skip]", slug)
            continue
        prompt = INK_ANIM.format(move=p["move"])
        print(f"\n=== ANIM {slug} ===")
        ok = hf_animate(still, out, prompt, duration=5, aspect_ratio="9:16")
        print("OK" if ok else "FAIL", slug)


def _paper(w, h):
    from PIL import Image
    import random
    img = Image.new("RGB", (w, h), (240, 230, 208))
    px = img.load()
    rnd = random.Random(7)
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            n = rnd.randint(-10, 8)
            r, g, b = px[x, y]
            px[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n - 1)), max(0, min(255, b + n - 3)))
    return img


def _border(draw, box, width=12, seed=0):
    import random
    x0, y0, x1, y1 = box
    rnd = random.Random(seed)
    steps = 20

    def side(pts):
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i + 1]], fill=(10, 8, 6), width=width)

    top = [(int(x0 + (x1 - x0) * i / steps) + rnd.randint(-2, 2), y0 + rnd.randint(-2, 2)) for i in range(steps + 1)]
    bot = [(int(x0 + (x1 - x0) * i / steps) + rnd.randint(-2, 2), y1 + rnd.randint(-2, 2)) for i in range(steps + 1)]
    lef = [(x0 + rnd.randint(-2, 2), int(y0 + (y1 - y0) * i / steps) + rnd.randint(-2, 2)) for i in range(steps + 1)]
    rig = [(x1 + rnd.randint(-2, 2), int(y0 + (y1 - y0) * i / steps) + rnd.randint(-2, 2)) for i in range(steps + 1)]
    for s in (top, bot, lef, rig):
        side(s)


def _caption(img, text, kw, y_bottom):
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(img)
    w, h = img.size
    band_h = 120
    y0 = y_bottom - band_h - 20
    draw.rectangle([36, y0, w - 36, y0 + band_h], fill=(234, 218, 182), outline=(18, 12, 8), width=4)
    try:
        font = ImageFont.truetype("arial.ttf", 34)
        font_kw = ImageFont.truetype("arialbd.ttf", 36)
    except Exception:
        font = ImageFont.load_default()
        font_kw = font
    # wrap
    words = text.split()
    lines, cur = [], ""
    for word in words:
        test = (cur + " " + word).strip()
        if draw.textlength(test, font=font) < w - 90:
            cur = test
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    ty = y0 + 20
    low_kw = (kw or "").lower()
    for line in lines[:2]:
        x = 50
        for word in line.split(" "):
            clean = word.strip(".,;:!?…\"'").lower()
            is_kw = bool(low_kw) and clean == low_kw
            f = font_kw if is_kw else font
            color = (150, 18, 18) if is_kw else (22, 16, 10)
            draw.text((x, ty), word + " ", fill=color, font=f)
            x += int(draw.textlength(word + " ", font=f))
        ty += 40


def _fit(im, tw, th):
    from PIL import Image
    im = im.convert("RGB")
    scale = max(tw / im.width, th / im.height)
    nw, nh = int(im.width * scale), int(im.height * scale)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return im.crop((left, top, left + tw, top + th))


def _frame_from_clip(clip: Path, t: float, dest: Path):
    _run(["ffmpeg", "-y", "-ss", str(t), "-i", str(clip), "-frames:v", "1", str(dest)], timeout=30)


def build_page_strip(p_top, p_bot, out_png, caption, kw):
    """True 2-panel vertical comic page."""
    from PIL import Image, ImageDraw, ImageEnhance
    W, H = 1080, 1920
    page = _paper(W, H)
    gutter = 28
    margin = 40
    cap_space = 150
    usable_h = H - margin * 2 - gutter - cap_space
    ph = usable_h // 2
    pw = W - margin * 2

    def load_art(p):
        clip = CLIPS / f"{p['slug']}.mp4"
        still = STILLS / f"{p['slug']}.png"
        tmp = WORK / f"_fr_{p['slug']}.png"
        WORK.mkdir(exist_ok=True)
        if clip.exists():
            _frame_from_clip(clip, 1.5, tmp)
            art = Image.open(tmp)
        else:
            art = Image.open(still)
        art = ImageEnhance.Contrast(art.convert("RGB")).enhance(1.12)
        return _fit(art, pw, ph)

    a1 = load_art(p_top)
    a2 = load_art(p_bot)
    y1 = margin
    y2 = margin + ph + gutter
    page.paste(a1, (margin, y1))
    page.paste(a2, (margin, y2))
    draw = ImageDraw.Draw(page)
    _border(draw, (margin - 4, y1 - 4, margin + pw + 4, y1 + ph + 4), width=10, seed=11)
    _border(draw, (margin - 4, y2 - 4, margin + pw + 4, y2 + ph + 4), width=10, seed=22)
    _border(draw, (16, 16, W - 16, H - 16), width=5, seed=3)
    _caption(page, caption, kw, H)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    page.save(out_png)
    return out_png


def build_page_splash(p, out_png, caption=None, kw=None):
    from PIL import Image, ImageDraw, ImageEnhance
    W, H = 1080, 1920
    page = _paper(W, H)
    margin = 44
    cap_space = 150
    pw = W - margin * 2
    ph = H - margin * 2 - cap_space
    clip = CLIPS / f"{p['slug']}.mp4"
    still = STILLS / f"{p['slug']}.png"
    tmp = WORK / f"_fr_{p['slug']}.png"
    WORK.mkdir(exist_ok=True)
    if clip.exists():
        _frame_from_clip(clip, 1.8, tmp)
        art = Image.open(tmp)
    else:
        art = Image.open(still)
    art = ImageEnhance.Contrast(art.convert("RGB")).enhance(1.12)
    art = _fit(art, pw, ph)
    page.paste(art, (margin, margin))
    draw = ImageDraw.Draw(page)
    _border(draw, (margin - 6, margin - 6, margin + pw + 6, margin + ph + 6), width=14, seed=hash(p["slug"]) % 99)
    _border(draw, (16, 16, W - 16, H - 16), width=5, seed=1)
    _caption(page, caption or p["caption"], kw or p["kw"], H)
    page.save(out_png)
    return out_png


def page_to_video(page_png: Path, clip: Path | None, out: Path, dur: float, *, motion="push"):
    """If clip given, put live clip inside the panel hole; else zoompan the page."""
    W, H = 1080, 1920
    if clip and clip.exists() and motion != "static_page":
        # simpler reliable path: zoompan the composited page (art already from mid-frame)
        # PLUS for splash pages, overlay live clip — complex. Use animated page via zoompan on still page
        # then for splash, prefer building a live-bordered clip like before.
        pass
    # Always: mild zoom on the finished comic PAGE (reads as turning/leaning into the page)
    zexpr = {
        "push": "min(1.08,1+0.014*on/30)",
        "hold": "min(1.03,1+0.005*on/30)",
        "drift": "min(1.05,1+0.008*on/30)",
    }.get(motion, "min(1.06,1+0.012*on/30)")
    vf = (
        f"fps=30,scale=1080:1920,"
        f"zoompan=z='{zexpr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d=1:s=1080x1920:fps=30,"
        f"fade=t=in:st=0:d=0.1:color=white,"
        f"trim=duration={dur},setpts=PTS-STARTPTS"
    )
    r = _run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(page_png),
        "-vf", vf, "-t", str(dur), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an", str(out),
    ], timeout=90)
    if not out.exists():
        print((r.stderr or "")[-500:])
    return out.exists()


def live_splash_video(p, out: Path, dur: float):
    """Live Kling clip inside comic chrome — the page is ALIVE."""
    from PIL import Image, ImageDraw
    W, H = 1080, 1920
    margin = 44
    cap_space = 150
    pw = W - margin * 2
    ph = H - margin * 2 - cap_space
    chrome = _paper(W, H)
    draw = ImageDraw.Draw(chrome)
    # panel well
    draw.rectangle([margin - 8, margin - 8, margin + pw + 8, margin + ph + 8], fill=(8, 6, 4))
    _border(draw, (margin - 6, margin - 6, margin + pw + 6, margin + ph + 6), width=14, seed=hash(p["slug"]) % 99)
    _border(draw, (16, 16, W - 16, H - 16), width=5, seed=1)
    _caption(chrome, p["caption"], p["kw"], H)
    chrome_path = WORK / f"chrome_{p['slug']}.png"
    WORK.mkdir(exist_ok=True)
    chrome.save(chrome_path)

    clip = CLIPS / f"{p['slug']}.mp4"
    if not clip.exists():
        return page_to_video(chrome_path, None, out, dur, motion="hold")

    # lateral drift for century_thread uses different crop bias
    if p["slug"] == "century_thread":
        z = "1.0"
        x = f"min(iw-ow, max(0, (iw-ow)*on/(30*{dur})))"  # pan left→right
        y = "(ih-oh)/2"
        inner = (
            f"[0:v]scale={pw}:{ph}:force_original_aspect_ratio=increase,"
            f"crop={pw}:{ph}:{x}:{y},fps=30,trim=duration={dur},setpts=PTS-STARTPTS[v];"
        )
    else:
        inner = (
            f"[0:v]scale={pw}:{ph}:force_original_aspect_ratio=increase,"
            f"crop={pw}:{ph},fps=30,"
            f"zoompan=z='min(1.1,1+0.018*on/30)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"d=1:s={pw}x{ph}:fps=30,trim=duration={dur},setpts=PTS-STARTPTS[v];"
        )
    vf = (
        inner +
        f"[1:v]scale={W}:{H},fps=30,trim=duration={dur},setpts=PTS-STARTPTS[bg];"
        f"[bg][v]overlay={margin}:{margin}:shortest=1,"
        f"fade=t=in:st=0:d=0.1:color=white,format=yuv420p"
    )
    r = _run([
        "ffmpeg", "-y", "-i", str(clip), "-loop", "1", "-i", str(chrome_path),
        "-filter_complex", vf, "-t", str(dur),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an", str(out),
    ], timeout=120)
    if not out.exists():
        print((r.stderr or "")[-600:])
        # fallback simpler
        return page_to_video(chrome_path, None, out, dur)
    return True


def stage_assemble():
    WORK.mkdir(parents=True, exist_ok=True)
    PAGES.mkdir(parents=True, exist_ok=True)
    by = {p["slug"]: p for p in PANELS}

    segs = []

    # PAGE 1 — true 2-panel strip (ink_drop over century_thread)
    page1 = PAGES / "page1_strip.png"
    build_page_strip(
        by["ink_drop"], by["century_thread"], page1,
        "God started a sentence. One line across five hundred years.",
        "sentence",
    )
    seg1 = WORK / "seg_01_page1.mp4"
    # For page1, also try to animate: use zoompan on page, but inject live clips is hard for 2-panel.
    # Composite live: build two half-clips and stack — more authentic.
    _build_live_two_panel(by["ink_drop"], by["century_thread"], seg1, dur=5.0,
                          caption="God started a sentence. One line across five hundred years.",
                          kw="sentence")
    segs.append(seg1)

    # PAGES 2–6 splash live
    plan = [
        ("spear_tunnel", 4.0),
        ("me_him", 4.2),
        ("double_sight", 4.0),
        ("sky_opens", 4.2),
        ("eyes_live", 4.5),
    ]
    for i, (slug, dur) in enumerate(plan, start=2):
        out = WORK / f"seg_{i:02d}_{slug}.mp4"
        ok = live_splash_video(by[slug], out, dur)
        print(f"seg {i} {slug}: {ok}")
        if ok:
            segs.append(out)

    # concat
    lst = WORK / "concat.txt"
    lst.write_text("\n".join(f"file '{s.as_posix()}'" for s in segs if s.exists()), encoding="utf-8")
    silent = HERE / "the_sentence_silent.mp4"
    _run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", str(silent),
    ], timeout=120)

    final = HERE / "the_sentence.mp4"
    if AUDIO.exists() and silent.exists():
        # duck: use a middle slice of narration that covers the theological spine
        # (proof + conviction land around mid) — for POC use 0–duration
        _run([
            "ffmpeg", "-y", "-i", str(silent), "-i", str(AUDIO),
            "-filter_complex",
            "[1:a]atrim=0:30,apad=whole_dur=30,volume=1.0[a]",
            "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-c:a", "aac",
            "-shortest", str(final),
        ], timeout=120)
        if not final.exists():
            shutil.copy2(silent, final)
    else:
        if silent.exists():
            shutil.copy2(silent, final)

    print("FINAL", final, final.exists() if final.exists() else False)
    stage_html()


def _build_live_two_panel(p_top, p_bot, out, dur, caption, kw):
    """Stack two live clips as a comic page with gutters + caption."""
    from PIL import Image, ImageDraw
    W, H = 1080, 1920
    gutter = 28
    margin = 40
    cap_space = 150
    usable_h = H - margin * 2 - gutter - cap_space
    ph = usable_h // 2
    pw = W - margin * 2
    y1 = margin
    y2 = margin + ph + gutter

    chrome = _paper(W, H)
    draw = ImageDraw.Draw(chrome)
    draw.rectangle([margin - 6, y1 - 6, margin + pw + 6, y1 + ph + 6], fill=(8, 6, 4))
    draw.rectangle([margin - 6, y2 - 6, margin + pw + 6, y2 + ph + 6], fill=(8, 6, 4))
    _border(draw, (margin - 4, y1 - 4, margin + pw + 4, y1 + ph + 4), width=10, seed=11)
    _border(draw, (margin - 4, y2 - 4, margin + pw + 4, y2 + ph + 4), width=10, seed=22)
    _border(draw, (16, 16, W - 16, H - 16), width=5, seed=3)
    _caption(chrome, caption, kw, H)
    chrome_path = WORK / "chrome_page1.png"
    chrome.save(chrome_path)

    c1 = CLIPS / f"{p_top['slug']}.mp4"
    c2 = CLIPS / f"{p_bot['slug']}.mp4"
    if not (c1.exists() and c2.exists()):
        # static page fallback
        page = PAGES / "page1_strip.png"
        build_page_strip(p_top, p_bot, page, caption, kw)
        return page_to_video(page, None, out, dur, motion="push")

    # top: push into drop; bottom: pan along thread
    fc = (
        f"[0:v]scale={pw}:{ph}:force_original_aspect_ratio=increase,"
        f"crop={pw}:{ph},fps=30,"
        f"zoompan=z='min(1.12,1+0.02*on/30)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d=1:s={pw}x{ph}:fps=30,trim=duration={dur},setpts=PTS-STARTPTS[v1];"
        f"[1:v]scale={pw*2}:{ph}:force_original_aspect_ratio=increase,"
        f"crop={pw}:{ph}:'min(iw-ow,max(0,(iw-ow)*on/(30*{dur})))':(ih-oh)/2,fps=30,"
        f"trim=duration={dur},setpts=PTS-STARTPTS[v2];"
        f"[2:v]scale={W}:{H},fps=30,trim=duration={dur},setpts=PTS-STARTPTS[bg];"
        f"[bg][v1]overlay={margin}:{y1}[tmp];"
        f"[tmp][v2]overlay={margin}:{y2}:shortest=1,"
        f"fade=t=in:st=0:d=0.1:color=white,format=yuv420p"
    )
    r = _run([
        "ffmpeg", "-y",
        "-i", str(c1), "-i", str(c2), "-loop", "1", "-i", str(chrome_path),
        "-filter_complex", fc, "-t", str(dur),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an", str(out),
    ], timeout=120)
    if not out.exists():
        print((r.stderr or "")[-700:])
        page = PAGES / "page1_strip.png"
        build_page_strip(p_top, p_bot, page, caption, kw)
        return page_to_video(page, None, out, dur)
    return True


def stage_html():
    rows = []
    for p in PANELS:
        slug = p["slug"]
        sp = f"stills/{slug}.png"
        cp = f"clips/{slug}.mp4"
        rows.append(f"""
        <section>
          <h2>{slug}</h2>
          <p class="idea">{p['caption']}</p>
          <div class="pair">
            <figure><figcaption>still</figcaption>
              <img src="{sp}" onerror="this.alt='missing'"/></figure>
            <figure><figcaption>clip</figcaption>
              <video controls loop muted src="{cp}"></video></figure>
          </div>
        </section>""")
    html = f"""<!doctype html>
<html><head><meta charset="utf-8"/><title>The Sentence — from scratch</title>
<style>
body{{font-family:Georgia,serif;background:#140f0c;color:#f0e2c8;margin:0;padding:28px}}
h1{{color:#f0c878}} h2{{color:#e0b060;margin-top:2em}}
.idea{{color:#cbb896;font-style:italic}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
figure{{margin:0;background:#221a14;padding:10px;border:1px solid #3a2a1c}}
img,video{{width:100%;max-height:560px;object-fit:contain;background:#000}}
.hero{{max-width:420px;margin:20px auto;display:block}}
.note{{border-left:4px solid #c44;padding:12px 16px;background:#221a14;margin:20px 0}}
</style></head><body>
<h1>The Sentence — built from scratch</h1>
<div class="note">
  <p><b>Not a re-render.</b> New images, new metaphors, new page structure.</p>
  <p>Thesis: God started a sentence. A spear finished it. Looking is life.</p>
</div>
<video class="hero" controls src="the_sentence.mp4"></video>
<p style="text-align:center">the_sentence.mp4 — the comic strip film</p>
{''.join(rows)}
</body></html>"""
    (HERE / "REVIEW.html").write_text(html, encoding="utf-8")
    print("wrote", HERE / "REVIEW.html")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="all",
                    choices=["stills", "redownload", "animate", "assemble", "html", "all"])
    ap.add_argument("--only", default="")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    only = {x.strip() for x in a.only.split(",") if x.strip()} or None
    if a.stage in ("stills", "all"):
        stage_stills(only=only, force=a.force)
        stage_redownload()
    if a.stage == "redownload":
        stage_redownload()
    if a.stage in ("animate", "all"):
        stage_animate(only=only, force=a.force)
    if a.stage in ("assemble", "all"):
        stage_assemble()
    if a.stage == "html":
        stage_html()


if __name__ == "__main__":
    main()
