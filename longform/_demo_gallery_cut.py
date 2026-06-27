"""Build the 10s GALLERY HARD-CUT demo: place the camera at fixed framings on the living
painting and HARD-CUT between them (no slow zoom/pan), fast, with the hook VO + music.
Crops are taken from living_whole.mp4 so every framing carries the ambient life (smoke/
flame) where it exists, still elsewhere. $0 (ffmpeg)."""
import subprocess
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "longform/EW01_Two_Goats/v1/short/visual_9x16_test/gallery_demo"
LIVING = D / "living_whole.mp4"
VO = D.parent / "variants" / "vo_slice.mp3"
MUSIC = Path(__file__).resolve().parent.parent / "music_library/clips/lonely_searching_a.mp3"
SEG = D / "_seg"; SEG.mkdir(exist_ok=True)

# framing boxes (normalized x,y,w,h) verified on boxes_strip2.png
BOX = {
 "whole":     (0.0, 0.0, 1.0, 1.0),
 "veil":      (0.00, 0.00, 0.20, 0.32),
 "scapegoat": (0.34, 0.14, 0.28, 0.14),
 "altar":     (0.34, 0.30, 0.32, 0.22),
 "twogoats":  (0.16, 0.50, 0.42, 0.23),
 "basin":     (0.00, 0.55, 0.30, 0.20),
 "priest":    (0.58, 0.50, 0.40, 0.38),
 "face":      (0.70, 0.52, 0.26, 0.20),
 "lamp":      (0.35, 0.82, 0.30, 0.15),
}
# eye-tour: whole -> witness -> the act -> the riddle -> back to whole. (name, dur, src_offset)
TOUR = [
 ("whole", 1.3, 0.0), ("face", 1.1, 0.5), ("twogoats", 1.0, 1.0), ("altar", 1.0, 1.5),
 ("basin", 0.9, 2.0), ("veil", 0.9, 0.8), ("scapegoat", 0.9, 2.5), ("lamp", 1.0, 3.0),
 ("priest", 1.1, 1.2), ("whole", 1.3, 3.5),
]
TOTAL = sum(d for _, d, _ in TOUR)

def run(c): subprocess.run(c, check=True)

files = []
for i, (name, dur, off) in enumerate(TOUR):
    x, y, w, h = BOX[name]
    vf = (f"crop=iw*{w}:ih*{h}:iw*{x}:ih*{y},"
          "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1")
    out = SEG / f"{i:02d}_{name}.mp4"
    run(["ffmpeg","-y","-loglevel","error","-stream_loop","-1","-ss",str(off),"-i",str(LIVING),
         "-t",str(dur),"-vf",vf,"-an","-c:v","libx264","-pix_fmt","yuv420p","-preset","veryfast",str(out)])
    files.append(out)

listf = SEG / "list.txt"
listf.write_text("".join(f"file '{f.as_posix()}'\n" for f in files), encoding="utf-8")
silent = D / "_silent.mp4"
run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(listf),"-c","copy",str(silent)])

bed = D / "_bed.mp3"
run(["ffmpeg","-y","-loglevel","error","-stream_loop","-1","-i",str(MUSIC),"-t",str(TOTAL+1),"-c","copy",str(bed)])

out = D / "gallery_demo.mp4"
run(["ffmpeg","-y","-loglevel","error","-i",str(silent),"-i",str(VO),"-i",str(bed),
     "-filter_complex","[1:a]atrim=0:%.2f,volume=1.0[vo];[2:a]volume=0.16[mu];[vo][mu]amix=inputs=2:duration=first[a]" % TOTAL,
     "-map","0:v","-map","[a]","-t",str(TOTAL),"-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac",str(out)])
print(f"[gallery] {out}  ({TOTAL:.1f}s, {len(TOUR)} shots, {len(TOUR)-1} hard cuts)")
