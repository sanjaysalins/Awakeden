"""Door episode sketch POC — step 1: cast-bible anchors for THIS style family.
Canon TEXT is shared with the painted-comic pieces; the anchor PNG is per-style
(a sketch anchor for sketch renders — cross-style anchors drag style in).
Writes cast/SEEKER.md + cast/JESUS.md + renders the two anchor portraits.

  .venv\\Scripts\\python.exe poc_castbible_look/episode_door/_e1_anchors.py
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
CAST = Path(__file__).resolve().parent / "cast"
CAST.mkdir(parents=True, exist_ok=True)

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

SEEKER_CANON = (
    "The Seeker: a weary grey-haired traveler -- short greying hair and a "
    "lined, weathered face with tired deep-set eyes; a loose undyed woolen "
    "mantle draped over his head, ankle-length undyed tunic with a simple "
    "cord girdle, leather thong sandals; large work-worn hands; a rolled "
    "parchment scroll clutched close to his chest."
)
JESUS_CANON = (
    "Jesus: long dark wavy hair, short dark beard, calm certain welcoming "
    "face with warm deep eyes; simple undyed homespun ankle-length tunic "
    "with a woven cord sash, leather sandals."
)

SHEETS = {
    "SEEKER.md": f"""# SEEKER — cast canon sheet (sketch-style family)

Created 2026-07-28 for the Door-episode sketch POC. Canon text shared with the
Gold Seam pieces (same figure); THIS anchor is the sketch-style family anchor.
Anchor: `cast/seeker_sketch_ref.png` — a regenerated portrait is a DIFFERENT
face, never lose the anchor.

## Canon description (paste VERBATIM into every prompt that shows the Seeker)

> {SEEKER_CANON}

## Usage
Chain the anchor via --image + append: "the SAME man as the reference image --
identical face, hair, and clothing."
""",
    "JESUS.md": f"""# JESUS — cast canon sheet (sketch-style family)

Created 2026-07-28 for the Door-episode sketch POC. Canon text matches the
series' standing description; THIS anchor is the sketch-style family anchor.
Anchor: `cast/jesus_sketch_ref.png` — a regenerated portrait is a DIFFERENT
face, never lose the anchor. Fail-closed eye-QC on every Jesus frame.

## Canon description (paste VERBATIM into every prompt that shows Jesus)

> {JESUS_CANON}

## Usage
Chain the anchor via --image + append: "the SAME man as the reference image --
identical face, beard, hair, and clothing."
""",
}

ANCHORS = [
    ("seeker_sketch_ref", SEEKER_CANON,
     "Close editorial portrait, head and shoulders, three-quarter view, tired "
     "quiet longing in the face, plain aged-paper backdrop."),
    ("jesus_sketch_ref", JESUS_CANON,
     "Close editorial portrait, head and shoulders, three-quarter view, calm "
     "open welcome in the face, warm light from one side, plain aged-paper "
     "backdrop."),
]


def run(prompt, out):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt,
           "--aspect_ratio", "1:1", "--resolution", "2k", "--wait"]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-250:]}")
        return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    for fn, text in SHEETS.items():
        (CAST / fn).write_text(text, encoding="utf-8")
        print(f"[sheet] {fn}")
    for name, canon, framing in ANCHORS:
        out = CAST / f"{name}.png"
        if out.exists():
            print(f"[skip] {name}")
            continue
        prompt = STYLE + "\n\nSCENE: " + canon + " " + framing
        print(f"[anchor] {name} ...", flush=True)
        ok = run(prompt, out)
        if not ok:
            time.sleep(5)
            ok = run(prompt, out)
        if ok:
            try:
                cost.record_hf(EPISODE, "short", "cast_anchor", MODEL, note=f"[door-sketch] {name}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")


if __name__ == "__main__":
    main()
