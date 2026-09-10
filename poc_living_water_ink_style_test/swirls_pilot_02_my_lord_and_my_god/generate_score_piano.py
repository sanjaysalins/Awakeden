"""Score for My Lord and My God (John 20:24-29, Doubting Thomas).

Built score-design-early, against this episode's own REAL shot timeline
(ASSEMBLY_PLAN.md, measured from real synthesized narration): resolution
point is Shot 6 / F05, "My Lord and my God", 44.10s. Final duration 64.40s
(61.30s narration + 3.10s landing hold).

Free-text `music_v1` prompt with "around Xs in..." cues, NOT a
`composition_plan`/`music_v2` request -- that structured route is a
confirmed dead end in this project, per
[[feedback_score_design_early_validated]].

Reuses the felt-piano identity validated on episode 8 ("love this score,
this perhaps the best north star score") and evolved on Naaman ep4, Barrel
ep5, Bier ep7, She Loved Much ep10, Where Are the Nine ep11, and The Cross
ep13 -- now extended to this pilot episode too.

TWO-PART GENERATION (locked standard, not a fallback -- see
generate_score_piano.py in swirls_episode_13_the_cross_that_wasnt_his for
the original incident: a single continuous "withheld" score can render
50s+ of near-total silence before the piano ever starts). Split at this
episode's own resolution boundary, Shot 6's start (44.10s) -- Part 1
(front..F04, doubt through the invitation) stays withheld/questioning
throughout but is short enough (44.1s) not to trigger the defect; Part 2
(F05..back, ~20.3s) opens ALREADY resolved, a warm chord in its very first
bar.

Real timing (ASSEMBLY_PLAN.md):
  0.00-7.10s    front  the hook -- Thomas at a door, catching a sliver of light, refusing
  7.10-18.54s   f01    "I will not believe" -- doubt stated flatly, unsteady line
  18.54-24.0s   f02    eight days pass -- he stays, still unconvinced
  24.0-31.32s   f03    "Peace be unto you" -- Jesus simply there, doors still shut
  31.32-44.10s  f04    "Reach hither thy hand" -- the invitation, doubt loosening
  44.10-48.96s  f05    HERO -- "My Lord and my God" -- the confession, resolution
  48.96-52.72s  f06    "he answered him -- answered you too" -- the blessing extended
  52.72-64.40s  back   the landing -- the road, blessed are they that have not seen
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENV_PATH = Path(r"F:\slk\PycharmProjects\PythonProject1\.env")
NARRATION = HERE / "narration.mp3"
RAW = HERE / "score_piano_raw.mp3"
FITTED = HERE / "score_piano.mp3"
PART1_RAW = HERE / "score_piano_part1_raw.mp3"
PART2_RAW = HERE / "score_piano_part2_raw.mp3"
OUTRO_HOLD = 3.10  # matches the real, already-locked landing hold (INV-26)
OUTRO_MARGIN = 2.5
SPLIT_S = 44.10  # F05's own start -- the resolution boundary
CROSSFADE_S = 0.4

PART1_PROMPT = (
    "Intimate modern-classical felt piano, instrumental, slow and rubato, around 60 bpm. One "
    "quiet, tender felt-piano motif of just a few notes carries the entire piece as its lead and "
    "almost only voice, played sparsely with long pedal decays; brief, real silences of a beat or "
    "two happen BETWEEN individual phrases only, the way a pianist breathes between them -- the "
    "piano itself is audibly present and playing throughout, from its very first second onward, "
    "never falling fully silent for more than a couple of seconds at a time; no drums, no "
    "percussion, no bassline, nothing rhythmic at all, ever. The piece opens immediately, spare, "
    "plain, and a little guarded, the motif cool and unresolved in the piano's low-middle "
    "register, short phrases that stop rather than land -- a flat, plain refusal, arms folded, "
    "not yet convinced. Around seven seconds in the motif goes flatter and more matter-of-fact, "
    "stating rather than feeling, still withheld -- a stated condition, not an open question. "
    "Around eighteen seconds in the phrases lengthen very slightly and grow more patient, still "
    "unresolved but no longer sharp -- waiting has replaced refusing, days passing quietly. "
    "Around twenty-four seconds in a calmer, steadier figure enters, simple and even, without "
    "urgency -- a presence arriving plainly, nothing dramatic, still no resolution. Around "
    "thirty-one seconds in the motif turns gently inviting for the first time, one soft "
    "questioning phrase reaching upward and left open, unanswered, repeating with small variations "
    "as if held out and waited on, patient, never insistent, never quite resolving even as it "
    "keeps almost arriving. Clean, airy, uncluttered mix with generous headroom, everything soft, "
    "underneath, and unhurried, but audible throughout, ending still unresolved, mid-reach, on a "
    "quiet open phrase held out and unanswered, not a full stop."
)

PART2_PROMPT = (
    "Intimate modern-classical felt piano, instrumental, slow and rubato, around 60 bpm, "
    "continuing directly from a quiet unresolved held phrase, reached out and left open. The SAME "
    "quiet, tender felt-piano motif that has carried the piece so far now, in the very first bar, "
    "resolves outright at last: one plain, warm, unambiguous chord, held long in the pedal, the "
    "motif returning steadied and whole, as if a hand finally closed around what it had been "
    "reaching for -- this chord is the loudest, clearest, most present moment so far, struck "
    "immediately, not built up to. No drums, no percussion, no bassline, nothing rhythmic at all, "
    "ever; the piano remains audibly present throughout every section below, never falling fully "
    "silent. From around five seconds in (measured from this part's own start), one or two soft "
    "sustained string tones begin to glow underneath, almost imperceptibly at first, warm and "
    "still, never swelling, never rising to anything dramatic -- peace, not triumph, staying "
    "gentle and far behind the piano the whole time. Around twelve seconds in the motif opens "
    "slightly wider and warmer, generous rather than grand, as if the same welcome is now being "
    "offered outward, to whoever is listening. Around seventeen seconds in (measured from this "
    "part's own start) the closing stretch settles into plain, humble stillness -- the motif one "
    "last time, slower and simpler than it has ever been, over the soft string glow, resolving "
    "completely and fading gently to true silence only at the very end. Clean, airy, uncluttered "
    "mix with generous headroom, everything soft, underneath, and unhurried."
)


def _resolve_key() -> str | None:
    try:
        from dotenv import dotenv_values
        v = dotenv_values(ENV_PATH).get("ELEVENLABS_API_KEY")
        if v and v.strip():
            return v.strip()
    except Exception:
        pass
    return os.getenv("ELEVENLABS_API_KEY")


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
    """Real defect this project has hit twice before on ep13: ElevenLabs Music can generate
    50s+ of near-total silence (-90dB) before the audible piano starts, on a single long
    'withheld' prompt. Fail loud rather than ship a broken score silently. Every `window`s
    slice inside the first `check_seconds`s must show SOME audible content."""
    t = 0.0
    while t + window <= check_seconds:
        m = _mean_db(p, t, window)
        if m is not None and m > threshold:
            return
        t += window
    sys.exit(f"[FAIL] {p.name}: no audible content above {threshold}dB anywhere in the "
              f"first {check_seconds:.0f}s -- dead-intro defect. Do not ship; revise or regenerate.")


def timeline_sweep(p: Path, *, step: float = 5.0) -> None:
    """Full-file dead-air sweep -- a full-file mean/max can hide a long dead stretch
    in the MIDDLE of a track, per this project's own already-learned lesson."""
    total = dur(p)
    t = 0.0
    print(f"  [sweep] {p.name} ({total:.1f}s):")
    while t < total:
        window = min(step, total - t)
        m = _mean_db(p, t, window)
        print(f"    t={t:5.1f}s  mean={m if m is not None else 'n/a'} dB")
        t += step


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
    narr = dur(NARRATION)
    total = 64.40  # locked final duration of this episode's assembled cut
    part1_len = SPLIT_S
    part2_len = total - SPLIT_S
    part1_glen = part1_len + OUTRO_MARGIN
    part2_glen = part2_len + OUTRO_MARGIN
    print(f"[full] narration={narr:.2f}s, locked total={total:.2f}s, "
          f"split at {SPLIT_S:.2f}s (part1 {part1_len:.2f}s / part2 {part2_len:.2f}s)")

    print("[part1] withheld/doubt arc, front..F04")
    _gen_music(PART1_PROMPT, part1_glen, PART1_RAW, key)
    print("[part2] resolution onward, F05..back")
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
    timeline_sweep(RAW)

    joined_len = dur(RAW)
    print(f"[joined] {RAW.name} = {joined_len:.2f}s (expected ~{total + OUTRO_MARGIN - CROSSFADE_S:.2f}s)")

    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(RAW), "-af",
         f"afade=t=in:st=0:d=1.0,afade=t=out:st={total-2.0:.2f}:d=2.0",
         "-t", f"{total:.2f}", str(FITTED)], check=True)
    print(f"[done] {FITTED} ready at {dur(FITTED):.2f}s")
    timeline_sweep(FITTED)


if __name__ == "__main__":
    main()
