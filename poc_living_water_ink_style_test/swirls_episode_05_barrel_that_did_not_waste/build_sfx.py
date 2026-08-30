"""Ambient/SFX bed for episode 5, "The Barrel That Did Not Waste" (1 Kings
17:8-16 + Luke 4:25-26) -- reuses the shared sfxlib.py mix pattern, $0,
reuse-only from sound_library.

Layer map keyed to the locked unit timeline (from the real assembled
final's own held durations, cross-checked against the assemble log's own
[plan] output): front 0-4.03 (the widow gathering sticks, the hook's own
image), f01 4.03-10.83 (the meeting at the gate), f02 10.83-19.87 (her
fear peak -- "we may eat it, and die"), f03 19.87-30.07 (the gospel turn
-- "Fear not," the first blue thread), f04 30.07-39.10 (the miracle --
"wasted not," indoors), f05 39.10-50.83 (Jesus's own citation, the NT
gospel-link page, the Nazareth crowd), f06 50.83-57.63 (the reflection --
the one lit house), back 57.63-68.51 (the landing, "He needs it open,"
including the +3.0s INV-26 hold).

Design, deliberately restrained from the start (Naaman ep4 needed two
rounds of "too loud" fixes before landing right -- this episode starts at
levels close to what Naaman's FINAL locked mix used, not its first
attempt): one continuous coastal-famine wind bed carries the whole
outdoor-into-early-indoor throughline (front through f04), with a
distant-sea layer establishing Zarephath's own coastline early (this
episode's one real geography difference from Naaman's landlocked river
setting) then receding once the story moves indoors. F02, the fear peak,
gets no new layer at all -- the wind bed alone, already quiet, carries
the "held breath" discipline the same way Naaman's own dialogue-dense
pages did. A hearth-fire crackle enters at F04's miracle (a domestic
cooking fire, the narration's own hook-image -- "her own funeral fire" --
inverted) and carries through F06 into the back-cover landing, the same
fire now feeding three instead of burning nothing. The one heavenly-choir
swell is reserved for F05, the actual NT gospel-link page (Jesus speaking
the citation in his own voice), matching episode 1's own choice to time
the swell to the gospel claim itself rather than the CTA cover.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "sfx_pilots"))
import sfxlib  # noqa: E402
from sfxlib import layer  # noqa: E402

CUT = HERE / "swirls_episode_05_barrel_that_did_not_waste_final_piano.mp4"
OUT = HERE / "swirls_episode_05_barrel_that_did_not_waste_final_piano_sfx.mp4"

LAYERS = [
    layer("coastal_wind",   "wind_desert_bleak",     "loop",     0.0, 40.0, -44.0, fin=2.0, fout=3.0),
    layer("distant_sea",    "sea_waves_shore",       "loop",     0.5, 10.0, -48.0, fin=2.0, fout=2.5),
    layer("hearth_fire",    "fire_crackling",        "loop",    30.0, 27.0, -38.0, fin=1.5, fout=3.0),
    layer("hometown_crowd", "crowd_murmur_distant",  "loop",    39.5, 10.5, -50.0, filt="lowpass=f=2200", fin=2.0, fout=2.5),
    layer("gospel_choir",   "heavenly_choir_soft",   "oneshot", 41.0,  9.0, -37.0, fin=2.0, fout=3.0),
    layer("landing_dawn",   "dawn_morning_warm",     "loop",    57.6, 11.0, -46.0, fin=2.0, fout=3.0),
]

if __name__ == "__main__":
    sfxlib.show_plan("Episode 5 -- The Barrel That Did Not Waste", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT, regions=[
        ("front the hook", 0.0, 4.03), ("f01 the gate", 4.03, 10.83),
        ("f02 fear peak", 10.83, 19.87), ("f03 Fear not", 19.87, 30.07),
        ("f04 the miracle", 30.07, 39.10), ("f05 NT link/choir", 39.10, 50.83),
        ("f06 reflection", 50.83, 57.63), ("back landing+hold", 57.63, 68.51),
    ])
