"""S_trailer score: layer a bespoke ElevenLabs Music cinematic score under the
ALREADY-FINISHED trailer (SEED_OF_THE_WOMAN_TRAILER.mp4), ducked under its own
existing narration. Reuses sfx_pilots/add_music.py's proven reshape_music()
(Eleven Music v1 crests/dies early -- that fix is nontrivial, don't reimplement)
but does NOT reuse its _mix_and_caption() -- that function adds its own
outro tpad/apad hold, which would extend a trailer that already has its own
correctly-timed title-card hold baked into its 29.667s length. Mix logic here
keeps the trailer's exact existing video/timing untouched, just adds a
sidechain-ducked music bed under the existing audio.

METERED (Eleven Music, ~$1 quoted). Run with --yes to actually spend.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from pipeline.assembly_align import _resolve_key  # noqa: E402
from sfx_pilots.add_music import dur, reshape_music, MUSIC_URL  # noqa: E402

HERE = Path(__file__).resolve().parent
SRC = HERE / "SEED_OF_THE_WOMAN_TRAILER.mp4"
MUSIC = HERE / "trailer_score.mp3"
OUT = HERE / "SEED_OF_THE_WOMAN_TRAILER_scored.mp4"

PROMPT = (
    "Cinematic orchestral film trailer score, sacred and reverent. Opens with "
    "tense hushed strings and a lone cello, mounting dread and grief, low brass "
    "swells and a soft rising string ostinato as tension builds. At the midpoint, "
    "pull back to near silence: a single sustained string note and a solo duduk, "
    "reverent and still. Then a slow dignified rise: warm strings and french horns "
    "building steadily, soft timpani entering, swelling to a full orchestral "
    "redemptive climax with soaring strings and brass in the final seconds, "
    "hopeful and glorious, resolving on a warm major chord. No drums, no choir, "
    "no vocals, instrumental only, cinematic film score mix."
)

GAIN_DB = -13.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--yes", action="store_true")
    ap.add_argument("--regen", action="store_true")
    a = ap.parse_args()

    if not SRC.exists():
        sys.exit(f"missing {SRC}")
    D = dur(SRC)
    print(f"[score] trailer source: {SRC.name} ({D:.3f}s)")

    if a.regen and MUSIC.exists():
        MUSIC.unlink()
    if MUSIC.exists():
        print(f"[score] {MUSIC.name} already exists -- skip generation (--regen to redo)")
    else:
        if not a.yes:
            print(f"\n>>> METERED. --yes to authorize Eleven Music (~{int(D)}s) for the trailer. <<<\n")
            return
        key = _resolve_key()
        if not key:
            sys.exit("no ELEVENLABS_API_KEY (PythonProject1/.env)")
        print(f"[score] composing ~{D:.0f}s cinematic score ...", flush=True)
        r = requests.post(
            MUSIC_URL,
            headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
            json={"prompt": PROMPT, "music_length_ms": int(D * 1000),
                  "force_instrumental": True, "model_id": "music_v1"},
            timeout=300,
        )
        if r.status_code != 200:
            sys.exit(f"[score] FAILED [{r.status_code}]: {r.text[:300]}")
        MUSIC.write_bytes(r.content)
        print(f"[score] ok -> {MUSIC}")
        reshape_music(MUSIC, D)

    # Mix: duck the score under the trailer's OWN existing narration (used as
    # its own sidechain key), keep the trailer's video/timing untouched.
    import subprocess
    fc = (
        f"[0:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,asplit=2[main][key];"
        f"[1:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,atrim=0:{D:.3f},"
        f"afade=t=in:st=0:d=1.5,afade=t=out:st={D - 2.0:.2f}:d=2.0,volume={GAIN_DB}dB[mus];"
        f"[mus][key]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[musd];"
        f"[main][musd]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix]"
    )
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(SRC), "-i", str(MUSIC),
           "-filter_complex", fc, "-map", "0:v", "-map", "[mix]",
           "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-t", f"{D:.3f}", str(OUT)]
    subprocess.run(cmd, check=True)
    print(f"[mix] ok -> {OUT}")


if __name__ == "__main__":
    main()
