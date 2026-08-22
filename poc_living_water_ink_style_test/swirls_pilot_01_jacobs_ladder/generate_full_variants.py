"""Full-episode-length score candidates for the Jacob's Ladder pilot.

CANDIDATE_B is the bake-off's B track (user's own revised prompt) — the
user's explicit pick ("do B for the whole of the Jacob's Ladder short").
COMBO_E and COMBO_F are new blends drawn from the bake-off's B/C/D
descriptors (user: "C is also good and D is also good... try various
combination for the whole episode") — genuinely new prompts, not a rename
of any single bake-off track, composed to test whether a blend beats B
alone for this specific piece.

Each is generated at the cut's own length (narration + 3.0s landing hold,
same INV-26 target `mix_score.py` mixes to), fitted with a short fade in/out
— same pattern as `generate_score.py` / `_score_bakeoff_dream_trance/
generate_bakeoff.py`.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_pilot_01_jacobs_ladder\\generate_full_variants.py
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
OUTRO_HOLD = 3.0
OUTRO_MARGIN = 2.5

# = bake-off candidate B verbatim (user's revised prompt, explicitly picked).
CANDIDATE_B = (
    "1990s dream trance, ethereal acoustic piano lead, melancholic but uplifting melody, "
    "driving 4/4 house beat, sweeping ambient synth pads, deep hypnotic bassline, soothing "
    "electronic, instrumental, nostalgic club comedown, atmospheric, 135 bpm"
)

# New blend: B's driving beat/bassline + C's acoustic-guitar texture and gentler build +
# D's breakdown-built arrangement.
COMBO_E = (
    "A 1990s instrumental dream house / dream trance track, around 136 BPM. An ethereal "
    "acoustic piano lead carries a melancholic but uplifting melody throughout. A driving "
    "four-on-the-floor kick and deep hypnotic bassline underpin the groove, warm and steady "
    "rather than aggressive. Sweeping ambient synth pads and soft strings fill the space with "
    "long reverb tails, and subtle acoustic guitar textures thread through quietly underneath. "
    "The arrangement breathes: it builds, then withdraws into a near-silent breakdown of just "
    "piano and pad, before returning to the full groove. Instrumental, nostalgic, hypnotic, "
    "and calming — a genuine 90s club comedown record."
)

# New blend: leans toward C/D's restraint — sparser, kick mixed further back, more
# contemplative than B or E.
COMBO_F = (
    "A restrained 1990s dream trance instrumental at 135 BPM. A simple, looping, wistful "
    "piano motif in a minor key is the emotional center. A soft four-on-the-floor kick and "
    "gentle offbeat hats stay mixed well back, felt more than heard. Warm synth bass moves "
    "slowly underneath. Ethereal pads and soft strings stretch out with heavy reverb and "
    "delay, spacious and dreamlike. The track favors quiet over intensity — no big drop, just "
    "a slow emotional swell and release. Melancholic, hypnotic, nostalgic, gently uplifting, "
    "instrumental, cinematic."
)

VARIANTS = {
    "score_B_full": CANDIDATE_B,
    "score_comboE_full": COMBO_E,
    "score_comboF_full": COMBO_F,
}


def dur(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def generate(key: str, slug: str, prompt: str, total: float) -> None:
    import requests
    raw = HERE / f"{slug}_raw.mp3"
    fitted = HERE / f"{slug}.mp3"
    if fitted.exists():
        print(f"[skip] {fitted.name} already exists")
        return
    glen = total + OUTRO_MARGIN
    print(f"[{slug}] generating ~{glen:.1f}s ...")
    r = requests.post(
        "https://api.elevenlabs.io/v1/music",
        headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
        json={"prompt": prompt, "music_length_ms": int(glen * 1000),
              "force_instrumental": True, "model_id": "music_v1"},
        timeout=300,
    )
    if r.status_code != 200:
        print(f"  FAILED [{r.status_code}]: {r.text[:300]}")
        return
    raw.write_bytes(r.content)
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-af",
         f"afade=t=in:st=0:d=1.0,afade=t=out:st={total-2.0:.2f}:d=2.0",
         "-t", f"{total:.2f}", str(fitted)], check=True)
    print(f"  -> {fitted.name} ({dur(fitted):.1f}s)")


def main() -> None:
    key = _resolve_key()
    if not key:
        sys.exit("no ELEVENLABS_API_KEY (PythonProject1/.env)")
    total = dur(NARRATION) + OUTRO_HOLD
    print(f"[plan] narration={dur(NARRATION):.2f}s + {OUTRO_HOLD}s hold -> target {total:.2f}s")
    for slug, prompt in VARIANTS.items():
        generate(key, slug, prompt, total)


if __name__ == "__main__":
    main()
