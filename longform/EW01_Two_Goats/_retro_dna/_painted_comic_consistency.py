"""Consistency test (2026-07-24): direct response to the independent review's
core complaint -- every passion/doctrine-gate claim in PAINTED_COMIC_SPEC.md
§10 rested on n=1 renders with no reroll accounting, despite the SAME section
documenting real reroll variance. This round reroll-tests the doctrine-gate
fix (robed crucifixion / deposition / via dolorosa), rerolls a full-colour
environmental scene for architecture/colour consistency, and adds 3 NEW
scenes (9, 22, 6) not yet tested at all, to widen coverage beyond the 2-3
recurring subjects the panel flagged as too narrow. 12 renders, ~$3.60.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_retro_dna/_painted_comic_consistency.py
"""
import json, re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
HERE = Path(__file__).resolve().parent
OUT = HERE / "_consistency"
OUT.mkdir(exist_ok=True)
PCT = HERE.parent / "v1" / "visual_16x9_inked" / "_painted_comic_test"
CHRIST_REF = PCT / "christ_pc_ref.png"
AARON_REF = PCT / "aaron_pc_ref.png"

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

plan = json.loads((HERE.parent / "v1" / "visual_16x9_inked" / "scene_plan.json").read_text(encoding="utf-8"))
scenes = {s["id"]: s for s in plan["scenes"]}

S_CROSS_ROBED = ("Jesus Christ crucified on a wooden cross, wearing a simple long pale robe covering "
                  "his body, a THIN, GAUNT, emaciated frame visible beneath the robe's folds, NO "
                  "heroic muscle, NO athletic build - as Isaiah wrote, no beauty that we should "
                  "desire him; head bowed low in sorrow; only faint matted blood at the hands and "
                  "brow, NOT bright droplets; a dark brooding storm sky, deeply reverent and sorrowful")
S_DEPOSITION = ("The body of Jesus Christ being gently lowered from the cross at dusk, wrapped partly "
                "in a pale linen cloth, a THIN, GAUNT, marred frame, NO heroic muscle; his mother Mary "
                "and two grieving disciples receiving him with great tenderness, faces full of sorrow; "
                "muted twilight colours, deeply reverent and solemn, no gore, restrained")
S_VIA_DOLOROSA = ("Jesus Christ, THIN, GAUNT and exhausted, struggling under the weight of a heavy "
                   "wooden cross beam on a narrow stone street, stumbling forward, a simple robe "
                   "covering his body, a crowd watching in mixed sorrow and mockery kept soft and in "
                   "shadow, a Roman soldier walking beside him; dusty, harsh midday light, deeply "
                   "sorrowful, no gore, restrained")

# (name, shot, refs) -- doctrine-gate rerolls
DOCTRINE_JOBS = [
    ("cross_r2", S_CROSS_ROBED, [CHRIST_REF]),
    ("cross_r3", S_CROSS_ROBED, [CHRIST_REF]),
    ("cross_r4", S_CROSS_ROBED, [CHRIST_REF]),
    ("deposition_r2", S_DEPOSITION, [CHRIST_REF]),
    ("deposition_r3", S_DEPOSITION, [CHRIST_REF]),
    ("viadolorosa_r2", S_VIA_DOLOROSA, [CHRIST_REF]),
    ("viadolorosa_r3", S_VIA_DOLOROSA, [CHRIST_REF]),
]

# environmental full-colour reroll (scene 11, already validated once as 10_scene11_fullcolour.png)
ENV_JOBS = [
    ("scene11_r2", scenes[11]["subject_block"], [AARON_REF]),
    ("scene11_r3", scenes[11]["subject_block"], [AARON_REF]),
]

# 3 NEW scenes, never tested in painted-comic before
NEW_JOBS = [
    ("scene9_new", scenes[9]["subject_block"], [AARON_REF]),
    ("scene22_new", scenes[22]["subject_block"], [CHRIST_REF]),
    ("scene6_new", scenes[6]["subject_block"], [AARON_REF]),
]

ALL_JOBS = DOCTRINE_JOBS + ENV_JOBS + NEW_JOBS


def run(prompt, out, refs):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt, "--aspect_ratio", "16:9",
           "--resolution", "2k", "--wait"]
    for r in refs:
        cmd += ["--image", str(r)]
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
    for name, shot, refs in ALL_JOBS:
        out = OUT / f"{name}.png"
        if out.exists() and out.stat().st_size > 1000:
            print(f"[skip] {out.name}"); continue
        prompt = f"{STYLE} Compose this frame: {shot}. {AVOID_FULL_COLOR} {MATCH}"
        print(f"[img ] {name} ...", flush=True); t = time.time()
        if run(prompt, out, refs):
            cost.record_hf("EW01_Two_Goats", "long", "stills", MODEL, note=f"[pc-consistency] {name}")
            print(f"   ok ({time.time()-t:.0f}s)")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
