"""A deliberately DIFFERENT score direction for The Ashes That Made Clean,
per the red-team finding: the "1990s dream trance / club comedown" family
(validated for Jacob's Ladder's hopeful dream/vision arc) is a plausible
tonal mismatch against this episode's own content (ceremonial defilement,
ash, death, ritual patience) -- not every episode needs the same "series
sound." This steps outside that whole family rather than picking another
variant within it.

Two-step: a short preview first, then full length once approved.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode_02_ashes_that_made_clean\\generate_score_somber.py --preview
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode_02_ashes_that_made_clean\\generate_score_somber.py --full
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
PREVIEW = HERE / "score_somber_preview.mp3"
RAW = HERE / "score_somber_raw.mp3"
FITTED = HERE / "score_somber.mp3"
OUTRO_HOLD = 3.0
OUTRO_MARGIN = 2.5

PROMPT = (
    "A sparse, contemplative instrumental in a minor key. A single restrained piano or "
    "plucked string figure plays slowly and deliberately, with real space and silence "
    "between phrases — no beat, no percussion, no rhythmic pulse of any kind. A deep, "
    "slow-moving low string or cello tone sits barely present underneath, more felt than "
    "heard. Muted, ashen, solemn atmosphere — the feeling of quiet ritual patience and grief "
    "held without drama, not sadness performed loudly, just stillness. A very occasional "
    "soft, single resonant tone marking the slow passage of time. No build, no climax, no "
    "percussion, no groove, extremely restrained and unhurried throughout. Instrumental only."
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
        sys.exit(f"FAILED [{r.status_code}]: {r.text[:300]}")
    out.write_bytes(r.content)
    print(f"-> {out} ({dur(out):.1f}s)")


def main() -> None:
    key = _resolve_key()
    if not key:
        sys.exit("no ELEVENLABS_API_KEY (PythonProject1/.env)")

    if "--preview" in sys.argv:
        print("[preview] ~25s candidate ...")
        _post(key, PROMPT, 25_000, PREVIEW)
        return

    if "--full" in sys.argv:
        total = dur(NARRATION) + OUTRO_HOLD
        glen = total + OUTRO_MARGIN
        print(f"[full] narration={dur(NARRATION):.2f}s + {OUTRO_HOLD}s hold -> generating ~{glen:.1f}s ...")
        _post(key, PROMPT, int(glen * 1000), RAW)
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(RAW), "-af",
             f"afade=t=in:st=0:d=1.5,afade=t=out:st={total-2.5:.2f}:d=2.5",
             "-t", f"{total:.2f}", str(FITTED)], check=True)
        print(f"[done] {FITTED} ready at {dur(FITTED):.2f}s")
        return

    sys.exit("usage: generate_score_somber.py --preview | --full")


if __name__ == "__main__":
    main()
