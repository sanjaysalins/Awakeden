"""Deterministic VIRAL HARD-CUT clip from ONE still — jump-cuts between static crops of the
REAL painted pixels ($0, zero hallucination, more faithful than Kling which re-paints crops).
Matches the Kling cut-plan look: image holds, then the FRAMING jumps. Optional tiny push per crop.

A crop = (zoom, cx, cy, dur, push). Hard cuts between crops (concat, no transitions)."""
import subprocess, tempfile, os, sys
from pathlib import Path
W, H, FPS = 1080, 1920, 30

def seg(png, crop, out):
    z, cx, cy, dur, push = crop
    d = max(2, int(round(dur * FPS)))
    base = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"
    z1 = z + push
    zexpr = f"{z}+({z1}-{z})*on/{d-1}"
    zp = (f"zoompan=z='{zexpr}':x='(iw-iw/zoom)*{cx}':y='(ih-ih/zoom)*{cy}'"
          f":d={d}:s={W}x{H}:fps={FPS}")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-loop","1","-i",str(png),
                    "-vf",f"{base},{zp},format=yuv420p","-t",f"{dur}","-r",str(FPS),
                    "-c:v","libx264","-pix_fmt","yuv420p",str(out)],check=True)

def build(png, out_mp4, crops):
    tmp = Path(tempfile.mkdtemp()); parts=[]
    for i,c in enumerate(crops):
        p=tmp/f"s{i}.mp4"; seg(png,c,p); parts.append(p)
    lst=tmp/"l.txt"; lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts),encoding="utf-8")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(lst),
                    "-c:v","libx264","-pix_fmt","yuv420p","-r",str(FPS),str(out_mp4)],check=True)
    for p in parts: os.remove(p)
    os.remove(lst); os.rmdir(tmp); print("SAVED",out_mp4)

if __name__=="__main__":
    NBP=Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\02_Psalm_22_Song_From_The_Cross\v1\shorts\06_The_Ends_Of_The_Earth\visual\nbp")
    OUT=Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\_hf_test")
    # (zoom, cx, cy, dur, push) — hard cuts between crops; tiny push for life
    # 03 cross: wide -> mid figure -> face -> nailed hand -> crowd/world below -> back wide
    crops03=[(1.02,0.50,0.45,0.9,0.04),(1.5,0.50,0.40,0.8,0.03),(2.7,0.50,0.20,0.8,0.04),
             (3.0,0.20,0.18,0.8,0.04),(1.7,0.50,0.82,0.8,0.03),(1.08,0.50,0.45,0.9,0.0)]
    # 10 tomb: wide -> doorway -> stone -> threshold/linen -> back wide
    crops10=[(1.02,0.50,0.45,0.9,0.04),(1.7,0.55,0.40,0.8,0.03),(2.4,0.30,0.45,0.8,0.04),
             (2.6,0.60,0.55,0.8,0.04),(1.08,0.50,0.45,0.9,0.0)]
    build(NBP/"03_all-the-ends-of-the-world.png", OUT/"03_ffhardcut.mp4", crops03)
    build(NBP/"10_the-empty-tomb.png", OUT/"10_ffhardcut.mp4", crops10)
