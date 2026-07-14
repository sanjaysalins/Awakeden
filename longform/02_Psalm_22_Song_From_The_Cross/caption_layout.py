#!/usr/bin/env python
"""caption_layout.py — deterministic 3-tier caption placement solver (SPEC v2 §R1/§R3/§4B).

For each (beat, caption) the solver reads the beat's panel geometry + each panel's mapped
subject keep-box (<slug>.anchor.json pushed through the SOLVED panel crop, same math as
comic_engine._panel_fill) and decides WHERE the caption may sit:

  Tier 1  a compact box that overlaps NO subject keep-box (kinetic <= 50% frame width)
  Tier 2  a translucent lower-third band over an expendable region: it must clear every
          CORE box (the tight area around each subject's focus — face/hands); ground,
          robe, shadow at the frame bottom may sit under the translucent band
  Tier 3  nothing fits -> FLAG the still for a caption-room re-render (the build falls
          back to Tier-2 geometry so the film still renders; the flag list drives the
          re-render batch)

Two caption CLASSES with different rules (§R3):
  kinetic    narrator keyword captions — ALWAYS compact, never full width
  redletter  KJV Scripture — plaque (<= 8 words, Tier-1 solve at wider widths) or a
             designed translucent parchment band over the LOWER portion (full width
             allowed HERE: readability of Scripture wins; band stays translucent)

Deterministic, $0, no API, no edits to the locked tooling (panel_fit / comic_engine).
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT = r"C:\Windows\Fonts\comicbd.ttf"
BASE_H = 1080.0                      # all px constants are designed at 1920x1080

# kinetic keyword captions (§R3: compact, <=50% width)
K_FSZ, K_PAD, K_LEAD = 38, 20, 10
K_WIDTHS = (0.42, 0.34, 0.27, 0.50)  # tried in order; 0.50 is the hard cap, last resort
# red-letter Scripture (§R3: plaque short / translucent band long)
R_FSZ, R_PAD, R_LEAD, R_TAG = 44, 24, 14, 30
R_PLAQUE_WIDTHS = (0.55, 0.46, 0.62)
R_SHORT_WORDS = 8
CHIP_H_PAD = 18                      # tag chip inner pad above plaque/band

MARGIN_X, MARGIN_TOP, MARGIN_BOT = 36, 40, 48
# 9:16 shorts platform safe-zone: TikTok/Reels/Shorts cover the bottom ~18% (caption,
# handle, progress bar) with UI, so captions must never sit there. Set by the portrait
# builder (fraction of H reserved at the bottom); 0 = off (long-form 16:9 unaffected).
SHORTS_SAFE_BOT = 0.0
GAP = 12                             # min clearance caption-box <-> keep-box
CORE_FRAC = 0.45                     # core box = this fraction of the keep box, on focus

# Motion magnifies the panel content, so still-space boxes understate what the composited
# frame shows. dynamic_cam pre-warps by COVER=1.18 x its end push (arc 1.10 / swoop 1.16 /
# push 1.12); Kling INK camera moves are gentler. Keep AND core boxes are inflated about
# the panel centre by the source's worst-case factor before any clearance test.
SRC_SCALE = {"dyncam_arc": 1.32, "dyncam_swoop": 1.40, "dyncam_push": 1.34,
             "dyncam_tour": 1.34, "dyncam_parallax": 1.30,
             "kling": 1.15, "still": 1.02}

_SLOP = {"—": "-", "–": "-", "―": "-", "‘": "'", "’": "'", "“": '"', "”": '"', "…": "..."}


def san(s):
    for k, v in _SLOP.items():
        s = s.replace(k, v)
    return s


# ---------------- text metrics (shared with the renderer) ----------------
_FONTS = {}


def font_at(fsz):
    if fsz not in _FONTS:
        _FONTS[fsz] = ImageFont.truetype(FONT, fsz)
    return _FONTS[fsz]


_D = ImageDraw.Draw(Image.new("RGBA", (4, 4)))


def wrap_lines(text, fsz, maxw):
    """Word-wrap UPPER-cased text to maxw px. -> (lines, widest_px)."""
    f = font_at(fsz)
    words, lines, cur = text.split(), [], []
    for w in words:
        t = " ".join(cur + [w])
        if not cur or _D.textlength(t, font=f) <= maxw:
            cur.append(w)
        else:
            lines.append(cur); cur = [w]
    if cur:
        lines.append(cur)
    widest = max(_D.textlength(" ".join(ln), font=f) for ln in lines)
    return [" ".join(ln) for ln in lines], widest


# ---------------- keep/core boxes mapped to page space ----------------
def _map_rect(panel_rect, still_wh, nrect, bias, zoom):
    """Map a normalised still rect through the engine's scale-to-fill + bias crop."""
    x, y, w, h = panel_rect
    iw, ih = still_wh
    s = max(w / iw, h / ih) * zoom
    sw, sh = iw * s, ih * s
    cx = min(max((sw - w) * bias[0], 0), max(sw - w, 0))
    cy = min(max((sh - h) * bias[1], 0), max(sh - h, 0))
    x0, y0 = x + nrect[0] * sw - cx, y + nrect[1] * sh - cy
    x1, y1 = x + nrect[2] * sw - cx, y + nrect[3] * sh - cy
    # only the part visible inside the panel matters
    x0, y0 = max(x0, x), max(y0, y)
    x1, y1 = min(x1, x + w), min(y1, y + h)
    if x1 <= x0 or y1 <= y0:
        return None
    return (x0, y0, x1, y1)


