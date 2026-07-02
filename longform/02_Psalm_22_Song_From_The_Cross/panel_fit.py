#!/usr/bin/env python
"""Scientific, repeatable panel-crop solver — stop the grid chopping heads.

A clip dropped into a grid panel is scale-to-filled then cropped (comic_engine._panel_fill).
The engine crops from dead centre (bias 0.5,0.5), blind to where the subject is, so a tall/wide
panel slices off whatever sits at the edge — usually the head. This module makes the crop a SOLVED
equation instead of a guess:

  MEASURE  each still once -> <slug>.anchor.json : a normalised keep-box (must-never-crop) + focus
  SOLVE    solve_crop(panel, still, anchor, motion) -> (bias, zoom) that keeps the box in frame,
           or fit=False when the panel aspect simply cannot contain it (template-aspect mismatch)
  VERIFY   fit_report(...) -> pre-flight warnings BEFORE any render/Kling spend

Coordinates are normalised 0..1 in the still. Still and clip share aspect (both 16:9), so a box
measured on the still transfers to the animated clip. Motion adds head-room (a push-in tightens).

No third-party deps (numpy/PIL only). Key-independent (no Anthropic API — anchors are local/cached).
"""
import json
from pathlib import Path

# extra top head-room for a push-in (the subject grows/rises toward the focus as it tightens)
_MOTION_TOP_PAD = {"pushin": 0.08, "dolly": 0.06, "pullback": 0.0, "static": 0.0}
_DEFAULT_PAD = 0.06


def _window_at_zoom(a_src, a_panel, zoom):
    """Normalised (cw, ch) of the crop window in source space at a given zoom (>=1 tightens)."""
    if a_src >= a_panel:            # source wider than panel -> full height, crop width
        cw, ch = a_panel / a_src, 1.0
    else:                           # source taller than panel -> full width, crop height
        cw, ch = 1.0, a_src / a_panel
    return cw / zoom, ch / zoom


def _place(lo_needed, hi_needed, cw, focus):
    """Pick a window top-left on one axis that covers [lo_needed, hi_needed], centred on focus.
    Returns (bias01, ok, deficit). bias01 in [0,1] maps to engine bias. ok=False if box too big."""
    span = 1.0 - cw
    if span <= 1e-6:                # window fills the axis (no crop on this axis)
        return 0.5, (hi_needed - lo_needed) <= cw + 1e-6, max(0.0, (hi_needed - lo_needed) - cw)
    wl_min = max(0.0, hi_needed - cw)     # window-left must be small enough to cover hi
    wl_max = min(span, lo_needed)         # window-left must be large enough to cover lo
    if wl_min <= wl_max + 1e-9:           # box fits -> centre on focus within the feasible band
        wl = min(max(focus - cw / 2.0, wl_min), wl_max)
        return wl / span, True, 0.0
    # box bigger than window -> cannot contain; protect the FOCUS, report the deficit
    wl = min(max(focus - cw / 2.0, 0.0), span)
    return wl / span, False, (hi_needed - lo_needed) - cw


def solve_crop(panel_wh, still_wh, anchor, motion="static"):
    """Deterministic. -> dict(bias=(bx,by), zoom, fit, lost=(dx,dy), reason).
    panel_wh, still_wh = (w,h) pixel sizes. anchor = {keep:[x0,y0,x1,y1], focus:[fx,fy], pad?}."""
    pw, ph = panel_wh
    sw, sh = still_wh
    a_panel, a_src = pw / ph, sw / sh
    x0, y0, x1, y1 = anchor["keep"]
    fx, fy = anchor.get("focus", [(x0 + x1) / 2.0, (y0 + y1) / 2.0])
    pad = anchor.get("pad", _DEFAULT_PAD)
    top_pad = pad + _MOTION_TOP_PAD.get(motion, 0.0)
    # padded keep-box (extra head-room on top for tightening motions)
    kx0, ky0 = max(0.0, x0 - pad), max(0.0, y0 - top_pad)
    kx1, ky1 = min(1.0, x1 + pad), min(1.0, y1 + pad)

    zoom = 1.0                      # z=1 gives the LARGEST window = best containment
    cw, ch = _window_at_zoom(a_src, a_panel, zoom)
    bx, okx, dx = _place(kx0, kx1, cw, fx)
    by, oky, dy = _place(ky0, ky1, ch, fy)
    fit = okx and oky
    reason = ""
    if not fit:
        worst = "width" if dx >= dy else "height"
        reason = (f"panel {a_panel:.2f}:1 vs still {a_src:.2f}:1 — keep-box {worst} exceeds the "
                  f"crop window by {max(dx, dy) * 100:.0f}% (focus protected, edges clipped). "
                  f"Consider a panel closer to {a_src:.2f}:1.")
    return {"bias": (round(bx, 4), round(by, 4)), "zoom": round(zoom, 4),
            "fit": fit, "lost": (round(dx, 4), round(dy, 4)), "reason": reason}


# ---------------- anchor IO ----------------
def load_anchor(pool: Path, slug: str):
    p = pool / f"{slug}.anchor.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def default_anchor():
    """No sidecar -> assume the subject is the upper-centre (where heads live), protect focus."""
    return {"keep": [0.30, 0.06, 0.70, 0.72], "focus": [0.50, 0.34], "pad": _DEFAULT_PAD,
            "note": "DEFAULT (no measured anchor) — upper-centre subject guess"}


# ---------------- pre-flight gate ----------------
def fit_report(beats, pool: Path, panel_rects_fn, still_size_fn):
    """Iterate beats -> panels, solve each clip, collect warnings. panel_rects_fn(tpl)->[(x,y,w,h)],
    still_size_fn(slug)->(w,h). Returns list of dict rows (one per clip↔panel pairing)."""
    rows = []
    for i, b in enumerate(beats, 1):
        rects = panel_rects_fn(b["tpl"])
        clips = b["clips"]
        for k, (x, y, w, h) in enumerate(rects):
            c = clips[k % len(clips)]
            slug = c["slug"]
            anc = load_anchor(pool, slug) or default_anchor()
            sol = solve_crop((w, h), still_size_fn(slug), anc, c.get("motion", "static"))
            rows.append({"beat": i, "tpl": b["tpl"], "panel": k, "slug": slug,
                         "measured": load_anchor(pool, slug) is not None, **sol})
    return rows
