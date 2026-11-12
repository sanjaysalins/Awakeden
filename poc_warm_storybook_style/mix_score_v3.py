"""v3 (words H): mix score_piano_v3.mp3 under the v3 preview. Same recipe as v2, times moved ($0).
Score -11 dB, lifting to -8 dB as part 2 enters (52.83-57.83 s), then to 0 dB (64.2-68.2 s) so the final
chord carries the 3 s landing hold. Part 2's 9.5 s chord attack now lands on "Lazarus" (62.4 s): smooth 6 dB dip.
Sidechain duck under the voice (thr 0.12, ratio 2.5, attack 20, release 250), alimiter. Gentle: 3 threads."""
import subprocess
from pathlib import Path
H = Path(__file__).resolve().parent
VID, SCORE, OUT = H / "MARY_MARTHA_PREVIEW_v3.mp4", H / "score_piano_v3.mp3", H / "MARY_MARTHA_SCORED_v3.mp4"
A, B = 52.83, 57.83
C, D = 64.2, 68.2
vol = (f"volume='pow(10,(if(lt(t,{A}),-11,if(lt(t,{B}),-11+3*(t-{A})/{B - A:.2f},"
       f"if(lt(t,{C}),-8,if(lt(t,{D}),-8+8*(t-{C})/{D - C:.2f},0)))))/20)':eval=frame")
dip = "volume='pow(10,-6*max(0,1-abs(t-62.5)/0.7)/20)':eval=frame"
fc = ("[0:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,asplit=2[v][sc];"
      f"[1:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,{vol},{dip}[m];"
      "[m][sc]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[md];"
      "[v][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "3", "-i", str(VID), "-i", str(SCORE),
                "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac",
                "-b:a", "192k", "-movflags", "+faststart", str(OUT)], check=True)
print(OUT)
