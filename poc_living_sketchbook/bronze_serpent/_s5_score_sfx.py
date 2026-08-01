"""Bronze Serpent episode -- step 5: SCORE + AMBIENT SFX BED (Stage 3b),
mixed onto the already-locked BRONZESERPENT_living_sketchbook.mp4 (video +
narration only, 71.5s, INV-26 hold already baked in -- see _s4_assemble.py).
No new frames are rendered; this is an audio-only remux onto the existing,
approved picture (per living-sketchbook style, the format has NO ivory
caption layer -- the hand-lettered devices already on the page ARE the
caption, see memory `caption-policy-comic-boxes` / `native-panel-captions-
minimal` -- so the finishing chain here is score -> sfx -> watermark ->
validate, not score -> sfx -> caption -> watermark).

Music arc (chained Suno instrumentals from music_library/clips, $0, per
[[longform-score-from-suno-library]]): the same validated ache-then-grace
pair as Isaiah 53 / Storm --
  lonely_searching_a  (dread/searching)   dominant s01-s06 (0-28.1s, the
                                            affliction/forge beats)
  sacred_grace_rise_a (orchestral swell)  dominant s07-s14 (28.1-71.5s)
crossfaded across s07's own window (28.1-36.9s), which is the episode's own
literary pivot line ("I speak now from the far side of my life, by the
light that came after") -- the music turn lands exactly on the narration's
own turn, not an arbitrary timestamp.

Ambient SFX bed (sound_library/clips, $0, ambience-only per
[[feedback-audio-layer-stack]] -- never a second musical pad, so
heavenly_choir_soft / score_reverent_grace are deliberately NOT used here,
see [[longform-score-from-suno-library]]'s DUAL-SCORE TRAP):
  wind_desert_bleak    looped (-stream_loop -1, source is 22s < 71.5s
                        episode), very low, whole episode -- grounds
                        "WILDERNESS. FORTIETH YEAR." (s01's own header)
  crowd_murmur_distant  s03 window (8.230-14.856s) -- the people's complaint
  rumble_deep_sub       same s03/s04 window, lower/subtler -- judgment dread
                        layered under the crowd, not instead of it
  fire_crackling        s06 window (18.798-28.105s) -- Moses at the forge

All background layers are summed into one bed, sidechain-ducked under the
narration (reusing pipeline/score_mix.py's AFMT/SIDECHAIN -- the project's
one shared constant, not re-derived), alimiter=0.85 per the /sfx skill's own
guardrail (not score_mix.mix_tail's 0.97 -- that helper is for the simpler
single-music-bed case and assumes narration+video share one input; here
narration is ALREADY muxed into input 0 alongside video, and there are
multiple summed SFX layers, so the tail is written out by hand, same as
storm/_s6_assemble.py's own precedent for a multi-layer bed).

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent/_s5_score_sfx.py
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

SRC = HERE / "BRONZESERPENT_living_sketchbook.mp4"
OUT = HERE / "BRONZESERPENT_living_sketchbook_sfx.mp4"
TOTAL = 71.5  # matches _s4_assemble.py's TOTAL exactly -- INV-26 hold already in SRC


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"missing base cut: {SRC} -- run _s4_assemble.py first")

    filt = (
        f"[1:a]{AFMT},atrim=0:35,afade=t=in:st=0:d=1.5,"
        f"afade=t=out:st=27:d=8,volume=-9dB[musA];"
        f"[2:a]{AFMT},adelay=28000|28000,atrim=0:{TOTAL},"
        f"afade=t=in:st=28:d=6,afade=t=out:st=68.0:d=3.5,volume=-8dB[musB];"
        f"[3:a]{AFMT},atrim=0:{TOTAL},afade=t=in:st=0:d=2,volume=-20dB[wind];"
        f"[4:a]{AFMT},atrim=0:6.6,adelay=8230|8230,"
        f"afade=t=in:st=8.23:d=0.8,afade=t=out:st=13.6:d=1.2,volume=-14dB[crowd];"
        f"[5:a]{AFMT},atrim=0:6.6,adelay=8230|8230,"
        f"afade=t=in:st=8.23:d=1.0,afade=t=out:st=13.6:d=1.2,volume=-18dB[rumble];"
        f"[6:a]{AFMT},atrim=0:9.3,adelay=18798|18798,"
        f"afade=t=in:st=18.8:d=1.0,afade=t=out:st=27.0:d=1.5,volume=-13dB[fire];"
        f"[musA][musB][wind][crowd][rumble][fire]amix=inputs=6:normalize=0[bed];"
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
         "-i", str(SND / "rumble_deep_sub.mp3"),
         "-i", str(SND / "fire_crackling.mp3"),
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
