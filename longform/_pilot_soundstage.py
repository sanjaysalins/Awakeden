"""Hand-crafted Isaiah 53 pilot soundstage — SMALL taste set (1 bed + 1 one-shot).
Generates 2 ElevenLabs Sound-FX (cached), then ffmpeg-mixes them under the locked
voice track. Re-runs are free once _sfx/ is cached. Metered ONLY on first generation."""
import subprocess
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from pipeline.assembly_align import _resolve_key  # noqa: E402

V1 = ROOT / "longform" / "01_Isaiah_53_Suffering_Servant" / "v1"
SFX = V1 / "_sfx"
SFX.mkdir(exist_ok=True)
SOUND_URL = "https://api.elevenlabs.io/v1/sound-generation"

# (filename, prompt, duration_seconds)
SOUNDS = [
    ("wind.mp3",
     "steady bleak desert wind blowing, present and clearly audible, gusting over open dry land, lonely and desolate, continuous ambience, wind only no music no voices",
     22.0),
    ("nail.mp3",
     "one single distant heavy iron hammer strike on a metal spike, deep, reverberant, solemn, struck once, no repeats, no echo spam",
     3.0),
]


def generate():
    key = _resolve_key()
    if not key:
        sys.exit("ELEVENLABS_API_KEY not found in PythonProject1/.env")
    for fname, prompt, dur in SOUNDS:
        out = SFX / fname
        if out.exists():
            print(f"[skip ] {fname} cached ({out.stat().st_size:,} bytes)")
            continue
        print(f"[gen  ] {fname}  ({dur}s)  '{prompt[:50]}...'", end=" ", flush=True)
        r = requests.post(
            SOUND_URL,
            headers={"xi-api-key": key, "Content-Type": "application/json",
                     "Accept": "audio/mpeg"},
            json={"text": prompt, "duration_seconds": dur, "prompt_influence": 0.4},
            timeout=180,
        )
        if r.status_code != 200:
            sys.exit(f"\nSound-FX failed [{r.status_code}]: {r.text[:300]}")
        out.write_bytes(r.content)
        print(f"ok ({len(r.content):,} bytes)")


def mix_one(out: Path, wind_db: float, nail_db: float):
    voice = V1 / "narration.mp3"
    wind = SFX / "wind.mp3"
    nail = SFX / "nail.mp3"
    # wind: loop to cover 0-42s, fade in 2 / out 3, then duck under the voice.
    # nail: single hit delayed to 115.56s (the word "wounded").
    fc = (
        "[0:a]aformat=sample_rates=44100:channel_layouts=stereo,asplit=2[v][key];"
        "[1:a]aformat=sample_rates=44100:channel_layouts=stereo,"
        f"atrim=0:42,afade=t=in:st=0:d=2,afade=t=out:st=39:d=3,volume={wind_db}dB[wraw];"
        "[wraw][key]sidechaincompress=threshold=0.06:ratio=3:attack=5:release=250[wind];"
        "[2:a]aformat=sample_rates=44100:channel_layouts=stereo,"
        f"adelay=115560|115560,volume={nail_db}dB[nail];"
        "[v][wind][nail]amix=inputs=3:duration=first:normalize=0[m];"
        "[m]alimiter=limit=0.95:level=disabled[out]"
    )
    cmd = [
        "ffmpeg", "-y",
        "-i", str(voice),
        "-stream_loop", "-1", "-i", str(wind),
        "-i", str(nail),
        "-filter_complex", fc,
        "-map", "[out]", "-c:a", "libmp3lame", "-b:a", "192k", "-ar", "44100",
        str(out),
    ]
    print(f"[mix  ] -> {out.name}  (wind {wind_db}dB, nail {nail_db}dB)")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit(f"ffmpeg mix failed:\n{res.stderr[-1500:]}")
    print(f"[done ] {out}")


def mix():
    mix_one(V1 / "narration.immersive_subtle.mp3", wind_db=-6, nail_db=-4)
    mix_one(V1 / "narration.immersive_present.mp3", wind_db=0, nail_db=1)


if __name__ == "__main__":
    generate()
    mix()
