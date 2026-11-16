"""Living Comic 10s PROOF ($0). Piece 1, audio 17.2-27.6s.
Rules tested (panel r1 fixes): ink wake only on first + Jesus panel; ONE big panel; Jesus balloon <=8 words,
chained, plain 0.25s fade (no pop), on screen >= 1.2+0.25*words; decode card; no invented lines.
 .venv\Scripts\python.exe poc_comic_page/_living_proof/build_proof.py"""
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
H = Path(__file__).resolve().parent; P = H.parent / "_piece1"; F = H.parent / "_living_comic_design" / "fonts"
T0 = 17.2; DUR = 11.0
def run(c): subprocess.run(c, check=True)
# --- balloons (text, rel start, rel end) ---
B = [("All that the Father giveth me", 1.95, 8.4),
     ("shall come to me;", 2.94, 8.4),
     ("and him that cometh to me", 4.36, 8.4),
     ("I will in no wise cast out.", 5.4, 8.4)]
for t, s, e in B:
    w = len(t.split()); assert w <= 8 and e - s >= 1.2 + 0.25 * w - 1e-6, (t, e - s)
font = ImageFont.truetype(str(F / "Kalam-Bold.ttf"), 64); tabf = ImageFont.truetype(str(F / "Kalam-Bold.ttf"), 34)
IVORY = (250, 244, 226); GOLD = (214, 160, 40); INK = (20, 18, 16); OY = 40
for i, (t, s, e) in enumerate(B):
    img = Image.new("RGBA", (1080, 230), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((70, 10+OY, 1010, 170+OY), 56, fill=GOLD + (255,))
    d.rounded_rectangle((82, 22+OY, 998, 158+OY), 46, fill=IVORY + (255,), outline=INK + (255,), width=5)
    if i == 0:
        for txt, x in (("JESUS", 90), ("JOHN 6:37", 800)):
            tw = d.textlength(txt, font=tabf); d.rounded_rectangle((x, 4, x+tw+36, 56), 20, fill=GOLD + (255,), outline=INK + (255,), width=3)
            d.text((x+18, 6), txt, font=tabf, fill=INK + (255,))
    tw = d.textlength(t, font=font); d.text(((1080 - tw) / 2, 36+OY), t, font=font, fill=INK + (255,))
    img.save(H / f"b{i}.png")
# decode card in the balloon style (not a meme block)
card = Image.new("RGBA", (900, 330), (0,0,0,0)); d = ImageDraw.Draw(card)
d.rounded_rectangle((0,0,899,329), 60, fill=GOLD+(255,)); d.rounded_rectangle((14,14,885,315), 48, fill=IVORY+(255,), outline=INK+(255,), width=5)
cf = ImageFont.truetype(str(F / "Kalam-Bold.ttf"), 110)
for txt, y, col in (("IN NO WISE", 30, INK), ("= NEVER", 165, (176,120,10))):
    tw = d.textlength(txt, font=cf); d.text(((900-tw)/2, y), txt, font=cf, fill=col+(255,))
card.save(H / "card.png")
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
def seg(name, clip, sketch, dur, wake, still_hold, crop, flip=False):
    out = H / f"{name}.mp4"; src = pingpong(clip, dur)
    base = (f"[0:v]scale={crop}," + ("hflip," if flip else "") + f"fps=30,trim=0:{dur},setpts=PTS-STARTPTS,"
            "zoompan=z='1.02+0.0016*in':x='iw/2-(iw/zoom/2)+4*sin(in/9)':y='ih/2-(ih/zoom/2)+3*cos(in/11)':d=1:s=1080x1920:fps=30,format=gbrp[c];")
    if wake:
        fc = (base + "[1:v]scale=1080:1920," + ("hflip," if flip else "") + "fps=30,format=gbrp,eq=saturation=0.0:contrast=1.1[sk];"
              "[c][sk]blend=all_expr='if(lt(X*0.6+Y*0.4+30*sin(Y/45), T/0.5*(W*0.6+H*0.4)), A, B)'[o];[o]format=yuv420p[v]")
        ins = ["-i", str(src), "-loop", "1", "-framerate", "30", "-i", str(P / "stills_v2" / "_sketch" / sketch)]
    else:
        fc = base + "[c]format=yuv420p[v]"; ins = ["-i", str(src)]
    run(["ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", fc, "-map", "[v]", "-t", str(dur), "-c:v", "libx264", "-crf", "17", "-r", "30", str(out)])
    return out
s1 = seg("s1", "p2a.mp4", "p2a_sketch.png", 1.4, True, 2, "1080:1920")
s2 = seg("s2", "p2b.mp4", "p2b_sketch.png", 7.0, True, 6, "1080:-2,crop=1080:1920", flip=True)
s3 = seg("s3", "p2a.mp4", None, 2.6, False, 0, "1080:1920")
lst = H / 'l.txt'; lst.write_text(''.join('file ' + chr(39) + x.as_posix() + chr(39) + chr(10) for x in (s1, s2, s3)))
run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(H / "base.mp4")])
# light sweep band
from PIL import ImageFilter
band=Image.new("RGBA",(700,1920),(0,0,0,0)); ImageDraw.Draw(band).polygon([(250,0),(450,0),(250,1920),(50,1920)],fill=(255,226,150,70))
band.filter(ImageFilter.GaussianBlur(60)).save(H/"band.png")
# --- overlays + card + audio ---
ins = ["-i", str(H / "base.mp4")]; fc = ""; prev = "[0:v]"
n_in = 1
for i, (t, s, e) in enumerate(B):
    y = f"{1010+i*170-OY}+5*sin(2*PI*t/2.4+{i})"
    nxt = B[i+1][1] if i+1 < len(B) else None
    ins += ["-loop", "1", "-framerate", "30", "-t", str(DUR), "-i", str(H / f"b{i}.png")]
    fc += f"[{n_in}:v]format=rgba,fade=in:st={s}:d=0.25:alpha=1,fade=out:st={e-0.15}:d=0.15:alpha=1[b{i}];{prev}[b{i}]overlay=x=0:y='{y}':eof_action=pass" + (f":enable='lt(t,{nxt})'" if nxt else "") + f"[o{i}];"
    prev = f"[o{i}]"; n_in += 1
    if nxt:  # older balloon ghosts to 50% once the next arrives
        ins += ["-loop", "1", "-framerate", "30", "-t", str(DUR), "-i", str(H / f"b{i}.png")]
        fc += f"[{n_in}:v]format=rgba,colorchannelmixer=aa=0.5,fade=in:st={nxt}:d=0.2:alpha=1,fade=out:st={e-0.15}:d=0.15:alpha=1[g{i}];{prev}[g{i}]overlay=x=0:y='{y}':eof_action=pass:enable='gte(t,{nxt})'[og{i}];"
        prev = f"[og{i}]"; n_in += 1
ins += ["-loop","1","-framerate","30","-t",str(DUR),"-i",str(H/"band.png")]
bi=n_in; n_in+=1
fc += f"[{bi}:v]format=rgba[bd];{prev}[bd]overlay=x='-700+mod(t*260,1900)':y=0:eof_action=pass[ol];"; prev="[ol]"
ins += ["-loop","1","-framerate","30","-t",str(DUR),"-i",str(H/"card.png")]
fc += f"[{n_in}:v]format=rgba,fade=in:st=8.5:d=0.25:alpha=1[cd];{prev}[cd]overlay=x=90:y=1250:eof_action=pass[out]"; n_in += 1
run(["ffmpeg", "-y", "-v", "error", *ins, "-ss", str(T0), "-t", str(DUR), "-i", str(P / "_v4_hook" / "audio_v4.m4a"),
     "-filter_complex", fc, "-map", "[out]", "-map", f"{n_in}:a", "-t", str(DUR), "-c:v", "libx264", "-crf", "18",
     "-pix_fmt", "yuv420p", "-c:a", "aac", str(H / "LIVING_PROOF_10s_v3.mp4")])
print("done")
