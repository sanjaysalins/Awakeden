"""build_nazareth.py - writes nazareth_episode.json for the NazarethComic composition (same kit + look as the Thief film). $0.
  .venv\\Scripts\\python.exe prophecy/02_nazareth/build/build_nazareth.py
Page plan (54.64 s, 1639 frames @30): A hook > B village+scroll > C poor/freedom > D roll-up > E Isaiah unread words (hush) > F every eye >
[Jesus line, S09 still] > G amazed > H townsman > I local boy / promise > J scroll shut > [S14 landing + 3 s hold]."""
import json, sys
from pathlib import Path
HERE = Path(__file__).parent
TB = Path(r"F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_ELEVATE\formula\build"); sys.path.insert(0, str(TB))
from geo import FW, FH
from pages import page_layout
FULL = [0, 0, FW, FH]; FRAMES = 1639
pills = json.load(open(HERE / "pills.json"))
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
    # ---- A hook (0-93): S01 + the staring men (S10); S01 dives full-bleed on "sentence." ----
    sc.append(dict(id="pgA", f0=0, f1=93, paper=True, panels=[
        P("J", "S01", S2[0], 0, 0, .5, .27, 1.0, 1.1, 93, tilt=-1),
        P("W", "S10", S2[1], 0, 0, .6, .35, 1.0, 1.08, 66, tilt=1, show=[0, 66])],
        moves=[slam("J", 0, 8), slam("W", 0, 0), dict(kind="panel_dive", panel="J", at=54, frames=12)]))
    ND("A_Jesus_S01", S2[0], 0, 54); ND("A_Jesus_S01_full", FULL, 54, 89); ND("B_Jesus_S03", BG, 147, 216)
    dd += [dict(kind="ink_splat", at=9, until=54, pos=dict(xy=[1056, 975]), r=16, seed=1, tone="ink", dir=90)]
    # ---- B (89-256): village + attendant hands over the scroll ----
    sc.append(dict(id="pgB", f0=89, f1=256, paper=True, panels=[
        P("V", "S02", BG, 89, 0, .5, .35, 1.0, 1.08, 147, show=[89, 147]),
        P("L", "S03", BG, 147, 0, .5, .33, 1.0, 1.08, 216, show=[147, 216]),
        P("I", "S08", BG, 216, 0, .4, .35, 1.0, 1.08, 256, show=[216, 256]),
        P("H", "S04", SMW, 93, 0, .5, .2, 1.0, 1.1, 244, tilt=-.8, show=[93, 244])],
        moves=[slam("V", 89, 0), slam("H", 93, 8), slam("L", 147, 8), slam("I", 216, 0)]))
    tr.append(dict(kind="slam_cut", **{"from": "pgA", "to": "pgB"}, at=89, frames=6, tilt=3))
    dd += [dict(kind="ink_splat", at=93, until=240, pos=dict(xy=[1062, 1112]), r=16, seed=2, tone="ink", dir=90)]
    # ---- C (250-515): the poor / Jesus reading > freedom > welcome ----
    sc.append(dict(id="pgC", f0=250, f1=515, paper=True, panels=[
        P("P", "S05", BG, 250, 0, .45, .3, 1.0, 1.1, 396, show=[250, 396]),
        P("S", "S06", BG, 396, 0, .45, .42, 1.0, 1.15, 505, tilt=.6),
        P("R", "S03", SMW, 250, 0, .5, .33, 1.0, 1.08, 324, tilt=.8, show=[250, 324]),
        P("W", "S02", SMW, 324, 0, .5, .3, 1.0, 1.1, 384, tilt=-.8, show=[324, 384]),
        P("Q", "S05", SMW, 396, 1.0, .45, .3, 1.0, 1.1, 505, tilt=.8)],
        moves=[slam("P", 250, 0), slam("R", 250, 8), slam("W", 324, 0), slam("S", 396, 8), slam("Q", 396, 0)]))
    tr.append(dict(kind="page_flip_up", **{"from": "pgB", "to": "pgC"}, at=250, frames=10))
    ND("C_Jesus_S03", SMW, 250, 324)
    dd += [dict(kind="rays", at=402, until=462, mode="soft", pos=dict(xy=[760, 130]), clear_r=150, len=280, arc=[60, 130], n=5, opacity=.7, tone="two", seed=12)]
    # ---- D (505-639): Jesus rolls the scroll; attendant takes it ----
    sc.append(dict(id="pgD", f0=505, f1=639, paper=True, panels=[
        P("R", "S07", BG, 505, 0, .55, .3, 1.0, 1.1, 633),
        P("A", "S04", SMW, 513, 0, .5, .62, 1.05, 1.15, 639, tilt=-.8)], moves=[slam("R", 505, 0), slam("A", 513, 8)]))
    tr.append(dict(kind="halftone_dissolve", **{"from": "pgC", "to": "pgD"}, at=505, frames=12, mode="radial", center=[540, 500]))
    ND("D_Jesus_S07", BG, 505, 639)
    dd += [dict(kind="jolt", at=530, amp=8, frames=4), dict(kind="pill_edge", at=pills[7]["f0"], until=pills[7]["f1"], style="dashed", pill=pb(7), radius=46, seed=5)]
    # ---- E (627-800): Isaiah's unread words (halftone hush) > He leaves them unread ----
    sc.append(dict(id="pgE", f0=627, f1=800, paper=True, panels=[
        P("I", "S08", BG, 627, 0, .4, .35, 1.0, 1.08, 703, show=[627, 703]),
        P("J", "S01", BG, 705, 1.0, .5, .27, 1.0, 1.08, 800, show=[705, 800]),
        P("B", "S07", SMW, 639, 0, .5, .68, 1.0, 1.1, 790, tilt=.8, show=[639, 790])],
        moves=[slam("I", 627, 0), slam("B", 639, 8), slam("J", 705, 8)]))
    tr.append(dict(kind="iris", **{"from": "pgD", "to": "pgE"}, at=627, frames=10, center=[540, 500], ring=False))
    ND("E_Jesus_S01", BG, 705, 800); ND("E_hands_S07", SMW, 639, 790)
    dd += [dict(kind="halftone_vignette", at=639, until=700, center=[540, 560], rx=520, ry=420, rmax=10.5, tone="bone", rect=[40, 200, 1000, 730]),
           dict(kind="pill_edge", at=pills[8]["f0"], until=pills[8]["f1"], style="dashed", pill=pb(8), radius=46, seed=9)]
    # ---- F (790-899): every eye ----
    sc.append(dict(id="pgF", f0=790, f1=899, paper=True, panels=[
        P("E", "S10", BG, 790, 0, .6, .33, 1.0, 1.1, 880, show=[790, 880]),
        P("D", "S12", SMW, 790, 0, .5, .3, 1.0, 1.1, 899, tilt=-.8)],
        moves=[slam("E", 790, 0), slam("D", 790, 8), dict(kind="panel_dive", panel="D", at=868, frames=10)]))
    tr.append(dict(kind="ink_bleed", **{"from": "pgE", "to": "pgF"}, at=790, frames=10, origin=[540, 500]))
    dd += [dict(kind="speed_lines", at=819, until=845, mode="focus", r0=300, arc=[160, 200], n=6, tone="ink", seed=9, pos=dict(xy=[620, 560])),
           dict(kind="ink_splat", at=849, until=868, pos=dict(xy=[1062, 1300]), r=16, seed=3, tone="ink", dir=90)]
    # ---- Jesus line: S09 still, static splash border only ----
    sc.append(dict(id="jesus", f0=889, f1=1043, splash=dict(inset=22, width=10), panels=[P("main", "S09", FULL, 889, 0, .5, .5, 1.0, 1.0, 1043, border=0)]))
    tr.append(dict(kind="border_fall", **{"from": "pgF", "to": "jesus"}, at=889, frames=10))
    ND("jesus_line_S09", FULL, 889, 1043)
    # ---- G (1033-1197): amazed > a local boy ----
    sc.append(dict(id="pgG", f0=1033, f1=1197, paper=True, panels=[
        P("A", "S11", BG, 1034, 0, .5, .3, 1.0, 1.1, 1184, show=[1034, 1184]),
        P("C", "S10", SMW, 1037, 0, .6, .33, 1.0, 1.08, 1115, tilt=.8, show=[1037, 1115]),
        P("M", "S13", SMW, 1115, 0, .45, .3, 1.0, 1.1, 1197, tilt=-.8)],
        moves=[slam("A", 1034, 0), slam("C", 1037, 8), slam("M", 1115, 8)]))
    tr.append(dict(kind="iris", **{"from": "jesus", "to": "pgG"}, at=1033, frames=10, center=[540, 640], ring=False))
    dd += [dict(kind="motion_ticks", at=1053, frames=14, dir=270, n=3, len=110, tone="ink", seed=5, pos=dict(xy=[90, 420])),
           dict(kind="motion_ticks", at=1053, frames=14, dir=270, n=3, len=110, tone="ink", seed=6, pos=dict(xy=[990, 420])),
           dict(kind="ink_splat", at=1115, until=1180, pos=dict(xy=[1062, 1300]), r=16, seed=4, tone="ink", dir=90)]
    # ---- H (1187-1277): the townsman ----
    sc.append(dict(id="pgH", f0=1187, f1=1277, paper=True, panels=[
        P("T", "S12", BG, 1187, 1.0, .5, .3, 1.0, 1.1, 1277),
        P("B", "S13", SMW, 1187, 2.0, .62, .3, 1.0, 1.1, 1277, tilt=.8)], moves=[slam("T", 1187, 0), slam("B", 1187, 8)]))
    tr.append(dict(kind="punch_cut", **{"from": "pgG", "to": "pgH"}, at=1187, frames=0))
    dd += [dict(kind="pill_edge", at=pills[14]["f0"], until=pills[14]["f1"], style="spiky", pill=pb(14), radius=46, tone="ink", seed=4), dict(kind="jolt", at=1224, amp=6, frames=4)]
    # ---- I (1271-1413): that local boy > Isaiah promise > about Him ----
    sc.append(dict(id="pgI", f0=1271, f1=1413, paper=True, panels=[
        P("Y", "S13", BG, 1271, 0, .45, .3, 1.0, 1.1, 1356, show=[1271, 1356]),
        P("J", "S01", BG, 1356, 0.2, .5, .27, 1.0, 1.1, 1413),
        P("W", "S05", SM1, 1271, 0, .45, .3, 1.0, 1.1, 1413, tilt=-1),
        P("F", "S06", SM2, 1307, 0, .45, .42, 1.0, 1.15, 1413, tilt=1)],
        moves=[slam("Y", 1271, 0), slam("W", 1271, 0), slam("F", 1307, 8), slam("J", 1356, 8)]))
    tr.append(dict(kind="page_flip_up", **{"from": "pgH", "to": "pgI"}, at=1271, frames=10))
    ND("I_Jesus_S01", BG, 1356, 1413); ND("I_boy_S13", BG, 1271, 1356)
    dd += [dict(kind="ink_splat", at=1307, until=1356, pos=dict(xy=[1062, 1300]), r=16, seed=6, tone="ink", dir=90)]
    # ---- J (1403-1503): He stopped at God's welcome ----
    sc.append(dict(id="pgJ", f0=1403, f1=1503, paper=True, panels=[
        P("R", "S07", BG, 1403, 0, .55, .3, 1.0, 1.1, 1503),
        P("W", "S02", SMW, 1403, 0, .5, .3, 1.0, 1.1, 1463, tilt=.8, show=[1403, 1463]),
        P("X", "S06", SMW, 1464, 0, .45, .42, 1.0, 1.1, 1503, tilt=-.8)], moves=[slam("R", 1403, 0), slam("W", 1403, 8), slam("X", 1464, 0)]))
    tr.append(dict(kind="halftone_dissolve", **{"from": "pgI", "to": "pgJ"}, at=1403, frames=12, mode="radial", center=[540, 700]))
    ND("J_Jesus_S07", BG, 1403, 1503)
    dd += [dict(kind="ink_splat", at=1431, until=1488, pos=dict(xy=[1062, 1300]), r=16, seed=7, tone="ink", dir=90)]
    # ---- landing + 3 s hold: S14, static border, nothing drawn ----
    sc.append(dict(id="land", f0=1491, f1=FRAMES, splash=dict(inset=22, width=10), panels=[P("main", "S14", FULL, 1491, 0, .5, .5, 1.0, 1.0, FRAMES, border=0)]))
    tr.append(dict(kind="border_fall", **{"from": "pgJ", "to": "land"}, at=1491, frames=10))
    ND("landing_S14", FULL, 1491, FRAMES)
    ep = dict(fps=30, frames=FRAMES, assets="comic_nazareth", scenes=sc, transitions=tr, doodles=dd, tracks={}, no_draw=nd,
              pills=[dict(png=p["png"], f0=p["f0"], f1=p["f1"], box=p["box"], radius=p["radius"]) for p in pills], hook=dict(png="pills/hook.png", f0=0, f1=66))
    (HERE / "nazareth_episode.json").write_text(json.dumps(ep, indent=1)); print("ok", len(sc), "scenes", len(dd), "doodles")


if __name__ == "__main__":
    build()
