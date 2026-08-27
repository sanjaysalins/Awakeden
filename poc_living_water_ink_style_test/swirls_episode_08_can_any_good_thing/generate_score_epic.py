"""Epic-soft north-star score for Can Any Good Thing -- upgrades the existing
"Fig Tree" felt-piano score_final.mp3 (this is the episode the north star
came FROM) to the fuller epic-soft direction, WITHOUT adding a swell.

Fable design pass (2026-08-27): same non-negotiable core as Fig Tree (felt
piano lead, no drums/percussion/bassline/rhythmic pulse ever, real silence
between phrases, clean/airy/uncluttered mix). Tailored to this episode: this
is the MOST restrained of the three, on purpose -- this episode's own SFX
bed (built today) already runs a real two-take choir crescendo across the
entire back half (confession -> Jacob's-Ladder vision -> dusk landing,
roughly 33-46s), so the score never rises to a swell at all. Its "epic" is a
slow, continuous string-widening (violas, then violins, then low cellos,
entering one at a time from the midpoint) that trails underneath the real
choir instead of competing with it for the same peak.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode_08_can_any_good_thing\\generate_score_epic.py
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
RAW = HERE / "score_epic_raw.mp3"
FITTED = HERE / "score_epic.mp3"
OUTRO_HOLD = 3.0
OUTRO_MARGIN = 2.5

PROMPT = (
    "Intimate modern-classical felt piano, instrumental, slow and rubato, around 60 bpm. One "
    "quiet, tender felt-piano motif of just a few notes carries the entire piece as its lead and "
    "almost only voice, played sparsely with long pedal decays and real silence between phrases; "
    "no drums, no percussion, no bassline, nothing rhythmic at all, ever. The opening has a "
    "gentle early-morning lightness, the motif simple and unguarded in the piano's middle "
    "register. Through the middle stretch the piano is completely alone -- no pad, no strings, "
    "nothing behind it -- intimate and personal, each small phrase left hanging in true silence, "
    "the feeling of a private moment quietly witnessed. From around the halfway point, strings "
    "begin to gather underneath one section at a time, each entry almost imperceptible: soft "
    "violas first, then muted violins, and finally low cellos, sustaining long warm tones that "
    "slowly widen the harmony beneath the unchanged piano motif. Crucially, this piece never "
    "rises to a big swell or crescendo: the strings only ever widen and warm, staying far behind "
    "the piano, a supportive glow that deepens gradually and continuously to the end without ever "
    "reaching a peak. The closing stretch settles into dusk-warm stillness -- the motif one last "
    "time, slower, over the wide soft string glow, resolving completely and fading gently to "
    "silence. Tender, wondering, seen and known, the feeling of doubt falling away before someone "
    "who was watching kindly all along; a clean, airy, uncluttered mix with generous headroom, "
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
