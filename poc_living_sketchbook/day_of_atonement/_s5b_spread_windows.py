"""Day of Atonement LONG -- step 5b: turn `_spread_table.py`'s
plan-estimated 76 windows + `_alignment.json`'s real forced-aligned word
timings into the one file `_s6_assemble.py` actually reads:
`_spread_windows.json`. Mirrors `bronze_serpent_long/_s6b_spread_windows.py`
exactly (same seam-snap + fill-mode logic), adapted for this episode's own
76 spreads and its own deterministic-camera roster.

Two corrections applied to the plan's estimated windows:
  1. SEAM SNAP -- every interior (sub-turn) spread boundary is an estimate
     (_PLAN.md sec 1c/2 says so explicitly; only turn-level boundaries are
     ffprobe-hard). Snap each boundary to the start of the nearest real word
     in `_alignment.json`, and print a drift report so anything that moved
     more than 1.5s gets a human look before assembly runs, not after.
  2. FINAL EXTENT -- spread 76 (the landing) is stretched from the last real
     word's end to LAST_WORD_END + LANDING_HOLD_S (INV-26, >=3.0s,
     audio=video). Spread 1 always starts at 0.00.

For each spread this also resolves a FILL MODE (how a clip shorter or
longer than its window gets stretched/trimmed to fill it exactly), given
each spread's live clip duration (ffprobe'd fresh, not hardcoded) -- v1
"simple cut" pass only implements the safe default modes; the directional
fwd_tail_bounce refinement (a completing gesture should never play in
reverse) is included since a visibly-reversed hand gesture is a correctness
bug, not a polish nicety -- see ONE_WAY below.

  .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_s5b_spread_windows.py
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

# Spreads with genuine one-directional COMPLETING motion in the source clip
# (the plan's own "designed acting spread" tag) -- a reverse (boomerang)
# bounce would visibly un-do the gesture. Play forward once, then bounce
# only a short calm TAIL, never a full-clip pingpong.
ONE_WAY = {
    "s29_hands_on_goat",   # Aaron's hands settling onto the goat's head
    "s75_the_reach",       # Christ's hand extending toward the viewer
}

# The 18 spreads animated by the $0 deterministic camera (panel_animator/
# dynamic_cam3d.py push/arc over the untouched still, zero repaint) rather
# than a generative Kling/Seedance clip -- 12 from the original animate
# batch (_s_christ_spreads_orbit.py + the individual _s05/_s25_orbit.py
# scripts) + 6 from the 2026-08-05 user-review fix pass
# (_s_fix_batch2_orbit.py). A reversed camera push/arc would look wrong
# (the camera un-pushing), so these get once_hold/once_trim, never a bounce.
DETERMINISTIC = {
    "s05_walking_to_veil", "s25_slaying_stage1",
    "s51_jesus_pivot", "s52_jesus_entering_formal", "s53_the_cross",
    "spread54_thread_leaf", "spread55_isaiah536",
    "s56_the_answer", "s57_without_the_gate", "s60_seated_glory",
    "s66_high_priests_face", "s76_already_inside",
    "s26_through_veil_stage2", "s27_sprinkling", "s34_riddle_recap",
    "s45_sign_before_veil", "s50_the_shadow", "s63_torn_veil_card",
}

# Not yet populated -- bronze_serpent_long's own NO_BOUNCE set (spreads
# whose pingpong bounce read as unwanted motion, e.g. "looks like he's
# dancing") was only discovered by the user watching the ASSEMBLED cut, not
# predicted in advance. Same discipline here: build the first cut with the
# general-purpose fill modes below, watch it, and add any offenders here
# before the next rebuild rather than guessing now.
NO_BOUNCE = set()


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
              f"windows uncorrected. Re-run after _s5_align.py finishes for real timing.")

    # Snap only the START of each spread (spread 1 always 0.00). Each
    # spread's END is then set to the NEXT spread's start -- never snapped
    # independently -- so consecutive windows share the exact same boundary
    # value with zero gap and zero overlap (bronze_serpent_long's own fix
    # for an ~18s missing-video bug caused by snapping start/end separately).
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
