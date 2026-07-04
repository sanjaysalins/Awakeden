#!/usr/bin/env python
"""Animated Bible-map engine (deterministic, $0) — reusable for ANY journey.

Renders an inked base map + a progressively-drawn dashed route with a walking
CARAVAN marker (camel + rider + followers, distance-driven walk cycle), place
labels that pop in on arrival, and a title card, over a gentle push-in camera.
No generative repaint -> nothing morphs or hallucinates.

Everything is data-driven by a route file (see route.json). To animate a new
journey: render a base map, plot the waypoints, run this. Nothing else changes.

    python mapengine.py --route route.json --base base_map.png --out out.mp4

route.json schema:
    {
      "title": "THE EXODUS",
      "subtitle": "from Egypt  to  the Promised Land",
      "config": {                     # all optional; sensible defaults below
        "fps": 30, "travel_s": 8.0, "dwell_s": 0.5, "intro_s": 0.6,
        "outro_s": 2.6, "caravan_scale": 0.95, "camera_zoom": 0.05
      },
      "waypoints": [
        {"name": "RAMESES", "x": 0.30, "y": 0.82, "label_dx": 0, "label_dy": 0.055},
        ...
      ]
    }
"""
from __future__ import annotations
import argparse, json, math, shutil, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
import caravan

W, H = 1920, 1080
STEP = 2.0                      # densify spacing (px); revealed distance = n_rev*STEP

FONT_LABEL = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 34)
FONT_TITLE = ImageFont.truetype("C:/Windows/Fonts/BOOKOSB.TTF", 76)
FONT_SUB = ImageFont.truetype("C:/Windows/Fonts/georgiai.ttf", 38)

INK = (54, 36, 22)
ROUTE = (168, 44, 28)
GLOW = (214, 96, 52)
GOLD = (196, 150, 62)
PILL = (241, 228, 200, 225)

DEFAULTS = dict(fps=30, travel_s=8.0, dwell_s=0.5, intro_s=0.6, outro_s=2.6,
                title_fade_s=1.1, caravan_scale=0.95, camera_zoom=0.05)


# ----------------------------------------------------------------------------- geometry
def load_route(route_path: Path):
    data = json.loads(route_path.read_text(encoding="utf-8"))
    cfg = {**DEFAULTS, **data.get("config", {})}
    wps = [((w["x"] * W, w["y"] * H), w["name"],
            (w.get("label_dx", 0) * W, w.get("label_dy", 0) * H))
           for w in data["waypoints"]]
    return data, cfg, wps


def densify(vertices, step=STEP):
    cum = [0.0]
    for a, b in zip(vertices, vertices[1:]):
        cum.append(cum[-1] + math.dist(a, b))
    vfrac = [c / cum[-1] for c in cum]
    pts = [vertices[0]]
    for a, b in zip(vertices, vertices[1:]):
        n = max(1, int(math.dist(a, b) / step))
        for k in range(1, n + 1):
            t = k / n
            pts.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    return pts, vfrac


def build_timeline(vfrac, cfg):
    fps = cfg["fps"]

    def ease(t):
        return t * t * (3 - 2 * t)

    frames = []
    for _ in range(int(cfg["intro_s"] * fps)):
        frames.append((0.0, 0.0))
    for i in range(len(vfrac) - 1):
        p0, p1 = vfrac[i], vfrac[i + 1]
        dur = max(0.25, cfg["travel_s"] * (p1 - p0))
        nf = int(dur * fps)
        for fr in range(nf):
            frames.append((p0 + (p1 - p0) * ease(fr / nf), 0.0))
        if i < len(vfrac) - 2:
            for _ in range(int(cfg["dwell_s"] * fps)):
                frames.append((p1, 0.0))
    nf = int(cfg["outro_s"] * fps)
    for fr in range(nf):
        frames.append((1.0, ease(min(1.0, (fr / fps) / cfg["title_fade_s"]))))
    return frames


# ----------------------------------------------------------------------------- drawing
def draw_route(layer, pts, n_rev):
    """Dashed revealed route with a soft glow (no marker — caravan draws that)."""
    glow = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    d = ImageDraw.Draw(layer)
    dash = 7
    for i in range(1, n_rev):
        if (i // dash) % 2 == 0:
            gd.line([pts[i - 1], pts[i]], fill=(*GLOW, 255), width=16)
    layer.alpha_composite(glow.filter(ImageFilter.GaussianBlur(9)))
    for i in range(1, n_rev):
        if (i // dash) % 2 == 0:
            d.line([pts[i - 1], pts[i]], fill=(*ROUTE, 255), width=6)


def draw_marker(layer, pts, n_rev, scale):
    """Walking caravan at the revealed tip; walk phase driven by distance."""
    if n_rev < 1:
        return
    tip = pts[min(n_rev, len(pts)) - 1]
    prev = pts[max(0, min(n_rev, len(pts)) - 6)]
    facing = 1 if (tip[0] - prev[0]) >= 0 else -1
    dist = n_rev * STEP
    phase = (dist / (22.0 * scale)) * 2 * math.pi     # stride ~22px
    # soft drop shadow at the feet
    sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([tip[0] - 26 * scale, tip[1] - 5 * scale,
                                tip[0] + 26 * scale, tip[1] + 7 * scale], fill=(30, 20, 12, 90))
    layer.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)))
    caravan.draw_caravan(layer, tip[0], tip[1], facing=facing, phase=phase, scale=scale)


