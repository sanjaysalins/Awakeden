"""Style x identity-lock bake-off -- 35 catalogued style variants (15 from
STYLE_VARIANTS.md + 20 from STYLE_LAB.md) + 1 plain baseline, all rendered
against ONE fixed Moses control scene chained to the repo cast anchor
(cast/moses_ref.png), so results are apples-to-apples on two questions at
once (per .claude/skills/living-sketchbook/STYLE_SELECTION.md Phase 0):
  (a) does the technique look handmade and alive (STYLE_LAB's own test)
  (b) does it survive character identity-lock (untested until now -- every
      variant so far was only demonstrated on a generic manna-crowd or
      unnamed-traveler scene, never a named ref-chained character)

Mechanism: both markdown files are the single source of truth for the
prompt text (no hand-retyped copies here) -- this script PARSES the
```text ... ``` / ``` ... ``` fenced blocks straight out of each file,
splits each on its first "SCENE:" or "SUBJECT:" marker to isolate the
reusable STYLE/technique prefix, discards the original demo scene, and
appends the SAME Moses control scene to all 36.

Budget: user-authorized 100cr ceiling. 36 renders x 2cr (nano_banana_pro)
= 72cr, leaving ~28cr margin for retries. Idempotent (skip existing files)
-- safe to re-run after a partial batch.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_style_identity_bakeoff/_run_bakeoff.py --list   (dry run, no spend)
  .venv\\Scripts\\python.exe poc_living_sketchbook/_style_identity_bakeoff/_run_bakeoff.py --only baseline,01_kinetic_storm_focus   (test-gate)
  .venv\\Scripts\\python.exe poc_living_sketchbook/_style_identity_bakeoff/_run_bakeoff.py    (full batch)
"""
import re
import subprocess
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
EPISODE = "LS_StyleIdentityBakeoff"
HERE = Path(__file__).resolve().parent
CAST = HERE.parent / "cast"

MOSES_REF = CAST / "moses_ref.png"
JESUS_REF = CAST / "jesus_ref.png"

SKILL_DIR = ROOT / ".claude" / "skills" / "living-sketchbook"
STYLE_VARIANTS_MD = SKILL_DIR / "STYLE_VARIANTS.md"
STYLE_LAB_MD = SKILL_DIR / "STYLE_LAB.md"

# Same MOSES canon text as bronze_serpent_long/_s2_stills.py (verbatim,
# age-corrected 2026-08-01) and the same FULLBLEED framing note, so this
# bake-off's baseline is directly comparable to real production renders.
MOSES = (
    "Moses: an elderly Hebrew man of about 120 years, at the very end of "
    "his life -- the aged lawgiver of Numbers, NOT the young Moses of the "
    "Exodus/burning-bush years -- his eye not dim, his natural force not "
    "abated (Deuteronomy 34:7), so drawn upright and vital despite his "
    "extreme age, never frail or feeble -- a broad weathered forehead, "
    "deep-set eyes beneath heavy grey brows, hollowed cheeks, a strong jaw "
    "beneath the beard, long white and grey hair swept back off the "
    "forehead and thinning at the crown, a long full white beard streaked "
    "with iron-grey reaching mid-chest, deeply sun-weathered leathery "
    "skin, an old man's spare sinewed frame -- still upright and "
    "strong-shouldered, never frail or youthful -- dark steady eyes "
    "weighted with authority and grief, large veined elder's hands, a "
    "plain undyed woolen robe with a coarse mantle draped over one "
    "shoulder, a woven cord girdle, plain leather sandals, always holding "
    "or beside a tall wooden staff worn smooth by decades of use. the SAME "
    "man as the reference image -- identical face, beard, hair, and "
    "clothing."
)
FULLBLEED = (
    "CRITICAL FRAMING: zoom in close enough that the illustrated subject "
    "and its immediate surroundings occupy the ENTIRE frame, corner to "
    "corner. There must be NO large empty cream-paper or kraft-paper "
    "region anywhere inside the frame, and no blank kraft-paper rectangle "
    "or sticky-note patch used as filler -- the torn-edge collage texture "
    "is only a narrow border treatment along the outermost margin, never a "
    "wide blank zone."
)
# Fixed control scene, reused verbatim across all 36 renders -- matches
# bronze_serpent_long spread s35's own composition (close, intimate,
# direct-address) so results are comparable to a real production spread.
MOSES_SCENE = (
    f"A close, intimate mid-shot: {MOSES}'s face turned directly toward "
    f"the viewer, his expression open and searching, about to speak "
    f"plainly, staff loosely at his side. {FULLBLEED}"
)

