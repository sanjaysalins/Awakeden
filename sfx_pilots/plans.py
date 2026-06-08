"""Per-episode SFX/ambience maps for the 8 finished shorts (Level A, no music, $0).
Each map syncs its key SOUND SHIFT to a forced-aligned Scripture beat (times verified
in sfx_pilots/work/<safe>.words.json). Gentle levels per the approved #02 storm pilot.
"""
from sfxlib import layer

NARR = r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"

# key: (folder_name, duration_s, [layers])
PLANS = {
    # ── 12 Prodigal: lonely road home → father SEES (23) → RUNS (28.2) → KISS (30.9) → warm welcome
    "12 The Kiss That Cut Off the Bargain": (59.009, [
        layer("road",    "wind_desert_bleak",      "loop",    0.0, 30.8, -30.0, fout=2.0),
        layer("walk",    "footsteps_dirt_approach", "oneshot", 3.2,  4.0, -26.0),
        layer("donkey",  "donkey_bray",            "oneshot", 6.4,  4.0, -33.0),
        layer("run",     "footsteps_dirt_approach", "oneshot", 27.6, 3.0, -22.0),   # father RANS (28.19)
        layer("welcome", "dawn_morning_warm",      "loop",   31.2, 27.8, -32.0, filt="lowpass=f=3000", fin=3.0),  # kiss/embrace → home
    ]),

    # ── 16 Fire: denial NIGHT (charcoal+distant crowd) → MORNING on the SHORE (11.6) restoration; fire = through-line
    "16 The Fire Jesus Built": (59.033, [
        layer("fire",    "fire_crackling",         "loop",    0.0, 59.0, -34.0),       # the coals, always
        layer("denial",  "crowd_murmur_distant",   "loop",    0.0, 11.0, -34.0, fout=2.5),  # the night he denied
        layer("shore",   "sea_waves_shore",        "loop",    9.5, 49.5, -34.0, filt="lowpass=f=2200", fin=2.5),  # morning shore
        layer("dawn",    "dawn_morning_warm",      "loop",   10.0, 49.0, -35.0, filt="lowpass=f=3000", fin=3.0),  # restoration warmth
    ]),

    # ── 18 Bethesda: merciless CROWD at the pool → Jesus singles HIM out "made whole?" (22.1) → crowd drops, intimate → healing warmth
    "18 He Never Said Yes": (59.026, [
        layer("pool",    "river_well_water",       "loop",    0.0, 59.0, -33.0),       # the pool
        layer("crowd",   "crowd_murmur_distant",   "loop",    0.0, 23.0, -33.0, fout=3.0),   # the merciless multitude (fades as He addresses him)
        layer("steps",   "footsteps_stone",        "oneshot", 11.0, 6.0, -26.0),       # Jesus walks straight to him
        layer("heal",    "dawn_morning_warm",      "loop",   45.0, 14.0, -35.0, filt="lowpass=f=3000", fin=3.0),  # rise/come to Him
    ]),

    # ── 32 Door: holy NAME (distant shofar) over the HILLS → "opened a door" creak (7.7) → "come in" footsteps (34.9)
    #    → brief PASTURE glimpse (flock 28-39, fades) → warm dawn carries the close → "step through": footsteps→door (51-54)
    "32_The_Door_Was_a_Body": (60.567, [
        layer("hills",   "wind_desert_bleak",       "loop",    0.0, 60.5, -34.0),
        layer("shofar",  "shofar_blast",            "oneshot", 0.6,  6.0, -27.0, filt="lowpass=f=2500"),  # the holy Name "I AM"
        layer("open",    "door_gate_creak",         "oneshot", 7.7,  5.0, -24.0),       # opened a door
        layer("enter",   "footsteps_dirt_approach", "oneshot", 34.7, 4.0, -25.0),       # come in through Him
        layer("pasture", "flock_sheep_field",       "loop",   28.0, 11.0, -34.0, fin=2.5, fout=3.5),  # a GLIMPSE of pasture
        layer("warm",    "dawn_morning_warm",       "loop",   30.0, 30.5, -34.0, filt="lowpass=f=3000", fin=3.0),  # saved, safe, fed
        layer("stepup",  "footsteps_dirt_approach", "oneshot", 50.9, 3.0, -24.0),       # step through (walk up)
        layer("thru",    "door_gate_creak",         "oneshot", 52.3, 5.0, -24.0),       # the door opens to enter
    ]),

    # ── 33 Shepherd: NIGHT hills + shepherd's watch-FIRE; flock = brief dusk glimpse only → he lies in the gap (footsteps 8.3)
    #    → the WOLF comes first (37.6): rumble + hollow unease → resolve → "you walk across" footsteps (56.8)
    "33_The_Shepherd_In_The_Gap": (60.170, [
        layer("hills",   "wind_desert_bleak",       "loop",    0.0, 60.1, -33.0, filt="lowpass=f=2600"),  # night hills (darker)
        layer("fire",    "fire_crackling",          "loop",    6.0, 54.1, -35.0, fin=3.0),  # the shepherd's night-watch fire
        layer("flock",   "flock_sheep_field",       "loop",    2.0, 11.0, -35.0, fin=2.5, fout=4.0),  # fold settling at dusk (brief)
        layer("lie",     "footsteps_dirt_approach", "oneshot", 8.3,  4.0, -27.0),       # he lies across the gap
        layer("wolf",    "rumble_deep_sub",         "loop",   35.8,  7.2, -30.0, fin=2.0, fout=3.0),  # the wolf comes first
        layer("unease",  "air_hollow_desolate",     "loop",   36.0,  7.0, -34.0, fin=2.0, fout=3.0),  # hollow dread under it
        layer("walk",    "footsteps_dirt_approach", "oneshot", 56.8, 3.0, -25.0),       # you walk across the One
    ]),

    # ── 34 Bread (modern/abstract): hollow ACHE (full but empty) → restless CHURN of "reaching" + the next PLATE (bread)
    #    + the next PURCHASE (coins) ~34-36 → "Come to the BREAD of life" (47) fuller tear → warm fill (the life your soul was made for)
    "34_The_Hunger_Bread_Cant_Fill": (52.886, [
        layer("ache",    "air_hollow_desolate",    "loop",    0.0, 13.0, -35.0, fin=2.0, fout=3.0),  # full, yet empty
        layer("churn",   "marketplace_chatter",    "loop",   23.0, 23.0, -36.0, filt="lowpass=f=1500", fin=3.0, fout=2.5),  # restless reaching
        layer("plate",   "bread_tearing",          "oneshot", 33.8, 3.0, -27.0),       # the next plate (hollow)
        layer("coins",   "coins_clinking",         "oneshot", 35.6, 3.0, -27.0),       # the next purchase
        layer("bread",   "bread_tearing",          "oneshot", 47.0, 4.0, -23.0),       # Come to the Bread of life (true)
        layer("filled",  "dawn_morning_warm",      "loop",   47.5,  5.4, -34.0, filt="lowpass=f=3000", fin=2.5),  # the life your soul was made for
    ]),

    # ── 35 Manna: DESERT + manna mornings + gathering footsteps → "they DIED/GRAVE" (9-16) hollow → "my FLESH" (31) tear
    #    → "die your DEATH" (~50) low boom → "fathers ate and DIED" (52.7) hollow → resurrection morning + tomb STONE on "grave defeated" (64)
    "35_Manna_Fulfilled": (65.212, [
        layer("desert",  "wind_desert_bleak",       "loop",    0.0, 65.2, -32.0),
        layer("morn",    "dawn_morning_warm",       "loop",    1.2,  7.3, -34.0, filt="lowpass=f=3200", fin=1.5, fout=2.5),  # bread each morning
        layer("gather",  "footsteps_dirt_approach", "oneshot", 4.5,  4.0, -27.0),       # they gathered it
        layer("grave",   "air_hollow_desolate",     "loop",    8.5,  8.0, -32.0, fin=1.5, fout=2.5),  # still, every one died
        layer("flesh",   "bread_tearing",           "oneshot", 31.1, 4.0, -24.0),       # my flesh, which I will give
        layer("death",   "impact_low_boom",         "oneshot", 50.3, 4.0, -26.0),       # He came to die your death
        layer("grave2",  "air_hollow_desolate",     "loop",   52.2, 5.3, -33.0, fin=1.5, fout=2.5),  # the fathers ate and died
        layer("risen",   "dawn_morning_warm",       "loop",   57.5,  7.7, -33.0, filt="lowpass=f=3000", fin=3.0),  # live for ever
        layer("stone",   "stone_roll_tomb",         "oneshot", 62.8, 4.0, -24.0),       # the grave DEFEATED (resurrection)
    ]),

    # ── 36 Cast Out (intimate): lonely THRESHOLD hush (muffled) → "the door… was never LOCKED" (52.4) it creaks OPEN
    "36_In_No_Wise_Cast_Out": (54.649, [
        layer("hush",    "wind_desert_bleak",      "loop",    0.0, 51.0, -37.0, filt="lowpass=f=1600", fin=3.0, fout=3.0),
        layer("unlock",  "door_gate_creak",        "oneshot", 52.4, 4.0, -23.0),       # was never locked → opens
    ]),
}
