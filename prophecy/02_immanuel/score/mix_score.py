"""Mix score.mp3 under film/IMMANUEL_FILM_v2.mp4 ($0). Same recipe as Ep 01 mix_score_cine.py: base -13 dB,
voice-keyed sidechain duck, alimiter. Panel shape: dips under the KJV lines (Isaiah, angel, Jesus), lift on the
'He rose' swell, tune up in the 3 s hold after 'That was God's answer.'"""
import json, subprocess
from pathlib import Path
H = Path(__file__).resolve().parent
import sys
VID = H.parent / "film" / (sys.argv[1] if len(sys.argv) > 1 else "IMMANUEL_FILM_v2.mp4")
OUT = H.parent / "film" / (sys.argv[2] if len(sys.argv) > 2 else "IMMANUEL_SCORED_v2.mp4")
SCORE = H / "score.mp3"
T = {x["i"]: x for x in json.loads((H.parent / "audio_v2" / "timeline.json").read_text(encoding="utf-8"))}
def seg(a, b, db, ramp=0.4):
    return f"({db})*min(1,max(0,min((t-{a:.2f})/{ramp},({b:.2f}-t)/{ramp})))"
end = T[10]["end"]
extra = "+".join([seg(-1, 4.5, 6), seg(37.8, 66.0, -4), seg(T[2]["start"] - 0.1, T[2]["end"] + 0.1, -6), seg(T[5]["start"] - 0.1, T[6]["end"] + 0.1, -4),
                  seg(T[9]["start"] - 0.1, T[9]["end"] + 0.1, -8), seg(56.5, 58.1, 2), seg(end + 0.1, 66.0, 9)])
vol = f"volume='pow(10,(-13+{extra})/20)':eval=frame"
fc = ("[0:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,asplit=2[v][sc];"
      f"[1:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,apad,{vol}[m];"
      "[m][sc]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[md];"
      "[v][md]amix=inputs=2:duration=first:normalize=0,volume=2.2dB,alimiter=limit=0.95[a]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "3", "-i", str(VID), "-i", str(SCORE), "-filter_complex", fc,
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(OUT)], check=True)
print(OUT)
