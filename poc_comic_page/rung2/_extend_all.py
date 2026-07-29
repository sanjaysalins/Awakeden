"""Comic Page Pipeline POC -- Rung 2 FINAL PHASE, Step 3: loop-extend all 14
raw clips to their page's exact dwell, $0 deterministic ffmpeg via rung1's
_extend_loop.py (boomerang / forward-crossfade). All 14 motions here are
symmetric/non-directional (breathing light, drifting motes, swaying cords,
flickering) so every clip uses boomerang, same as all 4 rung1 extensions.

  .venv\\Scripts\\python.exe poc_comic_page/rung2/_extend_all.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE.parent / "rung1"))
import _extend_loop as EL  # noqa

CLIPS = HERE / "clips"
EXT = CLIPS / "extended"
EXT.mkdir(parents=True, exist_ok=True)

# (clip_stem, target_seconds)
TARGETS = [
    ("p1a", 10.08), ("p1b", 10.08),
    ("p2a", 10.96), ("p2b", 10.96), ("p2c", 10.96),
    ("panel_b", 12.10), ("panel_c", 12.10), ("panel_d", 12.10),
    ("p4a", 10.64), ("p4b", 10.64), ("p4c", 10.64),
    ("p5a", 13.90), ("p5b", 13.90), ("p5c", 13.90),
]


def main():
    results = []
    for name, target in TARGETS:
        src = CLIPS / f"{name}.mp4"
        out = EXT / f"{name}.mp4"
        if not src.exists():
            print(f"[skip] {name}: no raw clip at {src}")
            results.append((name, "MISSING", None))
            continue
        print(f"[extend] {name} -> {target:.2f}s boomerang ...")
        EL.extend_boomerang(src, out, target, fps=24)
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
