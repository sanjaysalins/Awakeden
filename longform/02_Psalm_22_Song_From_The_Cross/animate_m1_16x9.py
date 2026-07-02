#!/usr/bin/env python
"""Animate the M1-slice inked 16:9 stills via HF Kling 3.0 pro (camera-only, invent-nothing).

Uses the INKED graphic-novel motion prompt (flat ink stays as printed, only the camera moves) so
Kling keeps the inked look instead of repainting it — NOT the Baroque cut-plan. 16:9, 5s. Writes
clips to v1/visual_16x9_inked/clips/<slug>.mp4 which build_mocomic_16x9.py --clips swaps in.
Writing-heavy stills are SKIPPED (Kling morphs legible text into garble — memory
feedback-never-animate-writing); they stay ken-burns. Idempotent (existing .mp4 skipped).
Test-gate ONE clip before the batch.

  ...\\python.exe longform/02_Psalm_22_Song_From_The_Cross/animate_m1_16x9.py --lint          # $0 preview
  ...\\python.exe longform/02_Psalm_22_Song_From_The_Cross/animate_m1_16x9.py --only cry_ninth_hour   # ~$0.65 test
  ...\\python.exe longform/02_Psalm_22_Song_From_The_Cross/animate_m1_16x9.py --all            # ~$5.85 (9 clips)
"""
import argparse, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from _hf_animate_short import hf_animate

POOL = HERE / "v1" / "visual_16x9_inked"
CLIPS = POOL / "clips"; CLIPS.mkdir(parents=True, exist_ok=True)
SPEC = POOL / "mocomic_16x9_m1.spec.json"

# Stills with legible writing -> NEVER generatively animate (Kling garbles the text). Kept static.
SKIP = {"scribe_over_manuscripts"}

# per-still camera move + focal point (what to keep centred / ease toward)
MOTION = {
    "cry_ninth_hour":        ("pullback", "the upturned crying face on the cross"),
    "crane_cross_soldiers":  ("pushin",   "the crucified figure"),
    "pierced_hands_feet":    ("pushin",   "the iron nail through the pierced hand"),
    "david_psalmist":        ("pushin",   "David's upturned singing face"),
    "david_old_deathbed":    ("pushin",   "the old king lying on his bed"),
    "convergence_on_cross":  ("pushin",   "the central cross on the hill"),
    "poured_out_bones":      ("pushin",   "the wasted body"),
    "mockers_wag_heads":     ("pushin",   "the mocking faces"),
    "storm_over_jerusalem":  ("pushin",   "the storm-lit city and the three crosses"),
}

INK_BASE = ("A finished inked graphic-novel comic panel — flat printed art with bold black ink "
            "outlines, cel-flat color and cross-hatching. Animate it as {move}. The drawing itself "
            "never moves, redraws, repaints, breathes or changes; the ink lines and flat colors stay "
            "exactly as printed; only the camera moves. No hard cuts, no dissolves, no morphing, no "
            "subject motion, no limbs moving, no new lines drawn. INVENT NOTHING: show ONLY what is "
            "already inked in this exact panel; do not add or generate any hand, finger, limb, face, "
            "halo, nail, wound, object or detail that is not literally drawn. Keep the subject whole in frame.")


def _move(motion, focus):
    return {
        "pushin":   f"ONE slow, steady, continuous push-in toward {focus}",
        "pullback": f"ONE slow, steady, continuous pull-back that starts on {focus} and reveals the whole panel",
        "dolly":    f"ONE slow, steady, continuous dolly forward toward {focus}",
    }.get(motion, f"ONE slow, steady, continuous push-in toward {focus}")


def distinct_slugs():
    beats = json.loads(SPEC.read_text(encoding="utf-8"))["beats"]
    seen = []
    for b in beats:
        for c in b["clips"]:
            if c["slug"] not in seen:
                seen.append(c["slug"])
    return seen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=""); ap.add_argument("--all", action="store_true")
    ap.add_argument("--lint", action="store_true"); ap.add_argument("--duration", type=int, default=5)
    a = ap.parse_args()
    only = {x.strip() for x in a.only.split(",") if x.strip()}
    if not (only or a.all or a.lint):
        ap.error("pass --only <slug>, --all, or --lint")
    slugs = [s for s in distinct_slugs() if s not in SKIP and (a.all or a.lint or s in only)]
    print(f"== animate {len(slugs)} inked 16:9 panels · HF Kling pro {a.duration}s "
          f"{'(LINT)' if a.lint else ''} (skip writing: {sorted(SKIP)}) ==")
    for slug in slugs:
        motion, focus = MOTION.get(slug, ("pushin", "the main subject"))
        prompt = INK_BASE.format(move=_move(motion, focus))
        still = POOL / f"{slug}.png"
        out = CLIPS / f"{slug}.mp4"
        print(f"-- {slug:26} [{motion}] -> {focus}")
        if a.lint:
            continue
        if out.exists() and out.stat().st_size > 0:
            print(f"     [skip] {out.name}"); continue
        ok = hf_animate(still, out, prompt, a.duration, aspect_ratio="16:9")
        print(f"     SAVED {out}" if ok else f"     [FAILED] {slug} (NSFW/credit/concurrent?)")
    print("== DONE ==")


if __name__ == "__main__":
    main()
