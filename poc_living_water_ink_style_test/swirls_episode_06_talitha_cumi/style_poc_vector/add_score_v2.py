"""Talitha Cumi vector POC - lay ep7's felt-piano score (reuse, $0) under preview v2.

Duck tuning = ep7's own DuckProfile (gain -6 dB, threshold 0.12, ratio 2.5,
release 250). Music fades out over the 3 s landing hold. Video stream copied.
"""
import subprocess, sys, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "TALITHA_PREVIEW_G5_v2.mp4"
SCORE = HERE.parents[1] / "swirls_episode_07_the_bier_he_touched" / "score_piano_raw.mp3"
OUT = HERE / "TALITHA_PREVIEW_G5_v2_score.mp4"
AFMT = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"
LOW = 0x00004000 if sys.platform == "win32" else 0


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


total = dur(SRC)
fc = (f"[1:a]{AFMT},atrim=0:{total:.3f},asetpts=PTS-STARTPTS,volume=-6dB,"
      f"afade=t=in:d=0.5,afade=t=out:st={total - 3.0:.3f}:d=3.0[mus];"
      f"[0:a]{AFMT},asplit=2[main][key];"
      f"[mus][key]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[musd];"
      f"[main][musd]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix]")
cmd = ["ffmpeg", "-y", "-hide_banner", "-threads", "3", "-i", str(SRC), "-i", str(SCORE),
       "-filter_complex", fc, "-map", "0:v", "-map", "[mix]", "-c:v", "copy",
       "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", "-movflags", "+faststart", str(OUT)]
r = subprocess.run(cmd, capture_output=True, text=True, creationflags=LOW)
if r.returncode:
    print(r.stderr[-2000:]); raise SystemExit(1)
print(json.dumps({"out": str(OUT), "total": total, "result": dur(OUT)}))
