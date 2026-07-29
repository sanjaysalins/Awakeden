"""Comic Page Pipeline POC -- Rung 1 Phase 2 URGENT AMENDMENT fix.

The stills-gate re-review caught a real anatomy defect in panel_b_door.png:
the Seeker's body walks away from the viewer but his HEAD is over-rotated
into a full sideways profile (jaw wrenched toward the shoulder). REJECTED.

This reroll, chained off panel_d_threshold.png (the settled anchor-correct
Jesus/door reference), replaces the composition with a strict "back of head
only, zero facial features" framing and adds an explicit HEAD POSE
CONSTRAINT anchor line. Same AESTHETIC/CONSTRAINT blocks and the ledger-
visible ANCHORS_B_V3 anchor (the one that produced the currently-standing,
otherwise-correct panel_b_door.png) as _reroll_bd_consistency.py used.

  .venv\\Scripts\\python.exe poc_comic_page/rung1/_reroll_bd_headfix.py [reroll]
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

HARD_CAP_USD = 1.00  # this fix alone (still + one allowed reroll)

# same ledger-visible anchor as PANEL_B_V3 in _reroll_bd_consistency.py, plus
# the new HEAD POSE CONSTRAINT line from the amendment.
ANCHORS_B_HEADFIX = (
    "CORE CHARACTER DESIGN ANCHORS:\n"
    "The Seeker: THE SAME MAN as in the reference image -- SHORT GREYING "
    "HAIR seen from behind, same earth-tone hooded cloak. His free hand "
    "(not on the door handle) is clutching his worn leather-bound ledger "
    "book pressed against his side/chest -- the ledger MUST be visibly "
    "held and visible in this shot, not absent or out of frame.\n"
    "The Door: THE SAME arch-topped iron-banded wooden door as in the "
    "reference image.\n"
    "HEAD POSE CONSTRAINT: the back of the head only -- hair and the two "
    "ear edges at most; zero facial features visible."
)

COMPOSITION_HEADFIX = (
    "SINGLE PANEL COMPOSITION: The Seeker seen from DIRECTLY BEHIND at "
    "medium distance, walking toward the great ancient arch-topped door "
    "standing ajar -- ONLY THE BACK OF HIS HEAD is visible, no profile, his "
    "face completely hidden from the viewer, head facing straight ahead "
    "toward the door. His worn leather ledger carried under his left arm, "
    "his right hand reaching toward the door handle. Warm golden light "
    "spilling through the door gap onto the stone floor toward his feet. "
    "Lighting: cold slate surroundings, warm light only from the door "
    "gap.\n\n"
)

PANEL_B_HEADFIX = (
    AESTHETIC + "\n\n" + CONSTRAINT + "\n\n" + ANCHORS_B_HEADFIX + "\n\n"
    + CHAIN_LINE + COMPOSITION_HEADFIX + STYLE_TAIL
)


def _next_backup_name(base: str) -> Path:
    # amendment explicitly names the backup panel_b_door.v3_HEADTWIST.png
    return OUT / f"{base}.v3_HEADTWIST.png"


def main():
    reroll = len(sys.argv) > 1 and sys.argv[1] == "reroll"
    ref_d = OUT / "panel_d_threshold.png"
    out = OUT / "panel_b_door.png"

    if not reroll:
        backup = _next_backup_name("panel_b_door")
        if out.exists():
            out.rename(backup)
            print(f"[keep] rejected head-twist render backed up -> {backup}")

    print(f"[img ] panel_b_door HEADFIX (chained off {ref_d.name}) ...", flush=True)
    t = time.time()
    ok = run(PANEL_B_HEADFIX, out, [ref_d])
    if ok:
        try:
            row = cost.record_hf(EPISODE, "short", "stills", "nano_banana_pro",
                                  note=f"[rung1-phase2] panel_b_door HEAD-FIX"
                                       + (" REROLL" if reroll else ""))
            usd = float(row.get("est_usd") or 0)
        except Exception as e:
            usd = None
            print(f"   (ledger record skipped: {e})")
        print(f"   ok ({time.time()-t:.0f}s)" + (f"  +${usd:.2f}" if usd else ""))
    else:
        print("   FAILED")
    print(f"\n[out] {out}")


if __name__ == "__main__":
    main()
