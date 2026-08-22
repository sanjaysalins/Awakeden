"""Full-woodcut HERO — the book's opening bookend, NOT part of the locked
pilot. F01's real content (dusk, fleeing, bowed, weary) rendered in the
pure full-woodcut-cinematic style — no panels, no baked title/frame-number/
captions, matching render_test.py's / jacob_char_woodcut_test.png's format.

This is the missing half of the bookend pair: the CLOSING hero already
exists as f08_durer_woodcut_test.png (Jacob standing at dawn — that test
was built from the "lone figure... standing in contemplation, facing the
dawn horizon" prompt, which already matches F08's own closing beat). This
script builds the OPENING match: Jacob fleeing at dusk, bowed, worn down —
F01's real content, imported from render_jacobs_ladder.py, not retyped.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_pilot_01_jacobs_ladder\\_style_test_durer_woodcut\\render_hero_open.py
"""
from __future__ import annotations

import re
import subprocess
import urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
HERE = Path(__file__).resolve().parent
REFS = HERE.parent / "refs"
OUT = HERE / "f01_hero_open_woodcut.png"

PROMPT = (
    "Jacob, a lone young man seen from behind, small in scale against the landscape, walking "
    "wearily away into the distance, his body heavy with exhaustion, his head bowed low, his "
    "stride worn down to a trudge, one hand gripping a plain wooden staff, the other holding "
    "his wind-blown mantle closed at his chest. Vast wind-scoured wilderness, rugged rocky hill "
    "country, sweeping stony valleys, carved structural cloud forms in an open sweeping sky. "
    "Low dusk sun already sinking, the sky banded in fading ochre and deep grey-umber, "
    "cinematic atmospheric haze, deep teal shadows gathering, dramatic volumetric light fading "
    "through the clouds, photographic tonality. Far behind him, small and fading into the "
    "haze, the low goat-hair tents of the home he has fled. 16th-century Albrecht Durer "
    "woodcut linework blended with contemporary cinematic landscape photography, dense "
    "parallel hatching, hard black contours, ink-on-block texture, vertical 9:16 aspect ratio, "
    "figure isolated in the lower third, stationary camera, wide static shot, ultra-crisp. "
    "Avoid: modern clothing, busy foreground, bright neon colors, any text or watermarks, "
    "deformed anatomy, blurry rendering, smooth photorealism without linework."
)

REF_IMAGES = [REFS / "jacob_ref.png", REFS / "staff_ref.png", REFS / "bethel_ref.png"]

_IMG_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)


def main() -> None:
    cmd = [HF_CLI, "generate", "create", "nano_banana_pro", "--prompt", PROMPT]
    for ref in REF_IMAGES:
        cmd += ["--image", str(ref)]
    cmd += ["--aspect_ratio", "9:16", "--resolution", "2k", "--wait"]
    print("[nano_banana_pro] rendering opening hero (full woodcut) ...")
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=600)
    if proc.returncode != 0:
        raise SystemExit(f"FAILED: hf CLI exit {proc.returncode}: "
                          f"{(proc.stderr or proc.stdout).strip()[-800:]}")
    match = _IMG_URL_RE.search(proc.stdout)
    if not match:
        raise SystemExit(f"FAILED: no output URL in stdout: {proc.stdout.strip()[-800:]}")
    req = urllib.request.Request(match.group(0), headers={"User-Agent": "JesusInTheBible-POC/1.0"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        OUT.write_bytes(resp.read())
    print(f"-> {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
