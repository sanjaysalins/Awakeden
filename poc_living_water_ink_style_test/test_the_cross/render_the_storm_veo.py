"""F06 "THE STORM" -- veo3_1_lite variant, same still + same animation prompt as
render_the_storm_f06.py's Kling render, for a direct bake-off. See that file's
docstring for the design rationale.

Run (after the Kling still already exists):
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\test_the_cross\\render_the_storm_veo.py
"""
from __future__ import annotations

import re
import subprocess
import urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
HERE = Path(__file__).resolve().parent
STILL_PNG = HERE / "the_storm_f06_9x16.png"
CLIP_MP4 = HERE / "the_storm_f06_9x16_veo.mp4"
_VID_URL_RE = re.compile(r"https://\S+?\.(?:mp4|mov|webm)", re.IGNORECASE)

ANIMATION_PROMPT = (
    "Stationary camera, locked wide shot of the 2D storyboard layout, frame borders and all "
    "baked text stay static. Animate isolated motion inside each panel: panel 1 light on the "
    "empty pillow deepens slightly; panel 2 storm light on Peter's face dims slowly; panel 3 "
    "the sea sketch's wash deepens slightly. Large bottom panel: Jesus stands firm at the "
    "stern, raised open hand held steady, robes and hair streaming in the wind; his lips stay "
    "closed and completely still — he is not speaking and his mouth does not move at all; "
    "Peter keeps gripping the gunwale, his mantle stirring; John stays braced against the "
    "mast, holding still; the green-black waves rise and fall within their own band around "
    "the hull, the boat rocking gently in place, keeping its steady lean; the golden halo "
    "line swirls rotate slowly around Jesus's head; the soft blue threads above his raised "
    "hand drift gently within their own small area; the furled sail stays lashed along the yard."
)


def render_animation() -> None:
    if CLIP_MP4.exists():
        print(f"  [skip] {CLIP_MP4.name} already exists")
        return
    if not STILL_PNG.exists():
        print("  FAILED: still not rendered yet.")
        return
    cmd = [HF_CLI, "generate", "create", "veo3_1_lite", "--prompt", ANIMATION_PROMPT,
           "--start-image", str(STILL_PNG), "--aspect_ratio", "9:16", "--duration", "4", "--wait"]
    print("  [veo3_1_lite] rendering animation...")
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=900)
    if proc.returncode != 0:
        print(f"        FAILED: hf CLI exit {proc.returncode}: {(proc.stderr or proc.stdout).strip()[-800:]}")
        return
    match = _VID_URL_RE.search(proc.stdout)
    if not match:
        print(f"        FAILED: no video URL in stdout: {proc.stdout.strip()[-800:]}")
        return
    req = urllib.request.Request(match.group(0), headers={"User-Agent": "JesusInTheBible-POC/1.0"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        CLIP_MP4.write_bytes(resp.read())
    print(f"        -> {CLIP_MP4.name} ({CLIP_MP4.stat().st_size:,} bytes)")


if __name__ == "__main__":
    render_animation()
