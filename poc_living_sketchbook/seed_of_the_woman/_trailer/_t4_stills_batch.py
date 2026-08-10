"""Trailer batch 2: 7 new stills (S1, S2, S4, S5, S7, S9, S10). S8 reuses
the existing approved stills/s48_heel_strike.png (no new render, per
Fable's own recommendation). S3 already fixed ($0 camera push over the
approved still); S6 already approved (serpent, Kling, real motion).

  .venv\\Scripts\\python.exe poc_living_sketchbook/seed_of_the_woman/_trailer/_t4_stills_batch.py
"""
import importlib.util
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
EPISODE = "SeedOfTheWoman"
HERE = Path(__file__).resolve().parent
OUT = HERE / "stills"
OUT.mkdir(parents=True, exist_ok=True)

EP_DIR = HERE.parent
CAST = EP_DIR.parent / "cast"
WORLD = EP_DIR.parent / "world"
SPREADS_STILLS = EP_DIR / "stills"

spec = importlib.util.spec_from_file_location("_ep_stills", EP_DIR / "_s2_stills.py")
ep = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ep)

REF_MAP = {
    "adam": CAST / "adam_ref.png",
    "eve": CAST / "eve_ref.png",
    "serpent": WORLD / "serpent_ref.png",
    "s18": SPREADS_STILLS / "s18_turns_to_serpent.png",
    "jesus": CAST / "jesus_ref.png",
    "s51": SPREADS_STILLS / "s51_bearing_wages.png",
    "eden": WORLD / "eden_ref.png",
}

