"""Living Comic 10s PROOF ($0). Piece 1, audio 17.2-27.6s.
Rules tested (panel r1 fixes): ink wake only on first + Jesus panel; ONE big panel; Jesus balloon <=8 words,
chained, plain 0.25s fade (no pop), on screen >= 1.2+0.25*words; decode card; no invented lines.
 .venv\Scripts\python.exe poc_comic_page/_living_proof/build_proof.py"""
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
H = Path(__file__).resolve().parent; P = H.parent / "_piece1"; F = H.parent / "_living_comic_design" / "fonts"
T0 = 17.2; DUR = 10.4
def run(c): subprocess.run(c, check=True)
# --- balloons (text, rel start, rel end) ---
B = [("All that the Father giveth me", 1.48, 8.5),
     ("shall come to me;", 2.94, 8.5),
     ("and him that cometh to me", 4.36, 8.5),
     ("I will in no wise cast out.", 5.5, 8.5)]
for t, s, e in B:
    w = len(t.split()); assert w <= 8 and e - s >= 1.2 + 0.25 * w - 1e-6, (t, e - s)
font = ImageFont.truetype(str(F / "Kalam-Bold.ttf"), 64)
IVORY = (250, 244, 226); GOLD = (214, 160, 40); INK = (20, 18, 16)
for i, (t, s, e) in enumerate(B):
    img = Image.new("RGBA", (1080, 190), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((70, 10, 1010, 170), 56, fill=GOLD + (255,))          # gold rule
    d.rounded_rectangle((82, 22, 998, 158), 46, fill=IVORY + (255,), outline=INK + (255,), width=5)
    if i == 0: d.polygon([(250, 22), (330, 22), (300, 0)], fill=IVORY + (255,), outline=INK + (255,))
    tw = d.textlength(t, font=font); d.text(((1080 - tw) / 2, 36), t, font=font, fill=INK + (255,))
    img.save(H / f"b{i}.png")
# --- panels ---
def pingpong(clip, dur):
    src = P / "clips" / clip; n = H / (Path(clip).stem + "_pp.mp4")
    d = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(src)],capture_output=True,text=True).stdout)
    if d >= dur: return src
    tail = H / "tail.mp4"; rev = H / "rev.mp4"
    run(["ffmpeg","-y","-v","error","-ss",f"{d-1.5:.3f}","-i",str(src),"-an","-c:v","libx264","-crf","14","-r","30",str(tail)])
    run(["ffmpeg","-y","-v","error","-i",str(tail),"-vf","reverse","-an","-c:v","libx264","-crf","14","-r","30",str(rev)])
    run(["ffmpeg","-y","-v","error","-i",str(src),"-r","30","-an","-c:v","libx264","-crf","14",str(H/"head.mp4")])
    seq=[H/"head.mp4"]
    while len(seq)<12: seq += [rev, tail]
    L=H/"pp.txt"; L.write_text("".join("file '" + x.as_posix() + "'" + chr(10) for x in seq))
    run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",str(L),"-c","copy",str(n)])
    return n
def seg(name, clip, sketch, dur, wake, still_hold, crop):
    out = H / f"{name}.mp4"; src = pingpong(clip, dur)
    base = (f"[0:v]scale={crop},fps=30,trim=0:{dur},setpts=PTS-STARTPTS,"
            "zoompan=z='1.02+0.0016*in':x='iw/2-(iw/zoom/2)+4*sin(in/9)':y='ih/2-(ih/zoom/2)+3*cos(in/11)':d=1:s=1080x1920:fps=30,format=gbrp[c];")
    if wake:
        fc = (base + "[1:v]scale=1080:1920,fps=30,format=gbrp,eq=saturation=0.0:contrast=1.1[sk];"
              "[c][sk]blend=all_expr='if(lt(X*0.6+Y*0.4+30*sin(Y/45), T/0.5*(W*0.6+H*0.4)), A, B)'[o];[o]format=yuv420p[v]")
        ins = ["-i", str(src), "-loop", "1", "-framerate", "30", "-i", str(P / "stills_v2" / "_sketch" / sketch)]
    else:
        fc = base + "[c]format=yuv420p[v]"; ins = ["-i", str(src)]
    run(["ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", fc, "-map", "[v]", "-t", str(dur), "-c:v", "libx264", "-crf", "17", "-r", "30", str(out)])
    return out
s1 = seg("s1", "p2a.mp4", "p2a_sketch.png", 1.4, True, 2, "1080:1920")
s2 = seg("s2", "p2b.mp4", "p2b_sketch.png", 9.0, True, 6, "1080:-2,crop=1080:1920")
lst = H / "l.txt"; lst.write_text(f"file '{s1.as_posix()}'\nfile '{s2.as_posix()}'\n")
run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(H / "base.mp4")])
# light sweep band
from PIL import ImageFilter
band=Image.new("RGBA",(700,1920),(0,0,0,0)); ImageDraw.Draw(band).polygon([(250,0),(450,0),(250,1920),(50,1920)],fill=(255,226,150,70))
band.filter(ImageFilter.GaussianBlur(60)).save(H/"band.png")
# --- overlays + card + audio ---
ins = ["-i", str(H / "base.mp4")]; fc = ""; prev = "[0:v]"
for i, (t, s, e) in enumerate(B):
    ins += ["-loop", "1", "-framerate", "30", "-t", str(DUR), "-i", str(H / f"b{i}.png")]
    fc += f"[{i+1}:v]format=rgba,fade=in:st={s}:d=0.25:alpha=1,fade=out:st={e-0.15}:d=0.15:alpha=1[b{i}];{prev}[b{i}]overlay=x=0:y='{1010+i*170}+5*sin(2*PI*t/2.4+{i})':eof_action=pass[o{i}];"
    prev = f"[o{i}]"
ins += ["-loop","1","-framerate","30","-t",str(DUR),"-i",str(H/"band.png")]
bi=len(B)+1
fc += f"[{bi}:v]format=rgba[bd];{prev}[bd]overlay=x='-700+mod(t*260,1900)':y=0:eof_action=pass[ol];"; prev="[ol]"
FI = "fontfile='C\:/Windows/Fonts/impact.ttf'"
def dt(tx, sz, col, y): return f"drawtext={FI}:text='{tx}':fontsize={sz}:fontcolor={col}:box=1:boxcolor=black@0.66:boxborderw=20:x=(w-text_w)/2:y={y}:enable='between(t,8.5,10.4)'"
fc += f"{prev}{dt('IN NO WISE',110,'white',1290)},{dt('= NEVER',130,'0xF2C14E',1440)}[out]"
run(["ffmpeg", "-y", "-v", "error", *ins, "-ss", str(T0), "-t", str(DUR), "-i", str(P / "_v4_hook" / "audio_v4.m4a"),
     "-filter_complex", fc, "-map", "[out]", "-map", f"{len(B)+2}:a", "-t", str(DUR), "-c:v", "libx264", "-crf", "18",
     "-pix_fmt", "yuv420p", "-c:a", "aac", str(H / "LIVING_PROOF_10s.mp4")])
print("done")
