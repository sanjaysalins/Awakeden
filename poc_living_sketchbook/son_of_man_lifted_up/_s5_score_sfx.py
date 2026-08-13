"""Even So Must the Son of Man Be Lifted Up -- step 5: SCORE + AMBIENT SFX
BED, mixed onto the already-captioned SONOFMANLIFTEDUP_living_sketchbook_cc.mp4.
Same combined single-pass recipe as this cluster's own bronze_serpent/
_s5_score_sfx.py, look_and_live/_s5_score_sfx.py, god_hung_up_a_snake/
_s5_score_sfx.py -- new segments/cues/timings for THIS narration's own
register: an intimate night dialogue (Nicodemus + Jesus) rather than a
crisis/plague, so the bed stays quieter and more contemplative through
most of the runtime, only opening up at the cross.

Music arc: lonely_searching_a stays dominant through the whole rooftop
dialogue AND the KJV quote itself (0-35.75s) -- crossfading into
sacred_grace_rise_a only at s08 (35.75-41.67s), the moment the narration
itself names the cross ("John uses that word again at the cross"). This is
the LATEST-arriving turn of the 3 shorts in this cluster, matching how
intimate/dialogue-driven this piece stays right up to the reveal.

Ambient SFX bed (sound_library/clips, $0, ambience-only):
  wind_desert_bleak    ONLY during the two OT-echo cutaways -- s04
                        (14.72-19.30s) and s06 (28.09-33.32s) -- grounding
                        the wilderness flashback specifically, not the
                        whole runtime (this episode is mostly a rooftop
                        scene, not a desert one).
  thunder_low_roll      s08 window (35.75-41.67s) -- "torn storm clouds
                        gathering" at the cross reveal, paired with the
                        music's own swell.
  crowd_murmur_distant  s10 window (44.27-48.58s, the witnesses at the
                        foot of the cross).

  .venv\\Scripts\\python.exe poc_living_sketchbook/son_of_man_lifted_up/_s5_score_sfx.py
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

SRC = HERE / "SONOFMANLIFTEDUP_living_sketchbook_cc.mp4"
OUT = HERE / "SONOFMANLIFTEDUP_living_sketchbook_cc_scored_sfx.mp4"
TOTAL = 58.0  # matches _s3_assemble.py's TOTAL exactly -- INV-26 hold already in SRC


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"missing captioned cut: {SRC} -- run _s4_captions.py first")

    filt = (
        f"[1:a]{AFMT},atrim=0:40,afade=t=in:st=0:d=1.5,"
        f"afade=t=out:st=35.75:d=6.0,volume=-9dB[musA];"
        f"[2:a]{AFMT},adelay=35750|35750,atrim=0:{TOTAL},"
        f"afade=t=in:st=35.75:d=6.0,afade=t=out:st=55.0:d=3.0,volume=-8dB[musB];"
        f"[3:a]{AFMT},atrim=0:4.58,adelay=14720|14720,"
        f"afade=t=in:st=14.72:d=0.8,afade=t=out:st=18.5:d=0.8,volume=-20dB[wind1];"
        f"[4:a]{AFMT},atrim=0:5.23,adelay=28090|28090,"
        f"afade=t=in:st=28.09:d=0.8,afade=t=out:st=32.5:d=0.8,volume=-20dB[wind2];"
        f"[5:a]{AFMT},atrim=0:5.92,adelay=35750|35750,"
        f"afade=t=in:st=35.75:d=0.8,afade=t=out:st=40.9:d=0.8,volume=-16dB[thunder];"
        f"[6:a]{AFMT},atrim=0:4.31,adelay=44270|44270,"
        f"afade=t=in:st=44.27:d=0.8,afade=t=out:st=47.8:d=0.8,volume=-15dB[crowd];"
        f"[musA][musB][wind1][wind2][thunder][crowd]amix=inputs=6:normalize=0[bed];"
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
         "-i", str(SND / "wind_desert_bleak.mp3"),
         "-i", str(SND / "thunder_low_roll.mp3"),
         "-i", str(SND / "crowd_murmur_distant.mp3"),
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
