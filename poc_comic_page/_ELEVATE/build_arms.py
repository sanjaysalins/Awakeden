"""ELEVATE bake-off, $0. Builds arms A (today), B ($0 stack), C (B + story order) for the opening ~31s of Mockers.
  .venv\\Scripts\\python.exe poc_comic_page/_ELEVATE/build_arms.py
Same stills/clips, same voice+score audio. Only the lever under test changes."""
import subprocess, math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
HERE = Path(__file__).resolve().parent; ROOT = HERE.parent.parent
CLIPS = ROOT / "batches/cluster_01_cross/mockers_words_ps227/visual/clips"
FILM = ROOT / "batches/cluster_01_cross/mockers_words_ps227/visual/mockers_words_ps227_y7_sfx.mp4"
WORK_CARDS = ROOT / "poc_comic_page/_living_comic/work/the_mockers_ps22_7_y7"
FONTS = ROOT / "poc_comic_page/_living_comic_design/fonts"
INK = (20, 18, 16); GOLD = (232, 168, 28); WHITE = (252, 250, 244); PARCH = (236, 214, 160); BROWN = (92, 58, 24)
BANG = lambda s: ImageFont.truetype(str(FONTS / "Bangers.ttf"), s)
KAL = lambda s: ImageFont.truetype(str(FONTS / "Kalam-Bold.ttf"), s)


def run(c): subprocess.run([str(x) for x in c], check=True)


# ---------- lettering ----------
def wrap(d, words, font, maxw):
    lines, cur = [], []
    for w in words:
        t = " ".join(cur + [w])
        if cur and d.textlength(t, font=font) > maxw: lines.append(cur); cur = [w]
        else: cur.append(w)
    return lines + [cur]


def draw_lines(d, lines, font, cx, y, lh, hi=(), fill=INK):
    for ln in lines:
        tw = sum(d.textlength(w + " ", font=font) for w in ln); x = cx - tw / 2
        for w in ln:
            col = (190, 110, 0) if w.strip(".,;").upper() in hi else fill
            d.text((x, y), w, font=font, fill=col)
            if col != fill: d.line((x, y + lh - 6, x + d.textlength(w, font=font), y + lh - 6), fill=GOLD, width=8)
            x += d.textlength(w + " ", font=font)
        y += lh


