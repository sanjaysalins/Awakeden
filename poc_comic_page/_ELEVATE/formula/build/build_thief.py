"""build_thief.py - writes thief_episode.json (the data the Remotion kit renders) for the 38 s Thief short.
Beats/devices follow COMIC_FULL_DESIGN.md section 2 with the owner decision: answer_light_profile (26.53-29.40 s) is KEPT clean
(Option B): no shatter / bleed / burst / crack there; punch_cut into it, iris out of it.
Run with the repo venv:  .venv\\Scripts\\python.exe poc_comic_page/_ELEVATE/formula/build/build_thief.py"""
import json, sys, math
from pathlib import Path
import numpy as np, cv2
HERE = Path(__file__).parent; sys.path.insert(0, str(HERE))
from geo import FW, FH, view, to_pic, to_screen, clamp
ROOT = Path(r"F:\slk\PycharmProjects\JesusInTheBible"); PUB = ROOT / "_remotion/public/comic_thief"
FULL = [0, 0, FW, FH]
pills = json.load(open(HERE / "pills.json"))


def shot(clip, t_in, f_start, cx, cy, z0, z1, f_z0=None, f_z1=None, freeze=None):
    return dict(clip=clip, t_in=t_in, f_start=f_start, cx=cx, cy=cy, z0=z0, z1=z1, f_z0=f_start if f_z0 is None else f_z0, f_z1=f_z1, freeze_f=freeze)


# shipped shot table (build_s32.SH) as exact segment boundaries
B = [0, 57, 113, 153, 208, 326, 378, 448, 561, 674, 796, 882, 960, 1050, 1140]
SH = dict(
    j1=shot("jesus_turns_to_thief", 0.0, 0, .55, .42, 1.3, 1.5, 0, 57), pen=shot("penitent_thief_face", 0.0, 57, .42, .42, 1.3, 1.5, 57, 113),
    two=shot("two_thieves_wide", 0.0, 113, .5, .5, 1.0, 1.12, 113, 153), gol=shot("golgotha_hill_wide", 0.0, 148, .5, .5, 1.0, 1.15, 153, 208),
    moc=shot("mocker_taunts_jesus", 0.5, 208, .5, .42, 1.15, 1.35, 208, 326), mface=shot("mocker_thief_face", 0.0, 326, .5, .42, 1.5, 1.7, 326, 378),
    pen2=shot("penitent_thief_face", 1.0, 378, .42, .45, 1.3, 1.5, 378, 448), conf=shot("confession_face_hands", 0.0, 448, .55, .55, 1.3, 1.5, 448, 561),
    king=shot("kingdom_light_clouds", 0.0, 561, .5, .4, 1.1, 1.3, 561, 674), jes=shot("jesus_turns_to_thief", 1.5, 674, .5, .42, 1.2, 1.4, 674, 796),
    ans=shot("answer_light_profile", 0.0, 796, .45, .5, 1.2, 1.4, 796, 882), risen=shot("risen_mercy_hand", 0.0, 882, .5, .45, 1.2, 1.4, 882, 960),
    us=shot("us_under_cross_shadow", 0.0, 960, .5, .5, 1.0, 1.2, 960, 1050), dawn=shot("paradise_dawn", 0.0, 1050, .5, .5, 1.05, 1.25, 1050, 1140, freeze=1116),
)


def P(id, shot_, box, mount=None, tilt=0, border=9, **kw):
    d = dict(id=id, shot=shot_, box=box, tilt=tilt, border=border);
    if mount is not None: d["mount"] = mount
    d.update(kw); return d


# ---- clip frame cache for tracking (half-res grey) ----
_cache = {}


def frames_of(clip):
    if clip not in _cache:
        cap = cv2.VideoCapture(str(PUB / (clip + ".mp4"))); fr = []
        while True:
            ok, im = cap.read()
            if not ok: break
            fr.append(cv2.resize(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY), (540, 960)))
        _cache[clip] = fr
    return _cache[clip]


