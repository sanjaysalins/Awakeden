"""Ambient/SFX bed for the Bethesda 'Far Corner' POC episode (John 5:1-9).

Kept light -- a cinematic music_library SCORE (sacred_grace_rise, glory_holy_stillness
layer) is already muxed in; SFX here is ambience/accent only, never a musical pad.
Arc: distant crowd murmur under the hook/crowd beats (fades as the camera leaves them
for the far corner), a constant very-quiet pool-water bed throughout (it's a pool
location start to finish), a brief lift on the water at the "stirs" insert, and soft
stone footsteps under Jesus's approach. Beat times from the real word-alignment.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

CUT = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible"
           r"\poc_bethesda_style_test\far_corner_episode\cut_v2_scored.mp4")
OUT = CUT.with_name("cut_v3_sfx.mp4")

LAYERS = [
    layer("crowd",       "crowd_murmur_distant", "loop", 0.0,  16.8,  -32.0, fin=1.0, fout=3.0),   # the porches, the waiting crowd
    layer("water_base",  "river_well_water",      "loop", 0.0,  61.88, -40.0, fin=1.5, fout=2.0),   # the pool, present throughout
    layer("water_stir",  "river_well_water",      "loop", 4.18, 5.0,   -28.0, fin=0.8, fout=1.5),   # "when the water stirs..."
    layer("footsteps",   "footsteps_stone",       "loop", 16.8, 9.24,  -36.0, filt="lowpass=f=3000", fin=0.5, fout=1.0),  # Jesus walks past the crowd
]

if __name__ == "__main__":
    sfxlib.show_plan("29 The Race He Could Never Win (Far Corner)", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
