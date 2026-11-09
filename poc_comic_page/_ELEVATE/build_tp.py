"""ELEVATE bake-off 1, $0: Today in Paradise. Same audio in every arm (shipped film's mix, 59.07s).
  .venv\\Scripts\\python.exe poc_comic_page/_ELEVATE/build_tp.py <arm>     arm in B0 L S P R1 W
Control R0 = shipped film (copied). B0 = rebuilt base (same beats, full-bleed push, old grey-pill lettering).
L = B0 + new lettering. S = B0 + fast cut-ins. P = B0 + split panels. R1 = L+S+P. W = Fable's blind recipe (tp/W_recipe.json)."""
import json, sys, math, subprocess, shutil
from pathlib import Path
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_arms as BA
HERE = BA.HERE; ROOT = BA.ROOT
EP = ROOT / "batches/cluster_01_cross/today_paradise_luke2343"; CL = EP / "visual/clips"
FILM = EP / "visual/today_paradise_luke2343_sfx_v5hook.mp4"; TOTAL = 59.07
INK, GOLD, WHITE, GREY = BA.INK, BA.GOLD, BA.WHITE, (225, 225, 228); BANG, KAL = BA.BANG, BA.KAL
run = BA.run
FADE = 0.10


# ---------- shot rendering ----------
def zp(z0, z1, n, cx, cy, size):
    return "zoompan=z='%.4f+(%.4f)*in/%d':x='max(0,min(iw-iw/zoom,%.4f*iw-iw/zoom/2))':y='max(0,min(ih-ih/zoom,%.4f*ih-ih/zoom/2))':d=1:s=%s:fps=30" % (z0, z1 - z0, n, cx, cy, size)


def render_shot(out, clip, t_in, dur, cx, cy, z0, z1, band=None):
    n = max(2, int(round(dur * 30))); pre = "scale=1080:1920,fps=30"
    if band is None: vf = pre + "," + zp(z0, z1, n, cx, cy, "1080x1920")
    else:
        cyl = min(1, max(0, (cy * 1920 - band) / 960)); vf = pre + ",crop=1080:960:0:%d," % band + zp(z0, z1, n, cx, cyl, "1080x960")
    run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-ss", "%.2f" % t_in, "-i", CL / (clip + ".mp4"), "-vf", vf + ",format=yuv420p", "-frames:v", n, "-an",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", out])


def render_split(out, top, bot, dur):
    parts = []
    for k, p in enumerate((top, bot)):
        o = out.with_name(out.stem + "_%d.mp4" % k); clip, t_in, cx, cy, z0, z1 = p
        band = int(min(960, max(0, cy * 1920 - 480))); render_shot(o, clip, t_in, dur, cx, cy, z0, z1, band); parts.append(o)
    run(["ffmpeg", "-y", "-v", "error", "-i", parts[0], "-i", parts[1], "-filter_complex", "[0:v][1:v]vstack,drawbox=x=0:y=950:w=1080:h=20:color=0xE8A81C:t=fill[v]",
         "-map", "[v]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", out])


# ---------- lettering ----------
def canvas(): return Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))


def pill(path, text, ref=None, speaker="narrator"):  # OLD style: grey pill, no tail (today's lettering)
    img = canvas(); d = ImageDraw.Draw(img); f = KAL(54); words = text.split(); lines = BA.wrap(d, words, f, 820)[:3]
    h = 60 + 62 * len(lines); y0 = 1000
    jesus = speaker == "jesus"
    d.rounded_rectangle((70, y0, 1010, y0 + h), 46, fill=(BA.IVORY if jesus else GREY) + (255,) if hasattr(BA, "IVORY") else GREY + (255,), outline=INK + (255,), width=5)
    y = y0 + 28
    for ln in lines:
        t = " ".join(ln); d.text((540 - d.textlength(t, font=f) / 2, y), t, font=f, fill=INK); y += 62
    if ref:
        tf = KAL(30); tw = d.textlength(ref, font=tf); d.rounded_rectangle((90, y0 - 26, 90 + tw + 36, y0 + 24), 18, fill=GOLD, outline=INK, width=3); d.text((108, y0 - 24), ref, font=tf, fill=INK)
    img.save(path)


