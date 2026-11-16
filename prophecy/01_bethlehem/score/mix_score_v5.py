"""Mix score_v5.mp3 under film/BETHLEHEM_FILM_v5.mp4 ($0). Same shape as mix_score.py (words v2), every cue moved
to the words-v3 timing: old cue times through the warp; the 'He came to us' drop from the real new word times."""
import json, subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent
sys.path.insert(0, str(H.parent / "motion_v5"))
from warp import o2n
VID, SCORE = H.parent / "film" / "BETHLEHEM_FILM_v5.mp4", H / "score_v5.mp3"
OUT = H.parent / "film" / "BETHLEHEM_SCORED_v5.mp4"
W = json.loads((H.parent / "audio_v3" / "narration_v3.words.json").read_text(encoding="utf-8"))
him = next(w for w in W if w["w"].lower().startswith("him") and w["start"] > 50)
us = W[-1]
def seg(a, b, db, ramp=0.4):
    return f"({db})*min(1,max(0,min((t-{a:.2f})/{ramp},({b:.2f}-t)/{ramp})))"
def oseg(a, b, db, ramp=0.4):
    return seg(o2n(a), o2n(b), db, ramp)
extra = "+".join([
    seg(15.9, 17.5, -8),                       # prophet KJV line
    oseg(32.1, 34.8, -5),                      # scribe KJV line
    oseg(36.7, 37.5, -40, 0.2),                # true silence after "close by"
    oseg(37.3, 40.5, -10),                     # the experts never went
    oseg(40.4, 43.6, 7),                       # the wise men went
    oseg(50.3, 52.6, 3),                       # one swell
    seg(him["end"] - 0.05, us["end"] + 0.25, -14),   # drop out under "He came to us."
    seg(us["end"] + 0.15, 61.0, 5),            # the tune finishes in the hold
])
vol = f"volume='pow(10,(-13+{extra})/20)':eval=frame"
fc = ("[0:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,asplit=2[v][sc];"
      f"[1:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,apad,{vol}[m];"
      "[m][sc]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[md];"
      "[v][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "3", "-i", str(VID), "-i", str(SCORE),
                "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac",
                "-b:a", "192k", "-movflags", "+faststart", str(OUT)], check=True)
print(OUT, "drop", round(him["end"], 2), "-", round(us["end"], 2))
