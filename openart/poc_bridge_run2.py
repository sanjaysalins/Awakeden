"""openart/poc_bridge_run2.py -- POC round 2: two more real pages through the
openart_bridge.py bridge, this time each WITH a single chained ref image (the
ref-upload half of the bridge was untested in round 1's F01, which has refs=[]).

F02: refs=[R_QUEEN] (queen_ref.png), panel_style woodcut_hybrid, single-line
     caption, 5s pro anim -- another data point on the round-1 caption-fade defect.
F06: refs=[R_JESUS] (jesus_ref.png), 2-line stacked caption (the exact page whose
     caption collapsed to one line in the 2026-08-27 manual bake-off), 9s pro anim
     -- checks whether that known defect reproduces through the real bridge, and
     whether the caption-fade defect also shows up on a longer clip.

Renders to openart/poc_bridge_run/, NOT the production episode folder.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
EPISODE_DIR = REPO / "poc_living_water_ink_style_test" / "swirls_episode_01_queen_who_came_to_test_him"
TEST_THE_CROSS = REPO / "poc_living_water_ink_style_test" / "test_the_cross"

sys.path.insert(0, str(TEST_THE_CROSS))
sys.path.insert(0, str(EPISODE_DIR.parent))
sys.path.insert(0, str(EPISODE_DIR))

from swirls_page import render_still, render_animation  # noqa: E402
from episode import F02, F06  # noqa: E402

OUT_DIR = HERE / "poc_bridge_run"
OUT_DIR.mkdir(exist_ok=True)

for label, spec in (("f02", F02), ("f06", F06)):
    out_png = OUT_DIR / f"{label}_still.png"
    out_mp4 = OUT_DIR / f"{label}_anim.mp4"

    print(f"=== POC round 2: OpenArt bridge, still ({label.upper()}) ===")
    if not render_still(spec, out_png):
        print(f"{label.upper()} STILL FAILED -- stopping.")
        sys.exit(1)

    print(f"=== POC round 2: OpenArt bridge, animation ({label.upper()}) ===")
    if not render_animation(spec, out_png, out_mp4):
        print(f"{label.upper()} ANIMATION FAILED.")
        sys.exit(1)

print("=== POC ROUND 2 DONE ===")
