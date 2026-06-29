"""WHOLE EW04 episode — comic framing over the existing animated clips ($0).
Editorial rhythm: heroes/pivots = FULL-FRAME; story beats = GRID templates.
Speech = red-letter bar (style C). Captions are terse comic accents; the audio
carries the full narration. Beats 8-10 (the gospel landing) REUSE clips as
placeholders — the visibly thin spot that proves where new stills/clips go."""
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import motion_comic as mc

EW = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\_style_poc\ew04")
ANIM = EW / "anim"
SCORED = EW / "cut" / "EW04_bronze_serpent_scored_captioned.mp4"
S = mc.S
OUT = S / "episode_comic.mp4"
PW, PH = 1080, 1920
INK = (18, 14, 8, 255)
FONT = mc.FONT

# grid geometry
PL = (34, 210, 526, 1886)
PR = (554, 210, 1046, 1886)
CW, CH = PL[2] - PL[0], PL[3] - PL[1]   # 492 x 1676

FILL = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1"
BOOM = "split[a][b];[b]reverse[rb];[a][rb]concat=n=2"


def A(stem):
    return str(ANIM / f"EW04__{stem}.mp4")


# ---------- PIL furniture (full-canvas RGBA PNGs) ----------
def _wrap(d, t, f, w):
    return mc._wrap(d, t, f, w)


def cap_top(text, fname, font_sz=50):
    img = Image.new("RGBA", (PW, PH), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT, font_sz); pad = 28
    lines = _wrap(d, text.upper(), font, PW - 80 - 2 * pad)
    lh = font_sz + 12; h = len(lines) * lh + 2 * pad
    d.rounded_rectangle([40, 38, PW - 40, 38 + h], radius=18,
                        fill=(245, 234, 208, 255), outline=INK, width=9)
    y = 38 + pad
    for ln in lines:
        d.text((40 + pad + 6, y), ln, font=font, fill=INK); y += lh
    img.save(S / fname); return S / fname


def cap_band(text, fname, font_sz=38):
    """sits in the top band above grid panels."""
    img = Image.new("RGBA", (PW, PH), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT, font_sz); pad = 20
    lines = _wrap(d, text.upper(), font, PW - 60 - 2 * pad)
    lh = font_sz + 8; h = len(lines) * lh + 2 * pad
    d.rounded_rectangle([30, 24, PW - 30, 24 + h], radius=12,
                        fill=(245, 234, 208, 255), outline=INK, width=7)
    y = 24 + pad
    for ln in lines:
        d.text((30 + pad + 4, y), ln, font=font, fill=INK); y += lh
    img.save(S / fname); return S / fname


def redletter_bar(text, speaker, ref, fname, font_sz=50):
    img = Image.new("RGBA", (PW, PH), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT, font_sz); tagf = ImageFont.truetype(FONT, 34)
    mx, pad = 46, 26
    lines = _wrap(d, text, font, PW - 2 * mx - 2 * pad)
    lh = font_sz + 12; bh = len(lines) * lh + 2 * pad
    top = PH - bh - 60
    tag = f"{speaker}  ·  {ref}"
    tw = d.textlength(tag, font=tagf)
    d.rounded_rectangle([mx, top - 56, mx + tw + 48, top + 6], radius=10,
                        fill=(150, 28, 24, 255), outline=INK, width=4)
    d.text((mx + 24, top - 48), tag, font=tagf, fill=(255, 248, 240, 255))
    d.rounded_rectangle([mx, top, PW - mx, top + bh], radius=16,
                        fill=(250, 248, 244, 255), outline=INK, width=7)
    y = top + pad
    for ln in lines:
        d.text((mx + pad, y), ln, font=font, fill=(150, 28, 24, 255)); y += lh
    img.save(S / fname); return S / fname


def border_frame(fname):
    img = Image.new("RGBA", (PW, PH), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    for r in (PL, PR):
        d.rectangle(r, outline=INK, width=11)
    img.save(S / fname); return S / fname


BF = border_frame("_ep_bframe.png")


def run(cmd, tag):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(f"ERR {tag}:", r.stderr[-600:]); raise SystemExit(1)


def clip_chain(label_in, label_out, dur):
    """fill, boomerang if needed, trim to dur."""
    boom = BOOM if dur > 4.9 else "null"
    return f"[{label_in}]{FILL},{boom},trim=duration={dur},setpts=PTS-STARTPTS[{label_out}]"


# ---------- segment builders ----------
def seg_full(out, clip, dur, furn_png, fade_st):
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", clip,
         "-loop", "1", "-framerate", "30", "-t", str(dur), "-i", str(furn_png),
         "-filter_complex",
         clip_chain("0:v", "v", dur) + ";"
         f"[1:v]format=rgba,fade=in:st={fade_st}:d=0.3:alpha=1[f];"
         f"[v][f]overlay=0:0,format=yuv420p[o]",
         "-map", "[o]", "-r", "30", "-c:v", "libx264", "-crf", "18",
         "-preset", "medium", str(out)], out.name)


