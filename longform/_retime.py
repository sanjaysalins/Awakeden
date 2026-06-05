"""Re-time the Isaiah 53 soundstage anchors + scene windows after the narrator
speed-up (1.0x -> 1.1013x). Builds a piecewise-linear warp from OLD aligned cue
times -> NEW aligned cue times and maps every BED/SHOT anchor + scene window
through it, so each cue still lands on its word. Prints new BEDS/SHOTS and
rewrites scene_plan.json's `t` windows. Free, read-only except scene_plan.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "longform" / "01_Isaiah_53_Suffering_Servant" / "v1" / "visual_16x9"

# (old, new) control points = cue phrase START times from _pilot_cue_times.py.
# OLD = canonical 1.0x baseline (NEVER changes). NEW = current target audio.
# Current target: narrator 1.20x (405.3s). Re-run _pilot_cue_times.py after any
# narrator-speed change and paste the new column here, then re-run this script.
CTRL = [
    (0.0,     0.0),
    (0.53,    0.43),
    (47.96,   40.14),   # behold (God)
    (60.42,   51.66),   # visage marred
    (75.72,   64.70),   # despised
    (110.90,  93.70),   # exchange start
    (117.48,  99.22),   # nail
    (175.86, 148.02),   # lamb
    (178.36, 150.02),   # shearers
    (192.56, 161.88),   # objection
    (286.00, 239.80),   # gaza chariot
    (298.28, 250.04),   # philip
    (316.22, 266.28),   # preached jesus
    (339.16, 285.42),   # thunder (it pleased)
    (366.96, 308.66),   # dawn
    (477.48, 400.40),   # close (His name is Jesus)
    (482.887, 405.26),  # end
]


def warp(t: float) -> float:
    """Piecewise-linear map old-time -> new-time."""
    if t <= CTRL[0][0]:
        return CTRL[0][1]
    if t >= CTRL[-1][0]:
        # extrapolate past last control point at the final local slope
        (o0, n0), (o1, n1) = CTRL[-2], CTRL[-1]
        return n1 + (t - o1) * (n1 - n0) / (o1 - o0)
    for (o0, n0), (o1, n1) in zip(CTRL, CTRL[1:]):
        if o0 <= t <= o1:
            return n0 + (t - o0) * (n1 - n0) / (o1 - o0)
    return t


# ---- BEDS / SHOTS from _soundstage_cinematic.py (OLD times) ------------------
BEDS = [
    ("wind_desert_bleak",     0,  47, 2, 4, -29),
    ("air_hollow_desolate",  53, 289, 4, 8, -32),
    ("crowd_murmur_distant", 71,  86, 3, 4, -30),
    ("rumble_deep_sub",     112, 142, 3, 6, -30),
    ("flock_sheep_field",   174, 198, 2, 4, -28),
    ("chariot_wheels_road", 285, 340, 2, 5, -26),
    ("horse_hooves_walk",   287, 337, 2, 5, -29),
    ("rumble_deep_sub",     337, 368, 2, 6, -28),
    ("dawn_morning_warm",   364, 482, 4, 8, -28),
    ("heavenly_choir_soft", 369, 482, 6, 9, -33),
]
SHOTS = [
    ("impact_low_boom",          60.4, -7),
    ("nail_strike_single",      117.5, -9),
    ("footsteps_dirt_approach", 298.3, -12),
    ("thunder_low_roll",        339.2, -6),
]


def fmt_beds():
    print("BEDS = [")
    for slug, s, e, fi, fo, db in BEDS:
        ns, ne = warp(s), warp(e)
        print(f'    ("{slug}", {ns:6.1f}, {ne:6.1f}, {fi}, {fo}, {db}),')
    print("]")


def fmt_shots():
    print("SHOTS = [")
    for slug, a, db in SHOTS:
        na = warp(a)
        print(f'    ("{slug}", {na:7.1f}, {db}),')
    print("]")


# canonical 1.0x scene windows (id -> [start, end]). NEVER edit; warp maps them.
SCENES_1X = {
    1: [0, 24], 2: [24, 47], 3: [48, 70], 4: [70, 92], 5: [92, 110],
    6: [110, 132], 7: [132, 155], 8: [155, 175], 9: [175, 200], 10: [200, 230],
    11: [230, 258], 12: [258, 285], 13: [286, 310], 14: [310, 326], 15: [326, 339],
    16: [339, 365], 17: [365, 392], 18: [392, 418], 19: [418, 444], 20: [444, 466],
    21: [466, 483],
}
AUDIO_LABEL = "narration.immersive.mp3 (balanced) -- 405.3s (narrator 1.20x)"


def retime_scene_plan():
    sp_path = OUT / "scene_plan.json"
    data = json.loads(sp_path.read_text(encoding="utf-8"))
    print("\n# scene windows (1.0x -> new):")
    for sc in data["scenes"]:
        os_, oe = SCENES_1X[sc["id"]]
        ns, ne = round(warp(os_), 1), round(warp(oe), 1)
        print(f'  S{sc["id"]:02d}  [{os_:>3},{oe:>3}] -> [{ns:>6.1f},{ne:>6.1f}]  win={ne-ns:4.1f}s')
        sc["t"] = [ns, ne]
    data["audio"] = AUDIO_LABEL
    sp_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[done] rewrote {sp_path}")


if __name__ == "__main__":
    fmt_beds()
    print()
    fmt_shots()
    retime_scene_plan()