def round_balloon(path, text, cx, top, tail_to, size=76, maxw=800, hi=()):
    img = canvas(); d = ImageDraw.Draw(img); f = BANG(size); lh = int(size * 1.08); lines = BA.wrap(d, text.upper().split(), f, maxw); h = len(lines) * lh
    x0, x1, y0, y1 = cx - maxw / 2 - 50, cx + maxw / 2 + 50, top, top + h + 70
    tx, ty = tail_to; bx = min(max(cx + (tx - cx) * 0.4, x0 + 90), x1 - 90); up = ty < y0
    base = y0 + 4 if up else y1 - 4; tail = [(bx - 45, base), (tx, ty), (bx + 45, base)]
    d.rounded_rectangle((x0, y0, x1, y1), 70, fill=WHITE, outline=INK, width=9)
    d.polygon(tail, fill=WHITE); d.line([tail[0], tail[1], tail[2]], fill=INK, width=9, joint="curve")
    d.line([(bx - 40, base), (bx + 40, base)], fill=WHITE, width=14)
    BA.draw_lines(d, lines, f, cx, y0 + 34, lh, hi); img.save(path)


def caption_box(path, text, top, size=64, maxw=800, hi=()):
    img = canvas(); d = ImageDraw.Draw(img); f = BANG(size); lh = int(size * 1.1); lines = BA.wrap(d, text.upper().split(), f, maxw); h = len(lines) * lh
    d.rectangle((540 - maxw / 2 - 40, top, 540 + maxw / 2 + 40, top + h + 50), fill=(250, 240, 214), outline=INK, width=8)
    BA.draw_lines(d, lines, f, 540, top + 22, lh, hi); img.save(path)


def light_text(path, text, top, size=88, maxw=860):
    img = canvas(); d = ImageDraw.Draw(img); f = BANG(size); lh = int(size * 1.1); lines = BA.wrap(d, text.upper().split(), f, maxw)
    y = top
    for ln in lines:
        t = " ".join(ln); x = 540 - d.textlength(t, font=f) / 2
        d.text((x, y), t, font=f, fill=(255, 238, 190), stroke_width=9, stroke_fill=(40, 22, 4)); y += lh
    img.save(path)


# ---------- script lines ----------
# (t0, t1, speaker, text, ref, anchor(clip, ax, ay) or None, hi)
LINES = [
    (0.04, 2.9, "narrator", "Two criminals died beside Jesus that afternoon", None, None, ()),
    (2.9, 5.2, "narrator", "Same nails. Same hill.", None, None, ()),
    (5.2, 7.84, "narrator", "Same distance. Opposite eternities.", None, None, ("OPPOSITE",)),
    (7.84, 12.04, "narrator", "Both guilty. Both spoke.", None, None, ()),
    (12.04, 15.32, "mocker", "If thou be Christ, save thyself and us", "LUKE 23:39", ("mocker_taunts_jesus", .41, .27), ()),
    (15.32, 18.82, "narrator", "The other thief rebuked him", None, None, ("REBUKED",)),
    (18.82, 23.0, "thief", "And we indeed justly; for we receive the due reward of our deeds:", "LUKE 23:40", ("two_thieves_wide", .17, .22), ()),
    (23.0, 27.4, "thief", "but this man hath done nothing amiss.", "LUKE 23:41", ("two_thieves_wide", .17, .22), ()),
    (27.4, 32.01, "narrator", "A confession. A verdict: innocent. Then one request.", None, None, ("INNOCENT",)),
    (32.01, 36.37, "thief", "Lord, remember me when thou comest into thy kingdom", "LUKE 23:42", None, ("REMEMBER",)),
    (36.37, 41.4, "jesus", "Verily I say unto thee, To day shalt thou be with me in paradise", "LUKE 23:43", None, ()),
    (41.4, 46.35, "narrator", "He asked for someday. Jesus gave him that same afternoon.", None, None, ("SOMEDAY", "AFTERNOON")),
    (46.35, 50.51, "narrator", "No merit. Just repentance and trust. We are all one of those two men.", None, None, ()),
    (50.51, 53.95, "narrator", "Ask what the thief asked. Remember me.", None, None, ()),
    (53.95, 57.09, "narrator", "Hear his answer. With me. Today.", None, None, ("WITH", "TODAY")),
    (57.09, 59.07, "narrator", "Paradise", None, None, ("PARADISE",)),
]
B0 = [(0, 2.9, "golgotha_hill_wide"), (2.9, 5.2, "nail_through_hand"), (5.2, 7.84, "thief_looks_to_jesus"), (7.84, 12.04, "mocker_thief_face"),
      (12.04, 15.32, "mocker_taunts_jesus"), (15.32, 18.82, "penitent_thief_face"), (18.82, 26.77, "two_thieves_wide"), (26.77, 32.01, "confession_face_hands"),
      (32.01, 36.37, "kingdom_light_clouds"), (36.37, 42.81, "jesus_turns_to_thief"), (42.81, 46.35, "risen_mercy_hand"), (46.35, 48.77, "nail_through_hand"),
      (48.77, 50.51, "golgotha_hill_wide"), (50.51, 53.95, "penitent_thief_face"), (53.95, 57.09, "answer_light_profile"), (57.09, 59.07, "paradise_dawn")]
