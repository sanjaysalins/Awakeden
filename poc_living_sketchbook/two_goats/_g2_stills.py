"""Two Goats — step 2: 14 spreads, 9:16. Veil-tear stages image-chain
(multi-stage hard-cut rule). Jesus reuses the Door episode's own anchor
($0, same style family).

  .venv\\Scripts\\python.exe poc_living_sketchbook/two_goats/_g2_stills.py
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
EPISODE = "LS_TwoGoats"
HERE = Path(__file__).resolve().parent
CAST = HERE / "cast"
OUT = HERE / "stills"
OUT.mkdir(parents=True, exist_ok=True)

PRIEST_REF = CAST / "priest_sketch_ref.png"
JESUS_REF = (ROOT / "poc_castbible_look" / "episode_door" / "cast" / "jesus_sketch_ref.png")

PRIEST = (
    "The Priest: an aging Hebrew man in his sixties -- deep-set solemn eyes, "
    "a long grey beard, a weathered careworn face; dressed ENTIRELY in plain "
    "undyed white linen for the Day of Atonement -- a plain linen coat, "
    "linen breeches, a linen girdle, a linen turban -- no gold, no jewels, "
    "no embroidered breastplate of any kind; bare feet. the SAME man as the "
    "reference image -- identical face, hair, and clothing."
)
JESUS = (
    "Jesus: long dark wavy hair, short dark beard, calm certain welcoming "
    "face with warm deep eyes; simple undyed homespun ankle-length tunic "
    "with a woven cord sash, leather sandals. the SAME man as the reference "
    "image -- identical face, beard, hair, and clothing."
)
VEIL = ("a massive heavy woven curtain of blue, purple, and scarlet thread "
        "hanging floor to ceiling across a stone sanctuary doorway, its "
        "surface worked with cherubim")

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

# (name, refs, chain_from, scene)
SHOTS = [
    ("g01_hook", [PRIEST_REF], None,
     f"{PRIEST} He stands alone facing {VEIL}, seen from behind and slightly "
     f"to the side, in a dim stone sanctuary lit by one small oil lamp; his "
     f"posture braced, uncertain, small before the great hanging curtain."),

    ("g02_bloodgoat", [PRIEST_REF], None,
     f"{PRIEST} Close on his weathered hands, stained dark with fresh blood, "
     f"drawing {VEIL} aside just enough to pass through; beyond the gap, deep "
     f"shadow within the sanctuary. A dead goat lies in soft shadow at the "
     f"edge of the frame, foreground, out of focus."),

    ("g03_scapegoat", [PRIEST_REF], None,
     f"{PRIEST} He kneels with both hands pressed on the head of a living "
     f"goat, head bowed over it in solemn confession, in an open courtyard "
     f"under a wide pale sky; the goat calm, standing, unharmed."),

    ("g04_intodesert", [], None,
     "A lone goat, seen small and distant, walking away alone across a vast "
     "empty desert wilderness under a wide bleached sky, its trail of "
     "footprints receding behind it; utterly alone, no herder, no path, no "
     "other creature in sight."),

    ("g05_onepay_onecarry", [], None,
     "A quiet symbolic spread: two goats faced in profile toward each other "
     "across the center of the page, one dark-marked and still at left, one "
     "pale and walking at right, a thin hand-drawn dividing line down the "
     "page between them; generous still paper, a faint gold thread "
     "connecting the two."),

    ("g06_yearsasked", [PRIEST_REF], None,
     f"{PRIEST} Close portrait, seated alone in dim lamplight within the "
     f"sanctuary, his face turned down in long unresolved thought, hands "
     f"loosely folded; years of quiet unanswered waiting in his eyes."),

    ("g07_bothhalves", [], None,
     "A stark spread: a single scarlet thread splits into two separate "
     "threads partway across the page, one thread ending at a small drawn "
     "altar, the other trailing off toward a faint sketched horizon; deep "
     "blue-wash shadow around them, generous still paper."),

    ("g08_jesuspivot", [JESUS_REF], None,
     f"{JESUS} He matches the reference image EXACTLY, with no drift at all: "
     f"the SAME full dark wavy/curly shoulder-length hair (not straight, not "
     f"short), the SAME full dark beard covering his jaw and chin (not a "
     f"thin shadow, not a light stubble), the SAME warm olive skin tone "
     f"(not lighter, not golden-tan). He stands facing the camera in warm "
     f"radiant gold light breaking through deep blue-wash shadow, arms "
     f"slightly open, His face calm and certain; the gold seam of light "
     f"burning along His edge, filling the frame with quiet weight."),

    ("g09_isaiah536", [], None,
     "A stark quiet editorial spread: a single scarlet thread laid across "
     "blank aged cream paper in one confident curved stroke, a thin gold "
     "leaf strip at the page edge, generous still empty space, faint "
     "engineering hairlines."),

    ("g10_finished", [JESUS_REF], None,
     f"{JESUS} Seen from behind and to the side, He sits at rest on a plain "
     f"stone ledge within a radiant doorway of warm gold light, His posture "
     f"utterly at peace, head slightly bowed; deep blue-wash shadow beyond "
     f"the light."),

    ("g11_veil_whole", [], None,
     f"{VEIL[0].upper()}{VEIL[1:]}, hanging whole and unbroken floor to "
     f"ceiling across the stone sanctuary doorway, still and undisturbed, "
     f"seen straight on, dim even lamplight."),

    ("g12_veil_tearing", [], "g11_veil_whole",
     f"THE SAME curtain as the reference image, same framing, same stone "
     f"doorway -- but now frozen at the instant of tearing: a jagged split "
     f"running down its full height, the woven blue-purple-scarlet fabric "
     f"peeling apart at the tear's edges, threads fraying outward in ink "
     f"linework, a sudden shaft of warm light breaking through the gap."),

    ("g13_veil_torn", [], "g12_veil_tearing",
     f"THE SAME view as the reference image, same framing -- the curtain "
     f"now fully torn in two from top to bottom, both halves hanging apart, "
     f"radiant warm gold light flooding through the wide gap between them "
     f"into the dim sanctuary, the torn threads still visible on both "
     f"ragged edges."),

    ("g14_landing", [], None,
     "A wide quiet landing spread: the torn curtain rendered as a TORN HOLE "
     "in the aged paper itself, radiant warm gold light glowing from "
     "beneath the page through the tear, the two ragged curtain-halves "
     "sketched faintly at the tear's edges; a fine scarlet thread runs "
     "across the paper and disappears into the torn opening; generous "
     "still paper space around, a thin gold leaf strip at the edge."),
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
    assert PRIEST_REF.exists(), f"missing {PRIEST_REF}"
    assert JESUS_REF.exists(), f"missing {JESUS_REF}"
    for name, refs, chain, scene in SHOTS:
        out = OUT / f"{name}.png"
        if out.exists():
            print(f"[skip] {name}")
            continue
        use_refs = list(refs)
        if chain:
            src = OUT / f"{chain}.png"
            if not src.exists():
                print(f"[HOLD] {name}: chain source {chain} missing")
                continue
            use_refs.append(src)
        prompt = STYLE + "\n\nSCENE: " + scene
        print(f"[img] {name} (refs={len(use_refs)}) ...", flush=True)
        ok = run(prompt, out, use_refs)
        if not ok:
            time.sleep(5)
            ok = run(prompt, out, use_refs)
        if ok:
            try:
                cost.record_hf(EPISODE, "short", "stills", MODEL, note=f"[two-goats] {name}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
