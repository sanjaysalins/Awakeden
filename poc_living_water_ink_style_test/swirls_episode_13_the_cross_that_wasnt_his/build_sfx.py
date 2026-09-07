"""Ambient/SFX bed for episode 13, "The Cross That Wasn't His" (Mark 15:20-21
/ Luke 23:26, Simon of Cyrene; Hebrews 13:11-13). Reuses the shared sfxlib.py
mix pattern, $0, reuse-only from sound_library.

Retimed to `unit_timing.json`'s REAL per-word alignment boundaries (score-
design-early): front 0-5.699 (the hook -- walking the wrong way), f01
5.699-15.299 (the compulsion -- soldiers, Simon named), f02 15.299-25.059
(the beam laid on him, "nobody asked"), f03 25.059-35.899 (THE GOSPEL TURN --
Simon turns, walks out too), f04 35.899-42.520 (the word -- "without"), f05
42.520-54.479 (the type -- the sin offering), f06 54.479-67.180 (HERO --
"suffered without the gate"), f07 67.180-75.080 (strings/camera-turn --
"Hebrews turns to you"), f08 75.080-82.220 (reproach is shame), f09
82.220-92.900 (the CTA -- "you are asked"), back 92.900-106.431 (the landing,
including the +3.0s INV-26 hold).

Design: entirely outdoors on a dry road at a city gate -- no water, no crowd
anywhere in this episode (every still's own spec repeats "no water anywhere",
"no hill, no crosses, no crowd"), so no water or crowd asset is used at all.
A single bleak desert wind carries the whole "compelled" half of the piece
(front through f05, the compulsion and the sin-offering typology), the same
register ep7/ep11 used for their own outdoor throughlines. Soldiers'
armor marks the compulsion specifically (f01+f02, before Simon's own turn) --
gone by f03, since from the turn on this is Simon's own road, not the
soldiers' errand. One gate-creak oneshot lands exactly at f01's start ("led
him out") -- the one moment the gate itself is crossed under compulsion; not
reused at F03's later, freely-chosen turn (a different gate-crossing, no
creak, so the two are never confused). One footsteps oneshot lands exactly
at f03's start, marking Simon's own first step of the turn itself. F06 (the
hero, "suffered without the gate") is intentionally left BARE -- no ambience
layer at all, words + score alone, the same "let the words carry it" rule
this project's own score/SFX design has used at every prior episode's
resolution beat (ep8/ep10/ep11). The wind returns from f07 (the camera turns
to address the viewer directly, strings entering in the score) through the
landing -- NOT a dawn cue: unlike ep11's back cover (dawn), THIS episode's
back cover art is explicit DUSK (the gate seen "from outside at dusk"), so
reusing ep11's dawn_morning_warm layer here would misrepresent the art; the
wind simply continues, unchanged in character, into the landing hold.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode_13_the_cross_that_wasnt_his\\build_sfx.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "sfx_pilots"))
import sfxlib  # noqa: E402
from sfxlib import layer  # noqa: E402

CUT = HERE / "swirls_episode_13_the_cross_that_wasnt_his_final_piano.mp4"
OUT = HERE / "swirls_episode_13_the_cross_that_wasnt_his_final_piano_sfx.mp4"

LAYERS = [
    layer("wind_compelled", "wind_desert_bleak",       "loop",    0.000, 54.479, -46.0, fin=2.0, fout=3.0),
    layer("gate_creak",     "door_gate_creak",          "oneshot", 5.699,  5.000, -30.0, fin=0.0, fout=1.0),
    layer("soldiers",       "soldiers_march_armor",     "loop",    5.699, 19.360, -42.0, fin=1.0, fout=2.0),
    layer("simon_turns",    "footsteps_dirt_approach",  "oneshot", 25.059, 4.000, -38.0, fin=0.0, fout=1.5),
    # f06 (54.479-67.180, the hero -- "suffered without the gate") deliberately bare: no layer.
    layer("wind_return",    "wind_desert_bleak",        "loop",   67.180, 39.251, -46.0, fin=3.0, fout=4.0),
]

if __name__ == "__main__":
    sfxlib.show_plan("Episode 13 -- The Cross That Wasn't His", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT, regions=[
        ("front hook", 0.0, 5.699), ("f01 compulsion", 5.699, 15.299),
        ("f02 nobody asked", 15.299, 25.059), ("f03 gospel turn", 25.059, 35.899),
        ("f04 the word", 35.899, 42.520), ("f05 the type", 42.520, 54.479),
        ("f06 HERO bare", 54.479, 67.180), ("f07 strings/turn", 67.180, 75.080),
        ("f08 reproach", 75.080, 82.220), ("f09 the CTA", 82.220, 92.900),
        ("back landing+hold", 92.900, 106.431),
    ])