# fast rhythm: (t0, t1, clip, t_in, cx, cy, z0, z1)
S_SHOTS = [(0, 1.5, "golgotha_hill_wide", 0, .5, .5, 1.0, 1.15), (1.5, 2.9, "golgotha_hill_wide", 1.0, .49, .17, 2.3, 2.7),
           (2.9, 4.04, "nail_through_hand", 0, .85, .67, 2.0, 2.3), (4.04, 5.2, "two_thieves_wide", 0, .5, .5, 1.0, 1.1),
           (5.2, 6.8, "thief_looks_to_jesus", 0, .6, .22, 2.0, 2.2), (6.8, 7.84, "thief_looks_to_jesus", 1.5, .5, .5, 1.0, 1.15),
           (7.84, 10.0, "mocker_thief_face", 0, .55, .3, 1.9, 2.3), (10.0, 12.04, "penitent_thief_face", 0, .3, .3, 2.0, 2.2),
           (12.04, 13.6, "mocker_taunts_jesus", 0, .41, .27, 2.2, 2.5), (13.6, 15.32, "mocker_taunts_jesus", 1.0, .7, .6, 2.2, 2.4),
           (15.32, 17.0, "penitent_thief_face", 0.5, .3, .3, 1.8, 2.1), (17.0, 18.82, "penitent_thief_face", 1.5, .27, .55, 2.0, 2.3),
           (18.82, 21.4, "two_thieves_wide", 0, .5, .5, 1.0, 1.15), (21.4, 24.0, "two_thieves_wide", 1.0, .17, .24, 2.6, 2.9), (24.0, 26.77, "two_thieves_wide", 2.0, .5, .22, 2.2, 2.5),
           (26.77, 29.2, "confession_face_hands", 0, .54, .58, 1.8, 2.0), (29.2, 30.6, "confession_face_hands", 1.5, .95, .45, 2.2, 2.4), (30.6, 32.01, "penitent_thief_face", 2.0, .3, .3, 2.4, 2.6),
           (32.01, 34.2, "kingdom_light_clouds", 0, .5, .3, 1.6, 1.9), (34.2, 36.37, "kingdom_light_clouds", 1.5, .5, .5, 1.0, 1.2),
           (36.37, 39.0, "jesus_turns_to_thief", 0, .57, .4, 1.8, 2.1), (39.0, 40.8, "jesus_turns_to_thief", 1.5, .15, .2, 2.2, 2.4), (40.8, 42.81, "jesus_turns_to_thief", 2.5, .5, .5, 1.0, 1.2),
           (42.81, 44.6, "risen_mercy_hand", 0, .5, .35, 1.7, 1.9), (44.6, 46.35, "risen_mercy_hand", 1.5, .7, .9, 2.0, 2.4),
           (46.35, 48.77, "nail_through_hand", 0.5, .5, .55, 1.6, 1.8), (48.77, 50.51, "golgotha_hill_wide", 2.0, .49, .17, 2.3, 2.6),
           (50.51, 52.3, "us_under_cross_shadow", 0, .5, .5, 1.0, 1.3), (52.3, 53.95, "penitent_thief_face", 2.5, .3, .3, 2.3, 2.5),
           (53.95, 55.6, "answer_light_profile", 0, .35, .6, 1.7, 2.0), (55.6, 57.09, "answer_light_profile", 1.5, .6, .15, 2.2, 2.0),
           (57.09, 59.07, "paradise_dawn", 0, .5, .5, 1.0, 1.25)]