SHOTS = [
    # S1: Eden whole, wide, no figures -- atmospheric push territory (Seedance).
    ("t_s1_eden_wide", "eden",
     f"WIDE establishing view, eye-level, looking into the heart of the "
     f"garden: {ep.EDEN} The two great central trees stand deep in frame, "
     f"morning gold light breaking through the high canopy in thick "
     f"visible shafts, mist drifting low across the ground between the "
     f"trunks. No figures present. {ep.FULLBLEED}"),
    # S2: the bitten fruit, frozen mid-fall from an open hand. Macro, no
    # face -- real invented object-action is low risk here (Kling).
    ("t_s2_fruit_falling", "",
     f"EXTREME MACRO shot, the frame filled almost entirely by a single "
     f"bitten fruit -- one clear bite mark, pale flesh exposed -- caught "
     f"in mid-fall just below an open human hand visible only from the "
     f"wrist down at the top edge of frame, no face, no body. Soft "
     f"golden light on the fruit's skin. Below, blurred dark earth waits "
     f"to receive it. {ep.FULLBLEED}"),
    # S4: Adam+Eve pressed into shadow behind the roots, a light shaft
    # beginning to reach toward them. REVISED animation treatment (not
    # this prompt) will keep the figures near-still and let the light
    # carry the motion, per the user's own running-shot lesson.
    ("t_s4_hiding_light", "adam,eve",
     f"MEDIUM shot, eye-level, camera positioned low among broad-leafed "
     f"undergrowth: {ep.ADAM} and {ep.EVE} pressed close together deep "
     f"in shadow behind a massive tree's exposed roots, genuinely "
     f"concealed, Eve's hand raised to cover her own mouth, both faces "
     f"turned toward one bright shaft of warm golden light that has just "
     f"begun to fall across the ground several feet away from them, not "
     f"yet reaching their hiding place -- clear dark shadow still "
     f"between the light's leading edge and the two figures. {ep.FULLBLEED}"),
    # S5: the sentencing tableau at trailer scale -- figures deliberately
    # TINY and distant (low identity-drift risk even under real camera
    # motion), a towering column of light, torn dark sky.
    ("t_s5_sentencing_wide", "adam,eve",
     f"VERY WIDE shot, low angle looking up a gentle rise: {ep.ADAM} and "
     f"{ep.EVE}, small and distant figures, heads bowed together, "
     f"standing braced before a towering vertical column of warm golden "
     f"light that dominates the frame's height, dwarfing them completely "
     f"-- the two figures are small enough that no facial detail is "
     f"legible at this distance. Torn dark storm-grey paper sky above. "
     f"{ep.FULLBLEED}"),
    # S7: the serpent flat and motionless, high-angle down, WITH an open
    # diagonal lane left clear across the ground for a $0 shadow-sweep
    # device to travel later (matching the main film's own build_s55
    # pattern) -- avoids ever asking a paid animator to touch the
    # serpent for this beat.
    ("t_s7_serpent_shadow_base", "serpent,s18",
     f"STEEP HIGH-ANGLE view, the camera looking sharply DOWN (per "
     f"world/SERPENT.md's locked camera rule): {ep.SERPENT} Lying belly-"
     f"flat and completely motionless in open dust, head low, in the "
     f"LOWER-LEFT of the frame. A clear stretch of open, evenly-lit "
     f"ground runs diagonally from the UPPER-RIGHT of the frame down to "
     f"the serpent's position, empty and unshadowed for now. Ink-blue-"
     f"toned scales throughout, cool judgment coloring, never gold, "
     f"never warm. {ep.FULLBLEED}"),
    # S9: the cross in silhouette, trailer-scale wide, low angle -- crane
    # target. Reuses this episode's own locked crucifixion conventions
    # (wound-free, gold-leaf edge, dark-not-storm sky) via s51+jesus refs.
    ("t_s9_cross_wide", "jesus,s51",
     f"VERY WIDE establishing shot, LOW angle looking UP a bare rocky "
     f"hill from its base: at the crest, small against a vast torn dark "
     f"sky, a single plain wooden cross, and upon it {ep.JESUS.split('.')[0]} "
     f"-- the SAME man as the reference images -- head bowed, arms "
     f"stretched along the crossbeam, wrists cord-bound, wound-free, no "
     f"visible blood, no graphic detail. The whole sky unnaturally dark "
     f"at midday, flat and heavy, NOT storm clouds, no lightning. A thin "
     f"strip of gold leaf remains visible along one edge of the page. "
     f"{ep.FULLBLEED}"),
    # S10: the tomb mouth, gold light blazing outward, no figure -- push-
    # into-light territory (Seedance).
    ("t_s10_tomb_wide", "",
     f"MEDIUM shot, eye-level, camera deliberately OFF-AXIS to one side "
     f"of a rock-hewn tomb's open mouth: a low rough-cut stone entrance "
     f"in a pale hillside, its great round stone rolled fully aside. "
     f"From within the dark doorway a warm gold light glows steadily "
     f"outward, spilling across the worn stone threshold. Just inside, "
     f"caught by the glow, folded LINEN grave-cloths lie neatly at rest, "
     f"undisturbed and empty. Pale rose-and-amber dawn light touches the "
     f"hillside outside. ABSOLUTELY NO figure anywhere. {ep.FULLBLEED}"),
]


def run(prompt, out, refs):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt,
           "--aspect_ratio", "16:9", "--resolution", "2k", "--wait"]
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


def resolve_refs(tag):
    refs = []
    for t in tag.split(","):
        t = t.strip()
        if t and REF_MAP.get(t) and REF_MAP[t].exists():
            refs.append(REF_MAP[t])
    return refs


def main():
    for name, tag, scene in SHOTS:
        out = OUT / f"{name}.png"
        if out.exists():
            print(f"[skip] {name}")
            continue
        refs = resolve_refs(tag)
        prompt = ep.STYLE + "\n\nSCENE: " + scene
        print(f"[img] {name} (refs={len(refs)}) ...", flush=True)
        ok = run(prompt, out, refs)
        if not ok:
            time.sleep(8)
            ok = run(prompt, out, refs)
        if ok:
            try:
                cost.record_hf(EPISODE, "long", "trailer_batch2", MODEL, note=f"[trailer] {name}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")


if __name__ == "__main__":
    main()
