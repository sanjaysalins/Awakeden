"""Even So Must the Son of Man Be Lifted Up (Bronze Serpent short #3, John
3:14-15) -- step 1: 13 spreads, 9:16. Jesus/Moses REUSED from the repo-level
cast anchors; the bronze serpent object chains from Look and Live's own
approved reference (same chain God Hung Up a Snake already used -- this is
the 3rd short in the cluster on the same design). Nicodemus is NEW -- no
prior anchor -- so s01 (his first appearance) becomes his own in-episode
reference for every later spread (same "first approved render = the
reference, no separate anchor-only spend" practice the serpent object
itself used in short #1). See _PLAN.md's reuse section and NICODEMUS.md.

kling_omni_image is the proven cheap default for this cluster (0.5cr);
seedream_v4_5 for the compositionally complex shots (s05's memory-bleed,
s10's crowd) -- same split god Hung Up a Snake used for its own landing
pair.

**s03/s08/s11/s13 (the 4 Jesus-alone face/hero shots) are sourced from NBP
instead** (`_nbp_test.py`, direct Google `gemini-3-pro-image-preview`,
~$0.50/still, Google-billed separately from the HF ledger) -- a real
side-by-side test confirmed noticeably better anatomy/composition on all 4
vs. this script's own kling/seedream output, per the user's own instinct
that NBP does especially well on Christ-alone shots (matches this project's
locked NBP-for-Christ/face precedent). This script's own SHOTS entries for
those 4 are left as-is for the record/fallback, but since the PNGs already
exist at their canonical paths, a plain re-run of this script will skip
them (idempotent) rather than overwrite the NBP renders -- use --regen-style
args or delete the file first if a genuine re-roll on kling/seedream is
ever wanted instead.

Run all (idempotent, skips existing):
  .venv\\Scripts\\python.exe poc_living_sketchbook/son_of_man_lifted_up/_s1_stills.py
Run specific shots only (e.g. a test batch):
  .venv\\Scripts\\python.exe poc_living_sketchbook/son_of_man_lifted_up/_s1_stills.py s01_hook s08_cross_hero
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
EPISODE = "LS_SonOfManLiftedUp"
HERE = Path(__file__).resolve().parent
OUT = HERE / "stills"
OUT.mkdir(parents=True, exist_ok=True)

LYL_SERPENT_REF = (ROOT / "poc_living_sketchbook" / "look_and_live" / "stills" /
                    "s02_object_reveal.png")
MOSES_REF = ROOT / "poc_living_sketchbook" / "cast" / "moses_ref.png"
JESUS_REF = ROOT / "poc_living_sketchbook" / "cast" / "jesus_ref.png"
NICODEMUS_REF = OUT / "s01_hook.png"  # this episode's own first render

STYLE = (
    "Editorial documentary sketch illustration: loose confident graphite-and-ink "
    "linework with muted watercolor wash, drawn on aged warm cream paper. "
    "Aged-print paper-collage aesthetic: warm cream and kraft textured stock, "
    "torn and cut-paper edges, subtle offset-halftone dot texture, faint "
    "engineering-grid hairlines, soft raking museum light, tactile hand-made "
    "feel, muted ink-red and ink-blue accents, a thin strip of gold leaf at one "
    "edge."
)

JESUS = (
    "Jesus: a Judean man in his early thirties. Face geometry: a strong "
    "straight nose, defined cheekbones, a broad calm forehead, an angular "
    "jaw beneath the beard. Hair: long dark wavy hair falling past the "
    "shoulders, parted center. Beard: short, close-cropped, dark, well-kept. "
    "Skin: sun-weathered olive Mediterranean complexion. Build: lean and "
    "wiry-strong. Eyes: warm deep brown, level and calm. Garment: simple "
    "undyed homespun ankle-length tunic with a woven cord sash -- the same "
    "every appearance."
)

MOSES = (
    "Moses: an elderly Hebrew man of about 120 years, at the very end of his "
    "life -- his eye not dim, his natural force not abated, drawn upright and "
    "vital despite his extreme age, never frail or feeble. Broad weathered "
    "forehead, deep-set eyes beneath heavy grey brows, hollowed cheeks, a "
    "strong jaw beneath the beard. Long white and grey hair swept back. Long "
    "full beard, white streaked with iron-grey. Deeply sun-weathered leathery "
    "skin. Plain undyed woolen robe, a coarse mantle over one shoulder."
)

NICODEMUS = (
    "Nicodemus: an elderly Hebrew Pharisee and ruler, a man of real means. "
    "Face geometry: a weathered, careful face, deep-set eyes narrowed in "
    "calculation, a broad forehead. Hair: grey, thinning, mostly covered. "
    "Beard: neatly trimmed grey beard. Skin: olive Mediterranean complexion, "
    "lined with age. Build: an elder's frame, upright, dignified, not frail. "
    "Eyes: dark, guarded, watchful. Garment: fine dark robes marking his "
    "rank, a wound turban, a phylactery strap visible at the brow -- a "
    "devout, wealthy Pharisee's dress."
)
NICODEMUS_CHAIN = " THE SAME man as the reference image -- identical face, beard, and clothing."

# (name, refs, chain_from, model, scene)
SHOTS = [
    ("s01_hook", [], None, MODEL,
     f"{NICODEMUS} {JESUS} WIDE: a rooftop terrace in Jerusalem at night, "
     "Nicodemus and Jesus seated across from each other around a single "
     "small oil lamp, distant lamplit rooftops and a starlit sky beyond a "
     "low parapet wall, tense stillness, warm upward lamp-light on both "
     "faces."),

    ("s02_close_faces", [JESUS_REF], "s01_hook", MODEL,
     f"{JESUS} {NICODEMUS}{NICODEMUS_CHAIN} CLOSE, both faces: two grown "
     "men of the SAME adult height and the SAME build, seated at the SAME "
     "distance from camera facing each other -- their heads and shoulders "
     "must be drawn at the SAME scale in frame, neither man larger, "
     "wider, or closer than the other. The oil lamp between them, warm "
     "upward light on both, Nicodemus's guarded expression meeting "
     "Jesus's calm steady gaze."),

    ("s03_jesus_split_light", [JESUS_REF], None, MODEL,
     f"{JESUS} CLOSE portrait, cropped at the chest -- Jesus's head, face, "
     "and neck are drawn at natural, realistic adult human proportions "
     "relative to His shoulders and chest, the SAME head-to-shoulder scale "
     "as the reference image, NOT enlarged, NOT a close-up crop that makes "
     "the head read oversized. Dramatic CHIAROSCURO single-source "
     "lighting: an ordinary hand-sized oil lamp glows from frame-left "
     "only, sitting on a stone ledge at a normal small scale relative to "
     "Jesus (not miniature, not toy-sized) -- the LEFT half of Jesus's "
     "face is bright warm gold and the RIGHT half of his face is in deep, "
     "clearly darker shadow -- a stark, high-contrast half-lit/half-dark "
     "split down the center of his face, not an even wash of light, calm, "
     "direct, unflinching expression."),

    ("s04_ot_echo", [LYL_SERPENT_REF], None, MODEL,
     f"{STYLE} WIDE: a wilderness camp at dusk, THE SAME bronze "
     "serpent-on-pole as the reference image standing at the center -- "
     "identical design and coloring to the reference image. The whole "
     "scene, including sky and background, stays in the SAME loose "
     "hand-drawn graphite-and-ink-with-watercolor-wash illustration style "
     "as the reference and the rest of this style block -- never "
     "photorealistic, never a painted photo, never a different rendering "
     "technique for any part of the frame. Stricken Israelites on the "
     "sand around its base, several faces lifted upward toward it."),

    ("s05_acting_memory_bleed", [JESUS_REF, NICODEMUS_REF, LYL_SERPENT_REF],
     None, "seedream_v4_5",
     f"{JESUS} {NICODEMUS}{NICODEMUS_CHAIN} Jesus speaking on the rooftop "
     "terrace at night, leaning forward with quiet authority, Nicodemus "
     "listening across the lamp -- and faintly bleeding into the frame "
     "behind Jesus, like a half-transparent memory, THE SAME bronze "
     "serpent-on-pole as the second reference image standing in a "
     "wilderness haze, the two scenes overlapping in one composition, the "
     "rooftop staying the dominant, sharper layer."),

    ("s06_serpent_healed_gaze", [LYL_SERPENT_REF], None, MODEL,
     "WIDE-to-mid: THE SAME bronze serpent-on-pole as the reference image, "
     "and below it one Israelite man on his knees in the sand, his face "
     "lifted in wonder toward it, dusk light, the moment of healing held "
     "still."),

    ("s07_nicodemus_skeptic", [NICODEMUS_REF], "s01_hook", MODEL,
     f"{NICODEMUS}{NICODEMUS_CHAIN} CLOSE portrait, Nicodemus alone on the "
     "rooftop, no one else in frame, guarded and unconvinced, lips parted "
     "around an unfinished question, lamp-glow warming one side of his "
     "face while the other falls into shadow."),

    ("s08_cross_hero", [JESUS_REF], None, "seedream_v4_5",
     f"{JESUS} HERO, wide, LOW ANGLE looking steeply upward: Christ genuinely "
     "ELEVATED and lifted high on a tall plain wooden cross, His feet raised "
     "well off the ground and resting together on a small wooden footrest "
     "partway up the upright beam -- His whole body is clearly hoisted into "
     "the air above the hilltop, not standing on the ground in front of the "
     "cross. The cross stands tall enough that the crowd-level ground and "
     "rocky hilltop are visible far BELOW His feet, small in the distance. "
     "Arms outstretched along the crossbeam, head bowed in reverent "
     "stillness, against a darkening Golgotha sky, torn storm clouds "
     "gathering behind Him, no visible wounds, no blood, the whole tableau "
     "held as a single iconic near-still image."),

    ("s09_nailed_hand_insert", [], None, MODEL,
     "EXTREME CLOSE object-insert, viewed straight-on from directly in "
     "front of the crossbeam (frontal angle, camera facing the wood "
     "square-on): an open hand already lying completely flat and open "
     "against the wood, palm facing the viewer, fingers open, straight, "
     "and spread apart, not curled, not bent, not clenched, not forming "
     "any kind of fist or grip -- an already-still, already-resting open "
     "palm. Through the exact center of this open palm passes one large "
     "square-headed iron spike -- a real Roman crucifixion spike, thick "
     "and substantial, not a small thin carpentry nail -- lying flush and "
     "quiet against the skin, no sparks, no impact marks, no starburst, "
     "no radiating lines around it, just a plain solid metal spike "
     "already in place. The skin across the whole hand and wrist is "
     "smooth, healthy, ordinary Mediterranean skin tone, completely calm "
     "except where the spike passes through. Tasteful and non-graphic, "
     "soft raking light, plain bare wood grain around the hand, no other "
     "part of the body in frame."),

    ("s10_crowd_multivignette", [], None, MODEL,
     "MID shot, cropped from the waist up only -- no ground, no feet, no "
     "floor visible anywhere in frame. A small group of people standing "
     "close together, seen from behind and the side, all looking the same "
     "direction upward and off-frame: a Roman soldier in plain armor with "
     "arms crossed, a woman with her hood up and head bowed, several other "
     "calm bystanders in plain robes. Soft even daylight, a plain empty "
     "sky filling the upper half of the frame."),

    ("s11_christ_face_reverent", [JESUS_REF], None, MODEL,
     f"{JESUS} CLOSE portrait, Christ's face on the cross, head bowed, eyes "
     "closed, soft even light, reverent and still, no visible wounds, no "
     "blood."),

    ("s12_nicodemus_tomb_daylight", [NICODEMUS_REF], "s01_hook", MODEL,
     f"{NICODEMUS}{NICODEMUS_CHAIN} WIDE, ordinary daylight (not night): "
     "Nicodemus standing in the open at the entrance of a rock-hewn tomb, "
     "no longer hidden or hooded, a bundle of burial spices in his arms, "
     "other mourners nearby -- the same man from the earlier night scene, "
     "now moving openly in the light."),

    ("s13_landing_christ_glory", [JESUS_REF], None, "seedream_v4_5",
     f"{JESUS} LANDING, sacred stillness: Christ lifted up on the cross, "
     "seen from a respectful distance, arms extended along the crossbeam, "
     "head bowed, radiant warm gold light surrounding His whole figure, "
     "the sky behind Him breaking open with light, held as a single "
     "iconic image, no visible wounds, no blood."),
]


def run(prompt, out, refs, model=MODEL):
    cmd = [HF, "generate", "create", model, "--prompt", prompt,
           "--aspect_ratio", "9:16", "--wait"]
    cmd += ["--quality", "high"] if model == "seedream_v4_5" else ["--resolution", "2k"]
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
    for name, refs, chain, model, scene in SHOTS:
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
            if src not in use_refs:
                use_refs.append(src)
        prompt = STYLE + "\n\nSCENE: " + scene
        print(f"[img] {name} (model={model}, refs={len(use_refs)}) ...", flush=True)
        ok = run(prompt, out, use_refs, model=model)
        if not ok:
            time.sleep(5)
            ok = run(prompt, out, use_refs, model=model)
        if ok:
            try:
                cost.record_hf(EPISODE, "short", "stills", model, note=f"[son-of-man-lifted-up] {name}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
