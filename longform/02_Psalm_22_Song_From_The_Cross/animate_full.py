#!/usr/bin/env python
"""Animate the FULL-film hero beats that want GENERATIVE Kling motion (INK camera-only, 16:9, 5s).

The cam:arc/swoop beats stay $0 dynamic_cam; writing stills stay dyncam (never Kling). This renders
only the chosen hero slugs -> v1/visual_16x9_inked/clips/<slug>.mp4. Idempotent. Reuses hf_animate +
the INK camera-only prompt. Focus point read from the anchor sidecar.

  ...python .../animate_full.py --lint                 # $0 preview
  ...python .../animate_full.py --only the_turn         # ~$0.65 test
  ...python .../animate_full.py --all                   # the hero set
"""
import argparse, importlib.util, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from _hf_animate_short import hf_animate

POOL = HERE / "v1" / "visual_16x9_inked"
CLIPS = POOL / "clips"; CLIPS.mkdir(parents=True, exist_ok=True)

INK_BASE = ("A finished inked graphic-novel comic panel — flat printed art with bold black ink "
            "outlines, cel-flat color and cross-hatching. Animate it as {move}. The drawing itself "
            "never moves, redraws, repaints, breathes or changes; the ink lines and flat colors stay "
            "exactly as printed; only the camera moves. No hard cuts, no dissolves, no morphing, no "
            "subject motion, no limbs moving, no new lines drawn. INVENT NOTHING: show ONLY what is "
            "already inked in this exact panel. Keep the subject whole in frame.")

# hero beats that want generative motion (writing stills excluded -> they stay $0 dyncam)
MOTION = {
    "thirst_dust":          ("pushin",   "the parched suffering face"),
    "face_anguish_closeup": ("pushin",   "the crying upturned face"),
    "the_turn":             ("pushin",   "the rising Christ in the light"),
    "risen_worshipper":     ("pullback", "the risen Christ, revealing the gathered congregation"),
    "ends_of_earth":        ("pushin",   "the cross on the hill drawing the nations"),
    "finished_work":        ("pushin",   "the risen Christ at rest"),
    "risen_hero_come":      ("pushin",   "the risen Christ's reaching open hand"),
}


def _move(motion, focus):
    return {
        "pushin":   f"ONE slow, steady, continuous push-in toward {focus}",
        "pullback": f"ONE slow, steady, continuous pull-back that starts on {focus} and reveals the whole panel",
    }.get(motion, f"ONE slow, steady, continuous push-in toward {focus}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=""); ap.add_argument("--all", action="store_true")
    ap.add_argument("--lint", action="store_true"); ap.add_argument("--duration", type=int, default=5)
    a = ap.parse_args()
    only = {x.strip() for x in a.only.split(",") if x.strip()}
    if not (only or a.all or a.lint):
        ap.error("pass --only <slug>, --all, or --lint")
    slugs = [s for s in MOTION if a.all or a.lint or s in only]
    print(f"== animate {len(slugs)} hero beats · HF Kling pro 16:9 {a.duration}s {'(LINT)' if a.lint else ''} ==")
    for slug in slugs:
        motion, focus = MOTION[slug]
        prompt = INK_BASE.format(move=_move(motion, focus))
        still = POOL / f"{slug}.png"; out = CLIPS / f"{slug}.mp4"
        print(f"-- {slug:24} [{motion}] -> {focus}")
        if a.lint:
            continue
        if out.exists() and out.stat().st_size > 0:
            print(f"     [skip] {out.name}"); continue
        ok = hf_animate(still, out, prompt, a.duration, aspect_ratio="16:9")
        print(f"     SAVED {out}" if ok else f"     [FAILED] {slug} (NSFW/credit?)")
    print("== DONE ==")


if __name__ == "__main__":
    main()
