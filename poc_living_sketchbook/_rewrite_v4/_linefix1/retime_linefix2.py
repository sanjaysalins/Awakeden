"""Jericho linefix2 re-time: linefix1 slot plan, but NO boomerang/loop of any kind. Every clip must be >= its slot (+offset); trim only, else FAIL.
New *_v2 Kling clips for j02/j06/j10/j11/j12/j13; the rest keep their original (already long enough) clips. Same narration, score, mix as linefix1.
Output: _linefix2/jericho_linefix2_pre.mp4"""
import json, math, subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent; V4 = H.parent; ROOT = V4.parents[1]
sys.path.insert(0, str(ROOT))
from pipeline.score_mix import AFMT, SIDECHAIN
SK = V4.parent
HOLD = 3.0; W, HT, FPS = 1080, 1920, 30
OLD = [("j01_walls",0),("j05_rahab",4.1),("j02_feet",10.1),("j06_thread",16.1),("j07_trumpets",21.7),("j08_stage_a",24.0),("j09_stage_b",24.8),("j10_stage_c",25.6),("j11_spared",26.8),("j06_thread",28.9),("j11_spared",33.1),("j12_line",38.6),("j13_landing",45.5)]
DELTA = 0.98
shots = [(s, (0 if i == 0 else (5.0 if i == 1 else round(t + DELTA, 3)))) for i, (s, t) in enumerate(OLD)]
NEW = {"j02_feet","j06_thread","j10_stage_c","j11_spared","j12_line","j13_landing"}
OFFSET = {9: 1.6, 10: 2.4}   # second use of j06 / j11 starts later in the clip (still trim only)
def run(c): subprocess.run(c, check=True)
def dur(p): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)],capture_output=True,text=True).stdout.strip())
aud = H/"narration_linefix1.wav"; al = json.load(open(H/"alignment_linefix1.json"))
total = math.ceil((al[-1]["end"] + HOLD) * FPS - 1e-6) / FPS
tmp = H/"_t2"; tmp.mkdir(exist_ok=True); segs = []
vf = f"scale={W}:{HT}:force_original_aspect_ratio=increase,crop={W}:{HT},fps={FPS},setsar=1,format=yuv420p"
for i,(shot,t0) in enumerate(shots):
    t1 = shots[i+1][1] if i+1 < len(shots) else total
    d = round(t1-t0, 3); seg = tmp/f"s{i:02d}.mp4"
    clip = SK/"jericho"/"clips"/(f"{shot}_v2.mp4" if shot in NEW else f"{shot}.mp4")
    off = OFFSET.get(i, 0.0); cd = dur(clip)
    print(f"slot {i:02d} {shot:14s} {t0:7.3f}-{t1:7.3f} d={d:6.3f} clip={cd:5.2f} off={off} {clip.name}")
    if cd + 0.02 < off + d: sys.exit(f"FAIL: clip shorter than slot (no boomerang/loop allowed): {clip}")
    run(["ffmpeg","-y","-v","error","-ss",str(off),"-i",str(clip),"-frames:v",str(round(t1*FPS)-round(t0*FPS)),"-vf",vf,"-an","-threads","3","-c:v","libx264","-crf","17","-r",str(FPS),str(seg)])
    segs.append(seg)
lst = tmp/"list.txt"; lst.write_text("".join(f"file '{s.as_posix()}'\n" for s in segs))
silent = tmp/"silent.mp4"
run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",str(lst),"-c","copy",str(silent)])
MUS = ROOT/"music_library"/"clips"/"lonely_searching_a.mp3"
filt = (f"[1:a]{AFMT},apad=whole_dur={total},asplit=2[main][key];"
        f"[2:a]{AFMT},atrim=0:{total},afade=t=in:st=0:d=1.5,afade=t=out:st={total-3:.2f}:d=3,volume=-11dB[m];"
        f"[m][key]sidechaincompress={SIDECHAIN}[md];[main][md]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix]")
out = H/"jericho_linefix2_pre.mp4"
run(["ffmpeg","-y","-v","error","-i",str(silent),"-i",str(aud),"-stream_loop","-1","-i",str(MUS),"-filter_complex",filt,"-map","0:v","-map","[mix]","-c:v","copy","-c:a","aac","-b:a","192k","-t",str(total),str(out)])
print("total", total, "out", round(dur(out),3))
