"""Score for Naaman in the Jordan.

Fable creative pass (2026-08-29): two candidate directions written for this
episode's own shape (fury -> gentle turning -> plain healing -> quiet landing),
not a reuse of the series' prior felt-piano north star (episode 8's "Fig Tree")
-- that episode had no anger beat and a different ending. Candidate A ("The
Argument", solo cello) built first per Fable's own recommendation: a single
voice gives the widest expressive range for the fury beat while staying the
most duckable texture (one line, real silence between phrases, no drums/
percussion/bassline ever -- the exact failure mode that sank the old "1990s
dream trance" identity on episode 8, "I hate the score and its too loud").
Candidate B ("The Plain Cure", harmonium + distant flute) is a second option,
not yet generated -- run generate_score_b.py if the user wants to hear it too.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode_04_naaman_in_the_jordan\\generate_score.py
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
RAW = HERE / "score_cello_raw.mp3"
FITTED = HERE / "score_cello.mp3"
OUTRO_HOLD = 3.0
OUTRO_MARGIN = 2.5

PROMPT = (
    "A solo cello, completely alone, closely miked in a small warm wooden room, playing a slow, "
    "sparse, rubato lament with no drums, no percussion, no bassline, no rhythmic pulse of any "
    "kind -- free-time phrases separated by real, audible silence where only the room breathes. "
    "The piece opens on a single high, tense, sustained note with a faint tremolo edge, minor "
    "and unresolved, held like held breath, then falling away to nothing. Around fifteen seconds "
    "in, the cello moves to its low register and states a plain, sober, almost spoken melody in "
    "short phrases, each one ending and leaving space, dynamics between pianissimo and "
    "mezzo-piano. Around thirty seconds the music reaches its one moment of heat: the bow digs "
    "in hard -- gritty, overpressured strokes, rough low double-stops, a raspy sul ponticello "
    "edge -- anger expressed entirely as friction and texture at the same quiet volume, never as "
    "speed, never as loudness, never as rhythm; two or three harsh gestures, each answered by "
    "silence. Then the anger drains: the same low melody returns softened, tender, hesitant, "
    "played gently as if being talked down. Around fifty seconds the register lifts suddenly "
    "into fragile natural harmonics -- high, glassy, weightless tones like light on moving "
    "water, open fifths, pure and astonished rather than triumphant, still very quiet, with long "
    "decays into silence between each touch. In the final stretch the cello restates the opening "
    "idea one last time in its plainest possible form, stripped of ornament, settling downward, "
    "and the piece ends on a single long, warm open-string note that simply fades into room tone "
    "-- no final chord, no swell, no resolution flourish -- leaving three full seconds of "
    "near-silence at the end. Mix character: intimate, dry, woody, with the bow noise and finger "
    "sounds audible; huge headroom, nothing dense, nothing layered, the entire piece one "
    "unaccompanied voice that a spoken narration can always sit on top of. Mood: grave, "
    "restrained, humble, ancient; a private argument that ends in surrender and peace."
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
