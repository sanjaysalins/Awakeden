"""Ambient/SFX bed for 'Father, forgive them' (Luke 23:34), livingpage rebuild.

Kept light — a Suno-library music score is already layered onto
father_forgive_them_scored.mp4 (SFX = ambience/accents only, never a
choir/musical pad under the score, per feedback-no-choir-pad-under-score).
Bed: a continuous quiet desolate-air base under the whole 57s, with the
nail (hook), the soldiers' dice (proof), Golgotha wind, the veil tearing
(conviction turn), and a warm dawn rising through the risen/mercy landing.
Sacred red-letter beat (beat 6, "Father, forgive them...") is deliberately
left bare of any new accent — the base bed alone, kept low, no punch.
Beat times from livingpage_short.spec.json (57.15s, 16 beats).
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

SRC = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\batches\cluster_01_cross"
           r"\father_forgive_them\visual\father_forgive_them_scored.mp4")
OUT = SRC.with_name("father_forgive_them_sfx.mp4")

LAYERS = [
    # continuous quiet base -- desolate air under the whole piece (extended for the
    # 3.0s outro hold added 2026-07-19 -- the CTA needs room to linger, not cut dead)
    layer("air",    "air_hollow_desolate",     "loop", 0.0,  60.1, -42.0, fin=1.0, fout=3.0),
    # beat 1: the nail through his hand
    layer("nail",   "nail_strike_single",      "oneshot", 0.25, 1.0, -24.0),
    # beats 2-3: soldiers gambling for his clothes + the mocking crowd
    layer("dice",   "coins_clinking",          "loop", 3.4,  7.0, -30.0, fin=0.5, fout=1.5),
    layer("mock",   "crowd_murmur_distant",    "loop", 7.0,  6.0, -34.0, fin=0.8, fout=2.0),
    # beats 5-6: Golgotha wind under the prayer -- kept low, no new accent on the red-letter itself
    layer("wind1",  "wind_desert_bleak",       "loop", 12.46, 9.6, -38.0, fin=1.5, fout=2.5),
    # beat 7-8: "Luke records it... cast lots" -- dice fading out under the scroll/typography panel
    layer("dice2",  "coins_clinking",          "loop", 22.06, 5.9, -34.0, fin=0.3, fout=2.0),
    # beat 10: Golgotha hill wide, the weight of "ours too"
    layer("thunder","thunder_low_roll",        "loop", 32.37, 6.5, -33.0, fin=1.0, fout=2.0),
    # beat 11: the veil torn -- the conviction turn
    layer("veil",   "veil_tearing",            "oneshot", 37.0, 2.2, -22.0),
    # beats 12-14: risen, interceding, "while we were yet sinners" -- warmth rising
    layer("choir",  "heavenly_choir_soft",     "loop", 39.8, 12.05, -36.0, fin=2.0, fout=2.0),
    # beats 15-16 + the 3.0s outro hold: the mercy hand held out, the landing lingers
    layer("dawn",   "dawn_morning_warm",       "loop", 51.85, 8.3, -32.0, fin=1.5, fout=2.5),
]

if __name__ == "__main__":
    sfxlib.show_plan("Father, forgive them", LAYERS)
    sfxlib.build(SRC, OUT, LAYERS)
    print(f"[ok] {OUT}")
    sfxlib.measure(OUT)
