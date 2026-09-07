"""Score for The Cross That Wasn't His (Mark 15:20-21 / Luke 23:26, Simon of
Cyrene; Hebrews 13:11-13 "without the camp/gate" typology).

Built score-design-early (SCORE_DESIGN_EARLY.md), from REAL per-word
alignment timestamps (`narration.alignment.json` -> `_compute_unit_timing.py`
-> `unit_timing.json`, verified word-for-word against the raw alignment file
and cross-checked against every page's own caption/corner-note text in
`episode.py` -- every unit's spoken text lines up exactly with its page).
Free-text `music_v1` prompt with "around Xs in..." cues, NOT a `composition_
plan`/`music_v2` request -- that structured route is a confirmed dead end in
this project (STATE.md 2026-08-10 and 2026-06-24 -- never built anywhere
runnable / injects vocals), per [[feedback_score_design_early_validated]].

Reuses the felt-piano "Fig Tree" identity validated on episode 8 ("love this
score, this perhaps the best north star score") and evolved on Naaman ep4,
the Barrel ep5, the Bier ep7, She Loved Much ep10, and Where Are the Nine
ep11 (a six-episode-validated series identity), now extended to a seventh
arc.

TWO-PART GENERATION (2026-09-07, real defect found and fixed): the first two
attempts at ONE continuous ~109s generation both came back with a severe,
previously-undocumented ElevenLabs Music failure -- 50-63 SECONDS of
near-total silence (-90dB) before the piano ever became audible, roughly
matching this episode's own long "withheld, unresolved" character arc up to
its resolution. Adding an explicit "the piano is audibly present throughout,
never falls silent" clause to the single long prompt did NOT fix it (attempt
2 was still dead through 50s+) -- this looks like a real limit on how long a
single generation can sustain a "quiet/withheld" character before the model
just renders literal silence, not a wording problem. Fix: split the
generation into TWO independent, much shorter calls at the episode's own
resolution boundary (F06, 54.479s) -- Part 1 (front..F05, ~57s requested)
stays withheld throughout but is short enough not to trigger the defect;
Part 2 (F06..back, ~52s requested) opens ALREADY resolved (a warm chord in
its very first bar), which is inherently unlikely to render as silence.
Each part is verified independently (`check_no_dead_intro`) before the two
are joined with a short crossfade at the splice (the F06 resolution point)
and put through the same fade-in/fade-out/trim contract as before. See
[[feedback_score_design_early_validated]] for the update to this pattern.

Real timing (unit_timing.json):
  0.0-5.7s     front  the hook -- the man who would carry it was walking the other way
  5.7-15.3s    f01    the compulsion -- soldiers, Simon named, led out
  15.3-25.1s   f02    two men, opposite roads, forced together -- nobody asked
  25.1-35.9s   f03    THE GOSPEL TURN -- Simon turns, walks out too (swirl begins here)
  35.9-42.5s   f04    the word -- outside is "without"
  42.5-54.5s   f05    the type -- the sin offering, burned without the camp
  54.5-67.2s   f06    HERO -- "suffered without the gate" -- the one true resolution
  67.2-75.1s   f07    strings gather -- "Hebrews turns to you"
  75.1-82.2s   f08    reproach is shame; bearing it is carrying it
  82.2-92.9s   f09    the CTA -- "you are asked... freely this time"
  92.9-106.4s  back   the landing -- through that gate first, with his own blood
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline.assembly_align import _resolve_key  # noqa: E402

HERE = Path(__file__).resolve().parent
NARRATION = HERE / "narration.mp3"
RAW = HERE / "score_piano_raw.mp3"
FITTED = HERE / "score_piano.mp3"
PART1_RAW = HERE / "score_piano_part1_raw.mp3"
PART2_RAW = HERE / "score_piano_part2_raw.mp3"
OUTRO_HOLD = 3.0
OUTRO_MARGIN = 2.5
SPLIT_S = 54.479  # F06's own start -- the resolution boundary
CROSSFADE_S = 0.4

PART1_PROMPT = (
    "Intimate modern-classical felt piano, instrumental, slow and rubato, around 60 bpm. One "
    "quiet, tender felt-piano motif of just a few notes carries the entire piece as its lead and "
    "almost only voice, played sparsely with long pedal decays; brief, real silences of a beat or "
    "two happen BETWEEN individual phrases only, the way a pianist breathes between them -- the "
    "piano itself is audibly present and playing throughout, from its very first second onward, "
    "never falling fully silent for more than a couple of seconds at a time; no drums, no "
    "percussion, no bassline, nothing rhythmic at all, ever. The piece opens immediately, spare, "
    "plain, and a little heavy, the motif cool and unresolved in the piano's low-middle register, "
    "short phrases that stop rather than land -- a man walking the wrong way, toward something he "
    "did not choose. Around six seconds in the motif goes flatter and more procedural, almost "
    "matter-of-fact, still unresolved -- names, soldiers, a road, nothing given away. Around "
    "fifteen seconds in a quiet unease enters, two simple lines moving in opposite directions "
    "against each other, restless, unresolved -- two men, two roads, forced together. Around "
    "twenty-five seconds in, on a single clear moment, the piano opens -- one real but effortful "
    "interval struck and left to ring, weighted, not light, as if something has been picked up "
    "that is heavy to carry -- then within a few seconds it draws back again, unresolved, because "
    "this turning is costly and compelled, not yet the piece's true turn. Around thirty-six "
    "seconds in the motif goes plain and instructional, almost spoken, a little searching, "
    "explaining rather than feeling. Around forty-three seconds in the piece goes slower and more "
    "solemn, older and more formal in character, grave without being loud -- something ancient "
    "being explained, still withheld, quietly held but always present, right up to the piece's own "
    "final bar. Clean, airy, uncluttered mix with generous headroom, everything soft, underneath, "
    "and unhurried, but audible throughout, ending still unresolved, mid-thought, on a quiet open "
    "phrase, not a full stop."
)

PART2_PROMPT = (
    "Intimate modern-classical felt piano, instrumental, slow and rubato, around 60 bpm, "
    "continuing directly from a quiet unresolved held phrase. The SAME quiet, tender felt-piano "
    "motif of just a few notes that has carried the piece so far now, in the very first bar, "
    "resolves outright at last: one plain, warm, unambiguous chord, held long in the pedal, the "
    "motif returning steadied and whole, as if the true weight of what was carried has finally "
    "been named -- this chord is the loudest, clearest, most present moment so far, struck "
    "immediately, not built up to. No drums, no percussion, no bassline, nothing rhythmic at all, "
    "ever; the piano remains audibly present throughout every section below, never falling fully "
    "silent. From around thirteen seconds in (measured from this part's own start), strings begin "
    "to gather underneath one section at a time, each entry almost imperceptible: soft violas "
    "first, then muted violins, then low cellos, sustaining long warm tones that slowly widen the "
    "harmony beneath the unchanged piano motif -- peace, not triumph -- and crucially this piece "
    "never rises to a big swell or crescendo: the strings only ever widen and warm, staying far "
    "behind the piano, a supportive glow that deepens gradually to the end without ever reaching a "
    "peak. Around twenty-one seconds in the motif turns plainer again, direct and unadorned, close "
    "and personal rather than grand. Around twenty-eight seconds in the phrases lengthen and open, "
    "warmer, inviting, unhurried, as if the same road that was forced on someone else is now being "
    "freely offered. Around thirty-nine seconds in the closing stretch settles into plain, humble "
    "stillness -- the motif one last time, slower and simpler than it has ever been, over the wide "
    "soft string glow, resolving completely and fading gently to silence only at the very end. "
    "Clean, airy, uncluttered mix with generous headroom, everything soft, underneath, and "
    "unhurried."
)


def dur(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def _mean_db(p: Path, ss: float, t: float) -> float | None:
    out = subprocess.run(
        ["ffmpeg", "-ss", str(ss), "-i", str(p), "-t", str(t), "-af", "volumedetect",
         "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.search(r"mean_volume:\s*(-?[0-9.]+) dB", out)
    return float(m.group(1)) if m else None


def check_no_dead_intro(p: Path, *, check_seconds: float = 10.0, window: float = 4.0,
                         threshold: float = -55.0) -> None:
    """Real defect found 2026-09-07: ElevenLabs Music can generate 50s+ of near-total
    silence (-90dB) before the audible piano starts, on a single long 'withheld' prompt.
    Fail loud rather than ship a broken score silently a second time -- every `window`s
    slice inside the first `check_seconds`s must show SOME audible content."""
    t = 0.0
    while t + window <= check_seconds:
        m = _mean_db(p, t, window)
        if m is not None and m > threshold:
            return
        t += window
    sys.exit(f"[FAIL] {p.name}: no audible content above {threshold}dB anywhere in the "
              f"first {check_seconds:.0f}s -- dead-intro defect. Do not ship; revise or regenerate.")


def _gen_music(prompt: str, glen: float, out: Path, key: str) -> None:
    import requests
    print(f"  requesting ~{glen:.1f}s ...", flush=True)
    r = requests.post(
        "https://api.elevenlabs.io/v1/music",
        headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
        json={"prompt": prompt, "music_length_ms": int(glen * 1000),
              "force_instrumental": True, "model_id": "music_v1"},
        timeout=300,
    )
    if r.status_code != 200:
        sys.exit(f"FAILED [{r.status_code}]: {r.text[:300]}")
    out.write_bytes(r.content)
    check_no_dead_intro(out)


def main() -> None:
    key = _resolve_key()
    if not key:
        sys.exit("no ELEVENLABS_API_KEY (PythonProject1/.env)")
    total = dur(NARRATION) + OUTRO_HOLD
    part1_len = SPLIT_S
    part2_len = total - SPLIT_S
    part1_glen = part1_len + OUTRO_MARGIN
    part2_glen = part2_len + OUTRO_MARGIN
    print(f"[full] narration={dur(NARRATION):.2f}s + {OUTRO_HOLD}s hold -> total {total:.2f}s, "
          f"split at {SPLIT_S:.2f}s (part1 {part1_len:.2f}s / part2 {part2_len:.2f}s)")

    print("[part1] withheld arc, front..F05")
    _gen_music(PART1_PROMPT, part1_glen, PART1_RAW, key)
    print("[part2] resolution onward, F06..back")
    _gen_music(PART2_PROMPT, part2_glen, PART2_RAW, key)

    # Trim each part to exactly its own span (no fades yet -- the crossfade below handles
    # the splice, the outer fade-in/out below handles the true start/end).
    p1_trim = HERE / "_p1_trim.mp3"
    p2_trim = HERE / "_p2_trim.mp3"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(PART1_RAW),
                    "-t", f"{part1_len + CROSSFADE_S:.2f}", str(p1_trim)], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(PART2_RAW),
                    "-t", f"{part2_len:.2f}", str(p2_trim)], check=True)

    # Crossfade the two parts together at the resolution boundary.
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-i", str(p1_trim), "-i", str(p2_trim),
        "-filter_complex", f"acrossfade=d={CROSSFADE_S}:c1=tri:c2=tri",
        str(RAW),
    ], check=True)
    p1_trim.unlink()
    p2_trim.unlink()
    check_no_dead_intro(RAW)

    joined_len = dur(RAW)
    print(f"[joined] {RAW.name} = {joined_len:.2f}s (expected ~{total + OUTRO_MARGIN - CROSSFADE_S:.2f}s)")

    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(RAW), "-af",
         f"afade=t=in:st=0:d=1.0,afade=t=out:st={total-2.0:.2f}:d=2.0",
         "-t", f"{total:.2f}", str(FITTED)], check=True)
    print(f"[done] {FITTED} ready at {dur(FITTED):.2f}s")


if __name__ == "__main__":
    main()
