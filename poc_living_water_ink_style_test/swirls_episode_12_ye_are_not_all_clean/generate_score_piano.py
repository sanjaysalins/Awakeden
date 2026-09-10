"""Score for "Ye Are Not All Clean" (John 13:1-30, Judas).

Built the same way as ep4/ep5/ep7/ep10/ep11/ep13 -- the six-episode-validated felt-piano
"Fig Tree" identity (locked after episode 8, "love this score, this perhaps the best north
star score"), TWO-PART generation split at the episode's own resolution point (F06, the
"unconditional grace" hero beat), per [[feedback_score_dead_air_two_part_generation_fix]] --
now the LOCKED STANDARD, not a fallback. Free-text `music_v1` prompt with "around Xs in..."
cues, not `composition_plan`/`music_v2` (a confirmed dead end, [[feedback_score_design_early_
validated]]).

This episode is a Google-Flow-piloted delivery (not OpenArt/HF), so there is no `episode.py`/
`unit_timing.json` -- timing comes straight from the real forced-alignment already run on the
locked `narration.mp3` (`narration.alignment.json`) and the real per-beat boundaries already
used to build `_assembly_v1/viral_cut_no_score.mp4`.

Real timing (matches _assembly_v1's own video timeline exactly):
  0.00-3.74s    front  the hook -- Judas walked out on feet Jesus had washed
  3.74-13.36s   F01    Jesus knew -- the devil already in Judas's heart
  13.36-19.52s  F02    the washing -- Jesus pours water, dries feet (swirl begins)
  19.52-34.38s  F03    "ye are clean, but not all" + the betrayal prophecy
  34.38-46.46s  F04    the sop, "do quickly," the misunderstanding
  46.46-50.34s  F05    "and it was night" -- Judas walks out (the dark page)
  50.34-63.34s  F06    HERO -- "knowing he wouldn't... that is what His love does" (the resolution)
  63.34-77.83s  back   "He knows your heart... bring Him your worst" (the landing + hold)

Split at F06's own start (50.34s) -- Part 1 (front..F05) stays withheld throughout; Part 2
(F06..back) opens already resolved in its first bar, matching the two-part fix's own logic.
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
FINAL_VIDEO = HERE / "_assembly_v1" / "viral_cut_no_score.mp4"
RAW = HERE / "score_piano_raw.mp3"
FITTED = HERE / "score_piano.mp3"
PART1_RAW = HERE / "score_piano_part1_raw.mp3"
PART2_RAW = HERE / "score_piano_part2_raw.mp3"
SPLIT_S = 50.34  # F06's own start -- the resolution boundary
OUTRO_MARGIN = 2.5
CROSSFADE_S = 0.4

PART1_PROMPT = (
    "Intimate modern-classical felt piano, instrumental, slow and rubato, around 60 bpm. One "
    "quiet, tender felt-piano motif of just a few notes carries the entire piece as its lead and "
    "almost only voice, played sparsely with long pedal decays; the piano is audibly present and "
    "playing throughout, from its very first second onward, never falling fully silent for more "
    "than a couple of seconds at a time; no drums, no percussion, no bassline, nothing rhythmic "
    "at all, ever. The piece opens quiet and plain, a little uneasy, the motif cool and withheld "
    "in the piano's low-middle register -- a familiar, ordinary evening that is not what it "
    "seems. Around four seconds in the motif turns a shade darker, still quiet, a private "
    "knowledge already settled and unmoving. Around fourteen seconds in a small, warm phrase "
    "rises briefly -- a simple act of care, gentle, unforced -- then within a few seconds it "
    "recedes again, because the piece is not ready to resolve yet. Around twenty seconds in the "
    "motif turns plainer and more grave, almost spoken, naming something the room does not yet "
    "understand. Around thirty-five seconds in the piece grows a little more tense, a held, "
    "watchful quality, brief small intervals repeating without settling -- something changing "
    "hands, quietly, and no one else noticing. Around forty-six seconds in the piece narrows to a "
    "single slow, low, repeating phrase -- spare, but always clearly and continuously audible, "
    "never approaching silence -- as if someone is walking away and not looking back. Clean, "
    "airy, uncluttered mix with generous headroom, everything soft, underneath, and unhurried, "
    "but audible throughout with no gaps, ending still unresolved, thin and open, not a full "
    "stop."
)

PART2_PROMPT = (
    "Intimate modern-classical felt piano, instrumental, slow and rubato, around 60 bpm, "
    "continuing directly from a quiet unresolved held phrase. The SAME quiet, tender felt-piano "
    "motif that has carried the piece so far now, in the very first bar, resolves outright at "
    "last: one plain, warm, unambiguous chord, held long in the pedal, struck immediately, not "
    "built up to -- the truest, most settled the piece has been, without hesitation. No drums, no "
    "percussion, no bassline, nothing rhythmic at all, ever; the piano remains audibly present "
    "throughout, never falling fully silent. From around eight seconds in (measured from this "
    "part's own start), a single soft, sustained string tone begins to underlie the piano, barely "
    "there, widening the warmth without ever swelling or rising to a peak -- steady, held, "
    "unhurried. Around thirteen seconds in the motif turns more direct and personal, closer, "
    "quieter, as if speaking straight to one listener. Around twenty seconds in the phrases "
    "settle into their simplest, plainest shape yet, warm and unhurried, resolving gently and "
    "completely, fading only in the very last bar. Clean, airy, uncluttered mix with generous "
    "headroom, everything soft, underneath, and unhurried."
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
    """Real defect found on ep13 (2026-09-07): ElevenLabs Music can generate 50s+ of near-total
    silence before the audible piano starts, on a single long 'withheld' prompt. Fail loud rather
    than ship a broken score silently -- every `window`s slice inside the first `check_seconds`s
    must show SOME audible content."""
    t = 0.0
    while t + window <= check_seconds:
        m = _mean_db(p, t, window)
        if m is not None and m > threshold:
            return
        t += window
    sys.exit(f"[FAIL] {p.name}: no audible content above {threshold}dB anywhere in the "
              f"first {check_seconds:.0f}s -- dead-intro defect. Do not ship; revise or regenerate.")


def check_timeline_sweep(p: Path, *, window: float = 5.0, threshold: float = -55.0) -> None:
    """The bigger lesson from the same ep13 incident: a whole-file mean/max measurement can
    completely hide a 50+ SECOND dead stretch in the MIDDLE of a piece, not just the intro.
    Sweep the entire timeline in windows, not just the first check_seconds."""
    total = dur(p)
    t = 0.0
    dead_spans = []
    while t < total:
        w = min(window, total - t)
        m = _mean_db(p, t, w)
        if m is None or m <= threshold:
            dead_spans.append((round(t, 1), round(t + w, 1)))
        t += window
    if dead_spans:
        sys.exit(f"[FAIL] {p.name}: dead/near-silent span(s) found in a full timeline sweep: "
                  f"{dead_spans} -- do not ship; revise or regenerate.")
    print(f"  [ok] timeline sweep clean, no window below {threshold}dB across {total:.1f}s")


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
    total = dur(FINAL_VIDEO)
    part1_len = SPLIT_S
    part2_len = total - SPLIT_S
    part1_glen = part1_len + OUTRO_MARGIN
    part2_glen = part2_len + OUTRO_MARGIN
    print(f"[full] final video={total:.2f}s, split at {SPLIT_S:.2f}s "
          f"(part1 {part1_len:.2f}s / part2 {part2_len:.2f}s)")

    print("[part1] withheld arc, front..F05")
    _gen_music(PART1_PROMPT, part1_glen, PART1_RAW, key)
    if PART2_RAW.exists():
        print(f"[part2] reusing existing {PART2_RAW.name} (already verified clean, no re-spend)")
        check_no_dead_intro(PART2_RAW)
    else:
        print("[part2] resolution onward, F06..back")
        _gen_music(PART2_PROMPT, part2_glen, PART2_RAW, key)

    p1_trim = HERE / "_p1_trim.mp3"
    p2_trim = HERE / "_p2_trim.mp3"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(PART1_RAW),
                    "-t", f"{part1_len + CROSSFADE_S:.2f}", str(p1_trim)], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(PART2_RAW),
                    "-t", f"{part2_len:.2f}", str(p2_trim)], check=True)

    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-i", str(p1_trim), "-i", str(p2_trim),
        "-filter_complex", f"acrossfade=d={CROSSFADE_S}:c1=tri:c2=tri",
        str(RAW),
    ], check=True)
    p1_trim.unlink()
    p2_trim.unlink()
    check_no_dead_intro(RAW)
    check_timeline_sweep(RAW)

    joined_len = dur(RAW)
    print(f"[joined] {RAW.name} = {joined_len:.2f}s (expected ~{total + OUTRO_MARGIN - CROSSFADE_S:.2f}s)")

    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(RAW), "-af",
         f"afade=t=in:st=0:d=1.0,afade=t=out:st={total-2.0:.2f}:d=2.0",
         "-t", f"{total:.2f}", str(FITTED)], check=True)
    check_timeline_sweep(FITTED)
    print(f"[done] {FITTED} ready at {dur(FITTED):.2f}s")


if __name__ == "__main__":
    main()
