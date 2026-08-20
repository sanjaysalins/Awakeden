"""16:9 check for "The Hem" F04 -- same still + animation prompts as the
validated 9:16 v2 (render_the_hem.py), only --aspect_ratio changed. Checks
whether the composition (Jesus left-third, woman center-right, stain
crossing the border, sky thread) still holds when the frame goes from
vertical to horizontal, and whether the story-motion animation still works.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\test_the_cross\\render_the_hem_16x9.py            # still
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\test_the_cross\\render_the_hem_16x9.py --animate  # animation
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_the_hem import F04_STILL_PROMPT, F04_ANIMATION_PROMPT, JESUS_REF, WOMAN_REF  # noqa: E402

HERE = Path(__file__).resolve().parent
# v1 (the_hem_f04_16x9.png/.mp4) rendered with ONLY jesus_ref chained -- the
# woman had no reference at all (two independent text-only generations),
# which the user correctly spotted as a likeness drift from the 9:16 version.
# v2 chained BOTH jesus_ref AND the_hem_woman_ref -- fixed the likeness drift
# but broke the touch itself (her fingertips no longer reached the hem, a
# MUST-SHOW/referent failure). v2 kept on disk as evidence; v3 is a same-
# prompt, same-refs regen (LAW 4: regen the still, never adapt the clause).
PNG = HERE / "the_hem_f04_16x9_v3.png"
MP4 = HERE / "the_hem_f04_16x9_v3.mp4"


def render_still_169() -> bool:
    if PNG.exists():
        print(f"  [skip] {PNG.name} already exists")
        return True
    if not WOMAN_REF.exists():
        print(f"  FAILED: {WOMAN_REF.name} missing.")
        return False
    from render_the_hem import HF_CLI, _IMG_URL_RE, _run_hf
    cmd = [HF_CLI, "generate", "create", "nano_banana_pro", "--prompt", F04_STILL_PROMPT,
           "--image", JESUS_REF, "--image", str(WOMAN_REF),
           "--aspect_ratio", "16:9", "--resolution", "2k", "--wait"]
    print(f"  [nano_banana_pro] rendering {PNG.name} (refs: jesus + woman)...")
    return _run_hf(cmd, PNG, _IMG_URL_RE, 600)


def render_animation_169() -> None:
    if MP4.exists():
        print(f"  [skip] {MP4.name} already exists")
        return
    if not PNG.exists():
        print("  FAILED: still not rendered yet.")
        return
    import subprocess
    from render_the_hem import HF_CLI, _VID_URL_RE, _run_hf
    cmd = [HF_CLI, "generate", "create", "kling3_0", "--prompt", F04_ANIMATION_PROMPT,
           "--start-image", str(PNG), "--aspect_ratio", "16:9",
           "--mode", "pro", "--duration", "5", "--sound", "off", "--wait"]
    print(f"  [kling3_0 pro] rendering {MP4.name}...")
    _run_hf(cmd, MP4, _VID_URL_RE, 900)


if __name__ == "__main__":
    if "--animate" in sys.argv:
        render_animation_169()
    else:
        render_still_169()
