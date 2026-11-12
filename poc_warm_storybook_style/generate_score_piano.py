"""Score for "Mary and Martha" (Warm Storybook POC, Luke 10:38-42 + John 11:5).

Same felt-piano identity and TWO-PART generation as ep16 (copied from its generate_score_piano.py),
split at the resolution: "So, did He care?" (64.55 s, whisperx). Part 2 resolves on
"Now Jesus loved Martha" (69.29 s = ~4.9 s into part 2). Free-text music_v1, never composition_plan.
Owner yes 2026-11-12 (~$2.50).
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pipeline.assembly_align import _resolve_key  # noqa: E402

HERE = Path(__file__).resolve().parent
FINAL_VIDEO = HERE / "MARY_MARTHA_PREVIEW_v1.mp4"
RAW = HERE / "score_piano_raw.mp3"
FITTED = HERE / "score_piano.mp3"
PART1_RAW = HERE / "score_piano_part1_raw.mp3"
PART2_RAW = HERE / "score_piano_part2_raw.mp3"
SPLIT_S = 64.40  # "So, did He care?" -- the resolution boundary
OUTRO_MARGIN = 2.5
CROSSFADE_S = 0.4

PART1_PROMPT = (
    "Intimate modern-classical felt piano, instrumental, slow and rubato, around 60 bpm. One "
    "quiet, tender felt-piano motif of just a few notes carries the entire piece as its lead and "
    "almost only voice, played sparsely with long pedal decays; the piano is audibly present and "
    "playing throughout, from its very first second onward, never falling fully silent for more "
    "than a couple of seconds at a time; no drums, no percussion, no bassline, nothing rhythmic "
    "at all, ever. The very first piano note sounds at second zero, the instant the piece begins, with no silent lead-in. From that first note the motif plays softly but clearly, a little tired and lonely, small and alone in "
    "the piano's middle register, like someone working late in an empty kitchen. Around ten "
    "seconds in the motif warms, a home with its door open, a guest welcomed. Around fourteen "
    "seconds in it grows very still and gentle, someone sitting and listening. Around eighteen "
    "seconds in the phrases turn uneasy and unfinished, a few low, worried notes beneath, a "
    "complaint held in for too long, never loud. Around twenty-six seconds in the motif softens "
    "into great tenderness, a gentle voice saying a name, and the same two soft notes are played "
    "twice, kindly. Around thirty-seven seconds in the motif walks gently and simply, patient and "
    "unhurried, like a careful explanation. Around fifty-two seconds in the piano opens into plain, "
    "warm, close chords, still not fully resolved. Around sixty seconds in it thins to one soft, "
    "open, questioning phrase, always clearly audible, waiting. Clean, airy, uncluttered mix with "
    "generous headroom, everything soft, underneath, and unhurried, but audible throughout with no "
    "gaps, ending unresolved and open, not a full stop."
)

PART2_PROMPT = (
    "Intimate modern-classical felt piano, instrumental, slow and rubato, around 60 bpm, "
    "continuing directly from a quiet, open, questioning phrase. For the first four seconds the "
    "same tender felt-piano motif asks its question softly once more, open and waiting. Around "
    "five seconds in, the motif resolves outright at last: one plain, warm, full chord, held long "
    "in the pedal, like being told you are loved -- the warmest, most settled the piece has been. "
    "No drums, no percussion, no bassline, nothing rhythmic at all, ever; the piano remains "
    "audibly present throughout, never falling fully silent. From around eight seconds in "
    "(measured from this part's own start), a single soft, sustained string tone begins to "
    "underlie the piano, barely there, widening the warmth without ever swelling to a peak. "
    "Around twelve seconds in the motif turns more direct and personal, closer and quieter, as if "
    "someone was right there in the room all along. Around fifteen seconds in the motif returns "
    "one more time, gentle and fully present, and keeps playing steadily at the same soft level "
    "right through to the very last second of the piece, with no fade-out and no early ending; "
    "the final chord is still ringing when the piece stops. Clean, airy, uncluttered mix with "
    "generous headroom, everything soft, underneath, and unhurried."
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
    part2_glen = part2_len + 8.0  # v1 faded out by 14 s; ask longer, trim
    print(f"[full] final video={total:.2f}s, split at {SPLIT_S:.2f}s "
          f"(part1 {part1_len:.2f}s / part2 {part2_len:.2f}s)")

    print("[part1] withheld arc, hook..explanation")
    if PART1_RAW.exists():
        print(f"[part1] reusing existing {PART1_RAW.name} (no re-spend)")
    else:
        _gen_music(PART1_PROMPT, part1_glen, PART1_RAW, key)
    if PART2_RAW.exists():
        print(f"[part2] reusing existing {PART2_RAW.name} (already verified clean, no re-spend)")
        check_no_dead_intro(PART2_RAW)
    else:
        print("[part2] resolution onward, here-is-what-He-did..end")
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
