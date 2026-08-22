"""Jacob's Ladder pilot — "modern groove" score, generated via ElevenLabs Music.

No cue in this repo's whole library (sound_library, music_library, the Suno
catalogue, the northstar POC's own score) is a modern/rhythmic/groove track —
every existing score is deliberately orchestral/ambient/reverent, "no drums,
no bassline, no electronic pulse" baked into every prior brief. This is a
genuine, user-requested departure, so it's generated fresh rather than reused.

Two-step, per the user's explicit approval: a short PREVIEW first (~20s, same
prompt) to react to before spending on the full-length track. No named
artist/song anywhere in the prompt (ElevenLabs Music ToS hard-blocks that).

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_pilot_01_jacobs_ladder\\generate_score.py --preview
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_pilot_01_jacobs_ladder\\generate_score.py --full
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline.assembly_align import _resolve_key  # noqa: E402

HERE = Path(__file__).resolve().parent
PREVIEW = HERE / "score_groove_preview.mp3"
RAW = HERE / "score_groove_raw.mp3"
FITTED = HERE / "score_groove.mp3"
OUTRO_HOLD = 3.0
OUTRO_MARGIN = 2.5

PROMPT = (
    "A modern, warm instrumental groove — a laid-back, contemporary beat built on a soft "
    "electronic kick and a gentle rimshot-style snare, a smooth, rounded synth-bass line "
    "moving underneath, warm analog synth pad chords holding a hopeful, uplifting major "
    "key, and a simple, clean electric-piano or plucked-synth melody line drifting on top. "
    "The groove stays understated and steady throughout, never aggressive, never clubby — "
    "closer to a modern devotional/contemporary-worship instrumental bed than a dance "
    "track, present and alive without ever fighting a spoken voice sitting on top of it. "
    "Instrumental only, no vocals, no choir."
)


def dur(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def _post(key: str, prompt: str, length_ms: int, out: Path) -> None:
    import requests
    r = requests.post(
        "https://api.elevenlabs.io/v1/music",
        headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
        json={"prompt": prompt, "music_length_ms": length_ms,
              "force_instrumental": True, "model_id": "music_v1"},
        timeout=300,
    )
    if r.status_code != 200:
        sys.exit(f"[music] FAILED [{r.status_code}]: {r.text[:300]}")
    out.write_bytes(r.content)
    print(f"[music] ok -> {out} ({dur(out):.1f}s)")


def main() -> None:
    key = _resolve_key()
    if not key:
        sys.exit("no ELEVENLABS_API_KEY (PythonProject1/.env)")

    if "--preview" in sys.argv:
        print("[preview] ~20s candidate, same prompt as the full track ...")
        _post(key, PROMPT, 20_000, PREVIEW)
        return

    if "--full" in sys.argv:
        narration = HERE / "narration.mp3"
        total = dur(narration) + OUTRO_HOLD
        glen = total + OUTRO_MARGIN
        print(f"[full] narration={dur(narration):.2f}s + {OUTRO_HOLD}s hold -> "
              f"generating ~{glen:.1f}s ...")
        _post(key, PROMPT, int(glen * 1000), RAW)
        # trim to the exact total, short fade in/out only (no atempo stretch —
        # groove tracks read as sped-up/slowed weirdly if retimed; length is
        # already close by construction)
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(RAW), "-af",
             f"afade=t=in:st=0:d=1.0,afade=t=out:st={total-2.0:.2f}:d=2.0",
             "-t", f"{total:.2f}", str(FITTED)], check=True)
        print(f"[done] {FITTED} ready at {dur(FITTED):.2f}s")
        return

    sys.exit("usage: generate_score.py --preview | --full")


if __name__ == "__main__":
    main()