def _inflate(rect, panel_rect, f):
    """Scale a page-space rect about the panel centre by f (motion magnification), then
    clip back to the panel. Approximation: dyncam/Kling magnify about the frame centre."""
    if not rect or f == 1.0:
        return rect
    x, y, w, h = panel_rect
    cx, cy = x + w / 2, y + h / 2
    x0, y0 = cx + (rect[0] - cx) * f, cy + (rect[1] - cy) * f
    x1, y1 = cx + (rect[2] - cx) * f, cy + (rect[3] - cy) * f
    x0, y0 = max(x0, x), max(y0, y)
    x1, y1 = min(x1, x + w), min(y1, y + h)
    if x1 <= x0 or y1 <= y0:
        return None
    return (x0, y0, x1, y1)


def panel_boxes(panel_rect, still_wh, anchor, bias=(0.5, 0.5), zoom=1.0, motion_scale=1.0):
    """-> {keep, core} page-space rects (either may be None if cropped out of view).
    motion_scale: worst-case content magnification of this panel's source (SRC_SCALE) —
    applied to BOTH boxes so clearance holds across the whole move, not just frame 0."""
    k = anchor["keep"]
    fx, fy = anchor.get("focus", [(k[0] + k[2]) / 2, (k[1] + k[3]) / 2])
    kw_, kh_ = (k[2] - k[0]) * CORE_FRAC, (k[3] - k[1]) * CORE_FRAC
    core_n = (max(k[0], fx - kw_ / 2), max(k[1], fy - kh_ / 2),
              min(k[2], fx + kw_ / 2), min(k[3], fy + kh_ / 2))
    keep = _inflate(_map_rect(panel_rect, still_wh, k, bias, zoom), panel_rect, motion_scale)
    core = _inflate(_map_rect(panel_rect, still_wh, core_n, bias, zoom), panel_rect, motion_scale)
    return {"keep": keep, "core": core}


# ---------------- geometry ----------------
def _overlaps(box, rect, gap):
    bx0, by0, bx1, by1 = box[0] - gap, box[1] - gap, box[0] + box[2] + gap, box[1] + box[3] + gap
    return not (bx1 <= rect[0] or bx0 >= rect[2] or by1 <= rect[1] or by0 >= rect[3])


def _clear(box, rects, gap=GAP):
    return all(not _overlaps(box, r, gap) for r in rects if r)


