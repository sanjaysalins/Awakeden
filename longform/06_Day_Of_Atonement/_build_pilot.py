"""Build the eyewitness-pilot TEST video for The Two Goats:
   Baroque stills slideshow (slow zoom, hard cuts) + the high-priest narration
   + a lonely->sacred score arc + a light SFX bed.  Output: _eyewitness_pilot/pilot_nocap.mp4
   (caption is a separate veed_io step). All $0 except the already-rendered voice."""
import subprocess, glob, os, tempfile, shutil, sys
from pathlib import Path

def run(cmd, **_ignore):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stdout.write("FFMPEG FAIL:\n" + " ".join(str(c) for c in cmd)[:300] + "\n")
        sys.stdout.write((r.stderr or "")[-1500:] + "\n"); sys.stdout.flush()
        raise SystemExit(1)
    return r

V1 = Path(__file__).resolve().parent / "v1"
VIS = V1 / "visual_16x9"
PILOT = V1 / "_eyewitness_pilot"
MUS = Path(__file__).resolve().parents[2] / "music_library" / "clips"
SFX = Path(__file__).resolve().parents[2] / "sound_library" / "clips"
NARR = PILOT / "narration.mp3"
AUD_DUR = float(subprocess.run(["ffprobe","-v","quiet","-show_entries","format=duration","-of","csv=p=0",str(NARR)],
                               capture_output=True,text=True).stdout.strip())

def png(n):  # find the PNG whose filename starts with the 2-digit scene number
    g = glob.glob(str(VIS / f"{n:02d}_*.png"))
    if not g: raise SystemExit(f"no PNG for scene {n}")
    return g[0]

# (scene, t0, t1) — slideshow timeline mapped to the narration beats
SEG = [(1,0.0,7.5),(3,7.5,15.7),(2,15.7,21.4),(6,21.4,28.5),(10,28.5,34.5),(11,34.5,39.6),
       (8,39.6,49.6),(14,49.6,55.5),(20,55.5,60.7),(12,60.7,69.1),(19,69.1,80.0),
       (21,80.0,88.0),(25,88.0,round(AUD_DUR,2))]

tmp = Path(tempfile.mkdtemp())
seglist = tmp / "segs.txt"
print(f"[visual] {len(SEG)} segments, audio {AUD_DUR:.1f}s")
with open(seglist,"w") as lf:
    for i,(sc,t0,t1) in enumerate(SEG):
        d = round(t1-t0,2)
        out = tmp / f"seg{i:02d}.mp4"
        frames = int(d*30)
        vf = ("scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,fps=30")
        run(["ffmpeg","-y","-loop","1","-t",str(d),"-i",png(sc),
                        "-vf",vf,"-c:v","libx264","-preset","ultrafast","-crf","23",
                        "-pix_fmt","yuv420p","-r","30","-t",str(d),str(out)])
        lf.write(f"file '{out.as_posix()}'\n")
        print(f"   S{sc} {d:.1f}s -> {out.name}")
silent = tmp / "silent.mp4"
run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(seglist),
                "-c:v","libx264","-pix_fmt","yuv420p","-r","30",str(silent)],
               check=True, capture_output=True)
print("[visual] concatenated")

# ---- audio mix: narration + score arc + sfx accents ----
def s(name, lib=SFX): return str(lib / f"{name}.mp3")
fc = (
 # score: lonely_searching -> sacred_grace_rise, crossfaded, ducked to ~-11dB
 f"[1:a]atrim=0:62,afade=t=in:st=0:d=2[lon];"
 f"[2:a]atrim=0:60,afade=t=in:st=0:d=2[sac];"
 f"[lon][sac]acrossfade=d=4[sc0];"
 f"[sc0]atrim=0:{AUD_DUR},volume=0.26,afade=t=out:st={AUD_DUR-3:.1f}:d=3[score];"
 # sfx beds/accents
 f"[3:a]atrim=0:22,volume=0.14,afade=t=out:st=19:d=3[a1];"            # hollow dread behind the veil
 f"[4:a]atrim=0:18,volume=0.20,adelay=33000|33000,afade=t=in:st=0:d=1,afade=t=out:st=15:d=3[a2];"  # wilderness wind
 f"[5:a]volume=0.55,adelay=54200|54200[a3];"                          # thunder on the veil-tear
 f"[6:a]volume=0.6,adelay=54600|54600[a4];"                          # low boom on the veil-tear
 f"[7:a]atrim=0:24,volume=0.16,adelay=87000|87000,afade=t=in:st=0:d=2[a5];"  # warm dawn on the CTA
 f"[0:a]volume=1.0[narr];"
 f"[narr][score][a1][a2][a3][a4][a5]amix=inputs=7:duration=first:normalize=0[mix]"
)
mixed = tmp / "mix.m4a"
run(["ffmpeg","-y","-i",str(NARR),"-i",s('lonely_searching_a',MUS),"-i",s('sacred_grace_rise_a',MUS),
                "-i",s('air_hollow_desolate'),"-i",s('wind_desert_bleak'),"-i",s('thunder_low_roll'),
                "-i",s('impact_low_boom'),"-i",s('dawn_morning_warm'),
                "-filter_complex",fc,"-map","[mix]","-c:a","aac","-b:a","192k",str(mixed)],
               check=True, capture_output=True)
print("[audio] mixed narration + score + sfx")

out = PILOT / "pilot_nocap.mp4"
run(["ffmpeg","-y","-i",str(silent),"-i",str(mixed),"-map","0:v","-map","1:a",
                "-c:v","copy","-c:a","aac","-b:a","192k","-shortest",str(out)],
               check=True, capture_output=True)
shutil.rmtree(tmp, ignore_errors=True)
print(f"[done] -> {out}")
