"""Front + back cover — full woodcut, no panels, for The Ashes That Made
Clean. Same technique validated on Jacob's Ladder
(swirls_pilot_01_jacobs_ladder/_style_test_durer_woodcut/render_covers.py):
these carry the OPENING and LANDING beats of the narration directly (per
the "book" plan's final structure — the front/back cover REPLACE what
would otherwise be separate interior pages for those two beats, not
duplicate them).

Front cover: the instant of contact (Para1, "by nightfall, the law calls
him unclean") — a hand near a fallen body, dry and grey rather than
Jacob's Ladder's warm dusk, matching this episode's own ash/grey palette.
Title "THE ASHES THAT MADE CLEAN" (the episode's own official title) /
"NUMBERS 19".

Back cover: Christ's hand touching the unclean (Para6, "He touched what
makes us unclean, and did not become unclean doing it") — a deliberate
visual rhyme with the front cover's own "touching" gesture, but this touch
does NOT mark him. Swirl (not stain) on his hand. Baked text carries the
CTA, matching Jacob's Ladder's back-cover pattern: "READY TO BE MADE
CLEAN?" / "HEBREWS 9:14".

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode_02_ashes_that_made_clean\\render_ashes_covers.py front
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode_02_ashes_that_made_clean\\render_ashes_covers.py back
"""
from __future__ import annotations

import re
import subprocess
import sys
import urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
HERE = Path(__file__).resolve().parent
REFS = HERE / "refs"

TITLE_STYLE = (
    "bold engraved wood-block title lettering, carved in the same dense woodcut style as the "
    "rest of the image — thick confident carved strokes, not a modern font, not a decorative "
    "flourish font, no drop shadow, no glow, no banner or box behind it, sitting naturally "
    "within the composition"
)

FRONT_PROMPT = (
    "A man's hand reaching down toward a still, fallen human form half-lost in dry grass at "
    "the edge of a bare field — the body itself left indistinct, unglamorized, no visible "
    "wound or gore, just a still shape and a reaching hand meeting it. Vast, wind-scoured, "
    "overcast wilderness under a flat grey sky, low scrub and stone, no vivid color anywhere. "
    "Cinematic atmospheric haze, deep grey and ash-toned shadow, a single shaft of pale, cold "
    "light breaking through the clouds behind the reaching hand, photographic tonality. "
    "16th-century Albrecht Durer woodcut linework blended with contemporary cinematic "
    "landscape photography, dense parallel hatching, hard black contours, ink-on-block "
    "texture, vertical 9:16 aspect ratio, the hand and the still form isolated in the lower "
    "third, stationary camera, wide static shot, ultra-crisp. "
    f"Near the top of the frame, {TITLE_STYLE}, reading: \"THE ASHES THAT MADE CLEAN\", with "
    "smaller matching lettering beneath it reading: \"NUMBERS 19\". No other text, letters, "
    "numbers, or words appear anywhere on the image beyond these two lines — no watermark, "
    "no invented captions. Avoid: modern clothing, visible wounds, blood, gore, busy "
    "foreground, bright colors, deformed anatomy, blurry rendering, smooth photorealism "
    "without linework."
)

BACK_PROMPT = (
    "A serene, dignified hand — its wrist and sleeve the only part of the figure visible, "
    "unhurried and warm-lit — reaching to rest gently on another hand marked with a faint "
    "grey ash smudge, held open at the edge of the frame; where the two hands meet, the grey "
    "mark begins to lift and lighten, without any wound or graphic detail. Vast wind-scoured "
    "wilderness under an open sky breaking from grey into warm gold, cinematic atmospheric "
    "haze, dramatic volumetric light rays widening behind the two hands, photographic "
    "tonality. A single restrained thread of luminous blue-gold ink winds once around the "
    "serene hand's wrist, behaving like living ink on paper, never a glow or halo, touching "
    "no other part of the frame. 16th-century Albrecht Durer woodcut linework blended with "
    "contemporary cinematic landscape photography, dense parallel hatching, hard black "
    "contours, ink-on-block texture, vertical 9:16 aspect ratio, the two hands isolated in "
    "the lower third, stationary camera, wide static shot, ultra-crisp. "
    f"Near the bottom of the frame, {TITLE_STYLE}, reading: \"READY TO BE MADE CLEAN?\", with "
    "smaller matching lettering beneath it reading: \"HEBREWS 9:14\". No other text, letters, "
    "numbers, or words appear anywhere on the image beyond these two lines — no watermark, "
    "no invented captions. Avoid: modern clothing, visible wounds, blood, gore, busy "
    "foreground, deformed anatomy, blurry rendering, smooth photorealism without linework."
)

REF_IMAGES_FRONT = [REFS / "unclean_man_ref.png"]  # skin tone / build continuity for the hand
REF_IMAGES_BACK = [REFS / "unclean_man_ref.png"]  # only the marked hand needs to match

_IMG_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)


def render(prompt: str, out: Path, refs: list[Path]) -> bool:
    cmd = [HF_CLI, "generate", "create", "nano_banana_pro", "--prompt", prompt]
    for ref in refs:
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


FRONT_ANIM = (
    "Stationary camera, locked wide static shot, no pan, no zoom. The baked title lettering "
    "at the top of the frame — both the large title and the smaller line beneath it — stays "
    "pixel-for-pixel identical for every single frame of the clip: same exact opacity from "
    "first frame to last, never fading in or out, never dissolving, never duplicating or "
    "doubling, never drifting position. The reaching hand and the still form beneath it stay "
    "exactly as drawn, in place, for the whole clip — no new motion in the hand or the body; "
    "the dry grass around them sways very gently in a passing wind; the shaft of pale light "
    "in the sky stays exactly as steady as it already is, unchanged for the whole clip; no "
    "new figure, mark, or text appears anywhere on the frame at any point."
)

_VID_URL_RE = re.compile(r"https://\S+?\.(?:mp4|mov|webm)", re.IGNORECASE)

BACK_ANIM = (
    "Stationary camera, locked wide static shot, no pan, no zoom. The baked closing "
    "lettering at the bottom of the frame — both lines — stays pixel-for-pixel identical for "
    "every single frame of the clip: same exact opacity from first frame to last, never "
    "fading in or out, never dissolving, never duplicating or doubling, never drifting "
    "position. The two hands stay exactly as drawn, in the same position, for the whole "
    "clip — no new motion, no further closing of the gap between them; the single restrained "
    "blue-gold thread on the wrist stays exactly as drawn, in place, for the whole clip, "
    "never spreading, never changing shape; the sleeve stirs very faintly in a passing wind; "
    "the volumetric light rays behind them stay exactly as steady as they already are, "
    "unchanged for the whole clip; no new figure, mark, or text appears anywhere on the "
    "frame at any point."
)


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
        if "--animate" in sys.argv:
            animate(HERE / "front_cover_woodcut.png", HERE / "front_cover_woodcut.mp4", FRONT_ANIM)
        else:
            render(FRONT_PROMPT, HERE / "front_cover_woodcut.png", REF_IMAGES_FRONT)
    if "back" in which:
        if "--animate" in sys.argv:
            animate(HERE / "back_cover_woodcut.png", HERE / "back_cover_woodcut.mp4", BACK_ANIM)
        else:
            render(BACK_PROMPT, HERE / "back_cover_woodcut.png", REF_IMAGES_BACK)


if __name__ == "__main__":
    main()
