"""Re-run ONLY the v6 audio mux with the FIXED filter graph (asplit=3).
The frame render + silent video + foley bus from the full run are valid and
on disk; the original process failed at the mux because it was launched
before the asplit fix landed and held the old graph in memory.

  POLITE_CPU=100 ..\\..\\..\\.venv\\Scripts\\python.exe _s6_mixfix.py
"""
import subprocess
from pathlib import Path

import _s6_assemble as S6

HERE = Path(__file__).resolve().parent
silent = HERE / "_silent_v6.mp4"
foley_raw = HERE / "_foley_v6.raw"
assert silent.exists() and silent.stat().st_size > 10_000_000, "silent video missing"
assert foley_raw.exists() and foley_raw.stat().st_size > 1_000_000, "foley bus missing"

OUT = S6.OUT
if OUT.exists() and OUT.stat().st_size == 0:
    OUT.unlink()  # the failed run's 0-byte corpse

SND = S6.ROOT / "sound_library" / "clips"
MUS = S6.ROOT / "music_library" / "clips"
vdur = S6.TOTAL
AFMT, SIDECHAIN = S6.AFMT, S6.SIDECHAIN

silence = "volume=0.18:enable='between(t,23.55,27.43)',"
filt = (
    f"[1:a]{AFMT},apad=whole_dur={vdur},asplit=3[main][key1][key2];"
    f"[2:a]{AFMT},atrim=0:{vdur},afade=t=in:st=0:d=1.5,"
    f"afade=t=out:st=29.5:d=2.5,volume=-9dB,{silence}anull[musA];"
    f"[3:a]{AFMT},adelay=28200|28200,atrim=0:{vdur},"
    f"afade=t=in:st=28.2:d=2.5,afade=t=out:st={vdur - 2.5:.1f}:d=2.5,"
    f"volume=-8dB[musB];"
    f"[musA][musB]amix=inputs=2:normalize=0[mus];"
    f"[mus][key1]sidechaincompress={SIDECHAIN}[musd];"
    f"[4:a]{AFMT},atrim=0:18.0,volume=-16dB[creak];"
    f"[5:a]atrim=0:6.0,volume=-14dB,adelay=0|0,{AFMT}[thunder];"
    f"[6:a]atrim=0:0.9,lowpass=f=700,volume=0.55,adelay=27800|27800,{AFMT}[boom];"
    f"[7:a]{AFMT},adelay=30000|30000,atrim=0:{vdur},volume=-18dB[shore];"
    f"[8:a]{AFMT}[foleyraw];"
    f"[foleyraw][key2]sidechaincompress={SIDECHAIN}[foleyd];"
    f"[main][musd][creak][thunder][boom][shore][foleyd]amix=inputs=7:normalize=0,"
    f"alimiter=limit=0.97,aresample=44100[mix]"
)
subprocess.run(["ffmpeg", "-y", "-v", "error",
                "-i", str(silent), "-i", str(S6.SRC_AUDIO),
                "-i", str(MUS / "lonely_searching_a.mp3"),
                "-i", str(MUS / "sacred_grace_rise_a.mp3"),
                "-i", str(SND / "boat_creak_oars.mp3"),
                "-i", str(SND / "thunder_low_roll.mp3"),
                "-i", str(SND / "impact_low_boom.mp3"),
                "-i", str(SND / "sea_waves_shore.mp3"),
                "-f", "f32le", "-ar", "44100", "-ac", "2", "-i", str(foley_raw),
                "-filter_complex", filt,
                "-map", "0:v", "-map", "[mix]", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k", "-t", f"{vdur}",
                str(OUT)], check=True)
print(f"[ok] {OUT} ({OUT.stat().st_size/1e6:.1f} MB)")