def jagged_balloon(path, text, cx, top, tail_to, hi=(), size=84, W=1080, maxw=800):
    img = Image.new("RGBA", (W, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(img); f = BANG(size); lh = int(size * 1.08)
    lines = wrap(d, text.upper().split(), f, maxw); h = len(lines) * lh
    a, b = maxw / 2 + 90, h / 2 + 70; cy = top + b
    pts = []
    for i in range(48):
        ang = 2 * math.pi * i / 48; r = 1.0 + (0.09 if i % 2 else 0)
        pts.append((cx + a * r * math.cos(ang), cy + b * r * math.sin(ang)))
    tx, ty = tail_to; bx = cx + (tx - cx) * 0.35
    tail = [(bx - 55, cy + b * 0.8), (tx, ty), (bx + 55, cy + b * 0.8)]
    d.polygon(tail, fill=WHITE); d.line(tail[:2] + [tail[2]], fill=INK, width=9, joint="curve")
    d.polygon(pts, fill=WHITE); d.line(pts + [pts[0]], fill=INK, width=9, joint="curve")
    d.polygon([(bx - 52, cy + b * 0.78), (bx, cy + b * 0.8 + 18), (bx + 52, cy + b * 0.78)], fill=WHITE)
    draw_lines(d, lines, f, cx, cy - h / 2 - 4, lh, hi); img.save(path)


def parchment(path, text, cx, top, hi=(), head=None, size=70, maxw=820):
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(img); f = BANG(size); lh = int(size * 1.1)
    lines = wrap(d, text.upper().split(), f, maxw); h = len(lines) * lh + (60 if head else 0)
    x0, x1, y0, y1 = cx - maxw / 2 - 50, cx + maxw / 2 + 50, top, top + h + 60
    rnd = random.Random(7); edge = lambda x, y: (x + rnd.uniform(-4, 4), y + rnd.uniform(-4, 4))
    poly = [edge(x, y0) for x in range(int(x0), int(x1), 40)] + [edge(x1, y) for y in range(int(y0), int(y1), 40)] + \
           [edge(x, y1) for x in range(int(x1), int(x0), -40)] + [edge(x0, y) for y in range(int(y1), int(y0), -40)]
    d.polygon(poly, fill=PARCH); d.line(poly + [poly[0]], fill=BROWN, width=7, joint="curve")
    y = y0 + 30
    if head: d.text((cx - d.textlength(head, font=KAL(40)) / 2, y), head, font=KAL(40), fill=BROWN); y += 58
    draw_lines(d, lines, f, cx, y, lh, hi, fill=(50, 28, 8)); img.save(path)


def label(path, text, y, size=58):
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(img); f = BANG(size); tw = d.textlength(text, font=f)
    d.rounded_rectangle((540 - tw / 2 - 40, y, 540 + tw / 2 + 40, y + size + 40), 24, fill=GOLD, outline=INK, width=6)
    d.text((540 - tw / 2, y + 12), text, font=f, fill=INK); img.save(path)


def refchip(path, text, y):
    label(path, text, y, 46)


# ---------- shots ----------
def shot(out, src, t_in, dur, cx, cy, z0, z1, band=None):
    """cut-in: crop window centred (cx,cy) in source, push z0->z1. band=(y0px of 1080x1920) -> 1080x960 half-panel."""
    n = int(round(dur * 30)); s = CLIPS / (src + ".mp4")
    pre = "scale=1080:1920:flags=bicubic,fps=30"
    if band is not None:
        pre += ",crop=1080:960:0:%d" % band; size = "1080x960"
    else: size = "1080x1920"
    zp = "zoompan=z='%.4f+(%.4f)*in/%d':x='max(0,min(iw-iw/zoom,%.4f*iw-iw/zoom/2))':y='max(0,min(ih-ih/zoom,%.4f*ih-ih/zoom/2))':d=1:s=%s:fps=30" % (z0, z1 - z0, n, cx, cy, size)
    run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-ss", "%.2f" % t_in, "-i", s, "-vf", pre + "," + zp + ",format=yuv420p", "-frames:v", n, "-an", "-c:v", "libx264", "-crf", "17", out])


def split_shot(out, top, bot, dur):
    t, b = out.with_name(out.stem + "_t.mp4"), out.with_name(out.stem + "_b.mp4")
    shot(t, *top[:2], dur, *top[2:], band=top[-1]) if False else None
    n = int(round(dur * 30))
    for o, (src, t_in, cx, cy, z0, z1, band) in ((t, top), (b, bot)):
        s = CLIPS / (src + ".mp4")
        zp = "zoompan=z='%.4f+(%.4f)*in/%d':x='max(0,min(iw-iw/zoom,%.4f*iw-iw/zoom/2))':y='max(0,min(ih-ih/zoom,%.4f*ih-ih/zoom/2))':d=1:s=1080x960:fps=30" % (z0, z1 - z0, n, cx, cy)
        run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-ss", "%.2f" % t_in, "-i", s, "-vf", "scale=1080:1920,fps=30,crop=1080:960:0:%d,%s,format=yuv420p" % (band, zp), "-frames:v", n, "-an", "-c:v", "libx264", "-crf", "17", o])
    run(["ffmpeg", "-y", "-v", "error", "-i", t, "-i", b, "-filter_complex", "[0:v][1:v]vstack,drawbox=x=0:y=950:w=1080:h=20:color=0xE8A81C:t=fill[v]", "-map", "[v]", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", out])


def build(name, shots, overlays, audio_filter, total, cards, shift=0.0):
    W = HERE / "work" / name; W.mkdir(parents=True, exist_ok=True); segs = []
    for k, sh in enumerate(shots):
        o = W / ("s%02d.mp4" % k)
        if sh[0] == "split": split_shot(o, sh[1], sh[2], sh[3])
        else: shot(o, *sh[:1], *sh[1:3], *sh[3:]) if False else shot(o, sh[0], sh[1], sh[2], sh[3], sh[4], sh[5], sh[6])
        segs.append(o)
    (W / "l.txt").write_text("".join("file '%s'\n" % s.as_posix() for s in segs))
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", W / "l.txt", "-c", "copy", W / "base.mp4"])
    ins = ["-i", W / "base.mp4"]; fc = ""; prev = "[0:v]"; n = 1
    loop = ["-loop", "1", "-framerate", "30", "-t", "%.2f" % total]
    for i, (png, t0, t1, y) in enumerate(overlays + cards):
        ins += loop + ["-i", png]
        fc += "[%d:v]format=rgba,fade=in:st=%.2f:d=0.12:alpha=1,fade=out:st=%.2f:d=0.12:alpha=1[o%d];%s[o%d]overlay=x=0:y=%d:eof_action=pass:enable='between(t,%.2f,%.2f)'[p%d];" % (n, t0, t1 - 0.12, i, prev, i, y, t0, t1, i)
        prev = "[p%d]" % i; n += 1
    fc += prev + "null[out]"
    return W, ins, fc, n


def finish(name, W, ins, fc, n, audio_in, afilter, total):
    out = HERE / "arms" / (name + ".mp4"); out.parent.mkdir(exist_ok=True)
    run(["ffmpeg", "-y", "-v", "error", *ins, *audio_in, "-filter_complex", fc + ";" + afilter, "-map", "[out]", "-map", "[aud]", "-t", "%.2f" % total, "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", out])
    print("built", out)


def card_png(name, i):  # reuse existing decode/hook cards from today's film, as-is
    src = WORK_CARDS / ("card%d.png" % i); dst = HERE / "work" / name / ("card%d_full.png" % i)
    dst.parent.mkdir(parents=True, exist_ok=True); im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); im.alpha_composite(Image.open(src).convert("RGBA"), (90, 1250)); im.save(dst); return str(dst)


def main():
    (HERE / "arms").mkdir(exist_ok=True)
    # ---- A: today's film, first 31.1s ----
    run(["ffmpeg", "-y", "-v", "error", "-i", FILM, "-t", "31.1", "-af", "afade=t=out:st=30.5:d=0.6", "-c:v", "libx264", "-crf", "18", "-c:a", "aac", HERE / "arms" / "A.mp4"]); print("built A")
    # ---- shared lettering ----
    L = HERE / "work" / "lettering"; L.mkdir(parents=True, exist_ok=True)
    mock_full = L / "mock_full.png"; jagged_balloon(mock_full, "He trusted in God; let him deliver him now", 540, 110, (575, 700), hi=("DELIVER",))
    mock_ref = L / "mock_ref.png"; refchip(mock_ref, "MATTHEW 27:43", 1560)
    mock_half = L / "mock_half.png"; jagged_balloon(mock_half, "...let him deliver him", 540, 40, (540, 400), hi=("DELIVER",), size=70, maxw=700)
    dav_half = L / "dav_half.png"; parchment(dav_half, "that he would deliver him", 540, 1040, hi=("DELIVER",), head="DAVID, 1,000 YEARS EARLIER", size=66)
    stamp = L / "stamp.png"; label(stamp, "SAME WORDS", 905, 52)
    dav_ref = L / "dav_ref.png"; refchip(dav_ref, "PSALM 22:8", 1560)
    # ---- B ----
    gold = "golgotha_hill_wide"; rul = "rulers_sneering"; dav = "david_writing_psalm"; scr = "psalm_scroll_night"
    B = [(gold, 0, 2.4, .5, .5, 1.0, 1.12), (gold, 0.5, 2.2, .49, .20, 2.4, 2.7), (gold, 1.0, 2.0, .5, .62, 1.3, 1.5),
         (rul, 0, 1.7, .6, .6, 1.2, 1.7),
         (rul, 0.5, 2.2, .74, .60, 2.0, 2.3), (rul, 1.5, 2.1, .76, .60, 2.5, 2.9),
         (dav, 0, 2.0, .5, .5, 1.0, 1.1), (dav, 1.0, 2.5, .30, .62, 2.2, 2.5), (dav, 1.5, 2.5, .28, .33, 1.8, 2.0),
         (scr, 0, 3.0, .5, .5, 1.0, 1.15), (scr, 1.0, 2.5, .80, .22, 2.4, 2.6), (scr, 0.5, 2.8, .5, .62, 1.6, 1.9),
         ("split", (rul, 1.0, .76, .60, 1.2, 1.35, 560), (dav, 1.0, .30, .62, 1.2, 1.35, 700), 3.3)]
    # timings of B shots sum: 2.4+2.2+2.0+1.7 = 8.3 ; mocker 8.3.. ; fix below by explicit durations
    Bd = [2.4, 2.2, 2.0, 1.6, 2.2, 2.3, 2.0, 2.5, 3.0, 3.0, 2.5, 2.8, 3.3]   # sums to 31.8 -> trimmed to total by -t
    Bs = []
    for s, dd in zip(B, Bd):
        Bs.append(s if s[0] == "split" else (s[0], s[1], dd, s[3], s[4], s[5], s[6]))
    Bs[-1] = ("split", B[-1][1], B[-1][2], 3.3)
    # correct totals: 8.2 (3 shots+mocker intro) -> mocker 8.2-12.5 ; david 12.5-19.5 ; scroll 19.5-27.8 ; split 27.8-31.1
    Bdur = [2.4, 2.2, 2.0, 1.6,          # 0-8.2  wide / jesus / hands / leaders
            2.2, 2.1,                    # 8.2-12.5 mouth push (balloon)
            2.0, 2.5, 2.5,               # 12.5-19.5 david wide / quill / face
            3.0, 2.5, 2.8,               # 19.5-27.8 scroll wide / lamp / text
            3.3]                         # 27.8-31.1 split
    shots = []
    for s, dd in zip(B, Bdur):
        shots.append(("split", s[1], s[2], dd) if s[0] == "split" else (s[0], s[1], dd, s[3], s[4], s[5], s[6]))
    shots[3] = (rul, 0, 1.6, .6, .6, 1.2, 1.7)
    # leaders + mouth block must end at 12.5: 8.2+2.2+2.1 = 12.5 ok; 0-8.2: 2.4+2.2+2.0+1.6 = 8.2 ok; 12.5+7=19.5 ok; +8.3 -> 27.8 ok; 3.3 -> 31.1
    cardsB = [(card_png("B", 0), 0.2, 2.8, 0), (card_png("B", 1), 12.9, 15.5, 0)]
    ovB = [(str(mock_full), 8.3, 12.2, 0), (str(mock_ref), 8.3, 12.2, 0), (str(mock_half), 27.8, 31.1, 0), (str(dav_half), 27.8, 31.1, 0), (str(stamp), 27.8, 31.1, 0), (str(dav_ref), 28.0, 31.1, 0)]
    W, ins, fc, n = build("B", shots, ovB, None, 31.1, cardsB)
    finish("B", W, ins, fc, n, ["-i", FILM], "[%d:a]atrim=0:31.1,afade=t=out:st=30.5:d=0.6[aud]" % n, 31.1)
    # ---- C: B + story order. Mouth hook first, then narration, then the rest. audio: mix[8.15-12.0] + mix[0-6.9] + mix[12.5-31.1] ----
    S = -1.75   # later events shift by this
    Cdur = [3.85,                                  # mouth hook (mocker line)
            2.15, 2.2, 2.55,                       # 3.85-10.75: wide / jesus face / leaders  (voice: 0-6.9 of narration)
            2.0, 2.5, 2.5,                         # david block 10.75-17.75
            3.0, 2.5, 2.8,                         # scroll block 17.75-26.05
            3.3]                                   # split 26.05-29.35
    C_shots = [(rul, 0.5, Cdur[0], .74, .60, 2.0, 2.6),
               (gold, 0, Cdur[1], .5, .5, 1.0, 1.12), (gold, 0.5, Cdur[2], .49, .20, 2.4, 2.7), (rul, 0, Cdur[3], .6, .6, 1.2, 1.7),
               (dav, 0, Cdur[4], .5, .5, 1.0, 1.1), (dav, 1.0, Cdur[5], .30, .62, 2.2, 2.5), (dav, 1.5, Cdur[6], .28, .33, 1.8, 2.0),
               (scr, 0, Cdur[7], .5, .5, 1.0, 1.15), (scr, 1.0, Cdur[8], .80, .22, 2.4, 2.6), (scr, 0.5, Cdur[9], .5, .62, 1.6, 1.9),
               ("split", B[-1][1], B[-1][2], Cdur[10])]
    tot = sum(Cdur)
    cardsC = [(card_png("C", 0), 0.2, 2.8, 0), (card_png("C", 1), 12.9 + S, 15.5 + S, 0)]
    ovC = [(str(mock_full), 0.1, 3.75, 0), (str(mock_ref), 0.1, 3.75, 0), (str(mock_half), 27.8 + S, 31.1 + S, 0), (str(dav_half), 27.8 + S, 31.1 + S, 0), (str(stamp), 27.8 + S, 31.1 + S, 0), (str(dav_ref), 28.0 + S, 31.1 + S, 0)]
    W, ins, fc, n = build("C", C_shots, ovC, None, tot, cardsC)
    af = ("[%d:a]atrim=8.15:12.0,asetpts=PTS-STARTPTS,afade=t=out:st=3.6:d=0.25[a1];[%d:a]atrim=0:6.9,asetpts=PTS-STARTPTS,afade=t=out:st=6.6:d=0.3[a2];"
          "[%d:a]atrim=12.5:31.1,asetpts=PTS-STARTPTS[a3];[a1][a2][a3]concat=n=3:v=0:a=1,afade=t=out:st=%.2f:d=0.6[aud]" % (n, n, n, tot - 0.6))
    finish("C", W, ins, fc, n, ["-i", FILM], af, tot)


if __name__ == "__main__":
    main()