# splits (t0, t1, top, bottom, stamp, stamp_time)
SPLITS = [(2.9, 7.84, ("mocker_thief_face", 0, .55, .3, 1.4, 1.6), ("penitent_thief_face", 0, .3, .35, 1.4, 1.6), "SAME NAILS. SAME HILL.", 3.0),
          (36.37, 42.81, ("penitent_thief_face", 1.0, .3, .3, 1.4, 1.6), ("jesus_turns_to_thief", 0, .57, .4, 1.4, 1.6), "ASKED SOMEDAY. GOT TODAY.", 36.5),
          (53.95, 57.09, ("penitent_thief_face", 2.0, .3, .3, 1.4, 1.6), ("risen_mercy_hand", 0, .5, .35, 1.4, 1.6), "WITH ME. TODAY.", 54.0)]


def shot_at(shots, t, clip=None):
    for s in shots:
        if s["t0"] <= t < s["t1"] and (clip is None or s.get("clip") == clip): return s
    for s in shots:
        if s["t0"] <= t < s["t1"]: return s


def to_screen(s, ax, ay):
    z = (s["z0"] + s["z1"]) / 2; vx = min(max(s["cx"] - 0.5 / z, 0), 1 - 1 / z); vy = min(max(s["cy"] - 0.5 / z, 0), 1 - 1 / z)
    return (ax - vx) * z * 1080, (ay - vy) * z * 1920


def make_overlays(arm_dir, shots, new_lettering, splits):
    ov = []; arm_dir.mkdir(parents=True, exist_ok=True)
    in_split = lambda t: any(a <= t < b for a, b, *_ in splits)
    for i, (t0, t1, spk, text, ref, anchor, hi) in enumerate(LINES):
        p = arm_dir / ("ln%02d.png" % i)
        if not new_lettering: pill(p, text, ref, spk); ov.append((str(p), t0, t1)); continue
        sp = in_split(t0)
        if spk == "narrator": caption_box(p, text, 90 if sp else 110, hi=hi)
        elif spk == "jesus": light_text(p, text, 1280 if sp else 1250)
        else:
            top = 1180; s = shot_at(shots, t0 + 0.1, anchor[0] if anchor else None) if anchor else None
            if anchor and s and s.get("clip") == anchor[0]:
                tx, ty = to_screen(s, anchor[1], anchor[2]); tx = min(max(tx, 80), 1000); ty = min(max(ty, 400), 1100)
            else: tx, ty = 40, 1000     # speaker off-panel: tail points to the edge
            (BA.jagged_balloon(p, text, 540, top, (tx, ty), hi=hi, size=78, maxw=780) if spk == "mocker" else round_balloon(p, text, 540, top, (tx, ty), hi=hi))
        ov.append((str(p), t0, t1))
        if new_lettering and ref and spk != "narrator":
            r = arm_dir / ("rf%02d.png" % i); BA.refchip(r, ref, 1790); ov.append((str(r), t0, t1))
    for k, (t0, t1, top, bot, stamp, st) in enumerate(splits):
        if not new_lettering and False: continue
        sp = arm_dir / ("stamp%d.png" % k); BA.label(sp, stamp, 905, 52); ov.append((str(sp), st, t1))
    return ov


