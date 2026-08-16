"""God Hung Up a Snake -- step 5: SCORE + AMBIENT SFX BED, mixed onto the
already-captioned GODHUNGUPASNAKE_living_sketchbook_cc.mp4. Same combined
single-pass recipe as bronze_serpent/_s5_score_sfx.py and this cluster's own
Look and Live/_s5_score_sfx.py, new segments/cues/timings for THIS
narration's own heavier, later-turning register (per _PLAN.md: "starker...
building to Christ BECOMING the curse, not just being lifted up for
healing... heavier, less invitational" than Look and Live).

Music arc (chained Suno instrumentals, $0): lonely_searching_a stays
dominant much longer than in Look and Live -- through the forge, the
mother-and-child, Moses's resolute face, and the darkest line in the piece
("He became your curse", s10, 41.6-47.3s) -- crossfading only at s11
(47.3-51.0s), where the text itself turns ("God hung up a snake so the camp
could live"), then sacred_grace_rise_a carries the landing (torn-to-gold,
Christ on the cross).

Ambient SFX bed (sound_library/clips, $0, ambience-only):
  wind_desert_bleak    looped (source 22s < 60.8s episode), very low, whole
                        episode.
  rumble_deep_sub       s01 window (0-4.6s, the plague-struck camp) -- dread
                        under the opening, before the serpent is even shown.
  crowd_murmur_distant  s04 window (9.5-15.0s, "the whole camp gathered,
                        every eye on the pole").
  fire_crackling        s05 window (15.0-19.0s, Moses at the forge).
  nail_strike_single    2 short punctuation hits inside s05's own window
                        (the hammer actually striking bronze), same
                        treatment as bronze_serpent_long's own forge beat.

  .venv\\Scripts\\python.exe poc_living_sketchbook/god_hung_up_a_snake/_s5_score_sfx.py
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

SRC = HERE / "GODHUNGUPASNAKE_living_sketchbook_cc.mp4"
OUT = HERE / "GODHUNGUPASNAKE_living_sketchbook_cc_scored_sfx.mp4"
# RE-ALIGNED 2026-08-16 against the re-synthesized narration.mp3 (scripture
# voice added to the Numbers 21:9 quote) -- every cue below recomputed from
# the fresh _alignment.json via the same gap-midpoint / interpolation used
# in _s3_assemble.py and _s3b_titlecards.py; old values in comments.
TOTAL = 62.0  # matches _s3_assemble.py's TOTAL exactly -- INV-26 hold already in SRC (was 60.8)


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"missing captioned cut: {SRC} -- run _s4_captions.py first")

    filt = (
        f"[1:a]{AFMT},atrim=0:52.7,afade=t=in:st=0:d=1.5,"                                    # atrim was 0:52
        f"afade=t=out:st=45.66:d=6.0,volume=-9dB[musA];"                                       # fade out st was 45.0
        f"[2:a]{AFMT},adelay=51657|51657,atrim=0:{TOTAL},"                                     # adelay was 45000
        f"afade=t=in:st=51.66:d=6.0,afade=t=out:st=59.0:d=3.0,volume=-8dB[musB];"               # fade in st was 45.0, fade out st was 57.8
        f"[3:a]{AFMT},atrim=0:{TOTAL},afade=t=in:st=0:d=2,volume=-20dB[wind];"
        f"[4:a]{AFMT},atrim=0:5.45,"                                                            # atrim was 0:4.6
        f"afade=t=in:st=0:d=0.8,afade=t=out:st=4.65:d=0.8,volume=-17dB[rumble];"                # fade out st was 3.8
        f"[5:a]{AFMT},atrim=0:5.46,adelay=10291|10291,"                                         # atrim was 0:5.5, adelay was 9500
        f"afade=t=in:st=10.29:d=0.8,afade=t=out:st=14.95:d=0.8,volume=-15dB[crowd];"            # fade in st was 9.5, fade out st was 14.2
        f"[6:a]{AFMT},atrim=0:4.91,adelay=15745|15745,"                                         # atrim was 0:4.0, adelay was 15000
        f"afade=t=in:st=15.75:d=0.8,afade=t=out:st=19.86:d=0.8,volume=-14dB[fire];"             # fade in st was 15.0, fade out st was 18.2
        f"[7:a]{AFMT},atrim=0:0.6,adelay=16968|16968,volume=-10dB[nail1];"                      # adelay was 16000
        f"[8:a]{AFMT},atrim=0:0.6,adelay=18988|18988,volume=-10dB[nail2];"                      # adelay was 17600
        f"[musA][musB][wind][rumble][crowd][fire][nail1][nail2]amix=inputs=8:normalize=0[bed];"
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
         "-i", str(SND / "rumble_deep_sub.mp3"),
         "-i", str(SND / "crowd_murmur_distant.mp3"),
         "-i", str(SND / "fire_crackling.mp3"),
         "-i", str(SND / "nail_strike_single.mp3"),
         "-i", str(SND / "nail_strike_single.mp3"),
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
