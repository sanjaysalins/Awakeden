"""POC (2026-08-05, round 3): all 6 motion-design options from the panel's
menu -- a fresh lens on the "no camera movement" hold problem, distinct from
the paper-physics/light family already built in rounds 1-2. New modules in
panel_animator/: registration_snap.py, ink_up_build.py, palette_pivot.py,
crop_mark_approval.py, letterpress_beat.py. Locked-Plate Parallax needs zero
new code -- it's the existing parallax_25d.py called with bg_amp=0 (the
"plate locked, one interior layer floats" configuration the panel argued is
genuinely camera-free, unlike the module's own default mode).

Run:
    .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_poc_motion_design.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "panel_animator"))
import registration_snap  # noqa: E402
import ink_up_build  # noqa: E402
import palette_pivot  # noqa: E402
import crop_mark_approval  # noqa: E402
import letterpress_beat  # noqa: E402
import parallax_25d  # noqa: E402

HERE = Path(__file__).resolve().parent
STILLS = HERE / "stills"
OUT = HERE / "_poc_motion_design"
OUT.mkdir(exist_ok=True)
WINDOWS = {r["name"]: r for r in json.loads((HERE / "_spread_windows.json").read_text(encoding="utf-8"))}
ALIGNMENT = json.loads((HERE / "_alignment.json").read_text(encoding="utf-8"))


def dur_of(name: str) -> float:
    return WINDOWS[name]["dur"]


def start_of(name: str) -> float:
    return WINDOWS[name]["start"]


if __name__ == "__main__":
    name = "s24_lots_card"
    registration_snap.render(STILLS / f"{name}.png", OUT / f"{name}_registration_snap.mp4", dur_of(name))

    name = "s56_the_answer"
    regions = [{"bbox": [38, 8, 24, 30]}, {"bbox": [8, 60, 20, 28]}, {"bbox": [72, 60, 20, 28]}]
    ink_up_build.render(STILLS / f"{name}.png", regions, OUT / f"{name}_ink_up_build.mp4", dur_of(name))

    name = "s51_jesus_pivot"
    parallax_25d.render(STILLS / f"{name}.png", OUT / f"{name}_locked_parallax.mp4",
                         dur_of(name), fg_amp=6.0, bg_amp=0.0)

    name = "s68_east_west_horizon"
    palette_pivot.render(STILLS / f"{name}.png", OUT / f"{name}_palette_pivot.mp4", dur_of(name))

    name = "s20_blood_atonement_card"
    crop_mark_approval.render(STILLS / f"{name}.png", OUT / f"{name}_crop_mark.mp4", dur_of(name))

    name = "s39_honesty_close"
    beats = letterpress_beat.beats_in_window(
        ALIGNMENT, start_of(name), start_of(name) + dur_of(name), letterpress_beat.MIN_SPACING)
    letterpress_beat.render(STILLS / f"{name}.png", OUT / f"{name}_letterpress_beat.mp4", dur_of(name), beats)
