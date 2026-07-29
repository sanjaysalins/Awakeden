"""Piece 1 assembly step 1: loop-extend all 15 Gold Seam clips to their page's
exact dwell (matching the proven v2.1 page durations -- narration timing is
unchanged, only the pictures changed). All 15 clips are frozen-tableau (camera
locked, only light/dust breathe) -- symmetric motion, safe to boomerang --
EXCEPT p4b, which the animation prompt explicitly allowed a slow camera drift
on, so it uses forward-crossfade per the project's own rule (directional
motion must never boomerang).

  .venv\\Scripts\\python.exe poc_comic_page/_extend_piece1_clips.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE / "rung1"))
import _extend_loop as EL  # noqa

CLIPS = HERE / "_piece1" / "clips"
EXT = CLIPS / "extended"
EXT.mkdir(parents=True, exist_ok=True)

# (clip_stem, target_seconds, mode)
TARGETS = [
    ("p1a", 10.08, "boomerang"), ("p1b", 10.08, "boomerang"),
    ("p2a", 10.96, "boomerang"), ("p2b", 10.96, "boomerang"), ("p2c", 10.96, "boomerang"),
    ("panel_b", 12.10, "boomerang"), ("panel_a", 12.10, "boomerang"),
    ("panel_c", 12.10, "boomerang"), ("panel_d", 12.10, "boomerang"),
    ("p4a", 10.64, "boomerang"), ("p4b", 10.64, "forward"), ("p4c", 10.64, "boomerang"),
    ("p5a", 13.90, "boomerang"), ("p5b", 13.90, "boomerang"), ("p5c", 13.90, "boomerang"),
]


def main():
    results = []
    for name, target, mode in TARGETS:
        src = CLIPS / f"{name}.mp4"
        out = EXT / f"{name}.mp4"
        if not src.exists():
            print(f"[skip] {name}: no raw clip at {src}")
            results.append((name, "MISSING", None))
            continue
        print(f"[extend] {name} -> {target:.2f}s {mode} ...")
        if mode == "boomerang":
            EL.extend_boomerang(src, out, target, fps=24)
        else:
            EL.extend_forward_crossfade(src, out, target, fps=24, crossfade=0.5)
        dur = EL.probe_duration(out)
        delta = dur - target
        status = "ok" if abs(delta) < 0.05 else f"DRIFT {delta:+.2f}s"
        print(f"   {out.name} -> {dur:.2f}s ({status})")
        results.append((name, status, dur))
    print("\n=== summary ===")
    for name, status, dur in results:
        print(f"  {name:10s} {status:12s} {dur if dur else ''}")


if __name__ == "__main__":
    main()
