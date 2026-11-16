"""build_nazareth_v3.py - writes nazareth_episode_v3.json for the NazarethComicV2 composition (same kit + look as the Thief film). $0.
  .venv\\Scripts\\python.exe prophecy/02_nazareth/build/build_nazareth_v3.py
v3 = v2 + Jesus panels replace widow (pgI) and shackle (pgJ) small panels. v2: new audio 59.18 s (closing line), fewer repeats (no clip on more than 2 pages), S13 warm (S13w), S04 cropped on hands + scroll only.
Page plan (1776 frames @30): A hook > B village/reading/scroll > C poor/freedom > D roll-up > E Isaiah unread words (hush) > F every eye >
[Jesus line, S09 still] > G amazed > H townsman > I local boy / promise > J scroll / God's welcome > [S14 landing + hold]."""
import json, sys
from pathlib import Path
HERE = Path(__file__).parent
TB = Path(r"F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_ELEVATE\formula\build"); sys.path.insert(0, str(TB))
from geo import FW, FH
from pages import page_layout
FULL = [0, 0, FW, FH]; FRAMES = 1776; LAND = 1498
pills = json.load(open(HERE / "pills_v2.json"))
S2 = page_layout("stack2"); BG = [40, 40, 1000, 1060]; SMW = [40, 1128, 1000, 752]; SM1 = [40, 1128, 486, 752]; SM2 = [554, 1128, 486, 752]


def P(id, c, box, mount, t_in, cx, cy, z0=1.0, z1=1.1, end=None, tilt=0, border=9, show=None, **kw):
    end = end or mount + 120
    sh = dict(clip=c, t_in=t_in, f_start=mount, cx=cx, cy=cy, z0=z0, z1=z1, f_z0=mount, f_z1=end, freeze_f=None)
    d = dict(id=id, shot=sh, box=box, tilt=tilt, border=border, mount=mount)
    if show: d["show"] = list(show)
    d.update(kw); return d


def slam(p, at, shake=0): return dict(kind="panel_slam", panel=p, at=at, shake=shake)


