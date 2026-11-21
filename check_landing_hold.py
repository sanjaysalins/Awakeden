"""INV-26 deterministic $0 gate: every finished cut (short or long-form) must
end with a real landing hold, not a silent early cutoff.

Two checks, run over every finished mp4 under `batches/` and `longform/`:

1. **FAIL-closed: audio/video duration parity.** If a finished file's audio
   track ends more than 0.3s before its video track (or vice versa), that's
   the exact bug class found 2026-07-19 in `run_piece.py`'s `score_cmd()` --
   a missing `apad` step let the narration audio end early, so a `-shortest`
   mux downstream silently chopped the hold even though the video intended
   one. This always FAILs; it's a real correctness bug, not a style choice.

2. **WARN-only: hold length below the 3.0s standard.** Reads `piece.json`'s
   `score.outro_hold`/`score.tpad` (shorts) where present. Does not fail --
   per the user's 2026-07-19 decision, the existing corpus (shorts at 1.5s,
   long-form at 2.5s) is not being retrofitted, only new pieces are held to
   the new standard. This surfaces the gap, it doesn't block anything.

Usage:
    .venv\\Scripts\\python.exe check_landing_hold.py            # scan everything
    .venv\\Scripts\\python.exe check_landing_hold.py <file.mp4>  # one file, parity only
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOLD_STANDARD = 3.0
PARITY_TOLERANCE = 0.3


def _durations(mp4: Path) -> tuple[float | None, float | None]:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,duration",
         "-of", "csv=p=0", str(mp4)],
        capture_output=True, text=True,
    ).stdout.strip()
    v = a = None
    for line in out.splitlines():
        parts = line.split(",")
        if len(parts) != 2:
            continue
        kind, dur = parts
        try:
            dur = float(dur)
        except ValueError:
            continue
        if kind == "video":
            v = dur
        elif kind == "audio":
            a = dur
    return v, a


def check_parity(mp4: Path) -> tuple[bool, str]:
    v, a = _durations(mp4)
    if v is None or a is None:
        return True, "SKIP (no video+audio streams)"
    gap = v - a
    if abs(gap) > PARITY_TOLERANCE:
        return False, f"FAIL  v={v:.2f}s a={a:.2f}s gap={gap:+.2f}s (>{PARITY_TOLERANCE}s tolerance)"
    return True, f"ok    v={v:.2f}s a={a:.2f}s gap={gap:+.2f}s"


def find_finished_mp4s() -> list[Path]:
    found = []
    for d in (ROOT / "batches", ROOT / "longform", ROOT / "poc_living_sketchbook"):
        if not d.exists():
            continue
        found += list(d.glob("**/*_sfx.mp4"))
        found += list(d.glob("**/*_scored_sfx.mp4"))
        found += list(d.glob("**/*_cc.mp4"))  # living-sketchbook's own final (captioned+watermarked) suffix
    # de-dupe, keep the most specific (already unique by glob, but stay safe)
    return sorted(set(found))


def check_piece_json_holds() -> list[str]:
    """Shorts: outro_hold lives in piece.json (real JSON, easy to read)."""
    warns = []
    for pj_path in (ROOT / "batches").glob("**/piece.json"):
        try:
            d = json.loads(pj_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        sc = d.get("score")
        if not sc:
            continue
        hold = sc.get("outro_hold")
        if hold is not None and hold < HOLD_STANDARD:
            warns.append(f"  WARN {pj_path.parent.name:35s} outro_hold={hold} (< {HOLD_STANDARD}s standard)")
    return warns


_OUTRO_RE = __import__("re").compile(r'"outro_s"\s*:\s*([\d.]+)')
_NAME_RE = __import__("re").compile(r'"(\d\d?_[A-Za-z_0-9]+|EW\d+_[A-Za-z_0-9]+)"\s*:\s*\{')


def check_longform_holds() -> list[str]:
    """Long-form: outro_s lives in Python dicts (EPISODES in longform/_add_score_lf.py,
    RECIPE in any per-episode fork like _add_score_inked.py) -- not JSON, so this
    regex-scans the source rather than importing (importing would run module-level
    code we don't need, and a regex is robust to either dict shape)."""
    warns = []
    seen_episodes = set()

    shared = ROOT / "longform" / "_add_score_lf.py"
    if shared.exists():
        text = shared.read_text(encoding="utf-8")
        # walk name/outro_s pairs in declaration order within the EPISODES dict
        names = [(m.start(), m.group(1)) for m in _NAME_RE.finditer(text)]
        outros = [(m.start(), float(m.group(1))) for m in _OUTRO_RE.finditer(text)]
        for i, (npos, name) in enumerate(names):
            nend = names[i + 1][0] if i + 1 < len(names) else len(text)
            block_outros = [v for (opos, v) in outros if npos < opos < nend]
            if block_outros:
                hold = block_outros[0]
                seen_episodes.add(name)
                if hold < HOLD_STANDARD:
                    warns.append(f"  WARN {name:35s} outro_s={hold} (< {HOLD_STANDARD}s standard) [{shared.name}]")

    for fork in (ROOT / "longform").glob("*/_add_score_*.py"):
        if fork == shared:
            continue
        text = fork.read_text(encoding="utf-8")
        m = _OUTRO_RE.search(text)
        if not m:
            continue
        ep_name = fork.parent.name
        hold = float(m.group(1))
        if ep_name in seen_episodes:
            # a per-episode fork overrides the shared recipe for this episode --
            # report the fork's value (what actually built the shipped file),
            # not the shared dict's (which may be stale/unused for this one)
            warns = [w for w in warns if not w.strip().startswith(f"WARN {ep_name}")]
        if hold < HOLD_STANDARD:
            warns.append(f"  WARN {ep_name:35s} outro_s={hold} (< {HOLD_STANDARD}s standard) [{fork.name}]")

    return warns


# ---- words-json hold gate (owner rule 2026-11-21) -------------------------------------------
# A NEW film must keep running >= 3.0 s after its LAST SPOKEN WORD, and end silent. The last word
# comes from the film's own sidecar `<stem>.words.json` ([{"w","start","end"}, ...] or {"words":[...]}).
# Files listed in data/landing_hold_shipped.json (grandfathered, already posted/locked) only WARN.
SHIPPED_LIST = ROOT / "data" / "landing_hold_shipped.json"
HOLD_TOL = 0.05
SILENT_DB = -45.0       # mean volume of the last 0.25 s must be at or below this (fade to silence)


def words_path(mp4: Path) -> Path:
    return mp4.with_name(mp4.stem + ".words.json")


def last_word_end(words_json: Path) -> float | None:
    try:
        d = json.loads(words_json.read_text(encoding="utf-8"))
    except Exception:
        return None
    if isinstance(d, dict):
        d = d.get("words") or d.get("segments") or []
    ends = []
    for w in d if isinstance(d, list) else []:
        if isinstance(w, dict):
            e = w.get("end", w.get("end_s"))
            if isinstance(e, (int, float)):
                ends.append(float(e))
    return max(ends) if ends else None


def load_shipped() -> set[str]:
    try:
        return set(json.loads(SHIPPED_LIST.read_text(encoding="utf-8")))
    except Exception:
        return set()


def tail_mean_db(mp4: Path, seconds: float = 0.25) -> float | None:
    p = subprocess.run(["ffmpeg", "-v", "info", "-sseof", f"-{seconds}", "-i", str(mp4), "-vn",
                        "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True)
    for line in p.stderr.splitlines():
        if "mean_volume:" in line:
            try:
                return float(line.split("mean_volume:")[1].split("dB")[0])
            except ValueError:
                return None
    return None


def hold_after_last_word(film_len: float, last_end: float) -> float:
    return film_len - last_end


def check_hold(mp4: Path, words_json: Path | None = None, check_silence: bool = True) -> tuple[bool, str]:
    """True = pass. Reads the film's words json; FAIL if the last word ends < 3.0 s before the
    film's end (or the last 0.25 s is not silent). A missing words json is a SKIP, not a pass of
    the standard (use --require-words to make it a FAIL)."""
    wj = words_json or words_path(mp4)
    if not wj.exists():
        return True, "SKIP (no words json)"
    le = last_word_end(wj)
    if le is None:
        return False, f"FAIL  unreadable words json {wj.name}"
    v, a = _durations(mp4)
    ends = [x for x in (v, a) if x is not None]
    if not ends:
        return True, "SKIP (no streams)"
    film = min(ends)
    hold = hold_after_last_word(film, le)
    msgs, ok = [f"hold={hold:.2f}s (last word {le:.2f}s, film {film:.2f}s)"], True
    if hold < HOLD_STANDARD - HOLD_TOL:
        ok = False
        msgs.append(f"< {HOLD_STANDARD}s standard")
    if check_silence and a is not None:
        db = tail_mean_db(mp4)
        if db is not None and db > SILENT_DB:
            ok = False
            msgs.append(f"last 0.25s not silent ({db:.1f} dB > {SILENT_DB} dB; need a ~2.5 s end fade)")
    return ok, ("ok    " if ok else "FAIL  ") + "; ".join(msgs)


def check_all_holds() -> tuple[int, list[str]]:
    """Scan finished mp4s that have a words json. Returns (n_fail, lines). Shipped -> WARN only."""
    shipped = load_shipped()
    fails, lines = 0, []
    for mp4 in find_finished_mp4s():
        if not words_path(mp4).exists():
            continue
        ok, msg = check_hold(mp4)
        if ok:
            continue
        if mp4.name in shipped:
            lines.append(f"  WARN (shipped) {msg}  {mp4.relative_to(ROOT)}")
        else:
            fails += 1
            lines.append(f"  {msg}  {mp4.relative_to(ROOT)}")
    return fails, lines


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if argv:
        mp4 = Path(argv[0])
        ok, msg = check_parity(mp4)
        print(f"{mp4.name}: {msg}")
        wj = words_path(mp4)
        if "--require-words" in argv and not wj.exists():
            print(f"{mp4.name}: FAIL  no words json {wj.name} (--require-words)")
            return 1
        hok, hmsg = check_hold(mp4)
        shipped = mp4.name in load_shipped()
        print(f"{mp4.name}: {hmsg}{'  [shipped: WARN only]' if (shipped and not hok) else ''}")
        return 0 if (ok and (hok or shipped)) else 1

    print("=== INV-26 landing-hold gate ===\n")
    print("-- audio/video duration parity (FAIL-closed) --")
    fails = 0
    for mp4 in find_finished_mp4s():
        ok, msg = check_parity(mp4)
        rel = mp4.relative_to(ROOT)
        print(f"  {msg:60s} {rel}")
        if not ok:
            fails += 1

    print("\n-- hold length vs 3.0s standard (WARN-only, not retrofitted) --")
    warns = check_piece_json_holds() + check_longform_holds()
    if warns:
        for w in warns:
            print(w)
    else:
        print("  (none below standard)")

    print("\n-- last word -> end >= 3.0s and silent end (words json; shipped = WARN only) --")
    hfails, hlines = check_all_holds()
    for ln in hlines:
        print(ln)
    if not hlines:
        print("  (all films with a words json pass)")
    fails += hfails

    print(f"\n{len(find_finished_mp4s())} files checked, {fails} FAIL, {len(warns)} hold WARN")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
