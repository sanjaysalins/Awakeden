"""POC (2026-08-05): replace the dynamic_cam3d push/arc hold-filler (user:
"I hate this animation, stop zoom in kenburns, it makes it look very
amateurish") with "The Lamp Finds the Page" -- raking-light sweep +
gold-leaf flare + a subtle line-boil wobble, over the clip's own last frame.
No camera move at all; the PAGE stays still and the LIGHT moves over it,
same register as this project's existing raking-light/line-boil skills.

Builds each POC spread as [real clip, played forward once] + [new living-
light tail], exactly the same plumbing as the current fwd_drift mode in
_s6_assemble.py, just swapping the tail generator. Nothing else in the film
touches -- this writes to a separate _poc_tails/ folder and a standalone
comparison gallery, NOT into clips/ or _segments/.

Run:
    .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_poc_tail_alternatives.py
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "panel_animator"))
from raking_light import apply_raking_light, paper_tooth_highpass  # noqa: E402
from line_boil import boil_params  # noqa: E402

HERE = Path(__file__).resolve().parent
CLIPS = HERE / "clips"
OUT = HERE / "_poc_tails"
OUT.mkdir(exist_ok=True)
WORK = OUT / "_work"
WORK.mkdir(exist_ok=True)

W, H, FPS = 1920, 1080, 30
SCALE_CROP = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
VCODEC = ["-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", str(FPS)]

WINDOWS = HERE / "_spread_windows.json"
rows = {r["name"]: r for r in json.loads(WINDOWS.read_text(encoding="utf-8"))}

# 3 varied spreads, picked for a real (not trivial) tail length + different
# content classes: object close-up, wide landscape, verse card.
SPREADS = ["s42_basin_linen_ready", "s68_east_west_horizon", "s16_lords_charge_card"]

BOIL_AMOUNT = 1.0
MARGIN = 1.03  # oversample so the boil's rotate/translate never exposes an edge


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"FAILED: {' '.join(str(c) for c in cmd)}\n{r.stderr[-3000:]}")


def build_living_light_tail(last_frame: Image.Image, tail_s: float, dest: Path):
    n = max(1, int(round(tail_s * FPS)))
    base = last_frame.convert("RGB").resize((W, H), Image.LANCZOS)
    tooth = paper_tooth_highpass(base)

    bw, bh = int(W * MARGIN), int(H * MARGIN)
    ox, oy = (bw - W) // 2, (bh - H) // 2
    base_padded = base.resize((bw, bh), Image.LANCZOS)

    frames_dir = WORK / f"{dest.stem}_frames"
    frames_dir.mkdir(exist_ok=True)
    for i in range(n):
        progress = i / max(1, n - 1)
        t = i / FPS
        # boil ramps in over the first 0.5s so frame 0 is byte-close to the
        # incoming clip's real last frame (no visible seam at the handoff)
        ramp = min(1.0, t / 0.5)
        dx, dy, rot = boil_params(t, BOIL_AMOUNT * ramp)

        wobbled = base_padded.rotate(rot, resample=Image.BICUBIC, center=(bw / 2, bh / 2))
        left, top = ox - dx, oy - dy
        wobbled = wobbled.crop((int(left), int(top), int(left) + W, int(top) + H))

        lit = apply_raking_light(wobbled, progress, tooth=tooth, k=0.03)
        lit.save(frames_dir / f"f{i:05d}.png")

    run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(frames_dir / "f%05d.png"),
         *VCODEC, str(dest)])


def build_poc(name: str):
    row = rows[name]
    clip = CLIPS / f"{name}.mp4"
    tail_s = row["tail_s"]
    dest = OUT / f"{name}_livinglight.mp4"

    fwd = WORK / f"{name}_fwd.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(clip), "-vf", SCALE_CROP, *VCODEC, str(fwd)])

    last_frame_path = WORK / f"{name}_lastframe.png"
    run(["ffmpeg", "-y", "-v", "error", "-sseof", "-0.15", "-i", str(clip),
         "-frames:v", "1", str(last_frame_path)])
    last_frame = Image.open(last_frame_path)

    tail = WORK / f"{name}_tail.mp4"
    build_living_light_tail(last_frame, tail_s, tail)

    listfile = WORK / f"{name}_concat.txt"
    listfile.write_text(f"file '{fwd.resolve()}'\nfile '{tail.resolve()}'\n", encoding="utf-8")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(listfile),
         *VCODEC, str(dest)])
    print(f"[ok] {name}: tail={tail_s:.2f}s -> {dest}")


if __name__ == "__main__":
    for name in SPREADS:
        build_poc(name)
