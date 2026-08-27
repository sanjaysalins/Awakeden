"""Epic-soft north-star score for Jacob's Ladder — replaces the old "1990s
dream trance" score_final.mp3 with a near-verbatim reuse of the "Fig Tree"
felt-piano identity (the user's own north star, 2026-08-24/25).

SECOND Fable pass (2026-08-27): the FIRST "epic" pass rewrote the whole
prompt from scratch (new imagery, added choir, restructured pacing) and the
user said it "lost the intimacy" and that the prompt-writing itself was the
problem, not the epic concept (see memory
feedback-fable-prompt-rewrite-dilutes-proven-direction). This version starts
from the exact original Fig Tree prompt verbatim and makes exactly ONE
surgical insertion (low cellos + soft double bass entering at the swell for
quiet depth, no choir -- the SFX bed already places a real choir on the
gospel-pivot line, so this stays support not competition) plus swaps the
closing emotional phrase to Jacob's own arc. Every other word is unchanged
from the proven original.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_pilot_01_jacobs_ladder\\generate_score_epic.py
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
    "quiet, tender felt-piano motif of just a few notes carries the entire piece as its only "
    "voice, played sparsely with long pedal decays and real silence between phrases; no drums, "
    "no percussion, no bassline, nothing rhythmic at all. A soft warm string pad and a faint "
    "breath of tape hiss sit far behind the piano, barely audible, supportive never prominent. "
    "In the final third the strings gently rise and open into a wide, radiant, hopeful swell, "
    "low cellos and a soft double bass entering underneath for the first time to give the swell "
    "quiet depth, while the piano keeps the same simple motif unchanged. Nocturnal, tender, "
    "awestruck, the feeling of waking on open ground to find heaven standing open above you; a "
    "clean, airy, uncluttered mix with generous space."
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
