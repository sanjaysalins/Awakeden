"""Bronze Serpent LONG -- step 6b: turn `_spread_table.py`'s plan-estimated
68 windows + `_alignment.json`'s real forced-aligned word timings into the
one file `_s7_assemble.py` actually reads: `_spread_windows.json`.

Two corrections applied to the plan's estimated windows:
  1. SEAM SNAP -- every interior (sub-turn) spread boundary is an estimate
     (_PLAN.md sec 1c/2 says so explicitly; only turn-level boundaries are
     ffprobe-hard). Snap each boundary to the start of the nearest real
     word in `_alignment.json`, and print a drift report so anything that
     moved more than 1.5s gets a human look before assembly runs, not
     after.
  2. FINAL EXTENT -- spread 68 (the landing) is stretched from the last
     real word's end to LAST_WORD_END + LANDING_HOLD_S (INV-26, >=3.0s,
     audio=video). Spread 1 always starts at 0.00 (covers the narration's
     own 0.4s pre-pause), not 0.40.

For each spread this also resolves a FILL MODE (how a clip shorter or
longer than its window gets stretched/trimmed to fill it exactly), given
each spread's live clip duration (ffprobe'd fresh, not hardcoded) --
v1 "simple cut" pass only implements the safe default modes; the
directional fwd_tail_bounce refinement (walking/falling/rising motion
should never play in reverse) is INCLUDED here since a visibly reversed
walk is a correctness bug, not a polish nicety -- see ONE_WAY below.

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent_long/_s6b_spread_windows.py
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _spread_table as ST

CLIPS = HERE / "clips"
STILLS = HERE / "stills"
ALIGNMENT = HERE / "_alignment.json"
OUT = HERE / "_spread_windows.json"

# Spreads whose motion is directionally one-way in the source drawing --
# a reverse (boomerang) bounce would visibly play the action backward.
# Hand-reviewed against each spread's own animation prompt / description,
# not guessed. These get fwd_tail_bounce (play forward once, then bounce
# only a short calm TAIL) instead of a full-clip pingpong.
ONE_WAY = {
    "s09_manna_scorned",       # manna falling
    "s54_timeshift_enshrined", # incense smoke rising
    "s05_graves",              # digging
    "s08_wandering_column",    # walking column
    "s34_moses_walking_dusk",  # Moses walking
}

DETERMINISTIC = {
    "s12_vc_wherefore", "s14_serpent_hint", "s18_moses_empty_hands",
    "s28_forge_acting", "s44_shadow_cross", "s46_thesis_pair",
    "s51_christ_draw_all_men", "s55_hezekiah_breaks",
    "s43_insert_scholars_margin2", "s67_insert_gilded_proclamation2",
}

# Spreads where user QC (2026-08-02, assembled-film watch) caught a
# forward+reverse bounce reading as unwanted motion ("looks like he's
# dancing") -- a close portrait where the base clip's own licensed motion
# (a halo/glow brightness pulse) doesn't necessarily return to its exact
# starting state at the reversal seam, and any resulting flicker is far
# more noticeable on a still face than on a wide/background shot.
# Forced to play forward once and hold the last frame -- zero reversal,
# zero risk -- rather than trying to tune the bounce.
#   s50_christ_close_words -- reported directly (07:31 in the first cut).
#   s49_christ_radiant_begin -- reported directly (07:23 in the second
#     cut, after s50's own fix moved the timestamp).
#   s57_bridge_moses_christ -- NOT reported, added proactively: its motion
#     prompt is "the soft halo glow around Christ breathes very gently
#     brighter and dimmer" -- near word-for-word the same pattern as
#     s49's already-confirmed defect, same pingpong mode. Fixing now
#     rather than waiting for a 3rd identical report.
# NOT included (motion is diffuse scene/paper-wide light, not a tight
# halo directly on the figure -- lower-risk pattern, no evidence yet):
# s45_golgotha_wide (already fixed+verified for a different, worse
# defect this session), s47_golgotha_midshot, s58_vc_john316,
# s65_christ_open_invite (already fixed for robe-sway separately).
NO_BOUNCE = {
    "s50_christ_close_words", "s49_christ_radiant_begin",
    "s57_bridge_moses_christ",
}


def ffprobe_dur(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def nearest_word_start(t: float, words: list) -> float:
    if not words:
        return t
    best = min(words, key=lambda w: abs(w["start"] - t))
    return best["start"] if abs(best["start"] - t) <= 3.0 else t


def fill_mode(name: str, window_dur: float, clip_dur: float) -> dict:
    if name in DETERMINISTIC:
        drift = window_dur - clip_dur
        if abs(drift) > 0.5:
            print(f"[note] {name}: real aligned window ({window_dur:.2f}s) differs from "
                  f"its deterministic clip's own duration ({clip_dur:.2f}s) by {drift:+.2f}s "
                  f"-- holding the last frame to cover it (or trimming if the window shrank).")
        if drift >= 0:
            return {"mode": "once_hold", "clip_dur": clip_dur}
        return {"mode": "once_trim", "clip_dur": clip_dur}
    if clip_dur >= window_dur:
        return {"mode": "once_trim", "clip_dur": clip_dur}
    if name in NO_BOUNCE:
        return {"mode": "once_hold", "clip_dur": clip_dur}
    if name in ONE_WAY:
        return {"mode": "fwd_tail_bounce", "clip_dur": clip_dur, "tail_s": 1.5}
    if window_dur <= 15.0:
        return {"mode": "pingpong", "clip_dur": clip_dur}
    factor = min(2.0, window_dur / (2.0 * clip_dur))
    return {"mode": "slow_pingpong", "clip_dur": clip_dur, "factor": round(factor, 4)}


def main():
    words = []
    if ALIGNMENT.exists():
        words = json.loads(ALIGNMENT.read_text(encoding="utf-8"))
        print(f"[align] loaded {len(words)} words from {ALIGNMENT.name}")
    else:
        print(f"[align] WARNING: {ALIGNMENT.name} not found -- using plan-estimated "
              f"windows uncorrected. Re-run after _s6_align.py finishes for real timing.")

    # Snap only the START of each spread (spread 1 always 0.00). Each spread's
    # END is then set to the NEXT spread's start -- never snapped independently
    # -- so consecutive windows share the exact same boundary value with zero
    # gap and zero overlap. (An earlier version snapped start/end independently;
    # since both search the same real word list, they could each land on a
    # slightly different nearby word for what should be the SAME boundary,
    # opening tiny gaps that summed to ~18s missing video across 67 seams --
    # caught by check_landing_hold.py's video/audio duration mismatch.)
    n = len(ST.SPREADS)
    starts = [0.00] * n
    for i, (num, name, beat, plan_start, plan_end) in enumerate(ST.SPREADS):
        starts[i] = 0.00 if num == 1 else (nearest_word_start(plan_start, words) if words else plan_start)
    last_word_end = max((w["end"] for w in words), default=ST.LAST_WORD_END_ESTIMATE)
    final_end = last_word_end + ST.LANDING_HOLD_S

    rows = []
    drift_report = []
    for i, (num, name, beat, plan_start, plan_end) in enumerate(ST.SPREADS):
        start = starts[i]
        end = starts[i + 1] if i + 1 < n else final_end

        drift = (start - plan_start, end - plan_end)
        if abs(drift[0]) > 1.5 or abs(drift[1]) > 1.5:
            drift_report.append((num, name, drift))

        clip_path = CLIPS / f"{name}.mp4"
        if name in ST.ALWAYS_STATIC_HOLD:
            fm = {"mode": "static_still", "clip_dur": None}
        elif clip_path.exists():
            clip_dur = ffprobe_dur(clip_path)
            fm = fill_mode(name, end - start, clip_dur)
        else:
            fm = {"mode": "MISSING_CLIP", "clip_dur": None}
            print(f"[MISSING] {name}: no clip at {clip_path}")

        rows.append({
            "num": num, "name": name, "beat": beat,
            "start": round(start, 3), "end": round(end, 3),
            "dur": round(end - start, 3),
            **fm,
        })

    OUT.write_text(json.dumps(rows, indent=1), encoding="utf-8")
    print(f"[out] {len(rows)} spreads -> {OUT}")

    if drift_report:
        print(f"\n[drift] {len(drift_report)} spread(s) with >1.5s seam drift vs plan estimate:")
        for num, name, (ds, de) in drift_report:
            print(f"  #{num:02d} {name}: start {ds:+.2f}s, end {de:+.2f}s")
    else:
        print("\n[drift] none >1.5s" if words else "\n[drift] skipped (no alignment yet)")

    modes = {}
    for r in rows:
        modes[r["mode"]] = modes.get(r["mode"], 0) + 1
    print(f"\n[fill modes] {modes}")


if __name__ == "__main__":
    main()
