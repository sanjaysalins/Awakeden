"""The Serpent-Crusher Promised -- step 5: SCORE + AMBIENT SFX BED, mixed
onto the already-captioned SERPENTCRUSHERPROMISED_living_sketchbook_cc.mp4.
Same combined single-pass recipe as the sibling shorts' own _s5_score_sfx.py
scripts -- new segments/cues/timings for THIS narration's own register.

Music arc: lonely_searching_a dominant through the exposition, the KJV
quote's own weight, AND the conviction ("you want to be the one who
crushes...") -- crossfading into sacred_grace_rise_a EXACTLY at the word
"Christ," in "it's Christ, finishing what He won" (53.482s per
_alignment.json). This is the piece's real gospel pivot -- the moment the
doctrinal tension it raised ("why still future?") resolves into present-
tense fulfillment, immediately before the landing.

2026-08-15: re-timed for the re-synthesized narration.mp3 (scripture voice
added for the KJV quote shifted every downstream timestamp; pivot word was
51.776s, now 53.482s).

Ambient SFX bed (sound_library/clips, $0, ambience-only):
  fire_crackling      s01 window (0-5.740s) -- the oil lamp the three
                      generations are gathered around.
  rumble_deep_sub      s05 HERO window (20.139-30.459s) -- gravity under
                      the KJV pronouncement itself.
  wind_desert_bleak   s07 window (39.305-49.767s) -- the night watchman's
                      lonely vigil.
  heavenly_choir_soft s09 window (55.952-62.0s) -- a reverent touch under
                      the landing.

  .venv\\Scripts\\python.exe poc_living_sketchbook/serpent_crusher_promised/_s5_score_sfx.py
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

SRC = HERE / "SERPENTCRUSHERPROMISED_living_sketchbook_cc.mp4"
OUT = HERE / "SERPENTCRUSHERPROMISED_living_sketchbook_cc_scored_sfx.mp4"
TOTAL = 62.0  # matches _s3_assemble.py's TOTAL exactly -- INV-26 hold already in SRC


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"missing captioned cut: {SRC} -- run _s4_captions.py first")

    filt = (
        f"[1:a]{AFMT},atrim=0:54,afade=t=in:st=0:d=1.5,"
        f"afade=t=out:st=47.5:d=6.0,volume=-9dB[musA];"
        f"[2:a]{AFMT},adelay=53482|53482,atrim=0:{TOTAL},"
        f"afade=t=in:st=53.482:d=6.0,afade=t=out:st={TOTAL}:d=4.0,volume=-8dB[musB];"
        f"[3:a]{AFMT},atrim=0:5.9,"
        f"afade=t=in:st=0:d=1.0,afade=t=out:st=4.1:d=1.5,volume=-20dB[fire];"
        f"[4:a]{AFMT},atrim=0:10.5,adelay=20139|20139,"
        f"afade=t=in:st=20.139:d=1.0,afade=t=out:st=29.5:d=1.5,volume=-18dB[rumble];"
        f"[5:a]{AFMT},atrim=0:10.7,adelay=39305|39305,"
        f"afade=t=in:st=39.305:d=1.2,afade=t=out:st=48.8:d=1.5,volume=-18dB[wind];"
        f"[6:a]{AFMT},atrim=0:6.3,adelay=55952|55952,"
        f"afade=t=in:st=55.952:d=1.5,afade=t=out:st={TOTAL}:d=2.0,volume=-16dB[choir];"
        f"[musA][musB][fire][rumble][wind][choir]amix=inputs=6:normalize=0[bed];"
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
         "-i", str(SND / "fire_crackling.mp3"),
         "-i", str(SND / "rumble_deep_sub.mp3"),
         "-i", str(SND / "wind_desert_bleak.mp3"),
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
