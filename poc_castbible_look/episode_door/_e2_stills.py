"""Door episode sketch POC — step 2: 12 spreads, 9:16, canon + anchors chained.

  .venv\\Scripts\\python.exe poc_castbible_look/episode_door/_e2_stills.py
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
EPISODE = "POC_Door_Sketch"
HERE = Path(__file__).resolve().parent
CAST = HERE / "cast"
OUT = HERE / "stills"
OUT.mkdir(parents=True, exist_ok=True)

SEEKER_REF = CAST / "seeker_sketch_ref.png"
JESUS_REF = CAST / "jesus_sketch_ref.png"

SEEKER = (
    "The Seeker: a weary grey-haired traveler -- short greying hair and a "
    "lined, weathered face with tired deep-set eyes; a loose undyed woolen "
    "mantle draped over his head, ankle-length undyed tunic with a simple "
    "cord girdle, leather thong sandals; large work-worn hands; a rolled "
    "parchment scroll clutched close to his chest. the SAME man as the "
    "reference image -- identical face, hair, and clothing."
)
JESUS = (
    "Jesus: long dark wavy hair, short dark beard, calm certain welcoming "
    "face with warm deep eyes; simple undyed homespun ankle-length tunic "
    "with a woven cord sash, leather sandals. the SAME man as the reference "
    "image -- identical face, beard, hair, and clothing."
)
DOOR = ("a great arch-topped door of plain bare wood planks set deep in an "
        "ancient stone wall, closed with a simple wooden bar-latch")
DOOR_OPEN = ("the great arch-topped plain plank door standing wide open, its "
             "wooden bar-latch hanging free")
LAMP = "a small terracotta saucer oil lamp with a low steady flame in a wall niche"

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

# (name, refs, scene)
SHOTS = [
    ("d01_hook", [SEEKER_REF],
     f"Seen from above at night: {SEEKER} He stands small and alone before "
     f"{DOOR}, warm gold light bleeding under the door and from {LAMP}, his "
     f"long shadow across worn flagstones; deep blue-black ink-wash night "
     f"around the pool of light."),

    ("d02_record", [SEEKER_REF],
     f"Close over-the-shoulder: the weathered hands of {SEEKER} clutching the "
     f"rolled parchment scroll to his chest, the massive plank edge of "
     f"{DOOR} looming close in soft shadow, a warm thread of light along the "
     f"door's bottom gap."),

    ("d03_rehearsing", [SEEKER_REF],
     f"{SEEKER} stands at the lamp niche, head lowered, one bare hand "
     f"half-raised as if practicing a plea, the scroll in the other; the "
     f"low flame of {LAMP} rims his mantle edge in warm light against the "
     f"cold blue ink-wash night."),

    ("d04_answered", [],
     f"{DOOR[0].upper()}{DOOR[1:]} now standing AJAR, a widening blade of "
     f"warm gold light breaking through the gap and across worn flagstones "
     f"toward the camera, the cold blue night pushed back at the edges."),

    ("d05_hiswords", [JESUS_REF],
     f"Close editorial portrait: {JESUS} His face calm and mid-speech, warm "
     f"gold light from one side against deep blue-wash shadow."),

    ("d06_verse", [JESUS_REF],
     f"{JESUS} He stands in the open arched doorway, one hand extended "
     f"outward in open welcome, radiant warm gold light flooding past him -- "
     f"the light rendered as REAL GOLD LEAF pressed onto the paper -- worn "
     f"flagstones catching the glow in front of him."),

    ("d07_exception", [SEEKER_REF],
     f"{SEEKER} half-turned away from the door, head bowed, the scroll "
     f"hanging heavy in one hand at his side; cold blue-wash shadow over "
     f"him; behind him the door's warm light-line still glows, low and "
     f"patient; a few drifted leaves on the flagstones."),

    ("d08_toofargone", [],
     "A stark spread: a worn parchment scroll lying UNROLLED across the "
     "paper, blank stained parchment, blotched and travel-worn, its edges "
     "curling; dark blue-black ink wash pooling and creeping in from the "
     "spread's corners toward it."),

    ("d09_nailed", [],
     "Close on a rough hewn wooden beam against a torn-paper sky: a rolled "
     "parchment scroll fixed to the wood by a single iron nail driven "
     "through it, the parchment edges curling, quiet and final; a faint "
     "warm glow behind the beam, gold leaf at the spread's edge."),

    ("d10_opendoor", [],
     f"{DOOR_OPEN[0].upper()}{DOOR_OPEN[1:]}, radiant warm gold light "
     f"flooding out of the doorway across worn flagstones toward the "
     f"camera, dust hanging in the light beam, the cold blue night peeled "
     f"back around the glow."),

    ("d11_welcome", [JESUS_REF, SEEKER_REF],
     f"At the open threshold, warm gold light surrounding them: {JESUS} He "
     f"lays one hand on the shoulder of {SEEKER} whose head is lifting, the "
     f"scroll hanging loose and released at his side. Exactly TWO people in "
     f"the frame, both figures full and clear."),

    ("d12_landing", [],
     "A wide quiet spread: an arched doorway rendered as a TORN HOLE in the "
     "aged paper itself, radiant warm gold light glowing from beneath the "
     "page through the tear; on the sketched flagstones before it lies a "
     "released rolled scroll, connected to the glowing doorway by a fine "
     "thread of real gold; generous still paper space around, a small "
     "sketched dove aloft near the top corner."),
]


def run(prompt, out, refs):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt,
           "--aspect_ratio", "9:16", "--resolution", "2k", "--wait"]
    for r in refs:
        cmd += ["--image", str(r)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-250:]}")
        return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    for name, refs, scene in SHOTS:
        out = OUT / f"{name}.png"
        if out.exists():
            print(f"[skip] {name}")
            continue
        prompt = STYLE + "\n\nSCENE: " + scene
        print(f"[img] {name} (refs={len(refs)}) ...", flush=True)
        ok = run(prompt, out, refs)
        if not ok:
            time.sleep(5)
            ok = run(prompt, out, refs)
        if ok:
            try:
                cost.record_hf(EPISODE, "short", "stills", MODEL, note=f"[door-sketch] {name}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
