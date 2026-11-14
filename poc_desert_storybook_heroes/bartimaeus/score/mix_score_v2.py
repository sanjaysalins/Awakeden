"""Mix score_v2.mp3 (melody) under film/bartimaeus_draft_v2.mp4 ($0). Same recipe as mix_score.py; part 1 -13, part 2 -14,
extra: dialogue 38.4-48.9 -3 | sight 49.3-56 +5 | cross 61.3-66 -3 (raw swells there) | hold +18 (raw tail fades). Duck + alimiter.

Voice-keyed sidechain duck, alimiter."""
import subprocess
from pathlib import Path
H = Path(__file__).resolve().parent
VID, SCORE = H.parent / "film" / "bartimaeus_draft_v2.mp4", H / "score_v2.mp3"
OUT = H.parent / "film" / "bartimaeus_scored_v2.mp4"
def seg(a, b, db, ramp=0.6):
    return f"({db})*min(1,max(0,min((t-{a})/{ramp},({b}-t)/{ramp})))"
base = "if(lt(t,26.1),-13,-14)"
extra = "+".join([seg(38.4, 48.9, -3), seg(49.3, 56.0, 5), seg(61.3, 66.0, -3), seg(76.3, 80.5, 18)])
vol = f"volume='pow(10,({base}+{extra})/20)':eval=frame"
fc = ("[0:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,asplit=2[v][sc];"
      f"[1:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,{vol}[m];"
      "[m][sc]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[md];"
      "[v][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "3", "-i", str(VID), "-i", str(SCORE),
                "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac",
                "-b:a", "192k", "-movflags", "+faststart", str(OUT)], check=True)
print(OUT)
