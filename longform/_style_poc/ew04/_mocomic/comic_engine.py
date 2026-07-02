"""Motion-comic engine — the locked, repeatable pipeline.

Pillars (user feedback, 2026-06-29, LOCKED):
  1. TEMPLATE LIBRARY — a comic-layout vocabulary, rotated for freshness; heroes stay `full`.
  2. ELEMENT-AWARE CROPPING — every clip carries anchors (bias + zoom; fracture anchors)
     so a split/fit never slices the main element (face, the snake on the ground, …).
  3. FILL guardrail (NO FREEZE) — to fill a window longer than a 5s clip:
       static      -> boomerang (in/out), slowed only if still short;
       directional/talk -> SLOW-MOTION stretch forward (never reversed, never frozen).
  4. KEN-BURNS source — a panel may be a STILL with a slow push ($0, no render). Rule:
     every multi-panel grid keeps >=1 truly animated clip; the rest may be ken-burns.
  5. RED SPEECH BAR = highlighted Scripture ONLY (a `cap.type:"redletter"`). Everything
     else is a plain parchment caption box.
  6. TEXT DE-SLOP — all caption text is sanitised (em/en dash -> hyphen, curly quotes ->
     straight, ellipsis -> ...), so no "AI-slop" punctuation is ever rendered.

Furniture is drawn in PIL and composited via ffmpeg OVER the clips — never baked into the
AI image. Preview (`render_still_page`) and video (`build_segment`) share geometry.
"""
from __future__ import annotations
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H, FPS = 1080, 1920, 30
M, G, BORDER = 30, 22, 10
TOP_BAND_H, BOT_BAR_H = 188, 196


def set_page(w, h):
    """Retarget the canvas aspect for this process (e.g. 16:9 long-form landscape).
    Additive + non-breaking: the default is 1080x1920 (9:16), so a 9:16 build that never
    calls this is byte-identical. Templates + furniture + segment math all read PAGE_W/PAGE_H
    as module globals at call time, so reassigning them here retargets the whole engine.
    Band reserves scale to the new height so the caption furniture stays proportionate."""
    global PAGE_W, PAGE_H, TOP_BAND_H, BOT_BAR_H
    PAGE_W, PAGE_H = w, h
    TOP_BAND_H = round(h * 188 / 1920)
    BOT_BAR_H = round(h * 196 / 1920)
PAPER = (252, 249, 241)
INK = (18, 14, 8, 255)
PARCH = (245, 234, 208, 255)
WHITE = (250, 248, 244, 255)
RED = (150, 28, 24, 255)
FONT = r"C:\Windows\Fonts\comicbd.ttf"

# ---------------- text de-slop ----------------
_SLOP = {"—": "-", "–": "-", "‒": "-", "―": "-",
         "‘": "'", "’": "'", "“": '"', "”": '"',
         "…": "...", " ": " ", "­": ""}


def sanitize(s):
    if not s:
        return s
    for k, v in _SLOP.items():
        s = s.replace(k, v)
    return s


# ---------------- geometry helpers ----------------
def _cols(area, n):
    x, y, w, h = area
    pw = (w - (n - 1) * G) / n
    return [(round(x + i * (pw + G)), y, round(pw), h) for i in range(n)]


def _rows(area, n):
    x, y, w, h = area
    ph = (h - (n - 1) * G) / n
    return [(x, round(y + i * (ph + G)), w, round(ph)) for i in range(n)]


def _quad(area):
    out = []
    for c in _cols(area, 2):
        out += _rows(c, 2)
    return out


def _inset(area):
    x, y, w, h = area
    sw, sh = round(w * 0.40), round(h * 0.34)
    return [(x, y, w, h), (x + w - sw - 18, y + h - sh - 18, sw, sh)]


def _big_two(area):
    x, y, w, h = area
    bw = round(w * 0.58)
    rx, rw = x + bw + G, w - bw - G
    ph = round((h - G) / 2)
    return [(x, y, bw, h), (rx, y, rw, ph), (rx, y + ph + G, rw, h - ph - G)]


