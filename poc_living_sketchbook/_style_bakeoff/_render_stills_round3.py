"""Style bake-off round 3 -- STORM COMPLEMENTS (Fable, 2026-07-31).

The user's ask: styles that complement/elevate the shipped Storm episode's
Style 1 spreads for storm/sea/weather/creation-obedience content, plus real
proof that Style 3 and Style 6 can be used IN COMBINATION with Storm's own
beats. 4 new candidates (one proof still each, every one an actual Storm
beat) + 2 combination stills:

  style12_tempestink_rebuke   NEW: expressive ink-storm (ink=storm, paper=calm)
  style13_chart_crossing      NEW: mariner's working chart of the crossing
  style14_engraving_tempest   NEW: intaglio line-engraving (line-field = wind-field)
  style15_deepvigil_perish    NEW: Style 5 storm-variation (the enormity of the deep)
  combo_style3_jonah_echo     Style 3 WITH Storm: Jonah 1 / Ps 107:29 echo sheet
  combo_style6_manner_of_man  Style 6 WITH Storm: Matt 8:27 gold-ground plate

Same nano_banana_pro path / canon text / NOTEXT / FULLBLEED rules as rounds
1-2. Ledgered under LS_StyleBakeoff, notes [bakeoff-r3-storm]. 6 x 2cr = 12cr
quote; hard stop for the round is 8 stills total.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_style_bakeoff/_render_stills_round3.py [name,name]
"""
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
EPISODE = "LS_StyleBakeoff"
OUT = Path(__file__).resolve().parent
OUT.mkdir(parents=True, exist_ok=True)

JESUS = (
    "Jesus: a Judean man in his early thirties. Face geometry: a strong "
    "straight nose, defined cheekbones, a broad calm forehead, an angular "
    "jaw beneath the beard. Hair: long dark wavy hair falling past the "
    "shoulders, parted center. Beard: short, close-cropped, dark, well-kept. "
    "Skin: sun-weathered olive Mediterranean complexion. Build: lean and "
    "wiry-strong, a carpenter's and traveler's frame. Eyes: warm deep brown, "
    "level and calm. Garment: simple undyed homespun ankle-length tunic with "
    "a woven cord sash, leather sandals."
)
NOTEXT = (
    "CRITICAL: absolutely NO lettering, numerals, words, handwriting, "
    "captions, or printed text ANYWHERE in the image -- every surface is "
    "blank textured stock."
)
FULLBLEED = (
    "CRITICAL FRAMING: the illustrated scene fills the ENTIRE frame edge to "
    "edge, corner to corner -- no large blank margin, no small inset drawing "
    "floating on empty paper; the artwork itself IS the page."
)

# ---- the two ALREADY-ADOPTED style blocks, byte-identical to round 1 --------

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

# ---- the four NEW candidate style blocks ------------------------------------

S12_TEMPEST_INK = (
    "An expressive ink-storm painting in bold wet black calligraphic ink "
    "and charcoal-gray wash on warm cream paper: the element itself is the "
    "subject -- huge confident wet brush strokes, dry-brush spray flicked "
    "from the brush tip, flung ink droplets, pooling washes with feathered "
    "blooming edges, enormous kinetic energy held in a few decisive marks; "
    "large regions of untouched cream paper carry the stillness wherever "
    "the storm is not; a single muted ink-blue undertone in the deepest "
    "washes. Tactile, hand-made, sheet-scale energy -- the violence is all "
    "ink, the calm is all paper. " + NOTEXT
)

S13_CHART = (
    "A hand-drawn mariner's chart in iron-gall sepia ink on aged, "
    "sea-stained parchment, in the idiom of an ancient pilot's own working "
    "chart: coastlines drawn with fine hatched shading, a hand-inked "
    "compass wind-rose of plain radiating points, faint ruled rhumb lines "
    "crossing the water, small plain dots for depth soundings, a dotted "
    "route line with small hand-drawn open-chevron direction arrows, tiny "
    "hand-inked wave marks on the open water, and exactly ONE element "
    "touched with real burnished gold leaf. Dense, orderly, tactile, "
    "hand-made -- a working seaman's document, never a modern printed map."
)

