"""Hard-content re-test v2 (2026-07-24): fix the body-gate miss found in round 1
(bare defined torso on the crucifixion/flogging) by robing Christ -- the same
device the ORIGINAL proven doctrine-gate test used, which sidesteps the
muscle-definition question entirely. Also adds 2 NEW hard scenes not tested
before (deposition, way of the cross) per the user's "test this real hard"
ask. 4 renders, ~$1.20.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_retro_dna/_painted_comic_hard_v2.py
"""
import re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
HERE = Path(__file__).resolve().parent
OUT = HERE / "_round4"
PCT = HERE.parent / "v1" / "visual_16x9_inked" / "_painted_comic_test"
CHRIST_REF = PCT / "christ_pc_ref.png"

STYLE = ("Bold inked biblical graphic-novel illustration: heavy confident black ink linework and "
         "dry-brush texture over rich painting, dramatic single strong key light with deep "
         "chiaroscuro shadow, a premium comic-cover finish. Non-photoreal, not smooth airbrushed, "
         "not a 3D render, no halftone dots, no vintage newsprint.")
AVOID_BASE = ("AVOID: no text, letters, numbers, digits, panel numbers, chapter numbers or captions "
              "anywhere in the frame, including carved into rock, wood, corners or borders; no speech "
              "balloons; no card, plate, tab, ribbon, banner, title-box, blank rectangle, empty caption "
              "box, page margin, gutter line or panel border of any kind (all text and framing are drawn "
              "separately by Remotion); no logo or watermark; no photoreal live-action; no smooth 3D "
              "render; no halftone dots; no modern machinery, clothing or tools; no gore.")
AVOID_FULL_COLOR = AVOID_BASE + (
    " Render in full rich natural colour throughout, painterly and reverent, not flat or garish, not "
    "a comic-book primary-colour look, no Ben-Day dots, no CMYK misregistration.")
MATCH = "Match the inked chiaroscuro rendering of the reference image(s)."

# ROBED this time (the device the original proof used) + explicit thin/gaunt/emaciated body language,
# no bare-chest description at all
S_CROSS_ROBED = ("Jesus Christ crucified on a wooden cross, wearing a simple long pale robe covering "
                  "his body, a THIN, GAUNT, emaciated frame visible beneath the robe's folds, NO "
                  "heroic muscle, NO athletic build - as Isaiah wrote, no beauty that we should "
                  "desire him; head bowed low in sorrow; only faint matted blood at the hands and "
                  "brow, NOT bright droplets; a dark brooding storm sky, deeply reverent and sorrowful")

# flogging: robe pulled to the waist (historically the scourging exposed the back), but a WIDER shot
# (less scrutiny on musculature) + explicit thin/gaunt language, no toned-body description
S_FLOGGING_V2 = ("Jesus Christ bound at a low stone scourging post in a dim Roman judgment courtyard, "
                  "seen in a wider view from a respectful distance, his robe pulled down to the waist, "
                  "a THIN, GAUNT frame, NOT muscular or athletic, head bowed low, back turned mostly "
                  "away from view so no graphic wounds are shown, a Roman soldier standing well back "
                  "with a scourge lowered at his side, the moment held in silence, deeply sorrowful "
                  "and reverent, restrained and not graphic")

S_DEPOSITION = ("The body of Jesus Christ being gently lowered from the cross at dusk, wrapped partly "
                "in a pale linen cloth, a THIN, GAUNT, marred frame, NO heroic muscle; his mother Mary "
                "and two grieving disciples receiving him with great tenderness, faces full of sorrow; "
                "muted twilight colours, deeply reverent and solemn, no gore, restrained")

S_VIA_DOLOROSA = ("Jesus Christ, THIN, GAUNT and exhausted, struggling under the weight of a heavy "
                   "wooden cross beam on a narrow stone street, stumbling forward, a simple robe "
                   "covering his body, a crowd watching in mixed sorrow and mockery kept soft and in "
                   "shadow, a Roman soldier walking beside him; dusty, harsh midday light, deeply "
                   "sorrowful, no gore, restrained")

JOBS = [
    ("15_crucifixion_robed", S_CROSS_ROBED),
    ("16_flogging_v2", S_FLOGGING_V2),
    ("17_deposition", S_DEPOSITION),
    ("18_via_dolorosa", S_VIA_DOLOROSA),
]


def run(prompt, out):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt, "--aspect_ratio", "16:9",
           "--resolution", "2k", "--wait", "--image", str(CHRIST_REF)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    if re.search(r"nsfw", blob, re.IGNORECASE):
        print("   NSFW-REJECTED"); return False
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-300:]}"); return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    for name, shot in JOBS:
        out = OUT / f"{name}.png"
        if out.exists() and out.stat().st_size > 1000:
            print(f"[skip] {out.name}"); continue
        prompt = f"{STYLE} Compose this frame: {shot}. {AVOID_FULL_COLOR} {MATCH}"
        print(f"[img ] {name} ...", flush=True); t = time.time()
        if run(prompt, out):
            cost.record_hf("EW01_Two_Goats", "long", "stills", MODEL, note=f"[pc-hard-v2] {name}")
            print(f"   ok ({time.time()-t:.0f}s)")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
