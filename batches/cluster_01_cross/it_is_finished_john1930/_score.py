#!/usr/bin/env python
"""It Is Finished (John 19:30) — $0 score: lonely_searching_a -> sacred_grace_rise_a, grace
landing on the border-break ('It is finished', 35.35s). Ducked under narration; dips under
the John 17:4 prayer bar and the John 19:30 bars; thinned under the CTA. Pilot mix stack."""
import subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MUS = ROOT / "music_library" / "clips"
SRC = HERE / "visual" / "livingpage_short.spec_preview.mp4"
OUT = HERE / "visual" / "it_is_finished_john1930_scored.mp4"
DARK, GRACE = MUS / "lonely_searching_a.mp3", MUS / "sacred_grace_rise_a.mp3"
TOTAL = 59.09 + 1.5                      # +1.5s outro hold on the dawn cross

fc = (
    f"[1:a]atrim=0:35.3,aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100[d];"
    f"[2:a]atrim=20:90,aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100[g];"
    f"[d][g]acrossfade=d=6:c1=exp:c2=exp[mch];"
    f"[mch]atrim=0:{TOTAL},afade=t=in:st=0:d=1.5,afade=t=out:st={TOTAL-1.5:.2f}:d=1.5,volume=-13dB,"
    f"volume=volume=0.4:enable='between(t,24.4,30.2)',"        # John 17:4 prayer bar
    f"volume=volume=0.35:enable='between(t,31.8,39.85)',"      # It is finished + bowed head bars
    f"volume=volume=0.5:enable='between(t,54.45,{TOTAL})'[mus];"  # thin under the CTA
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
