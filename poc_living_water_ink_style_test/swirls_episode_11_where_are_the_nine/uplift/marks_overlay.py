"""ep11 uplift pencil layer (Python port of the spec's 'swirls_kit': graphite + one red mark, wobble, 2-pass rings, boil).
Usage: python marks_overlay.py --animatic|--final
Reads work/base_<mode>.mp4, draws the marks on frames in their windows only (pixels elsewhere are untouched),
muxes the SHIPPED audio stream with -c:a copy, writes ep08_uplift_<mode>.mp4 (or animatic).
Clip pixels outside the thin pencil strokes are never altered."""
import json, math, random, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

EP = Path(__file__).resolve().parent.parent
UP = EP / "uplift"
MODE = "final"
W, H, FPS = 1080, 1920, 30
SHIPPED = EP / "swirls_episode_11_where_are_the_nine_final_piano_sfx.mp4"
GRAPHITE, RED = (0x4A, 0x46, 0x40), (0xA8, 0x43, 0x2F)

# ---------------------------------------------------------------- geometry helpers
def wob(pts, seed, amp=1.6, step=22):
    """resample a polyline every `step` px, jitter by +-amp, Catmull-Rom smooth."""
    rnd = random.Random(seed)
    P = [np.array(p, float) for p in pts]
    out = [P[0]]
    for a, b in zip(P[:-1], P[1:]):
        L = np.linalg.norm(b - a); n = max(1, int(L // step))
        for k in range(1, n + 1):
            out.append(a + (b - a) * k / n)
    out = [out[0]] + [q + np.array([rnd.uniform(-amp, amp), rnd.uniform(-amp, amp)]) for q in out[1:]]
    if len(out) < 3:
        return out
    sm = []
    ext = [out[0]] + out + [out[-1]]
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        for t in np.linspace(0, 1, 5, endpoint=False):
            sm.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    sm.append(out[-1])
    return sm

def ellipse_pts(cx, cy, rx, ry, a0=-100, a1=275, seed=0):
    rnd = random.Random(seed)
    n = 40
    pts = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        r = 1 + rnd.uniform(-0.012, 0.012)
        pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)))
    return pts

def rect_pts(x0, y0, x1, y1, seed=0):
    return [(x0, y0), (x1, y0 + 2), (x1 + 3, y1), (x0 - 2, y1 + 3), (x0 + 3, y0 - 4)]

def arrow_pts(a, b, bend=0.0):
    ax, ay = a; bx, by = b
    mx, my = (ax + bx) / 2, (ay + by) / 2
    dx, dy = bx - ax, by - ay
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    c = (mx + nx * bend * L, my + ny * bend * L)
    return [a, c, b]

def head(a, b, size=34, spread=28):
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    return [(b[0] - size * math.cos(ang - math.radians(spread)), b[1] - size * math.sin(ang - math.radians(spread))), b,
            (b[0] - size * math.cos(ang + math.radians(spread)), b[1] - size * math.sin(ang + math.radians(spread)))]

def plen(pts):
    return sum(math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in zip(pts[:-1], pts[1:]))

def truncate(pts, frac):
    if frac >= 1:
        return pts
    tgt = plen(pts) * max(frac, 0.0); acc = 0.0; out = [pts[0]]
    for p, q in zip(pts[:-1], pts[1:]):
        L = math.hypot(q[0] - p[0], q[1] - p[1])
        if acc + L >= tgt:
            t = (tgt - acc) / L if L else 0
            out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)); return out
        acc += L; out.append(q)
    return out

def eye_strokes(cx, cy, w):
    top = [(cx - w, cy), (cx - w * .5, cy - w * .42), (cx, cy - w * .55), (cx + w * .5, cy - w * .42), (cx + w, cy)]
    bot = [(cx - w, cy), (cx - w * .5, cy + w * .38), (cx, cy + w * .5), (cx + w * .5, cy + w * .38), (cx + w, cy)]
    pup = ellipse_pts(cx, cy, w * .22, w * .22, 0, 360)
    return [top, bot, pup]

# ---------------------------------------------------------------- MARKS (pixel coords on the 1080x1920 frame)
def S(pts, t0, dur, width=5, tone="g", second=False, dash=False, seed=0):
    return dict(pts=pts, t0=t0, dur=dur, width=width, tone=tone, second=second, dash=dash, seed=seed)

def foot(cx, cy, s=1.0, ang=0):
    """tiny footprint: sole ellipse + heel dot, as two stroke point lists, rotated by ang (deg, 0 = toes up)"""
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a)
    def R(x, y): return (cx + (x * ca - y * sa) * s, cy + (x * sa + y * ca) * s)
    sole = [R(x, y) for x, y in ellipse_pts(0, -10, 11, 20, 0, 360, seed=int(cx))]
    heel = [R(x, y) for x, y in ellipse_pts(0, 21, 7, 7, 0, 360, seed=int(cy))]
    return [sole, heel]

