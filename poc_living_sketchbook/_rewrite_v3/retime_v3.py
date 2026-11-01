"""Re-time existing spreads to the LOCKED v3 narration ($0, ffmpeg only). Output: _rewrite_v3/video/<piece>_v3.mp4 (pre-watermark)."""
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
 "jericho": ("jericho", "lonely_searching_a.mp3", [("j01_walls",0),("j05_rahab",4.2),("j06_thread",13.1),("j02_feet",21.4),("j07_trumpets",25.0),("j08_stage_a",27.4),("j09_stage_b",28.8),("j10_stage_c",30.2),("j11_spared",31.8),("j12_line",44.5),("j13_landing",57.0)]),
 "two_goats": ("two_goats", "lonely_searching_a.mp3", [("g01_hook",0),("g02_bloodgoat",11.3),("g03_scapegoat",24.2),("g04_intodesert",31.6),("g05_onepay_onecarry",35.8),("g08_jesuspivot",43.2),("g09_isaiah536",47.4),("g10_finished",52.3),("g11_veil_whole",55.2),("g12_veil_tearing",57.8),("g13_veil_torn",59.4),("g14_landing",62.4)]),
 "bronze_serpent": ("bronze_serpent", "lonely_searching_a.mp3", [("s01_wide",0),("s02_grief",5.4),("s03_complaint",9.9),("s05_intercession",16.4),("s06_forge",20.0),("s04_serpents",24.8),("s07_horizon",28.5),("s08_typology",33.2),("s09_shadow",46.6),("s10_golgotha",49.5),("s11_hearme",56.4),("s13_lifted",60.5)]),
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
                run(["ffmpeg","-y","-v","error","-i",str(clip),"-vf",vf+",split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1:a=0","-an","-c:v","libx264","-crf","17",str(bm)])
            run(["ffmpeg","-y","-v","error","-stream_loop","-1","-i",str(bm),"-t",str(d),"-an","-c:v","libx264","-crf","17","-r",str(FPS),str(seg)])
        else:
            n = int(d*FPS)
            run(["ffmpeg","-y","-v","error","-loop","1","-i",str(still),"-t",str(d),"-vf",f"scale={W*2}:{HT*2}:force_original_aspect_ratio=increase,zoompan=z='1.0+0.05*on/{n}':d={n}:s={W}x{HT}:fps={FPS},format=yuv420p","-an","-c:v","libx264","-crf","17",str(seg)])
        segs.append(seg)
    lst = tmp/"list.txt"; lst.write_text("".join(f"file '{s.as_posix()}'\n" for s in segs))
    silent = tmp/"silent.mp4"
    run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",str(lst),"-c","copy",str(silent)])
    MUS = ROOT/"music_library"/"clips"/mus
    filt = (f"[1:a]{AFMT},apad=whole_dur={total},asplit=2[main][key];"
            f"[2:a]{AFMT},atrim=0:{total},afade=t=in:st=0:d=1.5,afade=t=out:st={total-3:.2f}:d=3,volume=-11dB[m];"
            f"[m][key]sidechaincompress={SIDECHAIN}[md];[main][md]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix]")
    out = OUTD/f"{name}_v3.mp4"
    run(["ffmpeg","-y","-v","error","-i",str(silent),"-i",str(aud),"-stream_loop","-1","-i",str(MUS),"-filter_complex",filt,"-map","0:v","-map","[mix]","-c:v","copy","-c:a","aac","-b:a","192k","-t",str(total),str(out)])
    print(name, out, round(dur(out),2), "video-audio diff", round(abs(dur(out)-total),2))
for n in (sys.argv[1:] or PLAN): build(n)
