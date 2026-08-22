"""Front + back cover — full woodcut hero stills WITH baked title/closing
text, for bookending the LOCKED ink-wash interior (unchanged). Same scene
content as f01_hero_open_woodcut.png / f08_durer_woodcut_test.png (dusk-
fleeing / dawn-standing), same refs, now with a title card baked in.

Title text is grounded, not invented: "THE LADDER HE SAW" is drawn from the
narration's own line ("Jacob saw a ladder to heaven in a dream"); the
closing text "HE IS THAT LADDER" is F08's own already-locked caption
verbatim. Subtitles are real scripture references (Genesis 28 / John 1:51 --
the NT link the whole episode is built on).

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_pilot_01_jacobs_ladder\\_style_test_durer_woodcut\\render_covers.py
"""
from __future__ import annotations

import re
import subprocess
import sys
import urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
HERE = Path(__file__).resolve().parent
REFS = HERE.parent / "refs"

TITLE_STYLE = (
    "bold engraved wood-block title lettering, carved in the same dense woodcut style as the "
    "rest of the image — thick confident carved strokes, not a modern font, not a decorative "
    "flourish font, no drop shadow, no glow, no banner or box behind it, sitting naturally "
    "within the composition"
)

FRONT_PROMPT = (
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
    f"Near the top of the frame, {TITLE_STYLE}, reading: \"THE LADDER HE SAW\", with smaller "
    "matching lettering beneath it reading: \"GENESIS 28\". No other text, letters, numbers, "
    "or words appear anywhere on the image beyond these two lines — no watermark, no invented "
    "captions. Avoid: modern clothing, busy foreground, bright neon colors, deformed anatomy, "
    "blurry rendering, smooth photorealism without linework."
)

BACK_PROMPT = (
    "Jacob, a lone ancient figure seen from behind, small in scale against the landscape, his "
    "coarse woven robe and mantle stirred by the wind, holding a wooden staff upright, "
    "standing still in contemplation, facing the dawn horizon. Vast wind-scoured wilderness, "
    "rugged rocky terrain, sweeping desert valleys, carved structural cloud forms in an open "
    "sweeping sky. Low golden-hour sun, cinematic atmospheric haze, deep teal shadows, "
    "dramatic volumetric light rays piercing the clouds, photographic tonality. 16th-century "
    "Albrecht Durer woodcut linework blended with contemporary cinematic landscape "
    "photography, dense parallel hatching, hard black contours, ink-on-block texture, vertical "
    "9:16 aspect ratio, figure isolated in the lower third, stationary camera, wide static "
    "shot, ultra-crisp. "
    f"Near the bottom of the frame, {TITLE_STYLE}, reading: \"HE IS THAT LADDER\", with smaller "
    "matching lettering beneath it reading: \"JOHN 1:51\". No other text, letters, numbers, or "
    "words appear anywhere on the image beyond these two lines — no watermark, no invented "
    "captions. Avoid: modern clothing, busy foreground, bright neon colors, deformed anatomy, "
    "blurry rendering, smooth photorealism without linework."
)

REF_IMAGES = [REFS / "jacob_ref.png", REFS / "staff_ref.png", REFS / "bethel_ref.png"]

_IMG_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)


def render(prompt: str, out: Path) -> bool:
    cmd = [HF_CLI, "generate", "create", "nano_banana_pro", "--prompt", prompt]
    for ref in REF_IMAGES:
        cmd += ["--image", str(ref)]
    cmd += ["--aspect_ratio", "9:16", "--resolution", "2k", "--wait"]
    print(f"[nano_banana_pro] rendering {out.name} ...")
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=600)
    if proc.returncode != 0:
        print(f"  FAILED: hf CLI exit {proc.returncode}: "
              f"{(proc.stderr or proc.stdout).strip()[-800:]}")
        return False
    match = _IMG_URL_RE.search(proc.stdout)
    if not match:
        print(f"  FAILED: no output URL in stdout: {proc.stdout.strip()[-800:]}")
        return False
    req = urllib.request.Request(match.group(0), headers={"User-Agent": "JesusInTheBible-POC/1.0"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        out.write_bytes(resp.read())
    print(f"  -> {out.name} ({out.stat().st_size:,} bytes)")
    return True


def main() -> None:
    which = sys.argv[1:] or ["front", "back"]
    if "front" in which:
        render(FRONT_PROMPT, HERE / "front_cover_woodcut.png")
    if "back" in which:
        render(BACK_PROMPT, HERE / "back_cover_woodcut.png")


if __name__ == "__main__":
    main()
