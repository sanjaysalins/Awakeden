"""ep02 uplift pencil layer (Python port of the spec's 'swirls_kit': graphite + one red mark, wobble, 2-pass rings, boil).
Usage: python marks_overlay.py --animatic|--final
Reads work/base_<mode>.mp4, draws the marks on frames in their windows only (pixels elsewhere are untouched),
muxes the SHIPPED audio stream with -c:a copy, writes ep02_uplift_<mode>.mp4 (or animatic).
Clip pixels outside the thin pencil strokes are never altered."""
import json, math, random, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

EP = Path(__file__).resolve().parent.parent
UP = EP / "uplift"
MODE = "animatic" if "--animatic" in sys.argv else "final"
W, H, FPS = 1080, 1920, 30
SHIPPED = EP / "THE_ASHES_BOOK_final_sfx.mp4"
GRAPHITE, RED = (0x4A, 0x46, 0x40), (0xA8, 0x43, 0x2F)
NEW = json.loads((UP / "new_marks.json").read_text()) if (UP / "new_marks.json").exists() else {}

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

# ---------------------------------------------------------------- MARKS (pixel coords on the 1080x1920 frame, measured on the real stills)
def S(pts, t0, dur, width=5, tone="g", second=False, dash=False, seed=0):
    return dict(pts=pts, t0=t0, dur=dur, width=width, tone=tone, second=second, dash=dash, seed=seed)

def tally(t0s, dur, y0=650, y1=722, x0=560):
    """7-stroke tally: 4 verticals, a diagonal strike (5th), then 2 verticals. t0s = 7 start frames."""
    xs = [x0, x0 + 32, x0 + 64, x0 + 96]
    st = [S([(x, y0), (x + 2, y1)], t0s[k], dur, seed=k) for k, x in enumerate(xs)]
    st.append(S([(x0 - 16, y1 - 12), (x0 + 118, y0 + 14)], t0s[4], dur, seed=4))
    st.append(S([(x0 + 156, y0), (x0 + 158, y1)], t0s[5], dur, seed=5))
    st.append(S([(x0 + 188, y0), (x0 + 190, y1)], t0s[6], dur, seed=6))
    return st

MARKS = []
# M1: S1 ring round F01 top panel 3 "the burning" at "ash," (12.08)
MARKS.append(dict(id="M1", device="S1 ring", shot="S04", word="ash,", word_t=12.08, until=496,
    strokes=[S(rect_pts(708, 175, 1046, 634), 360, 10, width=6, second=True)]))
# M2: S5 tally of seven on F02C, drawn across "unclean seven days"; 5th stroke lands on "seven" (22.22)
MARKS.append(dict(id="M2", device="S5 tally x7 (F02C)", shot="S05", word="unclean", word_t=21.64, until=676,
    strokes=tally([647, 651, 655, 659, 663, 667, 671], 3)))
# M3: same tally redrawn on F02D; ring on stroke 3 at "third" (25.06), ring on stroke 7 at "seventh" (26.42)
MARKS.append(dict(id="M3", device="S5 tally + 2 rings (F02D)", shot="S06", word="third", word_t=25.06, until=853,
    strokes=tally([750, 754, 758, 772, 776, 780, 784], 3)
    + [S(ellipse_pts(624, 686, 27, 54, -100, 262, seed=11), 761, 10, width=6, second=True),
       S(ellipse_pts(748, 686, 27, 54, -100, 262, seed=12), 791, 10, width=6, second=True)]))
# M4: S3 RED circle round the baked word "stain" on F03's caption at "stain" (36.70)
MARKS.append(dict(id="M4", device="S3 circle RED", shot="S08", word="stain", word_t=36.70, until=1170, tone="r",
    strokes=[S(ellipse_pts(333, 1626, 64, 34, -100, 262, seed=3), 1099, 12, width=6, tone="r", second=True)]))
# M5: S2 underline under baked "unclean" on F05's caption at "unclean" (51.30)
MARKS.append(dict(id="M5", device="S2 underline", shot="S11", word="unclean", word_t=51.30, until=1736,
    strokes=[S([(725, 1852), (872, 1850)], 1537, 10)]))
MARKS.sort(key=lambda mm: min(st["t0"] for st in mm["strokes"]))

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
                segs, gaps, _ = sight_cache[st.get('key', 'M4')]
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
    base = UP / "work" / f"base_{MODE}.mp4"
    out = UP / (f"ep02_uplift_{MODE}.mp4")
    sc = {}
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(base), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    vid = UP / "work" / "overlay_video.mp4"
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-an", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", str(vid)], stdin=subprocess.PIPE)
    n = 0
    while True:
        buf = dec.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        rgb = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        rgb = render_frame(n, rgb, sc)
        enc.stdin.write(rgb.tobytes()); n += 1
    enc.stdin.close(); enc.wait(); dec.wait()
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(vid), "-i", str(SHIPPED), "-map", "0:v", "-map", "1:a", "-c", "copy", "-movflags", "+faststart", str(out)], check=True)
    print("frames", n, "->", out)

if __name__ == "__main__":
    main()