def compose(name, shots, overlays):
    W = HERE / "work" / ("tp_" + name); W.mkdir(parents=True, exist_ok=True); segs = []
    for k, s in enumerate(shots):
        o = W / ("s%02d.mp4" % k); d = round(s["t1"] - s["t0"], 3)
        if "split" in s: t, b = s["split"]; render_split(o, (t["clip"], t["t_in"], t["cx"], t["cy"], t["z0"], t["z1"]), (b["clip"], b["t_in"], b["cx"], b["cy"], b["z0"], b["z1"]), d)
        else: render_shot(o, s["clip"], s["t_in"], d, s["cx"], s["cy"], s["z0"], s["z1"])
        segs.append(o)
    (W / "l.txt").write_text("".join("file '%s'\n" % x.as_posix() for x in segs)); run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", W / "l.txt", "-c", "copy", W / "base.mp4"])
    ins = ["-i", W / "base.mp4"]; fc = ""; prev = "[0:v]"; n = 1; loop = ["-loop", "1", "-framerate", "30", "-t", "%.2f" % TOTAL]
    for i, (png, t0, t1) in enumerate(overlays):
        ins += loop + ["-i", png]
        fc += "[%d:v]format=rgba,fade=in:st=%.2f:d=%.2f:alpha=1,fade=out:st=%.2f:d=%.2f:alpha=1[o%d];%s[o%d]overlay=x=0:y=0:eof_action=pass:enable='between(t,%.2f,%.2f)'[p%d];" % (n, t0, FADE, max(t0, t1 - FADE), FADE, i, prev, i, t0, t1, i)
        prev = "[p%d]" % i; n += 1
    fc += prev + "null[out]"; out = HERE / "arms" / ("TP_%s.mp4" % name); out.parent.mkdir(exist_ok=True)
    run(["ffmpeg", "-y", "-v", "error", *ins, "-i", FILM, "-filter_complex", fc, "-map", "[out]", "-map", "%d:a" % n, "-t", "%.2f" % TOTAL, "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", out])
    print("built", out)


def shots_from(rows):
    return [dict(t0=r[0], t1=r[1], clip=r[2], t_in=r[3], cx=r[4], cy=r[5], z0=r[6], z1=r[7]) for r in rows]


def apply_splits(shots, splits):
    out = [s for s in shots if not any(a <= s["t0"] < b for a, b, *_ in splits)]
    for a, b, top, bot, stamp, st in splits:
        mk = lambda p: dict(clip=p[0], t_in=p[1], cx=p[2], cy=p[3], z0=p[4], z1=p[5]); out.append(dict(t0=a, t1=b, split=[mk(top), mk(bot)]))
    return sorted(out, key=lambda s: s["t0"])


def main(arm):
    if arm == "R0": (HERE / "arms").mkdir(exist_ok=True); shutil.copy(FILM, HERE / "arms" / "TP_R0.mp4"); print("R0 copied"); return
    b0 = shots_from([(a, b, c, 0.0, .5, .5, 1.0, 1.12) for a, b, c in B0])
    if arm in ("W", "W2"):
        global FADE
        FADE = 0.04 if arm == "W2" else 0.10
        r = json.load(open(HERE / "tp" / (arm + "_recipe.json"), encoding="utf-8")); shots = r["shots"]; ov = []; d = HERE / "work" / ("tp_%s_lett" % arm); d.mkdir(parents=True, exist_ok=True)
        for i, o in enumerate(r["overlays"]):
            p = d / ("o%02d.png" % i); k = o["kind"]; tx, ty = (o["tail"] if o.get("tail") else (40, o["top"] + 100)); hi = tuple(w.upper() for w in o.get("hi", []))
            if k == "jag": BA.jagged_balloon(p, o["text"], 540, o["top"], (tx, ty), hi=hi, size=78, maxw=780)
            elif k == "round": round_balloon(p, o["text"], 540, o["top"], (tx, ty), hi=hi)
            elif k == "caption": caption_box(p, o["text"], o["top"], hi=hi)
            elif k == "light": light_text(p, o["text"], o["top"])
            elif k == "ref": BA.refchip(p, o["text"], o["top"])
            elif k == "stamp": BA.label(p, o["text"], o["top"], 52)
            ov.append((str(p), o["t0"], o["t1"]))
        compose(arm, shots, ov); return
    new_l = arm in ("L", "R1"); fast = arm in ("S", "R1"); spl = arm in ("P", "R1")
    shots = shots_from(S_SHOTS) if fast else b0
    splits = SPLITS if spl else []
    if spl: shots = apply_splits(shots, splits)
    ov = make_overlays(HERE / "work" / ("tp_" + arm + "_lett"), shots, new_l, splits)
    compose(arm, shots, ov)


if __name__ == "__main__":
    main(sys.argv[1])
