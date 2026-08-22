"""Character-focused woodcut TEST #3 — NOT part of the locked pilot.

Both prior style tests (render_test.py, render_hybrid_panels.py) show Jacob
from behind, small or mid-distance — neither actually shows his FACE
rendered in the woodcut style. This test is a medium character study,
facing toward camera, so the woodcut/cinematic treatment can be judged
against his actual established likeness (face, beard, hair, dress), not
just his silhouette. Chains BOTH jacob_ref.png (full figure/build) AND
jacob_face_ref.png (the close crop that pins the sparse-beard, dark-curling-
hair specifics) — the two prior tests only used the full-figure ref.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_pilot_01_jacobs_ladder\\_style_test_durer_woodcut\\render_char_test.py
"""
from __future__ import annotations

import re
import subprocess
import urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
HERE = Path(__file__).resolve().parent
REFS = HERE.parent / "refs"
OUT = HERE / "jacob_char_woodcut_test.png"

PROMPT = (
    "Jacob (match his reference images — a young man with a smooth, unweathered face, quick "
    "watchful dark eyes, dark curling hair falling to his jaw, the first sparse shadow of a "
    "young beard, never a full or thick beard, a plain olive-green robe over a cream tunic, an "
    "ochre-brown mantle across one shoulder), a medium three-quarter portrait, facing partly "
    "toward camera, his expression watchful and weary, holding a plain straight wooden staff, "
    "standing on rugged rocky wilderness terrain at low golden-hour light. Deep teal shadows, "
    "dramatic volumetric light rays cutting through haze behind him, photographic tonality. "
    "16th-century Albrecht Durer woodcut linework blended with contemporary cinematic "
    "photography — dense parallel hatching following the forms of his face and robe, hard "
    "black contours, ink-on-block texture. Vertical 9:16 aspect ratio, stationary camera, wide "
    "static shot, ultra-crisp. Avoid: modern clothing, busy foreground, bright neon colors, any "
    "text or watermarks, deformed anatomy, blurry rendering, smooth photorealism without "
    "linework."
)

REF_IMAGES = [REFS / "jacob_ref.png", REFS / "jacob_face_ref.png", REFS / "staff_ref.png"]

_IMG_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)


def main() -> None:
    cmd = [HF_CLI, "generate", "create", "nano_banana_pro", "--prompt", PROMPT]
    for ref in REF_IMAGES:
        cmd += ["--image", str(ref)]
    cmd += ["--aspect_ratio", "9:16", "--resolution", "2k", "--wait"]
    print("[nano_banana_pro] rendering character-focused woodcut test ...")
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
