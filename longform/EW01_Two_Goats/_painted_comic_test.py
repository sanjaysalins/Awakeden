"""HONEST TEST (2026-07-22): does the ArkAIology /painted-comic style hold on OUR
Two Goats content? Uses the skill's frozen STYLE BLOCK + AVOID + ref-chaining,
via hf nano_banana_pro. Bootstraps 2 painted-comic character refs (Aaron, Christ)
from our identity stills, then renders 3 scenes chaining them:
  12 = Aaron face (character-consistency test)   11 = two goats (epic, no ref)
  25 = Christ hero (sacred + Christ ref)
Outputs to _painted_comic_test/ for side-by-side vs our current ink. ~$1.50.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_painted_comic_test.py
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
HERE = Path(__file__).resolve().parent
OUT = HERE / "v1" / "visual_16x9_inked" / "_painted_comic_test"
OUT.mkdir(parents=True, exist_ok=True)
VIS = HERE / "v1" / "visual_16x9_inked"
IMG = ROOT / "image_library" / "stills"

# --- frozen recipe (verbatim from PAINTED_COMIC_SPEC.md) ---
STYLE = ("Bold inked biblical graphic-novel illustration: heavy confident black ink linework and "
         "dry-brush texture over rich muted earth-tone painting, dramatic single strong key light "
         "with deep chiaroscuro shadow, a premium comic-cover finish. Non-photoreal, not smooth "
         "airbrushed, not a 3D render, no halftone dots, no vintage newsprint.")
AVOID = ("AVOID: no text, letters, numbers, digits, panel numbers, chapter numbers or captions "
         "anywhere in the frame, including carved into rock, wood, corners or borders; no speech "
         "balloons; no card, plate, tab, ribbon, banner, title-box, blank rectangle, empty caption "
         "box, page margin, gutter line or panel border of any kind (all text and framing are drawn "
         "separately by Remotion); no logo or watermark; no photoreal live-action; no smooth 3D "
         "render; no halftone dots; no modern machinery, clothing or tools; no gore.")
MATCH = "Match the inked chiaroscuro rendering of the reference image(s)."

R_AARON = "an aged patriarch high priest of Israel, about eighty, weathered sun-darkened Hebrew face, deep-set dark eyes, strong brow, long flowing grey-white beard to mid-chest, swept-back grey hair, calm and solemn, in plain undyed white linen priestly robes with no gold and no jewels; head-and-shoulders portrait, dramatic single key light from the left, deep shadow, brooding dark background"
R_CHRIST = "the risen Lord Jesus Christ, gentle and majestic, warm compassionate face, shoulder-length dark hair and a short beard, in a simple luminous undyed white robe and NOT any high-priestly breastplate or ornate vestments; head-and-shoulders portrait, a warm radiant single key light, deep chiaroscuro shadow, dark background"

S12 = "Aaron the aged high priest in plain white linen standing alone in an emptying ancient Near-Eastern tabernacle court at dusk, turning a question over; his lined weathered face lit by a single low altar flame with deep shadow around him; behind him one altar faintly smoking and one empty road running into the darkening waste; a small distant setting sun low in the sky well away from his face; mud-brick and reed period setting, no other people; keep the lower third quiet dark ground"
S11 = "one dramatic frame holding a riddle: on the left a single goat lying still and at peace on a low stone altar step bathed in the warm red glow of altar fire and rising smoke; on the right a live goat facing an open pale road into a vast wilderness; a dark bronze altar standing between them; a strong single key light and deep chiaroscuro, muted earth tones with the one red fire-glow as the single light event; ancient Near-Eastern mud-brick and reed setting; keep the sky upper-right simple and quiet"
S25 = "HERO splash: the risen Christ standing in a full open doorway of radiant light, a great torn temple veil framing him on either side, one hand extended toward the viewer in welcome, the way wide open behind him; warm and reverent, a strong radiant single key light from the doorway with deep chiaroscuro; ancient Near-Eastern setting; keep the lower third quiet"

# (out, shot, [refs], use_match) — refs generated earlier in the list are reused later
AARON_REF = OUT / "aaron_pc_ref.png"
CHRIST_REF = OUT / "christ_pc_ref.png"
JOBS = [
    ("aaron_pc_ref", R_AARON,  [VIS / "12_why_two_two_things_at_once.png"],       False),  # bootstrap ref
    ("christ_pc_ref", R_CHRIST, [IMG / "christ_risen_face_scars.png"],             False),  # bootstrap ref
    ("pc_12_aaron",  S12,       [AARON_REF],                                       True),
    ("pc_11_goats",  S11,       [],                                                True),
    ("pc_25_christ", S25,       [CHRIST_REF],                                      True),
]


def gen(name, shot, refs, use_match):
    prompt = f"{STYLE} Compose this frame: {shot}. {AVOID}"
    if use_match:
        prompt += " " + MATCH
    cmd = [HF, "generate", "create", "nano_banana_pro", "--prompt", prompt,
           "--aspect_ratio", "16:9", "--resolution", "2k", "--wait"]
    for r in refs:
        cmd += ["--image", str(r)]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (r.stdout or "") + "\n" + (r.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob)
    if not urls:
        urls = re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"       no image url: {blob.strip()[-300:]}")
        return None
    out = OUT / f"{name}.png"
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out if out.exists() and out.stat().st_size > 1000 else None


def main():
    print(f"[painted-comic test] hf nano_banana_pro @ 16:9 2k  ({len(JOBS)} renders)")
    for name, shot, refs, use_match in JOBS:
        missing = [r for r in refs if not Path(r).exists()]
        if missing:
            print(f"[SKIP] {name}: missing ref {missing}")
            continue
        print(f"[img ] {name}  refs={[Path(r).name for r in refs] or 'none'} ...", flush=True)
        t = time.time()
        out = gen(name, shot, refs, use_match)
        if out:
            cost.record_hf("EW01_Two_Goats", "long", "stills", "nano_banana_pro",
                           note=f"[painted-comic-test] {name}")
            print(f"       ok ({time.time()-t:.0f}s) -> {out.name}")
        else:
            print(f"       FAILED ({time.time()-t:.0f}s)")
    print(f"\n[done] -> {OUT}")


if __name__ == "__main__":
    main()
