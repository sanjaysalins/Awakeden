"""One-off visual-style TEST — NOT part of the locked Jacob's Ladder pilot.

The user found a Durer-woodcut-blended-with-cinematic-photography prompt
while testing elsewhere and asked to see how it would look/feel applied to
one of the Jacob's Ladder stills. F08 ("The True Ladder" landing page —
Jacob standing, seen from behind, staff upright, facing the dawn horizon,
wilderness) is by far the closest content match to the found prompt's own
"lone figure from behind, staff, standing in contemplation" framing, so
that's the scene substituted in below.

This is a completely different visual language from the locked pilot's
"Swirls of Life" hand-drawn ink-and-watercolor storyboard-page style (no
panels, no baked text, no motif — a single full-bleed image). Chained
Jacob/staff/place refs from the LOCKED pilot for character continuity, but
note in reporting whether they held across such a big style jump — that's
a real, useful part of the experiment, not just a footnote.

No negative_prompt param exists on nano_banana_pro (checked via
`hf model get nano_banana_pro`), so the found prompt's "Negative Prompt:"
block is folded into the main prompt as plain-language exclusions, dropping
the camera-motion-only items (irrelevant to a still: panning, zooming,
cinematic motion).

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_pilot_01_jacobs_ladder\\_style_test_durer_woodcut\\render_test.py
"""
from __future__ import annotations

import re
import subprocess
import urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
HERE = Path(__file__).resolve().parent
REFS = HERE.parent / "refs"
OUT = HERE / "f08_durer_woodcut_test.png"

PROMPT = (
    "Jacob, a lone ancient figure seen from behind, small in scale against the landscape, his "
    "coarse woven robe and mantle stirred by the wind, holding a wooden staff upright, "
    "standing still in contemplation, facing the dawn horizon. Vast wind-scoured wilderness, "
    "rugged rocky terrain, sweeping desert valleys, carved structural cloud forms in an open "
    "sweeping sky. Low golden-hour sun, cinematic atmospheric haze, deep teal shadows, "
    "dramatic volumetric light rays piercing the clouds, photographic tonality. 16th-century "
    "Albrecht Durer woodcut linework blended with contemporary cinematic landscape "
    "photography, dense parallel hatching, hard black contours, ink-on-block texture, vertical "
    "9:16 aspect ratio, figure isolated in the lower third, stationary camera, wide static "
    "shot, ultra-crisp. Avoid: modern clothing, busy foreground, bright neon colors, any text "
    "or watermarks, deformed anatomy, blurry rendering, smooth photorealism without linework."
)

REF_IMAGES = [REFS / "jacob_ref.png", REFS / "staff_ref.png", REFS / "bethel_ref.png"]

_IMG_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)


def main() -> None:
    cmd = [HF_CLI, "generate", "create", "nano_banana_pro", "--prompt", PROMPT]
    for ref in REF_IMAGES:
        cmd += ["--image", str(ref)]
    cmd += ["--aspect_ratio", "9:16", "--resolution", "2k", "--wait"]
    print("[nano_banana_pro] rendering style test ...")
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