def _candidates(page, bw, bh, sc):
    """Deterministic position preference: top-left narrator corner first (comic language),
    then the other corners, edges, then a top-first grid sweep from the edges inward."""
    W, H = page
    mx, mt, mb = round(MARGIN_X * sc), round(MARGIN_TOP * sc), round(MARGIN_BOT * sc)
    mb = max(mb, round(SHORTS_SAFE_BOT * H))    # keep captions above the shorts UI band
    xs_l, xs_r = mx, W - bw - mx
    yb, yt = H - bh - mb, mt
    out = [(xs_l, yt), (xs_r, yt), (xs_l, yb), (xs_r, yb),
           (xs_l, (H - bh) // 2), (xs_r, (H - bh) // 2),
           ((W - bw) // 2, yt), ((W - bw) // 2, yb)]
    n_y, n_x = 8, 12
    for iy in range(n_y):                       # top-preferred rows
        y = round(yt + iy * (yb - yt) / max(n_y - 1, 1))
        for ix in range(n_x):                   # edges inward, alternating L/R
            k = (ix + 1) // 2
            x = xs_l + k * (xs_r - xs_l) // (n_x - 1) if ix % 2 == 0 else xs_r - k * (xs_r - xs_l) // (n_x - 1)
            out.append((x, y))
    seen, uniq = set(), []
    for p in out:
        if p not in seen:
            seen.add(p); uniq.append(p)
    return uniq


def _shrink_wrap(text, fsz, pad, lead, width):
    """Wrap into a candidate width, then shrink the box to the widest actual line."""
    lines, widest = wrap_lines(text, fsz, width - 2 * pad)
    lh = fsz + lead
    bw = round(widest + 2 * pad)
    bh = len(lines) * lh + 2 * pad
    return lines, bw, bh, lh


# ---------------- the solver ----------------
def solve(page, panels, cap):
    """page=(W,H). panels=[{keep,core}] page-space. cap={"type","text",...}.
    -> {tier, cls, style, box=(x,y,w,h), lines, fsz, pad, lh, chip_h, flag, reason}"""
    W, H = page
    sc = H / BASE_H
    keeps = [p["keep"] for p in panels if p.get("keep")]
    cores = [p["core"] for p in panels if p.get("core")]
    cls = "redletter" if cap.get("type") == "redletter" else "kinetic"
    # sanitize ONCE here; renderers draw sol["lines"] verbatim (measured = drawn).
    # Kinetic is upper-cased; red-letter Scripture stays MIXED CASE (the locked red-bar look).
    text = san(cap["text"])
    if cls == "kinetic":
        text = text.upper()

    if cls == "kinetic":
        fsz, pad, lead = round(K_FSZ * sc), round(K_PAD * sc), round(K_LEAD * sc)
        for wf in K_WIDTHS:
            lines, bw, bh, lh = _shrink_wrap(text, fsz, pad, lead, round(wf * W))
            for (x, y) in _candidates(page, bw, bh, sc):
                if _clear((x, y, bw, bh), keeps):
                    return dict(tier=1, cls=cls, style="box", box=(x, y, bw, bh),
                                lines=lines, fsz=fsz, pad=pad, lh=lh, chip_h=0,
                                flag=False, reason=f"tier1 @ {wf:.0%} width")
        # Tier 2 — compact scrim low in the frame, over expendable (non-core) region
        # (raised above the shorts UI band when SHORTS_SAFE_BOT is set)
        mb_safe = max(round(MARGIN_BOT * sc), round(SHORTS_SAFE_BOT * H))
        lines, bw, bh, lh = _shrink_wrap(text, fsz, pad, lead, round(0.5 * W))
        for x in (round(MARGIN_X * sc), W - bw - round(MARGIN_X * sc), (W - bw) // 2):
            box = (x, H - bh - mb_safe, bw, bh)
            if _clear(box, cores):
                return dict(tier=2, cls=cls, style="scrim", box=box, lines=lines,
                            fsz=fsz, pad=pad, lh=lh, chip_h=0, flag=False,
                            reason="tier2 lower scrim (clears cores)")
        box = ((W - bw) // 2, H - bh - mb_safe, bw, bh)
        return dict(tier=3, cls=cls, style="scrim", box=box, lines=lines, fsz=fsz,
                    pad=pad, lh=lh, chip_h=0, flag=True,
                    reason="tier3 FLAG: no keep-clear box, cores block the lower third")

    # ---- red-letter Scripture ----
    fsz, pad, lead = round(R_FSZ * sc), round(R_PAD * sc), round(R_LEAD * sc)
    chip_h = round((R_TAG + CHIP_H_PAD) * sc)
    if len(cap["text"].split()) <= R_SHORT_WORDS:
        for wf in R_PLAQUE_WIDTHS:
            lines, bw, bh, lh = _shrink_wrap(text, fsz, pad, lead, round(wf * W))
            for (x, y) in _candidates(page, bw, bh + chip_h, sc):
                if _clear((x, y, bw, bh + chip_h), keeps):
                    return dict(tier=1, cls=cls, style="plaque", box=(x, y, bw, bh + chip_h),
                                lines=lines, fsz=fsz, pad=pad, lh=lh, chip_h=chip_h,
                                flag=False, reason=f"tier1 plaque @ {wf:.0%} width")
    # long verse (or no plaque spot): translucent parchment band over the lower portion
    mx = round(MARGIN_X * sc)
    lines, _w = wrap_lines(text, fsz, W - 2 * mx - 2 * pad)
    lh = fsz + lead
    bh = len(lines) * lh + 2 * pad + chip_h
    band_bot = max(round(24 * sc), round(SHORTS_SAFE_BOT * H))   # clear the shorts UI band
    box = (mx, H - bh - band_bot, W - 2 * mx, bh)
    ok_band = _clear(box, cores)
    # long-form keeps the "band within bottom-25%" check; shorts deliberately raise it, so
    # sitting above the bottom quarter is CORRECT there, not a flag.
    in_bottom = SHORTS_SAFE_BOT > 0 or box[1] + chip_h >= 0.75 * H
    if ok_band:
        return dict(tier=2, cls=cls, style="band", box=box, lines=lines, fsz=fsz,
                    pad=pad, lh=lh, chip_h=chip_h, flag=not in_bottom,
                    reason="tier2 band" + ("" if in_bottom else " (taller than bottom-25%: FLAG)"))
    return dict(tier=3, cls=cls, style="band", box=box, lines=lines, fsz=fsz,
                pad=pad, lh=lh, chip_h=chip_h, flag=True,
                reason="tier3 FLAG: core box under the band — pick another still/crop")


# ---------------- unit test: 3 stills, debug overlays ----------------
if __name__ == "__main__":
    import json

    HERE = Path(__file__).resolve().parent
    POOL = HERE / "v1" / "visual_16x9_inked"
    OUT = POOL / "_caption_layout_test"; OUT.mkdir(exist_ok=True)
    PAGE = (1920, 1080)
    CASES = [
        ("david_psalmist", {"type": "caption", "text": "Written a thousand years before", "kw": "A THOUSAND YEARS"}),
        ("cry_ninth_hour", {"type": "redletter", "text": "My God, my God, why hast thou forsaken me?",
                            "speaker": "JESUS", "ref": "Matthew 27:46"}),
        ("mockers_wag_heads", {"type": "caption", "text": "He trusted on the LORD - let him deliver him", "kw": "DELIVER"}),
    ]
    for slug, cap in CASES:
        anc = json.loads((POOL / f"{slug}.anchor.json").read_text(encoding="utf-8"))
        im = Image.open(POOL / f"{slug}.png").convert("RGB").resize(PAGE)
        panel = (0, 0, *PAGE)
        pb = panel_boxes(panel, PAGE, anc, motion_scale=SRC_SCALE["kling"])
        sol = solve(PAGE, [pb], cap)
        d = ImageDraw.Draw(im)
        if pb["keep"]:
            d.rectangle(pb["keep"], outline=(40, 90, 220), width=4)
        if pb["core"]:
            d.rectangle(pb["core"], outline=(0, 200, 220), width=4)
        x, y, w, h = sol["box"]
        d.rectangle([x, y, x + w, y + h], outline=(30, 200, 60) if sol["tier"] == 1 else (230, 60, 40), width=6)
        d.text((x + 8, y + 8), f"T{sol['tier']} {sol['style']}", font=font_at(sol["fsz"]), fill=(230, 60, 40))
        p = OUT / f"_layout_{slug}.png"
        im.save(p)
        print(f"{slug:22} tier={sol['tier']} style={sol['style']:6} box={sol['box']}  {sol['reason']}")
        print(f"   -> {p}")
