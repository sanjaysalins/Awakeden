"""Tier-2 REFERENCE-LOCK test (EW02): derive the continuity cast from the narration
(Abraham, Isaac), generate ONE clean reference per recurring character, then re-render every
scene attaching the present characters' references via nano_banana_2 --image (input_images).
Locks the actual FACES so 'the boy' stays the same boy. ~$3.2 (2 refs + 6 scenes)."""
import sys, time, subprocess, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline.visual_models import Scene
from pipeline import visual_render
from pipeline.visual_render import _HF_URL_RE

config.VISUAL_STYLE_BASE = ("Baroque oil painting, dramatic chiaroscuro, Caravaggio and "
    "Rembrandt lighting, fine visible brushwork, reverent sacred art")
config.VISUAL_STYLE_TAIL = "no text, vertical 9:16 composition"
STYLE = config.VISUAL_STYLE_BASE
TAIL = config.VISUAL_STYLE_TAIL

WORLD = {
 "period_place": ("Setting: the Patriarchal age, Middle Bronze Age Canaan and the stony hill "
    "country toward Moriah, about 2000 BC — black goat-hair tents, rocky scrubland, stony hill "
    "paths, a desert thicket; ancient and pre-Iron-Age"),
 "lighting": ("warm low chiaroscuro, deep shadow with a single dominant warm light per scene; "
    "muted ochre/umber/bone earth tones, consistent across every painting"),
 "negatives": ("STRICTLY no modern or anachronistic elements; no Greco-Roman/medieval/European "
    "objects, no metal armour, no eyeglasses. Abraham is the ONLY elderly grey-bearded man — do "
    "NOT add other old bearded men; background figures are younger and clearly Bronze-Age Semitic"),
}
ABRAHAM = ("ABRAHAM: an aged Semitic patriarch about one hundred years old, lean and upright, "
   "long flowing iron-grey beard, deeply lined sun-darkened face, deep-set sorrowful brown eyes, "
   "plain undyed coarse-wool robe and simple draped head-cloth")
ISAAC = ("ISAAC: a strong Hebrew youth of about twenty, dark wavy hair and a short dark beard, "
   "smooth olive skin, plain undyed linen tunic")

OUT = ROOT/"longform/EW02_Abraham/v1/short/_reflock_test"; OUT.mkdir(parents=True, exist_ok=True)

def hf_image(prompt, refs):
    cmd = [str(config.HF_CLI_PATH), "generate", "create", "nano_banana_2",
           "--prompt", prompt, "--aspect_ratio", "9:16", "--wait"]
    for r in refs: cmd += ["--image", str(r)]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                         errors="replace", timeout=600)
    m = _HF_URL_RE.search(res.stdout or "")
    if not m:
        raise RuntimeError(f"no image URL: {(res.stdout or res.stderr or '')[-400:]}")
    req = urllib.request.Request(m.group(0), headers={"User-Agent": "JITB/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()

# 1) generate ONE clean reference per recurring character (plain portrait, world-locked)
refs = {}
for name, desc in [("abraham", ABRAHAM), ("isaac", ISAAC)]:
    p = OUT/f"_ref_{name}.png"
    if not p.exists():
        prompt = (f"{STYLE}. A single clear full-length character portrait. {desc}. Standing in "
                  f"neutral warm light against a plain dark background, the face clearly visible. "
                  f"{WORLD['negatives']}. {TAIL}")
        print(f"[ref] {name} ...", flush=True); p.write_bytes(hf_image(prompt, []))
    refs[name] = p

# 2) re-render each scene attaching the present characters' references
def scene_prompt(subject):
    return (f"{STYLE}. {WORLD['period_place']}. {WORLD['lighting']}. SCENE: {subject}. "
            f"{WORLD['negatives']}. {TAIL}")

SCENES = [
 ("01_hook", ["abraham"], "Abraham (the man in the reference image) alone in a dim goat-hair tent at night, a clay lamp lighting his weathered face, cradling a sleeping swaddled infant against his chest, his other hand resting on a sheathed knife on a low table; a shaft of moonlight through the tent flap points to a dark distant mountain"),
 ("02_wood", ["abraham","isaac"], "the youth Isaac (from the reference) bowed under a heavy bundle of split firewood on his shoulders, climbing a rocky path at dawn; Abraham (from the reference) a step behind carrying fire and a knife, head lowered in grief; two figures, vast hillside"),
 ("03_lamb", ["abraham","isaac"], "the youth Isaac (from the reference) turned back looking up into Abraham's face with a question; Abraham (from the reference) breaking with sorrow, one hand half-raised to heaven; warm side-light on both faces"),
 ("04_altar", ["abraham","isaac"], "the youth Isaac (from the reference) bound with rope on a rough stone altar of firewood, eyes trusting; Abraham (from the reference) over him with a knife raised in a trembling fist; a burst of golden light tears the sky with a radiant restraining hand"),
 ("05_ram", ["abraham","isaac"], "a single ram caught by its horns in a desert thicket, a thin line of blood at its flank, the dominant subject; behind it the youth Isaac (from the reference) embraced by Abraham (from the reference) in soft shadow"),
 ("06_waiting", ["abraham","isaac"], "Abraham (from the reference) descending a mountain at dusk, the youth Isaac (from the reference) walking ahead into the valley; Abraham pausing to look back up at the bare dark summit, one empty open hand at his side; amber dusk"),
]
for slug, cast, subj in SCENES:
    png = OUT/f"{slug}.png"
    if png.exists(): print(f"[skip] {slug}"); continue
    print(f"[scene] {slug} refs={cast} ...", flush=True); t=time.time()
    png.write_bytes(hf_image(scene_prompt(subj), [refs[c] for c in cast]))
    print(f"[scene] {png}  ({time.time()-t:.0f}s)")
print("\nDONE -> _reflock_test/")