# JESUS text -- reused VERBATIM from bronze_serpent_long/_s2_stills.py.
JESUS = (
    "Jesus: a Judean man in his early thirties, long dark wavy hair past "
    "the shoulders parted center, short close-cropped dark beard, a "
    "strong straight nose and defined cheekbones, warm deep brown eyes "
    "level and calm, sun-weathered olive skin, lean wiry-strong build, "
    "simple undyed homespun ankle-length tunic with a woven cord sash, "
    "leather sandals. the SAME man as the reference image -- identical "
    "face, beard, hair, and clothing."
)
# Deliberately a PLAIN, non-glory scene (no radiant light, no gold) so this
# test doesn't entangle the separate "gold = His glory only" palette rule
# with the identity-lock question -- keeps this comparable to Moses's own
# plain control scene, same register, same crop, same distance.
JESUS_SCENE = (
    f"A close, intimate mid-shot: {JESUS}'s face turned directly toward "
    f"the viewer, His expression calm and warm, an ordinary teaching "
    f"moment -- no dramatic lighting, no glow, no glory register. "
    f"{FULLBLEED}"
)

CHARACTERS = {
    "moses": {"ref": MOSES_REF, "scene": MOSES_SCENE, "out": "stills"},
    "jesus": {"ref": JESUS_REF, "scene": JESUS_SCENE, "out": "stills_jesus"},
}

BASELINE_STYLE = (
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


def _split_marker(text):
    """Return the text BEFORE the first 'SCENE:' or 'SUBJECT:' marker
    (whichever appears first), i.e. the reusable style/technique prefix."""
    idxs = [i for i in (text.find("SCENE:"), text.find("SUBJECT:")) if i != -1]
    if not idxs:
        return text.strip()
    return text[:min(idxs)].strip()


def parse_style_variants(path):
    """STYLE_VARIANTS.md: '## N. Name' headers, ```text fenced blocks."""
    content = path.read_text(encoding="utf-8")
    out = []
    chunks = re.split(r"\n## (?=\d+\. )", content)
    for chunk in chunks[1:]:
        m = re.match(r"(\d+)\.\s+([^\n]+)", chunk)
        if not m:
            continue
        num, name = int(m.group(1)), m.group(2).strip()
        block = re.search(r"```text\n(.*?)\n```", chunk, re.S)
        if not block:
            continue
        prefix = _split_marker(block.group(1))
        slug = re.sub(r"[^a-z0-9]+", "_", name.split("⚠")[0].lower()).strip("_")
        out.append((f"sv{num:02d}_{slug}", name, prefix, "STYLE_VARIANTS.md"))
    return out


def parse_style_lab(path):
    """STYLE_LAB.md: '## NN — Name' headers, plain ``` fenced blocks."""
    content = path.read_text(encoding="utf-8")
    out = []
    chunks = re.split(r"\n## (?=\d\d\s+—)", content)
    for chunk in chunks[1:]:
        m = re.match(r"(\d\d)\s+—\s+([^\n]+)", chunk)
        if not m:
            continue
        num, name = int(m.group(1)), m.group(2).strip()
        block = re.search(r"```\n(.*?)\n```", chunk, re.S)
        if not block:
            continue
        prefix = _split_marker(block.group(1))
        slug = re.sub(r"[^a-z0-9]+", "_", name.split("⚠")[0].lower()).strip("_")
        out.append((f"sl{num:02d}_{slug}", name, prefix, "STYLE_LAB.md"))
    return out


def build_jobs():
    jobs = [("baseline", "Baseline (plain frozen style)", BASELINE_STYLE, "SKILL.md")]
    jobs += parse_style_variants(STYLE_VARIANTS_MD)
    jobs += parse_style_lab(STYLE_LAB_MD)
    return jobs


def run(prompt, out, ref):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt,
           "--aspect_ratio", "9:16", "--resolution", "2k", "--wait",
           "--image", str(ref)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-250:]}")
        return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    args = sys.argv[1:]
    jobs = build_jobs()

    if "--list" in args:
        print(f"{len(jobs)} jobs parsed:\n")
        for slug, name, prefix, src in jobs:
            print(f"[{slug}] {name}  ({src}, {len(prefix)} chars)")
            print(f"    {prefix[:100]}...")
        return

    char = "moses"
    if "--character" in args:
        char = args[args.index("--character") + 1]
    cfg = CHARACTERS[char]
    ref, scene = cfg["ref"], cfg["scene"]
    out_dir = HERE / cfg["out"]
    out_dir.mkdir(parents=True, exist_ok=True)

    only = None
    if "--only" in args:
        only = set(args[args.index("--only") + 1].split(","))
        jobs = [j for j in jobs if j[0] in only]

    if not ref.exists():
        print(f"FAILED -- missing {ref}, run its cast anchor script first")
        return

    for slug, name, style_prefix, src in jobs:
        out = out_dir / f"{slug}.png"
        if out.exists():
            print(f"[skip] {slug}")
            continue
        prompt = style_prefix + "\n\nSCENE: " + scene
        print(f"[img] {slug} ({name}) ...", flush=True)
        ok = run(prompt, out, ref)
        if not ok:
            time.sleep(5)
            ok = run(prompt, out, ref)
        if ok:
            try:
                cost.record_hf(EPISODE, "poc", "stills", MODEL, note=f"[stylebakeoff:{char}] {slug} ({name})")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")
    print(f"[out] {out_dir}")


if __name__ == "__main__":
    main()
