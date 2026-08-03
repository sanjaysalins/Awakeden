"""Bronze Serpent LONG -- step 9: ambient SFX bed, layered UNDER the scored
film via the shared long-form engine (pipeline/sfx_bed.py -- same one every
shipped long-form episode uses; the shorts keep a separate engine). Ambience
+ two motivated one-shots only -- NO choir/score_* clips under the music
(feedback-no-choir-pad-under-score / the DUAL-SCORE TRAP), matching this
project's audio layer stack: narration -> SCORE -> SFX (quietest).

Cue windows are read live from _spread_windows.json (the real aligned spread
timings, not the plan's rough estimate) so a future re-run after any spread
retiming stays correct without hand-edited timestamps.

Cue list, grounded in the beats each cue actually covers (per _PLAN.md):
  wind_desert_bleak     whole film, very low  -- constant wilderness ground,
                        same treatment as the SHORT's own s01 header beat.
  crowd_murmur_distant  s07-s11 (the discouraged/angry camp) AND s19-s20
                        (the now-contrite camp) -- same slug, two windows.
  rumble_deep_sub       s14-s17 (the serpents arrive / the bite / collapse)
                        -- judgment dread, paired with the crowd's own dread
                        the same way the SHORT layered it under s03/s04.
  fire_crackling        s27-s28 (forging) and s42 (finishing the forge,
                        bookends s28) -- the same slug, two windows.
  nail_strike_single    3 short punctuation hits inside s28's own window,
                        spaced out -- the hammer actually striking.
  impact_low_boom       s55 (Hezekiah breaks the bronze serpent) -- the
                        plan's OWN device note explicitly asks for "a real
                        SFX hit" to sync the impact-burst visual device to
                        (_PLAN.md row 55); this is that hit.

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent_long/_s9_sfx.py
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

SCORED = HERE / "BRONZESERPENT_LONG_living_sketchbook_scored.mp4"
OUT = HERE / "BRONZESERPENT_LONG_living_sketchbook_scored_sfx.mp4"
TOTAL = WINDOWS[-1]["end"]  # landing's own end = the film's real total


def w(name):
    r = BY_NAME[name]
    return r["start"], r["end"]


def span(name_a, name_b):
    return BY_NAME[name_a]["start"], BY_NAME[name_b]["end"]


def main():
    if not SCORED.exists():
        sys.exit(f"missing scored film: {SCORED} -- run _s8_score.py --yes first")

    crowd1 = span("s07_ungrateful_camp", "s11_crowd_angry")
    crowd2 = span("s19_people_kneel", "s20_vc_we_have_sinned")
    rumble = span("s14_serpent_hint", "s17_vignette_collapse")
    fire1 = span("s27_hands_gather_ore", "s28_forge_acting")
    fire2 = w("s42_hands_finish_forge")
    s28_start, s28_end = w("s28_forge_acting")
    s28_mid = s28_start + (s28_end - s28_start) * 0.5
    hezekiah_start, hezekiah_end = w("s55_hezekiah_breaks")
    impact_t = hezekiah_start + (hezekiah_end - hezekiah_start) * 0.35

    cues = [
        ("wind_desert_bleak", 0.0, TOTAL, -22),
        ("crowd_murmur_distant", crowd1[0], crowd1[1], -15),
        ("crowd_murmur_distant", crowd2[0], crowd2[1], -16),
        ("rumble_deep_sub", rumble[0], rumble[1], -17),
        ("fire_crackling", fire1[0], fire1[1], -14),
        ("fire_crackling", fire2[0], fire2[1], -16),
        ("nail_strike_single", s28_start + 1.0, s28_start + 1.6, -10),
        ("nail_strike_single", s28_mid, s28_mid + 0.6, -10),
        ("nail_strike_single", s28_end - 1.4, s28_end - 0.8, -10),
        ("impact_low_boom", impact_t, impact_t + 4.0, -9),
    ]

    print(f"[sfx] total={TOTAL:.1f}s  {len(cues)} cues")
    sfx_bed.build(SCORED, OUT, cues, TOTAL)


if __name__ == "__main__":
    main()
