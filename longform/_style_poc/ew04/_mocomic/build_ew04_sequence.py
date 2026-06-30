#!/usr/bin/env python
"""EW04 — a REAL landscape motion-comic SEQUENCE, end to end.

Maps the 10 EW04 narration beats -> landscape templates -> existing assets, builds
each page as a moving clip (cover-crop reuse clips + Ken Burns stills + the ONE veo
serpent hero on the pivot page), concats them, and muxes the existing narration+score.

$0 beyond the veo already rendered: every page is reuse / Ken Burns except beat 3,
which uses hero_serpent_wide.mp4. Because the reuse art is all PORTRAIT, the rich
multi-cell wide templates can't shine yet — those want fresh 16:9 veo heroes (the
upgrade lever). This proves the pipeline + pacing on real audio.

  .venv\\Scripts\\python.exe longform/_style_poc/ew04/_mocomic/build_ew04_sequence.py
"""
import importlib.util, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
le_spec = importlib.util.spec_from_file_location("le", HERE / "landscape_engine.py")
le = importlib.util.module_from_spec(le_spec); le_spec.loader.exec_module(le)

STILLS = HERE.parent / "stills"
ANIM = HERE.parent / "anim"
LAND = HERE / "_landscape"
AUDIO = HERE.parent / "cut" / "EW04_bronze_serpent_scored_captioned.mp4"
TMP = LAND / "_seq_tmp"; TMP.mkdir(parents=True, exist_ok=True)
OUT = LAND / "EW04_landscape_sequence.mp4"

PAGE_W, PAGE_H, FPS = le.PAGE_W, le.PAGE_H, 30
INK, PARCH, WHITE, RED = le.INK, le.PARCH, (250, 248, 244, 255), (150, 28, 24, 255)
FONT = le.FONT
PAPER_HEX = "0xFCF9F1"


def V(slug):   # reuse 9:16 clip (portrait — kept NATIVE, never cropped/zoomed)
    return {"k": "v", "ar": 9 / 16, "src": ANIM / f"EW04__{slug}.mp4"}
def K(name, bx=0.5, by=0.40, z=1.12):  # ken-burns still
    return {"k": "kb", "src": STILLS / f"{name}.png", "bx": bx, "by": by, "z": z}
def H(z=1.10):  # the veo serpent hero (16:9 — fills its 16:9 cell exactly)
    return {"k": "v", "ar": 16 / 9, "src": LAND / "hero_serpent_wide.mp4"}
def KW(bx=0.5, by=0.40, z=1.10):  # ken-burns the WIDE serpent still (a 16:9 'cheat hero')
    return {"k": "kb", "src": LAND / "hero_serpent_wide.png", "bx": bx, "by": by, "z": z}


# ---- the authored sequence: (t0, t1, template, [assets aligned to template cells], caption) ----
def cap(text):
    return {"type": "caption", "text": text}
def red(text):
    return {"type": "redletter", "speaker": "JESUS", "ref": "JOHN 3", "text": text}

