"""Brightness-tunability test (2026-07-22): prove painted-comic can go BRIGHT/warm,
not only dark chiaroscuro. Same ink + painted-colour + comic-cover finish, but the
light dialed to warm/radiant/airy. Re-renders the Christ hero (25, front-lit — also
fixes the too-dark backlit result) + a bright hope scene (23, the opened veil
flooding light). Reuses the christ_pc_ref from _painted_comic_test.py. ~$0.60.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_painted_comic_bright.py
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
OUT = Path(__file__).resolve().parent / "v1" / "visual_16x9_inked" / "_painted_comic_test"
CHRIST_REF = OUT / "christ_pc_ref.png"

# BRIGHT variant of the frozen STYLE BLOCK — only the LIGHT changes vs the dark version
STYLE_BRIGHT = ("Bold inked biblical graphic-novel illustration: heavy confident black ink linework "
                "and dry-brush texture over rich luminous earth-tone painting, a warm radiant bright "
                "key light with soft lifted shadows and a bright airy overall exposure, glowing golden "
                "highlights, a premium comic-cover finish. Non-photoreal, not smooth airbrushed, not a "
                "3D render, no halftone dots, no vintage newsprint.")
AVOID = ("AVOID: no text, letters, numbers, digits, panel numbers, chapter numbers or captions "
         "anywhere in the frame, including carved into rock, wood, corners or borders; no speech "
         "balloons; no card, plate, tab, ribbon, banner, title-box, blank rectangle, empty caption "
         "box, page margin, gutter line or panel border of any kind (all text and framing are drawn "
         "separately by Remotion); no logo or watermark; no photoreal live-action; no smooth 3D "
         "render; no halftone dots; no modern machinery, clothing or tools; no gore.")
MATCH = "Match the inked rendering of the reference image(s), but keep the bright warm luminous exposure."

S25 = ("HERO close: the risen Christ standing in a full open doorway, warm golden light falling ON his "
       "gentle welcoming FACE and on his open hand extended toward the viewer in welcome, front-lit with "
       "his face clearly and warmly lit (NOT a dark backlit silhouette), a great torn temple veil framing "
       "him, the way wide open behind him; reverent, radiant, bright and warm; ancient Near-Eastern setting; "
       "keep the lower third quiet")
S23 = ("the great torn temple veil now fully open, brilliant warm light flooding out into the once-dark holy "
       "place, a clear inviting bright path through the opening, no guard and no priest barring the way; "
       "radiant, bright, hopeful, warm golden light everywhere; ancient Near-Eastern mud-brick and reed "
       "setting; keep the lower third quiet")

JOBS = [
    ("pc_25_christ_bright", S25, [CHRIST_REF]),
    ("pc_23_open_bright",   S23, []),
]


def gen(name, shot, refs):
    prompt = f"{STYLE_BRIGHT} Compose this frame: {shot}. {AVOID}"
    if refs:
        prompt += " " + MATCH
    cmd = [HF, "generate", "create", "nano_banana_pro", "--prompt", prompt,
           "--aspect_ratio", "16:9", "--resolution", "2k", "--wait"]
    for r in refs:
        cmd += ["--image", str(r)]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (r.stdout or "") + "\n" + (r.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"       no url: {blob.strip()[-250:]}")
        return None
    out = OUT / f"{name}.png"
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out if out.exists() and out.stat().st_size > 1000 else None


def main():
    print(f"[painted-comic BRIGHT] hf nano_banana_pro @ 16:9 2k")
    for name, shot, refs in JOBS:
        print(f"[img ] {name} ...", flush=True)
        t = time.time()
        out = gen(name, shot, refs)
        if out:
            cost.record_hf("EW01_Two_Goats", "long", "stills", "nano_banana_pro",
                           note=f"[painted-comic-bright] {name}")
            print(f"       ok ({time.time()-t:.0f}s) -> {out.name}")
        else:
            print("       FAILED")
    print(f"\n[done] -> {OUT}")


if __name__ == "__main__":
    main()
