#!/usr/bin/env python
"""I Thirst (John 19:28 / Ps 22:15) — $0 score: lonely_searching_a -> sacred_grace_rise_a,
grace entering on the living-water turn (44.0s). Ducked under narration; dips under the
Ps 22:15 bars and the I-thirst cry; thinned under the CTA."""
import subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MUS = ROOT / "music_library" / "clips"
SRC = HERE / "visual" / "livingpage_short.spec_preview.mp4"
OUT = HERE / "visual" / "i_thirst_john1928_scored.mp4"
DARK, GRACE = MUS / "lonely_searching_a.mp3", MUS / "sacred_grace_rise_a.mp3"
TOTAL = 55.74 + 1.5                      # +1.5s outro hold on the dawn cross

fc = (
    f"[1:a]atrim=0:43.9,aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100[d];"
    f"[2:a]atrim=20:90,aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100[g];"
    f"[d][g]acrossfade=d=6:c1=exp:c2=exp[mch];"
    f"[mch]atrim=0:{TOTAL},afade=t=in:st=0:d=1.5,afade=t=out:st={TOTAL-1.5:.2f}:d=1.5,volume=-13dB,"
    f"volume=volume=0.4:enable='between(t,15.2,26.45)',"
    f"volume=volume=0.35:enable='between(t,32.6,36.7)',"
    f"volume=volume=0.5:enable='between(t,49.4,{TOTAL})'[mus];"
    f"[0:a]asplit=2[main][key];"
    f"[mus][key]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[musd];"
    f"[main][musd]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix];"
    f"[0:v]tpad=stop_mode=clone:stop_duration=1.5[vout]"
)
r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(SRC), "-i", str(DARK), "-i", str(GRACE),
                    "-filter_complex", fc, "-map", "[vout]", "-map", "[mix]",
                    "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(OUT)],
                   capture_output=True, text=True)
if r.returncode:
    sys.exit(f"score failed:\n{r.stderr[-800:]}")
print(f"DONE -> {OUT}")
