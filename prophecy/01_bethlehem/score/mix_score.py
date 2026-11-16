"""Mix score.mp3 under film/BETHLEHEM_FILM_v4c.mp4 ($0). Bartimaeus recipe: base -13 dB, voice-keyed sidechain duck,
alimiter. Planned shape (panel): KJV dips 15.8-17.7 + 32.2-34.7; silence 36.3-37.4; near-quiet 37.4-40.4 (experts
never went); back at 40.5; one swell ~50.5-52.4; drop out under "He came to us." 54.6-57.2; tune finishes in the hold."""
import subprocess
from pathlib import Path
H = Path(__file__).resolve().parent
VID, SCORE = H.parent / "film" / "BETHLEHEM_FILM_v4d.mp4", H / "score.mp3"
OUT = H.parent / "film" / "BETHLEHEM_SCORED_v2.mp4"
def seg(a, b, db, ramp=0.4):
    return f"({db})*min(1,max(0,min((t-{a})/{ramp},({b}-t)/{ramp})))"
base = "-13"
extra = "+".join([seg(15.7, 17.8, -8), seg(32.1, 34.8, -5), seg(36.7, 37.5, -40, 0.2), seg(37.3, 40.5, -10), seg(40.4, 43.6, 7),
                  seg(50.3, 52.6, 3), seg(54.5, 56.3, -14), seg(56.2, 60.5, 5)])
vol = f"volume='pow(10,({base}+{extra})/20)':eval=frame"
fc = ("[0:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,asplit=2[v][sc];"
      f"[1:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,{vol}[m];"
      "[m][sc]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[md];"
      "[v][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "3", "-i", str(VID), "-i", str(SCORE),
                "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac",
                "-b:a", "192k", "-movflags", "+faststart", str(OUT)], check=True)
print(OUT)
