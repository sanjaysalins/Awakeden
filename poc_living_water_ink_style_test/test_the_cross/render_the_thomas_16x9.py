"""16:9 check for "Doubting Thomas" F01 -- same still + animation prompts as
the 9:16 version, only --aspect_ratio changed. Applying today's ref-chaining
lesson from the start this time: Thomas's ref (cropped from the approved
9:16 render) is chained on this 16:9 render, unlike Hem's first 16:9 attempt
which had none.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\test_the_cross\\render_the_thomas_16x9.py            # still
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\test_the_cross\\render_the_thomas_16x9.py --animate  # animation
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_the_thomas import F01_STILL_PROMPT, F01_ANIMATION_PROMPT, THOMAS_REF  # noqa: E402
from render_the_hem import HF_CLI, _IMG_URL_RE, _VID_URL_RE, _run_hf  # noqa: E402

HERE = Path(__file__).resolve().parent
PNG = HERE / "the_thomas_f01_16x9.png"
MP4 = HERE / "the_thomas_f01_16x9.mp4"


def render_still_169() -> bool:
    if PNG.exists():
        print(f"  [skip] {PNG.name} already exists")
        return True
    if not THOMAS_REF.exists():
        print(f"  FAILED: {THOMAS_REF.name} missing.")
        return False
    cmd = [HF_CLI, "generate", "create", "nano_banana_pro", "--prompt", F01_STILL_PROMPT,
           "--image", str(THOMAS_REF), "--aspect_ratio", "16:9", "--resolution", "2k", "--wait"]
    print(f"  [nano_banana_pro] rendering {PNG.name} (ref: thomas)...")
    return _run_hf(cmd, PNG, _IMG_URL_RE, 600)


def render_animation_169() -> None:
    if MP4.exists():
        print(f"  [skip] {MP4.name} already exists")
        return
    if not PNG.exists():
        print("  FAILED: still not rendered yet.")
        return
    cmd = [HF_CLI, "generate", "create", "kling3_0", "--prompt", F01_ANIMATION_PROMPT,
           "--start-image", str(PNG), "--aspect_ratio", "16:9",
           "--mode", "pro", "--duration", "5", "--sound", "off", "--wait"]
    print(f"  [kling3_0 pro] rendering {MP4.name}...")
    _run_hf(cmd, MP4, _VID_URL_RE, 900)


if __name__ == "__main__":
    if "--animate" in sys.argv:
        render_animation_169()
    else:
        render_still_169()
