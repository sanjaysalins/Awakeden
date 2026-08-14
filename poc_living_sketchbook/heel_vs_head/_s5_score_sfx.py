"""Heel vs Head -- step 5: SCORE + AMBIENT SFX BED, mixed onto the
already-captioned HEELVSHEAD_living_sketchbook_cc.mp4. Same combined
single-pass recipe as the sibling shorts' own _s5_score_sfx.py scripts --
new segments/cues/timings for THIS narration's own register.

Music arc: lonely_searching_a dominant through the exposition AND the
personal address (0-50.8s: "you've heard it as a tie... you keep trying
to land your own blow") -- crossfading into sacred_grace_rise_a EXACTLY
at the word "Christ" in "Christ already delivered the blow that ends
it" (50.819s per _alignment.json). This is the piece's real gospel
pivot -- NOT the earlier KJV quote (s04), which is God's pronouncement
of the terms, not yet the resolution.

Ambient SFX bed (music_library+sound_library/clips, $0, ambience-only):
  wind_desert_bleak   s01 window (0-3.79s) -- quiet atmosphere under the
                      opening standoff.
  rumble_deep_sub     s04 window (23.21-34.78s) -- gravity under God's
                      own pronouncement.
  heavenly_choir_soft s07 window (53.52-65.0s) -- a reverent touch under
                      the landing.

  .venv\\Scripts\\python.exe poc_living_sketchbook/heel_vs_head/_s5_score_sfx.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline.score_mix import AFMT, SIDECHAIN  # noqa: E402 -- reuse, don't duplicate

HERE = Path(__file__).resolve().parent
MUS = ROOT / "music_library" / "clips"
SND = ROOT / "sound_library" / "clips"

SRC = HERE / "HEELVSHEAD_living_sketchbook_cc.mp4"
OUT = HERE / "HEELVSHEAD_living_sketchbook_cc_scored_sfx.mp4"
TOTAL = 65.0  # matches _s3_assemble.py's TOTAL exactly -- INV-26 hold already in SRC


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"missing captioned cut: {SRC} -- run _s4_captions.py first")

    filt = (
        f"[1:a]{AFMT},atrim=0:57,afade=t=in:st=0:d=1.5,"
        f"afade=t=out:st=44.8:d=6.0,volume=-9dB[musA];"
        f"[2:a]{AFMT},adelay=50800|50800,atrim=0:{TOTAL},"
        f"afade=t=in:st=50.8:d=6.0,afade=t=out:st=61.0:d=4.0,volume=-8dB[musB];"
        f"[3:a]{AFMT},atrim=0:4.5,"
        f"afade=t=in:st=0:d=1.0,afade=t=out:st=3.0:d=1.5,volume=-20dB[wind];"
        f"[4:a]{AFMT},atrim=0:12.5,adelay=23210|23210,"
        f"afade=t=in:st=23.21:d=1.2,afade=t=out:st=33.5:d=1.5,volume=-18dB[rumble];"
        f"[5:a]{AFMT},atrim=0:12.0,adelay=53520|53520,"
        f"afade=t=in:st=53.52:d=1.5,afade=t=out:st=63.0:d=2.0,volume=-16dB[choir];"
        f"[musA][musB][wind][rumble][choir]amix=inputs=5:normalize=0[bed];"
        f"[0:a]{AFMT},apad=whole_dur={TOTAL},asplit=2[main][key];"
        f"[bed][key]sidechaincompress={SIDECHAIN}[bedd];"
        f"[main][bedd]amix=inputs=2:normalize=0,"
        f"alimiter=limit=0.85:level=disabled,aresample=44100[mix]"
    )

    subprocess.run(
        ["ffmpeg", "-y", "-v", "error",
         "-i", str(SRC),
         "-i", str(MUS / "lonely_searching_a.mp3"),
         "-i", str(MUS / "sacred_grace_rise_a.mp3"),
         "-i", str(SND / "wind_desert_bleak.mp3"),
         "-i", str(SND / "rumble_deep_sub.mp3"),
         "-i", str(SND / "heavenly_choir_soft.mp3"),
         "-filter_complex", filt,
         "-map", "0:v", "-map", "[mix]", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "192k", "-t", f"{TOTAL}",
         "-movflags", "+faststart",
         str(OUT)],
        check=True,
    )
    print(f"[ok] {OUT}")


if __name__ == "__main__":
    main()