def figure(cx, base_y, h, seed=0):
    """empty pencil outline of a standing man (head circle + robe outline), cx = centre, base_y = feet line"""
    w = h * 0.32
    head = ellipse_pts(cx, base_y - h * 0.9, h * 0.085, h * 0.085, 0, 360, seed=seed)
    body = [(cx - w * .45, base_y - h * 0.78), (cx + w * .45, base_y - h * 0.78), (cx + w * .6, base_y - h * 0.38),
            (cx + w * .55, base_y), (cx - w * .55, base_y), (cx - w * .6, base_y - h * 0.38), (cx - w * .45, base_y - h * 0.78)]
    return [head, body]

MARKS = []
# M1 S5 dashed distance line + 2 end ticks, F01B (S03 273-378), "distance,"@11.62 -> f349, start f347
MARKS.append(dict(id="M1", device="S5 distance line", shot="S03", word="distance,", word_t=11.62, until=373,
    strokes=[S([(290, 1596), (290, 1644)], 347, 4, width=5), dict(special="dash", pts=[(298, 1620), (652, 1620)], t0=349, dur=12, key="M1"),
             S([(660, 1596), (660, 1644)], 361, 4, width=5)]))
# M2 S5 nine footprints then one turned-back pair, F05 (S08 891-1070), "Nine"@29.94 -> f898 start f896; "One"@31.52 -> f946
f9 = []
for i in range(9):
    for k, pts in enumerate(foot(190 + i * 92, 1735, 1.0, 90)):
        f9.append(S(pts, 896 + i * 3, 3, width=4, seed=i * 2 + k))
f1 = []
for j, x in enumerate((640, 740)):
    for k, pts in enumerate(foot(x, 1815, 1.0, -90)):
        f1.append(S(pts, 946 + j * 3, 3, width=4, seed=40 + j * 2 + k))
MARKS.append(dict(id="M2", device="S5 nine prints + one turned back", shot="S08", word="Nine", word_t=29.94, until=1065, strokes=f9 + f1))
# M3 S5 nine empty pencil outlines along the road, F07B (S11 1416-1518), "nine?"@49.50 -> f1485 start f1483
pts9 = [(150, 1390, 100), (260, 1350, 92), (380, 1312, 84), (500, 1282, 76), (620, 1258, 68), (720, 1232, 60), (800, 1198, 54), (868, 1160, 48), (918, 1122, 42)]
st = []
for i, (x, y, h) in enumerate(pts9):
    for k, pts in enumerate(figure(x, y, h, seed=i)):
        st.append(S(pts, 1483 + i * 2, 5, width=4, seed=i * 2 + k))
MARKS.append(dict(id="M3", device="S5 nine empty outlines", shot="S11", word="nine?", word_t=49.50, until=1513, strokes=st))
# M4 S3 red circle on baked "stranger", F08 (S12 1518-1656), "stranger."@54.70 -> f1641 start f1639
STR = json.loads((UP / "geom.json").read_text())["stranger"] if (UP / "geom.json").exists() else [622, 1815, 95, 34]
MARKS.append(dict(id="M4", device="S3 circle RED", shot="S12", word="stranger.", word_t=54.70, until=1651, tone="r",
    strokes=[S(ellipse_pts(STR[0], STR[1], STR[2], STR[3], -100, 262, seed=3), 1639, 12, width=6, tone="r", second=True)]))
# M5 S2 underline under baked "faith.", F10 (S15 1998-2235), "faith."@72.34 -> f2170 start f2168
FAI = json.loads((UP / "geom.json").read_text())["faith"] if (UP / "geom.json").exists() else [612, 1876, 722, 1874]
MARKS.append(dict(id="M5", device="S2 underline", shot="S15", word="faith.", word_t=72.34, until=2230,
    strokes=[S([(FAI[0], FAI[1]), (FAI[2], FAI[3])], 2168, 10)]))
MARKS.sort(key=lambda m: m["strokes"][0]["t0"])

# ---------------------------------------------------------------- raster
GRAIN = np.random.default_rng(7).uniform(0.78, 1.0, (H, W)).astype(np.float32)

def seg_mask(strokes_pts, width, scale=2):
    im = Image.new("L", (W * scale, H * scale), 0)
    d = ImageDraw.Draw(im)
    for pts in strokes_pts:
        q = [(x * scale, y * scale) for x, y in pts]
        if len(q) > 1:
            d.line(q, fill=255, width=int(width * scale), joint="curve")
        r = width * scale / 2
        for x, y in (q[0], q[-1]):
            d.ellipse([x - r, y - r, x + r, y + r], fill=255)
    return im.resize((W, H), Image.LANCZOS)

