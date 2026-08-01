"""Style bake-off round 5 -- BRONZE SERPENT E2E PLAN, section D proof still
(Fable's round, continued by Sonnet after Fable hit its usage limit,
2026-07-31). ONE render only, per the round's spend ceiling.

The ONE typology insert page the round's beat plan (_FABLE_ROUND9_
BRONZESERPENT_E2E_PLAN.md, section A, spread s08) calls for: Numbers 21's
bronze serpent lifted on its pole, beside John 3:14's "even so must the Son
of man be lifted up" -- the Scholar's-Margin register (Style 3), byte-
identical style block to the proven combo_style3_jonah_echo.png precedent,
new SCENE content only. Gold touches ONLY the Christ element (palette
theology: gold = His glory, never the bronze serpent, which stays bronze/
ochre). No locked Moses cast anchor exists yet in this project -- at this
diagram-panel scale (a small study figure, not a portrait close-up) that is
fine, per Round 3's own precedent on the boat-panel Jesus figure; a full
episode build would need a real cast/MOSES.md + anchor chained across every
appearance (see the plan doc's honest-flags section).

Crucifixion depicted reverently at diagram scale: arms along the crossbeam,
no nail/wound close-up detail (project convention favors under-specifying
fastening detail over graphic nails at small scale), head bowed -- doctrine
sound, nothing gratuitous.

Ledgered under LS_StyleBakeoff, note [bakeoff-r5-bronzeserpent-plan].

  .venv\\Scripts\\python.exe poc_living_sketchbook/_style_bakeoff/_render_r5_bronzeserpent_typology.py
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
EPISODE = "LS_StyleBakeoff"
OUT = Path(__file__).resolve().parent
NOTE = "bakeoff-r5-bronzeserpent-plan"

JESUS = (
    "Jesus: a Judean man in his early thirties. Face geometry: a strong "
    "straight nose, defined cheekbones, a broad calm forehead, an angular "
    "jaw beneath the beard. Hair: long dark wavy hair falling past the "
    "shoulders, parted center. Beard: short, close-cropped, dark, well-kept. "
    "Skin: sun-weathered olive Mediterranean complexion. Build: lean and "
    "wiry-strong, a carpenter's and traveler's frame."
)

MOSES = (
    "an elderly Hebrew prophet and leader in his eighties: a long flowing "
    "white beard and white hair, deeply weathered sun-browned skin, a "
    "strong upright bearing despite his age. Garment: a plain long undyed "
    "woolen robe belted at the waist, a simple woven mantle over one "
    "shoulder, leather sandals -- no headwear, no ornament."
)

FULLBLEED = (
    "CRITICAL FRAMING: the illustrated scene fills the ENTIRE frame edge to "
    "edge, corner to corner -- no large blank margin, no small inset drawing "
    "floating on empty paper; the artwork itself IS the page."
)

# byte-identical to the already-adopted Style 3 block (round 1/round 3 scripts)
S3_MARGIN = (
    "A scholar's analytical study sheet in iron-gall sepia ink on aged "
    "parchment, in the manner of a Renaissance workshop notebook page: "
    "small precise hand-inked diagrams, faint ruled construction lines and "
    "compass arcs, hand-drawn comparison arrows with open chevron heads, "
    "fine cross-hatched shading, small neat hand-lettered labels in antique "
    "serif capitals, scripture references in rubric-red ink, and exactly "
    "ONE element touched with real burnished gold leaf. The page reads as a "
    "working scholar's own analysis -- dense, orderly, tactile, hand-made "
    "-- never a modern printed chart or slide."
)

SCENE = (
    f"A scholar's typology comparison sheet on the wilderness serpent and "
    f"its fulfilment. LEFT: a hand-inked study of {MOSES} lifting high a "
    f"small serpent cast in bronze, coiled around the top of a bare wooden "
    f"pole planted upright in the sand, before a camp of simple tents in "
    f"open wilderness -- the serpent and pole stay plain bronze and wood, "
    f"untouched by gold -- labeled below in rubric-red antique serif "
    f"capitals with exactly the words \"NUMBERS 21\". RIGHT: a hand-inked "
    f"study of {JESUS}, his arms resting along a plain wooden crossbeam, "
    f"lifted up on a simple wooden cross planted on a bare hillside, his "
    f"head bowed in reverence, rendered at this small diagram scale with no "
    f"close-up wound or nail detail; his lifted figure and the light around "
    f"him are the sheet's ONLY element touched with real burnished gold "
    f"leaf -- labeled below in rubric-red antique serif capitals with "
    f"exactly the words \"JOHN 3\". Between the two studies a single "
    f"hand-drawn sepia comparison arrow with an open chevron head points "
    f"from the bronze serpent on its pole to the lifted figure on the "
    f"cross. Fine ruled construction lines and margin cross-hatching "
    f"complete the sheet; the margins are otherwise bare of any writing. "
    f"The ONLY text anywhere on the page is the two labels \"NUMBERS 21\" "
    f"and \"JOHN 3\" -- no other words, letters or numerals anywhere. "
    + FULLBLEED
)

NAME = "bronzeserpent_typology_numbers21_john3"


def run(prompt, out):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt,
           "--aspect_ratio", "9:16", "--resolution", "2k", "--wait"]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        return False, blob.strip()[-250:]
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000, ""


def main():
    out = OUT / f"{NAME}.png"
    if out.exists():
        print(f"[skip] {out} already exists")
        return
    prompt = S3_MARGIN + "\n\nSCENE: " + SCENE
    ok, err = run(prompt, out)
    if not ok:
        import time
        time.sleep(3)
        ok, err = run(prompt, out)
    if ok:
        cost.record_hf(EPISODE, "short", "stills", MODEL, note=f"[{NOTE}] {NAME}")
        print(f"[ok] {out}")
    else:
        print(f"[FAILED] {err}")


if __name__ == "__main__":
    main()
