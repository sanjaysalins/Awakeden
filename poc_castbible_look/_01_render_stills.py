"""cast-bible LOOK taste piece — step 1: render 6 editorial-sketch stills.
Uses the ArkAIology cast-bible skill EXACTLY as written: NOAH.md canon
description pasted verbatim + the committed anchor chained on every shot that
shows Noah + the flat-sided-ark gotcha line + the NO-TEXT guard (typography is
composited later as clean overlays, per the skill AND this repo's
never-animate-writing rule).

  .venv\\Scripts\\python.exe poc_castbible_look/_01_render_stills.py
"""
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"  # same model as the anchor's own provenance (NOAH.md)
EPISODE = "POC_CastBible_Look"
OUT = Path(__file__).resolve().parent / "stills"
OUT.mkdir(parents=True, exist_ok=True)

NOAH_REF = Path("C:/Users/sanjay/PycharmProjects/ArkAIology/episode-pipeline/cast/noah_ref.png")

# NOAH.md canon description, VERBATIM (skill rule 1)
CANON = (
    "Noah: an ancient, vigorous patriarch -- long white beard squared off at the "
    "chest, white hair swept back to the nape, heavy white brows over deep-set "
    "dark eyes, weathered olive-brown skin, broad strong nose, high forehead with "
    "deep horizontal creases; tall, lean, broad-shouldered; coarse undyed wool "
    "ankle-length tunic, faded terracotta mantle pinned over the left shoulder, "
    "plain rope belt, large rope-scarred hands."
)
SAME_MAN = ("the SAME man as the reference image -- identical face, beard, hair, "
            "and clothing.")
ARK = ("the vast FLAT-SIDED RECTANGULAR hull of hand-hewn planks, a giant box "
       "with straight vertical walls, NOT a curved boat bow")

STYLE = (
    "Editorial documentary sketch illustration: loose confident graphite-and-ink "
    "linework with muted watercolor wash, drawn on aged warm cream paper. "
    "Aged-print paper-collage aesthetic: warm cream and kraft textured stock, "
    "torn and cut-paper edges, subtle offset-halftone dot texture, faint "
    "engineering-grid hairlines, soft raking museum light, tactile hand-made "
    "feel, muted ink-red and ink-blue accents, a thin strip of gold leaf at one "
    "edge. CRITICAL: absolutely NO lettering, numerals, words, newsprint, "
    "printed book-page text, handwriting, ruler markings, dates, or captions "
    "ANYWHERE on ANY layer -- every paper surface is BLANK textured stock."
)

# (name, use_ref, scene)
SHOTS = [
    ("s1_builder", True,
     f"{ARK[0].upper()}{ARK[1:]} rises on timber scaffolding across the paper "
     f"spread, drawn in sketch cutaway style. Before it, small against the great "
     f"unfinished wall of planks, stands {CANON} {SAME_MAN} He looks up at the "
     f"hull, one hand resting on a hewn timber."),

    ("s2_rain", True,
     f"Dark ink-wash storm sky bleeds down the aged paper above {ARK}; the first "
     f"heavy rain falls in long graphite streaks. On the earthen ramp before the "
     f"great open side door of the hull stands {CANON} {SAME_MAN} He looks up "
     f"into the rain, mantle darkening with water."),

    ("s3_shut", False,
     "Close on the great side door of the ark: a massive flat rectangular plank "
     "door set in the towering flat-sided plank hull, closed, heavy and final, "
     "rain-dark timber streaked by graphite rain; a thin warm line of lamplight "
     "glows around its sealed edge, the only warmth in the cold ink-wash storm. "
     "Sketch cutaway style on aged paper."),

    ("s4_onedoor", False,
     "A stark quiet editorial spread: the shut rectangular plank door of the ark "
     "drawn alone at the center of blank aged paper, framed by torn kraft-paper "
     "edges and faint engineering grid, a single warm light-line around its "
     "sealed edge, generous empty paper space all around, still and final."),

    ("s5_thedoor", False,
     "The same great rectangular plank door now standing OPEN at the center of "
     "the paper spread, radiant warm gold light flooding out of the open doorway "
     "across the aged paper, gold leaf glinting where the light touches; the "
     "dark ink-wash storm peels back from the light like lifting torn-paper "
     "layers."),

    ("s6_landing", False,
     "A wide editorial spread: a small radiant OPEN doorway at the heart of the "
     "aged-paper collage, warm gold light spilling from it across the spread; "
     "around it the story sketched faint in graphite -- the vast flat-sided "
     "rectangular ark hull, the storm wash, a small dove in flight -- each "
     "sketch connected to the glowing doorway by a fine thread of gold across "
     "the paper."),
]


def run(prompt, out, use_ref):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt,
           "--aspect_ratio", "16:9", "--resolution", "2k", "--wait"]
    if use_ref:
        cmd += ["--image", str(NOAH_REF)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-300:]}")
        return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    assert NOAH_REF.exists(), f"missing anchor: {NOAH_REF}"
    for name, use_ref, scene in SHOTS:
        out = OUT / f"{name}.png"
        if out.exists():
            print(f"[skip] {name} exists")
            continue
        prompt = STYLE + "\n\n" + "SCENE: " + scene
        print(f"[img] {name} (ref={use_ref}) ...", flush=True)
        ok = run(prompt, out, use_ref)
        if not ok:
            print("   retrying once ...")
            time.sleep(5)
            ok = run(prompt, out, use_ref)
        if ok:
            try:
                cost.record_hf(EPISODE, "short", "stills", MODEL, note=f"[castbible-poc] {name}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
