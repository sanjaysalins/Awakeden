"""Look and Live (Bronze Serpent short #1, Numbers 21:8-9) -- step 1: 13
spreads, 9:16. No named human cast (the LORD is never shown as a human
figure; this narration never names Moses -- see _PLAN.md). The bronze
serpent is a NEW object this episode, no reusable anchor exists (checked --
world/SERPENT.md is the unrelated Eden tempter-serpent, wrong doctrine/
palette entirely). Locked object doctrine: plain bronze/copper, NEVER gold
(gold = Christ's glory alone, Round 9 PASS-verified precedent). s02 is the
approved reference (kling_omni_image, 0.5cr/still, user-approved 2026-08-12
after 2 rounds of fixes: no cobra hood, no gold collar) -- chained as the
reference for every later appearance.

nano_banana_pro was tried first and failed twice (server-side, no result --
see _TEST_REVIEW.html). kling_omni_image is the model in use for this
episode; NOT yet validated against this project's OTHER sketchbook episodes,
scoped to this short only.

Run all (idempotent, skips existing):
  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_s1_stills.py
Run specific shots only (e.g. the test batch):
  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_s1_stills.py s02 s12a
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
MODEL = "kling_omni_image"
EPISODE = "LS_LookAndLive"
HERE = Path(__file__).resolve().parent
OUT = HERE / "stills"
OUT.mkdir(parents=True, exist_ok=True)

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

SERPENT = (
    "a slender serpent figure cast in dull weathered bronze and dark copper, "
    "patina-green in places, its head slender and no wider than its own "
    "neck, the same plain worn metal continuing unbroken from head to tail "
    "with no different-colored band or collar anywhere -- fixed lengthwise "
    "to a plain rough wooden pole planted upright in the ground."
)

# (name, refs, chain_from, scene)
SHOTS = [
    ("s01_hook", [], None,
     "WIDE establishing shot, eye-level: a dusk wilderness camp in panic -- "
     "tents, dust, torn cloth, small serpents moving among the ground near "
     "people's feet; several unnamed figures recoiling, silhouetted or "
     "turned away, no face closer than mid-distance; ochre dust haze, "
     "deep blue-wash evening shadow."),

    ("s02_object_reveal", [], None,
     f"LOW ANGLE, looking steeply up: {SERPENT} standing alone against a "
     f"darkening sky, seen from below so it looms tall and still; no human "
     f"figure anywhere in frame; deep blue-wash dusk behind it, the pole's "
     f"base lost in shadow."),

    ("s03_unused_remedy", [], None,
     "CLOSE object-insert: a small scatter of discarded dried herbs, torn "
     "cloth bindings, and a cracked plain clay jar lying unused in pale "
     "dust, soft raking light, no figure, no hands."),

    ("s04_bitten_arm", [], None,
     "CLOSE, tasteful and non-graphic: a bound forearm wrapped in plain "
     "linen cloth, a small dark bite mark just visible at the wrist, no "
     "blood, no gore, no face or other body part in frame, dust-colored "
     "ground below."),

    ("s05_eye_reflection", [], None,
     "EXTREME CLOSE-UP on a single unnamed Hebrew person's eye and brow "
     "only, ordinary and weathered, no other feature identifiable; a "
     "tiny distant glint of the bronze serpent reflected small in the "
     "iris; everything else soft-focus dark."),

    ("s06_verse_backdrop", [], None,
     "WIDE: a knot of weary unnamed elders and travelers gathered on "
     "cracked dry wilderness ground, gesturing and arguing among "
     "themselves, one figure pointing back the way they came; harsh "
     "distant mountains on the horizon, generous still empty sky above "
     "for lettering; ochre dust haze, hard midday light."),

    ("s07_look_and_live_acting", [], None,
     "A single unnamed bitten figure collapsed low in the dust, robed, "
     "face and body turned away at first -- captured at the exact moment "
     "their head begins to lift and turn upward toward an unseen point "
     "off-frame; the ground around them still in cool blue-wash shadow, "
     "but a warm light begins to touch the side of their face and "
     "shoulder as they look up; low camera angle, close, intimate."),

    ("s08_crowd_healing", [], "s02_object_reveal",
     "GROUND LEVEL, camera low among the crowd looking up and past "
     "several unnamed robed Hebrew figures' heads and shoulders in the "
     "foreground, all in plain undyed wilderness robes and headcloths, "
     "no modern clothing of any kind: THE SAME bronze serpent-on-pole "
     "as the reference image rising beyond them in the middle distance, "
     "figures turning to look up toward it, one already recovered and "
     "standing straighter; a faint warm glow touching the nearer faces; "
     "deep blue-wash shadow at the frame's edges. A very different "
     "framing from a tall vertical portrait of the pole -- intimate, "
     "crowded, seen from within the camp rather than facing the pole "
     "head-on."),

    ("s09_atmosphere_dawn", [], None,
     "An unnamed elderly man kneels alone on bare wilderness ground, "
     "head bowed and one hand raised in prayer, seen from behind and to "
     "the side; harsh cracked earth, pale dawn light just beginning to "
     "break over distant mountains, the resting camp small and quiet far "
     "in the background; generous still empty paper, a transitional "
     "hush, no other figures nearby."),

    ("s10_own_cure", [], None,
     "CLOSE on a pair of hands reaching for and gathering a small "
     "personal herb-pouch and cloth wrap in the dust; nothing else in "
     "frame, plain out-of-focus dusty ground filling the background; "
     "warm foreground light."),

    ("s11_plain_sight", [], "s02_object_reveal",
     "A wide dusk camp of tents in rows, several unnamed robed figures "
     "going about ordinary tasks -- walking between tents, tending a "
     "small cooking-fire, folding cloth -- with THE SAME bronze "
     "serpent-on-pole as the reference image standing at the edge of "
     "the scene, smaller than the tents nearest it, plainly visible but "
     "not the center of anyone's attention; soft even daylight, warm "
     "ochre tones."),

    ("s12a_torn_to_gold", [], "s02_object_reveal",
     "A landing-device spread: a ragged HOLE physically torn straight "
     "through the aged paper itself, at the center of the page, in the "
     "exact silhouette shape of the serpent-and-pole from the reference "
     "image -- this is a TEAR IN THE PAPER, not a painted or drawn shape "
     "-- the torn paper's rough deckled fibrous edges are clearly visible "
     "all around the rim of the hole, catching the light unevenly; "
     "radiant warm gold light pours out through the torn opening from "
     "behind the page, brightest at the hole's center, illuminating the "
     "torn paper edges from behind; everywhere OUTSIDE the hole remains "
     "ordinary aged cream paper with its normal texture, completely "
     "unlit and unchanged; a thin gold leaf strip at one page edge."),

    ("s12b_landing_gold",
     [ROOT / "poc_living_sketchbook" / "cast" / "jesus_ref.png"],
     "s12a_torn_to_gold",
     "Through the SAME torn paper opening as the reference image, same "
     "shape and same ragged fibrous torn edges: Christ hangs lifted up "
     "on a plain wooden cross, seen from a respectful distance, arms "
     "extended along the crossbeam, head bowed, reverent, no visible "
     "wounds, no blood -- the SAME man as the other reference image, "
     "identical face, beard, and hair -- His whole figure filling the "
     "opening, radiant warm gold light surrounding Him. Small and dark "
     "in the immediate foreground below the tear, the plain bronze "
     "serpent-on-pole sits earthbound and unlit, dull metal in shadow, "
     "clearly smaller and lower than the radiant figure above. "
     "Everywhere outside the tear stays plain aged cream paper, "
     "untouched. Utterly still and quiet, sacred stillness."),
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
    only = set(sys.argv[1:]) or None
    for name, refs, chain, scene in SHOTS:
        if only and name not in only:
            continue
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
                cost.record_hf(EPISODE, "short", "stills", MODEL, note=f"[look-and-live] {name}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
