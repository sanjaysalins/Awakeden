"""Score for The Bier He Touched (Luke 7:11-17, the widow of Nain).

Reuses the felt-piano "Fig Tree"/epic-soft identity validated on episode 8
("love this score, this perhaps the best north star score", see
[[feedback_score_felt_piano_over_trance]]) and evolved on Naaman ep4 and the
Barrel ep5 ("lock this, this is great" / a two-episode-validated series
identity), now extended to a third narrative arc. Per
[[feedback_fable_prompt_rewrite_dilutes_proven_direction]], this is a
near-verbatim evolution of the Barrel's own winning prompt, not a
reinvention: same instrument, same core rules (no drums/percussion/bassline
ever, no big swell, strings widen but never peak). The only real change is
WHAT the piano's turning moments mean and WHEN they land, re-timed to this
episode's own arc (word-weight proportional against the 184-word/69.03s
locked narration, matching the assemble MANIFEST's own unit word weights):

  0.0-8.6s   front  grief -- the widow behind the bier, "all she had left"
  8.6-16.5s  f01    the law of distance -- everyone kept away
  16.5-25.5s f02    Jesus walks TOWARD her; "Weep not" -- the first warmth
  25.5-34.1s f03    he touches the bier; the bearers stand still -- held breath
  34.1-44.6s f04    "the touch should have made him unclean" -> "Arise" -- the turn
  44.6-51.4s f05    the boy sits up, speaks, is delivered to his mother
  51.4-57.0s f06    "Death didn't spread... Life spread" -- the reversal named
  57.0-69.0s back   "it became a homecoming" -- the landing

Distinct from the Barrel's single dread->relief arc: this piece has TWO
turning moments -- a quiet warming at "Weep not" (compassion, not yet
resolution) and the real harmonic resolution at "Arise" -- so the piano
passes through withdrawn/guarded (the law of distance) rather than dread,
softens without resolving at the first Jesus line, then fully resolves at
the touch/command. Strings enter after the resolution (the boy sitting up),
not before it, so their gathering warmth tracks the restoration rather than
anticipating it.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode_07_the_bier_he_touched\\generate_score_piano.py
"""
from __future__ import annotations

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
OUTRO_HOLD = 3.0
OUTRO_MARGIN = 2.5

PROMPT = (
    "Intimate modern-classical felt piano, instrumental, slow and rubato, around 60 bpm. One "
    "quiet, tender felt-piano motif of just a few notes carries the entire piece as its lead and "
    "almost only voice, played sparsely with long pedal decays and real silence between phrases; "
    "no drums, no percussion, no bassline, nothing rhythmic at all, ever. The opening is spare "
    "and hollow, the motif grieving and unguarded in the piano's middle-to-low register, small "
    "phrases trailing off into real silence rather than resolving -- a private sorrow, walking "
    "behind something already lost. Around eight seconds in, the same piano -- and only the "
    "piano -- draws inward: the touch grows lighter and more withdrawn, the phrases shorter and "
    "further apart, spacing itself out as if keeping a careful distance; no dissonance, no "
    "anger, just a guarded, held-back quality, colder than the opening. Around sixteen seconds "
    "in, on a single clear moment, the piano softens without fully resolving: one gentle, warmer "
    "interval is struck and left to ring, the motif loosening and drawing nearer again, tentative "
    "compassion rather than relief. Around twenty-five seconds in the piece goes almost still: "
    "one long sustained tone, held far longer than anything before it, the phrases nearly "
    "stopping altogether -- a held breath, waiting. Around thirty-four seconds in, on a single "
    "clear moment, that held stillness resolves outright: one plain, warm, unambiguous chord, "
    "held long in the pedal, the motif returning steadied and simple, as if a held breath had "
    "finally been let out. From around forty seconds, strings begin to gather underneath one "
    "section at a time, each entry almost imperceptible: soft violas first, then muted violins, "
    "then low cellos, sustaining long warm tones that slowly widen the harmony beneath the "
    "unchanged piano motif -- wonder, not triumph -- and crucially this piece never rises to a "
    "big swell or crescendo: the strings only ever widen and warm, staying far behind the piano, "
    "a supportive glow that deepens gradually to the end without ever reaching a peak. The "
    "closing stretch settles into plain, humble stillness -- the motif one last time, slower and "
    "simpler than it has ever been, over the wide soft string glow, resolving completely and "
    "fading gently to silence. Grieving, guarded, steadied, the feeling of a distance closed by "
    "one who was never afraid to cross it; a clean, airy, uncluttered mix with generous headroom, "
    "everything soft, underneath, and unhurried."
)


def dur(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def main() -> None:
    key = _resolve_key()
    if not key:
        sys.exit("no ELEVENLABS_API_KEY (PythonProject1/.env)")
    import requests
    total = dur(NARRATION) + OUTRO_HOLD
    glen = total + OUTRO_MARGIN
    print(f"[full] narration={dur(NARRATION):.2f}s + {OUTRO_HOLD}s hold -> generating ~{glen:.1f}s ...")
    r = requests.post(
        "https://api.elevenlabs.io/v1/music",
        headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
        json={"prompt": PROMPT, "music_length_ms": int(glen * 1000),
              "force_instrumental": True, "model_id": "music_v1"},
        timeout=300,
    )
    if r.status_code != 200:
        sys.exit(f"FAILED [{r.status_code}]: {r.text[:300]}")
    RAW.write_bytes(r.content)
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(RAW), "-af",
         f"afade=t=in:st=0:d=1.0,afade=t=out:st={total-2.0:.2f}:d=2.0",
         "-t", f"{total:.2f}", str(FITTED)], check=True)
    print(f"[done] {FITTED} ready at {dur(FITTED):.2f}s")


if __name__ == "__main__":
    main()
