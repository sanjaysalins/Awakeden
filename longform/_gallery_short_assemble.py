"""Assemble the full EW01 punchy short from the 8 gallery clips: concat -> SPEED-TO-FIT the
video to the 74.7s VO (overshoot->compress = punch) -> narration + dread->hope music arc ->
kinetic captions. $0 (ffmpeg + offline captions)."""
import subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SHORT = ROOT / "longform/EW01_Two_Goats/v1/short"
CLIPS = SHORT / "gallery_clips"
VO = SHORT / "narration.mp3"
SPOKEN = SHORT / "narration.spoken.txt"
ML = ROOT / "music_library/clips"
T = CLIPS / "_t"; T.mkdir(exist_ok=True)
NORM = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1"

def run(c): subprocess.run(c, check=True)
def dur(f):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","default=nk=1:nw=1",str(f)],capture_output=True,text=True).stdout.strip())

ORDER = ["01_hook.mp4","02_overview.mp4","03_two_goats.mp4","04_blood_veil.mp4",
         "05_confess.mp4","06_scapegoat.mp4","07_turn.mp4","08_punch.mp4"]
clips = [CLIPS/c for c in ORDER if (CLIPS/c).exists()]
print(f"{len(clips)}/{len(ORDER)} clips present")

# 1. normalize + concat
norm = []
for i, c in enumerate(clips):
    o = T/f"n{i:02d}.mp4"
    run(["ffmpeg","-y","-loglevel","error","-i",str(c),"-vf",NORM,"-an","-c:v","libx264",
         "-pix_fmt","yuv420p","-preset","veryfast",str(o)]); norm.append(o)
lf = T/"list.txt"; lf.write_text("".join(f"file '{f.as_posix()}'\n" for f in norm),encoding="utf-8")
silent = T/"concat.mp4"
run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(lf),"-c","copy",str(silent)])

# 2. speed-to-fit the VO length
VOL = dur(VO); VID = dur(silent); factor = VID/VOL
sped = T/"sped.mp4"
run(["ffmpeg","-y","-loglevel","error","-i",str(silent),"-vf",f"setpts=PTS/{factor:.5f},fps=30",
     "-an","-c:v","libx264","-pix_fmt","yuv420p","-preset","veryfast",str(sped)])
print(f"video {VID:.1f}s -> {VOL:.1f}s (sped {factor:.2f}x)")

# 3. dread->hope music arc: lonely_searching -> sacred_grace_rise, looped/trimmed to VO len
bed = T/"bed.mp3"
run(["ffmpeg","-y","-loglevel","error","-i",str(ML/"lonely_searching_a.mp3"),
     "-i",str(ML/"sacred_grace_rise_a.mp3"),"-filter_complex",
     "[0:a][1:a]acrossfade=d=3:c1=tri:c2=tri[arc]","-map","[arc]",str(T/"arc.mp3")])
run(["ffmpeg","-y","-loglevel","error","-stream_loop","-1","-i",str(T/"arc.mp3"),
     "-t",f"{VOL+1:.2f}","-c","copy",str(bed)])

# 4. mux narration (0dB) + music (-14dB)
muxed = CLIPS/"ew01_short_nocap.mp4"
run(["ffmpeg","-y","-loglevel","error","-i",str(sped),"-i",str(VO),"-i",str(bed),
     "-filter_complex","[1:a]volume=1.0[vo];[2:a]volume=0.18[mu];[vo][mu]amix=inputs=2:duration=first[a]",
     "-map","0:v","-map","[a]","-t",f"{VOL:.2f}","-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac",str(muxed)])
print(f"[muxed] {muxed}")

# 5. kinetic captions (run from repo root)
out = CLIPS/"ew01_short.mp4"
print("[caption] impact ...")
r = subprocess.run([str(ROOT/".venv/Scripts/python.exe"),"-m","veed_io.caption","--video",str(muxed),
     "--script",str(SPOKEN),"--style","impact","--out",str(out)],cwd=str(ROOT),
     capture_output=True,text=True)
print(r.stdout[-300:] if r.returncode==0 else "CAPTION FAIL:\n"+r.stderr[-400:])
print(f"\nDONE -> {out if out.exists() else muxed}")
