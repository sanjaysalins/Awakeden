"""Comic Page Pipeline POC -- Rung 2 FINAL PHASE, Step 1: 2 corrective stills.

Fixes two CP-G10 defects caught at the stills gate:
  p1a_night_door  -- current version shows a DOUBLE-leaf door (two door
                      panels with a visible center seam); canon (rung1
                      panel_b_door.png) is a SINGLE arch-topped iron-banded
                      door leaf. Re-render explicitly locking to one leaf.
  p2c_light_line  -- current version shows the Seeker's legs wrapped in
                      cross-gartered leggings to the knee ("OLDLEGS"); brief
                      wants bare weathered ankles + sandals beneath an
                      ankle-length tunic hem instead.

Reuses the verbatim aesthetic / GLOBAL TEXTUAL CONSTRAINT / CORE CHARACTER
DESIGN ANCHORS / style-tail blocks from _render_panel_stills.py (this dir).

  .venv\\Scripts\\python.exe poc_comic_page/rung2/_corrective_stills.py
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config  # noqa
from pipeline import cost  # noqa
import poc_comic_page.rung2._render_panel_stills as R  # noqa

HERE = Path(__file__).resolve().parent
OUT = HERE / "stills"
EPISODE = "CPP_Rung2_InNoWise"
HARD_CAP_USD = 1.00  # generous headroom for 2 stills @ ~$0.30 each, 1 reroll max each

JOBS = [
    ("p2c_light_line", "9:16", OUT / "p2a_rehearsing.png",
     "Extreme close-up at floor level: the thin line of warm golden light "
     "under the great door's edge spilling across worn stone flags, and at "
     "its edge in cold shadow the Seeker's worn leather sandals and bare "
     "weathered ankles beneath the hem of his ankle-length rough-woven "
     "tunic. Lighting: one warm light-line cutting the cold dark."),

    ("p1a_night_door", "1:1", ROOT / "poc_comic_page" / "rung1" / "stills" / "panel_b_door.png",
     "Wide establishing shot at night: the Seeker standing alone and small "
     "before the great SINGLE arch-topped iron-banded door (the same door "
     "as the reference), shut, in a vast rough stone wall -- cold "
     "slate-blue darkness, one thin line of warm light under the door. He "
     "stands a few paces back, the rolled scroll held to his chest, head "
     "cloth and ankle-length tunic. Lighting: cold moonless night, the only "
     "warmth the light-line under the door."),
]


def main():
    spent_usd = 0.0
    results = []
    for name, ar, ref, comp in JOBS:
        out = OUT / f"{name}.png"
        prompt = R.PREFIX + R.CHAIN_LINE + f"SINGLE PANEL COMPOSITION: {comp}\n\n" + R.STYLE_TAIL
        print(f"[img ] {name} (AR {ar}, ref {ref.name}) ...", flush=True)
        if spent_usd >= HARD_CAP_USD:
            print(f"   STOP: hard cap ${HARD_CAP_USD:.2f} reached -- escalating.")
            results.append((name, "ESCALATED-cap", None))
            continue
        t = time.time()
        ok = R.run(prompt, out, [ref], ar)
        if not ok:
            print("   first attempt FAILED -- one re-roll allowed")
            time.sleep(3)
            ok = R.run(prompt, out, [ref], ar)
        if ok:
            try:
                row = cost.record_hf(EPISODE, "short", "stills", R.MODEL,
                                      note=f"[rung2-final-phase] {name} CORRECTIVE")
                spent_usd += float(row.get("est_usd") or 0)
            except Exception as e:
                print(f"   (ledger record skipped: {e})")
            print(f"   ok ({time.time()-t:.0f}s)  running spend ~${spent_usd:.2f}")
            results.append((name, "clean", out))
        else:
            print("   FAILED twice -- escalate")
            results.append((name, "FAILED", None))
    print(f"\n[out] {OUT}")
    print(f"[spend] ~${spent_usd:.2f} of ${HARD_CAP_USD:.2f} cap")
    for name, status, out in results:
        print(f"  {name}: {status}" + (f" -> {out}" if out else ""))


if __name__ == "__main__":
    main()
