"""pipeline/thumbnails.py — $0 thumbnail stage: 16:9 + 9:16 + 1:1 per piece.

Design: the piece's hero FRAME (pulled from the finished _sfx video at its strongest
beat) cover-cropped, a bottom ink gradient, the title in ivory Georgia Bold caps, the
verse ref beneath, and the red AWAKEDEN wordmark. Writes to
<piece>/publish/thumbs/. Also exports the standalone brand watermark assets
(_brand/awakeden_watermark*.png) for YouTube Studio's branding slot.

  .venv\\Scripts\\python.exe pipeline/thumbnails.py            # all pieces + assets
  .venv\\Scripts\\python.exe pipeline/thumbnails.py pierced    # substring filter
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageStat

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

IVORY = (245, 240, 208)    # caption ivory
INK = (12, 10, 8)

GEORGIA_B = r"C:\Windows\Fonts\georgiab.ttf"
GEORGIA = r"C:\Windows\Fonts\georgia.ttf"
ARIAL_B = r"C:\Windows\Fonts\arialbd.ttf"


def _font(path: str, size: int) -> ImageFont.FreeTypeFont:
    for p in (path, GEORGIA_B, ARIAL_B):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _sfx_video(piece_dir: Path) -> Path:
    from pipeline.finality import final_video  # ONE rule (skips .bak backups)
    _status, video = final_video(piece_dir)
    if not video:
        raise FileNotFoundError(f"no final video under {piece_dir / 'visual'}")
    return video


# Pieces come from _website/manifest.yaml (the hard join) — no hardcoded list.
# Per-piece art direction lives in the piece's publish_meta.json:
#   "thumb": {"t": <hero-frame seconds>, "title": ["LINE1","LINE2"], "ref": "PSALM 22:18"}
# Missing spec -> defaults: t = 40% of the video, title/ref from the manifest item.

SIZES = {"16x9": (1280, 720), "9x16": (1080, 1920), "1x1": (1080, 1080)}


def _grab_raw(video: Path, t: float, out_png: Path) -> Image.Image:
    out_png.parent.mkdir(parents=True, exist_ok=True)
    # ffmpeg -ss past EOF exits 0 and writes NOTHING — a leftover _frame.png from
    # the previous run would then be composed and stamped fresh (red-team C2).
    out_png.unlink(missing_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t),
                    "-i", str(video), "-frames:v", "1", str(out_png)], check=True)
    if not out_png.is_file():
        raise RuntimeError(f"ffmpeg produced no frame at t={t}s from {video.name} "
                           "(hero time past the end? fix publish_meta.json thumb.t)")
    return Image.open(out_png).convert("RGB")


def blank_fraction(img: Image.Image, grid: int = 10) -> float:
    """Fraction of the frame that is UNPAINTED CANVAS — a comic panel-grid slot
    that hasn't been inked in yet at this exact video instant (found by red-team
    follow-up 2026-07-15: several migrated hero timestamps landed mid panel-slam,
    showing a flat pale placeholder where art belongs). Calibrated on a confirmed
    bad frame: blank luminance ~228/std~7, real linework ~72/std~68 — bright AND
    flat is the signature; dramatic dark-flat skies (legit) score 0 since they're
    dark, not bright."""
    g = img.convert("L")
    w, h = g.size
    cw, ch = max(1, w // grid), max(1, h // grid)
    flat_cells = 0
    total = 0
    for gy in range(grid):
        for gx in range(grid):
            box = (gx * cw, gy * ch, min(w, (gx + 1) * cw), min(h, (gy + 1) * ch))
            if box[2] <= box[0] or box[3] <= box[1]:
                continue
            total += 1
            stat = ImageStat.Stat(g.crop(box))
            if stat.mean[0] > 195 and stat.stddev[0] < 10:
                flat_cells += 1
    return flat_cells / total if total else 0.0


def grab_frame(video: Path, t: float, out_png: Path, *, duration: float = 0.0,
               piece_label: str = "") -> Image.Image:
    """Grab a hero frame, auto-avoiding unpainted-canvas moments (blank_fraction
    too high -> try nearby offsets before giving up on the requested t)."""
    frame = _grab_raw(video, t, out_png)
    if blank_fraction(frame) < 0.12:
        return frame
    offsets = [-0.4, 0.4, -0.8, 0.8, -1.2, 1.2, -1.6, 1.6, -2.0, 2.0, -3.0, 3.0]
    for off in offsets:
        cand_t = t + off
        if cand_t < 0.2 or (duration and cand_t > duration - 0.3):
            continue
        cand = _grab_raw(video, cand_t, out_png)
        if blank_fraction(cand) < 0.12:
            print(f"  !! {piece_label}: t={t}s was mostly blank canvas - used t={cand_t}s instead "
                  f"(consider updating publish_meta.json thumb.t)")
            return cand
    print(f"  !! {piece_label}: t={t}s AND every nearby offset look mostly blank canvas - "
          "using it anyway; INSPECT this thumbnail")
    return frame


def cover_crop(img: Image.Image, w: int, h: int) -> Image.Image:
    sw, sh = img.size
    scale = max(w / sw, h / sh)
    img = img.resize((round(sw * scale), round(sh * scale)), Image.LANCZOS)
    sw, sh = img.size
    # bias the crop toward the upper-middle (faces live high in our frames)
    x = (sw - w) // 2
    y = min((sh - h) // 3, sh - h)
    return img.crop((x, y, x + w, y + h))


def _fit_title_font(dr: ImageDraw.ImageDraw, title: list[str], start_size: int,
                    max_w: float, min_size: int = 24) -> ImageFont.FreeTypeFont:
    """Shrink the title font until every line fits max_w (red-team follow-up:
    'THEY SHALL LOOK ON HIM' / 'THE SONG FROM THE CROSS' ran off the canvas at
    the fixed size — long titles need this, short ones are untouched)."""
    size = start_size
    while size > min_size:
        f = _font(GEORGIA_B, size)
        if all(dr.textlength(line, font=f) <= max_w for line in title):
            return f
        size -= 2
    return _font(GEORGIA_B, min_size)


def compose(frame: Image.Image, size_key: str, title: list[str], ref: str) -> Image.Image:
    w, h = SIZES[size_key]
    im = cover_crop(frame, w, h)
    dr = ImageDraw.Draw(im, "RGBA")

    # bottom ink gradient (title zone); 9:16 keeps the bottom fifth clear of text
    # because the Shorts UI covers it — the title sits in the upper third instead.
    grad_h = int(h * (0.42 if size_key != "9x16" else 0.30))
    for i in range(grad_h):
        a = int(235 * (i / grad_h) ** 1.4)
        y = h - grad_h + i if size_key != "9x16" else grad_h - i
        dr.line([(0, y), (w, y)], fill=INK + (a,))

    ts0 = int(w * (0.105 if size_key == "16x9" else 0.115))
    margin = int(w * 0.055)
    f_title = _fit_title_font(dr, title, ts0, w - 2 * margin - int(w * 0.16))
    ts = f_title.size
    f_ref = _font(GEORGIA, int(ts * 0.36))
    f_brand = _font(ARIAL_B, int(ts * 0.30))

    if size_key == "9x16":
        ty = int(h * 0.055) + int(ts * 0.2)
    else:
        block = len(title) * int(ts * 1.08) + int(ts * 0.55)
        ty = h - margin - block

    # solid scrim behind the text block, on top of the diagonal gradient: some
    # source videos run a caption/subtitle continuously with no clean gap (found
    # 2026-07-15 auditing Isaiah 53 — a documentary-style long has one running
    # almost the whole film), which ghosts through the gradient alone at the TOP
    # of the title zone where its alpha is still low. A flat scrim guarantees
    # legibility regardless of what the source frame is doing underneath.
    scrim_top = ty - int(ts * 0.35)
    scrim_bot = h if size_key != "9x16" else ty + len(title) * int(ts * 1.08) + int(ts * 1.3)
    dr.rectangle([0, max(0, scrim_top), w, scrim_bot], fill=INK + (225,))

    for line in title:
        dr.text((margin + 4, ty + 4), line, font=f_title, fill=(0, 0, 0, 210))  # shadow
        dr.text((margin, ty), line, font=f_title, fill=IVORY)
        ty += int(ts * 1.08)
    dr.text((margin, ty), ref, font=f_ref, fill=IVORY)

    # site wordmark (AWAK bone + EDEN red) — top-right (16:9, 1:1) / bottom-left (9:16)
    from pipeline.channel_dress import draw_wordmark, wordmark_width
    bsize = int(ts * 0.26)
    bw = wordmark_width(bsize)
    if size_key == "9x16":
        bx, by = margin, h - int(h * 0.16)
    else:
        bx, by = w - margin - bw, int(h * 0.045)
    draw_wordmark(im, bx, by, bsize, glow=False, shadow=True)
    return im


def compose_tiktok(frame: Image.Image, title: list[str], ref: str) -> Image.Image:
    """TikTok cover: the feed grid crops covers to the CENTRE band, so ALL
    content (art + title + ref + wordmark) sits inside the middle 3:4 of the
    9:16 canvas, over a blurred dimmed backdrop (the HF-POC gen_tiktok_covers
    recipe)."""
    w, h = 1080, 1920
    im = cover_crop(frame, w, h).filter(ImageFilter.GaussianBlur(26))
    im = Image.eval(im, lambda px: int(px * 0.45))          # dim the backdrop
    dr = ImageDraw.Draw(im, "RGBA")

    zone_top, zone_bot = (h - 1440) // 2, (h + 1440) // 2   # centre 1080x1440 (3:4)
    ts0 = int(w * 0.095)
    f_title = _fit_title_font(dr, title, ts0, w * 0.90)
    ts = f_title.size
    f_ref = _font(GEORGIA, int(ts * 0.38))

    # the un-blurred art, fitted INSIDE the safe zone
    art_w = int(w * 0.88)
    scale = art_w / frame.width
    art = frame.resize((art_w, round(frame.height * scale)), Image.LANCZOS)
    max_art_h = int(1440 * 0.56)
    if art.height > max_art_h:
        art = art.crop((0, (art.height - max_art_h) // 2,
                        art.width, (art.height + max_art_h) // 2))
    title_block = len(title) * int(ts * 1.1) + int(ts * 0.8)
    art_y = zone_top + title_block + int(ts * 0.3)
    im.paste(art, ((w - art.width) // 2, art_y))
    dr.rectangle([(w - art.width) // 2 - 3, art_y - 3,
                  (w + art.width) // 2 + 3, art_y + art.height + 3],
                 outline=IVORY + (160,), width=3)

    ty = zone_top + int(ts * 0.3)
    for line in title:
        lw = dr.textlength(line, font=f_title)
        x = (w - lw) / 2
        dr.text((x + 4, ty + 4), line, font=f_title, fill=(0, 0, 0, 210))
        dr.text((x, ty), line, font=f_title, fill=IVORY)
        ty += int(ts * 1.1)

    ry = art_y + art.height + int(ts * 0.45)
    rw = dr.textlength(ref, font=f_ref)
    x0 = (w - rw) / 2
    dr.text((x0, ry), ref, font=f_ref, fill=IVORY)

    from pipeline.channel_dress import draw_wordmark, wordmark_width
    bsize = int(ts * 0.30)
    bx = (w - wordmark_width(bsize)) // 2
    by = min(ry + int(ts * 1.1), zone_bot - int(bsize * 1.6))
    draw_wordmark(im, bx, by, bsize, glow=False, shadow=True)
    return im


# Per-surface SAFE ZONE (fraction of canvas reserved at each edge, where no text/
# logo/important art may sit). Researched 2026-09 against each platform's own
# published guidance (YouTube: support.google.com/youtube/answer/72431; TikTok:
# kreatli.com/guides/tiktok-safe-zone + checksafe.zone's 2026 safe-area guide;
# Instagram: outfy.com's safe-zone guide + postfa.st's Reel-cover safe-zone guide;
# Facebook Reels: sendshort.ai's Facebook Reels size guide).
#
# 16:9 and 1:1 are STATIC thumbnail/post surfaces (YouTube search/suggested grid,
# Instagram feed) with no player chrome drawn over them -- only a small legibility
# margin is needed. 9:16 is a FULL-SCREEN PLAYER surface shared by YouTube Shorts,
# TikTok, Instagram Reels, and Facebook Reels alike, and each reserves real screen
# space for its own chrome while playing (profile/follow/live badge at the top;
# a like/comment/share icon column plus caption/username/sound-title band at the
# bottom-right) -- and grid/profile previews (Shorts shelf ~2:3, IG profile ~3:4)
# crop the same canvas further, shaving more off the top and bottom. The numbers
# below are the STRICTEST combination across all four platforms (top 150-200px,
# bottom 250-400px, right 100-270px on a 1080x1920 canvas), used symmetrically
# left+right for simplicity/safety, so ONE 9:16 export is safe on every one of
# them rather than tuned to just one.
SAFE_ZONES = {
    "16x9": {"top": 0.05, "bottom": 0.05, "left": 0.05, "right": 0.05},
    "9x16": {"top": 0.104, "bottom": 0.208, "left": 0.083, "right": 0.083},
    "1x1": {"top": 0.05, "bottom": 0.05, "left": 0.05, "right": 0.05},
}


def compose_centered(frame: Image.Image, w: int, h: int, title: list[str], ref: str,
                     safe: dict | None = None) -> Image.Image:
    """Swirls-of-Life thumbnail: works for ANY target aspect (16:9, 9:16, 1:1) via one
    code path, unlike compose()/compose_tiktok() above (main-engine, horizontally-shot
    footage where a directional crop makes sense). Swirls stills are shot 9:16 and
    describe subjects small against the landscape anywhere in the frame (e.g. a line of
    figures across the LOWER third) -- compose()'s crop bias would cut real subject
    content out of a 16:9/1:1 canvas. So here the source is never cropped: a blurred
    full-bleed backdrop of it fills the canvas, the WHOLE frame is scaled to fit and
    centered on top -- but title, art, ref, and wordmark are ALL laid out strictly
    inside `safe` (see SAFE_ZONES), never just centered on the raw canvas, so nothing
    important lands where a platform's own on-screen chrome would cover it."""
    safe = safe or SAFE_ZONES["16x9"]
    im = cover_crop(frame, w, h).filter(ImageFilter.GaussianBlur(28))
    im = Image.eval(im, lambda px: int(px * 0.42))
    dr = ImageDraw.Draw(im, "RGBA")

    sx0, sx1 = w * safe["left"], w * (1 - safe["right"])
    sy0, sy1 = h * safe["top"], h * (1 - safe["bottom"])
    safe_w, safe_h = sx1 - sx0, sy1 - sy0

    ts0 = int(min(safe_w, safe_h) * 0.16)
    f_title = _fit_title_font(dr, title, ts0, safe_w)
    ts = f_title.size
    f_ref = _font(GEORGIA, int(ts * 0.36))

    title_block_h = len(title) * int(ts * 1.1) + int(ts * 0.5)
    bottom_block_h = int(ts * 1.6)  # ref + wordmark row
    gap = int(ts * 0.35)
    art_max_w = safe_w
    art_max_h = max(1, safe_h - title_block_h - bottom_block_h - 2 * gap)

    scale = min(art_max_w / frame.width, art_max_h / frame.height, 1.0)
    art = frame.resize((max(1, round(frame.width * scale)), max(1, round(frame.height * scale))), Image.LANCZOS)
    art_x = int(sx0 + (safe_w - art.width) / 2)
    art_y = int(sy0 + title_block_h + gap)
    im.paste(art, (art_x, art_y))
    dr.rectangle([art_x - 3, art_y - 3, art_x + art.width + 3, art_y + art.height + 3],
                 outline=IVORY + (160,), width=3)

    ty = int(sy0)
    for line in title:
        lw = dr.textlength(line, font=f_title)
        x = sx0 + (safe_w - lw) / 2
        dr.text((x + 3, ty + 3), line, font=f_title, fill=(0, 0, 0, 210))
        dr.text((x, ty), line, font=f_title, fill=IVORY)
        ty += int(ts * 1.1)

    ry = art_y + art.height + gap
    rw = dr.textlength(ref, font=f_ref)
    x0 = sx0 + (safe_w - rw) / 2
    dr.text((x0, ry), ref, font=f_ref, fill=IVORY)

    from pipeline.channel_dress import draw_wordmark, wordmark_width
    bsize = int(ts * 0.28)
    bw = wordmark_width(bsize)
    by = min(ry + int(ts * 1.1), sy1 - int(bsize * 1.3))
    draw_wordmark(im, sx0 + (safe_w - bw) / 2, by, bsize, glow=False, shadow=True)
    return im