SAND = (214, 193, 150)
LIP = (30, 105, 110)          # deeper water heaped at the wall base
FOAM = (210, 236, 226)


def water_mask(base_rgb):
    """Boolean-ish 'L' mask of the map's teal sea/rivers (so the parting stays
    inside real water and never spills onto desert)."""
    a = np.asarray(base_rgb.convert("RGB")).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    wet = (b > 105) & (g > 105) & (r < 165) & (((g + b) / 2 - r) > 22) & (np.abs(g - b) < 72)
    return Image.fromarray((wet * 255).astype("uint8"), "L")


def parting_amount(progress, fc, fn):
    """0..1 openness: parts as the caravan reaches the crossing, holds while it
    walks through, closes behind it on the way to the next stop."""
    def ease(t):
        t = min(1.0, max(0.0, t))
        return t * t * (3 - 2 * t)

    open_before = 0.06
    span = max(1e-6, fn - fc)
    if progress < fc - open_before:
        return 0.0
    if progress < fc:
        return ease((progress - (fc - open_before)) / open_before)
    if progress < fc + 0.60 * span:
        return 1.0
    if progress < fc + 0.90 * span:
        return 1.0 - ease((progress - (fc + 0.60 * span)) / (0.30 * span))
    return 0.0


def draw_sea_parting(frame, C, angle, length_px, gap_px, amount, wmask):
    """A dry sand corridor cut through the map's water (the map's own teal is the
    wall), with a deeper-water lip + foam crests. Confined to real water pixels."""
    if amount <= 0.01:
        return
    sp = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(sp)
    ux, uy = math.cos(angle), math.sin(angle)
    vx, vy = -math.sin(angle), math.cos(angle)
    HL = length_px / 2
    hw = 0.5 * gap_px * amount
    lip = max(9, gap_px * 0.34)

    def P(u, v):
        return (C[0] + u * ux + v * vx, C[1] + u * uy + v * vy)

    # deeper-water lip heaped just outside the corridor edges
    for sgn in (1, -1):
        d.polygon([P(-HL, sgn * hw), P(HL, sgn * hw),
                   P(HL, sgn * (hw + lip)), P(-HL, sgn * (hw + lip))], fill=(*LIP, 255))
    # dry corridor
    d.polygon([P(-HL, -hw), P(HL, -hw), P(HL, hw), P(-HL, hw)], fill=(*SAND, 255))
    d.line([P(-HL, 0), P(HL, 0)], fill=(198, 182, 146, 90), width=4)   # wet sheen
    # foam crest (scalloped) along each corridor edge
    for sgn in (1, -1):
        inv = sgn * hw
        steps = max(4, int(length_px / 15))
        for i in range(steps + 1):
            u = -HL + i * (length_px / steps)
            fx, fy = P(u, inv)
            d.ellipse([fx - 5, fy - 5, fx + 5, fy + 5], fill=(*FOAM, 235))
        d.line([P(-HL, inv), P(HL, inv)], fill=(*FOAM, 255), width=3)
    # confine to the map's actual water, then soften
    sp.putalpha(ImageChops.multiply(sp.getchannel("A"), wmask))
    frame.alpha_composite(sp.filter(ImageFilter.GaussianBlur(1.0)))


def draw_pin(d, x, y):
    s = 15
    d.polygon([(x, y - s), (x + s, y), (x, y + s), (x - s, y)],
              fill=(*GOLD, 255), outline=(*INK, 255))
    d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(*INK, 255))


def draw_label(layer, x, y, dx, dy, text, alpha):
    if alpha <= 0.02:
        return
    d = ImageDraw.Draw(layer)
    draw_pin(d, x, y)
    tx, ty = x + dx, y + dy
    bb = d.textbbox((0, 0), text, font=FONT_LABEL)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pad = 14
    pill = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    pd = ImageDraw.Draw(pill)
    pd.rounded_rectangle([tx - tw / 2 - pad, ty - th / 2 - pad, tx + tw / 2 + pad, ty + th / 2 + pad],
                         radius=12, fill=PILL, outline=(*INK, 255), width=2)
    pd.text((tx - tw / 2, ty - th / 2 - bb[1]), text, font=FONT_LABEL, fill=(*INK, 255))
    if alpha < 1:
        pill.putalpha(pill.getchannel("A").point(lambda a: int(a * alpha)))
    layer.alpha_composite(pill)


