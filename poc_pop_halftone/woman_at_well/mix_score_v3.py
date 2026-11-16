"""Mix score/score.mp3 under motion_v2/WOMAN_AT_WELL_MOTION_v2.mp4 ($0). Second Fire recipe.
Base gain: part 1 -10 dB, part 2 (louder raw, from 54.3 s) -15 dB. Automation (extra dB):
drain 23.0-29.8 -4 | flood lift 30.6-37.4 +3 | tomb 81.5-84.74 -5 | 3 s hold ramps back up +4 so the last note rings.
Voice-keyed sidechain duck, alimiter."""
import subprocess
from pathlib import Path
H = Path(__file__).resolve().parent
VID, SCORE = H / "motion_v3" / "WOMAN_AT_WELL_MOTION_v3.mp4", H / "score" / "score_v3.mp3"
OUT = H / "WOMAN_AT_WELL_SCORED_v3.mp4"
def seg(a, b, db, ramp=0.6):  # smooth bump of db between a and b
    return (f"({db})*min(1,max(0,min((t-{a})/{ramp},({b}-t)/{ramp})))")
base = "if(lt(t,56.71),-10,-15)"
extra = "+".join([seg(23.0, 29.8, -4), seg(30.6, 37.4, 3), seg(84.0, 88.04, -5)])
vol = f"volume='pow(10,({base}+{extra})/20)':eval=frame"
fc = ("[0:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,asplit=2[v][sc];"
      f"[1:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,{vol}[m];"
      "[m][sc]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[md];"
      "[v][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "3", "-i", str(VID), "-i", str(SCORE),
                "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac",
                "-b:a", "192k", "-movflags", "+faststart", str(OUT)], check=True)
print(OUT)
