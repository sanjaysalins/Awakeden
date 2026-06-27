"""Assemble the 3 SHORT energy variants from the rendered Kling clips + VO + music.
V1 moderate fast-cut (viral clips, ~3s cuts) · V2 parallax (depth clips, ~3s cuts) ·
V3 max energy (viral clips chopped ~1.5s, rapid). Same 45.3s VO + music bed. $0 (ffmpeg)."""
import subprocess, sys
from pathlib import Path

V = Path(__file__).resolve().parent.parent / "longform/EW01_Two_Goats/v1/short/visual_9x16_test"
VAR = V / "variants"
NORM = VAR / "_norm"; NORM.mkdir(exist_ok=True)
SEG = VAR / "_seg"; SEG.mkdir(exist_ok=True)
VO = VAR / "vo_slice.mp3"
MUSIC = Path(__file__).resolve().parent.parent / "music_library/clips/lonely_searching_a.mp3"
DUR = 45.3
ORDER = ["s1_hook", "s2_two_goats", "s3_blood_veil", "s4_hands_confess", "s5_scapegoat_desert"]

def run(cmd): subprocess.run(cmd, check=True)

# 1. normalize every source clip to 1080x1920 30fps silent
def norm(name):
    src = VAR / f"{name}.mp4"; out = NORM / f"{name}.mp4"
    if not out.exists():
        run(["ffmpeg","-y","-loglevel","error","-i",str(src),"-vf",
             "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30",
             "-an","-c:v","libx264","-pix_fmt","yuv420p","-preset","veryfast",str(out)])
    return out

for k in ORDER:
    norm(f"{k}.v1_viral"); norm(f"{k}.v2_parallax")

# 2. looped music bed to 46s
bed = VAR / "_musicbed.mp3"
if not bed.exists():
    run(["ffmpeg","-y","-loglevel","error","-stream_loop","-1","-i",str(MUSIC),"-t","46",
         "-c","copy",str(bed)])

# 3. cut a segment from a normalized clip
def cut(clipname, start, dur, tag):
    out = SEG / f"{tag}.mp4"
    run(["ffmpeg","-y","-loglevel","error","-ss",str(start),"-i",str(NORM/f'{clipname}.mp4'),
         "-t",str(dur),"-c:v","libx264","-pix_fmt","yuv420p","-preset","veryfast","-an",str(out)])
    return out

# build a variant: segs = list of (clipname, start, dur)
def build(name, segs):
    files = []
    for i,(clip,st,du) in enumerate(segs):
        files.append(cut(clip, st, du, f"{name}_{i:02d}"))
    listf = SEG / f"{name}.txt"
    listf.write_text("".join(f"file '{f.as_posix()}'\n" for f in files), encoding="utf-8")
    silent = VAR / f"_{name}_silent.mp4"
    run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(listf),
         "-c","copy",str(silent)])
    out = VAR / f"cut_{name}.mp4"
    run(["ffmpeg","-y","-loglevel","error","-i",str(silent),"-i",str(VO),"-i",str(bed),
         "-filter_complex","[1:a]volume=1.0[vo];[2:a]volume=0.16[mu];[vo][mu]amix=inputs=2:duration=first[a]",
         "-map","0:v","-map","[a]","-t",str(DUR),"-c:v","libx264","-pix_fmt","yuv420p",
         "-c:a","aac","-shortest",str(out)])
    print(f"[{name}] {out}")
    return out

# segment plans -------------------------------------------------------------
# V1 moderate: 15 cuts ~3.02s each (5 images x 3 revisits), alternating crop start
v1 = []
for k in ORDER:
    for j,st in enumerate([0.0,1.6,0.4]):
        v1.append((f"{k}.v1_viral", st, 3.02))
# V2 parallax: same rhythm, parallax clips
v2 = []
for k in ORDER:
    for st in [0.0,1.6,0.4]:
        v2.append((f"{k}.v2_parallax", st, 3.02))
# V3 max energy: 30 cuts ~1.51s each (5 images x 6 rapid revisits), viral clips
v3 = []
for k in ORDER:
    for st in [0.0,1.0,2.0,3.0,0.6,2.6]:
        v3.append((f"{k}.v1_viral", st, 1.51))

build("v1_viral", v1)
build("v2_parallax", v2)
build("v3_maxenergy", v3)
print("\nDONE. cut_v1_viral.mp4 / cut_v2_parallax.mp4 / cut_v3_maxenergy.mp4")
