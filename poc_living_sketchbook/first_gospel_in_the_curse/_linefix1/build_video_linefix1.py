"""first_gospel_in_the_curse linefix1 video. D = -155 frames.
head (frames 0..122 = 4.1 s) rebuilt TRIM-ONLY: s01 = clip frames 0..59 (hook card 0-2.0 s, title card), s02 = clip frames 0..62.
middle = the pinned v5hook final, frames 278..1597 (old s03 .. s08b), untouched (its captions/cards already burned, now D earlier).
tail (frames 1443..1708 = 8.87 s) rebuilt TRIM-ONLY from the two landing clips: s09 frames 0..145, s10 frames 0..119.
Captions re-burned on head and tail from the new alignment. Total 1709 frames = 56.9667 s = last word end 53.963 + 3.0 s hold (ceil to frame)."""
import json, shutil, subprocess, sys
from pathlib import Path
from PIL import Image
H = Path(__file__).resolve().parent; FILM = H.parent; PS = FILM.parent; ROOT = PS.parent
sys.path.insert(0, str(PS)); sys.path.insert(0, str(FILM)); sys.path.insert(0, str(ROOT))
import _short_captions as C
import _s3b_titlecards as T
W, HT, FPS = 1080, 1920, 30
NH, MID0, MID1 = 123, 278, 1598
B1 = 60                         # s01 frames 0..59, s02 frames 60..122
S09_N = 146
TOTAL_F = 1709
TAIL_F = TOTAL_F - NH - (MID1 - MID0)       # 266
OLDF = FILM/"FIRSTGOSPELINTHECURSE_living_sketchbook_cc_scored_sfx_v5hook.mp4"
tmp = H/"_t"; shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir()
def run(c): subprocess.run(c, check=True)
def ext(name):
    d = tmp/name; d.mkdir()
    run(["ffmpeg","-y","-v","error","-i",str(FILM/"clips"/f"{name}.mp4"),"-vf",f"scale={W}:{HT}:force_original_aspect_ratio=increase,crop={W}:{HT}","-r",str(FPS),"-start_number","0",str(d/"f%05d.png")])
    return sorted(d.glob("f*.png"))
fr = {n: ext(n) for n in ("s01_hook_hands","s02_waiting_in_trees","s09_landing_transition","s10_landing_christ")}
for n, f in fr.items(): print(n, len(f), "clip frames")
assert len(fr["s01_hook_hands"]) >= B1 and len(fr["s02_waiting_in_trees"]) >= NH - B1                      # trim only
assert len(fr["s09_landing_transition"]) >= S09_N and len(fr["s10_landing_christ"]) >= TAIL_F - S09_N       # trim only
s02_t0 = B1/FPS; s03_t0 = NH/FPS
# cards: same shapes as the pinned film; title on s01 only, quote+citation over s02 (same relative timing as before)
CARDS = [(0.30, 1.90, "hilite", "THE FIRST GOSPEL\nIN THE CURSE.", 0.50, 0.09),
         (s02_t0+0.08, s03_t0-0.15, "quote", "AND I WILL PUT ENMITY\nBETWEEN THEE AND\nTHE WOMAN...", 0.50, 0.20),
         (s02_t0+0.30, s03_t0-0.15, "card", "GENESIS 3:15", 0.50, 0.40)]
cards = [(a,b,T.type_img(t, T.final_size(k), k),cx,cy) for a,b,k,t,cx,cy in CARDS]
hook = Image.open(H/"hook_card.png").convert("RGBA")
words = [w for w in json.load(open(H/"alignment_linefix1.json")) if any(ch.isalnum() for ch in w["w"])]
def overlay(f, img, cxf, cyf, k):
    s2 = 1.30-0.30*k
    oi = img.resize((int(img.width*s2), int(img.height*s2)), Image.LANCZOS)
    if k < 1.0: oi.putalpha(oi.split()[3].point(lambda v: int(v*k)))
    f.alpha_composite(oi, (int(W*cxf-oi.width/2), int(HT*cyf-oi.height/2)))
# ---- head
out = tmp/"head"; out.mkdir()
for i in range(NH):
    t = i/FPS
    f = Image.open(fr["s01_hook_hands"][i] if i < B1 else fr["s02_waiting_in_trees"][i-B1]).convert("RGBA")
    for (t0,t1,img,cxf,cyf) in cards:
        if t0 <= t <= t1: overlay(f, img, cxf, cyf, T.ease(min(1.0,(t-t0)/0.18)))
    if t < 2.0: f.alpha_composite(hook)
    f.convert("RGB").save(out/f"g{i:05d}.png")
aud = H/"narration_linefix1.wav"
headpre = tmp/"head_pre.mp4"
run(["ffmpeg","-y","-v","error","-framerate",str(FPS),"-i",str(out/"g%05d.png"),"-i",str(aud),"-map","0:v","-map","1:a","-c:v","libx264","-crf","17","-pix_fmt","yuv420p","-c:a","aac","-t",f"{NH/FPS}",str(headpre)])
hw = [w for w in words if w["end"] <= NH/FPS - 0.05]
print("head caption words:", " ".join(w["w"] for w in hw))
headcc = tmp/"head_cc.mp4"
C.burn(headpre, headcc, hw, [], tmp/"_cc_h")
# ---- tail
TAIL_T0 = (NH + MID1 - MID0)/FPS            # 48.1
out2 = tmp/"tail"; out2.mkdir()
for i in range(TAIL_F):
    src = fr["s09_landing_transition"][i] if i < S09_N else fr["s10_landing_christ"][i-S09_N]
    Image.open(src).convert("RGB").save(out2/f"g{i:05d}.png")
tw = [{"w":w["w"],"start":round(w["start"]-TAIL_T0,3),"end":round(w["end"]-TAIL_T0,3)} for w in words if w["start"] >= TAIL_T0-0.05]
print("tail caption words:", " ".join(w["w"] for w in tw))
tailpre = tmp/"tail_pre.mp4"
run(["ffmpeg","-y","-v","error","-framerate",str(FPS),"-i",str(out2/"g%05d.png"),"-ss",f"{TAIL_T0}","-i",str(aud),"-map","0:v","-map","1:a","-c:v","libx264","-crf","17","-pix_fmt","yuv420p","-c:a","aac","-t",f"{TAIL_F/FPS}",str(tailpre)])
tailcc = tmp/"tail_cc.mp4"
C.burn(tailpre, tailcc, tw, [], tmp/"_cc_t")
# ---- join
final_v = H/"video_linefix1_noaudio.mp4"
fc = (f"[0:v]fps={FPS},setsar=1,format=yuv420p,setpts=PTS-STARTPTS[a];"
      f"[1:v]trim=start_frame={MID0}:end_frame={MID1},setpts=PTS-STARTPTS,fps={FPS},setsar=1,format=yuv420p[b];"
      f"[2:v]fps={FPS},setsar=1,format=yuv420p,setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0[v]")
run(["ffmpeg","-y","-v","error","-i",str(headcc),"-i",str(OLDF),"-i",str(tailcc),"-filter_complex",fc,"-map","[v]","-an","-c:v","libx264","-crf","17","-pix_fmt","yuv420p","-r",str(FPS),str(final_v)])
print("ok", final_v)
