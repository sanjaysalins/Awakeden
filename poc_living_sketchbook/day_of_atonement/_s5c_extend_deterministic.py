"""Day of Atonement LONG -- step 5c: re-render the deterministic dynamic_cam3d
spreads whose real aligned window (per `_spread_windows.json`) runs LONGER
than the duration they were originally rendered at. Those were rendered
before real forced-alignment existed, using a guessed duration -- assembly
was covering the gap by holding the push/arc's LAST frame frozen for the
remainder (sometimes 5-6+ seconds). A multi-second freeze reads as "just a
still" -- the user flagged exactly this after watching the first cut. Fix:
re-run the SAME move/focus/amp (same still, same camera language, zero
repaint risk, zero new invention risk) at the REAL duration, so the camera
keeps gracefully moving across the whole window instead of finishing early
and freezing.

Only the 11 spreads with >0.5s positive drift get touched. The other 7
deterministic spreads (s05, s25, s26, s27, s45, spread54, spread55) already
match their real window closely (or run LONGER than the window, in which
case `_s6_assemble.py`'s once_trim mode already handles it correctly by
trimming -- extending would just add motion that gets cut off anyway).

Run AFTER `_s5b_spread_windows.py` has produced real windows, BEFORE the
final `_s6_assemble.py` build:
    .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_s5c_extend_deterministic.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "panel_animator"))
from dynamic_cam3d import render_move  # noqa: E402

HERE = Path(__file__).resolve().parent
STILLS = HERE / "stills"
CLIPS = HERE / "clips"
WINDOWS = HERE / "_spread_windows.json"

# (name, move, focus, amp) -- EXACT same camera language as the original
# render (_s_christ_spreads_orbit.py / _s25_orbit.py / _s76_landing.py /
# _s_fix_batch2_orbit.py), only the duration changes.
SPREADS = [
    ("s34_riddle_recap", "push", (0.68, 0.45), 0.5),
    ("s50_the_shadow", "arc", (0.55, 0.55), 0.6),
    ("s51_jesus_pivot", "push", (0.50, 0.28), 0.7),
    ("s52_jesus_entering_formal", "arc", (0.50, 0.40), 0.7),
    ("s53_the_cross", "arc", (0.51, 0.30), 0.8),
    ("s56_the_answer", "push", (0.50, 0.35), 0.7),
    ("s57_without_the_gate", "arc", (0.50, 0.55), 0.9),
    ("s60_seated_glory", "push", (0.50, 0.45), 0.6),
    ("s63_torn_veil_card", "push", (0.50, 0.42), 0.6),
    ("s66_high_priests_face", "arc", (0.50, 0.30), 0.5),
    ("s76_already_inside", "push", (0.50, 0.35), 0.5),
]

if __name__ == "__main__":
    rows = {r["name"]: r for r in json.loads(WINDOWS.read_text(encoding="utf-8"))}
    for name, move, focus, amp in SPREADS:
        still = STILLS / f"{name}.png"
        dest = CLIPS / f"{name}.mp4"
        target_dur = rows[name]["dur"]
        if not still.exists():
            print(f"[HOLD] {name}: still missing")
            continue
        out = render_move(still, move, target_dur, focus, dest, amp=amp)
        print(f"[ok] {name} ({move}, {target_dur:.2f}s) -> {out}")
