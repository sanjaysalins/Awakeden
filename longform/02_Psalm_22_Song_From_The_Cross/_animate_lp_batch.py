#!/usr/bin/env python
"""Living-page full-film hero batch: retries the HF-502 failures + the 2 extras (~$3.25).
Idempotent. HF first; stubborn failures fall back to the DIRECT Kling API (image_to_kling.py)."""
import subprocess, sys
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

MOTION = {
    "risen_worshipper":    "ONE slow, steady, continuous pull-back that starts on the risen Christ and reveals the whole radiant panel",
    "ends_of_earth":       "ONE slow, steady, continuous push-in toward the cross on the hill drawing the nations",
    "finished_work":       "ONE slow, steady, continuous push-in toward the risen Christ at rest",
    "empty_tomb_open":     "ONE slow, steady, continuous push-in toward the folded grave-cloths in the dawn light",
    "parting_storm_light": "ONE slow, steady, continuous push-in toward the cross in the breaking light",
}

for slug, move in MOTION.items():
    still, out = POOL / f"{slug}.png", CLIPS / f"{slug}.mp4"
    if out.exists() and out.stat().st_size > 0:
        print(f"[skip] {slug}"); continue
    ok = hf_animate(still, out, INK_BASE.format(move=move), 5, aspect_ratio="16:9")
    if not ok:
        print(f"[HF failed] {slug} -> direct Kling API fallback")
        r = subprocess.run([sys.executable, str(ROOT.parent / "PythonProject1" / "jesus" / "image_to_kling.py"),
                            str(still), "--out", str(out), "--prompt", INK_BASE.format(move=move),
                            "--duration", "5", "--stage-b-only"],
                           capture_output=True, text=True)
        ok = out.exists() and out.stat().st_size > 0
        if not ok:
            print(f"   [direct-kling stderr] {r.stderr[-300:]}")
    print(f"SAVED {slug}" if ok else f"FAILED {slug} (dyncam fallback will carry it)")
print("DONE")
