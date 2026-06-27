"""EW01 short v2 — tighter racing middle + breathing Christ close + flame fix.
Each fast clip's 10s tour is compressed into a shorter window (faster internal cuts);
07_turn is trimmed to drop the flame tail; the punch holds + lands on the risen Christ.
$0 (ffmpeg + offline captions)."""
import subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SHORT = ROOT / "longform/EW01_Two_Goats/v1/short"
CLIPS = SHORT / "gallery_clips"
CHRIST = SHORT / "visual_9x16_test/christ.png"
VO = SHORT / "narration.mp3"
SPOKEN = SHORT / "narration.spoken.txt"
ML = ROOT / "music_library/clips"
T = CLIPS / "_t2"; T.mkdir(exist_ok=True)
NORM = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1"

def run(c): subprocess.run(c, check=True)
def dur(f): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
    "-of","default=nk=1:nw=1",str(f)],capture_output=True,text=True).stdout.strip())

# (clip, seconds of source to use, screen-time window).  Fast middle, breathing close.
SEGS = [
 ("01_hook.mp4",     10.0, 7.5),
 ("02_overview.mp4", 10.0, 6.5),
 ("03_two_goats.mp4",10.0, 7.0),
 ("04_blood_veil.mp4",10.0,7.0),
 ("05_confess.mp4",  10.0, 7.0),
 ("06_scapegoat.mp4",10.0, 7.0),
 ("07_turn.mp4",      9.0, 11.0),   # trim flame tail (use 0-9s), let the gospel turn breathe
 ("08_punch.mp4",     6.0, 6.0),    # only 0-6s (wide->face->hand); drops the invented flame at ~7s
]
HOLD = 10.9   # breathing hold on the risen Christ (still) for the CTA landing

segfiles = []
for i, (clip, src, win) in enumerate(SEGS):
    src = min(src, dur(CLIPS/clip))
    factor = src / win                      # <1 => speed up (tighter); >1 => slow (breathe)
    o = T/f"s{i:02d}.mp4"
    run(["ffmpeg","-y","-loglevel","error","-t",f"{src}","-i",str(CLIPS/clip),
         "-vf",f"{NORM},setpts=PTS*{win/src:.5f}","-an","-c:v","libx264","-pix_fmt","yuv420p",
         "-preset","veryfast",str(o)])
    segfiles.append(o)
# breathing Christ hold (LIVING christ — locked camera, soft light glow, no flame)
LIVING = CLIPS/"living_christ.mp4"
hold = T/"hold.mp4"
ld = dur(LIVING)
run(["ffmpeg","-y","-loglevel","error","-i",str(LIVING),
     "-vf",f"{NORM},setpts=PTS*{HOLD/ld:.5f}","-an","-c:v","libx264","-pix_fmt","yuv420p","-r","30",str(hold)])
segfiles.append(hold)

lf = T/"list.txt"; lf.write_text("".join(f"file '{f.as_posix()}'\n" for f in segfiles),encoding="utf-8")
silent = T/"silent.mp4"
run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(lf),"-c","copy",str(silent)])
VID = dur(silent); VOL = dur(VO)
print(f"video {VID:.1f}s  vo {VOL:.1f}s")

# music arc dread->hope
run(["ffmpeg","-y","-loglevel","error","-i",str(ML/"lonely_searching_a.mp3"),
     "-i",str(ML/"sacred_grace_rise_a.mp3"),"-filter_complex",
     "[0:a][1:a]acrossfade=d=3:c1=tri:c2=tri[arc]","-map","[arc]",str(T/"arc.mp3")])
bed = T/"bed.mp3"
run(["ffmpeg","-y","-loglevel","error","-stream_loop","-1","-i",str(T/"arc.mp3"),"-t",f"{VOL+1:.2f}","-c","copy",str(bed)])

muxed = CLIPS/"ew01_short_v2_nocap.mp4"
run(["ffmpeg","-y","-loglevel","error","-i",str(silent),"-i",str(VO),"-i",str(bed),
     "-filter_complex","[1:a]volume=1.0[vo];[2:a]volume=0.18[mu];[vo][mu]amix=inputs=2:duration=first[a]",
     "-map","0:v","-map","[a]","-t",f"{VOL:.2f}","-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac",str(muxed)])

out = CLIPS/"ew01_short_v2.mp4"
print("[caption] impact ...")
r = subprocess.run([str(ROOT/".venv/Scripts/python.exe"),"-m","veed_io.caption","--video",str(muxed),
     "--script",str(SPOKEN),"--style","impact","--out",str(out)],cwd=str(ROOT),capture_output=True,text=True)
print(r.stdout[-200:] if r.returncode==0 else "CAPTION FAIL:\n"+r.stderr[-300:])
print(f"\nDONE -> {out if out.exists() else muxed}")
