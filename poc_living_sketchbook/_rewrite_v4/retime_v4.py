"""Re-time existing spreads to the LOCKED v4 narration ($0, ffmpeg only). Output: _rewrite_v4/video/<piece>_v4.mp4 (pre-watermark)."""
import json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline.score_mix import AFMT, SIDECHAIN
SK = Path(__file__).resolve().parents[1]; H = Path(__file__).resolve().parent
OUTD = H / "video"; OUTD.mkdir(exist_ok=True)
HOLD = 3.0; W, HT, FPS = 1080, 1920, 30
# (shot, start_s)  -- clip unless suffix ':still'
PLAN = {
 "jericho": ("jericho", "lonely_searching_a.mp3", [("j01_walls",0),("j05_rahab",4.1),("j02_feet",10.1),("j06_thread",16.1),("j07_trumpets",21.7),("j08_stage_a",24.0),("j09_stage_b",24.8),("j10_stage_c",25.6),("j11_spared",26.8),("j06_thread",28.9),("j11_spared",33.1),("j12_line",38.6),("j13_landing",45.5)]),
 "two_goats": ("two_goats", "lonely_searching_a.mp3", [("g01_hook",0),("g06_yearsasked",4.3),("g02_bloodgoat",10.1),("g03_scapegoat",19.3),("g04_intodesert",25.2),("g05_onepay_onecarry",29.7),("g07_bothhalves",31.8),("g08_jesuspivot",33.9),("g09_isaiah536",36.6),("g10_finished",38.8),("g11_veil_whole",40.3),("g12_veil_tearing",41.5),("g13_veil_torn",42.8),("g14_landing",45.7)]),
 "bronze_serpent": ("bronze_serpent", "lonely_searching_a.mp3", [("s01_wide",0),("s02_grief",5.1),("s03_complaint",6.7),("s04_serpents",8.9),("s05_intercession",14.0),("s06_forge",17.9),("s07_horizon",23.6),("s08_typology",27.9),("s09_shadow",33.4),("s12_echo",38.5),("s10_golgotha",42.6),("s11_hearme",44.8),("s13_lifted",50.6)]),
}
def run(c): subprocess.run(c, check=True)
def dur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)],capture_output=True,text=True).stdout.strip())
def build(name):
    folder, mus, shots = PLAN[name]
    aud = H/"audio"/name/"narration.mp3"; al = json.load(open(H/"audio"/name/"alignment.json"))
    total = round(al[-1]["end"] + HOLD, 2); total = int(total*FPS)/FPS
    tmp = OUTD/f"_{name}"; tmp.mkdir(exist_ok=True); segs = []
    vf = f"scale={W}:{HT}:force_original_aspect_ratio=increase,crop={W}:{HT},fps={FPS},setsar=1,format=yuv420p"
    for i,(shot,t0) in enumerate(shots):
        t1 = shots[i+1][1] if i+1 < len(shots) else total
        d = round(t1-t0, 3); seg = tmp/f"s{i:02d}.mp4"
        clip = SK/folder/"clips"/f"{shot}.mp4"; still = SK/folder/"stills"/f"{shot}.png"
        if clip.exists():
            bm = tmp/f"bm_{shot}.mp4"
            if not bm.exists():
                run(["ffmpeg","-y","-v","error","-i",str(clip),"-vf",vf+",split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1:a=0","-an","-threads","3","-c:v","libx264","-crf","17",str(bm)])
            run(["ffmpeg","-y","-v","error","-stream_loop","-1","-i",str(bm),"-t",str(d),"-an","-threads","3","-c:v","libx264","-crf","17","-r",str(FPS),str(seg)])
        else:
            n = int(d*FPS)
            run(["ffmpeg","-y","-v","error","-loop","1","-i",str(still),"-t",str(d),"-vf",f"scale={W*2}:{HT*2}:force_original_aspect_ratio=increase,zoompan=z='1.0+0.05*on/{n}':d={n}:s={W}x{HT}:fps={FPS},format=yuv420p","-an","-threads","3","-c:v","libx264","-crf","17",str(seg)])
        segs.append(seg)
    lst = tmp/"list.txt"; lst.write_text("".join(f"file '{s.as_posix()}'\n" for s in segs))
    silent = tmp/"silent.mp4"
    run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",str(lst),"-c","copy",str(silent)])
    MUS = ROOT/"music_library"/"clips"/mus
    filt = (f"[1:a]{AFMT},apad=whole_dur={total},asplit=2[main][key];"
            f"[2:a]{AFMT},atrim=0:{total},afade=t=in:st=0:d=1.5,afade=t=out:st={total-3:.2f}:d=3,volume=-11dB[m];"
            f"[m][key]sidechaincompress={SIDECHAIN}[md];[main][md]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix]")
    out = OUTD/f"{name}_v4.mp4"
    run(["ffmpeg","-y","-v","error","-i",str(silent),"-i",str(aud),"-stream_loop","-1","-i",str(MUS),"-filter_complex",filt,"-map","0:v","-map","[mix]","-c:v","copy","-c:a","aac","-b:a","192k","-t",str(total),str(out)])
    print(name, out, round(dur(out),2), "video-audio diff", round(abs(dur(out)-total),2))
for n in (sys.argv[1:] or PLAN): build(n)
