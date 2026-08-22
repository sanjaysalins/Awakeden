"""B-fix attempt — the user reports hearing "two scores together" even in
the raw, unmixed score_B_full.mp3 (confirmed: not a mixing artifact, the
duck/level changes didn't touch it). Audio diagnostic (autocorrelation, L/R
correlation) found no smoking-gun technical defect (no near-1.0 duplicate-
audio correlation, no phase-cancellation red flag) — the likely cause is a
coherence problem in the generation itself: two competing melodic/lead
ideas (piano + a synth/pad line) that don't read as one unified track.

This prompt explicitly asks for a single lead voice and a clean, uncluttered
mix, targeting that failure mode directly. Short 25s preview first, per the
same test-before-committing pattern used earlier in this session.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_pilot_01_jacobs_ladder\\_score_bakeoff_dream_trance\\generate_b_fix.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from pipeline.assembly_align import _resolve_key  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "b_fix_single_lead.mp3"

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
    print("[preview] generating ~25s single-lead-voice candidate ...")
    r = requests.post(
        "https://api.elevenlabs.io/v1/music",
        headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
        json={"prompt": PROMPT, "music_length_ms": 25_000,
              "force_instrumental": True, "model_id": "music_v1"},
        timeout=300,
    )
    if r.status_code != 200:
        sys.exit(f"FAILED [{r.status_code}]: {r.text[:300]}")
    OUT.write_bytes(r.content)
    print(f"-> {OUT} ({dur(OUT):.1f}s)")


if __name__ == "__main__":
    main()
