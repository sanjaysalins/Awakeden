"""Episode 12 v3 - sparse $0 SFX bed (sound_library reuse via sfx_pilots/sfxlib).

Under the owner's score and the voice, kept low: lamp crackle in the room, water
during the washing, Judas's footsteps on stone as he walks out, cool night air
once the door stands open, lamp again for the landing.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EP = HERE.parent
sys.path.insert(0, str(EP.parents[1] / "sfx_pilots"))
import sfxlib  # noqa: E402
from sfxlib import layer  # noqa: E402

SRC = HERE / "EP12_REMOTION_v1.mp4"
OUT = EP / "swirls_episode_12_ye_are_not_all_clean_v3_final_sfx.mp4"
TOTAL = 81.33

LAYERS = [
    layer("room_lamp", "fire_crackling", "loop", 0.0, 51.9, -54.0, filt="lowpass=f=3500", fin=1.5, fout=2.0),
    layer("washing_water", "river_well_water", "loop", 29.9, 6.6, -48.0, fin=0.6, fout=1.2),
    layer("judas_steps", "footsteps_stone", "loop", 51.7, 4.6, -47.0, fin=0.3, fout=1.5),
    layer("night_air", "wind_desert_bleak", "loop", 51.9, 18.0, -54.0, filt="lowpass=f=1800", fin=2.0, fout=3.0),
    layer("landing_lamp", "fire_crackling", "loop", 69.6, TOTAL - 69.6, -55.0, filt="lowpass=f=3500", fin=2.0, fout=2.5),
]

if __name__ == "__main__":
    sfxlib.show_plan("Ep 12 v3 -- Ye Are Not All Clean", LAYERS)
    sfxlib.build(SRC, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT, regions=[("supper", 0, 21.6), ("washing", 21.6, 41.0), ("unto the end", 41.0, 51.6),
                                 ("night", 51.6, 66.8), ("landing+music end", 66.8, TOTAL)])
