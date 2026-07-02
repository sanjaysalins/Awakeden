#!/usr/bin/env python
"""FAST-CUT 16:9 mocomic builder (the SHORT's approach at 16:9).

Quick full-frame beats that CUT fast (every ~5-7s), each a distinct 16:9 still ken-burned (or
punched), with kinetic word-cascade captions + static red Scripture bars over the top, muxed to
the narration. This is what makes it "feel like the short" (cut rate, not panels-per-page).
$0 preview: existing stills as ken-burns. Reuses the short pilot's kinetic_caption at 16:9.

  .venv\\Scripts\\python.exe longform/02_Psalm_22_Song_From_The_Cross/build_fastcut_16x9.py --spec m1_fastcut.json
"""
import argparse, importlib.util, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
POOL = HERE / "v1" / "visual_16x9_inked"
WORK = POOL / "_fastcut_work"; WORK.mkdir(parents=True, exist_ok=True)
PAGE = (1920, 1080)
FONT = r"C:\Windows\Fonts\comicbd.ttf"
RED = (170, 30, 26, 255); WHITE = (250, 248, 244, 255); INK = (18, 14, 8, 255)

kc_spec = importlib.util.spec_from_file_location(
    "kc", ROOT / "batches" / "cluster_01_cross" / "father_forgive_them" / "kinetic_caption.py")
kc = importlib.util.module_from_spec(kc_spec); kc_spec.loader.exec_module(kc)


def kb_clip(still: Path, dur: float, motion: str, dest: Path) -> Path:
    # FAST ken-burns via a moving crop on an oversized frame (zoompan is too slow on full stills).
    # push = slow vertical drift; punch = start tighter (center crop of a bigger scale) — cheap.
    scale = "2304:1296" if motion == "punch" else "2112:1188"   # 1.2x / 1.1x oversample
    if motion == "punch":
        x, y = "(iw-1920)/2", "(ih-1080)/2"
    else:
        x, y = "(iw-1920)/2", f"(ih-1080)*(0.5-0.28*t/{dur})"    # gentle upward drift
    vf = (f"scale={scale}:force_original_aspect_ratio=increase,crop={scale.split(':')[0]}:{scale.split(':')[1]},"
          f"crop=1920:1080:x='{x}':y='{y}',setsar=1,fps=30")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-t", f"{dur}", "-i", str(still),
                    "-vf", vf, "-r", "30", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
                    "-pix_fmt", "yuv420p", str(dest)], check=True)
    return dest


def _san(s):
    for k, v in {"—": "-", "’": "'", "“": '"', "”": '"'}.items():
        s = s.replace(k, v)
    return s


def redbar_png(text, speaker, ref, dest):
    W, H = PAGE
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT, 46); tf = ImageFont.truetype(FONT, 30)
    mx, pad = 70, 24
    words = _san(text).split(); lines, cur = [], []
    for w in words:
        if d.textlength(" ".join(cur + [w]), font=f) <= W - 2 * mx - 2 * pad or not cur:
            cur.append(w)
        else:
            lines.append(" ".join(cur)); cur = [w]
    if cur:
        lines.append(" ".join(cur))
    lh = 58; bh = len(lines) * lh + 2 * pad; top = H - bh - 60
    tag = _san(f"{speaker}  -  {ref}"); tw = d.textlength(tag, font=tf)
    d.rounded_rectangle([mx, top - 50, mx + tw + 44, top + 4], radius=8, fill=RED, outline=INK, width=4)
    d.text((mx + 22, top - 44), tag, font=tf, fill=WHITE)
    d.rounded_rectangle([mx, top, W - mx, top + bh], radius=14, fill=WHITE, outline=INK, width=6)
    y = top + pad
    for ln in lines:
        d.text((mx + pad, y), ln, font=f, fill=RED); y += lh
    img.save(dest); return dest


def overlay_kinetic(seg, text, kw, dur, stem, dest):
    paths, _, _ = kc.render_states(text, kw, WORK, stem, page=PAGE)
    n = len(paths); reveal = max(0.6, min(dur * 0.6, dur - 0.4)); dt = reveal / n
    bounds = [k * dt for k in range(1, n)]
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(seg)]
    for p in paths:
        cmd += ["-loop", "1", "-t", f"{dur}", "-i", str(p)]
    parts = ["[1:v]format=rgba,fade=t=in:st=0:d=0.1:alpha=1[k1]"]
    for j in range(2, n + 1):
        parts.append(f"[{j}:v]format=rgba[k{j}]")
    prev = "0:v"
    for idx in range(1, n + 1):
        a = 0.0 if idx == 1 else bounds[idx - 2]
        en = f"between(t,{a:.3f},{bounds[idx-1]:.3f})" if idx < n else f"gte(t,{a:.3f})"
        out = f"o{idx}" if idx < n else "outv"
        parts.append(f"[{prev}][k{idx}]overlay=0:0:enable='{en}'[{out}]"); prev = out
    cmd += ["-filter_complex", ";".join(parts), "-map", "[outv]", "-r", "30",
            "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(dest)]
    subprocess.run(cmd, check=True); return dest


def overlay_static(seg, png, dur, dest):
    # -t hard-caps the output: the -loop 1 PNG is an infinite input and -shortest alone
    # does NOT reliably bound it here (overlay repeats the base's last frame), which
    # produced a runaway multi-GB seg. Cap at the beat duration.
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(seg), "-loop", "1", "-i", str(png),
                    "-filter_complex", "[1:v]format=rgba,fade=t=in:st=0.1:d=0.25:alpha=1[c];[0:v][c]overlay=0:0[outv]",
                    "-map", "[outv]", "-r", "30", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
                    "-pix_fmt", "yuv420p", "-t", f"{dur}", str(dest)], check=True)
    return dest


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--spec", default="m1_fastcut.json")
    a = ap.parse_args()
    spec = json.loads((POOL / a.spec).read_text(encoding="utf-8"))
    segs = []
    for i, b in enumerate(spec["beats"], 1):
        dur = round(b["t"][1] - b["t"][0], 3)
        still = POOL / f"{b['img']}.png"
        raw = kb_clip(still, dur, b.get("motion", "push"), WORK / f"raw_{i:02d}.mp4")
        cap = b.get("cap"); out = WORK / f"seg_{i:02d}.mp4"
        if cap and cap["type"] == "caption":
            overlay_kinetic(raw, cap["text"], cap.get("kw", ""), dur, f"{i:02d}", out)
        elif cap and cap["type"] == "redletter":
            png = redbar_png(cap["text"], cap.get("speaker", "SCRIPTURE"), cap.get("ref", ""), WORK / f"rb_{i:02d}.png")
            overlay_static(raw, png, dur, out)
        else:
            out = raw
        print(f"  [{i:2}] {dur:4.1f}s  {b['img']:24} {b.get('motion'):6} {cap['type'] if cap else '-'}", flush=True)
        segs.append(out)
    lst = WORK / "concat.txt"; lst.write_text("".join(f"file '{s.as_posix()}'\n" for s in segs), encoding="utf-8")
    silent = WORK / "_silent.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(silent)], check=True)
    total = spec["beats"][-1]["t"][1]
    audio = (POOL / spec["narration"]).resolve()
    out = POOL / (Path(a.spec).stem + "_preview.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(silent), "-i", str(audio),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-t", f"{total:.2f}", str(out)], check=True)
    print(f"\nDONE -> {out}\n  file:///{str(out).replace(chr(92),'/')}")


if __name__ == "__main__":
    main()
