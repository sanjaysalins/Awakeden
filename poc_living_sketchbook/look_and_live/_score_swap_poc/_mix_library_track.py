"""Look and Live -- score-swap POC, take 2: use the user's OWN supplied track
(music/Cathedral Loop.mp3) instead of an Eleven Music generation. $0 -- no
API call, no spend.

Section chosen by mechanical volume-envelope scan (mean_volume sampled every
8s across all 5 tracks in music/): Cathedral Loop.mp3's 0:00-61.9s is a
clean, sustained rise (-27dB hushed open -> holds -14/-15dB with -3/-4dB
peaks by 56-64s) with NO dip or resolution anywhere in that window -- almost
exactly Look and Live's 61.9s target length, so no loop/stretch needed, just
a trim + the same edge fades as the Eleven POC candidate (2s fade-in, 2.5s
anti-click fade-out -- NOT a musical resolution, matches this project's own
edge-fade convention elsewhere).

Reuses the exact same SFX-layer + sidechain-duck filter graph as
_generate_and_mix.py's mix() (wind/crowd/rumble/dawn cues, narration duck) --
only the music source changed. Produces a SEPARATE candidate file so both
POC takes can be compared side by side; does not touch the real final.

  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_score_swap_poc/_mix_library_track.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from pipeline.score_mix import AFMT, SIDECHAIN  # noqa: E402

HERE = Path(__file__).resolve().parent
EP = HERE.parent
SND = ROOT / "sound_library" / "clips"
MUS_SRC = ROOT / "music" / "Cathedral Loop.mp3"

SRC = EP / "LOOKANDLIVE_living_sketchbook_cc.mp4"     # pre-score, captioned
MUSIC = HERE / "cathedral_loop_build.mp3"
OUT = HERE / "LOOKANDLIVE_CATHEDRALPOC_cc_scored_sfx.mp4"

TOTAL = 61.900  # matches ../_s5_score_sfx.py exactly (INV-26 hold baked into SRC)


def extract_build() -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(MUS_SRC),
         "-af", f"afade=t=in:st=0:d=2,afade=t=out:st={TOTAL-2.5:.2f}:d=2.5",
         "-t", f"{TOTAL:.3f}", str(MUSIC)], check=True)
    print(f"[extract] {MUS_SRC.name} 0:00-{TOTAL:.1f}s -> {MUSIC}")


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
    if not MUS_SRC.exists():
        sys.exit(f"missing source track: {MUS_SRC}")
    extract_build()
    mix()


if __name__ == "__main__":
    main()
