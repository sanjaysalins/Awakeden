"""Ambient/SFX bed for 'The Well That Never Runs Dry' (John 4, $0 reuse).

Kept light because a bespoke ElevenLabs Cinematic-Orchestral SCORE is layered on top.
SFX = ambience + event accents only: a soft noon desert wind + gentle well-water under
the hook/well scenes, brighter well-water as the living water springs up, a soft heavenly
choir under 'everlasting life' / the risen Christ, the clay waterpot dropping + running feet
exactly on 'she dropped her waterpot and ran', a quiet door-open under 'He still offers it',
and warm dawn into the grace landing. Beat times from the assembly phrase board (cut 59.0s).
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
           r"\08 The Well That Never Runs Dry\v1\assembly\viral_cut.mp4")
OUT = CUT.with_name("viral_cut_sfx.mp4")

LAYERS = [
    layer("noon_wind", "wind_desert_bleak",  "loop",     0.0, 10.0, -39.0, fin=2.0, fout=4.0),                 # well at noon
    layer("well",      "river_well_water",   "loop",     0.0, 18.0, -34.0, filt="lowpass=f=4000", fin=2.0, fout=3.0),  # the well / thirst
    layer("spring",    "river_well_water",   "loop",    18.0,  8.0, -30.0, fin=1.5, fout=3.0),                 # living water springing up
    layer("choir",     "heavenly_choir_soft","loop",    26.5, 11.0, -35.0, fin=3.0, fout=4.0),                 # everlasting life / risen Christ
    layer("waterpot",  "waterpot_drop_run",  "oneshot", 37.4,  3.2, -25.0),                                    # she dropped her waterpot and ran
    layer("door",      "door_gate_creak",    "oneshot", 50.5,  2.2, -31.0, filt="lowpass=f=3000"),             # He still offers it
    layer("dawn",      "dawn_morning_warm",  "loop",    52.0,  7.0, -34.0, filt="lowpass=f=3400", fin=3.0),    # the same grace — come
]

if __name__ == "__main__":
    sfxlib.show_plan("The Well That Never Runs Dry", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
