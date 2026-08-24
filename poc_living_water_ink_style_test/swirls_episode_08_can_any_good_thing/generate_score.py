"""Score for Can Any Good Thing.

SUPERSEDES the first generation (the locked series "1990s dream trance"
identity, reused verbatim from the pilot/episode 2): the user heard the
finished cut and said "I hate the score and its too loud." Root cause of
"too loud" confirmed by measurement, not guesswork -- the trance track's own
solo mean volume (-13.0dB) was actually LOUDER than the narration's own solo
mean volume (-18.6dB) even before any mixing, and the duck settings inherited
from episode 2 (gain_db=-1, threshold=0.7, ratio=1.15) were far too mild to
compensate -- the final mix's mean volume (-13.2dB) barely moved from the
score's own solo level, meaning narration was getting buried.

New direction from a Fable creative pass (2026-08-24, "The Fig Tree" --
Fable's own top pick of 4 proposed directions, chosen specifically because
its arrangement is easy to duck under speech: a lone felt-piano motif with
soft attacks and real silence between phrases, no drums/percussion/bassline
at all, opening into a warm string swell right where the confession lands).
This is a genuine one-episode-only test of a new candidate series identity,
not yet adopted for the whole series -- that's the user's call once they've
heard it.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode_08_can_any_good_thing\\generate_score.py
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
    "Intimate modern-classical felt piano, instrumental, slow and rubato, around 60 bpm. One "
    "quiet, tender felt-piano motif of just a few notes carries the entire piece as its only "
    "voice, played sparsely with long pedal decays and real silence between phrases; no drums, "
    "no percussion, no bassline, nothing rhythmic at all. A soft warm string pad and a faint "
    "breath of tape hiss sit far behind the piano, barely audible, supportive never prominent. "
    "In the final third the strings gently rise and open into a wide, radiant, hopeful swell "
    "while the piano keeps the same simple motif unchanged. Nocturnal, tender, awestruck, the "
    "feeling of being quietly and completely known; a clean, airy, uncluttered mix with "
    "generous space."
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