def track(sh, box, ref_f, scr_center, f0, f1, off_scr=(0, 0), half=40):
    """doc `anchor`: matchTemplate per source frame. Tracks the patch at scr_center (screen px at ref_f); returns pic pts for f0..f1
    of the point (patch centre + off_scr), offset kept constant in picture space."""
    fr = frames_of(sh["clip"]); n = len(fr)
    idx = lambda f: (round(sh["t_in"] * 30) + (f - sh["f_start"])) % n
    pic0 = to_pic(scr_center, box, sh, ref_f); vx, vy, S, _, _ = view(box, sh, ref_f)
    off_pic = (off_scr[0] / (FW * S), off_scr[1] / (FH * S))
    cx, cy = pic0[0] * 540, pic0[1] * 960
    tpl = fr[idx(ref_f)][int(cy - half):int(cy + half), int(cx - half):int(cx + half)]
    pts = {ref_f: (pic0[0], pic0[1])}
    for rng in (range(ref_f + 1, f1 + 1), range(ref_f - 1, f0 - 1, -1)):
        px, py = cx, cy
        for f in rng:
            img = fr[idx(f)]; R = 70
            x0, y0 = int(max(0, px - half - R)), int(max(0, py - half - R)); x1, y1 = int(min(540, px + half + R)), int(min(960, py + half + R))
            win = img[y0:y1, x0:x1]
            if win.shape[0] <= tpl.shape[0] or win.shape[1] <= tpl.shape[1]: pts[f] = (px / 540, py / 960); continue
            res = cv2.matchTemplate(win, tpl, cv2.TM_CCOEFF_NORMED); _, mv, _, ml = cv2.minMaxLoc(res)
            if mv > 0.35: px, py = x0 + ml[0] + half, y0 + ml[1] + half
            pts[f] = (px / 540, py / 960)
    return dict(f0=f0, pts=[[round(pts[f][0] + off_pic[0], 5), round(pts[f][1] + off_pic[1], 5)] for f in range(f0, f1 + 1)])


def keyed(sh, box, keys, f0, f1, off=(0, 0)):
    """hand-keyed anchor (screen px at chosen frames, read off the shipped film), linear in picture space between keys."""
    ks = sorted(keys); pic = [(f, to_pic((x + off[0], y + off[1]), box, sh, f)) for f, x, y in ks]; out = []
    for f in range(f0, f1 + 1):
        a = max([k for k in pic if k[0] <= f], key=lambda k: k[0], default=pic[0]); b = min([k for k in pic if k[0] >= f], key=lambda k: k[0], default=pic[-1])
        t = 0 if b[0] == a[0] else (f - a[0]) / (b[0] - a[0]); out.append([round(a[1][0] + (b[1][0] - a[1][0]) * t, 5), round(a[1][1] + (b[1][1] - a[1][1]) * t, 5)])
    return dict(f0=f0, pts=out)


def anc(scene, panel, scr, ref_f, box, sh, track_name=None):
    p = to_pic(scr, box, sh, ref_f); a = dict(scene=scene, panel=panel, pic=[round(p[0], 5), round(p[1], 5)])
    if track_name: a["track"] = track_name
    return dict(pos=dict(anchor=a))


