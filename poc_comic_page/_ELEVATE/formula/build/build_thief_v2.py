"""build_thief_v2.py - v2: the Thief film as real comic PAGES (2-4 live panels on screen together), writes thief_episode_v2.json.
Page plan (38 s):  A hook page (4 panels) > B three-stack > C mocker big+2 > [mocker face punch] > D diagonal split page > E prayer 2-stack >
F hope big+2 > [Jesus splash, still] > [answer splash, clean] > G Jesus+thief 2-stack > H "you" 2-stack > [dawn hold].
  .venv\\Scripts\\python.exe poc_comic_page/_ELEVATE/formula/build/build_thief_v2.py"""
import json, sys
from pathlib import Path
HERE = Path(__file__).parent; sys.path.insert(0, str(HERE))
from geo import FW, FH, to_pic, to_screen
from build_thief import shot, P, keyed, anc, SH, FULL, pills
from pages import page_layout


def build():
    scenes, tr, dd, tracks = [], [], [], {}
    pb = lambda i: pills[i]["box"]
    S2 = page_layout("stack2"); S3 = page_layout("stack3")
    # ---------- A: hook page, 4 panels (Jesus wide, then paradise / mocker / thief) ----------
    J = P("J", dict(SH["j1"], cx=.58, cy=.465, z0=1.0, z1=1.12, f_z1=113), [50, 520, 980, 420], mount=2, tilt=-1)
    PD = P("PD", shot("paradise_dawn", 0.0, 31, .5, .4, 1.0, 1.15, 31, 113), [50, 968, 308, 900], mount=31, tilt=1)
    M = P("M", shot("mocker_thief_face", 0.0, 54, .5, .42, 1.2, 1.4, 54, 113), [386, 968, 308, 900], mount=54, tilt=-1)
    T = P("T", SH["pen"], [722, 968, 308, 900], mount=56, tilt=1.5)
    scenes.append(dict(id="pgA", f0=0, f1=117, paper=True, panels=[J, PD, M, T], moves=[
        dict(kind="panel_slam", panel="J", at=2, shake=8), dict(kind="panel_slam", panel="PD", at=31, shake=0), dict(kind="panel_slam", panel="M", at=54, shake=0),
        dict(kind="panel_slam", panel="T", at=56, shake=8), dict(kind="panel_dive", panel="T", at=98, frames=12)]))
    dd += [dict(kind="ink_splat", at=2, until=98, pos=dict(xy=[1058, 960]), r=16, seed=1, tone="ink", dir=90),
           dict(kind="ink_splat", at=54, until=98, pos=dict(xy=[540, 1896]), r=14, seed=2, tone="ink", dir=90)]
    # ---------- B: two stacked panels: the crosses / a criminal on his cross ----------
    A = P("A", shot("two_thieves_wide", 0.0, 113, .5, .3, 1.0, 1.12, 113, 153), S2[0], mount=113)
    Bp = P("B", shot("thief_looks_to_jesus", 0.0, 123, .6, .22, 1.8, 1.9, 123, 215), S2[1], mount=123, tilt=.8)
    scenes.append(dict(id="pgB", f0=113, f1=215, paper=True, panels=[A, Bp], moves=[dict(kind="panel_slam", panel="B", at=123, shake=8), dict(kind="panel_dive", panel="A", at=198, frames=10)]))
    tr.append(dict(kind="whip_pan", **{"from": "pgA", "to": "pgB"}, at=113, frames=4, dir="up"))
    # ---------- C: mocker page (big + 2 small) ----------
    BG = [40, 40, 1000, 1060]; SM1 = [40, 1128, 486, 752]; SM2 = [554, 1128, 486, 752]; SMW = [40, 1128, 1000, 752]
    moc = dict(SH["moc"], cx=.5, cy=.30, z0=1.1, z1=1.2)
    Cb = P("big", moc, BG, mount=209); C1 = P("s1", shot("penitent_thief_face", 0.0, 209, .42, .40, 1.2, 1.4, 209, 327), SMW, mount=214, tilt=-.6)
    scenes.append(dict(id="pgC", f0=209, f1=327, paper=True, panels=[Cb, C1], moves=[dict(kind="panel_slam", panel="s1", at=214, shake=8)]))
    tr.append(dict(kind="slam_cut", **{"from": "pgB", "to": "pgC"}, at=209, frames=6, tilt=3))
    MK = [(209, 492, 657), (233, 523, 654), (250, 535, 662), (264, 481, 600), (280, 390, 520), (296, 270, 460), (300, 240, 430), (310, 150, 330), (318, 110, 260), (327, 70, 180)]
    tracks["mocker_mouth"] = keyed(SH["moc"], FULL, MK, 209, 327); tracks["mocker_head"] = keyed(SH["moc"], FULL, MK, 209, 327, off=(-20, -100))
    mo = lambda tn, scr: anc("pgC", "big", scr, 233, FULL, SH["moc"], tn)
    dd += [dict(kind="pill_edge", at=pills[2]["f0"], until=pills[2]["f1"], style="spiky", pill=pb(2), radius=46, tone="ink", seed=4),
           dict(kind="shout_fan", at=233, until=322, pops=[233, 264, 273, 314], big=[2], arc=[-45, 20], inner=120, n=6, tone="bone", **mo("mocker_mouth", (523, 654))),
           dict(kind="speed_lines", at=264, until=300, mode="focus", r0=380, arc=[150, 270], n=9, tone="bone", **mo("mocker_mouth", (523, 654))),
           dict(kind="jolt", at=264, amp=8, frames=4),
           dict(kind="drops", at=314, frames=13, n=3, dir=230, tone="bone", **mo("mocker_head", (503, 554)))]
    # ---------- mocker face punch (full-bleed) ----------
    scenes.append(dict(id="mface", f0=322, f1=378, panels=[P("main", SH["mface"], FULL, mount=322, border=0)]))
    tr.append(dict(kind="speed_zoom", **{"from": "pgC", "to": "mface"}, at=322, frames=5, center=[400, 500], lines_arc=[95, 335]))
    dd += [dict(kind="drops", at=331, frames=24, n=3, dir=40, tone="bone", **anc("mface", "main", (850, 640), 331, FULL, SH["mface"])),
           dict(kind="motion_ticks", at=348, frames=14, dir=270, n=3, len=110, tone="bone", seed=5, **anc("mface", "main", (90, 780), 348, FULL, SH["mface"])),
           dict(kind="motion_ticks", at=348, frames=14, dir=270, n=3, len=110, tone="bone", seed=6, **anc("mface", "main", (990, 780), 348, FULL, SH["mface"]))]
    # ---------- D: diagonal-gutter page (ink-slash split), framed ----------
    L = P("L", SH["mface"], FULL, mount=378, border=0, filter=dict(f0=406, f1=414, brightness=.55, saturate=.35))
    R = P("R", SH["pen2"], FULL, mount=378, border=0, filter=dict(f0=406, f1=414, brightness=1.08, saturate=1.0))
    scenes.append(dict(id="pgD", type="split", f0=378, f1=461, margin=40, panels=[L, R], slash=dict(p0=[762, 0], p1=[318, 1920], width=84, gutter=26, frames=6),
                       shifts=[dict(at=406, frames=8, dx=-150), dict(at=436, frames=12, dx=-700)], hatch=dict(at=406, frames=10, pitch=46, opacity=.75)))
    tr.append(dict(kind="ink_slash_split", **{"from": "mface", "to": "pgD"}, at=378, frames=6))
    # ---------- E: prayer page (2 stacked): thief praying / Jesus listens ----------
    E1 = P("top", shot("confession_face_hands", 0.0, 448, .55, .45, 1.05, 1.2, 448, 561), S2[0], mount=449, tilt=-.6)
    E2 = P("bot", shot("jesus_turns_to_thief", 1.0, 453, .6, .5, 1.0, 1.1, 453, 561), S2[1], mount=453, tilt=.6)
    scenes.append(dict(id="pgE", f0=449, f1=568, paper=True, panels=[E1, E2], moves=[dict(kind="panel_slam", panel="bot", at=453, shake=0)]))
    tr.append(dict(kind="halftone_dissolve", **{"from": "pgD", "to": "pgE"}, at=449, frames=12, mode="radial", center=[540, 500]))
    dd += [dict(kind="pill_edge", at=453, until=561, style="dashed", pill=pb(4), radius=46, seed=9),
           dict(kind="halftone_vignette", at=461, until=558, center=[540, 480], rx=500, ry=440, rmax=10.5, tone="bone", rect=[40, 40, 1000, 906], top_fade=dict(y=300, f0=546, f1=558))]
    # ---------- F: hope page (big + 2 small) ----------
    kg = dict(SH["king"], f_start=561)
    F1 = P("big", kg, BG, mount=558)
    F2 = P("s1", shot("penitent_thief_face", 2.0, 558, .35, .42, 1.3, 1.45, 558, 674), SM1, mount=558, tilt=-1)
    F3 = P("s2", shot("paradise_dawn", 0.0, 647, .5, .4, 1.0, 1.15, 647, 674), SM2, mount=647, tilt=1)
    scenes.append(dict(id="pgF", f0=558, f1=674, paper=True, panels=[F1, F2, F3], moves=[dict(kind="panel_slam", panel="s2", at=648, shake=8)]))
    tr.append(dict(kind="page_flip_up", **{"from": "pgE", "to": "pgF"}, at=558, frames=10))
    ray = anc("pgF", "big", (540, 280), 600, FULL, SH["king"])
    dd.append(dict(kind="rays", at=572, until=642, mode="soft", clear_r=200, len=300, arc=[45, 135], n=6, opacity=.75, tone="two", seed=12, **ray))
    # ---------- Jesus' line: shipped pixels + static splash border only ----------
    scenes.append(dict(id="jesus", f0=664, f1=796, splash=dict(inset=22, width=10), panels=[
        P("main", SH["jes"], FULL, mount=664, border=0, show=[664, 674]),
        P("shipped", shot("shipped_ref", 674 / 30, 674, .5, .5, 1.0, 1.0, 674, 796), FULL, mount=674, border=0, show=[674, 796])]))
    tr.append(dict(kind="border_fall", **{"from": "pgF", "to": "jesus"}, at=664, frames=10))
    scenes.append(dict(id="answer", f0=796, f1=892, panels=[P("main", SH["ans"], FULL, mount=796, border=0)]))
    tr.append(dict(kind="punch_cut", **{"from": "jesus", "to": "answer"}, at=796, frames=0))
    # ---------- G: Jesus + thief page, "With Him" joins the panels ----------
    G1 = P("top", shot("risen_mercy_hand", 0.0, 882, .5, .32, 1.0, 1.1, 882, 960), S2[0], mount=882)
    G2 = P("bot", shot("thief_looks_to_jesus", 0.0, 882, .6, .22, 1.9, 2.0, 882, 960), S2[1], mount=882, tilt=-1.5)
    scenes.append(dict(id="pgG", f0=882, f1=968, paper=True, panels=[G1, G2], moves=[dict(kind="panel_join", panel="bot", at=944, frames=8, to_box=[40, 868, 1000, 906], tilt=-2.5, arc=90)]))
    tr.append(dict(kind="iris", **{"from": "answer", "to": "pgG"}, at=882, frames=10, center=[606, 740], ring=False))
    # ---------- H: "you can ask" page: kneelers + the thief's prayer echo ----------
    H1 = P("top", shot("us_under_cross_shadow", 0.0, 960, .5, .30, 1.0, 1.1, 960, 1050), S2[0], mount=958)
    H2 = P("bot", shot("confession_face_hands", 0.0, 960, .55, .42, 1.05, 1.15, 960, 1062), S2[1], mount=958, tilt=.6)
    scenes.append(dict(id="pgH", f0=958, f1=1062, paper=True, panels=[H1, H2]))
    tr.append(dict(kind="page_flip_up", **{"from": "pgG", "to": "pgH"}, at=958, frames=10))
    dd += [dict(kind="speed_lines", at=992, until=1012, mode="focus", r0=330, arc=[175, 365], n=8, tone="ink", seed=9, **anc("pgH", "top", (540, 420), 992, S2[0], H1["shot"])),
           dict(kind="pill_edge", at=1002, until=1040, style="dashed", pill=pb(9), radius=46, seed=10)]
    # ---------- hold ----------
    scenes.append(dict(id="dawn", f0=1050, f1=1140, paper=True, panels=[P("main", SH["dawn"], FULL, mount=1050, border=0)], moves=[dict(kind="page_settle", panel="main", at=1104, frames=12, scale=.93, tilt=-.7)]))
    tr.append(dict(kind="halftone_dissolve", **{"from": "pgH", "to": "dawn"}, at=1050, frames=12, mode="rise", center=[540, 960]))
    dd.append(dict(kind="border_build", at=1068, until=1140, frames_per_side=8, tone="two", seed=7, box=[20, 20, 1060, 1900]))

    # ---------- no-draw masks (screen boxes, per window) ----------
    jh = to_pic((930, 1010), FULL, SH["moc"], 250)
    def jmask(f0, f1, fr):
        x, y = to_screen(jh, BG, moc, fr); return dict(label="far_Jesus_pgC", box=[int(x - 150), int(y - 150), 300, 330], f0=f0, f1=f1)
    no_draw = [dict(label="pgA_J_eyes", box=J["box"], f0=2, f1=99), dict(label="jesus_line_shot", box=[0, 0, FW, FH], f0=664, f1=796), dict(label="answer_shot", box=[0, 0, FW, FH], f0=796, f1=892),
               dict(label="pgE_Jesus_panel", box=[int(v) for v in S2[1]], f0=453, f1=568), dict(label="pgG_Jesus_panel", box=[int(v) for v in S2[0]], f0=882, f1=968),
               jmask(209, 268, 233), jmask(268, 327, 300)]
    ep = dict(fps=30, frames=1140, assets="comic_thief", scenes=scenes, transitions=tr, doodles=dd, tracks=tracks, no_draw=no_draw,
              pills=[dict(png=p["png"], f0=p["f0"], f1=p["f1"], box=p["box"], radius=p["radius"]) for i, p in enumerate(pills) if i != 6], hook=dict(png="pills/hook.png", f0=0, f1=66),
              gates=dict(anchor=dict(scene="pgC", panel="big", track="mocker_mouth", keys={str(f): [x, y] for f, x, y in MK[1:6]})))
    (HERE / "thief_episode_v2.json").write_text(json.dumps(ep, indent=1)); print("v2 ok", len(scenes), "scenes", len(dd), "doodles")


if __name__ == "__main__":
    build()
