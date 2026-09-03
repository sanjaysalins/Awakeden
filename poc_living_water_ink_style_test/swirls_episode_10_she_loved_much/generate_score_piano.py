"""Score for She Loved Much (Luke 7:36-50, the woman who washed Jesus's feet).

Reuses the felt-piano "Fig Tree" identity validated on episode 8 ("love this
score, this perhaps the best north star score", see
[[feedback_score_felt_piano_over_trance]]) and evolved on Naaman ep4, the
Barrel ep5, and the Bier ep7 (a four-episode-validated series identity), now
extended to a fifth arc. Per
[[feedback_fable_prompt_rewrite_dilutes_proven_direction]], this is a
near-verbatim evolution of the prior episodes' own winning prompt, not a
reinvention: same instrument, same core rules (no drums/percussion/bassline
ever, no big swell, strings widen but never peak, real silence between
phrases). The only real change is WHAT the piano's turning moments mean and
WHEN they land, re-timed to this episode's own arc (word-weight proportional
against the 240-word/103.29s locked narration, matching the assemble
MANIFEST's own unit word weights):

  0.0-3.9s    front  the three absences -- "no water, no kiss, no oil"
  3.9-14.6s   f01    she walks in anyway, uninvited, carrying the stain
  14.6-24.5s  f02    she stands behind him, weeping -- the tears begin
  24.5-32.3s  f03    the kiss, the ointment -- her love at its rawest,
                       NOT yet the resolution (the stain stays unchanged here)
  32.3-42.6s  f04    Simon's unspoken judgment; the first blue thread answers it
  42.6-53.8s  f05    the parable -- debt forgiven freely, a first tentative warmth
  53.8-61.6s  f06    Simon's grudging hedge -- held, withheld, waiting
  61.6-69.7s  f07    "Seest thou this woman?" -- the crossing point
  69.7-82.6s  f08    "Her sins... are forgiven" -- THE resolution, the hero page
  82.6-92.5s  f09    "Thy faith hath saved thee" -- strings gather, Stage 3
  92.5-103.3s back   "she left carrying his peace" -- the landing, +3.0s hold

Distinct from ep7's single withheld->resolved arc: THIS piece has to hold its
resolution back for longer and more deliberately, because the doctrine itself
demands it -- her tears and her kiss (f02-f03) are the emotional peak of her
own love, but the visual design keeps the stain completely unchanged through
both those pages (the narration's own "Not thy tears. Not thy ointment."),
so the score must NOT resolve there either, or it would musically re-commit
the exact backwards-causality error the whole episode was built to avoid.
Instead f02-f03 stay tender but genuinely unresolved -- aching, private,
unanswered -- and the real turn doesn't begin until f05 (the parable's first
spoken forgiveness), builds through the withheld f06 and the crossing-point
f07, and only fully resolves at f08, exactly where the visual stain also
clears to a dried ring. Strings enter after that resolution, not before it
(same rule as ep7), so their gathering warmth tracks Stage 3's diffusion
(f09) rather than anticipating it.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode_10_she_loved_much\\generate_score_piano.py
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
    "and plain, a little withholding, the motif cool and unresolved in the piano's "
    "middle register, small phrases that stop short rather than land -- something being kept "
    "back. Around four seconds in, on the same plain motif, a quiet, private tenderness enters -- "
    "the touch grows softer and closer, but still does not resolve; the phrases linger and ache "
    "rather than settle, unanswered, intimate, almost too much, never once relaxing into a full "
    "chord. Around thirty-two seconds in the piano cools again, drawing back to something more "
    "guarded and closed, the phrases shorter and more careful, no warmth given away. Around "
    "forty-three seconds in, on a single clear moment, the piano softens without fully resolving: "
    "one gentle, warmer interval is struck and left to ring, tentative, a first small kindness, "
    "still short of relief. Around fifty-four seconds in the piece goes almost still: one long "
    "sustained tone, held far longer than anything before it, the phrases nearly stopping "
    "altogether -- a held breath, waiting, withheld on purpose. Around seventy seconds in, on a "
    "single clear moment, that held stillness resolves outright at last: one plain, warm, "
    "unambiguous chord, held long in the pedal, the motif returning steadied and simple, as if "
    "a debt had actually been forgiven. From around eighty-three seconds, strings begin to "
    "gather underneath one section at a time, each entry almost imperceptible: soft violas "
    "first, then muted violins, then low cellos, sustaining long warm tones that slowly widen "
    "the harmony beneath the unchanged piano motif -- peace, not triumph -- and crucially this "
    "piece never rises to a big swell or crescendo: the strings only ever widen and warm, "
    "staying far behind the piano, a supportive glow that deepens gradually to the end without "
    "ever reaching a peak. The closing stretch settles into plain, humble stillness -- the motif "
    "one last time, slower and simpler than it has ever been, over the wide soft string glow, "
    "resolving completely and fading gently to silence. Withheld, aching, finally answered; a "
    "clean, airy, uncluttered mix with generous headroom, everything soft, underneath, and "
    "unhurried."
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
