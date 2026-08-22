"""Score for The Ashes That Made Clean — reuses the exact prompt validated
and locked on Jacob's Ladder (the "single lead voice" fix), regenerated at
THIS episode's own length. Same score identity across the series, per the
"north star" template.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode_02_ashes_that_made_clean\\generate_score.py
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
RAW = HERE / "score_final_raw.mp3"
FITTED = HERE / "score_final.mp3"
OUTRO_HOLD = 3.0
OUTRO_MARGIN = 2.5

PROMPT = (
    "1990s dream trance, instrumental, 135 bpm. ONE clear ethereal acoustic piano melody "
    "carries the whole piece as its single lead voice, with no second competing melodic line "
    "and no countermelody fighting it. A steady four-on-the-floor kick and a simple hypnotic "
    "bassline sit underneath, mixed cleanly and kept simple, never busy. Warm ambient synth "
    "pads fill the background softly, supportive rather than prominent. Nostalgic, "
    "melancholic but uplifting, soothing club comedown atmosphere. Minimal delay and echo, a "
    "clean, uncluttered, unlayered mix."
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