def build():
    scenes, tr, dd, tracks = [], [], [], {}
    # ---------- 1 page1 (cards 1-2) ----------
    j = P("J", dict(SH["j1"], cx=.58, cy=.465, z0=1.0, z1=1.12, f_z1=113), [60, 470, 960, 470], mount=2, tilt=-1)
    m = P("M", shot("mocker_thief_face", 0.0, 54, .5, .3, 1.15, 1.3, 54, 113), [555, 1290, 465, 350], mount=54, tilt=2)
    t = P("T", SH["pen"], [60, 1290, 465, 350], mount=56, tilt=-2)
    scenes.append(dict(id="page1", f0=0, f1=117, paper=True, panels=[j, m, t], moves=[
        dict(kind="panel_slam", panel="J", at=2, shake=8), dict(kind="panel_slam", panel="M", at=54, shake=0), dict(kind="panel_slam", panel="T", at=56, shake=8),
        dict(kind="panel_dive", panel="T", at=71, frames=12)]))
    # ---------- 2 page2 (card 3-4) ----------
    A = P("A", SH["two"], [40, 60, 1000, 1800], mount=113); Bp = P("B", SH["gol"], [40, 1980, 1000, 1800], mount=148)
    scenes.append(dict(id="page2", f0=113, f1=215, paper=True, page_h=3840, panels=[A, Bp], moves=[dict(kind="page_glide", at=148, frames=10, dy=1920)]))
    tr.append(dict(kind="whip_pan", **{"from": "page1", "to": "page2"}, at=113, frames=4, dir="up"))
    # ---------- 3 mocker (card 5) ----------
    scenes.append(dict(id="mocker", f0=209, f1=327, panels=[P("main", SH["moc"], FULL, mount=209, border=0)]))
    tr.append(dict(kind="slam_cut", **{"from": "page2", "to": "mocker"}, at=209, frames=6, tilt=3))
    # ---------- 4 mocker face (card 6) ----------
    scenes.append(dict(id="mface", f0=322, f1=378, panels=[P("main", SH["mface"], FULL, mount=322, border=0)]))
    tr.append(dict(kind="speed_zoom", **{"from": "mocker", "to": "mface"}, at=322, frames=5, center=[520, 700], lines_arc=[95, 335]))
    # ---------- 5 split (card 7) ----------
    L = P("L", SH["mface"], FULL, mount=378, border=0, filter=dict(f0=406, f1=414, brightness=.55, saturate=.35))
    R = P("R", SH["pen2"], FULL, mount=378, border=0, filter=dict(f0=406, f1=414, brightness=1.08, saturate=1.0))
    scenes.append(dict(id="split", type="split", f0=378, f1=461, panels=[L, R], slash=dict(p0=[762, 0], p1=[318, 1920], width=84, gutter=26, frames=6),
                       shifts=[dict(at=406, frames=8, dx=-150), dict(at=436, frames=12, dx=-700)], hatch=dict(at=406, frames=10, pitch=46, opacity=.75)))
    tr.append(dict(kind="ink_slash_split", **{"from": "mface", "to": "split"}, at=378, frames=6))
    # ---------- 6 confession (card 8) ----------
    scenes.append(dict(id="conf", f0=449, f1=568, panels=[P("main", SH["conf"], FULL, mount=449, border=0)]))
    tr.append(dict(kind="halftone_dissolve", **{"from": "split", "to": "conf"}, at=449, frames=12, mode="radial", center=[600, 1240]))
    # ---------- 7 kingdom (card 9-10) ----------
    scenes.append(dict(id="king", f0=558, f1=674, paper=True, panels=[P("main", SH["king"], FULL, mount=558)], moves=[dict(kind="pull_out_to_page", panel="main", at=648, frames=10, box=[260, 220, 560, 700], tilt=-1)]))
    tr.append(dict(kind="page_flip_up", **{"from": "conf", "to": "king"}, at=558, frames=10))
    # ---------- 8 Jesus' line: splash border only (card 11) ----------
    # Jesus' line: pixels from the shipped film itself (zoompan resampling cannot match 2.0), pill baked in, only the static splash border is added
    scenes.append(dict(id="jesus", f0=664, f1=796, splash=dict(inset=22, width=10), panels=[
        P("main", SH["jes"], FULL, mount=664, border=0, show=[664, 674]),
        P("shipped", shot("shipped_ref", 674 / 30, 674, .5, .5, 1.0, 1.0, 674, 796), FULL, mount=674, border=0, show=[674, 796])]))
    tr.append(dict(kind="border_fall", **{"from": "king", "to": "jesus"}, at=664, frames=10))
    # ---------- 9 answer_light_profile: KEPT, nothing drawn (Option B) ----------
    scenes.append(dict(id="answer", f0=796, f1=892, panels=[P("main", SH["ans"], FULL, mount=796, border=0)]))
    tr.append(dict(kind="punch_cut", **{"from": "jesus", "to": "answer"}, at=796, frames=0))
    # ---------- 10 page4 (card 14) ----------
    PJ = P("J", shot("risen_mercy_hand", 0.0, 882, .5, .30, 1.05, 1.15, 882, 960), [60, 210, 960, 730], mount=882, tilt=0)
    PT = P("T", shot("thief_looks_to_jesus", 0.0, 882, .6, .23, 1.9, 2.0, 882, 960), [60, 1290, 300, 280], mount=882, tilt=-2)
    scenes.append(dict(id="page4", f0=882, f1=968, paper=True, panels=[PJ, PT], moves=[dict(kind="panel_join", panel="T", at=944, frames=8, to_box=[30, 680, 300, 280], tilt=-3)]))
    tr.append(dict(kind="iris", **{"from": "answer", "to": "page4"}, at=882, frames=10, center=[606, 740], ring=False))
    # ---------- 11 us under cross (card 15) ----------
    scenes.append(dict(id="us", f0=958, f1=1062, panels=[P("main", SH["us"], FULL, mount=958, border=0)]))
    tr.append(dict(kind="page_flip_up", **{"from": "page4", "to": "us"}, at=958, frames=10))
    # ---------- 12 dawn (card 16) ----------
    scenes.append(dict(id="dawn", f0=1050, f1=1140, paper=True, panels=[P("main", SH["dawn"], FULL, mount=1050, border=0)], moves=[dict(kind="page_settle", panel="main", at=1104, frames=12, scale=.93, tilt=-.7)]))
    tr.append(dict(kind="halftone_dissolve", **{"from": "us", "to": "dawn"}, at=1050, frames=12, mode="rise", center=[540, 960]))

    pb = lambda i: pills[i]["box"]
    # ================= doodles =================
    # card 1: splats in the gutters
    dd += [dict(kind="ink_splat", at=2, until=71, pos=dict(xy=[1034, 972]), r=18, seed=1, tone="ink", dir=80),
           dict(kind="ink_splat", at=54, until=71, pos=dict(xy=[1040, 1340]), r=18, seed=2, tone="ink"),
           dict(kind="ink_splat", at=56, until=71, pos=dict(xy=[62, 1665]), r=20, seed=3, tone="ink")]
    # card 2: "Why?" shock crown round the penitent head (full-bleed shipped view, anchored)
    dd.append(dict(kind="shock_lines", at=102, until=112, tone="ink", n=8, arc=[200, 340], r0=520, r1=[620, 700], seed=3,
                   **anc("page1", "T", (420, 820), 102, FULL, SH["pen"])))
    # card 3: border_build round each thief (anchored to the page-2 panel A picture)
    boxA = [40, 60, 1000, 1800]
    def pb2(x0, y0, x1, y1, f=120):
        return [list(to_pic((x0, y0), boxA, SH["two"], f)), list(to_pic((x1, y1), boxA, SH["two"], f))]
    dd.append(dict(kind="border_build", at=116, until=152, frames_per_side=8, tone="two", seed=2, box=[60, 390, 270, 940], pic_box=pb2(60, 390, 270, 940), anchor=dict(scene="page2", panel="A", pic=[0, 0])))
    dd.append(dict(kind="border_build", at=123, until=152, frames_per_side=8, tone="two", seed=5, box=[770, 400, 1010, 950], pic_box=pb2(770, 400, 1010, 950), anchor=dict(scene="page2", panel="A", pic=[0, 0])))
    # card 5: mocker shouts
    MK = [(209, 492, 657), (233, 523, 654), (250, 535, 662), (264, 481, 600), (280, 390, 520), (296, 270, 460), (300, 240, 430), (310, 150, 330), (318, 110, 260), (327, 70, 180)]
    tracks["mocker_mouth"] = keyed(SH["moc"], FULL, MK, 209, 327)
    tracks["mocker_head"] = keyed(SH["moc"], FULL, MK, 209, 327, off=(-20, -100))
    mo = lambda tn, scr: anc("mocker", "main", scr, 233, FULL, SH["moc"], tn)
    dd += [dict(kind="ink_splat", at=210, until=322, pos=dict(xy=[84, 150]), r=26, seed=2, tone="ink"), dict(kind="ink_splat", at=211, until=322, pos=dict(xy=[1000, 160]), r=22, seed=3, tone="bone"),
           dict(kind="pill_edge", at=pills[2]["f0"], until=pills[2]["f1"], style="spiky", pill=pb(2), radius=46, tone="ink", seed=4),
           dict(kind="shout_fan", at=233, until=322, pops=[233, 264, 273, 314], big=[2], arc=[-88, -4], n=6, tone="bone", **mo("mocker_mouth", (523, 654))),
           dict(kind="speed_lines", at=264, until=300, mode="focus", r0=420, arc=[150, 270], n=9, tone="bone", **mo("mocker_mouth", (523, 654))),
           dict(kind="jolt", at=264, amp=8, frames=4),
           dict(kind="drops", at=314, frames=13, n=3, dir=230, kind2="sweat", tone="bone", **mo("mocker_head", (503, 554)))]
    # card 6: mocker face close-up
    dd += [dict(kind="drops", at=331, frames=24, n=3, dir=40, tone="bone", **anc("mface", "main", (850, 640), 331, FULL, SH["mface"])),
           dict(kind="motion_ticks", at=348, frames=14, dir=270, n=3, len=110, tone="bone", seed=5, **anc("mface", "main", (90, 780), 348, FULL, SH["mface"])),
           dict(kind="motion_ticks", at=348, frames=14, dir=270, n=3, len=110, tone="bone", seed=6, **anc("mface", "main", (990, 780), 348, FULL, SH["mface"]))]
    # card 8: whisper edge + hush
    dd += [dict(kind="pill_edge", at=453, until=561, style="dashed", pill=pb(4), radius=46, seed=9),
           dict(kind="halftone_vignette", at=461, until=558, center=[600, 1240], rx=470, ry=560, rmax=10.5, tone="bone", top_fade=dict(y=700, f0=546, f1=558))]
    # card 9: soft rays from the light gap
    dd.append(dict(kind="rays", at=572, until=642, mode="soft", pos=dict(xy=[540, 280]), clear_r=230, len=320, arc=[45, 135], n=6, opacity=.75, tone="two", seed=12))
    # card 15-16
    dd += [dict(kind="speed_lines", at=992, until=1012, mode="focus", pos=dict(xy=[540, 800]), r0=520, arc=[175, 365], n=8, tone="ink", seed=9),
           dict(kind="pill_edge", at=1002, until=1040, style="dashed", pill=pb(9), radius=46, seed=10),
           dict(kind="border_build", at=1068, until=1140, frames_per_side=8, tone="two", seed=7, box=[20, 20, 1060, 1900])]
    for d in dd:
        if d.get("kind2"): d.pop("kind2")
    no_draw = [dict(label="jesus_line_shot", box=[0, 0, FW, FH], f0=664, f1=796), dict(label="answer_light_profile_shot", box=[0, 0, FW, FH], f0=796, f1=892),
               dict(label="panelJ_risen_face", box=[60, 210, 960, 730], f0=882, f1=968), dict(label="panelJ_page1_eyes", box=[60, 470, 960, 470], f0=2, f1=72),
               dict(label="far_Jesus_on_mocker_shot", box=[780, 900, 300, 330], f0=209, f1=327)]
    ep = dict(fps=30, frames=1140, assets="comic_thief", scenes=scenes, transitions=tr, doodles=dd, tracks=tracks, no_draw=no_draw,
              pills=[dict(png=p["png"], f0=p["f0"], f1=p["f1"], box=p["box"], radius=p["radius"]) for i, p in enumerate(pills) if i != 6], hook=dict(png="pills/hook.png", f0=0, f1=66))
    (HERE / "thief_episode.json").write_text(json.dumps(ep, indent=1)); print("episode ok", len(scenes), "scenes", len(dd), "doodles")


if __name__ == "__main__":
    build()
