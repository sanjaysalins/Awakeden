"""Ambient/SFX beds for the 10 cluster-1 Cross shorts + the inked Psalm 22 LONG (L1+L3).

One bespoke layer map per piece, synced to its livingpage spec beats. Reuse-only from
sound_library ($0). Levels conservative (loops -36..-42dB, accents -27..-34dB); the
narration ducks the bed via sfxlib's sidechain; sacred bars stay quiet (the score dips
already clear those windows — the bed adds ambience, never slams). Pieces whose BUILD
already embeds spec-level sfx (it_is_finished, into_thy_hands hooks etc.) get thinner
beds so nothing doubles.

  .venv\\Scripts\\python.exe sfx_pilots/build_cluster1_sfx.py            # all 11
  .venv\\Scripts\\python.exe sfx_pilots/build_cluster1_sfx.py pierced    # substring filter
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sfxlib
from sfxlib import layer

REPO = HERE.parent
CL = REPO / "batches" / "cluster_01_cross"


def cut(piece: str) -> Path:
    # (father_forgive_them migrated to the standard livingpage layout 2026-07-15;
    # its old mocomic special-case path is gone)
    return CL / piece / "visual" / f"{piece}_scored.mp4"


PIECES: dict[str, list] = {
    # 57.15s — nails -> gambling -> the prayer -> Ps22 receipt -> ours too -> risen mercy
    # (Wave E livingpage migration 2026-07-15. Build embeds nail_strike + dawn accents +
    # heartbeat 28-36.2 + veil_tearing at the border-break - the bed stays UNDER those.)
    "father_forgive_them": [
        layer("wind",   "wind_desert_bleak",    "loop",    0.0, 16.9, -40.0, fin=0.5, fout=2.0),
        layer("lots",   "coins_clinking",       "oneshot", 4.6, 2.2,  -32.0, fout=0.8),
        layer("crowd",  "crowd_murmur_distant", "loop",    7.0, 3.3,  -39.0, fin=0.8, fout=1.0),
        layer("hollow", "air_hollow_desolate",  "loop",   16.9, 11.1, -39.0, filt="lowpass=f=3000", fin=1.5, fout=1.5),
        layer("lamp",   "fire_crackling",       "loop",   22.1, 5.9,  -42.0, filt="lowpass=f=4200", fin=1.0, fout=1.0),
        layer("rumble", "rumble_deep_sub",      "oneshot",36.3, 4.0,  -34.0, fout=2.5),
    ],
    # 72.54s — David writes it, soldiers gamble it: night scroll -> Golgotha -> lots -> dawn
    "crucifixion_foretold_ps2218": [
        layer("wind",   "wind_desert_bleak",   "loop",    0.0, 31.0, -40.0, fin=0.5, fout=2.0),
        layer("scroll", "fire_crackling",      "loop",    6.5, 9.7,  -41.0, filt="lowpass=f=4200", fin=1.0, fout=1.5),
        layer("crowd",  "crowd_murmur_distant","loop",   16.2, 15.3, -39.0, fin=1.5, fout=1.5),
        layer("lots1",  "coins_clinking",      "oneshot",31.6, 2.2,  -30.0, fout=0.8),
        layer("lots2",  "coins_clinking",      "oneshot",41.3, 2.2,  -31.0, fout=0.8),
        layer("night2", "fire_crackling",      "loop",   56.1, 2.0,  -41.0, filt="lowpass=f=4200", fin=0.5, fout=0.5),
        layer("dawn",   "dawn_morning_warm",   "loop",   63.3, 9.2,  -36.0, filt="lowpass=f=3400", fin=2.0),
    ],
    # 58.18s — darkness -> the cry -> ninth hour -> grace poured -> dawn
    "forsaken_cry_ps221": [
        layer("rumble", "rumble_deep_sub",     "oneshot", 0.1, 4.0,  -33.0, fout=2.5),
        layer("wind",   "wind_desert_bleak",   "loop",    0.0, 27.0, -39.0, fin=0.5, fout=2.0),
        layer("hollow", "air_hollow_desolate", "loop",   22.6, 12.0, -38.0, filt="lowpass=f=3000", fin=1.5, fout=2.0),
        layer("dawn",   "dawn_morning_warm",   "loop",   47.9, 10.3, -36.0, filt="lowpass=f=3400", fin=2.5),
    ],
    # 55.74s — every ocean -> dry potsherd -> I thirst -> living water -> dawn
    "i_thirst_john1928": [
        layer("ocean",  "sea_waves_shore",     "loop",    0.0, 5.5,  -36.0, fin=0.3, fout=1.2),
        layer("dry",    "wind_desert_bleak",   "loop",    4.9, 27.5, -39.0, fin=1.5, fout=2.0),
        layer("water",  "river_well_water",    "loop",   44.0, 9.3,  -37.0, fin=1.2, fout=1.5),
        layer("dawn",   "dawn_morning_warm",   "loop",   49.4, 6.3,  -37.0, filt="lowpass=f=3400", fin=2.0),
    ],
    # 59.03s — a child's lamp -> darkness -> the Father's hands -> morning (build has hook sfx)
    "into_thy_hands_luke2346": [
        layer("lamp1",  "fire_crackling",      "loop",    4.2, 5.1,  -41.0, filt="lowpass=f=4200", fin=1.0, fout=1.0),
        layer("dark",   "wind_desert_bleak",   "loop",   14.6, 6.6,  -40.0, fin=1.2, fout=1.2),
        layer("home",   "fire_crackling",      "loop",   25.2, 15.8, -42.0, filt="lowpass=f=4200", fin=1.5, fout=2.0),
        layer("dawn",   "dawn_morning_warm",   "loop",   41.8, 17.2, -36.0, filt="lowpass=f=3400", fin=2.5),
    ],
    # 59.09s — Eden -> workshop -> Golgotha -> tomb seal -> morning (spec already carries boom/air/wind/dawn accents: THIN bed)
    "it_is_finished_john1930": [
        layer("eden",   "dawn_morning_warm",   "loop",    0.0, 6.8,  -39.0, filt="lowpass=f=3400", fin=0.5, fout=1.5),
        layer("bench",  "fire_crackling",      "loop",    7.0, 5.0,  -42.0, filt="lowpass=f=4200", fin=1.0, fout=1.0),
        layer("seal",   "stone_roll_tomb",     "oneshot",43.2, 2.2,  -31.0, fout=1.0),
        layer("dawn",   "dawn_morning_warm",   "loop",   48.9, 10.2, -37.0, filt="lowpass=f=3400", fin=2.0),
    ],
    # 59.04s — the spear -> the scroll -> the crowd -> grace poured -> look & live
    "pierced_zech1210": [
        layer("rumble", "rumble_deep_sub",     "oneshot", 0.1, 3.0,  -33.0, fout=2.0),
        layer("scroll", "fire_crackling",      "loop",    2.9, 9.1,  -41.0, filt="lowpass=f=4200", fin=1.0, fout=1.2),
        layer("crowd",  "crowd_murmur_distant","loop",   21.6, 10.4, -38.0, fin=1.2, fout=1.5),
        layer("wind",   "wind_desert_bleak",   "loop",   12.0, 24.0, -41.0, fin=1.5, fout=2.0),
        layer("dawn",   "dawn_morning_warm",   "loop",   38.1, 20.9, -36.0, filt="lowpass=f=3400", fin=3.0),
    ],
    # 59.08s — coins have a sound: scatter -> weighed -> cast down -> blood money -> go free
    "thirty_pieces_zech11": [
        layer("coins0", "coins_clinking",      "oneshot", 0.1, 2.4,  -29.0, fout=0.8),
        layer("scroll", "fire_crackling",      "loop",    5.2, 6.8,  -41.0, filt="lowpass=f=4200", fin=1.0, fout=1.2),
        layer("weigh",  "coins_clinking",      "oneshot", 9.7, 2.0,  -31.0, fout=0.8),
        layer("temple", "marketplace_chatter", "loop",   28.4, 6.0,  -40.0, fin=1.0, fout=1.0),
        layer("cast",   "coins_clinking",      "oneshot",31.2, 2.4,  -28.0, fout=0.8),
        layer("scatter","coins_clinking",      "oneshot",34.5, 2.0,  -30.0, fout=0.8),
        layer("wind",   "wind_desert_bleak",   "loop",   38.8, 12.0, -40.0, fin=1.5, fout=1.5),
        layer("dawn",   "dawn_morning_warm",   "loop",   56.8, 2.3,  -37.0, filt="lowpass=f=3400", fin=1.0),
    ],
    # 59.07s — two crosses in a storm -> the confession -> paradise dawn
    "today_paradise_luke2343": [
        layer("wind",   "wind_desert_bleak",   "loop",    0.0, 19.0, -39.0, fin=0.5, fout=2.0),
        layer("thunder","thunder_low_roll",    "oneshot", 7.9, 3.5,  -33.0, fout=2.0),
        layer("crowd",  "crowd_murmur_distant","loop",    7.8, 8.0,  -40.0, fin=1.0, fout=1.2),
        layer("hollow", "air_hollow_desolate", "loop",   18.8, 13.2, -39.0, filt="lowpass=f=3000", fin=1.5, fout=1.5),
        layer("dawn",   "dawn_morning_warm",   "loop",   42.8, 16.3, -36.0, filt="lowpass=f=3400", fin=3.0),
    ],
    # 59.0s — Gethsemane night: quiet wind, the cup, the sleeping men, warm close
    "watch_one_hour_matt2640": [
        layer("night",  "wind_desert_bleak",   "loop",    0.0, 42.0, -41.0, fin=0.5, fout=2.5),
        layer("hollow", "air_hollow_desolate", "loop",   11.0, 11.0, -41.0, filt="lowpass=f=3000", fin=1.5, fout=1.5),
        layer("dawn",   "dawn_morning_warm",   "loop",   48.7, 10.3, -37.0, filt="lowpass=f=3400", fin=2.5),
    ],
    # 59.06s — Simeon's temple -> the sword -> the cross -> John takes her HOME
    "woman_behold_john1926": [
        layer("temple", "crowd_murmur_distant","loop",    0.0, 7.5,  -41.0, fin=0.5, fout=1.0),
        layer("wind",   "wind_desert_bleak",   "loop",    7.8, 24.0, -40.0, fin=1.2, fout=1.5),
        layer("steps",  "footsteps_dirt_approach","oneshot",36.3, 3.0, -34.0, fout=1.0),
        layer("door",   "door_gate_creak",     "oneshot",39.9, 1.8,  -34.0, fout=0.6),
        layer("home",   "fire_crackling",      "loop",   40.2, 7.5,  -42.0, filt="lowpass=f=4200", fin=1.0, fout=1.5),
        layer("dawn",   "dawn_morning_warm",   "loop",   49.2, 9.9,  -36.0, filt="lowpass=f=3400", fin=2.0),
    ],
    # 60s pilot — the mob, the nails (already scored+mixed by add_music_sfx; SKIP by default)
    # ---- Wave F ps22 rebuilds (2026-07-15): 5 inked living-page shorts ----
    # 78.02s — mocking crowd -> David writes -> wagging heads -> rulers sneer -> He stayed -> dawn
    "mockers_words_ps227": [
        layer("crowd0", "crowd_murmur_distant","loop",    0.0, 4.4,  -39.0, fin=0.4, fout=1.0),
        layer("scroll", "fire_crackling",      "loop",    4.6, 5.4,  -41.0, filt="lowpass=f=4200", fin=1.0, fout=1.2),
        layer("wind",   "wind_desert_bleak",   "loop",   10.1, 21.8, -40.0, fin=1.5, fout=2.0),
        layer("crowd1", "crowd_murmur_distant","loop",   19.3, 9.5,  -41.0, fin=1.2, fout=1.5),
        layer("lots",   "coins_clinking",      "oneshot",34.6, 2.2,  -32.0, fout=0.8),
        layer("hollow", "air_hollow_desolate", "loop",   41.0, 7.1,  -39.0, filt="lowpass=f=3000", fin=1.5, fout=1.5),
        layer("wind2",  "wind_desert_bleak",   "loop",   48.1, 15.1, -41.0, fin=1.5, fout=2.0),
        layer("dawn",   "dawn_morning_warm",   "loop",   68.5, 9.5,  -37.0, filt="lowpass=f=3400", fin=2.5),
    ],
    # 58.96s — darkness open -> psalm turn -> the congregation -> risen -> family -> dawn
    "declared_brethren_ps2222": [
        layer("hollow", "air_hollow_desolate", "loop",    0.0, 7.4,  -39.0, filt="lowpass=f=3000", fin=0.5, fout=1.5),
        layer("scroll", "fire_crackling",      "loop",    7.4, 8.5,  -41.0, filt="lowpass=f=4200", fin=1.2, fout=1.5),
        layer("hall",   "crowd_murmur_distant","loop",   16.0, 5.8,  -42.0, fin=1.2, fout=1.5),
        layer("wind",   "wind_desert_bleak",   "loop",   21.9, 10.3, -41.0, fin=1.5, fout=1.5),
        layer("stone",  "stone_roll_tomb",     "oneshot",32.4, 2.4,  -33.0, fout=1.0),
        layer("dawn",   "dawn_morning_warm",   "loop",   36.6, 22.4, -37.0, filt="lowpass=f=3400", fin=3.0),
    ],
    # 42.70s — David + bowed head -> done -> vinegar -> finished -> home lamp -> dawn
    "he_hath_done_this_ps2231": [
        layer("scroll", "fire_crackling",      "loop",    0.0, 7.9,  -41.0, filt="lowpass=f=4200", fin=0.5, fout=1.2),
        layer("wind",   "wind_desert_bleak",   "loop",    7.9, 12.6, -41.0, fin=1.5, fout=1.5),
        layer("hollow", "air_hollow_desolate", "loop",   20.5, 5.4,  -40.0, filt="lowpass=f=3000", fin=1.2, fout=1.2),
        layer("wind2",  "wind_desert_bleak",   "loop",   25.9, 10.6, -41.0, fin=1.5, fout=1.5),
        layer("home",   "fire_crackling",      "loop",   36.5, 4.0,  -41.0, filt="lowpass=f=4200", fin=1.0, fout=1.0),
        layer("dawn",   "dawn_morning_warm",   "loop",   40.5, 2.2,  -38.0, filt="lowpass=f=3400", fin=0.8),
    ],
    # 67.50s — one forsaken man -> all nations turn -> tomb -> worship -> landing rays
    "ends_of_earth_ps2227": [
        layer("hollow", "air_hollow_desolate", "loop",    0.0, 7.5,  -39.0, filt="lowpass=f=3000", fin=0.5, fout=1.5),
        layer("wind",   "wind_desert_bleak",   "loop",    7.5, 14.0, -40.0, fin=1.5, fout=1.5),
        layer("nations","crowd_murmur_distant","loop",   16.8, 4.6,  -42.0, fin=1.2, fout=1.2),
        layer("wind2",  "wind_desert_bleak",   "loop",   21.5, 11.1, -40.0, fin=1.5, fout=1.5),
        layer("stone",  "stone_roll_tomb",     "oneshot",32.8, 2.4,  -33.0, fout=1.0),
        layer("worship","crowd_murmur_distant","loop",   39.4, 6.5,  -40.0, fin=1.2, fout=1.5),
        layer("dawn",   "dawn_morning_warm",   "loop",   48.1, 19.4, -36.0, filt="lowpass=f=3400", fin=3.0),
    ],
    # 66.94s — David writes -> watch the body -> bones out of joint -> staring crowd -> crushed for you
    "body_foretold_ps2214": [
        layer("scroll", "fire_crackling",      "loop",    0.0, 10.0, -41.0, filt="lowpass=f=4200", fin=0.5, fout=1.5),
        layer("wind",   "wind_desert_bleak",   "loop",   10.1, 8.2,  -40.0, fin=1.5, fout=1.5),
        layer("hollow", "air_hollow_desolate", "loop",   18.3, 12.9, -40.0, filt="lowpass=f=3000", fin=1.5, fout=2.0),
        layer("wind2",  "wind_desert_bleak",   "loop",   31.2, 13.4, -41.0, fin=1.5, fout=1.5),
        layer("stare",  "crowd_murmur_distant","loop",   38.6, 6.1,  -40.0, fin=1.2, fout=1.5),
        layer("rumble", "rumble_deep_sub",     "oneshot",52.6, 3.5,  -34.0, fout=2.0),
        layer("dawn",   "dawn_morning_warm",   "loop",   59.9, 7.0,  -37.0, filt="lowpass=f=3400", fin=2.5),
    ],
}

# ---- the inked Psalm 22 LONG (418.2s, 7 movements) --------------------------------
LONG_CUT = (REPO / "longform" / "02_Psalm_22_Song_From_The_Cross" / "v1"
            / "visual_16x9" / "LivingPage_Psalm22_16x9_scored.mp4")
LONG_LAYERS = [
    # M1 the cry (0-45): storm over Jerusalem
    layer("m1wind",  "wind_desert_bleak",   "loop",    0.0, 45.0, -39.0, fin=0.5, fout=3.0),
    layer("m1thund", "thunder_low_roll",    "oneshot", 4.1, 4.0,  -32.0, fout=2.5),
    layer("m1crowd", "crowd_murmur_distant","loop",   35.0, 10.0, -41.0, fin=1.5, fout=1.5),
    # M2 David + the scribes (45-98): lamplit rooms
    layer("m2fire",  "fire_crackling",      "loop",   44.9, 53.0, -42.0, filt="lowpass=f=4200", fin=2.5, fout=2.5),
    # M3 the execution anatomy (98-143): bleak
    layer("m3hollow","air_hollow_desolate", "loop",   98.0, 45.0, -39.0, filt="lowpass=f=3000", fin=2.5, fout=2.5),
    # M4 garments + lots (143-210): the crowd, the dice
    layer("m4crowd", "crowd_murmur_distant","loop",  143.0, 60.0, -40.0, fin=2.0, fout=2.0),
    layer("m4lots",  "coins_clinking",      "oneshot",148.8, 2.2, -31.0, fout=0.8),
    layer("m4lots2", "coins_clinking",      "oneshot",201.9, 2.0, -32.0, fout=0.8),
    # M5 Alexandria (210-233): the harbor
    layer("m5sea",   "sea_waves_shore",     "loop",  213.9, 19.0, -39.0, fin=2.0, fout=2.0),
    # M6 the turn (233-296): stillness, then the tomb opens
    layer("m6wind",  "wind_desert_bleak",   "loop",  233.0, 56.0, -42.0, fin=2.5, fout=2.0),
    layer("m6stone", "stone_roll_tomb",     "oneshot",289.3, 2.5, -30.0, fout=1.0),
    # M7 risen -> the nations -> COME (296-418): dawn all the way home
    layer("m7dawn",  "dawn_morning_warm",   "loop",  296.2, 122.0,-37.0, filt="lowpass=f=3400", fin=4.0),
    layer("m7cong",  "crowd_murmur_distant","loop",  337.0, 14.0, -42.0, fin=2.0, fout=2.0),
    layer("m7stone", "stone_roll_tomb",     "oneshot",327.6, 2.2, -32.0, fout=1.0),
    layer("m7door",  "door_gate_creak",     "oneshot",400.5, 1.8, -34.0, fout=0.6),
]


# ---- the inked Isaiah 53 LONG (405.26s, 95 beats; scored by longform/_add_score_lf.py) ----
ISAIAH_CUT = (REPO / "longform" / "01_Isaiah_53_Suffering_Servant" / "v1"
              / "visual_16x9_inked" / "LivingPage_Isaiah53_16x9_scored.mp4")
ISAIAH_LAYERS = [
    # M1 the lamplit scroll + 700BC Jerusalem (0-22)
    layer("m1fire",  "fire_crackling",      "loop",    0.0, 19.0, -41.0, filt="lowpass=f=4200", fin=0.5, fout=2.0),
    # M2 the report -> exalted -> marred (22-65): open air, then the picture breaks
    layer("m2wind",  "wind_desert_bleak",   "loop",   19.0, 28.0, -41.0, fin=2.0, fout=2.0),
    layer("m2thund", "thunder_low_roll",    "oneshot",49.9, 3.5,  -34.0, fout=2.0),
    # M3 despised and rejected (65-90): the crowd that looks away
    layer("m3crowd", "crowd_murmur_distant","loop",   64.7, 14.9, -40.0, fin=1.5, fout=1.5),
    layer("m3wind",  "wind_desert_bleak",   "loop",   79.6, 19.4, -40.0, fin=1.5, fout=1.5),
    # M4 the transaction (99-135): sacred hollow under the wounds verses
    layer("m4hollow","air_hollow_desolate", "loop",   99.0, 29.0, -40.0, filt="lowpass=f=3000", fin=2.0, fout=2.0),
    layer("m4sheep", "flock_sheep_field",   "loop",  128.4, 4.2,  -40.0, fin=0.8, fout=1.0),
    # M5 the silent lamb (142-158): torch-lit trial night
    layer("m5torch", "fire_crackling",      "loop",  142.4, 11.4, -41.0, filt="lowpass=f=4200", fin=1.2, fout=1.5),
    # M6 the honest question / Israel (158-234): study air, the exile road
    layer("m6wind",  "wind_desert_bleak",   "loop",  158.0, 32.0, -42.0, fin=2.0, fout=2.0),
    layer("m6exile", "crowd_murmur_distant","loop",  167.3, 4.1,  -42.0, fin=1.0, fout=1.0),
    layer("m6hollow","air_hollow_desolate", "loop",  195.8, 17.9, -40.0, filt="lowpass=f=3000", fin=1.5, fout=2.0),
    # M7 the eunuch's chariot (234-282): hooves + wheels on the desert road (diegetic star)
    layer("m7wind",  "wind_desert_bleak",   "loop",  234.0, 48.0, -42.0, fin=2.0, fout=2.0),
    layer("m7hooves","horse_hooves_walk",   "loop",  237.6, 24.5, -39.0, fin=1.2, fout=2.0),
    layer("m7wheels","chariot_wheels_road", "loop",  238.0, 24.0, -40.0, fin=1.2, fout=2.0),
    # M8 it pleased the LORD to bruise him (282-306): darkness
    layer("m8rumble","rumble_deep_sub",     "oneshot",285.4, 4.0, -34.0, fout=2.5),
    layer("m8hollow","air_hollow_desolate", "loop",  282.2, 23.5, -39.0, filt="lowpass=f=3000", fin=1.5, fout=2.5),
    # M9 the morning turn (306-342): dawn + the stone
    layer("m9dawn",  "dawn_morning_warm",   "loop",  305.7, 36.3, -37.0, filt="lowpass=f=3400", fin=3.0, fout=2.0),
    layer("m9stone", "stone_roll_tomb",     "oneshot",318.3, 2.4, -33.0, fout=1.0),
    # M10 back to the lamp -> verse six -> the name (342-405): warm all the way home
    layer("m10fire", "fire_crackling",      "loop",  342.0, 5.3,  -41.0, filt="lowpass=f=4200", fin=1.0, fout=1.2),
    layer("m10wind", "wind_desert_bleak",   "loop",  347.3, 16.8, -42.0, fin=2.0, fout=2.0),
    layer("m10dawn", "dawn_morning_warm",   "loop",  364.1, 41.2, -36.0, filt="lowpass=f=3400", fin=3.0),
]


def main():
    flt = sys.argv[1] if len(sys.argv) > 1 else ""
    built = []
    for piece, layers in PIECES.items():
        if flt and flt not in piece:
            continue
        src = cut(piece)
        out = src.with_name(src.name.replace("_scored.mp4", "_sfx.mp4"))
        sfxlib.show_plan(piece, layers)
        sfxlib.build(src, out, layers)
        sfxlib.measure(out)
        built.append(out)
    if not flt or "psalm" in flt.lower() or "long" in flt.lower():
        out = LONG_CUT.with_name(LONG_CUT.name.replace("_scored.mp4", "_scored_sfx.mp4"))
        sfxlib.show_plan("PSALM 22 LONG (inked)", LONG_LAYERS)
        sfxlib.build(LONG_CUT, out, LONG_LAYERS)
        sfxlib.measure(out)
        built.append(out)
    if (not flt or "isaiah" in flt.lower() or "long" in flt.lower()) and ISAIAH_CUT.exists():
        out = ISAIAH_CUT.with_name(ISAIAH_CUT.name.replace("_scored.mp4", "_scored_sfx.mp4"))
        sfxlib.show_plan("ISAIAH 53 LONG (inked)", ISAIAH_LAYERS)
        sfxlib.build(ISAIAH_CUT, out, ISAIAH_LAYERS)
        sfxlib.measure(out)
        built.append(out)
    print("\nBUILT:")
    for b in built:
        print(" ", b)


if __name__ == "__main__":
    main()
