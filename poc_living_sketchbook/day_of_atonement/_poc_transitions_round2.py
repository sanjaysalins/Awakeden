"""POC (2026-08-05, round 3): the 4 transition options the user picked from
the design panel's menu -- Unseen Hand, Leaf-Flick, Tipped-In Plate (all new
panel_animator/ modules this session) and Lift-Away (an already-built,
previously-unused module, retimed for a general-purpose ~0.9s cut instead of
its original 2.3s reflective-turn design). Same 3 varied cut pairs as round 1
(narrative-to-narrative, narrative-to-versecard, beat-turn) so all 7 options
tested so far (blot, wipe, tailored-origin, slow-duration, + these 4) sit in
one comparable set.

Builds [~2s tail of A] + [transition] + [~2s head of B] per pair/mode, same
context-preserving pattern as round 1/2. Writes to _poc_transitions/.

Run:
    .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_poc_transitions_round2.py
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "panel_animator"))
import unseen_hand  # noqa: E402
import leaf_flick  # noqa: E402
import tipped_in_plate  # noqa: E402
from lift_away import LiftAwayPage  # noqa: E402
from page_transitions import scale_crop  # noqa: E402

HERE = Path(__file__).resolve().parent
SEGMENTS = HERE / "_segments"
OUT = HERE / "_poc_transitions"
OUT.mkdir(exist_ok=True)
WORK = OUT / "_work"
WORK.mkdir(exist_ok=True)

W, H, FPS = 1920, 1080, 30
SCALE_CROP = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
VCODEC = ["-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", str(FPS)]
CONTEXT_S = 2.0

PAIRS = [
    ("narrative_to_narrative", "s01_cold_open", "s02_tabernacle_wide"),
    ("narrative_to_versecard", "s19_altar_ministry", "s20_blood_atonement_card"),
    ("beat_turn", "s45_sign_before_veil", "s46_aged_unchanged_veil"),
]

MODES = {
    "unseen_hand": 0.7,
    "leaf_flick": 0.32,
    "tipped_in_plate": 0.6,
    "lift_away": 0.9,
}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"FAILED: {' '.join(str(c) for c in cmd)}\n{r.stderr[-3000:]}")


def context_clip(clip: Path, dest: Path, from_end: bool, skip_s: float, take_s: float):
    cmd = ["ffmpeg", "-y", "-v", "error"]
    if from_end:
        cmd += ["-sseof", f"-{take_s:.3f}"]
    else:
        cmd += ["-i", str(clip), "-ss", f"{skip_s:.3f}"]
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(clip), "-ss", f"{skip_s:.3f}",
               "-t", f"{take_s:.3f}", "-vf", SCALE_CROP, *VCODEC, str(dest)]
        run(cmd)
        return
    cmd += ["-i", str(clip), "-t", f"{take_s:.3f}", "-vf", SCALE_CROP, *VCODEC, str(dest)]
    run(cmd)


def build_lift_away_bridge(a_clip: Path, b_clip: Path, dest: Path, duration: float):
    a_png, b_png = WORK / f"{dest.stem}_a.png", WORK / f"{dest.stem}_b.png"
    run(["ffmpeg", "-y", "-v", "error", "-sseof", "-0.1", "-i", str(a_clip), "-frames:v", "1",
         "-vf", SCALE_CROP, str(a_png)])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(b_clip), "-frames:v", "1",
         "-vf", SCALE_CROP, str(b_png)])
    above = scale_crop(Image.open(a_png).convert("RGB"), W, H)
    below = scale_crop(Image.open(b_png).convert("RGB"), W, H)
    grab_t, lift_t, settle_t = duration * 0.22, duration * 0.5, duration
    tr = LiftAwayPage(above, below, grab_t=grab_t, lift_t=lift_t, settle_t=settle_t)

    frames_dir = WORK / f"{dest.stem}_frames"
    frames_dir.mkdir(exist_ok=True)
    n = max(1, int(round(duration * FPS)))
    for i in range(n):
        t = i / FPS
        tr.compose(t).save(frames_dir / f"f{i:04d}.png")
    run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(frames_dir / "f%04d.png"),
         *VCODEC, str(dest)])


def build(label: str, a_name: str, b_name: str, mode: str, duration: float):
    a_clip = SEGMENTS / f"seg_{a_name}.mp4"
    b_clip = SEGMENTS / f"seg_{b_name}.mp4"
    dest = OUT / f"{label}_{mode}.mp4"

    a_head = WORK / f"{label}_{mode}_a_head.mp4"
    context_clip(a_clip, a_head, True, 0, CONTEXT_S - duration)

    trans = WORK / f"{label}_{mode}_trans.mp4"
    if mode == "unseen_hand":
        unseen_hand.render(a_clip, b_clip, trans, duration)
    elif mode == "leaf_flick":
        leaf_flick.render(a_clip, b_clip, trans, duration)
    elif mode == "tipped_in_plate":
        tipped_in_plate.render(a_clip, b_clip, trans, duration)
    elif mode == "lift_away":
        build_lift_away_bridge(a_clip, b_clip, trans, duration)

    b_tail = WORK / f"{label}_{mode}_b_tail.mp4"
    context_clip(b_clip, b_tail, False, duration, CONTEXT_S - duration)

    listfile = WORK / f"{label}_{mode}_concat.txt"
    listfile.write_text(
        f"file '{a_head.resolve()}'\nfile '{trans.resolve()}'\nfile '{b_tail.resolve()}'\n",
        encoding="utf-8")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(listfile),
         *VCODEC, str(dest)])
    print(f"[ok] {label} ({mode}) -> {dest}")


if __name__ == "__main__":
    for label, a_name, b_name in PAIRS:
        for mode, dur in MODES.items():
            build(label, a_name, b_name, mode, dur)
