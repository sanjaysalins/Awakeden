"""Animate the front/back cover stills. veo3_1_lite (atmospheric hold, no
completing gesture -- this project's established "veo lane" for exactly
this kind of shot), 4s each, matching F01/F08's own veo duration.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_pilot_01_jacobs_ladder\\_style_test_durer_woodcut\\animate_covers.py front
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_pilot_01_jacobs_ladder\\_style_test_durer_woodcut\\animate_covers.py back
"""
from __future__ import annotations

import re
import subprocess
import sys
import urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
HERE = Path(__file__).resolve().parent

FRONT_ANIM = (
    "Stationary camera, locked wide static shot, no pan, no zoom. The baked title lettering "
    "at the top of the frame — both the large title and the smaller line beneath it — stays "
    "pixel-for-pixel identical for every single frame of the clip: same exact opacity from "
    "first frame to last, never fading in or out, never dissolving, never duplicating or "
    "doubling, never drifting position. Jacob "
    "continues his slow, weary walk forward, one heavy step after another at the same tired, "
    "even pace for the whole clip, his head staying low, his staff swinging gently with his "
    "stride; his mantle stirs faintly in the evening wind; the dusk light stays exactly as "
    "warm and dim as it already is, unchanged for the whole clip; the distant tents stay "
    "exactly as drawn; no new figure, mark, or text appears anywhere on the frame at any point."
)

BACK_ANIM = (
    "Stationary camera, locked wide static shot, no pan, no zoom. The baked closing lettering "
    "at the bottom of the frame stays perfectly static and unchanged for the whole clip. Jacob "
    "stands still, facing the dawn horizon, only his mantle and the hem of his robe stirring "
    "gently in the morning wind; his staff stays upright and still in his hand; the dawn light "
    "stays exactly as it already is, unchanged for the whole clip; no new figure, mark, or "
    "text appears anywhere on the frame at any point."
)

_VID_URL_RE = re.compile(r"https://\S+?\.(?:mp4|mov|webm)", re.IGNORECASE)


def animate(png: Path, mp4: Path, prompt: str) -> bool:
    cmd = [HF_CLI, "generate", "create", "veo3_1_lite", "--prompt", prompt,
           "--start-image", str(png), "--aspect_ratio", "9:16", "--duration", "4", "--wait"]
    print(f"[veo3_1_lite] rendering {mp4.name} ...")
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=900)
    if proc.returncode != 0:
        print(f"  FAILED: hf CLI exit {proc.returncode}: "
              f"{(proc.stderr or proc.stdout).strip()[-800:]}")
        return False
    match = _VID_URL_RE.search(proc.stdout)
    if not match:
        print(f"  FAILED: no output URL in stdout: {proc.stdout.strip()[-800:]}")
        return False
    req = urllib.request.Request(match.group(0), headers={"User-Agent": "JesusInTheBible-POC/1.0"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        mp4.write_bytes(resp.read())
    print(f"  -> {mp4.name} ({mp4.stat().st_size:,} bytes)")
    return True


def main() -> None:
    which = sys.argv[1:] or ["front", "back"]
    if "front" in which:
        animate(HERE / "front_cover_woodcut.png", HERE / "front_cover_woodcut.mp4", FRONT_ANIM)
    if "back" in which:
        animate(HERE / "back_cover_woodcut.png", HERE / "back_cover_woodcut.mp4", BACK_ANIM)


if __name__ == "__main__":
    main()
