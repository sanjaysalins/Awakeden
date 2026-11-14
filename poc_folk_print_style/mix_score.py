"""Mix score_piano.mp3 under SECOND_FIRE_PREVIEW_v2.mp4 ($0). Mary & Martha / ep16 recipe.
Part 1 (0-53.2 s) measured ~5 dB quieter than part 2, so: -9 dB before the split, -14 dB after;
lift to -9 dB over "Three times, yes" (75.2-80.3 s), then to -4 dB for the 3 s landing hold
(84.9-87.9 s). Sidechain duck under the voice (thr 0.12, ratio 2.5, attack 20, release 250),
alimiter. Gentle: 3 threads."""
import subprocess
from pathlib import Path
H = Path(__file__).resolve().parent
VID, SCORE, OUT = H / "SECOND_FIRE_PREVIEW_v2.mp4", H / "score_piano.mp3", H / "SECOND_FIRE_SCORED_v1.mp4"
S = 53.2            # split
A, B = 75.2, 80.3   # "Three times, yes" lift
C, D = 84.9, 87.9   # landing hold
vol = (f"volume='pow(10,(if(lt(t,{S}),-9,if(lt(t,{A}),-14,if(lt(t,{B}),-14+5*(t-{A})/{B - A:.2f},"
       f"if(lt(t,{C}),-9,-9+5*min(1,(t-{C})/1.5))))))/20)':eval=frame")
fc = ("[0:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,asplit=2[v][sc];"
      f"[1:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,{vol}[m];"
      "[m][sc]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[md];"
      "[v][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "3", "-i", str(VID), "-i", str(SCORE),
                "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac",
                "-b:a", "192k", "-movflags", "+faststart", str(OUT)], check=True)
print(OUT)
