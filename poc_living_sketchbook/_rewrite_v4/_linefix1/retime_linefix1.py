"""Jericho linefix1 re-time: same chain as ../retime_v4.py (same shots/clips/music/mix), new narration + alignment.
Every shot after the first moves +0.98 s (new first sentence is 0.98 s longer). j01_walls is cut at 5.0 s (its clip is 5.04 s: trim only, no loop);
j05_rahab picks up at 5.0 s (clip 8.04 s, slot 6.08 s: trim only). Landing hold >= 3.0 s (ceil to the frame). Output: _linefix1/jericho_linefix1_pre.mp4 (no captions yet)."""
import json, math, shutil, subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent; V4 = H.parent; ROOT = V4.parents[1]
sys.path.insert(0, str(ROOT))
from pipeline.score_mix import AFMT, SIDECHAIN
SK = V4.parent
HOLD = 3.0; W, HT, FPS = 1080, 1920, 30
OLD = [("j01_walls",0),("j05_rahab",4.1),("j02_feet",10.1),("j06_thread",16.1),("j07_trumpets",21.7),("j08_stage_a",24.0),("j09_stage_b",24.8),("j10_stage_c",25.6),("j11_spared",26.8),("j06_thread",28.9),("j11_spared",33.1),("j12_line",38.6),("j13_landing",45.5)]
DELTA = 0.98
shots = [(s, (0 if i == 0 else (5.0 if i == 1 else round(t + DELTA, 3)))) for i, (s, t) in enumerate(OLD)]
def run(c): subprocess.run(c, check=True)
def dur(p): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)],capture_output=True,text=True).stdout.strip())
aud = H/"narration_linefix1.wav"; al = json.load(open(H/"alignment_linefix1.json"))
total = math.ceil((al[-1]["end"] + HOLD) * FPS - 1e-6) / FPS
tmp = H/"_t"; tmp.mkdir(exist_ok=True); segs = []
vf = f"scale={W}:{HT}:force_original_aspect_ratio=increase,crop={W}:{HT},fps={FPS},setsar=1,format=yuv420p"
for i,(shot,t0) in enumerate(shots):
    t1 = shots[i+1][1] if i+1 < len(shots) else total
    d = round(t1-t0, 3); seg = tmp/f"s{i:02d}.mp4"
    clip = SK/"jericho"/"clips"/f"{shot}.mp4"
    bm = tmp/f"bm_{shot}.mp4"
    if not bm.exists():
        old_bm = V4/"video"/"_jericho"/f"bm_{shot}.mp4"
        if old_bm.exists(): shutil.copy(old_bm, bm)
        else: run(["ffmpeg","-y","-v","error","-i",str(clip),"-vf",vf+",split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1:a=0","-an","-threads","3","-c:v","libx264","-crf","17",str(bm)])
    cd = dur(clip); loops = d > cd + 0.02
    print(f"slot {i:02d} {shot:14s} {t0:7.3f}-{t1:7.3f} d={d:6.3f} clip={cd:5.2f} {'LOOP(boomerang)' if loops else 'trim only'}")
    run(["ffmpeg","-y","-v","error","-stream_loop","-1","-i",str(bm),"-t",str(d),"-an","-threads","3","-c:v","libx264","-crf","17","-r",str(FPS),str(seg)])
    segs.append(seg)
lst = tmp/"list.txt"; lst.write_text("".join(f"file '{s.as_posix()}'\n" for s in segs))
silent = tmp/"silent.mp4"
run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",str(lst),"-c","copy",str(silent)])
MUS = ROOT/"music_library"/"clips"/"lonely_searching_a.mp3"
filt = (f"[1:a]{AFMT},apad=whole_dur={total},asplit=2[main][key];"
        f"[2:a]{AFMT},atrim=0:{total},afade=t=in:st=0:d=1.5,afade=t=out:st={total-3:.2f}:d=3,volume=-11dB[m];"
        f"[m][key]sidechaincompress={SIDECHAIN}[md];[main][md]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix]")
out = H/"jericho_linefix1_pre.mp4"
run(["ffmpeg","-y","-v","error","-i",str(silent),"-i",str(aud),"-stream_loop","-1","-i",str(MUS),"-filter_complex",filt,"-map","0:v","-map","[mix]","-c:v","copy","-c:a","aac","-b:a","192k","-t",str(total),str(out)])
print("total", total, "out", round(dur(out),3))
