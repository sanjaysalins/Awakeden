"""Score for Naaman in the Jordan -- take 2.

The first Fable pass (solo cello, `generate_score.py` / score_cello.mp3) was
rejected by the user: "I dont like this, its not fables best work" -- no more
specific complaint. That pass had deliberately avoided reusing episode 8's
loved felt-piano "Fig Tree"/epic-soft identity (user: "love this score, this
perhaps the best north star score", see [[feedback_score_felt_piano_over_trance]])
in favor of inventing new instrumentation from scratch. See
[[feedback_naaman_score_cello_rejected]].

This take fixes that: Fable was handed the actual winning epic-soft prompt
verbatim and asked to evolve it with the smallest changes that serve this
story, not reinvent it (per [[feedback_fable_prompt_rewrite_dilutes_proven_direction]]).
Same felt piano throughout -- exactly two surgical edits: a ~30s fury passage
where the SAME piano turns hard through touch/harmony alone (low register,
harder attacks, dissonant clusters, tightened phrasing, never louder/faster
as rhythm), and the string entry moved to ~50s so the warmth lands on the
healing beat instead of the generic halfway point.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode_04_naaman_in_the_jordan\\generate_score_piano.py
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
    "no drums, no percussion, no bassline, nothing rhythmic at all, ever. The opening has a "
    "gentle early-morning lightness, the motif simple and unguarded in the piano's middle "
    "register, each small phrase left hanging in true silence, a private moment quietly "
    "witnessed. Just before the halfway point, around thirty seconds in, the same piano -- and "
    "only the piano -- briefly turns hard: the motif drops into the low register with firmer, "
    "heavier hammer attacks, a dissonant cluster or two struck and left to ring into the pedal, "
    "the phrases suddenly tighter and closer together, crowding the silence without ever filling "
    "it; the anger lives entirely in touch and harmony, never in volume or rhythm -- no "
    "percussion arrives, no pulse forms, and within a few phrases the tension loosens, the "
    "clusters resolve, the spacing opens back out, and the motif returns chastened to the middle "
    "register as if talked gently down. From around fifty seconds, strings begin to gather "
    "underneath one section at a time, each entry almost imperceptible: soft violas first, then "
    "muted violins, then low cellos, sustaining long warm tones that slowly widen the harmony "
    "beneath the unchanged piano motif -- wonder, not triumph -- and crucially this piece never "
    "rises to a big swell or crescendo: the strings only ever widen and warm, staying far behind "
    "the piano, a supportive glow that deepens gradually to the end without ever reaching a peak. "
    "The closing stretch settles into plain, humble stillness -- the motif one last time, slower "
    "and simpler than it has ever been, over the wide soft string glow, resolving completely and "
    "fading gently to silence. Tender, humbled, wondering, the feeling of fury laid down in plain "
    "water and an argument worth losing; a clean, airy, uncluttered mix with generous headroom, "
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
