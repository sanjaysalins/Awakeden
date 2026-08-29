"""openart/poc_bridge_run.py -- POC: drive swirls_page.py's render_still/render_animation
through the real openart_bridge.py file-bridge for the first time (previously only tested
via a 2-page manual bake-off done before the bridge existed, and one trivial MCP smoke test
that bypassed swirls_page.py entirely).

Reuses episode 1's real F01 PageSpec (queen at the ridge, refs=[]) verbatim -- no ref images
to upload, so this POC tests the still+animation bridge mechanism itself, not the ref-upload
path. Renders to openart/poc_bridge_run/, NOT the production episode folder -- does not touch
or overwrite the already-shipped f01 PNG/MP4.
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
from episode import F01  # noqa: E402

OUT_DIR = HERE / "poc_bridge_run"
OUT_DIR.mkdir(exist_ok=True)

out_png = OUT_DIR / "f01_still.png"
out_mp4 = OUT_DIR / "f01_anim.mp4"

print("=== POC: OpenArt bridge, still (F01) ===")
if not render_still(F01, out_png):
    print("STILL FAILED -- stopping.")
    sys.exit(1)

print("=== POC: OpenArt bridge, animation (F01) ===")
if not render_animation(F01, out_png, out_mp4):
    print("ANIMATION FAILED.")
    sys.exit(1)

print("=== POC DONE ===")
print(f"still: {out_png}")
print(f"anim:  {out_mp4}")