def draw_title(layer, data, alpha):
    if alpha <= 0.02:
        return
    tl = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(tl)
    title, sub = data["title"], data.get("subtitle", "")
    cx = W / 2
    bb = d.textbbox((0, 0), title, font=FONT_TITLE)
    tw = bb[2] - bb[0]
    d.rounded_rectangle([cx - tw / 2 - 40, 44, cx + tw / 2 + 40, 190],
                        radius=16, fill=(241, 228, 200, 235), outline=(*INK, 255), width=3)
    d.text((cx - tw / 2, 58), title, font=FONT_TITLE, fill=(*ROUTE, 255))
    sbb = d.textbbox((0, 0), sub, font=FONT_SUB)
    d.text((cx - (sbb[2] - sbb[0]) / 2, 138), sub, font=FONT_SUB, fill=(*INK, 255))
    tl.putalpha(tl.getchannel("A").point(lambda a: int(a * alpha)))
    layer.alpha_composite(tl)


def apply_camera(frame, zoom, cx, cy):
    if zoom <= 1.0001:
        return frame
    cw, ch = W / zoom, H / zoom
    x0 = max(0, min(W - cw, cx - cw / 2))
    y0 = max(0, min(H - ch, cy - ch / 2))
    return frame.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.LANCZOS)


# ----------------------------------------------------------------------------- main
def render(base_png, route_json, out_mp4):
    data, cfg, wps = load_route(route_json)
    vertices = [p for p, _, _ in wps]
    pts, vfrac = densify(vertices)
    timeline = build_timeline(vfrac, cfg)

    base = Image.open(base_png).convert("RGB").resize((W, H), Image.LANCZOS)
    cx = sum(p[0] for p in vertices) / len(vertices)
    cy = sum(p[1] for p in vertices) / len(vertices)
    wmask = water_mask(base)

    # locate an optional sea-parting event (angle = the crossing leg's direction)
    parting = None
    for i, w in enumerate(data["waypoints"]):
        if "sea_parting" in w and i + 1 < len(vertices):
            sp = w["sea_parting"]
            a = vertices[i]
            b = vertices[i + 1]
            parting = dict(
                C=(sp["cx"] * W, sp["cy"] * H),
                angle=math.atan2(b[1] - a[1], b[0] - a[0]),
                length=sp["length"] * H, gap=sp["gap"] * H,
                fc=vfrac[i], fn=vfrac[i + 1])

    frames_dir = out_mp4.parent / (out_mp4.stem + "_frames")
    if frames_dir.exists():
        shutil.rmtree(frames_dir)
    frames_dir.mkdir(parents=True)

    N = len(timeline)
    for idx, (progress, talpha) in enumerate(timeline):
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        n_rev = max(0, int(progress * len(pts)))
        draw_route(layer, pts, n_rev)
        for i, (p, name, dl) in enumerate(wps):
            la = 1.0 if progress >= 1.0 else min(1.0, max(0.0, (progress - vfrac[i]) / 0.04))
            draw_label(layer, p[0], p[1], dl[0], dl[1], name, la)
        draw_marker(layer, pts, n_rev, cfg["caravan_scale"])
        draw_title(layer, data, talpha)

        frame = base.convert("RGBA")
        if parting:
            amt = parting_amount(progress, parting["fc"], parting["fn"])
            draw_sea_parting(frame, parting["C"], parting["angle"],
                             parting["length"], parting["gap"], amt, wmask)
        frame.alpha_composite(layer)
        zoom = 1.0 + cfg["camera_zoom"] * (idx / N)
        apply_camera(frame.convert("RGB"), zoom, cx, cy).save(frames_dir / f"f{idx:05d}.png")
        if idx % 30 == 0:
            print(f"  frame {idx}/{N}", flush=True)

    subprocess.run(["ffmpeg", "-y", "-framerate", str(cfg["fps"]),
                    "-i", str(frames_dir / "f%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(cfg["fps"]),
                    str(out_mp4)], check=True, capture_output=True)
    shutil.rmtree(frames_dir)
    print(f"[ok] {out_mp4}", flush=True)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=str(here / "base_map.png"))
    ap.add_argument("--route", default=str(here / "route.json"))
    ap.add_argument("--out", default=str(here / "A_caravan.mp4"))
    a = ap.parse_args()
    render(Path(a.base), Path(a.route), Path(a.out))
