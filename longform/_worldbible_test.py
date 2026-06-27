"""World & Character Bible test — re-render EW02's Abraham stills with a per-episode world
spec (period+place, lighting, exact character sheets, hard no-modern + no-stray-bearded-men
negatives) injected into EVERY prompt, for cross-still CONSISTENCY. Renders to a test folder
for old-vs-new comparison. ~$2.4 (6 stills)."""
import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline.visual_models import Scene
from pipeline import visual_render

config.VISUAL_STYLE_BASE = ("Baroque oil painting, dramatic chiaroscuro, Caravaggio and "
    "Rembrandt lighting, fine visible brushwork, reverent sacred art")
config.VISUAL_STYLE_TAIL = "no text, vertical 9:16 composition"

WORLD = {
 "period_place": ("Setting: the Patriarchal age, Middle Bronze Age Canaan and the stony hill "
    "country toward Moriah, about 2000 BC — the world of a wandering Semitic herdsman-"
    "patriarch: black goat-hair tents, rocky scrubland, stony hill paths, a desert thicket; "
    "everything ancient and pre-Iron-Age"),
 "lighting": ("Lighting & palette: warm low chiaroscuro, deep shadow with a single dominant "
    "warm light per scene (a clay oil lamp, dawn, or amber dusk); muted earth tones of ochre, "
    "umber, bone-white and deep brown, consistent across every painting"),
 "characters": {
  "Abraham": ("ABRAHAM (the SAME man in every painting): an aged Semitic patriarch about one "
     "hundred years old yet lean and upright, with a long flowing iron-grey beard, a deeply "
     "lined sun-darkened face, heavy sorrowful deep-set brown eyes, wearing a plain undyed "
     "coarse-wool robe and a simple draped head-cloth"),
  "Isaac_youth": ("ISAAC (the SAME young man each time he appears): a strong Hebrew youth of "
     "about twenty, dark wavy hair and a short dark beard, smooth olive skin, in a plain "
     "undyed linen tunic"),
  "Isaac_infant": ("the infant ISAAC: a sleeping newborn boy swaddled in plain cloth"),
 },
 "negatives": ("STRICTLY no modern or anachronistic elements — no Iron-Age, Greco-Roman, "
    "medieval, European or modern objects, no metal armour, no later stone-temple "
    "architecture, no eyeglasses, no modern fabric or stitching. ABRAHAM is the ONLY elderly "
    "grey-bearded man in any scene — do NOT add any other old bearded men; incidental "
    "background figures are younger and clearly Bronze-Age Semitic"),
}

def world_prompt(cast, subject):
    sheets = " ".join(WORLD["characters"][c] for c in cast)
    return (f"{WORLD['period_place']}. {WORLD['lighting']}. CHARACTERS: {sheets}. "
            f"SCENE: {subject}. {WORLD['negatives']}")

# (slug, cast, subject core)
PAINTINGS = [
 ("01_hook", ["Abraham","Isaac_infant"],
  "Abraham alone in a dim goat-hair tent at night, a clay lamp lighting his weathered face; one hand cradling the sleeping infant Isaac against his chest, the other resting on a sheathed sacrificial knife on a low table; a shaft of cold moonlight through the tent flap points toward a dark distant mountain; one dominant figure, deep negative space"),
 ("02_wood", ["Abraham","Isaac_youth"],
  "Isaac bowed under a heavy bundle of split firewood lashed across his shoulders, climbing a rocky mountain path at dawn; Abraham a step behind carrying fire and a knife, head lowered in grief; two figures only, vast empty hillside, the wood the bright focal mass"),
 ("03_lamb", ["Abraham","Isaac_youth"],
  "Isaac paused on the mountain path, turned back looking up into Abraham's face with a question on his lips; Abraham's face breaking with unspeakable sorrow, one hand half-raised toward heaven; warm low side-light on both faces, the slope falling into shadow"),
 ("04_altar", ["Abraham","Isaac_youth"],
  "Isaac bound with rope upon a rough stone altar stacked with firewood, eyes open and trusting; Abraham standing over him, a knife raised high in a trembling fist; a sudden burst of golden light tears the upper sky with an outstretched radiant hand of restraint within it, the knife caught at the top of its arc"),
 ("05_ram", ["Abraham","Isaac_youth"],
  "A single ram caught fast by its curling horns in a dense desert thicket, struggling in a pool of warm light, a thin line of blood at its flank; behind it the empty altar and the freed Isaac embraced by Abraham in soft shadow; the ram the bright dominant subject"),
 ("06_waiting", ["Abraham","Isaac_youth"],
  "Abraham descending a mountain at dusk, Isaac walking ahead into the valley; Abraham pausing to look back up at the bare dark summit with a searching, unfinished expression, one empty open hand at his side; long amber dusk light, deep negative sky"),
]

OUT = ROOT/"longform/EW02_Abraham/v1/short/_worldlock_test"; OUT.mkdir(parents=True, exist_ok=True)
prov = visual_render.HFProvider()
for slug, cast, subj in PAINTINGS:
    png = OUT/f"{slug}.png"
    if png.exists(): print(f"[skip] {slug}"); continue
    sc = Scene(index=0, slug=slug, title=slug, scene_type="single", arc_position="body",
        framing="medium", purpose=slug, rationale="worldlock",
        visible_elements=subj[:150], emotional_tone="reverent",
        subject_block=world_prompt(cast, subj), mood_block="reverent", jesus_variant=None)
    print(f"[still] {slug} (world-locked) ...", flush=True); t=time.time()
    png.write_bytes(prov.generate(sc))
    print(f"[still] {png}  ({time.time()-t:.0f}s)")
print("\nDONE -> _worldlock_test/")
