"""One-off design-machine smoke test -- "The Cross", 1 shot x 2 aspect ratios.
See DESIGN.md for the Step 0 output this prompt came from.

Run: .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\test_the_cross\\render_test.py
"""
from __future__ import annotations

import re
import subprocess
import urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
HERE = Path(__file__).resolve().parent
REFS_DIR = HERE.parents[1] / ".claude" / "skills" / "swirls-of-life" / "references"
JESUS_REF = str(REFS_DIR / "jesus_ref.png")
MODEL = "nano_banana_pro"
_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)

PROMPT = (
    'One single storyboard page of hand-drawn animation development art, delicate ink linework and watercolor on aged cream paper, laid out like a real found piece of production art. Top-left title, handwrite: "SEQ: THE CROSS". Top-right frame number, handwrite: "F01". Across the top, a row of exactly three small labeled storyboard panels numbered 1, 2, 3: panel 1 a small sketch of his mother Mary standing at the foot of the cross, one hand pressed to her mouth, grief held with quiet dignity, panel 2 a small sketch of Roman soldiers below the cross, one crouched casting lots on the ground for his garment, spear and helmet loosely inked, panel 3 a small establishing sketch of Golgotha, the bare skull-shaped hill outside the city wall, three crosses in silhouette against a darkening sky. Below them, ONE large full-scene illustration filling the lower half of the page — a HELD SINGLE, close on Jesus alone: Jesus alone on the cross at Golgotha, his upper body filling the frame, arms outstretched along the crossbeam, head bowed slightly; the sky behind him gone dark though it is midday, the bare hill falling away soft and unfinished at the page edges beneath him; stillness and complete surrender. Jesus (match the attached reference for his face, hair, and build): a first-century Jewish man in his early thirties, weathered calm face, dark textured shoulder-length hair, short natural beard, drawn in broad confident economical ink strokes; here on the cross, stripped for the crucifixion but modestly wrapped in a plain loincloth, a crown of twisted thorns pressed into his brow, faint ink marks of the nails at his hands, a faint incomplete calligraphic halo of muted gold-and-blue curls, never a solid disc. Stage 3 dosage: the blue-and-gold ink motif is fully diffused but subdued — quiet threads of blue with the barest trace of gold woven faintly through the darkened sky and along the base of the cross, not tied to any single figure, behaving like wet ink bled deep into the paper, grave and quiet, never bright, never celebratory. Small handwritten production notes integrated naturally on the page: a caption beneath the main scene, handwrite: "Father, forgive them", and a corner note, handwrite: "NOTE: darkness at noon". Palette: black ink, ochre, muted brown, olive green, clay-red, touches of soft gold wash on aged cream paper with visible grain. Not photorealistic, not anime, not Disney, no polished graphic design, no clean comic-book inking, no Renaissance religious staging, no glowing spiritual VFX — every blue or gold element behaves like literal wet ink bleeding into paper, never a magic-particle glow.'
)


def render_one(ratio: str) -> None:
    out_path = HERE / f"the_cross_{ratio.replace(':', 'x')}.png"
    if out_path.exists():
        print(f"  [skip] {out_path.name} already exists")
        return
    cmd = [HF_CLI, "generate", "create", MODEL, "--prompt", PROMPT,
           "--image", JESUS_REF, "--aspect_ratio", ratio, "--resolution", "2k", "--wait"]
    print(f"  [{MODEL}] {ratio}")
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=600)
    if proc.returncode != 0:
        print(f"        FAILED: hf CLI exit {proc.returncode}: {(proc.stderr or proc.stdout).strip()[-800:]}")
        return
    match = _URL_RE.search(proc.stdout)
    if not match:
        print(f"        FAILED: no image URL in stdout: {proc.stdout.strip()[-800:]}")
        return
    url = match.group(0)
    req = urllib.request.Request(url, headers={"User-Agent": "JesusInTheBible-POC/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        out_path.write_bytes(resp.read())
    print(f"        -> {out_path.name} ({out_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    for ratio in ("9:16", "16:9"):
        render_one(ratio)
