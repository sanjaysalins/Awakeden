"""Look and Live -- score-swap POC: ONE continuous Eleven Music "Robert Miles
Children build-up" bed replacing the current two-bed Suno crossfade (musA/musB
in ../_s5_score_sfx.py), while keeping the same ambient SFX layers (wind/
crowd/rumble/dawn) and narration sidechain-ducking untouched.

Prompt reused verbatim from the panel-synthesized version at
../../son_of_man_lifted_up/_score_swap_poc/_PANEL_PROMPTS.md -- it's generic
musical language with no episode-specific references, so it transfers
cleanly to this episode too. Retargeted here (2026-08-16, this session) from
son_of_man_lifted_up (58.0s) to Look and Live (61.9s) per the user's request.

Deliberately does NOT apply add_music.py's reshape_music() ease-down arc (it
crests at 70% then fades to a floor by the end) -- this POC wants the
OPPOSITE: a continuous rising build-up register the WHOLE way. Only
trims/stretches to fill the full length if Eleven's raw generation dies
early (a known issue), with a short 2.5s anti-click edge-fade at the very
tail -- that's audio-engineering courtesy, not the musical "resolution" the
brief explicitly avoids.

Produces a CANDIDATE file beside (not overwriting) the already-finished/
watermarked real final -- listen and compare before promoting.

  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_score_swap_poc/_generate_and_mix.py --yes
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from pipeline.score_mix import AFMT, SIDECHAIN  # noqa: E402
from pipeline.assembly_align import _resolve_key  # noqa: E402

HERE = Path(__file__).resolve().parent
EP = HERE.parent
SND = ROOT / "sound_library" / "clips"

SRC = EP / "LOOKANDLIVE_living_sketchbook_cc.mp4"     # pre-score, captioned
RAW = HERE / "miles_build_raw.mp3"
MUSIC = HERE / "miles_build.mp3"
OUT = HERE / "LOOKANDLIVE_MILESPOC_cc_scored_sfx.mp4"

TOTAL = 61.900          # matches ../_s5_score_sfx.py exactly (INV-26 hold baked into SRC)
OUTRO_MARGIN = 2.5       # generate a touch longer than TOTAL so trimming avoids Eleven's early-death tail

# Original panel-synthesized prompt named "Robert Miles' Children" directly --
# ElevenLabs' Music API rejected it as a ToS violation (named-artist/song
# reference, confirmed 2026-08-16: 400 "bad_prompt"). Re-worded to keep every
# musical descriptor the panel converged on (arpeggiated piano, warm pads,
# cello drone, pipe-organ swell, continuously intensifying, never resolving)
# while dropping the artist/song name -- the descriptors alone already carry
# the "Children"-style build-up brief.
PROMPT = (
    "Sacred ambient dream-trance instrumental, reverent and awe-filled, never clubby: a slow "
    "arpeggiated piano cycling over warm analog pads, joined by a soft cello drone and a "
    "distant pipe-organ swell. The arrangement begins hushed and continuously intensifies in "
    "harmonic density and lift for the full length, in the style of a classic 1990s dream-"
    "trance anthem's opening build -- the slow arpeggiated climb right before a beat would "
    "have dropped, but sacred, not euphoric. No drums, no beat, no drop, no vocals: one "
    "unbroken ascent that never resolves into a pulse."
)


def dur(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def _mean_db(path: Path, ss: float, d: float):
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-ss", str(ss), "-t", str(d), "-i", str(path),
         "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    m = re.search(r"mean_volume:\s*(-?[0-9.]+) dB", out)
    return float(m.group(1)) if m else None


def generate(key: str) -> None:
    import requests
    glen = TOTAL + OUTRO_MARGIN
    print(f"[music] composing ~{glen:.1f}s Robert-Miles-build-up score ...", flush=True)
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


def fit_to_total() -> None:
    """Trim/stretch the raw gen to fill TOTAL exactly -- NO ease-down arc (deliberate,
    see module docstring). Detects Eleven's known early-death tail the same way
    add_music.py's reshape_music() does, then atempo-stretches to fill, then a short
    2.5s anti-click edge-fade at the very end only."""
    draw = dur(RAW)
    aud_end, t = draw, max(4.0, draw - 2.0)
    while t > draw * 0.55:
        m = _mean_db(RAW, t, 2.0)
        if m is not None and m > -30.0:
            aud_end = min(draw, t + 2.0)
            break
        t -= 2.0
    aud_end = max(aud_end, draw * 0.6)
    target = TOTAL + OUTRO_MARGIN
    tempo = max(0.5, min(1.0, aud_end / target))
    af = (f"atrim=0:{aud_end:.2f},asetpts=PTS-STARTPTS,atempo={tempo:.4f},"
          f"afade=t=in:st=0:d=2,afade=t=out:st={target-2.5:.2f}:d=2.5")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(RAW), "-af", af,
         "-t", f"{target:.2f}", str(MUSIC)], check=True)
    print(f"[fit] audible 0-{aud_end:.1f}s of {draw:.1f}s raw -> stretched to fill "
          f"{target:.1f}s (atempo {tempo:.4f}), no ease-down (per POC brief)")


def mix() -> None:
    if not SRC.exists():
        sys.exit(f"missing: {SRC}")
    filt = (
        f"[1:a]{AFMT},atrim=0:{TOTAL},volume=-8dB[mus];"
        f"[2:a]{AFMT},atrim=0:{TOTAL},afade=t=in:st=0:d=2,volume=-20dB[wind];"
        f"[3:a]{AFMT},atrim=0:3.859,"
        f"afade=t=in:st=0:d=0.5,afade=t=out:st=3.059:d=0.8,volume=-15dB[crowd1];"
        f"[4:a]{AFMT},atrim=0:5.221,adelay=26237|26237,"
        f"afade=t=in:st=26.237:d=0.8,afade=t=out:st=30.658:d=0.8,volume=-15dB[crowd2];"
        f"[5:a]{AFMT},atrim=0:4.645,adelay=7692|7692,"
        f"afade=t=in:st=7.692:d=1.0,afade=t=out:st=11.437:d=0.9,volume=-17dB[rumble];"
        f"[6:a]{AFMT},atrim=0:7.072,adelay=31458|31458,"
        f"afade=t=in:st=31.458:d=1.5,afade=t=out:st=37.53:d=1.0,volume=-18dB[dawn];"
        f"[mus][wind][crowd1][crowd2][rumble][dawn]amix=inputs=6:normalize=0[bed];"
        f"[0:a]{AFMT},apad=whole_dur={TOTAL},asplit=2[main][key];"
        f"[bed][key]sidechaincompress={SIDECHAIN}[bedd];"
        f"[main][bedd]amix=inputs=2:normalize=0,"
        f"alimiter=limit=0.85:level=disabled,aresample=44100[mix]"
    )
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error",
         "-i", str(SRC),
         "-i", str(MUSIC),
         "-stream_loop", "-1", "-i", str(SND / "wind_desert_bleak.mp3"),
         "-i", str(SND / "crowd_murmur_distant.mp3"),
         "-i", str(SND / "crowd_murmur_distant.mp3"),
         "-i", str(SND / "rumble_deep_sub.mp3"),
         "-i", str(SND / "dawn_morning_warm.mp3"),
         "-filter_complex", filt,
         "-map", "0:v", "-map", "[mix]", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "192k", "-t", f"{TOTAL}",
         "-movflags", "+faststart",
         str(OUT)],
        check=True,
    )
    print(f"[ok] {OUT}")


def main() -> None:
    if "--yes" not in sys.argv:
        sys.exit(">>> METERED (~$1, Eleven Music). Re-run with --yes to authorize. <<<")
    if RAW.exists():
        print(f"[music] raw already exists, skip generation -> {RAW}")
    else:
        key = _resolve_key()
        if not key:
            sys.exit("no ELEVENLABS_API_KEY (PythonProject1/.env)")
        generate(key)
    fit_to_total()
    mix()


if __name__ == "__main__":
    main()
