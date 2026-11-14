"""Mix score/score.mp3 under film/bartimaeus_draft_v2.mp4 ($0). Second Fire / Well recipe.
Base: part 1 -10 dB, part 2 (raw ~4 dB louder, from 26.1 s) -14 dB. Automation (extra dB):
3-voice exchange 38.4-48.9 -3 | sight lift 49.3-56 +3 | hold 76.3-79.17 +12 (music leads the 3 s hold).
Voice-keyed sidechain duck, alimiter."""
import subprocess
from pathlib import Path
H = Path(__file__).resolve().parent
VID, SCORE = H.parent / "film" / "bartimaeus_draft_v2.mp4", H / "score.mp3"
OUT = H.parent / "film" / "bartimaeus_scored_v1.mp4"
def seg(a, b, db, ramp=0.6):
    return f"({db})*min(1,max(0,min((t-{a})/{ramp},({b}-t)/{ramp})))"
base = "if(lt(t,26.1),-10,-14)"
extra = "+".join([seg(38.4, 48.9, -3), seg(49.3, 56.0, 3), seg(76.3, 80.5, 12)])
vol = f"volume='pow(10,({base}+{extra})/20)':eval=frame"
fc = ("[0:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,asplit=2[v][sc];"
      f"[1:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,{vol}[m];"
      "[m][sc]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[md];"
      "[v][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "3", "-i", str(VID), "-i", str(SCORE),
                "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac",
                "-b:a", "192k", "-movflags", "+faststart", str(OUT)], check=True)
print(OUT)