def build_swirls_thumbnails(episode_dir: Path) -> list[Path]:
    """Thumbnails for one Swirls-of-Life episode (poc_living_water_ink_style_test/
    swirls_episode_*/). Source art is the episode's own front_cover.png -- a real
    composed hero image, not a video-frame grab (grabbing a frame from the finished
    ANIMATED cover risks landing mid-motion; the cover art itself is already the
    intended hero shot). Title/ref come from the SAME FRONT_COVER the episode's own
    on-screen title card uses (via episode.py, same MANIFEST introspection
    upload_engine.harvest_facts() already uses) -- one source of truth for the title,
    not a second guess at it."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(f"swirls_episode_{episode_dir.name}", episode_dir / "episode.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    front = mod.FRONT_COVER

    cover = episode_dir / "front_cover.png"
    if not cover.is_file():
        cover = episode_dir / "front_cover_9x16.png"  # older episodes (pre-episode.py naming, e.g. Naaman)
    if not cover.is_file():
        raise FileNotFoundError(f"no front_cover.png / front_cover_9x16.png under {episode_dir}")
    frame = Image.open(cover).convert("RGB")
    title = _default_title(front.title)
    ref = front.subtitle

    pub = episode_dir / "publish" / "thumbs"
    pub.mkdir(parents=True, exist_ok=True)
    out_paths = []
    for key, (w, h) in SIZES.items():
        out = pub / f"thumb_{key}.jpg"
        compose_centered(frame, w, h, title, ref, safe=SAFE_ZONES[key]).save(out, quality=92)
        out_paths.append(out)
    return out_paths


def brand_assets(out_dir: Path) -> None:
    """Site-identity marks (AWAK bone + EDEN red, exactly as the website renders
    the wordmark). The YouTube branding watermark is the same mark, corner-subtle;
    awakeden_watermark_overlay.png is the transparent shadowed variant for
    burning into videos (scale it down at overlay time)."""
    from pipeline.channel_dress import (ARIAL_BLK, BONE, RED_BRIGHT,
                                        draw_wordmark, font as cd_font,
                                        wordmark_width)
    out_dir.mkdir(parents=True, exist_ok=True)

    from pipeline.channel_dress import draw_word_centered
    # YouTube renders the branding watermark in a small square with slight padding:
    # give the word a soft ink chip so bone letters survive light footage.
    for px, name in ((800, "awakeden_watermark.png"), (150, "awakeden_watermark_150.png")):
        im = Image.new("RGBA", (px, px), (0, 0, 0, 0))
        ImageDraw.Draw(im).rounded_rectangle(
            [0, px * 0.36, px, px * 0.64], radius=px * 0.05, fill=(12, 14, 18, 215))
        draw_word_centered(im, (px * 0.04, px * 0.40, px * 0.96, px * 0.60))
        im.save(out_dir / name)
    # horizontal wordmark (transparent)
    w = int(wordmark_width(220, 0.14)) + 80
    im = Image.new("RGBA", (w, 320), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    f = cd_font(ARIAL_BLK, 220)
    cx = 40.0
    for i, ch in enumerate("AWAKEDEN"):
        dr.text((cx, 40), ch, font=f, fill=(BONE if i < 4 else RED_BRIGHT) + (255,))
        cx += dr.textlength(ch, font=f) + 220 * 0.14
    im.save(out_dir / "awakeden_wordmark.png")
    # video-overlay variant: same wordmark over a soft blurred shadow so the bone
    # letters survive bright footage, still fully transparent outside the glyphs
    from PIL import ImageFilter
    im = Image.new("RGBA", (w, 320), (0, 0, 0, 0))
    sh = Image.new("RGBA", (w, 320), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    cx = 40.0
    for ch in "AWAKEDEN":
        sd.text((cx + 6, 46), ch, font=f, fill=(0, 0, 0, 235))
        cx += sd.textlength(ch, font=f) + 220 * 0.14
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
    dr = ImageDraw.Draw(im)
    cx = 40.0
    for i, ch in enumerate("AWAKEDEN"):
        dr.text((cx, 40), ch, font=f, fill=(BONE if i < 4 else RED_BRIGHT) + (255,))
        cx += dr.textlength(ch, font=f) + 220 * 0.14
    im.save(out_dir / "awakeden_watermark_overlay.png")
    print(f"brand assets -> {out_dir}")


def _default_title(title: str) -> list[str]:
    words = title.upper().split()
    lines, cur = [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > 14 and len(lines) < 1:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    lines.append(cur)
    return lines[:2]


def _duration(video: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(video)], capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        return 30.0


_SWIRLS_DIR = ROOT / "poc_living_water_ink_style_test"


def _main_swirls(arg: str) -> int:
    """arg is either a Swirls episode folder (has episode.py) or '--swirls' to do
    every swirls_episode_* under poc_living_water_ink_style_test/."""
    if arg == "--swirls":
        dirs = sorted(d for d in _SWIRLS_DIR.glob("swirls_episode_*") if (d / "episode.py").is_file())
    else:
        dirs = [Path(arg).resolve()]
    made = 0
    for d in dirs:
        out = build_swirls_thumbnails(d)
        made += len(out)
        print(f"{d.name}: {len(out)} thumbnails -> {out[0].parent}")
    print(f"\n{made} thumbnails written")
    return 0


def main() -> int:
    from pipeline import finality, release_state
    flt = sys.argv[1] if len(sys.argv) > 1 else ""
    if flt == "--swirls" or (flt and (Path(flt) / "episode.py").is_file()):
        return _main_swirls(flt)
    brand_assets(ROOT / "_brand")
    states, _orphans, _orphan_pages = release_state.gather()
    made, skipped = [], []
    for s in states:
        if flt and flt not in s.slug and flt not in (s.source_dir.name if s.source_dir else ""):
            continue
        if not s.source_dir or not s.video or not s.finality.startswith("FINAL"):
            if s.status in ("studio_complete", "live"):
                skipped.append(s.slug)
            continue
        spec = {}
        pm = s.source_dir / "publish_meta.json"
        if pm.is_file():
            try:
                spec = json.loads(pm.read_text(encoding="utf-8")).get("thumb", {})
            except ValueError:
                print(f"  !! {s.slug}: publish_meta.json is malformed JSON - thumb art "
                      "direction (t/title/ref) DROPPED, using defaults")
        dur = _duration(s.video)
        t = min(spec.get("t", round(dur * 0.4, 1)), max(dur - 0.5, 0.0))
        title = spec.get("title") or _default_title(s.title)
        ref = spec.get("ref") or s.ref.upper()
        pub = s.source_dir / "publish" / "thumbs"
        frame = grab_frame(s.video, t, pub / "_frame.png", duration=dur, piece_label=s.slug)
        for key in SIZES:
            out = pub / f"thumb_{key}.jpg"
            compose(frame, key, title, ref).save(out, quality=92)
            made.append(out)
        tk = pub / "thumb_tiktok.jpg"
        compose_tiktok(frame, title, ref).save(tk, quality=92)
        made.append(tk)
        # re-hash at stamp time (not the gather-time sha) so a final replaced
        # mid-run can't be stamped with the wrong fingerprint (red-team m4)
        (pub / "_meta.json").write_text(json.dumps({
            "video": s.video.name, "final_sha": finality.content_sha(s.video), "t": t,
        }, indent=2), encoding="utf-8")
        print(f"{s.slug}: 16x9 + 9x16 + 1x1 + tiktok + _meta -> {pub}")
    print(f"\n{len(made)} thumbnails written")
    if skipped:
        print(f"skipped (no FINAL video yet): {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
