"""ep07 uplift pencil layer (Python port of the spec's 'swirls_kit': graphite + one red mark, wobble, 2-pass rings, boil).
Usage: python marks_overlay.py --animatic|--final
Reads work/base_<mode>.mp4, draws the marks on frames in their windows only (pixels elsewhere are untouched),
muxes the SHIPPED audio stream with -c:a copy, writes ep07_uplift_<mode>.mp4 (or animatic).
Clip pixels outside the thin pencil strokes are never altered."""
import json, math, random, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

EP = Path(__file__).resolve().parent.parent
UP = EP / "uplift"
MODE = "animatic" if "--animatic" in sys.argv else "final"
W, H, FPS = 1080, 1920, 30
SHIPPED = EP / "swirls_episode_07_the_bier_he_touched_final_piano_sfx.mp4"
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

def tick(c, ang, r0=18, r1=52):
    a = math.radians(ang)
    return [(c[0] + r0 * math.cos(a), c[1] + r0 * math.sin(a)), (c[0] + r1 * math.cos(a), c[1] + r1 * math.sin(a))]

MARKS = []
# M1 S5 dashed gap line on F01B (S03), "distance." @13.90 -> f417-2; dashed line + two end ticks across the bare strip right of the bier
MARKS.append(dict(id="M1", device="S5 dashed gap line", shot="S03", word="distance.", word_t=13.90, until=505,
    strokes=[dict(special="gapline", pts=[(632, 1376), (700, 1376)], t0=415, dur=12),
             S([(632, 1360), (632, 1392)], 427, 3, width=4), S([(700, 1360), (700, 1392)], 428, 3, width=4)]))
# M2 S4 margin arrow on F02A (S04), "toward" @18.06 -> f542-2
A2, B2 = (840, 1700), (655, 1445)
MARKS.append(dict(id="M2", device="S4 margin arrow", shot="S04", word="toward", word_t=18.06, until=586,
    strokes=[S(arrow_pts(A2, B2, 0.12), 540, 12, width=5), S(head(arrow_pts(A2, B2, 0.12)[1], B2), 552, 3, width=5)]))
# M3 S8 tick burst on S07 F03 wide, "still." @32.44 -> f973-2, right of the bearers' feet
TC = (1000, 1420)
MARKS.append(dict(id="M3", device="S8 tick burst", shot="S07", word="still.", word_t=32.44, until=1013,
    strokes=[S(tick(TC, a_), 971 + i, 4, width=5, seed=i) for i, a_ in enumerate((-30, 0, 30))]))
# M4 S3 RED circle round the baked "Arise" on F04 (S09), "Arise." @43.90 -> f1317-2; leaves 5 f before the cut
MARKS.append(dict(id="M4", device="S3 circle RED", shot="S09", word="Arise.", word_t=43.90, until=1333, tone="r",
    strokes=[S(ellipse_pts(716, 1795, 70, 38, -100, 262, seed=3), 1315, 12, width=6, tone="r", second=True)]))
# M5 S5 reversed arrow on F06 (S11): grey arrow boy->Jesus "Death" @51.60, one cross-out "Jesus." @53.04, firm arrow Jesus->boy "Life" @54.30
MARKS.append(dict(id="M5", device="S5 reversed arrow", shot="S11", word="Death", word_t=51.60, until=1690,
    strokes=[S(arrow_pts((800, 1730), (990, 1730), 0.0), 1546, 10, width=4), S(head((800, 1730), (990, 1730), 28, 28), 1556, 3, width=4),
             S([(880, 1700), (915, 1762)], 1592, 4, width=5),
             S(arrow_pts((990, 1795), (800, 1795), 0.0), 1627, 10, width=6), S(head((990, 1795), (800, 1795), 32, 28), 1637, 3, width=6)]))
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
            if "special" in st:   # gapline: straight dashed line drawn from its first point to its last
                p = ease((f - st["t0"]) / st["dur"])
                if p <= 0: continue
                seg = truncate(wob(st["pts"], 5 + seed_k, 1.2), p)
                mk = np.asarray(seg_mask(dash_split(seg, 12, 9), 4), np.float32) / 255
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
    out = UP / (f"ep07_uplift_{MODE}.mp4")
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
