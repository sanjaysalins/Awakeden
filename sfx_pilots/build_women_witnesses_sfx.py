"""Ambient/SFX bed for 'Women as First Witnesses' (Luke 24:5-6) — cluster-2.

Arc: a hollow indoor stone room under the hook + the apostles' unbelief (idle
tales); a bleak grief wind as the women watch Him die afar and see the burial;
their dawn footsteps returning to the tomb; a soft radiant warmth as the two
shining men appear; a held-breath hollow for 'He is not here, but is risen'
(the score carries the reveal, no choir pad); then rising dawn warmth from the
kept-promise through the CTA to the risen-Christ close. SFX = ambience/accents
only; the dark->grace score carries the emotion. Beat times from the 82.04s cut
(+1.5s outro hold = 83.54s).
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\batches\cluster_02_resurrection"
           r"\women_first_witnesses_luke245\visual\women_first_witnesses_luke245_scored.mp4")
OUT = CUT.with_name("women_first_witnesses_luke245_sfx.mp4")

LAYERS = [
    # indoor stone room — hook + "idle tales" + the apologetic middle (beats 1-5)
    layer("room",    "air_hollow_desolate",  "loop",    0.0, 21.5, -41.0, filt="lowpass=f=2800", fin=1.0, fout=1.5),
    # grief — "they watched Him die" (afar) + "where He was buried" (beats 7-8)
    layer("grief",   "wind_desert_bleak",    "loop",    26.5, 5.7, -38.0, fin=1.0, fout=1.5),
    # "At dawn, they were back" — footfalls returning to the tomb (beat 9)
    layer("dawnstep","footsteps_dirt_approach", "oneshot", 32.6, 2.0, -34.0, fout=0.6),
    layer("dawnwind","wind_desert_bleak",    "loop",    32.2, 6.2, -43.0, filt="lowpass=f=3400", fin=1.0, fout=1.0),
    # the two shining men appear — soft radiant presence (beat 10)
    layer("radiance","dawn_morning_warm",    "loop",    38.4, 5.0, -40.0, filt="lowpass=f=3400", fin=2.0, fout=1.5),
    # "He is not here, but is risen" — held-breath hollow (score heartbeat lives here, beat 11)
    layer("hush",    "air_hollow_desolate",  "loop",    43.27, 6.0, -42.0, filt="lowpass=f=2800", fin=1.5, fout=2.0),
    # the promise kept / "the first to know" — dawn warmth begins to build (beats 15-16)
    layer("dawn1",   "dawn_morning_warm",    "loop",    63.6, 9.4, -39.0, filt="lowpass=f=3400", fin=2.5, fout=1.5),
    # "to the overlooked" -> CTA -> risen close — full dawn warmth (beats 17-18 + outro)
    layer("dawn2",   "dawn_morning_warm",    "loop",    73.0, 10.5, -36.0, filt="lowpass=f=3400", fin=2.0),
    # --- VIRAL ACCENTS (tasteful; reverence preserved — build-and-hush, not hype drop) ---
    # low sub RISER building anticipation INTO the angel reveal, resolves before it (38.4)
    layer("riser",   "rumble_deep_sub",      "loop",    36.4, 2.0, -29.0, filt="lowpass=f=1600", fin=1.9, fout=0.15),
    # the great stone ROLLS — accent on the empty-tomb reveal / "the first to know" (beat 14)
    layer("stone",   "stone_roll_tomb",      "oneshot", 63.5, 3.5, -19.0, fout=1.0),
]

if __name__ == "__main__":
    sfxlib.show_plan("Women as First Witnesses (Luke 24:5-6)", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