PAGES = [
    (0.0, 8.2, "10_rail_duo",
     [V("01b_moses_close"), K("01_hook_moses", 0.5, 0.42), K("02_judgment_plague", 0.42, 0.74)],
     cap("My people were dying of snakebite.")),

    (8.2, 14.8, "04_triptych_cols",
     [V("02_judgment_plague"), V("02b_serpents_spread"), V("08_bitten_multitude")],
     cap("The venom was the judgment our sin had earned.")),

    (14.8, 18.6, "01_full_bleed",
     [K("01b_moses_close", 0.30, 0.40, 1.10)],
     cap("I begged Him. He would not.")),

    (18.6, 24.1, "07_big_inset",                      # <-- the ONE veo page
     [H(), K("03b_serpent_atop_sky", 0.5, 0.30), K("04b_face_to_life", 0.5, 0.32)],
     cap("Forge the very thing killing us -- and lift it high.")),

    (24.1, 27.7, "01_full_bleed",
     [K("04b_face_to_life", 0.5, 0.34, 1.10)],
     cap("The bitten had only to look, and live.")),

    (27.7, 36.8, "06_grid_2x3",
     [KW(0.5, 0.42), K("05_night_teacher", 0.5, 0.40), K("03b_serpent_atop_sky", 0.5, 0.30),
      V("05_night_teacher"), K("06_cross_lifted", 0.5, 0.35), V("05b_jesus_speaks")],
     cap("From the far side of my life, the Teacher answered:")),

    (36.8, 43.5, "01_full_bleed",
     [K("05b_jesus_speaks", 0.5, 0.38, 1.08)],
     red("And as Moses lifted up the serpent in the wilderness, even so must the Son of man be lifted up.")),

    (43.5, 52.6, "01_full_bleed",
     [K("06_cross_lifted", 0.5, 0.35, 1.10)],
     cap("They lifted Jesus on a Roman pole, bearing our judgment.")),

    (52.6, 62.7, "10_rail_duo",
     [V("08_bitten_multitude"), K("02b_serpents_spread", 0.5, 0.72), K("04b_face_to_life", 0.5, 0.32)],
     cap("You who are bitten -- that is every one of us.")),

    (62.7, 69.3, "01_full_bleed",
     [K("07_risen_christ", 0.5, 0.36, 1.10)],
     cap("Lift your eyes to Jesus. Look, and live.")),
]


def ff(args):
    subprocess.run(["ffmpeg", "-y", "-v", "error"] + args, check=True)


