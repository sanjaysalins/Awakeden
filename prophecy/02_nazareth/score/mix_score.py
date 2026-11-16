r"""Mix score.mp3 under film/NAZARETH_COMIC_v5.mp4 ($0). Base -13 dB, voice-keyed sidechain duck, alimiter (Bethlehem mix_score_cine pattern).
Shape (panel): -6 under Isaiah / 'heal thyself' / the leader; near-silent under Jesus' first line (sacred stillness); small lift on the last line; open up in the 3 s hold."""
import subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent
VID = H.parent / "film" / (sys.argv[1] if len(sys.argv) > 1 else "NAZARETH_COMIC_v5.mp4")
SCORE, OUT = H / "score.mp3", H.parent / "film" / "NAZARETH_SCORED_v5.mp4"
def seg(a, b, db, ramp=0.3):
    return f"({db})*min(1,max(0,min((t-{a:.2f})/{ramp},({b:.2f}-t)/{ramp})))"
extra = "+".join([seg(13.8, 16.8, -6), seg(20.6, 25.3, -14), seg(27.3, 30.0, -6), seg(43.2, 46.0, -6),
                  seg(50.1, 56.1, 2), seg(56.1, 60.0, 6)])
vol = f"volume='pow(10,(-13+{extra})/20)':eval=frame"
fc = ("[0:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,asplit=2[v][sc];"
      f"[1:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,apad,{vol}[m];"
      "[m][sc]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[md];"
      "[v][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "2", "-i", str(VID), "-i", str(SCORE), "-filter_complex", fc,
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(OUT)], check=True)
print(OUT)
