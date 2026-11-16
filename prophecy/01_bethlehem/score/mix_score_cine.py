"""Mix the CINEMATIC score (score_cine.mp3) under film/BETHLEHEM_FILM_v6.mp4 ($0). Real film times (words v3), no warp.
Base -13 dB, voice-keyed sidechain duck, alimiter. Shape from the panel: dips under both KJV lines, TRUE silence
38.0-39.0, lift on 'The wise men went', lift on the 'He rose' swell, drop out under 'He came to us.', tune in the hold."""
import json, subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent
VID = H.parent / "film" / (sys.argv[1] if len(sys.argv) > 1 else "BETHLEHEM_FILM_v6.mp4")
SCORE, OUT = H / "score_cine.mp3", H.parent / "film" / "BETHLEHEM_SCORED_v6.mp4"
W = json.loads((H.parent / "audio_v3" / "narration_v3.words.json").read_text(encoding="utf-8"))
him = next(w for w in W if w["w"].lower().startswith("him") and w["start"] > 50); us = W[-1]
def seg(a, b, db, ramp=0.4):
    return f"({db})*min(1,max(0,min((t-{a:.2f})/{ramp},({b:.2f}-t)/{ramp})))"
extra = "+".join([seg(15.9, 17.5, -8), seg(33.8, 36.5, -5), seg(37.95, 39.05, -40, 0.15),
                  seg(42.1, 45.0, 3), seg(52.5, 54.4, 2), seg(him["end"] - 0.05, us["end"] + 0.2, -14), seg(us["end"] + 0.1, 61.0, 5)])
vol = f"volume='pow(10,(-13+{extra})/20)':eval=frame"
fc = ("[0:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,asplit=2[v][sc];"
      f"[1:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,apad,{vol}[m];"
      "[m][sc]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[md];"
      "[v][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "3", "-i", str(VID), "-i", str(SCORE), "-filter_complex", fc,
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(OUT)], check=True)
print(OUT)
