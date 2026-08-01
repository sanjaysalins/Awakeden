"""Bronze Serpent -- s12 rebuild, Style 6 GILDED PROCLAMATION insert page
(2026-07-31, second insert page per the user's own request: "one more page
like [s08]").

Context (read before touching this file):
- poc_living_sketchbook/_FABLE_STYLE_TOOLKIT.md Style 6 section -- the
  register: illuminated-manuscript plate on aged vellum, the scene's LIGHT
  rendered as burnished real gold leaf, iron-gall underdrawing, lapis +
  vermilion accents, psalter-miniature formality, accurate ancient dress,
  no lettering. "gold = His glory only... this register lets glory own the
  whole ground."
- poc_living_sketchbook/_style_bakeoff/_render_stills_round3.py -- the
  S6_GILDED style block below is BYTE-IDENTICAL to that already-adopted
  block (combo_style6_manner_of_man, style6_gilded_bush/transfiguration).
- poc_living_sketchbook/bronze_serpent/_s2_stills.py -- JESUS canon +
  BRONZE_SERPENT constant (gold reserved for Christ's glory alone, never
  the serpent -- the Nehushtan error) + s12's original Style-1 SCENE, kept
  here only as a comment for continuity, not reused.
- poc_living_sketchbook/bronze_serpent/_TIMING.md -- s12's real window
  57.128-62.936s, beat text "The cure was never in you; it hangs in plain
  sight, and costs you nothing but a look."

s08 was a two-panel LABELED comparison (Scholar's Margin / Style 3,
"NUMBERS 21" / "JOHN 3"). s12 is deliberately different: ONE UNIFIED
composition (no split, no labels, no verse references) -- the bronze
serpent low and small in the earthbound foreground, the cross rising gold
behind/above it, both held in a single unbroken view. No repo-level Jesus
anchor is chained (matching the style bake-off's own precedent for Style 6
-- SKILL.md sec.2: anchor PNGs are PER STYLE FAMILY, a Style-1 sketch
anchor would drag that style's line-and-wash look into a gold-ground plate;
canon TEXT only, same as the s08 Style-3 render's own precedent).

Ledgered under LS_BronzeSerpent, note [bronzeserpent] s12_echo_style6.

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent/_s12_style6_render.py
"""
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
EPISODE = "LS_BronzeSerpent"
OUT = Path(__file__).resolve().parent / "stills" / "s12_echo.png"
NOTE = "bronzeserpent] s12_echo_style6"

JESUS = (
    "Jesus: a Judean man in his early thirties. Face geometry: a strong "
    "straight nose, defined cheekbones, a broad calm forehead, an angular "
    "jaw beneath the beard. Hair: long dark wavy hair falling past the "
    "shoulders, parted center. Beard: short, close-cropped, dark, well-kept. "
    "Skin: sun-weathered olive Mediterranean complexion. Build: lean and "
    "wiry-strong, a carpenter's and traveler's frame."
)

BRONZE_SERPENT = (
    "a serpent cast in dull matte olive-bronze and tan metal, NOT bright or "
    "gleaming, NOT gold-toned, its color clearly duller and colder than any "
    "gold elsewhere on the page, coiled around a SINGLE STRAIGHT wooden "
    "pole -- the pole is a plain bare rod only, perfectly straight, with "
    "NO crossbar, NO horizontal beam, NO second piece of wood anywhere on "
    "it, NOT cross-shaped or T-shaped in any way, nothing else attached to "
    "it -- gold is reserved for Christ's glory alone in this episode, "
    "never for the serpent or its pole"
)

NOTEXT = (
    "CRITICAL: absolutely NO lettering, numerals, words, handwriting, "
    "captions, scripture references, or printed text ANYWHERE in the "
    "image -- every surface is blank textured stock."
)

FULLBLEED = (
    "CRITICAL FRAMING: the illustrated scene fills the ENTIRE frame edge to "
    "edge, corner to corner -- no large blank margin, no small inset drawing "
    "floating on empty paper; the artwork itself IS the page."
)

# byte-identical to the already-adopted Style 6 block
# (_style_bakeoff/_render_stills_round3.py's S6_GILDED)
S6_GILDED = (
    "An illuminated manuscript painting on aged vellum: the light of the "
    "scene rendered as burnished REAL GOLD LEAF pressed onto the page, "
    "gleaming, with visible leaf seams and burnish marks, over fine "
    "iron-gall ink underdrawing; mineral pigment accents of deep lapis "
    "blue and vermilion; the flat sacred formality of an ancient psalter "
    "miniature joined to tender, accurate hand-painted detail -- dress and "
    "world faithfully ancient Judean. Tactile hand-made vellum grain, "
    "quiet margins. "
) + NOTEXT

SCENE = (
    f"A single unified vision, one continuous scene with no dividing line, "
    f"no border, and no second panel anywhere on the page -- nothing here "
    f"is split or compared side by side. The lower part of the page is "
    f"bare sunbaked earth and sand; standing on that plain ground, low and "
    f"small in the near foreground, {BRONZE_SERPENT}, planted upright in "
    f"the sand -- its own dull metal never catches any gold reflection, "
    f"whatever light fills the page above it. Rising directly up out of "
    f"that same ground and filling the greater part of the page above the "
    f"serpent, {JESUS} lifted up on a plain wooden cross, arms resting "
    f"along the crossbeam, head bowed low in stillness and peace, a plain "
    f"white loincloth His only garment -- His skin is entirely smooth and "
    f"unmarked all over, exactly like an unbroken sculpture, with no crown "
    f"of thorns, no wound, no cut, no scratch, no bruise, and absolutely "
    f"no red, pink, or dark mark of any kind anywhere on His body -- not "
    f"on His hands, wrists, feet, ribs, side, or torso -- the skin along "
    f"His ribs and side in particular is completely plain and untouched, "
    f"the same smooth tone as the rest of His torso, and the nail "
    f"fastening at His hands and feet is not shown in any close detail. "
    f"Behind and around His lifted figure, from "
    f"the crossbeam to the very top of the page, the whole sky is burnished "
    f"real gold leaf pressed in visible sheets with leaf seams and burnish "
    f"marks -- one single gathered radiance, filling the heavens above Him "
    f"and stopping at the earth-line where the serpent stands, so the gold "
    f"and the dull bronze never touch or mix: the glory belongs to Him "
    f"alone. No crowd, no soldiers, no other figure, no hillside, no camp "
    f"-- only the small plain serpent low in front and the gold-crowned "
    f"cross rising behind it, both held together within one single "
    f"unbroken view, hanging in plain sight together. " + FULLBLEED
)


def run(prompt, out):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt,
           "--aspect_ratio", "9:16", "--resolution", "2k", "--wait"]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        return False, blob.strip()[-300:]
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000, ""


def main():
    tmp = OUT.with_name("s12_echo.style6_candidate_v3.png")
    prompt = S6_GILDED + "\n\nSCENE: " + SCENE
    ok, err = run(prompt, tmp)
    if not ok:
        time.sleep(3)
        ok, err = run(prompt, tmp)
    if ok:
        cost.record_hf(EPISODE, "short", "stills", MODEL, note=f"[{NOTE}]")
        print(f"[ok] {tmp}")
    else:
        print(f"[FAILED] {err}")


if __name__ == "__main__":
    main()
