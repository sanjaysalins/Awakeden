"""B-fix round 2 — two more 25s previews, each attacking the "two scores"
coherence problem from a different angle than the first fix attempt
(b_fix_single_lead.mp3, in this same folder):

  - SPARSE_SYNTH: drops piano entirely (a synth lead instead), radically
    minimal layering, explicitly asks for a dry mix with no delay/echo.
  - SOLO_PIANO: strips everything down to piano + kick only — nothing else
    for a second melodic idea to compete with, and explicitly bans any
    doubling/chorus effect on the piano itself (in case ElevenLabs was
    applying unison-doubling production polish that read as "two scores").

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_pilot_01_jacobs_ladder\\_score_bakeoff_dream_trance\\generate_b_fix2.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from pipeline.assembly_align import _resolve_key  # noqa: E402

HERE = Path(__file__).resolve().parent

SPARSE_SYNTH = (
    "1990s dream trance, instrumental, 132 bpm. ONE simple analog synth lead melody carries "
    "the piece — no piano, no second melodic layer. Minimal accompaniment: a soft steady "
    "four-on-the-floor kick and one sustained pad chord underneath, nothing else. Extremely "
    "clean and minimal arrangement, spacious but uncluttered. Nostalgic, melancholic, calming. "
    "Dry mix with only a touch of reverb, no delay or echo effects."
)

SOLO_PIANO = (
    "A minimal 1990s dream trance instrumental at 135 bpm built around a single solo piano "
    "melody, played simply and clearly, with no other melodic instrument at all. A soft, "
    "steady four-on-the-floor kick drum only — no bass synth, no pads, no strings, no "
    "additional layers. The piano carries the entire emotional and melodic content alone. "
    "Nostalgic, melancholic, calming. A completely dry, close recording of the piano — no "
    "delay, no chorus, no unison-doubling effect of any kind."
)

CANDIDATES = {
    "b_fix2_sparse_synth": SPARSE_SYNTH,
    "b_fix2_solo_piano": SOLO_PIANO,
}


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
    for slug, prompt in CANDIDATES.items():
        out = HERE / f"{slug}.mp3"
        if out.exists():
            print(f"[skip] {out.name}")
            continue
        print(f"[{slug}] generating ~25s ...")
        r = requests.post(
            "https://api.elevenlabs.io/v1/music",
            headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
            json={"prompt": prompt, "music_length_ms": 25_000,
                  "force_instrumental": True, "model_id": "music_v1"},
            timeout=300,
        )
        if r.status_code != 200:
            print(f"  FAILED [{r.status_code}]: {r.text[:300]}")
            continue
        out.write_bytes(r.content)
        print(f"  -> {out.name} ({dur(out):.1f}s)")


if __name__ == "__main__":
    main()