def dash_split(pts, dash=20, gap=16):
    out, acc, on, cur = [], 0.0, True, [pts[0]]
    for p, q in zip(pts[:-1], pts[1:]):
        L = math.hypot(q[0] - p[0], q[1] - p[1]); pos = 0.0
        while pos < L:
            lim = (dash if on else gap) - acc
            step = min(lim, L - pos)
            pos += step; acc += step
            pt = (p[0] + (q[0] - p[0]) * pos / L, p[1] + (q[1] - p[1]) * pos / L)
            if on: cur.append(pt)
            if acc >= (dash if on else gap) - 1e-6:
                if on: out.append(cur)
                on = not on; acc = 0.0; cur = [pt]
    if on and len(cur) > 1: out.append(cur)
    return out

def ease(t):
    t = min(max(t, 0), 1); return t * t * (3 - 2 * t)

def sightline_pts(base_rgb, A=(972.0, 892.0), B=(615.0, 1240.0)):
    """straight line eye -> man, lifted (48 px gap) wherever it crosses the blue contour ring."""
    A = np.array(A, float); B = np.array(B, float)
    L = np.linalg.norm(B - A); u = (B - A) / L
    blue = []
    for s in np.arange(0, L, 2.0):
        x, y = A + u * s
        xi, yi = int(x), int(y)
        patch = base_rgb[max(0, yi - 10):yi + 10, max(0, xi - 10):xi + 10].astype(int)
        if patch.size and ((patch[..., 2] - patch[..., 0]) > 30).any():
            blue.append(s)
    gaps = []
    if blue:
        grp = [[blue[0], blue[0]]]
        for s in blue[1:]:
            if s - grp[-1][1] <= 6: grp[-1][1] = s
            else: grp.append([s, s])
        gaps = [((a0 + a1) / 2) for a0, a1 in grp]
    segs, cur_s = [], 0.0
    for g in gaps:
        if g - 24 > cur_s: segs.append((cur_s, g - 24))
        cur_s = g + 24
    if cur_s < L: segs.append((cur_s, L))
    return [[tuple(A + u * s0), tuple(A + u * s1)] for s0, s1 in segs if s1 - s0 > 6], gaps, (A, B)

def render_frame(f, rgb, sight_cache):
    out = None
    for m in MARKS:
        t_first = min(st.get("t0", 1e9) for st in m["strokes"])
        if f < t_first or f > m["until"]:
            continue
        fade = min(1.0, (m["until"] - f) / 5.0)
        seed_k = (f // 4) % 2
        acc = np.zeros((H, W), np.float32); acc_red = np.zeros((H, W), np.float32)
        for st in m["strokes"]:
            if "special" in st:
                segs = [st["pts"]]
                p = ease((f - st["t0"]) / st["dur"])
                if p <= 0: continue
                total = sum(plen(s) for s in segs); drawn = total * p; used = 0
                parts = []
                for s in segs:
                    Ls = plen(s)
                    if used + Ls <= drawn: parts.append(s)
                    elif used < drawn: parts.append(truncate(s, (drawn - used) / Ls))
                    used += Ls
                dashed = []
                for s in parts:
                    dashed += dash_split(wob(s, 5 + seed_k, 1.2), 20, 16)
                mk = np.asarray(seg_mask(dashed, 4), np.float32) / 255
                acc = np.maximum(acc, mk); continue
            p = ease((f - st["t0"]) / st["dur"]) if st["dur"] > 1 else (1.0 if f >= st["t0"] else 0.0)
            if f < st["t0"]: continue
            pts = wob(st["pts"], st.get("seed", 0) * 13 + seed_k * 101 + sum(map(ord, m["id"])), 1.6)
            mk = np.asarray(seg_mask([truncate(pts, p)], st["width"]), np.float32) / 255
            if st["second"]:
                pts2 = [(x + 1.5, y + 1.5) for x, y in wob(st["pts"], 77 + seed_k, 1.6)]
                mk = np.maximum(mk, 0.35 * np.asarray(seg_mask([truncate(pts2, p)], st["width"]), np.float32) / 255)
            if st["tone"] == "r": acc_red = np.maximum(acc_red, mk)
            else: acc = np.maximum(acc, mk)
        for mask, col, op in ((acc, GRAPHITE, 0.82), (acc_red, RED, 0.85)):
            if mask.max() <= 0: continue
            a = (mask * op * fade * GRAIN)[..., None]
            c = np.array(col, np.float32) / 255
            rgb = (rgb.astype(np.float32) * (1 - a * (1 - c))).clip(0, 255).astype(np.uint8)
    return rgb

def main():
    base = UP / "work" / "base_final.mp4"
    out = UP / "ep11_uplift_final.mp4"
    sc = {}
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(base), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", str(SHIPPED), "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p",
                            "-c:a", "copy", "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
    n = 0
    while True:
        buf = dec.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        rgb = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        rgb = render_frame(n, rgb, sc)
        enc.stdin.write(rgb.tobytes()); n += 1
    enc.stdin.close(); enc.wait(); dec.wait()
    print("frames", n, "->", out)

if __name__ == "__main__":
    main()
