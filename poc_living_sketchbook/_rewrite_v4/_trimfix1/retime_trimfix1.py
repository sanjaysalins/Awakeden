"""Moses and the snake on a pole -- trimfix1. NO reverse/boomerang/ping-pong/freeze/zoom fill. Every slot is covered by real forward clip footage
(trim only; a few slots at <=1.15x slow-mo, factor printed). Boundaries moved only inside narration silences / between words. Narration + score untouched.
s07 Moses close-up: only the first 1.75 s (clean) is used; the blue sports collar appears from ~1.9 s."""
import json, math, subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent; V4 = H.parent; ROOT = V4.parents[1]; SK = V4.parent
sys.path.insert(0, str(ROOT))
from pipeline.score_mix import AFMT, SIDECHAIN
HOLD = 3.0; W, HT, FPS = 1080, 1920, 30
# (clip, start, end, max_source_seconds_usable or None)
PLAN = [("s01_wide",0,4.3,None),("s02_grief",4.3,6.5,None),("s03_complaint",6.5,9.8,None),("s04_serpents",9.8,14.55,None),
 ("s05_intercession",14.55,17.85,None),("s06_forge",17.85,23.1,None),("s07_horizon",23.1,25.03,1.75),("s08_typology",25.03,32.0,None),
 ("s09_shadow",32.0,35.98,None),("s12_echo",35.98,41.7,None),("s10_golgotha",41.7,48.54,None),("s11_hearme",48.54,52.2,None),("s13_lifted",52.2,None,None)]
def run(c): subprocess.run(c, check=True)
def dur(p): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)],capture_output=True,text=True).stdout.strip())
aud = V4/"audio"/"bronze_serpent"/"narration.mp3"; al = json.load(open(V4/"audio"/"bronze_serpent"/"alignment.json"))
total = math.ceil((al[-1]["end"] + HOLD)*FPS - 1e-6)/FPS
tmp = H/"_t"; tmp.mkdir(exist_ok=True); segs = []; report = []
vf = f"scale={W}:{HT}:force_original_aspect_ratio=increase,crop={W}:{HT},fps={FPS},setsar=1,format=yuv420p"
for i,(shot,t0,t1,cap) in enumerate(PLAN):
    t1 = total if t1 is None else t1
    n = round(t1*FPS) - round(t0*FPS); d = n/FPS
    clip = SK/"bronze_serpent"/"clips"/f"{shot}.mp4"; cd = dur(clip)
    usable = min(cd, cap) if cap else cd
    f = max(1.0, d/usable)   # slow-mo factor (1.0 = pure trim)
    if f > 1.15 + 1e-6: sys.exit(f"FAIL {shot}: needs {f:.3f}x slow-mo (>1.15) slot {d:.2f} usable {usable:.2f}")
    report.append((shot, t0, t1, d, cd, usable, f)); print(f"{shot:18s} {t0:7.2f}-{t1:7.2f} slot {d:5.2f} clip {cd:5.2f} usable {usable:5.2f} slow {f:.3f}x")
    seg = tmp/f"s{i:02d}.mp4"
    if not seg.exists(): run(["ffmpeg","-y","-v","error","-i",str(clip),"-vf",(f"setpts={f:.5f}*PTS," if f>1 else "")+vf,"-frames:v",str(n),"-an","-threads","3","-c:v","libx264","-crf","17","-r",str(FPS),str(seg)])
    got = round(dur(seg)*FPS)
    if got < n: sys.exit(f"FAIL {shot}: only {got} frames of {n}")
    segs.append(seg)
(H/"plan_report.json").write_text(json.dumps(report, indent=1))
lst = tmp/"list.txt"; lst.write_text("".join(f"file '{s.as_posix()}'\n" for s in segs))
silent = tmp/"silent.mp4"; run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",str(lst),"-c","copy",str(silent)])
MUS = ROOT/"music_library"/"clips"/"lonely_searching_a.mp3"
filt = (f"[1:a]{AFMT},apad=whole_dur={total},asplit=2[main][key];"
        f"[2:a]{AFMT},atrim=0:{total},afade=t=in:st=0:d=1.5,afade=t=out:st={total-3:.2f}:d=3,volume=-11dB[m];"
        f"[m][key]sidechaincompress={SIDECHAIN}[md];[main][md]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix]")
out = H/"bronze_serpent_trimfix1_pre.mp4"
run(["ffmpeg","-y","-v","error","-i",str(silent),"-i",str(aud),"-stream_loop","-1","-i",str(MUS),"-filter_complex",filt,"-map","0:v","-map","[mix]","-c:v","copy","-c:a","aac","-b:a","192k","-t",str(total),str(out)])
print("total", total, "out", round(dur(out),3))
