"""Her Seed -- s05 "The Rubber-Stamp Genealogy" motion graphic. Production
build of the concept Fable designed and the user approved from the preview
(`_MOTION_CONCEPTS_s03_s05.html`), replacing the flat $0 line_boil hold.

Reuses blue_line.py's own hand-wobbled-front mask TECHNIQUE (jittered
polygon + Gaussian blur), rotated 90 degrees -- a horizontal front
descending top->bottom instead of a diagonal one -- per that skill's own
guardrail against hand-rolling a second mask-generation routine.

The zigzag genealogy line and all 5 silhouettes are already baked into the
still's own raster art, so a progressive top-to-bottom reveal of the SAME
finished image (composited over a blank paper veil) is enough to make the
whole device -- figures AND the connecting line -- feel like it is
arriving in sequence, with no second overlay layer needed. Brief
brightness pulses at each figure's vertical position sell the
"stamp-press" rhythm on top of the reveal. A small ink blot grows at the
very end, past the fifth figure, standing in for the unwritten sixth name
-- the trapdoor the next spread ("Here, he doesn't...") falls through.

  .venv\\Scripts\\python.exe poc_living_sketchbook/her_seed/_s05_genealogy_reveal.py
"""
import random
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "panel_animator"))
from blue_line import scale_crop  # noqa: E402 -- reuse, don't duplicate

HERE = Path(__file__).resolve().parent
STILL = HERE / "stills" / "s05_line_of_fathers_vertical.png"
OUT = HERE / "clips" / "s05_line_of_fathers_vertical.mp4"
WORK = HERE / "_s05_work"

W, H, FPS = 1080, 1920, 30
DURATION = 5.0
FIGURE_Y_FRAC = [0.10, 0.28, 0.46, 0.64, 0.82]  # vertical centers, estimated from the locked still
REVEAL_START, REVEAL_END = 0.06, 0.86           # fraction of DURATION the wipe runs across
BLOT_START = 0.90                                # fraction of DURATION the ink blot begins
FEATHER_PX = 90.0


def _horizontal_wobbled_mask(w, h, progress, seed=7, feather_px=FEATHER_PX):
    """0/255 feathered mask: 255 = show finished (revealed), 0 = show veil
    (not yet revealed). A hand-wobbled front descends top->bottom as
    progress goes 0->1 -- same jittered-polygon-then-Gaussian-blur
    technique as blue_line._wobbled_diagonal_mask, rotated 90 degrees."""
    rng = random.Random(seed)
    margin = feather_px * 3.0
    front_y = -margin + max(0.0, min(1.0, progress)) * (h + 2 * margin)
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    step = 40
    jitter = feather_px * 0.5
    poly = [(-margin, -margin * 2), (w + margin, -margin * 2)]
    x = w + step
    while x >= -step:
        poly.append((x, front_y + rng.uniform(-jitter, jitter)))
        x -= step
    d.polygon(poly, fill=255)
    return m.filter(ImageFilter.GaussianBlur(feather_px * 0.4))


def main():
    WORK.mkdir(exist_ok=True)
    finished = scale_crop(Image.open(STILL).convert("RGB"), W, H)

    # veil: blank aged paper, sampled from the still's own top margin (untouched cream stock)
    sample = finished.crop((0, 0, W, int(H * 0.03)))
    paper_color = tuple(int(v) for v in np.array(sample).reshape(-1, 3).mean(axis=0))
    veil = Image.new("RGB", (W, H), paper_color)

    margin = FEATHER_PX * 3.0
    n = int(DURATION * FPS)
    for i in range(n):
        t = i / FPS
        frac = t / DURATION
        reveal_progress = (frac - REVEAL_START) / max(1e-6, (REVEAL_END - REVEAL_START))
        mask = _horizontal_wobbled_mask(W, H, reveal_progress)
        frame = Image.composite(finished, veil, mask)

        # stamp pulses: brief brightness flash as the front passes each figure's y
        front_y = -margin + max(0.0, min(1.0, reveal_progress)) * (H + 2 * margin)
        arr = np.array(frame).astype(float)
        for fy_frac in FIGURE_Y_FRAC:
            fy = fy_frac * H
            dist = abs(front_y - fy)
            if dist < 90:
                pulse = (1.0 - dist / 90.0) ** 2 * 50.0
                y0, y1 = max(0, int(fy - 130)), min(H, int(fy + 130))
                arr[y0:y1] = np.clip(arr[y0:y1] + pulse, 0, 255)
        frame = Image.fromarray(arr.astype("uint8"))

        # ink blot growing past the fifth figure, end of clip
        if frac >= BLOT_START:
            blot_p = (frac - BLOT_START) / (1.0 - BLOT_START)
            r = 3 + blot_p * 9
            bx, by = int(W * 0.485), int(H * 0.895)
            d = ImageDraw.Draw(frame)
            shade = int(30 + 10 * (1 - blot_p))
            d.ellipse([bx - r, by - r, bx + r, by + r], fill=(shade, shade, shade))

        frame.save(WORK / f"f{i:04d}.png")

    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(WORK / "f%04d.png"),
         "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(OUT)], check=True)

    for f in WORK.glob("f*.png"):
        f.unlink()
    WORK.rmdir()
    print(f"[ok] -> {OUT}")


if __name__ == "__main__":
    main()
