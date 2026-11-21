"""Living Comic composer ($0): episode.json -> film. Runs lc_gates first; refuses to build on FAIL.
  .venv\\Scripts\\python.exe poc_comic_page/_living_comic/lc_compose.py <episode.json>
Moves in v1: ink wake (first + jesus panel), hard cut, slow push + drift + light sweep, jesus/human balloons
(chained, ghost older), decode card. Not in v1: break-out, page turn, panel walk."""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = Path(__file__).resolve().parent; ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE)); import lc_gates
FONTS = HERE.parent / "_living_comic_design" / "fonts"
IVORY = (250, 244, 226); GOLD = (214, 160, 40); INK = (20, 18, 16); GREY = (225, 225, 228); OY = 40
NL = chr(10); Q = chr(39)


def run(c): subprocess.run(c, check=True)


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)


def listfile(path, items):
    path.write_text("".join("file " + Q + x.as_posix() + Q + NL for x in items))


def main(path):
    ep = json.load(open(path, encoding="utf-8-sig")); name = ep["episode"]
    res = lc_gates.gates(ep); bad = [(n, m) for n, ok, m in res if not ok]
    for n, ok, m in res:
        print(("PASS " if ok else "FAIL ") + n + (" -> " + m if m else ""))
    if bad: raise SystemExit("gates failed; not building")
    W = HERE / "work" / name; W.mkdir(parents=True, exist_ok=True); DUR = ep["audio"]["dur"]
    font = ImageFont.truetype(str(FONTS / "Kalam-Bold.ttf"), 64); tabf = ImageFont.truetype(str(FONTS / "Kalam-Bold.ttf"), 34)
    B = ep["balloons"]
    for i, b in enumerate(B):
        img = Image.new("RGBA", (1080, 230), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
        jesus = b["speaker"] == "jesus"
        if jesus: d.rounded_rectangle((70, 10 + OY, 1010, 170 + OY), 56, fill=GOLD + (255,))
        d.rounded_rectangle((82, 22 + OY, 998, 158 + OY), 46, fill=(IVORY if jesus else GREY) + (255,), outline=INK + (255,), width=5)
        for txt, x in b.get("tabs", []):
            tw = d.textlength(txt, font=tabf); d.rounded_rectangle((x, 4, x + tw + 36, 56), 20, fill=GOLD + (255,), outline=INK + (255,), width=3)
            d.text((x + 18, 6), txt, font=tabf, fill=INK + (255,))
        tw = d.textlength(b["text"], font=font); d.text(((1080 - tw) / 2, 36 + OY), b["text"], font=font, fill=INK + (255,)); img.save(W / ("b%d.png" % i))
    C = ep.get("cards", []); cf = ImageFont.truetype(str(FONTS / "Kalam-Bold.ttf"), 110)
    for i, c in enumerate(C):
        card = Image.new("RGBA", (900, 330), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
        d.rounded_rectangle((0, 0, 899, 329), 60, fill=GOLD + (120,)); d.rounded_rectangle((14, 14, 885, 315), 48, fill=IVORY + (105,), outline=INK + (170,), width=5)  # see-through card (owner 2026-11-08)
        for txt, y, col in zip(c["lines"], (30, 165), (INK, (176, 120, 10))):
            tw = d.textlength(txt, font=cf); d.text(((900 - tw) / 2, y), txt, font=cf, fill=col + (255,))
        card.save(W / ("card%d.png" % i))
    band = Image.new("RGBA", (700, 1920), (0, 0, 0, 0)); ImageDraw.Draw(band).polygon([(250, 0), (450, 0), (250, 1920), (50, 1920)], fill=(255, 226, 150, 70))
    band.filter(ImageFilter.GaussianBlur(60)).save(W / "band.png")
    segs = []
    for k, p in enumerate(ep["panels"]):
        d_ = p["t"][1] - p["t"][0]; src = ROOT / p["clip_src"]
        if dur(src) < d_:  # ping-pong the settled tail instead of freezing
            import sys as _s, pathlib as _p
            _s.path.insert(0, str(next(q for q in _p.Path(__file__).resolve().parents if (q / "fill_guard.py").exists())))
            import fill_guard  # fail-closed: ping-pong fill forbidden (owner rule 2026-11-21)
            fill_guard.require_clip_covers_slot('panel %d (%s)' % (k, p['clip_src']), dur(src), d_, what='ping-pong fill')
            tail, rev, head = W / ("t%d.mp4" % k), W / ("r%d.mp4" % k), W / ("h%d.mp4" % k); L = dur(src)
            run(["ffmpeg", "-y", "-v", "error", "-ss", "%.3f" % (L - 1.5), "-i", str(src), "-an", "-c:v", "libx264", "-crf", "14", "-r", "30", str(tail)])
            run(["ffmpeg", "-y", "-v", "error", "-i", str(tail), "-vf", "reverse", "-an", "-c:v", "libx264", "-crf", "14", "-r", "30", str(rev)])
            run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-r", "30", "-an", "-c:v", "libx264", "-crf", "14", str(head)])
            seq = [head]
            while len(seq) < 12: seq += [rev, tail]
            lst = W / ("pp%d.txt" % k); listfile(lst, seq); src = W / ("pp%d.mp4" % k)
            run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(src)])
        fl = "hflip," if p.get("flip") else ""
        base = ("[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920," + fl + "fps=30,trim=0:%s,setpts=PTS-STARTPTS," % d_ +
                "zoompan=z='1.02+0.0016*in':x='iw/2-(iw/zoom/2)+4*sin(in/9)':y='ih/2-(ih/zoom/2)+3*cos(in/11)':d=1:s=1080x1920:fps=30,format=gbrp[c];")
        out = W / ("s%d.mp4" % k); ins = ["-i", str(src)]
        if p.get("ink_wake") and p.get("sketch"):
            fc = (base + "[1:v]scale=1080:1920," + fl + "fps=30,format=gbrp,eq=saturation=0.0:contrast=1.1[sk];"
                  "[c][sk]blend=all_expr='if(lt(X*0.6+Y*0.4+30*sin(Y/45), T/0.5*(W*0.6+H*0.4)), A, B)'[o];[o]format=yuv420p[v]")
            ins += ["-loop", "1", "-framerate", "30", "-i", str(ROOT / ep["sketch_dir"] / p["sketch"])]
        else:
            fc = base + "[c]format=yuv420p[v]"
        run(["ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", fc, "-map", "[v]", "-t", str(d_), "-c:v", "libx264", "-crf", "17", "-r", "30", str(out)]); segs.append(out)
    lst = W / "l.txt"; listfile(lst, segs)
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(W / "base.mp4")])
    ins = ["-i", str(W / "base.mp4")]; fc = ""; prev = "[0:v]"; n = 1
    loop = ["-loop", "1", "-framerate", "30", "-t", str(DUR)]
    slot, slots = 0, []
    for b in B:
        slot = 0 if b.get("tabs") or not slots else slot + 1; slots.append(slot)
    for i, b in enumerate(B):
        s0, e0 = b["t"]; y = "%d+5*sin(2*PI*t/2.4+%d)" % (1010 + slots[i] * 170 - OY, i)
        nxt = B[i + 1]["t"][0] if i + 1 < len(B) else None
        ins += loop + ["-i", str(W / ("b%d.png" % i))]
        fc += "[%d:v]format=rgba,fade=in:st=%s:d=0.25:alpha=1,fade=out:st=%s:d=0.15:alpha=1[b%d];%s[b%d]overlay=x=0:y='%s':eof_action=pass%s[o%d];" % (
            n, s0, e0 - 0.15, i, prev, i, y, (":enable='lt(t,%s)'" % nxt) if nxt else "", i)
        prev = "[o%d]" % i; n += 1
        if nxt:
            ins += loop + ["-i", str(W / ("b%d.png" % i))]
            fc += "[%d:v]format=rgba,colorchannelmixer=aa=0.5,fade=in:st=%s:d=0.2:alpha=1,fade=out:st=%s:d=0.15:alpha=1[g%d];%s[g%d]overlay=x=0:y='%s':eof_action=pass:enable='gte(t,%s)'[og%d];" % (
                n, nxt, e0 - 0.15, i, prev, i, y, nxt, i)
            prev = "[og%d]" % i; n += 1
    ins += loop + ["-i", str(W / "band.png")]
    fc += "[%d:v]format=rgba[bd];%s[bd]overlay=x='-700+mod(t*260,1900)':y=0:eof_action=pass[ol];" % (n, prev); prev = "[ol]"; n += 1
    for i, c in enumerate(C):
        ins += loop + ["-i", str(W / ("card%d.png" % i))]
        fc += "[%d:v]format=rgba,fade=in:st=%s:d=0.25:alpha=1[cd%d];%s[cd%d]overlay=x=90:y=1250:eof_action=pass:enable='between(t,%s,%s)'[oc%d];" % (
            n, c["t"][0], i, prev, i, c["t"][0], c["t"][1], i)
        prev = "[oc%d]" % i; n += 1
    fc += prev + "null[out]"
    out = ROOT / ep["output"]; out.parent.mkdir(parents=True, exist_ok=True); a = ep["audio"]
    run(["ffmpeg", "-y", "-v", "error", *ins, "-ss", str(a["t0"]), "-t", str(DUR), "-i", str(ROOT / a["file"]), "-filter_complex", fc,
         "-map", "[out]", "-map", "%d:a" % n, "-t", str(DUR), "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", str(out)])
    print("built", out, dur(out))


if __name__ == "__main__":
    main(sys.argv[1])
