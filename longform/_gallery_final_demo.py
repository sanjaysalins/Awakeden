"""Assemble the COMPLETE gallery grammar: full-res living-painting WIDE bookends + the
winning V2 (timecoded) model hard-cut tour + hook VO + music. Two outputs: natural, and a
speed-to-fit 'punch' version (video compressed to the VO length, VO stays natural). $0."""
import subprocess
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "longform/EW01_Two_Goats/v1/short/visual_9x16_test/gallery_demo"
LIVING = D / "living_whole.mp4"
TOUR = D / "bakeoff_v2_timecoded.mp4"
VO = D.parent / "variants" / "vo_slice.mp3"
MUSIC = Path(__file__).resolve().parent.parent / "music_library/clips/lonely_searching_a.mp3"
T = D / "_t"; T.mkdir(exist_ok=True)
NORM = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1"

def run(c): subprocess.run(c, check=True)

# wide bookends from the living painting (full frame, alive), + the tour
def seg(src, ss, dur, out):
    run(["ffmpeg","-y","-loglevel","error","-ss",str(ss),"-i",str(src),"-t",str(dur),
         "-vf",NORM,"-an","-c:v","libx264","-pix_fmt","yuv420p","-preset","veryfast",str(out)])
def norm(src, out):
    run(["ffmpeg","-y","-loglevel","error","-i",str(src),"-vf",NORM,"-an",
         "-c:v","libx264","-pix_fmt","yuv420p","-preset","veryfast",str(out)])

seg(LIVING, 0.0, 1.3, T/"open.mp4")
norm(TOUR, T/"tour.mp4")
seg(LIVING, 3.2, 1.3, T/"close.mp4")

listf = T/"list.txt"
listf.write_text(f"file '{(T/'open.mp4').as_posix()}'\nfile '{(T/'tour.mp4').as_posix()}'\nfile '{(T/'close.mp4').as_posix()}'\n", encoding="utf-8")
silent = D/"_grammar_silent.mp4"
run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(listf),"-c","copy",str(silent)])

import json
def dur(f):
    o = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",str(f)],capture_output=True,text=True).stdout.strip()
    return float(o)
VID = dur(silent)
bed = D/"_bed2.mp3"
run(["ffmpeg","-y","-loglevel","error","-stream_loop","-1","-i",str(MUSIC),"-t",str(VID+2),"-c","copy",str(bed)])

def mux(video, vo_len, out):
    run(["ffmpeg","-y","-loglevel","error","-i",str(video),"-i",str(VO),"-i",str(bed),
         "-filter_complex",f"[1:a]atrim=0:{vo_len:.2f},volume=1.0[vo];[2:a]volume=0.16[mu];[vo][mu]amix=inputs=2:duration=first[a]",
         "-map","0:v","-map","[a]","-t",f"{vo_len:.2f}","-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac",str(out)])

# natural: VO matches video length
mux(silent, VID, D/"gallery_final.mp4")

# punch: speed video to fit a 10.5s VO slot (overshoot -> compress = punch); VO stays natural
PUNCH = 10.5
factor = VID / PUNCH
punch_silent = D/"_grammar_punch.mp4"
run(["ffmpeg","-y","-loglevel","error","-i",str(silent),"-vf",f"setpts=PTS/{factor:.4f},fps=30","-an",
     "-c:v","libx264","-pix_fmt","yuv420p","-preset","veryfast",str(punch_silent)])
mux(punch_silent, PUNCH, D/"gallery_final_punch.mp4")
print(f"natural={VID:.1f}s  punch={PUNCH}s (video sped {factor:.2f}x)")
print("DONE: gallery_final.mp4  +  gallery_final_punch.mp4")
