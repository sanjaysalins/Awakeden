#!/usr/bin/env python
"""Camera choreography across a live comic grid -- instead of every panel just
looping independently in its fixed cell, a virtual "page camera" racks focus
toward whichever panel currently holds attention (brighten, NOT zoom -- see
2026-07-24 note below) while the others dim, then smoothly moves on to the
next. Pure post-process over already-rendered clips, no new generation.

Draws a paper-coloured gutter between panels + a hand-wobbled ink border
around each -- without this the grid reads as clips taped together, not a
comic page (2026-07-24 finding).

Supports several named panel LAYOUTS (not just a fixed 2x2) so a sequence can
mix grid shapes and stay visually dynamic across a piece, per the same date's
follow-up: "let it be dynamic, sometimes hero, sometimes various grid
formations."

$0, deterministic: PIL per-frame compositing + ffmpeg encode.

Usage:
    python grid_choreography.py --clips a.mp4 b.mp4 c.mp4 d.mp4 --out grid.mp4 --layout 2x2
        [--per-panel 1.2] [--transition 0.35] [--w 1080 --h 1920]
        [--gutter 14] [--border-px 6] [--paper-hex #E8D9B5] [--ink-hex #231F20]
"""
from __future__ import annotations
import argparse
import math
import random
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance

FPS = 30
W, H = 1920, 1080

# Named layouts: each panel is a fractional (x, y, w, h) rect of the full
# canvas, BEFORE gutter inset (inset is applied uniformly per-panel in
# render()). Order matters -- it's the clip order on the CLI.
LAYOUTS: dict[str, list[tuple[float, float, float, float]]] = {
    "2x2":         [(0.0, 0.0, 0.5, 0.5), (0.5, 0.0, 0.5, 0.5),
                     (0.0, 0.5, 0.5, 0.5), (0.5, 0.5, 0.5, 0.5)],  # TL,TR,BL,BR
    "2v":          [(0.0, 0.0, 1.0, 0.5), (0.0, 0.5, 1.0, 0.5)],  # top / bottom
    "2h":          [(0.0, 0.0, 0.5, 1.0), (0.5, 0.0, 0.5, 1.0)],  # left / right
    "3-big-left":  [(0.0, 0.0, 0.62, 1.0), (0.62, 0.0, 0.38, 0.5), (0.62, 0.5, 0.38, 0.5)],
    "3-big-top":   [(0.0, 0.0, 1.0, 0.58), (0.0, 0.58, 0.5, 0.42), (0.5, 0.58, 0.5, 0.42)],
    "3-big-right": [(0.38, 0.0, 0.62, 1.0), (0.0, 0.0, 0.38, 0.5), (0.0, 0.5, 0.38, 0.5)],
}


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)


