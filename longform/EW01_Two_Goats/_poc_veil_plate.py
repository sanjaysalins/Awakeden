"""POC (2026-07-23): kinetic-ink-lettering-over-living-plate test, step 1 of 3.

Renders ONE painted-comic PLATE for scene 20 ("He sat down — the veil rent from
the top", Matthew 27:51) with a QUIET NEGATIVE-SPACE ZONE deliberately reserved
in-scene (per the VOX §10 habit + painted-comic SPEC §6) so a Remotion kinetic
ink-scripture layer can be composited on top later. NO baked text in the art.

Chains christ_pc_ref (scene 20 is face_nbp=True) for Christ consistency.
~$0.30 (2 cr, nano_banana_pro). Records to the spend ledger.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_poc_veil_plate.py
"""
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
TESTDIR = Path(__file__).resolve().parent / "v1" / "visual_16x9_inked" / "_painted_comic_test"
OUT = Path(__file__).resolve().parent / "v1" / "visual_16x9_inked" / "_poc_kinetic_type"
OUT.mkdir(parents=True, exist_ok=True)
CHRIST_REF = TESTDIR / "christ_pc_ref.png"

# Frozen painted-comic STYLE BLOCK (dark chiaroscuro variant, from PAINTED_COMIC_SPEC.md §2)
STYLE = ("Bold inked biblical graphic-novel illustration: heavy confident black ink linework "
         "and dry-brush texture over rich muted earth-tone painting, dramatic single strong key "
         "light with deep chiaroscuro shadow, a premium comic-cover finish. Non-photoreal, not "
         "smooth airbrushed, not a 3D render, no halftone dots, no vintage newsprint.")
AVOID = ("AVOID: no text, letters, numbers, digits, panel numbers, chapter numbers or captions "
         "anywhere in the frame, including carved into rock, wood, corners or borders; no speech "
         "balloons; no card, plate, tab, ribbon, banner, title-box, blank rectangle, empty caption "
         "box, page margin, gutter line or panel border of any kind (all text and framing are drawn "
         "separately by Remotion); no logo or watermark; no photoreal live-action; no smooth 3D "
         "render; no halftone dots; no modern machinery, clothing or tools; no gore.")
MATCH = "Match the inked chiaroscuro rendering of the reference image(s)."

# Reserve a quiet dark zone as IN-SCENE negative space (never "an open box") for the Remotion type
SHOT = ("the risen High-Priest Christ seated at rest in glory at the right hand, calm and reverent, "
        "a warm golden key light falling on him; beside and behind him the great temple veil rent in "
        "two from the top downward by no human hand, a clean vertical shaft of pale light breaking "
        "through the torn gap; ancient Near-Eastern temple interior held in deep chiaroscuro shadow; "
        "let quiet deep shadow fill the lower-left of the frame with nothing painted there, and keep "
        "the upper-right glow simple and uncluttered")

NAME = "pc_20_veil_plate"


def main():
    prompt = f"{STYLE} Compose this frame: {SHOT}. {AVOID} {MATCH}"
    cmd = [HF, "generate", "create", "nano_banana_pro", "--prompt", prompt,
           "--aspect_ratio", "16:9", "--resolution", "2k", "--wait",
           "--image", str(CHRIST_REF)]
    print(f"[POC plate] {NAME} — rendering (nano_banana_pro 16:9 2k, christ ref chained) ...", flush=True)
    t = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (r.stdout or "") + "\n" + (r.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"  NO URL / FAILED:\n{blob.strip()[-400:]}")
        sys.exit(1)
    out = OUT / f"{NAME}.png"
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    if out.exists() and out.stat().st_size > 1000:
        cost.record_hf("EW01_Two_Goats", "long", "stills", "nano_banana_pro",
                       note=f"[POC kinetic-type] {NAME}")
        print(f"  ok ({time.time()-t:.0f}s) -> {out}")
    else:
        print("  FAILED (no file / empty)")
        sys.exit(1)


if __name__ == "__main__":
    main()