S14_ENGRAVING = (
    "An antique intaglio line-engraving printed in warm black ink on ivory "
    "laid paper: the entire image built from dense systems of fine engraved "
    "lines that swell and taper, deep cross-hatched shadow, short burin "
    "flicks for spray; in the sky every line is a wind-line following the "
    "gale, in the sea every line is a current-line following the swell -- "
    "one continuous flowing field of force rendered entirely in line; deep "
    "tonal blacks, silvery middle grays, sparing white paper lights. "
    "Hand-engraved, hand-printed energy, never a photograph. " + NOTEXT
)

S15_DEEP_VIGIL = (
    "A grave chiaroscuro ink nocturne on ash-gray toned paper: deep "
    "near-black ink wash masses holding almost the whole page in darkness, "
    "the sea and the night sky one continuous dark, restrained deliberate "
    "linework, exactly TWO small light sources -- one cold pale break of "
    "moonlight far above, one tiny warm lantern point below -- a nearly "
    "monochrome palette of slate, ash and bone. Solemn, vast, utterly "
    "reverent restraint: the enormity of the deep carries the weight. Aged "
    "hand-made paper. " + NOTEXT
)

# ---- shots: (name, style_block, scene) --------------------------------------

SHOTS = [
    ("style12_tempestink_rebuke", S12_TEMPEST_INK,
     f"Matthew 8:26 -- he arose, and rebuked the winds and the sea: a "
     f"towering storm wave rendered as one colossal rearing arc of wet "
     f"black ink curling over a small first-century Galilean fishing boat "
     f"with a single bare mast, the wave's crest breaking into dry-brush "
     f"spray and flung ink droplets arrested mid-air; standing upright and "
     f"utterly calm in the boat's stern, one arm raised toward the wave: "
     f"{JESUS} His ankle-length tunic is ONE continuous garment falling all "
     f"the way to the deck, and his leather sandals are visible on his feet "
     f"beneath its hem. Ahead of the boat, where his arm points, the water is "
     f"already glass-flat untouched cream paper crossed by two thin "
     f"confident horizon strokes. {FULLBLEED}"),

    ("style13_chart_crossing", S13_CHART,
     "The night crossing of the Sea of Galilee: the lake drawn as a broad "
     "harp-shaped inland sea seen from above, hatched hills along its "
     "shores, a dotted crossing route running from the northwest shore "
     "toward the southeast shore; midway along the route the open water is "
     "hatched dense and dark into a drawn squall -- a whorl of driving "
     "hand-inked wind-lines; at the exact heart of the squall a small "
     "hand-inked first-century fishing boat seen from above, and touching "
     "the boat the chart's single gold-leaf element: a small pressed-gold "
     "flame-point marking the One asleep aboard her, the squall's "
     "wind-lines bending around that gold point. The ONLY text anywhere on "
     "the chart is two short hand-lettered labels in rubric-red antique "
     "serif capitals: exactly the words \"GALILEE\" on the open water and "
     "exactly the words \"MATTHEW 8\" in the lower margin -- no other "
     "words, letters or numerals anywhere. " + FULLBLEED),

    ("style14_engraving_tempest", S14_ENGRAVING,
     "Matthew 8:24 -- and, behold, there arose a great tempest in the sea: "
     "a small first-century Galilean fishing boat with a single mast and "
     "furled sail heels in the trough between two enormous engraved "
     "swells, three tiny figures aboard her straining at oars and bailing "
     "-- first-century Judean fishermen, every one of them bare-headed "
     "with dark hair and short beards in the ancient Judean manner, "
     "wearing simple knee-length working tunics girded with a cord; "
     "the whole sky above is one vast spiraling system of engraved "
     "storm-lines converging over the mast, driving rain cut as fine "
     "diagonal lines, spray cut as white flecks against the black sea. "
     + FULLBLEED),

    ("style15_deepvigil_perish", S15_DEEP_VIGIL,
     "Psalm 107:23-27 heard through Matthew 8:25 -- they that go down to "
     "the sea in ships... Lord, save us: we perish: seen from high and far "
     "away, a tiny single-masted first-century fishing boat, lit only by "
     "the one small warm lantern glow aboard her, lies deep in the trough "
     "between mountainous near-black swells rising above her on either "
     "side; far above, one narrow cold break of moonlight opens in the "
     "storm sky and falls toward the boat. The boat is almost nothing "
     "against the deep; the deep is almost nothing against that light. "
     + FULLBLEED),

    # ---- the two COMBINATION proofs (adopted styles x Storm's own beats) ----

    ("combo_style3_jonah_echo", S3_MARGIN,
     f"A typology comparison sheet of two storms at sea. LEFT: a "
     f"hand-inked study of the prophet's ship out of Joppa in a raging "
     f"tempest, oars straining, as one lone robed man is cast over her "
     f"side toward the towering sea -- labeled below in rubric-red antique "
     f"serif capitals with exactly the words \"JONAH 1\". RIGHT: a "
     f"hand-inked study of a first-century Galilean fishing boat on water "
     f"gone dead flat, and standing upright in her stern with one arm "
     f"extended over the sea: {JESUS} His standing figure and the light "
     f"around him are the sheet's ONLY element touched with burnished gold "
     f"leaf -- labeled below in rubric-red antique serif capitals with "
     f"exactly the words \"MATTHEW 8\". Between the two studies a single "
     f"hand-drawn sepia comparison arrow with an open chevron head points "
     f"from the ship of Joppa to the Galilean boat. Centered below both "
     f"studies, a small hand-inked diagram of one storm wave settling into "
     f"a flat calm line, labeled in rubric-red antique serif capitals with "
     f"exactly the words \"PSALM 107:29\". Fine ruled construction lines "
     f"and margin cross-hatching complete the sheet; the margins are "
     f"otherwise bare of any writing. The ONLY text on the page is the "
     f"three labels \"JONAH 1\", \"MATTHEW 8\" and \"PSALM 107:29\" -- no "
     f"other words, letters or numerals anywhere. " + FULLBLEED),

    ("combo_style6_manner_of_man", S6_GILDED,
     f"Matthew 8:27 -- what manner of man is this, that even the winds and "
     f"the sea obey him: {JESUS} He stands upright in the stern of a "
     f"first-century Galilean fishing boat, arms lowered and at rest, his "
     f"face serene and level; the ENTIRE sky behind and above him, from "
     f"the horizon to the top of the page, is burnished real gold leaf "
     f"pressed in visible sheets with leaf seams and burnish marks -- the "
     f"storm gone, the heavens holding his glory; the sea below lies as "
     f"flat polished glass in deep lapis blue, carrying one narrow column "
     f"of gold reflection straight down from him; in the boat's waist "
     f"three disciples in lapis-shadowed robes shrink back in awe, faces "
     f"lifted toward him, half in shadow. {FULLBLEED}"),
]


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


def one(name, style, scene):
    out = OUT / f"{name}.png"
    if out.exists():
        return name, "skip"
    prompt = style + "\n\nSCENE: " + scene
    ok, err = run(prompt, out)
    if not ok:
        time.sleep(3)
        ok, err = run(prompt, out)
    if ok:
        try:
            cost.record_hf(EPISODE, "short", "stills", MODEL, note=f"[bakeoff-r3-storm] {name}")
        except Exception:
            pass
        return name, "ok"
    return name, f"FAILED {err}"


def main(only=None):
    shots = SHOTS if only is None else [s for s in SHOTS if s[0] in only]
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(one, n, s, sc): n for n, s, sc in shots}
        for fut in as_completed(futs):
            name, status = fut.result()
            print(f"[{status}] {name}", flush=True)
    print(f"[out] {OUT}")


if __name__ == "__main__":
    only = sys.argv[1].split(",") if len(sys.argv) > 1 else None
    main(only)
