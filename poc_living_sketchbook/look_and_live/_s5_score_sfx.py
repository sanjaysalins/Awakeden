"""Look and Live -- step 5: SCORE + AMBIENT SFX BED, mixed onto the already-
captioned LOOKANDLIVE_living_sketchbook_cc.mp4 (score/sfx are separate
follow-up stages after captions here, since -- unlike bronze_serpent's own
short -- this episode DOES have a burned ivory caption layer, see
_s4_captions.py). Same combined single-pass recipe as bronze_serpent/
_s5_score_sfx.py (proven precedent, same episode family/style), just new
segments/cues/timings for this narration.

Music arc (chained Suno instrumentals from music_library/clips, $0, per
[[longform-score-from-suno-library]]): lonely_searching_a (dread/the object
that isn't medicine) dominant s01-s06 (0-18.7s), crossfading across s07's
own window (18.7-24.9s) -- the episode's own literary turn ("when he
looketh upon it, shall live") -- into sacred_grace_rise_a, dominant through
the landing. Same pivot-on-the-turn-line discipline as bronze_serpent short.

Ambient SFX bed (sound_library/clips, $0, ambience-only per
[[feedback-audio-layer-stack]] -- no second musical pad):
  wind_desert_bleak    looped (source 22s < 62.5s episode), very low, whole
                        episode -- the wilderness ground.
  crowd_murmur_distant  s01 window (0-4.4s, the panic) AND s08 window
                        (24.9-30.5s, the healing crowd) -- same slug, two
                        windows, matching bronze_serpent_long's own pattern
                        for a recurring crowd beat.
  rumble_deep_sub       s03/s04 window (7.9-11.9s, the unused remedy /
                        bitten arm) -- dread under the wound, not the cure.
  dawn_morning_warm     s09 window (30.5-38.6s, "calm dawn sky") -- subtle,
                        motivated by the plan's own atmosphere description,
                        not a stretch addition.

No forge/fire cue here -- unlike short #2, this narration never names Moses
or the forging (per _PLAN.md's own cast census), so fire_crackling doesn't
apply.

  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_s5_score_sfx.py
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

SRC = HERE / "LOOKANDLIVE_living_sketchbook_cc.mp4"
OUT = HERE / "LOOKANDLIVE_living_sketchbook_cc_scored_sfx.mp4"
TOTAL = 62.5  # matches _s3_assemble.py's TOTAL exactly -- INV-26 hold already in SRC


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"missing captioned cut: {SRC} -- run _s4_captions.py first")

    filt = (
        f"[1:a]{AFMT},atrim=0:25,afade=t=in:st=0:d=1.5,"
        f"afade=t=out:st=18.7:d=6.2,volume=-9dB[musA];"
        f"[2:a]{AFMT},adelay=18700|18700,atrim=0:{TOTAL},"
        f"afade=t=in:st=18.7:d=6.2,afade=t=out:st=59.5:d=3.0,volume=-8dB[musB];"
        f"[3:a]{AFMT},atrim=0:{TOTAL},afade=t=in:st=0:d=2,volume=-20dB[wind];"
        f"[4:a]{AFMT},atrim=0:4.4,"
        f"afade=t=in:st=0:d=0.5,afade=t=out:st=3.6:d=0.8,volume=-15dB[crowd1];"
        f"[5:a]{AFMT},atrim=0:5.6,adelay=24900|24900,"
        f"afade=t=in:st=24.9:d=0.8,afade=t=out:st=29.7:d=0.8,volume=-15dB[crowd2];"
        f"[6:a]{AFMT},atrim=0:4.0,adelay=7900|7900,"
        f"afade=t=in:st=7.9:d=1.0,afade=t=out:st=11.0:d=0.9,volume=-17dB[rumble];"
        f"[7:a]{AFMT},atrim=0:8.1,adelay=30500|30500,"
        f"afade=t=in:st=30.5:d=1.5,afade=t=out:st=37.6:d=1.0,volume=-18dB[dawn];"
        f"[musA][musB][wind][crowd1][crowd2][rumble][dawn]amix=inputs=7:normalize=0[bed];"
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


if __name__ == "__main__":
    main()
