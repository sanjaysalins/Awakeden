"""Comic Page Pipeline POC -- Rung 1 Phase 1 CONSISTENCY FIX.

Designer verification confirmed three character/prop drifts across the 4
panel stills in poc_comic_page/rung1/stills/:
  1. panel_b_door.png: the Seeker's hair (seen from behind) reads dark/longish
     -- the anchor is SHORT GREYING HAIR (panel_d had it right). B is wrong.
  2. panel_d_threshold.png: Jesus reads slimmer/younger, cream tunic + brown
     sash -- panel_a_jesus.png is the anchor-correct reference (broader
     rugged face, undyed woolen robe, no sash). D is wrong.
  3. The door is arch-topped in B, straight-topped in D -- inconsistent.

Fix, in order:
  STEP 1: reroll panel_d_threshold, chained off panel_a_jesus.png (the
          settled, anchor-correct reference) with STRENGTHENED anchors that
          explicitly forbid the drifted traits.
  STEP 2 (only after STEP 1 passes self-check): reroll panel_b_door, chained
          off the NEW panel_d_threshold.png, with anchors stressed on the
          Seeker's hair + the arch-topped door.

Reuses the validated call/ledger pattern from _render_panel_stills.py / run()
and the backup-then-overwrite pattern from _reroll_panel_a.py.

  .venv\\Scripts\\python.exe poc_comic_page/rung1/_reroll_bd_consistency.py
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline import cost

from _render_panel_stills import AESTHETIC, CONSTRAINT, CHAIN_LINE, STYLE_TAIL, run

EPISODE = "CPP_Rung1_InNoWise"
HERE = Path(__file__).resolve().parent
OUT = HERE / "stills"

HARD_CAP_USD = 3.00

# ---- STEP 1: panel_d_threshold, strengthened anchors, chained off panel A --
ANCHORS_D = (
    "CORE CHARACTER DESIGN ANCHORS:\n"
    "Jesus Christ: THE SAME MAN as in the reference image -- the same "
    "broader, rugged face, the same shoulder-length dark wavy hair and full "
    "beard, wearing the SAME simple undyed woolen robe with a rough-woven "
    "mantle. No sash, no cream-colored tunic.\n"
    "The Seeker: an ordinary weary man in his forties, SHORT GREYING HAIR, "
    "lined face, plain earth-tone tunic and hooded cloak, clutching his "
    "worn leather ledger.\n"
    "The Door: a massive ancient ARCH-TOPPED wooden door, iron-banded, in a "
    "rough stone wall."
)

COMPOSITION_D = (
    "SINGLE PANEL COMPOSITION: Wide shot -- the Seeker crossing the "
    "threshold into the light, door swung open, and beyond it the standing "
    "figure of Jesus with a hand extended in welcome. Lighting: the warm "
    "light now dominant, shadows breaking.\n\n"
)

PANEL_D_V2 = (
    AESTHETIC + "\n\n" + CONSTRAINT + "\n\n" + ANCHORS_D + "\n\n"
    + CHAIN_LINE + COMPOSITION_D + STYLE_TAIL
)

# ---- STEP 2: panel_b_door, anchors stressed, chained off NEW panel D ------
ANCHORS_B = (
    "CORE CHARACTER DESIGN ANCHORS:\n"
    "The Seeker: THE SAME MAN as in the reference image -- SHORT GREYING "
    "HAIR seen from behind, same earth-tone hooded cloak, same worn "
    "leather ledger carried under his arm.\n"
    "The Door: THE SAME arch-topped iron-banded wooden door as in the "
    "reference image."
)

COMPOSITION_B = (
    "SINGLE PANEL COMPOSITION: The Seeker seen from behind at medium "
    "distance, stepping toward the great ancient door standing ajar, warm "
    "golden light spilling through the gap onto the stone floor toward his "
    "feet. Lighting: cold slate surroundings, warm light only from the door "
    "gap.\n\n"
)

PANEL_B_V2 = (
    AESTHETIC + "\n\n" + CONSTRAINT + "\n\n" + ANCHORS_B + "\n\n"
    + CHAIN_LINE + COMPOSITION_B + STYLE_TAIL
)

# ---- STEP 2 RE-ROLL: same as V2, but the ledger prop rendered ABSENT from
# both hands in the first V2 render (a real continuity break vs panel C's
# ledger close-up and panel D's held ledger) -- reinforce it explicitly.
ANCHORS_B_V3 = (
    "CORE CHARACTER DESIGN ANCHORS:\n"
    "The Seeker: THE SAME MAN as in the reference image -- SHORT GREYING "
    "HAIR seen from behind, same earth-tone hooded cloak. His free hand "
    "(not on the door handle) is clutching his worn leather-bound ledger "
    "book pressed against his side/chest -- the ledger MUST be visibly "
    "held and visible in this shot, not absent or out of frame.\n"
    "The Door: THE SAME arch-topped iron-banded wooden door as in the "
    "reference image."
)

COMPOSITION_B_V3 = (
    "SINGLE PANEL COMPOSITION: The Seeker seen from behind at medium "
    "distance, one hand reaching for the great ancient door standing ajar, "
    "his OTHER hand clutching his worn leather ledger pressed to his side, "
    "warm golden light spilling through the gap onto the stone floor toward "
    "his feet. Lighting: cold slate surroundings, warm light only from the "
    "door gap.\n\n"
)

PANEL_B_V3 = (
    AESTHETIC + "\n\n" + CONSTRAINT + "\n\n" + ANCHORS_B_V3 + "\n\n"
    + CHAIN_LINE + COMPOSITION_B_V3 + STYLE_TAIL
)


def _reroll(name, prompt, ref, note_suffix, spent_usd):
    out = OUT / f"{name}.png"
    backup = OUT / f"{name}.v1_DRIFT.png"
    n = 2
    while backup.exists():
        backup = OUT / f"{name}.v{n}_DRIFT.png"
        n += 1
    if out.exists():
        out.rename(backup)
        print(f"[keep] previous render backed up -> {backup}")
    if spent_usd >= HARD_CAP_USD:
        print(f"   STOP: hard cap ${HARD_CAP_USD:.2f} reached -- escalating.")
        if backup.exists():
            backup.rename(out)
        return spent_usd, False
    print(f"[img ] {name} (chained off {ref.name}) ...", flush=True)
    t = time.time()
    ok = run(prompt, out, [ref])
    if ok:
        try:
            row = cost.record_hf(EPISODE, "short", "stills", "nano_banana_pro",
                                  note=f"[rung1-phase1] {name} {note_suffix}")
            spent_usd += float(row.get("est_usd") or 0)
        except Exception as e:
            print(f"   (ledger record skipped: {e})")
        print(f"   ok ({time.time()-t:.0f}s)  running phase spend ~${spent_usd:.2f}")
        return spent_usd, True
    print("   FAILED -- restoring previous render.")
    if backup.exists():
        backup.rename(out)
    return spent_usd, False


def main():
    step = sys.argv[1] if len(sys.argv) > 1 else "d"
    spent_usd = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
    print(f"[start] step={step}  phase spend so far ~${spent_usd:.2f} (cap ${HARD_CAP_USD:.2f})")

    if step == "d":
        ref_a = OUT / "panel_a_jesus.png"
        spent_usd, ok_d = _reroll("panel_d_threshold", PANEL_D_V2, ref_a, "CONSISTENCY-FIX", spent_usd)
        print(f"\n[step1] panel_d_threshold: {'ok' if ok_d else 'FAILED'}  phase spend ~${spent_usd:.2f}")
        if not ok_d:
            print("[abort] STEP 1 failed -- not proceeding to STEP 2 (escalate).")
    elif step == "d_reroll":
        # one extra attempt if the self-check on the STEP 1 render FAILs (still
        # chained off panel_a_jesus.png, the anchor-correct reference).
        ref_a = OUT / "panel_a_jesus.png"
        spent_usd, ok_d = _reroll("panel_d_threshold", PANEL_D_V2, ref_a, "CONSISTENCY-FIX-REROLL2", spent_usd)
        print(f"\n[step1-reroll] panel_d_threshold: {'ok' if ok_d else 'FAILED'}  phase spend ~${spent_usd:.2f}")
    elif step == "b":
        ref_d = OUT / "panel_d_threshold.png"
        spent_usd, ok_b = _reroll("panel_b_door", PANEL_B_V2, ref_d, "CONSISTENCY-FIX", spent_usd)
        print(f"\n[step2] panel_b_door: {'ok' if ok_b else 'FAILED'}  phase spend ~${spent_usd:.2f}")
    elif step == "b_reroll":
        ref_d = OUT / "panel_d_threshold.png"
        spent_usd, ok_b = _reroll("panel_b_door", PANEL_B_V3, ref_d, "CONSISTENCY-FIX-REROLL2-ledger", spent_usd)
        print(f"\n[step2-reroll] panel_b_door: {'ok' if ok_b else 'FAILED'}  phase spend ~${spent_usd:.2f}")
    else:
        print(f"unknown step {step!r}")


if __name__ == "__main__":
    main()
