#!/usr/bin/env python
"""Re-roll the flagged stills with CORRECTED, pure-positive prompts (user: 'loads of issues').

Fixes applied (from the render_lint rules + probe cookbook):
  - crucified hands OPEN + pierced, never fists/rope (pure-positive, no forbidding words)
  - no church / dome / cross-topped building (period-correct houses + wall)
  - lots = carved knucklebones in the dust, never dice/dominoes/tiles
  - no free-standing candle outdoors (storm daylight)
  - nails shown as WOUNDS not proud studs (drop the word 'nail'; caption carries it)
  - risen face = same MATURE man (structural marks: lean face/high cheekbones/aquiline nose), one healed scar

CLEAR fixes render IN PLACE (old png + old mp4 deleted, still + clip DE-INDEXED per the standing rule).
RISEN face-drift candidates render to visual/_reface/ for a side-by-side pick (originals untouched
until the user chooses). Each prompt is linted pre-flight. ~9 cr with --render.

  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/refix_stills.py            # lint only
  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/refix_stills.py --render   # spend ~9 cr
"""
import argparse, importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]

def _load(n, rel):
    s = importlib.util.spec_from_file_location(n, ROOT / rel); m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m); return m

ber = _load("ber", "longform/_base_elements_refs.py")
rl = _load("rll", "render_lint/lint.py")
ax = _load("ax", "asset_index.py")

NBP = HERE / "visual" / "nbp"
REFACE = HERE / "visual" / "_reface"; REFACE.mkdir(parents=True, exist_ok=True)

# canonical descriptor + probe-#4 STRUCTURAL marks (tighten identity, no drifting spot-mole)
CHRIST = ("the SAME man throughout: a bearded man in his early thirties with a calm Near-Eastern face, "
          "a lean face with high cheekbones and a slightly aquiline nose, warm olive skin, deep brown "
          "eyes, a short dark full beard and long dark wavy hair parted in the middle")

# ---- CLEAR fixes (render in place) ----
CLEAR = {
    "01b_nailed_hands": (
        "A stark close macro of BOTH of the crucified Christ's hands, OPEN and flat against the dark "
        "rough wooden crossbeam, palms facing the viewer, fingers relaxed and gently parted, a dark "
        "ragged pierced wound in the CENTRE of each open palm with dark red blood running down toward "
        "the wrists. Behind, a black storm sky. Reverent, visceral."),
    "01c_soldiers_gamble": (
        "Three Roman soldiers in first-century legionary armour kneeling in the dust at the foot of the "
        "cross, casting small carved animal knucklebones scattered across the dust between them, their "
        "faces cold and indifferent. Behind them the base of the wooden upright is planted in the rocky "
        "ground, and high at the top edge of the frame the crucified man's pierced feet are just visible. "
        "A dark storm sky, only low flat-roofed pale limestone houses far in the distance. Period-accurate."),
    "01_golgotha_hook": (
        f"A WIDE dramatic view of {CHRIST}, crucified on a tall rough wooden cross under a black storm "
        "sky, his head bowed, his arms stretched along the crossbeam with BOTH hands OPEN and flat, palms "
        "forward, a dark pierced wound in the centre of each open palm, his feet pierced against the "
        "upright. Far below, a few small Roman soldiers. In the far distance only low flat-roofed pale "
        "limestone houses and a plain city wall. Reverent, epic, desolate."),
    "02_jesus_prays": (
        f"{CHRIST}, crucified on a wooden cross, his body hanging with EXACTLY TWO arms — one arm "
        "stretched straight out to each side ALONG the horizontal crossbeam, both hands OPEN and flat "
        "against the beam, palms forward, fingers relaxed, a dark pierced wound in the centre of each "
        "open palm. His head is lifted and tilted back toward heaven, his lips parting as he speaks a "
        "prayer. A single warm shaft of light across his face. A dark storm sky behind; far below, small "
        "Roman soldiers gather his garment. Correct human anatomy — only two arms and two hands. Reverent, merciful."),
    "05_pierced_hand": (
        f"A CLOSE shot of the crucified Christ's face and outstretched wounded hand ({CHRIST}): his head "
        "lifted, his near hand OPEN and flat, palm forward, reaching toward the viewer, showing a dark "
        "ragged pierced hole in the centre of the open palm with dark red blood running toward the wrist; "
        "his other arm rests along the wooden crossbeam, its hand also OPEN and flat with a matching "
        "pierced wound. A dark storm sky, one warm shaft of light across his face and the wounded open "
        "hand. Reverent, merciful."),
    "04_cast_lots": (
        "A ground-level close view in the dust at the foot of the cross: two weathered Roman soldiers' "
        "hands casting small carved animal knucklebones scattered across the dust, a heaped seamless white "
        "robe lying beside them, lit by the grey storm-broken daylight of the execution ground. Ancient "
        "Near-Eastern, period-accurate."),
}

# ---- RISEN face-drift candidates (render to _reface/ for a pick; originals untouched) ----
RISEN = {
    "06c_intercession_lives": (
        f"The living, risen Christ ({CHRIST}), standing calm in warm golden light, both hands lifted and "
        "OPEN in intercession, each open palm showing ONE single round healed scar of smooth closed pale "
        "skin at its centre. A steady warm radiance around him. His face calm, mature and weathered, "
        "exactly the same man as the suffering Christ. Reverent, alive, merciful."),
    "07b_gospel_wide": (
        f"The risen Christ ({CHRIST}) standing in a bright open ancient stone doorway flooded with warm "
        "golden morning light, his arms opening in welcome, both hands OPEN showing ONE single round healed "
        "scar in each palm, his bare feet planted on the stone. His face calm, mature and weathered, exactly "
        "the same man as the suffering Christ. Inviting, triumphant, reverent."),
    "07_risen_hero": (
        f"A close hero portrait of the risen Christ ({CHRIST}), his face calm and at peace, one hand OPEN "
        "and reaching gently toward the viewer, the open palm showing ONE single round healed scar of "
        "smooth closed pale skin at its centre, warm golden light behind him. His face mature and weathered, "
        "exactly the same man as the suffering Christ. Reverent, merciful, the mercy held out."),
}


def _lint(slug, subj):
    rl.report(subj, stage="still", context=f"REFIX {slug}")
    ber.lint_canonical(slug, subj)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--render", action="store_true")
    ap.add_argument("--only", default="", help="comma slugs to (re)do; default = all")
    a = ap.parse_args()
    only = {s.strip() for s in a.only.split(",") if s.strip()}

    print("\n########## CLEAR FIXES (in place) ##########")
    for slug, subj in CLEAR.items():
        if only and slug not in only:
            continue
        _lint(slug, subj)
        if not a.render:
            continue
        png = NBP / f"{slug}.png"; mp4 = NBP / f"{slug}.mp4"
        for p in (png, mp4):                     # delete old (redo rule)
            if p.exists(): p.unlink()
        ax.deindex(id=f"fft_{slug}"); ax.deindex(id=f"fft_{slug}_clip")
        print("  ->", ber.render(subj + ber.STYLE + ber.ONE, png, refs=None))

    print("\n########## RISEN CANDIDATES (-> _reface/, pick later) ##########")
    for slug, subj in RISEN.items():
        if only and slug not in only:
            continue
        _lint(slug, subj)
        if not a.render:
            continue
        print("  ->", ber.render(subj + ber.STYLE + ber.ONE, REFACE / f"{slug}.png", refs=None))

    if not a.render:
        print("\n[lint-only] add --render to spend ~9 cr")


if __name__ == "__main__":
    main()
