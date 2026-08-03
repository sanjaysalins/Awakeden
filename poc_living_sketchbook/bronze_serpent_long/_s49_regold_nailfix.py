"""One-off retry of s49_christ_radiant_begin (gold-icon style, sl17): the
first attempt had the hands read as gripping/wrapped around the crossbeam
rather than pinned by a nail -- close crop confirmed fingers curling OVER
and slightly behind the wood's edge, an active-hold read, not a passive
hang. User chose: keep the gold-icon style, retry with stronger, more
explicit anti-grip anatomy language (same fix pattern already proven once
on this exact spread earlier in the session, before the style change).

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent_long/_s49_regold_nailfix.py
"""
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _s2_stills as s2
import _s5_redo_styles_round2 as r2

NAME = "s49_christ_radiant_begin"
OUT = s2.OUT / f"{NAME}.png"

SCENE = (
    f"{r2.JESUS} lifted up on the plain wooden cross, head still bowed, "
    f"and the register turning from suffering to glory: the darkened sky "
    f"of the earlier spreads is gone, and behind Him the entire sky is "
    f"the burnished, cracked gold-leaf ground itself, an icon panel's "
    f"field of glory -- the gold touches ONLY that sky-ground around "
    f"Christ; His body, the cross, and the bare hill stay plain graphite, "
    f"ink, and muted wash. Both of His hands are pinned flat to the "
    f"crossbeam, palm facing outward toward the viewer, by a single "
    f"small dark nail through the center of each palm -- the fingers "
    f"hang loosely open and slightly curled downward ONLY from their own "
    f"weight, exactly the way a hand relaxes when nothing is gripping "
    f"anything -- the fingers and thumb do NOT close around, wrap "
    f"behind, or grasp any edge or surface of the wood anywhere; no part "
    f"of either hand touches or holds the wood except at the single nail "
    f"point. No visible wound beyond the one small nail mark on each "
    f"palm, no blood, restrained and sacred. " + s2.FULLBLEED
)


def main():
    if OUT.exists():
        print(f"[skip] {NAME} already has a still")
        return
    refs = s2.resolve_refs("jesus2")
    prompt = r2.STYLE_SL17_GOLD_GROUND + "\n\nSCENE: " + SCENE
    print(f"[img] {NAME} (refs={len(refs)}) ...", flush=True)
    ok = s2.run(prompt, OUT, refs)
    if not ok:
        time.sleep(5)
        ok = s2.run(prompt, OUT, refs)
    if ok:
        try:
            s2.cost.record_hf(s2.EPISODE, "long", "stills_restyle_round2_nailfix", s2.MODEL, note=f"[bronzeserpentlong-restyle2-nailfix] {NAME}")
        except Exception as e:
            print(f"   (ledger skipped: {e})")
        print("   ok")
    else:
        print("   FAILED")


if __name__ == "__main__":
    main()
