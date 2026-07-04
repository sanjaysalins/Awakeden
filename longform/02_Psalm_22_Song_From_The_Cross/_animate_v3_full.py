#!/usr/bin/env python
"""v3 upgrade Kling batch (LIVINGPAGE_STANDARD 3b: >=80% generative floor).
Batch A = existing stills (17). Batch B (--heroes) = the 6 new hero stills after eye-audit."""
import argparse, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from _hf_animate_short import hf_animate

POOL = HERE / "v1" / "visual_16x9_inked"
CLIPS = POOL / "clips"

INK_BASE = ("A finished inked graphic-novel comic panel — flat printed art with bold black ink "
            "outlines, cel-flat color and cross-hatching. Animate it as {move}. The drawing itself "
            "never moves, redraws, repaints, breathes or changes; the ink lines and flat colors stay "
            "exactly as printed; only the camera moves. No hard cuts, no dissolves, no morphing, no "
            "subject motion, no limbs moving, no new lines drawn. INVENT NOTHING: show ONLY what is "
            "already inked in this exact panel. Keep the subject whole in frame.")

A = {
    "worm_reproach":        "ONE slow, steady, continuous push-in toward the bowed despised figure",
    "scholar_hand_on_text": "ONE slow, steady, continuous push-in toward the scholar's furrowed brow",
    "mocker_faces_trio":    "ONE slow, steady, continuous push-in toward the three sneering faces",
    "worm_lowest":          "ONE slow, steady, continuous push-in toward the bowed broken figure",
    "dogs_encompass":       "ONE slow, steady, continuous push-in toward the tightening ring of dogs",
    "lion_gape":            "ONE slow, steady, continuous push-in toward the roaring jaws",
    "kindreds_bowing":      "ONE slow, steady, continuous pull-back that starts on the central light and reveals the whole bowing ring",
    "nations_streaming_wide": "ONE slow, steady, continuous push-in toward the hill of light where the roads converge",
    "dawn_empty_cross":     "ONE slow, steady, continuous push-in toward the cross in the dawn light",
    "kneeling_at_cross":    "ONE slow, steady, continuous push-in rising toward the towering cross above the kneelers",
    "hand_reaching_closeup": "ONE slow, steady, continuous push-in toward the open scarred palm",
    "vinegar_sponge":       "ONE slow, steady, continuous push-in toward the lifted sponge on the reed",
    "cry_face_tears":       "ONE slow, steady, continuous push-in toward the parched tearful face",
    "risen_hands_raised":   "ONE slow, steady, continuous push-in toward the serene lifted face",
    "david_hands_lyre":     "ONE slow, steady, continuous push-in toward the hands on the lyre strings",
    "garment_tug":          "ONE slow, steady, continuous push-in toward the taut robe between the fists",
    "ends_of_earth":        "ONE slow, steady, continuous push-in toward the cross on the hill drawing the nations",
}
B = {
    "cry_profile_dark":     "ONE slow, steady, continuous push-in toward the rim-lit crying profile",
    "wrists_bound_beam_macro": "ONE slow, steady, continuous push-in toward the lashed wrist on the beam",
    "substitute_shadow":    "ONE slow, steady, continuous push-in following the cross shadow toward the spared people",
    "mockers_below_cross_low": "ONE slow, steady, continuous push-in rising past the jeering shoulders up toward the cross",
    "john_at_cross_foot":   "ONE slow, steady, continuous push-in toward the young witness looking up",
    "golgotha_three_crosses_ridge": "ONE slow, steady, continuous push-in toward the three crosses on the ridge",
}

ap = argparse.ArgumentParser()
ap.add_argument("--heroes", action="store_true")
args = ap.parse_args()
batch = B if args.heroes else A
for slug, move in batch.items():
    still, out = POOL / f"{slug}.png", CLIPS / f"{slug}.mp4"
    if not still.exists():
        print(f"[no-still] {slug}"); continue
    if out.exists() and out.stat().st_size > 0:
        print(f"[skip] {slug}"); continue
    ok = hf_animate(still, out, INK_BASE.format(move=move), 5, aspect_ratio="16:9")
    print(f"SAVED {slug}" if ok else f"FAILED {slug}")
print("DONE")
