"""One-off fresh re-render of s50_christ_close_words: user says the still is
still not right (after the halo-lock and mouth-lock animation fixes) and
asked to just reimage it as a new generation, rather than keep patching.
Same style (STYLE_SL06_WET_IN_WET) and same scene text as the round-2
restyle -- a fresh generation call naturally produces a different image.

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent_long/_s50_reimage.py
"""
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _s2_stills as s2
import _s5_redo_styles_round2 as r2

NAME = "s50_christ_close_words"
OUT = s2.OUT / f"{NAME}.png"

SCENE = (
    f"A close reverent shot on {r2.JESUS}'s face and upper form, lifted on "
    f"the cross, His expression calm and resolved, about to speak -- His "
    f"face, eyes, and beard held in the sharpest, most precise ink "
    f"linework in the frame, while the gathering warm glow around His "
    f"head and shoulders is painted wet-into-wet, the warm pigment "
    f"blooming and bleeding softly outward from His form into the damp "
    f"paper beyond it, as though the light itself is spreading through "
    f"the page -- no visible wound, no blood, the warm gold tones "
    f"reserved only for this glow, never elsewhere in the frame. "
    f"{r2.FULLBLEED}"
)


def main():
    if OUT.exists():
        archived = s2.OUT / f"{NAME}.v3_reimage_reject.png"
        if not archived.exists():
            OUT.rename(archived)
            print(f"[archive] {NAME} -> {archived.name}")
    refs = s2.resolve_refs("jesus2")
    prompt = r2.STYLE_SL06_WET_IN_WET + "\n\nSCENE: " + SCENE
    print(f"[img] {NAME} (refs={len(refs)}) ...", flush=True)
    ok = s2.run(prompt, OUT, refs)
    if not ok:
        time.sleep(5)
        ok = s2.run(prompt, OUT, refs)
    if ok:
        try:
            s2.cost.record_hf(s2.EPISODE, "long", "stills_reimage", s2.MODEL, note=f"[bronzeserpentlong-s50-reimage] {NAME}")
        except Exception as e:
            print(f"   (ledger skipped: {e})")
        print("   ok")
    else:
        print("   FAILED")


if __name__ == "__main__":
    main()
