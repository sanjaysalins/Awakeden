"""POC (2026-08-05, round 3): user confirmed "plain hold, no camera move,
transition carries the cut" -- which means the 18 deterministic spreads
that used push/arc as their PRIMARY animation (not a hold-filler) become
pure static holds once the camera move is dropped too. User asked to test
what that reads like, and to compare against the "spotlight" family from
the earlier design pass (panel_animator/focal_tour.py) -- light settles on
the subject rather than a camera moving, so it isn't "amateurish zoom" but
also isn't a dead frozen frame either.

2 spreads (a long hold and a short one, so the timing tradeoff is visible),
4 treatments each (one skipped where its own minimum timing doesn't fit the
duration -- flagged, not silently forced): plain static hold, dramatic
spotlight, caravaggio pulse (breathing halo), slow breath (very slow settle
-- long-hold spreads only, its own minimum schedule is ~17s).

Single face-region focal box per still (eye-checked against the art) -- a
single-figure portrait doesn't need a multi-element tour, just one settle.

Run:
    .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_poc_spotlight_holds.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "panel_animator"))
import focal_tour  # noqa: E402

HERE = Path(__file__).resolve().parent
STILLS = HERE / "stills"
OUT = HERE / "_poc_spotlight"
OUT.mkdir(exist_ok=True)

W, H = 1920, 1080

# (name, duration_s, focal bbox [x%,y%,w%,h%] -- face, eye-checked)
SPREADS = [
    ("s51_jesus_pivot", 13.32, [38, 6, 24, 32]),
    ("s60_seated_glory", 7.42, [40, 4, 20, 30]),
]


def build_static(name: str, still: Path, duration: float, dest: Path):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(still),
                    "-t", f"{duration:.3f}",
                    "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", str(dest)],
                   check=True, capture_output=True)
    print(f"[ok] {name} static -> {dest}")


if __name__ == "__main__":
    for name, dur, bbox in SPREADS:
        still = STILLS / f"{name}.png"
        regions = [{"bbox": bbox}]

        build_static(name, still, dur, OUT / f"{name}_static.mp4")

        # dramatic_spotlight / caravaggio_pulse: tune hold/move to the
        # spread's own duration rather than trust the style's 2.5/1.0/2.5
        # default (which needs >=8s minimum and would run past a short spread).
        init_hold = max(0.8, min(2.5, dur * 0.18))
        move = max(0.5, min(1.0, dur * 0.08))
        final_hold = max(0.8, min(2.5, dur * 0.18))
        for style in ("dramatic_spotlight", "caravaggio_pulse"):
            dest = OUT / f"{name}_{style}.mp4"
            focal_tour._RENDERERS[style](
                __import__("PIL.Image", fromlist=["Image"]).open(still).convert("RGB"),
                regions, dur, W, H, dest,
                initial_hold_sec=init_hold, move_sec=move, final_hold_sec=final_hold)
            print(f"[ok] {name} {style} -> {dest}")

        # slow_breath's own minimum schedule is ~17s (5+3+3+3+5 for n=1) --
        # its internal timing can't be overridden through render_clip (the
        # dispatcher hardcodes it), so on a shorter spread the render just
        # gets cut off wherever the (unfinished) schedule is at that point.
        # Render it anyway on both and eye-check rather than assume broken.
        dest = OUT / f"{name}_slow_breath.mp4"
        focal_tour.render_clip(still, regions, "slow_breath", dur, W, H, dest)
        note = "" if dur >= 17.0 else f" (NOTE: {dur:.1f}s < its own ~17s minimum -- may not finish settling back)"
        print(f"[ok] {name} slow_breath -> {dest}{note}")
