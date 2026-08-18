"""_panel_dna_dispatch.py — one-off: fan a TECHNICAL musical-DNA research brief for
Robert Miles' "Children" (pre-drop build section only) out to the local AI CLI panel.

Reuses independent_review.py's own run_one()/PROVIDERS dispatch (local subscription
CLIs, NOT metered API). This is a deeper follow-up to the first (mood-word) panel pass
already saved in poc_living_sketchbook/son_of_man_lifted_up/_score_swap_poc/ — the user
asked for literal musical structure this time: BPM, key, chord progression, arpeggio
pattern, layering order, instrumentation, dynamics arc.

Run gently: dispatched with limited concurrency (max_workers=2), not all 5 at once,
per the user's "gentle CPU/memory" request for this session.

Usage:
  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_score_swap_poc/_panel_dna_dispatch.py
"""
from __future__ import annotations

import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from independent_review import run_one, PROVIDERS  # noqa: E402

OUTDIR = Path(__file__).resolve().parent
NAMES = ["cursor", "claude", "gemini", "codex", "grok"]
GENTLE_CONCURRENCY = 2  # dispatch 2 at a time, not all 5 — keep local CPU/RAM low

BRIEF = """You are a professional electronic-music producer and musicologist.

Describe the ACTUAL musical structure of Robert Miles' 1995 track "Children" —
specifically ONLY its opening / pre-drop build section (the arpeggiated piano intro,
before the beat/drum drop enters). Be precise and technical, not just mood words:

1. TEMPO — the actual BPM.
2. KEY / MODE — the key the intro is in (major/minor), and whether it modulates within
   the build.
3. CHORD PROGRESSION — the actual chord sequence the arpeggio outlines, as a roman-
   numeral or note-name progression, looped through the build.
4. ARPEGGIO PATTERN — the specific note pattern and rhythmic subdivision (e.g. is it a
   16th-note broken-chord run, ascending, descending, ascending-then-descending; how
   many notes per chord; does the pattern itself vary or repeat unchanged).
5. LAYERING ORDER — what enters first (just the piano alone?), then second, then third,
   roughly how many bars/seconds apart, through to the point right before the drop.
6. INSTRUMENTATION — the actual timbres/patches used (e.g. the specific electric-piano
   or piano patch, pad synth character, any strings/bass presence, filter character).
7. DYNAMICS ARC — how volume, harmonic density, and stereo width evolve across just
   this build section (not the whole song).
8. Any other structural detail a producer would need (filter sweeps, reverb/delay
   character, sidechain pumping if any, low-end presence or absence) to recreate the
   FEEL of this specific build without literally copying the melody.

CONTEXT for why this matters: this technical description will be used to brief an AI
music-generation model (ElevenLabs Music) to compose an ORIGINAL sacred/reverent
instrumental cue for a Bible-teaching short film — inspired by this build's musical DNA,
NOT a copy of the melody, and the final generation prompt will NOT name the artist or
song (ElevenLabs' own ToS blocks named-artist references). We need your description to
be specific enough that someone who has never heard the song could still recreate its
STRUCTURE (tempo, chords, layering, arc) in an original piece.

Answer ONLY the 8 numbered points above, as specifically as you can. If you are not
certain of an exact number (e.g. the precise BPM), give your best-informed estimate and
say so, rather than refusing to answer."""


def main() -> int:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    (OUTDIR / "_dna_brief.txt").write_text(BRIEF, encoding="utf-8")
    print(f"[dna] dispatching {len(NAMES)} voices, {GENTLE_CONCURRENCY} at a time -> {OUTDIR}")

    results: dict[str, tuple[bool, str, float]] = {}
    with ThreadPoolExecutor(max_workers=GENTLE_CONCURRENCY) as ex:
        futs = {ex.submit(run_one, n, BRIEF, OUTDIR): n for n in NAMES}
        for f in as_completed(futs):
            name, ok, out, dur = f.result()
            results[name] = (ok, out, dur)
            (OUTDIR / f"dna_{name}.txt").write_text(out, encoding="utf-8")
            line = f"  [{'ok ' if ok else 'FAIL'}] {name:<7} {dur:5.0f}s"
            print(line.encode("ascii", "replace").decode("ascii"))

    healthy = sum(1 for ok, _, _ in results.values() if ok)
    print(f"[dna] done: {healthy}/{len(NAMES)} healthy voices. Raw files: dna_<name>.txt")
    return 0 if healthy >= 3 else 1


if __name__ == "__main__":
    raise SystemExit(main())