def _content(cap_slot):
    top = M + (TOP_BAND_H if cap_slot == "top_band" else 0)
    bot = PAGE_H - M - (BOT_BAR_H if cap_slot == "bottom_bar" else 0)
    return (M, top, PAGE_W - 2 * M, bot - top)


# ---------------- TEMPLATE LIBRARY ----------------
TEMPLATES = {
    "full":       ("single",     "overlay",    lambda a: [(0, 0, PAGE_W, PAGE_H)]),
    "two_v":      ("fill_each",   "bottom_bar", lambda a: _cols(a, 2)),
    "split_v":    ("split_page",  "top_band",   lambda a: _cols(a, 2)),
    "stack_h":    ("fill_each",   "bottom_bar", lambda a: _rows(a, 2)),
    "big_inset":  ("fill_each",   "corner",     lambda a: _inset(a)),
    "triptych_v": ("split_page",  "top_band",   lambda a: _cols(a, 3)),
    "strip_h3":   ("fill_each",   "bottom_bar", lambda a: _rows(a, 3)),
    "quad":       ("fill_each",   "corner",     lambda a: _quad(a)),
    "hero_frac3": ("fracture",    "corner",     lambda a: _big_two(a)),
    "hero_frac4": ("fracture",    "corner",     lambda a: _quad(a)),
    "hero_band3": ("fracture",    "bottom_bar", lambda a: _rows(a, 3)),
}


def panels_for(tpl):
    mode, cap, layout = TEMPLATES[tpl]
    return layout(_content(cap))


def template_mode(tpl):
    return TEMPLATES[tpl][0]


# ---------------- clip normalisation ----------------
def norm_clip(c):
    """-> dict(kind, path, motion, bias, zoom, anchors). kind: 'clip'(mp4) | 'kenburns'(still)."""
    if isinstance(c, dict):
        return dict(kind=c.get("kind", "clip"), path=c["path"], motion=c.get("motion", "static"),
                    bias=tuple(c.get("bias", (0.5, 0.5))), zoom=c.get("zoom", 1.0),
                    anchors=[tuple(a) for a in c.get("anchors", [])])
    path, motion = c
    return dict(kind="clip", path=path, motion=motion, bias=(0.5, 0.5), zoom=1.0, anchors=[])


# ---------------- furniture (PIL) ----------------
def _wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def _box(d, rect, text, font_sz, fill, txt_fill, radius, pad):
    font = ImageFont.truetype(FONT, font_sz)
    lines = _wrap(d, sanitize(text).upper(), font, rect[2] - rect[0] - 2 * pad)
    lh = font_sz + 12
    h = len(lines) * lh + 2 * pad
    d.rounded_rectangle([rect[0], rect[1], rect[2], rect[1] + h], radius=radius, fill=fill, outline=INK, width=8)
    y = rect[1] + pad
    for ln in lines:
        d.text((rect[0] + pad + 4, y), ln, font=font, fill=txt_fill); y += lh


