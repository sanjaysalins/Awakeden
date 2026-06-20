"""Ambient/SFX bed for 'The Door Was a Body' (John 10:9, $0 reuse).

Kept light because a bespoke ElevenLabs Cinematic-Orchestral SCORE is layered on top.
SFX = ambience + event accents: a cold night wind at the shut door, a soft door-creak at the
opening, a deep low weight under the unreachable high wall, a soft heavenly choir as 'I am the
door' / the pasture opens, a warm door-open under 'the door is already open', distant sheep in
the pasture under the shepherd/come-in gather, and warm dawn into the close. Beat times from the
assembly phrase board (cut 60.57s).
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
           r"\32_The_Door_Was_a_Body\v1\assembly\viral_cut.mp4")
OUT = CUT.with_name("viral_cut_sfx.mp4")

LAYERS = [
    layer("night",    "wind_desert_bleak",  "loop",     0.0, 12.0, -39.0, fin=2.0, fout=4.0),                  # night at the shut door
    layer("shut_door","door_gate_creak",    "oneshot",  0.8,  2.6, -33.0, filt="lowpass=f=2600"),              # the great closed door
    layer("wall",     "rumble_deep_sub",    "loop",     3.0, 12.0, -40.0, filt="lowpass=f=600", fin=2.0, fout=4.0),  # the unreachable high wall
    layer("choir",    "heavenly_choir_soft","loop",    19.4, 10.0, -35.0, fin=3.0, fout=4.0),                  # I am the door / pasture opens
    layer("open_door","door_gate_creak",    "oneshot", 43.2,  2.6, -28.0, filt="lowpass=f=3200"),              # the door is already open
    layer("pasture",  "flock_sheep_field",  "loop",    46.0, 12.0, -37.0, filt="lowpass=f=4500", fin=2.0, fout=4.0),  # gathered, safe, and fed
    layer("dawn",     "dawn_morning_warm",  "loop",    53.0,  7.0, -34.0, filt="lowpass=f=3400", fin=3.0),     # the pasture was waiting — come
]

if __name__ == "__main__":
    sfxlib.show_plan("The Door Was a Body", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