def seg_grid_split(out, clip, dur, cap_png, fade_st):
    """one clip split into two facing panels (shot/reverse)."""
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", clip,
         "-f", "lavfi", "-i", f"color=c=0xFCF9F1:s={PW}x{PH}",
         "-loop", "1", "-framerate", "30", "-t", str(dur), "-i", str(BF),
         "-loop", "1", "-framerate", "30", "-t", str(dur), "-i", str(cap_png),
         "-filter_complex",
         clip_chain("0:v", "bm", dur) + ";"
         f"[bm]split[L][R];"
         f"[L]crop={CW}:{CH}:40:130[lc];"
         f"[R]crop={CW}:{CH}:548:130[rc];"
         f"[1:v]trim=duration={dur},setpts=PTS-STARTPTS[pp];"
         f"[pp][lc]overlay={PL[0]}:{PL[1]}[p1];"
         f"[p1][rc]overlay={PR[0]}:{PR[1]}[p2];"
         f"[p2][2:v]overlay=0:0[p3];"
         f"[3:v]format=rgba,fade=in:st={fade_st}:d=0.3:alpha=1[cf];"
         f"[p3][cf]overlay=0:0,format=yuv420p[o]",
         "-map", "[o]", "-r", "30", "-c:v", "libx264", "-crf", "18",
         "-preset", "medium", str(out)], out.name)


def seg_grid_two(out, clipL, clipR, dur, cap_png, fade_st):
    """two different clips, one per panel."""
    pscale = f"scale={CW}:{CH}:force_original_aspect_ratio=increase,crop={CW}:{CH},setsar=1"
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", clipL, "-i", clipR,
         "-f", "lavfi", "-i", f"color=c=0xFCF9F1:s={PW}x{PH}",
         "-loop", "1", "-framerate", "30", "-t", str(dur), "-i", str(BF),
         "-loop", "1", "-framerate", "30", "-t", str(dur), "-i", str(cap_png),
         "-filter_complex",
         f"[0:v]{pscale},{BOOM if dur>4.9 else 'null'},trim=duration={dur},setpts=PTS-STARTPTS[lc];"
         f"[1:v]{pscale},{BOOM if dur>4.9 else 'null'},trim=duration={dur},setpts=PTS-STARTPTS[rc];"
         f"[2:v]trim=duration={dur},setpts=PTS-STARTPTS[pp];"
         f"[pp][lc]overlay={PL[0]}:{PL[1]}[p1];"
         f"[p1][rc]overlay={PR[0]}:{PR[1]}[p2];"
         f"[p2][3:v]overlay=0:0[p3];"
         f"[4:v]format=rgba,fade=in:st={fade_st}:d=0.3:alpha=1[cf];"
         f"[p3][cf]overlay=0:0,format=yuv420p[o]",
         "-map", "[o]", "-r", "30", "-c:v", "libx264", "-crf", "18",
         "-preset", "medium", str(out)], out.name)


# ---------- beat schedule (t0, t1, layout, ...) ----------
BEATS = [
    (0.0,  8.2,  "TWO",   "01b_moses_close", "01_hook_moses",
     cap_band("My people were dying of snakebite.", "_b1.png")),
    (8.2,  14.8, "TWO",   "02_judgment_plague", "02b_serpents_spread",
     cap_band("The venom was the judgment our sin had earned.", "_b2.png")),
    (14.8, 18.6, "FULL",  "01b_moses_close",
     cap_top("I begged Him. He would not.", "_b3.png")),
    (18.6, 24.1, "TWO",   "03_bronze_lifted", "03b_serpent_atop_sky",
     cap_band("Forge the very thing killing us — and lift it high.", "_b4.png")),
    (24.1, 27.7, "FULL",  "04b_face_to_life",
     cap_top("The bitten had only to look — and live.", "_b5.png")),
    (27.7, 36.8, "SPLIT", "05_night_teacher",
     cap_band("From the far side of my life, the Teacher answered:", "_b6.png")),
    (36.8, 43.5, "FULL",  "05b_jesus_speaks",
     redletter_bar("And as Moses lifted up the serpent in the wilderness, "
                   "even so must the Son of man be lifted up.", "JESUS", "JOHN 3", "_b7.png")),
    # ---- gospel landing: NEW dedicated assets ----
    (43.5, 52.6, "FULL",  "06_cross_lifted",
     cap_top("They lifted Jesus on a Roman pole — bearing our judgment.", "_b8.png")),
    (52.6, 62.7, "FULL",  "08_bitten_multitude",
     cap_top("You who are bitten — that is every one of us.", "_b9.png")),
    (62.7, 68.12, "FULL", "07_risen_christ",
     cap_top("Lift your eyes to Jesus. Look, and live.", "_b10.png")),
]

segs = []
for i, b in enumerate(BEATS):
    t0, t1, kind = b[0], b[1], b[2]
    dur = round(t1 - t0, 3)
    out = S / f"_ep_seg{i:02d}.mp4"
    fade = 0.5 if i < 9 else 0.4
    if kind == "FULL":
        seg_full(out, A(b[3]), dur, b[4], fade)
    elif kind == "SPLIT":
        seg_grid_split(out, A(b[3]), dur, b[4], fade)
    elif kind == "TWO":
        seg_grid_two(out, A(b[3]), A(b[4]), dur, b[5], fade)
    segs.append(out)
    print(f"beat {i} [{t0}-{t1}] {kind} done", flush=True)

lst = S / "_ep_concat.txt"
lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in segs))
joined = S / "_ep_joined.mp4"
run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
     "-c", "copy", str(joined)], "concat")
run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(joined), "-i", str(SCORED),
     "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
     "-shortest", str(OUT)], "mux")
print("FINAL ->", OUT, flush=True)
