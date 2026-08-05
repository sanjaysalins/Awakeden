"""POC (2026-08-05, round 2b): 2 more transition options on top of the
blot/wipe comparison in _poc_cut_transitions.py -- user asked "what are
more options." The skill's own guidance (ink-transition SKILL.md) says the
blot origin should sit at the story's focal point, not dead center by
default -- round 1 used a generic (0.5, 0.55) for every pair. This tests:
  1. blot with a TAILORED origin (Aaron's face, where the eye actually goes
     on the cold-open still) instead of the generic point.
  2. a slower duration (1.4s instead of the 0.9s default) on the veil-to-veil
     beat-turn pair, to compare pacing -- a lingering bleed vs a quick one.

Run:
    .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_poc_cut_transitions_v2.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "panel_animator"))
import ink_transition  # noqa: E402

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


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"FAILED: {' '.join(str(c) for c in cmd)}\n{r.stderr[-3000:]}")


def build(label: str, a_name: str, b_name: str, mode: str, origin: tuple, duration: float):
    a_clip = SEGMENTS / f"seg_{a_name}.mp4"
    b_clip = SEGMENTS / f"seg_{b_name}.mp4"
    dest = OUT / f"{label}.mp4"

    a_head = WORK / f"{label}_a_head.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-sseof", f"-{CONTEXT_S:.3f}", "-i", str(a_clip),
         "-t", f"{(CONTEXT_S - duration):.3f}", "-vf", SCALE_CROP, *VCODEC, str(a_head)])

    trans = WORK / f"{label}_trans.mp4"
    ink_transition.render(a_clip, b_clip, trans, duration, mode, origin, FPS)

    b_tail = WORK / f"{label}_b_tail.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(b_clip), "-ss", f"{duration:.3f}",
         "-t", f"{(CONTEXT_S - duration):.3f}", "-vf", SCALE_CROP, *VCODEC, str(b_tail)])

    listfile = WORK / f"{label}_concat.txt"
    listfile.write_text(
        f"file '{a_head.resolve()}'\nfile '{trans.resolve()}'\nfile '{b_tail.resolve()}'\n",
        encoding="utf-8")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(listfile),
         *VCODEC, str(dest)])
    print(f"[ok] {label} -> {dest}")


if __name__ == "__main__":
    # 1. tailored origin -- blot starts right at Aaron's face, not a generic point
    build("tailored_origin_blot", "s01_cold_open", "s02_tabernacle_wide",
          "blot", (0.50, 0.30), 0.9)
    # 2. slower duration -- a lingering 1.4s bleed instead of the 0.9s default
    build("slow_duration_blot", "s45_sign_before_veil", "s46_aged_unchanged_veil",
          "blot", (0.50, 0.50), 1.4)
