"""The First Gospel in the Curse -- step 5: SCORE + AMBIENT SFX BED, mixed
onto the already-captioned FIRSTGOSPELINTHECURSE_living_sketchbook_cc.mp4.
Same combined single-pass recipe as the Bronze Serpent shorts' own
_s5_score_sfx.py scripts -- new segments/cues/timings for THIS narration's
own register.

Music arc: lonely_searching_a dominant through the waiting/fear section AND
into the turn itself (0-18.42s) -- crossfading into sacred_grace_rise_a
EXACTLY at s04's own window start (18.42s), the precise moment the
narration's own KJV quote begins ("And I will put enmity..."). This is
literally the piece's own thesis ("Grace Spoken First") made audible: the
music turns the instant the promise is spoken, not at the landing.

Ambient SFX bed (sound_library/clips, $0, ambience-only):
  air_hollow_desolate   0-18.42s -- the waiting/dread section, an isolated
                        held-breath quality before the turn.
  thunder_low_roll       s07 window (35.27-42.94s) -- the storm-cloud
                        gold-thread visual, a subtle low rumble under it.

  .venv\\Scripts\\python.exe poc_living_sketchbook/first_gospel_in_the_curse/_s5_score_sfx.py
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

SRC = HERE / "FIRSTGOSPELINTHECURSE_living_sketchbook_cc.mp4"
OUT = HERE / "FIRSTGOSPELINTHECURSE_living_sketchbook_cc_scored_sfx.mp4"
TOTAL = 69.0  # matches _s3_assemble.py's TOTAL exactly -- INV-26 hold already in SRC


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"missing captioned cut: {SRC} -- run _s4_captions.py first")

    filt = (
        f"[1:a]{AFMT},atrim=0:24,afade=t=in:st=0:d=1.5,"
        f"afade=t=out:st=18.42:d=6.0,volume=-9dB[musA];"
        f"[2:a]{AFMT},adelay=18420|18420,atrim=0:{TOTAL},"
        f"afade=t=in:st=18.42:d=6.0,afade=t=out:st=65.0:d=3.0,volume=-8dB[musB];"
        f"[3:a]{AFMT},atrim=0:18.42,"
        f"afade=t=in:st=0:d=1.5,afade=t=out:st=16.5:d=1.9,volume=-20dB[air];"
        f"[4:a]{AFMT},atrim=0:7.0,adelay=35270|35270,"
        f"afade=t=in:st=35.27:d=1.0,afade=t=out:st=41.5:d=1.4,volume=-16dB[thunder];"
        f"[musA][musB][air][thunder]amix=inputs=4:normalize=0[bed];"
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
         "-i", str(SND / "air_hollow_desolate.mp3"),
         "-i", str(SND / "thunder_low_roll.mp3"),
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