# ---------------- cell renderers (each -> an mp4 at cell size, length=dur) ----------------
def fit_box(rect, ar=9 / 16):
    """largest centred box of aspect `ar` (w/h) that fits inside the cell, even-snapped."""
    x, y, w, h = rect
    if w / h > ar:                       # cell too wide -> limit by height
        bh = le._even(h); bw = le._even(round(h * ar))
    else:                                # cell too tall -> limit by width
        bw = le._even(w); bh = le._even(round(w / ar))
    return (x + (w - bw) // 2, y + (h - bh) // 2, bw, bh)


def vid_cell(src, dest, w, h, dur, contain=True):
    """contain=True : keep the clip NATIVE (fit inside, paper margins, no crop, no zoom)
       contain=False: fill the cell exactly (used only for the 16:9 veo hero in a 16:9 cell)."""
    if contain:
        vf = (f"scale={w}:{h}:force_original_aspect_ratio=decrease:flags=lanczos,"
              f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color={PAPER_HEX},fps={FPS},setsar=1")
    else:
        vf = (f"scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,"
              f"crop={w}:{h},fps={FPS},setsar=1")
    ff(["-stream_loop", "-1", "-i", str(src), "-t", f"{dur:.3f}", "-vf", vf,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", str(dest)])


def kb_cell(a, dest, w, h, dur):
    crop = le.lt.fill_bias(Image.open(a["src"]).convert("RGB"), w * 3, h * 3, a["bx"], a["by"])
    src = TMP / f"_s_{dest.stem}.png"; crop.save(src)
    fr = max(int(round(dur * FPS)), 2)
    rate = (a["z"] - 1.0) / fr
    vf = (f"zoompan=z='min(1+{rate:.6f}*on,{a['z']})':d={fr}:"
          f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps={FPS},setsar=1")
    ff(["-loop", "1", "-i", str(src), "-t", f"{dur:.3f}", "-r", str(FPS), "-vf", vf,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", str(dest)])


# ---------------- furniture (borders + caption / redletter) ----------------
def _wrap(d, text, font, mw):
    out, cur = [], ""
    for wd in le.lt.sanitize(text).split():
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=font) <= mw:
            cur = t
        else:
            out.append(cur); cur = wd
    if cur:
        out.append(cur)
    return out


def furniture(rects, capspec, dest):
    page = Image.new("RGBA", (PAGE_W, PAGE_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(page)
    for x, y, w, h in rects:             # border hugs the actual drawn box (tight to native clips)
        d.rectangle([x, y, x + w, y + h], outline=INK, width=le.BORDER)
    if capspec["type"] == "redletter":
        f = ImageFont.truetype(FONT, 58); tf = ImageFont.truetype(FONT, 40)
        mx, pad = 64, 30
        lines = _wrap(d, capspec["text"], f, PAGE_W - 2 * mx - 2 * pad)
        lh = 72; bh = len(lines) * lh + 2 * pad; top = PAGE_H - bh - 70
        tag = f"{capspec['speaker']}  -  {capspec['ref']}"
        tw = d.textlength(tag, font=tf)
        d.rounded_rectangle([mx, top - 64, mx + tw + 56, top + 6], radius=10, fill=RED, outline=INK, width=4)
        d.text((mx + 28, top - 56), tag, font=tf, fill=WHITE)
        d.rounded_rectangle([mx, top, PAGE_W - mx, top + bh], radius=18, fill=WHITE, outline=INK, width=8)
        yy = top + pad
        for ln in lines:
            d.text((mx + pad, yy), ln, font=f, fill=RED); yy += lh
    else:
        le.lt._box(d, le.M + 12, le.M + 12, le.M + 12 + 980, capspec["text"], 50, PARCH, INK)
    page.save(dest)


# ---------------- page compositor ----------------
def build_page(i, t0, t1, tname, assets, capspec):
    dur = t1 - t0
    cells = le.TEMPLATES[tname]()["cells"]
    cell_clips, draw_rects = [], []
    for j, (c, a) in enumerate(zip(cells, assets)):
        rect = c["rect"]
        dest = TMP / f"p{i:02d}_c{j}.mp4"
        if a["k"] == "v":
            if a.get("ar", 9 / 16) < 1:          # 9:16 reuse clip -> NATIVE box, no crop/zoom
                rect = fit_box(rect)
                x, y, w, h = rect
                vid_cell(a["src"], dest, w, h, dur, contain=True)
            else:                                # 16:9 veo hero -> fills its 16:9 cell
                x, y, w, h = rect
                vid_cell(a["src"], dest, w, h, dur, contain=False)
        else:
            x, y, w, h = rect
            kb_cell(a, dest, w, h, dur)
        cell_clips.append((dest, x, y))
        draw_rects.append(rect)
    furn = TMP / f"p{i:02d}_furn.png"
    furniture(draw_rects, capspec, furn)

    inputs, fc, last = [], [f"color=c={PAPER_HEX}:s={PAGE_W}x{PAGE_H}:d={dur:.3f}:r={FPS}[bg];"], "bg"
    for k, (clip, x, y) in enumerate(cell_clips):
        inputs += ["-i", str(clip)]
        tag = f"o{k}"
        fc.append(f"[{last}][{k}:v]overlay={x}:{y}[{tag}];"); last = tag
    inputs += ["-loop", "1", "-i", str(furn)]
    fi = len(cell_clips)
    fc.append(f"[{last}][{fi}:v]overlay=0:0[out]")
    pageclip = TMP / f"page{i:02d}.mp4"
    ff(inputs + ["-filter_complex", "".join(fc), "-map", "[out]", "-t", f"{dur:.3f}", "-r", str(FPS),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", str(pageclip)])
    print(f"[page {i:02d}] {tname:16s} {dur:4.1f}s  cells={len(cells)}")
    return pageclip


def main():
    pages = [build_page(i, *p) for i, p in enumerate(PAGES)]
    lst = TMP / "concat.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in pages), encoding="utf-8")
    silent = TMP / "_silent.mp4"
    ff(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(silent)])
    ff(["-i", str(silent), "-i", str(AUDIO), "-map", "0:v", "-map", "1:a",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
        "-movflags", "+faststart", str(OUT)])
    print(f"\nsequence -> {OUT}")
    # 3 review frames
    for t in (3, 21, 65):
        ff(["-ss", str(t), "-i", str(OUT), "-frames:v", "1", str(LAND / f"_seq_f{t}.png")])


if __name__ == "__main__":
    main()