def activeness(panel_i: int, t: float, per_panel: float, trans: float, n: int) -> float:
    """0..1 how 'in focus' panel_i is at time t, smoothly crossfading at boundaries."""
    cur = int(t // per_panel) % n
    frac = (t % per_panel) / per_panel
    local_trans = trans / per_panel
    if panel_i == cur:
        if frac < local_trans:
            return ease(0.5 + 0.5 * frac / local_trans)          # rising from prior cut
        if frac > 1 - local_trans:
            return ease(0.5 + 0.5 * (1 - frac) / local_trans)    # falling into next cut
        return 1.0
    nxt = (cur + 1) % n
    if panel_i == nxt and frac > 1 - local_trans:
        return ease(0.5 * (frac - (1 - local_trans)) / local_trans)
    prv = (cur - 1) % n
    if panel_i == prv and frac < local_trans:
        return ease(0.5 * (1 - frac / local_trans))
    return 0.0


def _hex(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _wobbled_rect(draw: "ImageDraw.ImageDraw", box: tuple[int, int, int, int],
                   ink: tuple[int, int, int], width: int, seed: int) -> None:
    """A hand-inked border, not a perfect machine rectangle -- each edge is a short
    polyline with a small fixed (seed-based, not per-frame) jitter so it holds
    steady across the clip instead of crawling frame to frame."""
    rng = random.Random(seed)
    x0, y0, x1, y1 = box
    jig = max(2, width)

    def jitter_line(p0, p1, n=5):
        pts = []
        for i in range(n + 1):
            t = i / n
            x = p0[0] + (p1[0] - p0[0]) * t
            y = p0[1] + (p1[1] - p0[1]) * t
            if 0 < i < n:
                x += rng.uniform(-jig, jig)
                y += rng.uniform(-jig, jig)
            pts.append((x, y))
        draw.line(pts, fill=ink, width=width, joint="curve")

    jitter_line((x0, y0), (x1, y0))
    jitter_line((x1, y0), (x1, y1))
    jitter_line((x1, y1), (x0, y1))
    jitter_line((x0, y1), (x0, y0))


def render(clips: list[Path], out_mp4: Path, per_panel: float, trans: float,
           w: int = W, h: int = H, gutter: int = 10,
           paper_hex: str = "#E8D9B5", ink_hex: str = "#231F20", border_px: int = 5,
           layout: str = "2x2", total_duration: float | None = None):
    rects = LAYOUTS[layout]
    if len(rects) != len(clips):
        raise SystemExit(f"layout {layout!r} needs {len(rects)} clips, got {len(clips)}")

    # 2026-07-24 fix: DON'T inherit the source clip's own fps -- Kling outputs
    # 24fps, Seedance 30fps, so probing clips[0] made the grid's fps depend on
    # which source happened to be first, causing a real duration mismatch when
    # concatenated with other 30fps segments later (17s of drift on an 8s
    # clip). Always output the module's fixed FPS regardless of source.
    fps = FPS
    n = len(clips)
    # 2026-07-25 fix: `duration` used to be hardcoded to exactly one sweep
    # (per_panel * n). activeness() is already cyclic (`% n`), so a longer
    # explicit total_duration gives multiple sweeps across the same panels
    # for free -- needed when panel count is small relative to the piece's
    # runtime (comic-strip-grid effect: the page stays alive and read
    # multiple times, not one pass then done).
    duration = total_duration if total_duration is not None else per_panel * n
    n_frames = int(duration * fps)

    # 2026-07-24 fix: the panel PUSH used to zoom into an already-downscaled cell
    # (upsampling -> visible softness/pixelation, caught by the user: "careful not
    # to zoom in, it will [hurt] the resolution"). Fix: extract every cell AND the
    # composited canvas at SS x the true output size, and do the "push" as a PURE
    # TRANSLATE crop within that supersampled canvas -- never an upscale. The only
    # resize in the whole pipeline is the final supersample -> native downscale,
    # which sharpens, it doesn't soften.
    SS = 1.18
    boxes = []  # (ox, oy, cw, ch) in supersampled px, per panel
    for fx, fy, fw, fh in rects:
        x0, y0 = fx * w * SS, fy * h * SS
        x1, y1 = (fx + fw) * w * SS, (fy + fh) * h * SS
        g = gutter * SS / 2
        boxes.append((int(x0 + g), int(y0 + g), int(x1 - g) - int(x0 + g), int(y1 - g) - int(y0 + g)))
    centers = [(ox + cw / 2, oy + ch / 2) for ox, oy, cw, ch in boxes]
    paper = _hex(paper_hex)
    ink = _hex(ink_hex)

    work = out_mp4.parent / (out_mp4.stem + "_work")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    # 2026-07-25 fix: only extract each source clip's OWN natural length (not
    # `-t duration`, the full grid runtime) -- extracting frames past the
    # source's own end just repeats ffmpeg's last decoded frame under a new
    # name, which is how the old code silently froze every panel whose
    # spotlight dwell outlasted its ~5-6s source clip. Loop the real frames
    # instead (below) so every panel stays genuinely animated for its whole
    # time on screen, never a held still.
    frame_dirs = []
    for i, (c, (ox, oy, cw, ch)) in enumerate(zip(clips, boxes)):
        d = work / f"src{i}"
        d.mkdir()
        subprocess.run(["ffmpeg", "-y", "-i", str(c),
                        "-vf", f"scale={cw}:{ch}:force_original_aspect_ratio=increase,crop={cw}:{ch}",
                        "-r", str(fps), str(d / "f%05d.png")],
                       check=True, capture_output=True)
        frame_dirs.append(sorted(d.glob("f*.png")))

    out_dir = work / "grid_frames"
    out_dir.mkdir()
    ssw, ssh = int(w * SS), int(h * SS)
    for i in range(n_frames):
        t = i / fps
        acts = [activeness(p, t, per_panel, trans, n) for p in range(n)]
        canvas = Image.new("RGB", (ssw, ssh), paper)
        for p in range(n):
            src_frames = frame_dirs[p]
            # loop (wrap) the source's own frames instead of freezing on the
            # last one once i exceeds the clip's real length -- see fix note above
            cell = Image.open(src_frames[i % len(src_frames)]).convert("RGB")
            a = acts[p]
            bright = 0.45 + 0.55 * a
            cell = ImageEnhance.Brightness(cell).enhance(bright)
            cell = ImageEnhance.Contrast(cell).enhance(0.85 + 0.15 * a)
            # NO push-zoom on the cell itself -- brightness/contrast alone carries
            # the "spotlight" read without any resolution cost (2026-07-24).
            canvas.paste(cell, (boxes[p][0], boxes[p][1]))

        draw = ImageDraw.Draw(canvas)
        for p in range(n):
            ox, oy, cw, ch = boxes[p]
            _wobbled_rect(draw, (ox, oy, ox + cw, oy + ch), ink, int(border_px * SS), seed=1000 + p)

        # virtual page camera: PAN (translate only, never scale) toward the
        # attention-weighted centroid, cropped out of the supersampled canvas.
        tw = sum(acts) or 1.0
        fx = sum(a * c[0] for a, c in zip(acts, centers)) / tw
        fy = sum(a * c[1] for a, c in zip(acts, centers)) / tw
        sx = max(0, min(ssw - w, fx - w / 2))
        sy = max(0, min(ssh - h, fy - h / 2))
        frame = canvas.crop((int(sx), int(sy), int(sx) + w, int(sy) + h))
        frame.save(out_dir / f"g{i:05d}.png")

    subprocess.run(["ffmpeg", "-y", "-framerate", str(fps), "-i", str(out_dir / "g%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(fps), str(out_mp4)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--clips", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--per-panel", type=float, default=1.2, dest="per_panel")
    ap.add_argument("--transition", type=float, default=0.35, dest="trans")
    ap.add_argument("--w", type=int, default=W, help="output width (default 1920, 16:9)")
    ap.add_argument("--h", type=int, default=H, help="output height (default 1080, 16:9)")
    ap.add_argument("--gutter", type=int, default=10, help="px gap between panels + outer margin, paper-coloured")
    ap.add_argument("--paper-hex", default="#E8D9B5", dest="paper_hex")
    ap.add_argument("--ink-hex", default="#231F20", dest="ink_hex")
    ap.add_argument("--border-px", type=int, default=5, dest="border_px")
    ap.add_argument("--layout", default="2x2", choices=sorted(LAYOUTS.keys()))
    ap.add_argument("--total-duration", type=float, default=None, dest="total_duration",
                     help="override total runtime (enables multiple cyclic sweeps across the "
                          "same panels instead of exactly one per_panel*n pass)")
    a = ap.parse_args()
    render([Path(c) for c in a.clips], Path(a.out), a.per_panel, a.trans,
           a.w, a.h, a.gutter, a.paper_hex, a.ink_hex, a.border_px, a.layout, a.total_duration)