def furniture_png(cap_slot, spec, out_path):
    if not spec:
        return None
    img = Image.new("RGBA", (PAGE_W, PAGE_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    typ = spec.get("type", "caption")
    text = sanitize(spec["text"])
    if typ == "redletter":   # highlighted Scripture only
        font = ImageFont.truetype(FONT, 50); tagf = ImageFont.truetype(FONT, 34)
        mx, pad = 46, 26
        lines = _wrap(d, text, font, PAGE_W - 2 * mx - 2 * pad)
        lh = 62; bh = len(lines) * lh + 2 * pad; top = PAGE_H - bh - 64
        tag = sanitize(f"{spec.get('speaker','JESUS')}  ·  {spec.get('ref','')}").replace("·", "-")
        tw = d.textlength(tag, font=tagf)
        d.rounded_rectangle([mx, top - 56, mx + tw + 48, top + 6], radius=10, fill=RED, outline=INK, width=4)
        d.text((mx + 24, top - 48), tag, font=tagf, fill=(255, 248, 240, 255))
        d.rounded_rectangle([mx, top, PAGE_W - mx, top + bh], radius=16, fill=WHITE, outline=INK, width=7)
        y = top + pad
        for ln in lines:
            d.text((mx + pad, y), ln, font=font, fill=RED); y += lh
    elif cap_slot == "corner":
        _box(d, (40, 38, 660, 0), text, 40, PARCH, INK, 14, 22)
    elif cap_slot == "bottom_bar":
        font = ImageFont.truetype(FONT, 46)
        lines = _wrap(d, text.upper(), font, PAGE_W - 120)
        h = len(lines) * 58 + 48; top = PAGE_H - h - 40
        _box(d, (40, top, PAGE_W - 40, 0), text, 46, PARCH, INK, 16, 24)
    elif cap_slot == "top_band":
        _box(d, (30, 26, PAGE_W - 30, 0), text, 40, PARCH, INK, 14, 22)
    else:  # overlay top
        _box(d, (40, 40, PAGE_W - 40, 0), text, 50, PARCH, INK, 18, 28)
    img.save(out_path)
    return out_path


def border_png(rects, out_path):
    img = Image.new("RGBA", (PAGE_W, PAGE_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for (x, y, w, h) in rects:
        d.rectangle([x, y, x + w, y + h], outline=INK, width=BORDER)
    img.save(out_path)
    return out_path


# ---------------- shared crop math (preview) ----------------
def _fill_bias(im, w, h, zoom=1.0, bx=0.5, by=0.5):
    iw, ih = im.size
    s = max(w / iw, h / ih) * zoom
    sw, sh = max(round(iw * s), w), max(round(ih * s), h)
    im2 = im.resize((sw, sh), Image.LANCZOS)
    x = min(max(round((sw - w) * bx), 0), sw - w)
    y = min(max(round((sh - h) * by), 0), sh - h)
    return im2.crop((x, y, x + w, y + h))


def _still_path(clip):
    """ken-burns sources point at a still; clip sources may map to their still for preview."""
    return clip["path"]


# ---------------- STILL preview renderer ----------------
def render_still_page(tpl, clips, cap_spec, out_path):
    clips = [norm_clip(c) for c in clips]
    mode, cap, _ = TEMPLATES[tpl]
    rects = panels_for(tpl)
    bleed = (mode == "single")

    if bleed:
        page = Image.new("RGB", (PAGE_W, PAGE_H), (0, 0, 0))
        c = clips[0]
        page.paste(_fill_bias(Image.open(_still_path(c)).convert("RGB"), PAGE_W, PAGE_H, c["zoom"], *c["bias"]), (0, 0))
    else:
        page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
        if mode == "split_page":
            full = _fill_bias(Image.open(_still_path(clips[0])).convert("RGB"), PAGE_W, PAGE_H)
            for (x, y, w, h) in rects:
                page.paste(full.crop((x, y, x + w, y + h)), (x, y))
        elif mode == "fracture":
            anchors = clips[0]["anchors"] or [(1.0, 0.5, 0.5)] * len(rects)
            im = Image.open(_still_path(clips[0])).convert("RGB")
            for k, (x, y, w, h) in enumerate(rects):
                z, bx, by = anchors[k % len(anchors)]
                page.paste(_fill_bias(im, w, h, z, bx, by), (x, y))
        else:  # fill_each
            for k, (x, y, w, h) in enumerate(rects):
                c = clips[k % len(clips)]
                page.paste(_fill_bias(Image.open(_still_path(c)).convert("RGB"), w, h, c["zoom"], *c["bias"]), (x, y))

    page = page.convert("RGBA")
    if not bleed:
        page.alpha_composite(Image.open(border_png(rects, out_path.parent / "_tmp_brd.png")).convert("RGBA"))
    fp = furniture_png(cap, cap_spec, out_path.parent / "_tmp_cap.png")
    if fp:
        page.alpha_composite(Image.open(fp).convert("RGBA"))
    page.convert("RGB").save(out_path)
    return out_path


# ---------------- video helpers ----------------
_DUR_CACHE = {}


def _clip_len(path):
    p = str(path)
    if p not in _DUR_CACHE:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", p], capture_output=True, text=True)
        try:
            _DUR_CACHE[p] = float(r.stdout.strip())
        except ValueError:
            _DUR_CACHE[p] = 5.0
    return _DUR_CACHE[p]


def _temporal(idx, dur, motion, clip_len, out):
    """Produce [out] of length `dur` with NO freeze and no illegal reverse."""
    if dur <= clip_len + 0.05:
        return f"[{idx}:v]trim=duration={dur},setpts=PTS-STARTPTS[{out}]"
    if motion == "static":
        if 2 * clip_len >= dur:
            return (f"[{idx}:v]split[a{idx}][b{idx}];[b{idx}]reverse[rv{idx}];"
                    f"[a{idx}][rv{idx}]concat=n=2,trim=duration={dur},setpts=PTS-STARTPTS[{out}]")
        f = dur / (2 * clip_len)
        return (f"[{idx}:v]split[a{idx}][b{idx}];[b{idx}]reverse[rv{idx}];"
                f"[a{idx}][rv{idx}]concat=n=2,setpts={f:.4f}*PTS,trim=duration={dur},setpts=PTS-STARTPTS[{out}]")
    f = dur / clip_len   # directional/talk: slow forward, no reverse, no freeze
    return f"[{idx}:v]setpts={f:.4f}*PTS,trim=duration={dur},setpts=PTS-STARTPTS[{out}]"


def _panel_fill(inlabel, out, w, h, zoom=1.0, bx=0.5, by=0.5):
    tw, th = round(w * zoom), round(h * zoom)
    return (f"[{inlabel}]scale={tw}:{th}:force_original_aspect_ratio=increase,"
            f"crop={w}:{h}:(iw-{w})*{bx}:(ih-{h})*{by},setsar=1[{out}]")


def _kenburns(idx, out, w, h, dur, bias=(0.5, 0.5), z_to=1.12):
    n = max(1, round(dur * FPS))
    inc = (z_to - 1.0) / n
    return (f"[{idx}:v]scale={w}:{h}:force_original_aspect_ratio=increase,"
            f"crop={w}:{h}:(iw-{w})*{bias[0]}:(ih-{h})*{bias[1]},setsar=1[kf{idx}];"
            f"[kf{idx}]zoompan=z='min(zoom+{inc:.6f}\\,{z_to})':x='iw/2-(iw/zoom/2)':"
            f"y='ih/2-(ih/zoom/2)':d=1:s={w}x{h}:fps={FPS},trim=duration={dur},setpts=PTS-STARTPTS[{out}]")


# ---------------- VIDEO segment builder ----------------
def build_segment(out_path, tpl, clips, dur, cap_spec, work_dir, fade_st=0.5):
    clips = [norm_clip(c) for c in clips]
    mode, cap, _ = TEMPLATES[tpl]
    rects = panels_for(tpl)
    bleed = (mode == "single")
    # GUARDRAIL: a multi-panel fill_each grid must keep >=1 truly animated clip
    # (the rest may be ken-burns for freshness/cost) — never an all-still grid.
    if mode == "fill_each" and len(rects) > 1:
        used = [clips[k % len(clips)] for k in range(len(rects))]
        if all(c["kind"] == "kenburns" for c in used):
            raise ValueError(f"{tpl}: every panel is ken-burns; keep >=1 animated clip per grid")
    parts, feed, panel_labels = [], [], []   # feed: list of ("clip"|"img", path)

    def add_input(kind, path):
        feed.append((kind, path))
        return len(feed) - 1

    if mode == "split_page":
        idx = add_input("clip", clips[0]["path"])
        parts.append(_temporal(idx, dur, clips[0]["motion"], _clip_len(clips[0]["path"]), "t0"))
        parts.append(f"[t0]{_panel_fill_full()}[full]")
        parts.append(f"[full]split={len(rects)}" + "".join(f"[s{k}]" for k in range(len(rects))))
        for k, (x, y, w, h) in enumerate(rects):
            parts.append(f"[s{k}]crop={w}:{h}:{x}:{y}[p{k}]")
            panel_labels.append((f"p{k}", x, y))
    elif mode == "fracture":
        c = clips[0]
        idx = add_input("clip", c["path"])
        parts.append(_temporal(idx, dur, c["motion"], _clip_len(c["path"]), "t0"))
        parts.append(f"[t0]split={len(rects)}" + "".join(f"[f{k}]" for k in range(len(rects))))
        anchors = c["anchors"] or [(1.0, 0.5, 0.5)] * len(rects)
        for k, (x, y, w, h) in enumerate(rects):
            z, bx, by = anchors[k % len(anchors)]
            parts.append(_panel_fill(f"f{k}", f"p{k}", w, h, z, bx, by))
            panel_labels.append((f"p{k}", x, y))
    else:  # single / fill_each — one input per panel (clip or ken-burns)
        for k, (x, y, w, h) in enumerate(rects):
            c = clips[k % len(clips)]
            pw, ph = (PAGE_W, PAGE_H) if bleed else (w, h)
            if c["kind"] == "kenburns":
                idx = add_input("img", c["path"])
                parts.append(_kenburns(idx, f"p{k}", pw, ph, dur, c["bias"]))
            else:
                idx = add_input("clip", c["path"])
                parts.append(_temporal(idx, dur, c["motion"], _clip_len(c["path"]), f"t{idx}"))
                parts.append(_panel_fill(f"t{idx}", f"p{k}", pw, ph, c["zoom"], *c["bias"]))
            panel_labels.append((f"p{k}", x, y))

    border = None if bleed else border_png(rects, Path(work_dir) / f"_brd_{out_path.stem}.png")
    cap_path = furniture_png(cap, cap_spec, Path(work_dir) / f"_cap_{out_path.stem}.png")

    if bleed:
        chain = "p0"
    else:
        parts.append(f"color=c=0x{PAPER[0]:02X}{PAPER[1]:02X}{PAPER[2]:02X}:s={PAGE_W}x{PAGE_H}:r={FPS}:d={dur}[bg]")
        prev = "bg"
        for n, (lbl, x, y) in enumerate(panel_labels):
            parts.append(f"[{prev}][{lbl}]overlay={x}:{y}[o{n}]"); prev = f"o{n}"
        parts.append(f"[{prev}][BORDER]overlay=0:0[withb]"); chain = "withb"

    if cap_path:
        parts.append(f"[CAP]format=rgba,fade=in:st={fade_st}:d=0.3:alpha=1[capf]")
        parts.append(f"[{chain}][capf]overlay=0:0,format=yuv420p[outv]")
    else:
        parts.append(f"[{chain}]format=yuv420p[outv]")

    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for kind, path in feed:
        if kind == "img":
            cmd += ["-loop", "1", "-framerate", str(FPS), "-t", str(dur), "-i", str(path)]
        else:
            cmd += ["-i", str(path)]
    nin = len(feed)
    if border:
        cmd += ["-loop", "1", "-framerate", str(FPS), "-t", str(dur), "-i", str(border)]
    if cap_path:
        cmd += ["-loop", "1", "-framerate", str(FPS), "-t", str(dur), "-i", str(cap_path)]

    fc = ";".join(parts)
    if border:
        fc = fc.replace("[BORDER]", f"[{nin}:v]"); nin += 1
    if cap_path:
        fc = fc.replace("[CAP]", f"[{nin}:v]")

    cmd += ["-filter_complex", fc, "-map", "[outv]", "-r", str(FPS),
            "-c:v", "libx264", "-crf", "18", "-preset", "medium", str(out_path)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"segment {out_path.name} ({tpl}) failed:\n{r.stderr[-900:]}")
    return out_path


def _panel_fill_full():
    return f"scale={PAGE_W}:{PAGE_H}:force_original_aspect_ratio=increase,crop={PAGE_W}:{PAGE_H},setsar=1"
