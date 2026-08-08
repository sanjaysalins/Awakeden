"""Seed of the Woman LONG -- step 5b: fix the confirmed ~7s cumulative drift
in `_turn_boundaries.json` (see RESUME.md 2026-08-07 night handover, step 2).

Unlike Day of Atonement (where turn-level boundaries come from real ffprobe'd
per-turn clips and only INTERIOR sub-turn seams are estimates), this
episode's `_turn_boundaries.json` turned out to be a proportional estimate
at the TURN level too -- confirmed by searching the real per-word
`_alignment.json` for "That is the cross" (turn 34's first words): real
346.673s vs `_turn_boundaries.json`'s claimed 353.657s, a 6.98s drift that
grows through the file (cumulative tokenization mismatch).

Fix: for every turn, find its own first few words as a literal sequence in
the real per-word `_alignment.json` (the same technique that found the
drift above) to get a REAL turn start. Then remap every spread boundary
from `_spread_table.py`: find which claimed turn range it falls in, keep
its FRACTIONAL position within that turn (the plan's own intra-turn design
intent), and re-apply that fraction to the turn's REAL (not claimed)
window. This corrects the actual bug (turn-level drift) while preserving
the plan's sub-turn split design, exactly as `_spread_table.py`'s own
docstring already describes sub-turn seams: "word-proportional ESTIMATES".

Prints a full drift report, then prints a ready-to-paste corrected SPREADS
list (spreads 1-5 and the already-correct s06/s16 test tier untouched --
their turns 0-4 have near-zero drift already).

  .venv\\Scripts\\python.exe poc_living_sketchbook/seed_of_the_woman/_s5b_reconcile_timing.py
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _spread_table as ST  # noqa: E402

TURNS = json.loads((HERE / "_turn_boundaries.json").read_text(encoding="utf-8"))
WORDS = json.loads((HERE / "_alignment.json").read_text(encoding="utf-8"))


def _norm(w: str) -> str:
    return re.sub(r"[^a-z']", "", w.lower())


def find_turn_real_start(turn_text: str, cursor: int) -> tuple:
    """Search WORDS forward from `cursor` for a literal word-sequence from
    the turn's own claimed text. `_turn_boundaries.json`'s `text` field
    turned out to sometimes NOT match the real spoken audio verbatim (e.g.
    turn 18 claims '"therefore also that holy thing...' but the real
    narration.mp3 only speaks '"that holy thing...' -- a real draft/audio
    mismatch, confirmed by hand). So try a 3-word needle at word-offsets
    0, 1, 2 into the turn's own text (skips up to 2 possibly-unspoken
    leading words) before giving up."""
    turn_words = [w for w in turn_text.split() if _norm(w)]
    for offset in (0, 1, 2):
        needle = [_norm(w) for w in turn_words[offset:offset + 3]]
        if len(needle) < 2:
            continue
        n = len(needle)
        for i in range(cursor, len(WORDS) - n + 1):
            window = [_norm(WORDS[i + k]["w"]) for k in range(n)]
            if window == needle:
                return WORDS[i]["start"], i
    raise SystemExit(f"[FATAL] could not locate turn text {turn_text[:40]!r} after word index {cursor}")


def main():
    real_start = {}
    cursor = 0
    print("[turn drift report] claimed vs real start, per turn:")
    for t in TURNS:
        rs, idx = find_turn_real_start(t["text"], cursor)
        real_start[t["index"]] = rs
        # Advance the cursor PAST this turn's own words (using its own
        # n_words count, with a small safety margin) before searching for
        # the NEXT turn -- some turns rhetorically echo the previous turn's
        # phrasing (e.g. a scripture quote's "made of a woman" immediately
        # followed by narrator text starting "Made of a woman."), which
        # would otherwise re-match the same earlier occurrence.
        cursor = idx + max(1, t.get("n_words", 1) - 2)
        drift = rs - t["start"]
        flag = "  <-- >1.5s" if abs(drift) > 1.5 else ""
        print(f"  turn {t['index']:2d}: claimed {t['start']:7.3f}  real {rs:7.3f}  drift {drift:+6.2f}s{flag}")

    n_turns = len(TURNS)
    claimed_start = {t["index"]: t["start"] for t in TURNS}
    claimed_end = {t["index"]: t["end"] for t in TURNS}
    real_end = {i: (real_start[i + 1] if i + 1 < n_turns else WORDS[-1]["end"]) for i in range(n_turns)}

    def remap(ts: float) -> float:
        # which claimed turn window does ts fall in?
        for t in TURNS:
            i = t["index"]
            cs, ce = claimed_start[i], claimed_end[i]
            if cs - 0.05 <= ts <= ce + 0.05 or (i == n_turns - 1 and ts > ce):
                frac = 0.0 if ce <= cs else max(0.0, min(1.0, (ts - cs) / (ce - cs)))
                rs, re_ = real_start[i], real_end[i]
                return rs + frac * (re_ - rs)
        raise SystemExit(f"[FATAL] timestamp {ts} not inside any claimed turn window")

    print("\n[spread remap] num name  plan_start -> corrected_start  (delta)")
    corrected = []
    for num, name, beat, t0, t1 in ST.SPREADS:
        new_t0 = 0.0 if num == 1 else remap(t0)
        corrected.append([num, name, beat, new_t0])
        delta = new_t0 - t0
        flag = "  <-- >1.0s" if abs(delta) > 1.0 else ""
        print(f"  #{num:02d} {name:<28s} {t0:7.3f} -> {new_t0:7.3f}  ({delta:+6.2f}s){flag}")

    # ends = next spread's corrected start; last spread end = last word end (unchanged, INV-26 hold added at assembly)
    out_rows = []
    for i, (num, name, beat, new_t0) in enumerate(corrected):
        new_t1 = corrected[i + 1][3] if i + 1 < len(corrected) else WORDS[-1]["end"]
        out_rows.append((num, name, beat, round(new_t0, 2), round(new_t1, 2)))

    out_path = HERE / "_corrected_spreads.json"
    out_path.write_text(json.dumps(out_rows, indent=1), encoding="utf-8")
    print(f"\n[out] wrote {len(out_rows)} corrected spread rows -> {out_path}")
    print(f"[check] last spread end = {out_rows[-1][4]:.3f} (should match last word end {WORDS[-1]['end']:.3f})")


if __name__ == "__main__":
    main()
