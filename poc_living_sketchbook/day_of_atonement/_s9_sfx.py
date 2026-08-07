"""Day of Atonement LONG -- step 9: ambient SFX bed, layered UNDER the scored
film via the shared long-form engine (pipeline/sfx_bed.py -- same one every
shipped long-form episode uses). Ambience + motivated one-shots only -- NO
choir/score_* clips under the music (feedback-no-choir-pad-under-score / the
DUAL-SCORE TRAP), matching this project's audio layer stack: narration ->
SCORE -> SFX (quietest). No thunder near s53_the_cross either -- this
episode's own locked fact card (crucifixion-still-facts.md) says the
darkness at the cross was NOT storm weather.

Cue windows are read live from _spread_windows.json (the real aligned spread
timings) so a future re-run after any spread retiming stays correct without
hand-edited timestamps.

Cue list, grounded in the beats each cue actually covers (per _spread_table.py):
  wind_desert_bleak     whole film, very low -- constant wilderness ground.
  air_hollow_desolate   s06 (the empty Holy of Holies) -- the vacancy itself.
  crowd_murmur_distant  s07 (the nation waiting outside).
  door_gate_creak       s08 (the curtain sealing shut behind him) and, much
                        gentler, s70 (the answering bookend -- the veil held
                        OPEN, not shut).
  fire_crackling        s10 (the strange fire, Nadab and Abihu).
  impact_low_boom       s11 (struck down) and s25 (the goat slain) -- two
                        separate weighty judgment/sacrifice beats, same slug.
  footsteps_dirt_approach s05 (Aaron's own walk to the veil) and, mirrored,
                        s73 (Aaron steps aside) -- a deliberate bookend.
  waterpot_drop_run     s42 (the basin made ready).
  veil_tearing          s62 (the veil torn) -- the film's one loudest cue,
                        exact content match.

  .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_s9_sfx.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline import sfx_bed  # noqa: E402

HERE = Path(__file__).resolve().parent
WINDOWS = json.loads((HERE / "_spread_windows.json").read_text(encoding="utf-8"))
BY_NAME = {r["name"]: r for r in WINDOWS}

SCORED = HERE / "DAYOFATONEMENT_LONG_living_sketchbook_scored.mp4"
OUT = HERE / "DAYOFATONEMENT_LONG_living_sketchbook_scored_sfx.mp4"
TOTAL = WINDOWS[-1]["end"]  # landing's own end = the film's real total


def w(name):
    r = BY_NAME[name]
    return r["start"], r["end"]


def main():
    if not SCORED.exists():
        sys.exit(f"missing scored film: {SCORED} -- run _s8_score.py --yes first")

    walk_to_veil = w("s05_walking_to_veil")
    empty_hol = w("s06_holy_of_holies_empty")
    nation_outside = w("s07_nation_outside")
    curtain_shut = w("s08_curtain_shut")
    strange_fire = w("s10_strange_fire")
    struck_down = w("s11_struck_down")
    slaying = w("s25_slaying_stage1")
    basin_ready = w("s42_basin_linen_ready")
    veil_torn = w("s62_veil_torn")
    veil_open = w("s70_veil_held_open")
    aaron_aside = w("s73_aaron_steps_aside")

    cues = [
        ("wind_desert_bleak", 0.0, TOTAL, -22),
        ("footsteps_dirt_approach", walk_to_veil[0], walk_to_veil[1], -16),
        ("air_hollow_desolate", empty_hol[0], empty_hol[1], -18),
        ("crowd_murmur_distant", nation_outside[0], nation_outside[1], -15),
        ("door_gate_creak", curtain_shut[0], curtain_shut[1], -14),
        ("fire_crackling", strange_fire[0], strange_fire[1], -14),
        ("impact_low_boom", struck_down[0], struck_down[1], -11),
        ("impact_low_boom", slaying[0], slaying[1], -12),
        ("waterpot_drop_run", basin_ready[0], basin_ready[1], -15),
        ("veil_tearing", veil_torn[0], veil_torn[1], -8),
        ("door_gate_creak", veil_open[0], veil_open[1], -18),
        ("footsteps_dirt_approach", aaron_aside[0], aaron_aside[1], -16),
    ]

    print(f"[sfx] total={TOTAL:.1f}s  {len(cues)} cues")
    sfx_bed.build(SCORED, OUT, cues, TOTAL)


if __name__ == "__main__":
    main()
