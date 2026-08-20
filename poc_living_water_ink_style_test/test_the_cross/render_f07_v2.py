"""F07 v2 -- still + animation designed together (Fable, 2026-08-20), per
NORTH_STAR_ANIMATION_PROMPT.md's WORKED EXAMPLE. Redesigns the retired shot 7
composition: lateral profile run (matches the drawn vector to the intended
motion), well+pot small and behind her, ground explicitly dry, ink motif
moved to a sky band instead of ground ribbons.

Run: .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\test_the_cross\\render_f07_v2.py
"""
from __future__ import annotations

import re
import subprocess
import urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
HERE = Path(__file__).resolve().parent
REFS_DIR = HERE.parents[1] / ".claude" / "skills" / "swirls-of-life" / "references"
WOMAN_REF = str(REFS_DIR / "john4_woman_ref.png")
STILL_PNG = HERE / "f07_v2_9x16.png"
CLIP_MP4 = HERE / "f07_v2_9x16.mp4"
_IMG_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
_VID_URL_RE = re.compile(r"https://\S+?\.(?:mp4|mov|webm)", re.IGNORECASE)

STILL_PROMPT = (
    'One single storyboard page of hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper, laid out like a real found piece of production art. Top-left title, handwrite: "SEQ: THE WELL". Top-right frame number, handwrite: "F07". Across the top, a row of exactly three small storyboard panels, each with a circled number 1, 2, 3 as its ONLY label: panel 1 (handwrite: "pot left behind") a small sketch of the round clay waterpot sitting abandoned on the stone rim of the well, panel 2 (handwrite: "urgent joy") a study of the woman\'s face mid-run, alight with urgent joy, panel 3 (handwrite: "town ahead") a small sketch of the town\'s flat rooftops and gate on the road ahead. Below them, ONE large full-scene illustration filling the lower half of the page — a WIDE PROFILE shot: the Samaritan woman in full figure, seen from the side in profile, running from the left of the frame toward the right in mid-stride, her garments and head covering streaming out behind her; the dry dirt path she runs on leads from the old stone well — small and fully inside the frame at the lower left, behind her, the abandoned clay waterpot fully visible sitting alone on its stone rim — rising gently across open country to the distant town, its flat rooftops and gate small and fully inside the frame on the higher right horizon ahead of her; long afternoon light; the ground, the path, and all the country below the horizon are dry ochre earth and grass, with no stream, no water, and no blue anywhere on the ground. The Samaritan woman (match the attached reference): an ordinary first-century working woman with a strong distinctive face and expressive eyes, dark hair partly under a practical head covering, layered garments in burnt umber wash with muted olive-green and clay-red accents, drawn in dense cross-hatching and short dry-brush strokes, her cross-hatching drawn visibly looser now, almost flying. Stage 3 beginning dosage: the blue ink motif begins to diffuse — one loose open band of blue ink threads with traces of muted gold drifting high in the sky, stretching from above the well at the left across the upper air toward the town at the right, tied to no single figure and touching nothing on the ground, no longer one single thread but not yet filling the scene, behaving like wet ink bled into the paper\'s sky wash. Small handwritten production notes integrated naturally on the page: a caption beneath the main scene, handwrite: "Come, see a man", and a corner note, handwrite: "NOTE: pot left behind". No other text, letters, numbers, or words appear anywhere on the page beyond the exact handwrite strings given above — no invented captions, signs, inscriptions, or titulus. Palette: black ink, ochre, muted brown, olive green, clay-red, touches of soft gold wash on aged cream paper with visible grain. Not photorealistic, not anime, not Disney, no polished graphic design, no clean comic-book inking, no Renaissance religious staging, no glowing spiritual VFX — every blue or gold element behaves like literal wet ink bleeding into paper, never a magic-particle glow.'
)

ANIMATION_PROMPT = (
    "Stationary camera, locked wide shot of the 2D storyboard layout, frame borders and all "
    "baked text stay static. Animate isolated motion inside each panel: panel 1 the warm "
    "afternoon light on the clay pot deepens very slightly, nothing else changes; panel 2 a "
    "few loose strands of the woman's hair stir in the wind of her run; panel 3 a thin banner "
    "of dust drifts across the road before the town gate. Large bottom panel: the woman keeps "
    "running from left to right along the dirt path toward the distant town gate, one "
    "continuous steady stride the whole clip, her robes and head covering streaming behind "
    "her; the blue-and-gold ink threads high in the sky drift smoothly within their own fixed "
    "band across the sky; the waterpot sits still on the well's edge."
)


def render_still() -> bool:
    if STILL_PNG.exists():
        print(f"  [skip] {STILL_PNG.name} already exists")
        return True
    cmd = [HF_CLI, "generate", "create", "nano_banana_pro", "--prompt", STILL_PROMPT,
           "--image", WOMAN_REF, "--aspect_ratio", "9:16", "--resolution", "2k", "--wait"]
    print("  [nano_banana_pro] rendering still...")
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=600)
    if proc.returncode != 0:
        print(f"        FAILED: hf CLI exit {proc.returncode}: {(proc.stderr or proc.stdout).strip()[-800:]}")
        return False
    match = _IMG_URL_RE.search(proc.stdout)
    if not match:
        print(f"        FAILED: no image URL in stdout: {proc.stdout.strip()[-800:]}")
        return False
    req = urllib.request.Request(match.group(0), headers={"User-Agent": "JesusInTheBible-POC/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        STILL_PNG.write_bytes(resp.read())
    print(f"        -> {STILL_PNG.name} ({STILL_PNG.stat().st_size:,} bytes)")
    return True


def render_animation() -> None:
    if CLIP_MP4.exists():
        print(f"  [skip] {CLIP_MP4.name} already exists")
        return
    cmd = [HF_CLI, "generate", "create", "kling3_0", "--prompt", ANIMATION_PROMPT,
           "--start-image", str(STILL_PNG), "--aspect_ratio", "9:16",
           "--mode", "pro", "--duration", "5", "--sound", "off", "--wait"]
    print("  [kling3_0] rendering animation...")
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
    if render_still():
        render_animation()
