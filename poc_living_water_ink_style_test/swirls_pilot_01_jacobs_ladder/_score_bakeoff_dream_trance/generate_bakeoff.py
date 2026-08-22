"""Dream-trance score bake-off — 4 candidate prompts, generated via ElevenLabs
Music, for the user to compare by ear before picking a direction.

One prompt needed adaptation from what the user gave verbatim (flagged to
the user, not silently changed): CANDIDATE_C named "Robert Miles 'Children'"
-- ElevenLabs Music's ToS hard-blocks named artist/song references (see
generate_score.py and eleven_music.py's module docstrings elsewhere in this
repo). Stripped ONLY that clause; every stylistic descriptor around it is
kept verbatim.

CANDIDATE_B was originally an image/video prompt (camera framing, a
"Negative Prompt:" block) -- flagged to the user as a likely mismatch, who
confirmed and replaced it with a proper audio-style prompt (below).

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_pilot_01_jacobs_ladder\\_score_bakeoff_dream_trance\\generate_bakeoff.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from pipeline.assembly_align import _resolve_key  # noqa: E402

HERE = Path(__file__).resolve().parent
LENGTH_MS = 40_000  # 40s per candidate -- long enough to hear a build/breakdown

CANDIDATE_A = (
    "137 BPM 90s dream trance: four-on-the-floor groove, hypnotic melancholic piano motif, "
    "warm synth bass, ethereal pads and strings, spacious reverb, gradual progressive "
    "arrangement, nostalgic and euphoric but calming, instrumental and cinematic."
)

CANDIDATE_B = (
    "1990s dream trance, ethereal acoustic piano lead, melancholic but uplifting melody, "
    "driving 4/4 house beat, sweeping ambient synth pads, deep hypnotic bassline, soothing "
    "electronic, instrumental, nostalgic club comedown, atmospheric, 135 bpm"
)

# "in the vein of Robert Miles 'Children'" removed (named-artist ToS block); rest verbatim.
CANDIDATE_C = (
    "Pioneering dream trance / dream house style: simple looping emotional piano melody in "
    "minor key, lush atmospheric synth pads and soft strings, steady but restrained "
    "four-on-the-floor kick, heavy reverb and delay creating a spacious dreamy soundscape, "
    "subtle acoustic guitar elements, mid-tempo around 138 BPM, instrumental, melancholic yet "
    "gently uplifting, nostalgic and hypnotic atmosphere, organic electronic fusion"
)

CANDIDATE_D = (
    "A mid-90s instrumental dream-house track at 137 BPM. A wistful minor-key piano melody "
    "carries the entire hook — no vocals, no acid line, nothing to replace it. Underneath, a "
    "soft four-on-the-floor kick and gentle offbeat hats, mixed back rather than forward. Wide "
    "ambient pads and string-like synth washes with long reverb tails fill the space. The "
    "arrangement is built around its breakdowns rather than its drops: it builds, then "
    "withdraws into near-silence with just piano and pad, then returns. Emotionally "
    "bittersweet and calming despite the tempo — a come-down record you can still dance to. No "
    "aggression, no hoover stabs, no rave riffs."
)

CANDIDATES = {
    "a_dream_trance": CANDIDATE_A,
    "b_dream_trance_v2": CANDIDATE_B,
    "c_dream_house_sanitized": CANDIDATE_C,
    "d_90s_dreamhouse_breakdown": CANDIDATE_D,
}


def dur(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def generate(key: str, slug: str, prompt: str) -> None:
    import requests
    out = HERE / f"{slug}.mp3"
    if out.exists():
        print(f"[skip] {out.name} already exists")
        return
    print(f"[{slug}] generating ...")
    r = requests.post(
        "https://api.elevenlabs.io/v1/music",
        headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
        json={"prompt": prompt, "music_length_ms": LENGTH_MS,
              "force_instrumental": True, "model_id": "music_v1"},
        timeout=300,
    )
    if r.status_code != 200:
        print(f"  FAILED [{r.status_code}]: {r.text[:300]}")
        return
    out.write_bytes(r.content)
    print(f"  -> {out.name} ({dur(out):.1f}s, {out.stat().st_size:,} bytes)")


def main() -> None:
    key = _resolve_key()
    if not key:
        sys.exit("no ELEVENLABS_API_KEY (PythonProject1/.env)")
    for slug, prompt in CANDIDATES.items():
        generate(key, slug, prompt)


if __name__ == "__main__":
    main()
