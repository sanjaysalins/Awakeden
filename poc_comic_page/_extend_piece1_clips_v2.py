"""Piece 1 v2 (period-corrected) assembly step 1: loop-extend all 15 clips to
their page dwell. Same durations as the approved build, including the
already-extended page5 lingering hold (17.90s, not the original 13.90s).
All frozen-tableau, safe to boomerang, except p4b (allowed camera drift).

  .venv\\Scripts\\python.exe poc_comic_page/_extend_piece1_clips_v2.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE / "rung1"))
import _extend_loop as EL  # noqa

CLIPS = HERE / "_piece1" / "clips_v2"
EXT = CLIPS / "extended"
EXT.mkdir(parents=True, exist_ok=True)

# (clip_stem, target_seconds, mode)
TARGETS = [
    ("p1a", 10.08, "boomerang"), ("p1b", 10.08, "boomerang"),
    ("p2a", 10.96, "boomerang"), ("p2b", 10.96, "boomerang"), ("p2c", 10.96, "boomerang"),
    ("panel_b", 12.10, "boomerang"), ("panel_a", 12.10, "boomerang"),
    ("panel_c", 12.10, "boomerang"), ("panel_d", 12.10, "boomerang"),
    ("p4a", 10.64, "boomerang"), ("p4b", 10.64, "forward"), ("p4c", 10.64, "boomerang"),
    ("p5a", 17.90, "boomerang"), ("p5b", 17.90, "boomerang"), ("p5c", 17.90, "boomerang"),
]


def main():
    for name, target, mode in TARGETS:
        src = CLIPS / f"{name}.mp4"
        out = EXT / f"{name}.mp4"
        if not src.exists():
            print(f"[skip] {name}: no raw clip at {src}")
            continue
        print(f"[extend] {name} -> {target:.2f}s {mode} ...")
        if mode == "boomerang":
            EL.extend_boomerang(src, out, target, fps=24)
        else:
            EL.extend_forward_crossfade(src, out, target, fps=24, crossfade=0.5)
        dur = EL.probe_duration(out)
        print(f"   {out.name} -> {dur:.2f}s")


if __name__ == "__main__":
    main()