def build():
    sc, tr, dd, nd = [], [], [], []
    pb = lambda i: pills[i]["box"]
    def ND(label, box, f0, f1): nd.append(dict(label=label, box=[int(v) for v in box], f0=f0, f1=f1))
    # ---- A hook (0-93): S01 + Isaiah writing (S08, first 2.5 s); S01 dives full-bleed on "sentence." ----
    sc.append(dict(id="pgA", f0=0, f1=93, paper=True, panels=[
        P("J", "S01", S2[0], 0, 0, .5, .27, 1.0, 1.1, 93, tilt=-1),
        P("W", "S08", S2[1], 0, 0, .4, .38, 1.0, 1.08, 66, tilt=1, show=[0, 66])],
        moves=[slam("J", 0, 8), slam("W", 0, 0), dict(kind="panel_dive", panel="J", at=54, frames=12)]))
    ND("A_Jesus_S01", S2[0], 0, 54); ND("A_Jesus_S01_full", FULL, 54, 89)
    dd += [dict(kind="ink_splat", at=9, until=54, pos=dict(xy=[1056, 975]), r=16, seed=1, tone="ink", dir=90)]
    # ---- B (89-238): village (2 s) > Jesus reads (S03 early) ; hands + scroll handed over (S04 hands only) ----
    sc.append(dict(id="pgB", f0=89, f1=238, paper=True, panels=[
        P("V", "S02", BG, 89, 0, .5, .35, 1.0, 1.08, 150, show=[89, 150]),
        P("L", "S03", BG, 150, 0, .5, .33, 1.0, 1.08, 225, show=[150, 225]),
        P("H", "S04", SMW, 93, 0, .5, .68, 1.0, 1.1, 225, tilt=-.8, show=[93, 225])],
        moves=[slam("V", 89, 0), slam("H", 93, 8), slam("L", 150, 8)]))
    tr.append(dict(kind="slam_cut", **{"from": "pgA", "to": "pgB"}, at=89, frames=6, tilt=3))
    ND("B_Jesus_S03", BG, 150, 225)
    dd += [dict(kind="ink_splat", at=93, until=225, pos=dict(xy=[1062, 1112]), r=16, seed=2, tone="ink", dir=90)]
    # ---- C (232-515): the poor, men listen, Jesus reads > freedom > welcome ----
    sc.append(dict(id="pgC", f0=232, f1=515, paper=True, panels=[
        P("P", "S05", BG, 232, 0, .45, .3, 1.0, 1.1, 383, show=[232, 383]),
        P("S", "S06", BG, 396, 0, .45, .42, 1.0, 1.15, 505, tilt=.6),
        P("Q", "S10", SMW, 232, 0, .6, .33, 1.0, 1.08, 324, tilt=.8, show=[232, 324]),
        P("R", "S03", SMW, 324, 0, .5, .33, 1.0, 1.08, 396, tilt=-.8, show=[324, 396])],
        moves=[slam("P", 232, 0), slam("Q", 232, 8), slam("R", 324, 8), slam("S", 396, 8)]))
    tr.append(dict(kind="page_flip_up", **{"from": "pgB", "to": "pgC"}, at=232, frames=6))
    ND("C_Jesus_S03", SMW, 324, 396)
    dd += [dict(kind="rays", at=402, until=462, mode="soft", pos=dict(xy=[760, 130]), clear_r=150, len=280, arc=[60, 130], n=5, opacity=.7, tone="two", seed=12)]
    # ---- D (505-639): Jesus rolls the scroll; attendant's hands take it ----
    sc.append(dict(id="pgD", f0=505, f1=639, paper=True, panels=[
        P("R", "S07", BG, 505, 0, .55, .3, 1.0, 1.1, 633),
        P("A", "S04", SMW, 513, 0.5, .5, .68, 1.05, 1.15, 639, tilt=-.8)], moves=[slam("R", 505, 0), slam("A", 513, 8)]))
    tr.append(dict(kind="halftone_dissolve", **{"from": "pgC", "to": "pgD"}, at=505, frames=12, mode="radial", center=[540, 500]))
    ND("D_Jesus_S07", BG, 505, 639)
    dd += [dict(kind="jolt", at=530, amp=8, frames=4), dict(kind="pill_edge", at=pills[7]["f0"], until=pills[7]["f1"], style="dashed", pill=pb(7), radius=46, seed=5)]
    # ---- E (627-800): Isaiah's unread words (halftone hush) > He leaves them unread, sits down (S09 seated, later part) ----
    sc.append(dict(id="pgE", f0=627, f1=800, paper=True, panels=[
        P("I", "S08", BG, 627, 0, .4, .35, 1.0, 1.08, 703, show=[627, 703]),
        P("J", "S09", BG, 705, 5.0, .5, .3, 1.0, 1.08, 800, show=[705, 800]),
        P("H", "S07", SMW, 639, 0, .5, .68, 1.0, 1.1, 703, tilt=.8, show=[639, 703]),
        P("B", "S07", SMW, 705, 1.5, .5, .68, 1.0, 1.1, 800, tilt=.8, show=[705, 800])],
        moves=[slam("I", 627, 0), slam("H", 639, 8), slam("J", 705, 8), slam("B", 705, 0)]))
    tr.append(dict(kind="iris", **{"from": "pgD", "to": "pgE"}, at=627, frames=10, center=[540, 500], ring=False))
    ND("E_Jesus_S09", BG, 705, 800)
    dd += [dict(kind="halftone_vignette", at=639, until=700, center=[540, 560], rx=520, ry=420, rmax=10.5, tone="bone", rect=[40, 200, 1000, 730]),
           dict(kind="pill_edge", at=pills[8]["f0"], until=pills[8]["f1"], style="dashed", pill=pb(8), radius=46, seed=9)]
    # ---- F (790-898): every eye ----
    sc.append(dict(id="pgF", f0=790, f1=898, paper=True, panels=[
        P("E", "S10", BG, 790, 0, .6, .33, 1.0, 1.1, 880, show=[790, 880]),
        P("D", "S12", SMW, 790, 0, .5, .3, 1.0, 1.1, 898, tilt=-.8)],
        moves=[slam("E", 790, 0), slam("D", 790, 8), dict(kind="panel_dive", panel="D", at=868, frames=10)]))
    tr.append(dict(kind="ink_bleed", **{"from": "pgE", "to": "pgF"}, at=790, frames=10, origin=[540, 500]))
    dd += [dict(kind="speed_lines", at=819, until=845, mode="focus", r0=300, arc=[160, 200], n=6, tone="ink", seed=9, pos=dict(xy=[620, 560])),
           dict(kind="ink_splat", at=849, until=868, pos=dict(xy=[1062, 1300]), r=16, seed=3, tone="ink", dir=90)]
    # ---- Jesus line: S09 still, static splash border only ----
    sc.append(dict(id="jesus", f0=888, f1=1043, splash=dict(inset=22, width=10), panels=[P("main", "S09", FULL, 888, 0, .5, .5, 1.0, 1.0, 1043, border=0)]))
    tr.append(dict(kind="border_fall", **{"from": "pgF", "to": "jesus"}, at=888, frames=10))
    ND("jesus_line_S09", FULL, 888, 1043)
    # ---- G (1033-1197): amazed > a local boy ----
    sc.append(dict(id="pgG", f0=1033, f1=1197, paper=True, panels=[
        P("A", "S11", BG, 1034, 0, .5, .3, 1.0, 1.1, 1184, show=[1034, 1184]),
        P("M", "S13w", SMW, 1112, 0, .3, .33, 1.0, 1.1, 1197, tilt=-.8)],
        moves=[slam("A", 1034, 0), slam("M", 1112, 8)]))
    tr.append(dict(kind="iris", **{"from": "jesus", "to": "pgG"}, at=1033, frames=10, center=[540, 640], ring=False))
    dd += [dict(kind="motion_ticks", at=1053, frames=14, dir=270, n=3, len=110, tone="ink", seed=5, pos=dict(xy=[90, 420])),
           dict(kind="motion_ticks", at=1053, frames=14, dir=270, n=3, len=110, tone="ink", seed=6, pos=dict(xy=[990, 420])),
           dict(kind="ink_splat", at=1112, until=1180, pos=dict(xy=[1062, 1300]), r=16, seed=4, tone="ink", dir=90)]
    # ---- H (1187-1277): the townsman ----
    sc.append(dict(id="pgH", f0=1187, f1=1277, paper=True, panels=[
        P("T", "S12", BG, 1187, 1.0, .5, .3, 1.0, 1.1, 1277),
        P("B", "S11", SMW, 1187, 2.0, .5, .3, 1.0, 1.1, 1277, tilt=.8)], moves=[slam("T", 1187, 0), slam("B", 1187, 8)]))
    tr.append(dict(kind="punch_cut", **{"from": "pgG", "to": "pgH"}, at=1187, frames=0))
    dd += [dict(kind="pill_edge", at=pills[14]["f0"], until=pills[14]["f1"], style="spiky", pill=pb(14), radius=46, tone="ink", seed=4), dict(kind="jolt", at=1224, amp=6, frames=4)]
    # ---- I (1271-1413): that local boy > Isaiah's promise (widow echo) ----
    sc.append(dict(id="pgI", f0=1271, f1=1413, paper=True, panels=[
        P("Y", "S13w", BG, 1271, 0, .45, .3, 1.0, 1.1, 1413),
        P("W", "S09", SMW, 1271, 2.0, .5, .28, 1.3, 1.4, 1413, tilt=-1)],
        moves=[slam("Y", 1271, 0), slam("W", 1271, 8)]))
    tr.append(dict(kind="page_flip_up", **{"from": "pgH", "to": "pgI"}, at=1271, frames=10))
    ND("I_boy_S13", BG, 1271, 1413)
    ND("I_Jesus_S09_crop", [40, 1128, 920, 752], 1271, 1413)
    dd += [dict(kind="ink_splat", at=1307, until=1413, pos=dict(xy=[1062, 1300]), r=16, seed=6, tone="ink", dir=90)]
    # ---- J (1403-1508): He stopped at God's welcome ----
    sc.append(dict(id="pgJ", f0=1403, f1=1508, paper=True, panels=[
        P("R", "S01", BG, 1403, 0.5, .5, .27, 1.0, 1.1, 1508),
        P("W", "S02", SMW, 1403, 0, .5, .3, 1.0, 1.1, 1463, tilt=.8, show=[1403, 1463]),
        P("X", "S03", SMW, 1464, 0, .5, .27, 1.5, 1.6, 1508, tilt=-.8)], moves=[slam("R", 1403, 0), slam("W", 1403, 8), slam("X", 1464, 0)]))
    tr.append(dict(kind="halftone_dissolve", **{"from": "pgI", "to": "pgJ"}, at=1403, frames=12, mode="radial", center=[540, 700]))
    ND("J_Jesus_S01", BG, 1403, 1508)
    ND("J_Jesus_S03_crop", [40, 1128, 920, 752], 1464, 1508)
    dd += [dict(kind="ink_splat", at=1431, until=1498, pos=dict(xy=[1062, 1300]), r=16, seed=7, tone="ink", dir=90)]
    # ---- landing + hold: S14 full-bleed, static border, nothing drawn ----
    sc.append(dict(id="land", f0=LAND, f1=FRAMES, splash=dict(inset=22, width=10), panels=[P("main", "S14", FULL, LAND, 0, .5, .5, 1.0, 1.0, FRAMES, border=0)]))
    tr.append(dict(kind="border_fall", **{"from": "pgJ", "to": "land"}, at=LAND, frames=10))
    ND("landing_S14", FULL, LAND, FRAMES)
    ep = dict(fps=30, frames=FRAMES, assets="comic_nazareth", scenes=sc, transitions=tr, doodles=dd, tracks={}, no_draw=nd,
              pills=[dict(png=p["png"], f0=p["f0"], f1=p["f1"], box=p["box"], radius=p["radius"]) for p in pills], hook=dict(png="pills_v2/hook.png", f0=0, f1=66))
    (HERE / "nazareth_episode_v3.json").write_text(json.dumps(ep, indent=1)); print("ok", len(sc), "scenes", len(dd), "doodles")


if __name__ == "__main__":
    build()
