"""god_hung_up_a_snake linefix1 video: rebuild ONLY the head (frames 0..225 = old s01+s02 slots, up to the hard cut into s03),
trim-only (no loop / ping-pong): s01 = clip frames 0..110, s02 = clip frames 0..114. Title cards + captions re-burned from the NEW alignment.
Tail = the pinned v5hook final from frame 243 (its s03 start) to the end, untouched (video re-encoded once, crf 17)."""
import json, shutil, subprocess, sys
from pathlib import Path
from PIL import Image
H = Path(__file__).resolve().parent; FILM = H.parent; PS = FILM.parent; ROOT = PS.parent
sys.path.insert(0, str(PS)); sys.path.insert(0, str(FILM)); sys.path.insert(0, str(ROOT))
import _short_captions as C
import _s3b_titlecards as T
W, HT, FPS = 1080, 1920, 30
B1, N = 111, 226            # s01 = frames 0..110, s02 = frames 111..225; tail old frame 243 -> new frame 226
OLDF = FILM/"GODHUNGUPASNAKE_living_sketchbook_cc_scored_sfx_v5hook.mp4"
tmp = H/"_t"; shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir()
fr = {}
for name in ("s01_hook", "s02_pole_reveal"):
    d = tmp/name; d.mkdir()
    subprocess.run(["ffmpeg","-y","-v","error","-i",str(FILM/"clips"/f"{name}.mp4"),"-vf",f"scale={W}:{HT}:force_original_aspect_ratio=increase,crop={W}:{HT}","-r",str(FPS),"-start_number","0",str(d/"f%05d.png")],check=True)
    fr[name] = sorted(d.glob("f*.png")); print(name, len(fr[name]), "clip frames")
assert len(fr["s01_hook"]) >= B1 and len(fr["s02_pole_reveal"]) >= N - B1   # trim only
s02_t0 = B1/FPS; s03_t0 = N/FPS
CARDS = [(0.34, s02_t0-0.438, "hilite", "GOD HUNG UP A SNAKE.", 0.50, 0.09),
         (s02_t0+0.222, s03_t0-0.162, "quote", "AND MOSES MADE A SERPENT\nOF BRASS, AND PUT IT\nUPON A POLE.", 0.50, 0.20),
         (s02_t0+0.562, s03_t0-0.162, "card", "NUMBERS 21:9", 0.50, 0.44)]
cards = [(a,b,T.type_img(t, T.final_size(k), k),cx,cy) for a,b,k,t,cx,cy in CARDS]
out = tmp/"grid"; out.mkdir()
for i in range(N):
    t = i/FPS
    f = Image.open(fr["s01_hook"][i] if i < B1 else fr["s02_pole_reveal"][i-B1]).convert("RGBA")
    for (t0,t1,img,cxf,cyf) in cards:
        if t0 <= t <= t1:
            k = T.ease(min(1.0, (t-t0)/0.18)); s2 = 1.30-0.30*k
            oi = img.resize((int(img.width*s2), int(img.height*s2)), Image.LANCZOS)
            if k < 1.0: oi.putalpha(oi.split()[3].point(lambda v: int(v*k)))
            f.alpha_composite(oi, (int(W*cxf-oi.width/2), int(HT*cyf-oi.height/2)))
    f.convert("RGB").save(out/f"g{i:05d}.png")
head_dur = N/FPS
nw = [w for w in json.load(open(H/"alignment_linefix1.json")) if w["end"] <= 7.3]
print("head caption words:", " ".join(w["w"] for w in nw))
headpre = tmp/"head_pre.mp4"
subprocess.run(["ffmpeg","-y","-v","error","-framerate",str(FPS),"-i",str(out/"g%05d.png"),"-i",str(H/"narration_linefix1.wav"),"-map","0:v","-map","1:a","-c:v","libx264","-crf","17","-pix_fmt","yuv420p","-c:a","aac","-t",f"{head_dur}",str(headpre)],check=True)
headcc = tmp/"head_cc.mp4"
C.burn(headpre, headcc, [{"w":w["w"],"start":w["start"],"end":w["end"]} for w in nw], [], tmp/"_cc")
final_v = H/"video_linefix1_noaudio.mp4"
fc = (f"[0:v]fps={FPS},setsar=1,format=yuv420p,setpts=PTS-STARTPTS[a];"
      f"[1:v]trim=start_frame=243,setpts=PTS-STARTPTS,fps={FPS},setsar=1,format=yuv420p[b];[a][b]concat=n=2:v=1:a=0[v]")
subprocess.run(["ffmpeg","-y","-v","error","-i",str(headcc),"-i",str(OLDF),"-filter_complex",fc,"-map","[v]","-an","-c:v","libx264","-crf","17","-pix_fmt","yuv420p","-r",str(FPS),str(final_v)],check=True)
print("ok", final_v)
