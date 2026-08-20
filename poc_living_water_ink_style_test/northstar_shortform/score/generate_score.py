"""North-star pattern-lock POC — fresh score, fit to the narration's own length.

Fresh direction (user's explicit call, 2026-08-19): NOT the Look-and-Live /
Robert-Miles trance-build direction — a distinct, intimate, water-themed arc
built for THIS piece's own emotional shape (wary -> warming -> vulnerable ->
one real hushed arrival at the revelation -> joyful lift -> settled, at rest).

No named artist/song anywhere (ElevenLabs Music ToS hard-blocks that).

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test/northstar_shortform/score/generate_score.py --yes
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from pipeline import cost  # noqa: E402

HERE = Path(__file__).resolve().parent
NARRATION_MP3 = Path(
    r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
    r"\SwirlsOfLife_JohnFour_POC\v1\narration.mp3"
)
OUTRO_HOLD = 3.0  # INV-26 landing-hold floor
OUTRO_MARGIN = 2.5  # generate a touch longer than needed, trim in fit_to_total

RAW = HERE / "score_raw.mp3"
FITTED = HERE / "score.mp3"

PROMPT = (
    "A gentle, intimate instrumental built around the recurring image of running "
    "water. Opens spare and wary: a lone, softly plucked classical guitar or harp "
    "figure over a very low sustained string drone, hesitant, in a minor key -- two "
    "strangers meeting. A simple flowing arpeggiated pattern, like water welling up, "
    "enters quietly underneath as trust slowly builds, its repeating shape widening a "
    "little each time; a warm string pad joins, then a low cello. About two-thirds of "
    "the way through, the texture opens into one genuine moment of hushed clarity: "
    "the arpeggio thins to almost nothing, a single sustained warm chord holds, still "
    "and suspended -- a real arrival, not a held-back build. From there the piece "
    "brightens and lifts: a light, quicker plucked-string pulse and soft mallet "
    "percussion carry a feeling of joyful motion and running, the harmony warming "
    "toward major, more voices joining as if a whole community is arriving. It ends "
    "open, warm, and at rest -- settled, not unresolved. No drums, no bassline, no "
    "electronic pulse, no vocals, no choir -- devotional, intimate, water-like in "
    "character throughout."
)


def dur(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def _mean_db(path: Path, ss: float, d: float) -> float | None:
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-ss", str(ss), "-t", str(d), "-i", str(path),
         "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    m = re.search(r"mean_volume:\s*(-?[0-9.]+) dB", out)
    return float(m.group(1)) if m else None


def generate(key: str, total: float) -> None:
    import requests
    glen = total + OUTRO_MARGIN
    print(f"[music] composing ~{glen:.1f}s score ...", flush=True)
    r = requests.post(
        "https://api.elevenlabs.io/v1/music",
        headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
        json={"prompt": PROMPT, "music_length_ms": int(glen * 1000),
              "force_instrumental": True, "model_id": "music_v1"},
        timeout=300,
    )
    if r.status_code != 200:
        sys.exit(f"[music] FAILED [{r.status_code}]: {r.text[:300]}")
    RAW.write_bytes(r.content)
    print(f"[music] ok -> {RAW} ({dur(RAW):.1f}s raw)")
    cost.record("SwirlsOfLife_JohnFour_POC", "short", "score", "elevenlabs-music", "eleven_music_v1",
                units=1, est_usd="~1", mode="metered",
                note=f"fresh water-theme score, {dur(RAW):.1f}s raw -> score.mp3")


def fit_to_total(total: float) -> None:
    """Trim to fill TOTAL, with a genuine arrival + lift arc — no forced ease-down,
    the prompt's own shape carries the arc. Fades only at the very edges."""
    draw = dur(RAW)
    aud_end, t = draw, max(4.0, draw - 2.0)
    while t > draw * 0.55:
        m = _mean_db(RAW, t, 2.0)
        if m is not None and m > -30.0:
            aud_end = min(draw, t + 2.0)
            break
        t -= 2.0
    aud_end = max(aud_end, draw * 0.6)
    tempo = max(0.5, min(1.0, aud_end / total))
    af = (f"atrim=0:{aud_end:.2f},asetpts=PTS-STARTPTS,atempo={tempo:.4f},"
          f"afade=t=in:st=0:d=1.5,afade=t=out:st={total-2.5:.2f}:d=2.5")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(RAW), "-af", af,
         "-t", f"{total:.2f}", str(FITTED)], check=True)
    print(f"[fit] audible 0-{aud_end:.1f}s of {draw:.1f}s raw -> stretched to fill "
          f"{total:.1f}s (atempo {tempo:.4f})")


def main() -> None:
    if "--yes" not in sys.argv:
        sys.exit(">>> METERED (~$1, ElevenLabs Music). Re-run with --yes to authorize. <<<")
    if not NARRATION_MP3.exists():
        sys.exit(f"missing: {NARRATION_MP3}")
    total = dur(NARRATION_MP3) + OUTRO_HOLD
    print(f"[plan] narration={dur(NARRATION_MP3):.2f}s + {OUTRO_HOLD}s hold -> score target {total:.2f}s")

    from pipeline.assembly_align import _resolve_key  # noqa: E402
    key = _resolve_key()
    if not key:
        sys.exit("no ELEVENLABS_API_KEY (PythonProject1/.env)")

    if RAW.exists():
        print(f"[music] raw already exists, skip generation -> {RAW}")
    else:
        generate(key, total)
    fit_to_total(total)
    print(f"\n[done] {FITTED} ready at {dur(FITTED):.2f}s")


if __name__ == "__main__":
    main()
