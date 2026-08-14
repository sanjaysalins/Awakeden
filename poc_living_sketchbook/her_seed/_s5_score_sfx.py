"""Her Seed -- step 5: SCORE + AMBIENT SFX BED, mixed onto the already-
captioned HERSEED_living_sketchbook_cc.mp4. Same combined single-pass
recipe as the sibling shorts' own _s5_score_sfx.py scripts -- new
segments/cues/timings for THIS narration's own register.

Music arc: neutral_teaching_warm_a dominant through the "unpacking a
detail" section (0-35.061s: the Plan-B subversion, Genesis's own promise,
Paul's phrase, the expected genealogy pattern) -- crossfading into
sacred_grace_rise_a EXACTLY at s06's own window start (35.061s), the
piece's real thesis turn ("Here, he doesn't. He writes: made of a woman,
the woman promised in the garden") -- not the earlier KJV-quote moment
(s04), since THIS piece's payoff is the garden-to-gospel connection, not
the quote itself.

Ambient SFX bed (music_library+sound_library/clips, $0, ambience-only):
  dawn_morning_warm   s02 window (8.087-12.896s) -- light arriving on Eve,
                      reinforces the promise-spoken warmth.
  heavenly_choir_soft s04 window (19.328-29.274s) -- a reverent touch under
                      Scripture's own words arriving (Galatians 4:4).
  wind_desert_bleak   s06 window (35.061-41.043s) -- very quiet, the
                      outdoor cross scene.

Timings recomputed 2026-08-14 -- adding a dedicated "scripture" voice for
Paul's KJV quote (s04) shifted word timing throughout the back half of
the piece; all cue points here re-derived from the new _alignment.json.

  .venv\\Scripts\\python.exe poc_living_sketchbook/her_seed/_s5_score_sfx.py
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

SRC = HERE / "HERSEED_living_sketchbook_cc.mp4"
OUT = HERE / "HERSEED_living_sketchbook_cc_scored_sfx.mp4"
TOTAL = 62.0  # matches _s3_assemble.py's TOTAL exactly -- INV-26 hold already in SRC


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"missing captioned cut: {SRC} -- run _s4_captions.py first")

    filt = (
        f"[1:a]{AFMT},atrim=0:42,afade=t=in:st=0:d=1.5,"
        f"afade=t=out:st=29.061:d=6.0,volume=-9dB[musA];"
        f"[2:a]{AFMT},adelay=35061|35061,atrim=0:{TOTAL},"
        f"afade=t=in:st=35.061:d=6.0,afade=t=out:st=58.0:d=4.0,volume=-8dB[musB];"
        f"[3:a]{AFMT},atrim=0:5.5,adelay=8087|8087,"
        f"afade=t=in:st=8.087:d=1.0,afade=t=out:st=11.95:d=1.5,volume=-18dB[dawn];"
        f"[4:a]{AFMT},atrim=0:8.0,adelay=19328|19328,"
        f"afade=t=in:st=19.328:d=1.2,afade=t=out:st=27.9:d=1.5,volume=-16dB[choir];"
        f"[5:a]{AFMT},atrim=0:7.0,adelay=35061|35061,"
        f"afade=t=in:st=35.061:d=1.0,afade=t=out:st=40.13:d=1.5,volume=-20dB[wind];"
        f"[musA][musB][dawn][choir][wind]amix=inputs=5:normalize=0[bed];"
        f"[0:a]{AFMT},apad=whole_dur={TOTAL},asplit=2[main][key];"
        f"[bed][key]sidechaincompress={SIDECHAIN}[bedd];"
        f"[main][bedd]amix=inputs=2:normalize=0,"
        f"alimiter=limit=0.85:level=disabled,aresample=44100[mix]"
    )

    subprocess.run(
        ["ffmpeg", "-y", "-v", "error",
         "-i", str(SRC),
         "-i", str(MUS / "neutral_teaching_warm_a.mp3"),
         "-i", str(MUS / "sacred_grace_rise_a.mp3"),
         "-i", str(SND / "dawn_morning_warm.mp3"),
         "-i", str(SND / "heavenly_choir_soft.mp3"),
         "-i", str(SND / "wind_desert_bleak.mp3"),
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
