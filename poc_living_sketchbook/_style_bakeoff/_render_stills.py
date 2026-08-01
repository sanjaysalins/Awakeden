"""Style bake-off — 5 complementary living-sketchbook styles, 2 stills each.
Funded round (user, 2026-07-30, ceiling 200cr). Additive only: everything in
_style_bakeoff/. nano_banana_pro 2cr/still via HF CLI (the proven storm/_s2
path), ledgered per render (episode LS_StyleBakeoff).

Per SKILL.md sec.2: canon TEXT is series-wide, anchor PNGs are PER STYLE
FAMILY -- so no cross-style anchor chaining here (it would drag Style 1's
look into the new styles). Winning styles mint their own anchors later.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_style_bakeoff/_render_stills.py [name,name]
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
EPISODE = "LS_StyleBakeoff"
OUT = Path(__file__).resolve().parent
OUT.mkdir(parents=True, exist_ok=True)

# Series-wide canon TEXT, verbatim from cast/JESUS.md (no anchor: per-style-family rule)
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
    "captions, or printed text ANYWHERE in the image -- every paper surface "
    "is blank textured stock."
)
FULLBLEED = (
    "CRITICAL FRAMING: the illustrated scene fills the ENTIRE frame edge to "
    "edge, corner to corner -- no large blank paper region, no small inset "
    "drawing floating on empty paper; the artwork itself IS the page."
)

# ---- the five style blocks (frozen; only the SCENE changes) -----------------

S2_GESTURE = (
    "A rough charcoal gesture study on warm gray toned newsprint paper: "
    "fast, confident vine-charcoal strokes, shading smudged and dragged by "
    "thumb, sweeping kinetic motion lines, loose unfinished edges where "
    "strokes trail off mid-gesture, white chalk highlights on the light "
    "side, the drawing caught mid-thought like a courtroom artist working "
    "at full speed. Palette: charcoal black, warm gray paper, white chalk, "
    "and ONE dry ink-red accent at most. Charcoal dust and finger smudges "
    "live in the margins; tactile hand-made sketchbook page. "
) + NOTEXT

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

S4_HEARTH = (
    "A warm storybook illustration in gouache and colored pencil on cream "
    "cotton paper: soft rounded brushwork, a honey-amber, olive-green and "
    "terracotta palette, gentle golden-hour light, visible dry-brush paper "
    "grain, tender folk-tale warmth carried with real human dignity -- "
    "never cartoonish, never cute; faces are simply drawn but true and "
    "expressive, dress and world faithfully ancient Judean. A hand-made "
    "picture-book page with softly feathered painted edges. "
) + NOTEXT

S5_VIGIL = (
    "A grave chiaroscuro ink drawing on ash-gray toned paper: deep "
    "near-black ink wash masses holding most of the page in shadow, "
    "restrained deliberate linework, a single source of pale cold light, "
    "charcoal depth worked into the darks, a nearly monochrome palette of "
    "slate, ash and bone with at most one sparing dried-blood red accent. "
    "Solemn, still, utterly reverent restraint -- the shadow and the "
    "emptiness carry the weight. Aged hand-made paper, quiet plain "
    "margins. "
) + NOTEXT

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

# ---- shots: (name, style_block, scene) --------------------------------------

SHOTS_ALL = [
    # STYLE 2 -- charcoal gesture (action/transition register)
    ("style2_gesture_temple", S2_GESTURE,
     f"Matthew 21:12 -- Jesus casting out the moneychangers: {JESUS} He "
     f"strides forward mid-motion, both hands overturning a wooden "
     f"moneychanger's table, coins scattering in the air, doves bursting "
     f"upward from toppling wicker cages, two merchants recoiling as loose "
     f"gesture figures; massive ashlar stone columns of the Jerusalem "
     f"temple court behind. Everything caught in urgent sweeping charcoal "
     f"motion. No whip or scourge anywhere. {FULLBLEED}"),

    ("style2_gesture_bartimaeus", S2_GESTURE,
     f"Mark 10:50 -- blind Bartimaeus rising: a ragged Judean beggar "
     f"caught mid-rise from the dusty Jericho roadside, flinging his heavy "
     f"outer cloak away behind him in one sweeping charcoal motion arc, "
     f"face lifted with desperate hope, arms reaching forward. He wears a "
     f"single plain ragged knee-length tunic -- ONE continuous garment "
     f"ending above the knee, never separate trouser legs -- with bare "
     f"legs and bare feet below its hem. Ahead of him stands a calm robed "
     f"figure seen from behind waiting on the road, a loose crowd of "
     f"onlookers as bare gesture outlines. The thrown cloak is the single "
     f"ink-red accent. {FULLBLEED}"),

    # STYLE 3 -- scholar's margin (diagram-native register; short labels ONLY)
    ("style3_margin_typology", S3_MARGIN,
     "A typology comparison sheet. LEFT: a hand-inked study of the bronze "
     "serpent of Moses -- a serpent of brass wound around a plain wooden "
     "pole standard, small sick figures at its base looking up at it, "
     "desert ground -- labeled below in rubric-red antique serif capitals "
     "with exactly the words \"NUMBERS 21\". RIGHT: a hand-inked study of "
     "the cross of Christ on the hill, empty, rendered with burnished gold "
     "leaf light behind it -- labeled below in rubric-red antique serif "
     "capitals with exactly the words \"JOHN 3\". Between the two studies "
     "a single hand-drawn sepia comparison arrow with an open chevron "
     "head points from the serpent-pole to the cross. Fine ruled "
     "construction lines and margin cross-hatching complete the sheet. "
     "The ONLY text on the page is the two labels \"NUMBERS 21\" and "
     "\"JOHN 3\" -- no other words, letters or numerals anywhere. "
     + FULLBLEED),

    ("style3_margin_lastweek", S3_MARGIN,
     "A chronology study sheet of the final week: one hand-ruled sepia "
     "timeline band runs down the page, and along it five small "
     "hand-inked vignette studies in sequence: a palm branch; the temple "
     "facade; a cup on a table; the cross on the hill rendered with "
     "burnished gold leaf light behind it; an open empty rock-cut tomb "
     "with its round stone rolled aside. Each vignette sits at its own "
     "tick mark on the ruled line, connected by fine hand-drawn arrows "
     "with open chevron heads, with ruled construction lines and margin "
     "cross-hatching around them. NO words, letters or numerals anywhere "
     "on this sheet -- the five drawings and the ruled line alone carry "
     "the sequence. " + FULLBLEED),

    # STYLE 4 -- hearth storybook (parable register)
    ("style4_hearth_father_ran", S4_HEARTH,
     "Luke 15:20 -- the father who ran: an elderly Judean landowner in "
     "fine but simple robes runs down a dusty village road at golden "
     "hour, robes hitched up in both fists, sandaled feet mid-stride, "
     "face broken open with compassion; far down the road a gaunt ragged "
     "young man walks home small in the distance, barefoot and ashamed; "
     "olive trees, stone walls, warm evening light flooding the whole "
     "road. " + FULLBLEED),

    ("style4_hearth_sower", S4_HEARTH,
     "Matthew 13:3-4 -- the sower went forth to sow: a Judean farmer "
     "broadcast-sowing seed by hand from a cloth sling bag at golden "
     "hour, seed scattering in a warm arc from his open hand; the ground "
     "before him readable in bands -- a trodden wayside path where small "
     "birds wheel down after the fallen seed, a patch of stony shallow "
     "soil, a tangle of thorns, and rich dark tilled earth; terraced "
     "Galilean hillside behind. " + FULLBLEED),

    # STYLE 5 -- passion vigil (grave register)
    ("style5_vigil_gethsemane", S5_VIGIL,
     f"Matthew 26:39 -- Gethsemane: {JESUS} He has fallen forward on his "
     f"knees and face in prayer beneath the black twisted mass of ancient "
     f"olive trees, hands pressed to the rock, pale cold moonlight "
     f"finding only his back and hands out of the enveloping darkness; "
     f"three sleeping figures barely suggested as dark shapes far behind "
     f"him. Almost the whole page is held in deep ink shadow. {FULLBLEED}"),

    ("style5_vigil_darkness", S5_VIGIL,
     "Matthew 27:45 -- darkness over all the land: a wide distant view of "
     "the hill of crucifixion at midday, three crosses in silhouette "
     "against an unnatural failing daylight -- a clear sky gone dark as "
     "if the sun itself is veiled, NO storm clouds, NO lightning, NO "
     "rain; a few small mourning figures stand far below the hill; the "
     "city wall a faint gray mass behind. The dim veiled light is the "
     "single pale source; near-total ink shadow holds the land. "
     + FULLBLEED),

    # STYLE 6 -- gilded proclamation (glory register)
    ("style6_gilded_bush", S6_GILDED,
     "Exodus 3:14 -- the bush that burned and was not consumed: a low "
     "desert thornbush alive with flame rendered entirely as burnished "
     "gold leaf, every tongue of fire pressed gold, the bush's green "
     "branches whole and unburnt within the gold blaze; in the near "
     "foreground a pair of worn leather sandals set aside on the holy "
     "ground. The bush stands utterly alone: bare sun-warmed rock and "
     "sand of Horeb surround it on every side, rendered in warm ochre "
     "ink wash reaching every edge of the frame. The whole page holds "
     "exactly three colors: the pressed gold of the flames, the green of "
     "the living branches, and the warm ochre of bare stone and vellum. "
     + FULLBLEED),

    ("style6_gilded_transfiguration", S6_GILDED,
     f"Matthew 17:2 -- the Transfiguration: {JESUS} He stands on a high "
     f"mountain summit, his face shining and his raiment white as light, "
     f"the radiance around him rendered as burnished gold leaf filling "
     f"the upper page; at his either side two luminous indistinct robed "
     f"forms barely emerge from the gold light; below on the rock three "
     f"disciples have fallen face-down, faces hidden against the ground, "
     f"lapis-blue shadow pooling around them. Only Jesus's face is "
     f"rendered sharp and true. {FULLBLEED}"),
]


def run(prompt, out):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt,
           "--aspect_ratio", "9:16", "--resolution", "2k", "--wait"]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-250:]}")
        return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main(only=None):
    shots = SHOTS_ALL if only is None else [s for s in SHOTS_ALL if s[0] in only]
    for name, style, scene in shots:
        out = OUT / f"{name}.png"
        if out.exists():
            print(f"[skip] {name}")
            continue
        prompt = style + "\n\nSCENE: " + scene
        print(f"[img] {name} ...", flush=True)
        ok = run(prompt, out)
        if not ok:
            time.sleep(5)
            ok = run(prompt, out)
        if ok:
            try:
                cost.record_hf(EPISODE, "short", "stills", MODEL, note=f"[bakeoff] {name}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    only = sys.argv[1].split(",") if len(sys.argv) > 1 else None
    main(only)
