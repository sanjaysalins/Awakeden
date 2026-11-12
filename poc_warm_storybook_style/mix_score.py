"""Mix score_piano.mp3 under the voice-only preview ($0). Ep16 recipe: score at -11 dB (this score is ~4 dB quieter than ep16's), lifting to -6 dB, then 0 dB from 74-78 s for the hold;
over the resolution (64.4-69.3 s, "So, did He care?" -> "Now Jesus loved Martha"), sidechain duck under
the voice (thr 0.12, ratio 2.5, attack 20, release 250), alimiter. Gentle: 3 threads."""
import subprocess
from pathlib import Path
H = Path(__file__).resolve().parent
VID, SCORE, OUT = H / "MARY_MARTHA_PREVIEW_v1.mp4", H / "score_piano.mp3", H / "MARY_MARTHA_SCORED_v1.mp4"
A, B = 64.4, 69.3
C, D = 74.0, 78.0  # lift the decaying final chord so it carries the 3 s landing hold
vol = (f"volume='pow(10,(if(lt(t,{A}),-11,if(lt(t,{B}),-11+5*(t-{A})/{B - A:.2f},"
       f"if(lt(t,{C}),-6,if(lt(t,{D}),-6+6*(t-{C})/{D - C:.2f},0)))))/20)':eval=frame")
fc = ("[0:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,asplit=2[v][sc];"
      f"[1:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,{vol}[m];"
      "[m][sc]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[md];"
      "[v][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "3", "-i", str(VID), "-i", str(SCORE),
                "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac",
                "-b:a", "192k", "-movflags", "+faststart", str(OUT)], check=True)
print(OUT)
