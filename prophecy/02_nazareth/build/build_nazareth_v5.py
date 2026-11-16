"""build_nazareth_v5.py - writes nazareth_episode_v5.json for the NazarethComicV5 composition. $0.  (words v6 + new voice, audio 59.08 s = 1773 frames @30)
  .venv\\Scripts\\python.exe prophecy/02_nazareth/build/build_nazareth_v5.py
Pages: A hook > B village/reading/hands > C poor/freedom/welcome > D Isaiah sentence + his line > F unread, sat down > [Jesus line S09 still] > G his town (townsmen + 'Physician')
> H foreigners (S18 widow) > I furious crowd (S15) > J walked through them (S16) > K the cross (S17, reverent, nothing drawn) > [S14 landing + hold]."""
import json, sys
from pathlib import Path
HERE = Path(__file__).parent
TB = Path(r"F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_ELEVATE\formula\build"); sys.path.insert(0, str(TB))
from geo import FW, FH
from pages import page_layout
FULL = [0, 0, FW, FH]; FRAMES = 1773; LAND = 1496
pills = json.load(open(HERE / "pills_v4.json"))
S2 = page_layout("stack2"); BG = [40, 40, 1000, 1060]; SMW = [40, 1128, 1000, 752]


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
    # ---- A hook (0-95): S01 + Isaiah writing (S08, first 2.6 s); S01 dives full-bleed on "sentence." ----
    sc.append(dict(id="pgA", f0=0, f1=95, paper=True, panels=[
        P("J", "S01", S2[0], 0, 0, .5, .27, 1.0, 1.1, 93, tilt=-1),
        P("W", "S08", S2[1], 0, 0, .4, .38, 1.0, 1.08, 66, tilt=1, show=[0, 66])],
        moves=[slam("J", 0, 8), slam("W", 0, 0), dict(kind="panel_dive", panel="J", at=54, frames=12)]))
    ND("A_Jesus_S01", S2[0], 0, 54); ND("A_Jesus_S01_full", FULL, 54, 89)
    dd += [dict(kind="ink_splat", at=9, until=54, pos=dict(xy=[1056, 975]), r=16, seed=1, tone="ink", dir=90)]
    # ---- B (89-183): village (2 s) > Jesus reads on "He read" ; attendant's hands (S04 hands only) ----
    sc.append(dict(id="pgB", f0=89, f1=183, paper=True, panels=[
        P("V", "S02", BG, 89, 0, .5, .35, 1.0, 1.08, 138, show=[89, 138]),
        P("L", "S03", BG, 138, 0, .5, .33, 1.0, 1.08, 183),
        P("H", "S04", SMW, 89, 0, .5, .68, 1.0, 1.1, 183, tilt=-.8)],
        moves=[slam("V", 89, 0), slam("H", 89, 8), slam("L", 138, 8)]))
    tr.append(dict(kind="slam_cut", **{"from": "pgA", "to": "pgB"}, at=89, frames=6, tilt=3))
    ND("B_Jesus_S03", BG, 138, 183)
    dd += [dict(kind="ink_splat", at=93, until=176, pos=dict(xy=[1062, 1112]), r=16, seed=2, tone="ink", dir=90)]
    # ---- C (177-359): the poor > freedom > God's welcome ----
    sc.append(dict(id="pgC", f0=177, f1=359, paper=True, panels=[
        P("P", "S05", BG, 177, 0, .45, .3, 1.0, 1.1, 249, show=[177, 249]),
        P("S", "S06", BG, 249, 0, .45, .42, 1.0, 1.15, 359, tilt=.6),
        P("Q", "S11", SMW, 177, 0, .5, .37, 1.0, 1.08, 270, tilt=.8, show=[177, 270]),
        P("R", "S03", SMW, 270, 0, .5, .33, 1.0, 1.08, 347, tilt=-.8, show=[270, 347])],
        moves=[slam("P", 177, 0), slam("Q", 177, 8), slam("S", 249, 8), slam("R", 270, 8)]))
    tr.append(dict(kind="page_flip_up", **{"from": "pgB", "to": "pgC"}, at=177, frames=6))
    ND("C_Jesus_S03", SMW, 270, 347)
    dd += [dict(kind="rays", at=327, until=347, mode="soft", pos=dict(xy=[760, 130]), clear_r=150, len=280, arc=[60, 130], n=5, opacity=.7, tone="two", seed=12)]
    # ---- D (347-519): "The prophet Isaiah's sentence goes on" (S08 hush) > Isaiah's unread line (scroll in Jesus' hands) ----
    sc.append(dict(id="pgD", f0=347, f1=519, paper=True, panels=[
        P("I", "S08", BG, 347, 0, .4, .35, 1.0, 1.08, 425, show=[347, 425]),
        P("J", "S07", BG, 426, .5, .55, .3, 1.0, 1.1, 519),
        P("K", "S11", SMW, 347, 0, .5, .3, 1.0, 1.1, 443, tilt=.8, show=[351, 443]),
        P("M", "S04", SMW, 443, 1.5, .5, .68, 1.0, 1.1, 519, tilt=-.8)],
        moves=[slam("I", 347, 0), slam("K", 347, 8), slam("J", 426, 0), slam("M", 443, 8)]))
    tr.append(dict(kind="halftone_dissolve", **{"from": "pgC", "to": "pgD"}, at=347, frames=12, mode="radial", center=[540, 500]))
    ND("D_Jesus_S07", BG, 426, 519)
    dd += [dict(kind="halftone_vignette", at=347, until=420, center=[540, 560], rx=520, ry=420, rmax=10.5, tone="bone", rect=[40, 200, 1000, 730]),
           dict(kind="jolt", at=362, amp=8, frames=4),
           dict(kind="pill_edge", at=pills[6]["f0"], until=pills[6]["f1"], style="dashed", pill=pb(6), radius=46, seed=9)]
    # ---- F (509-638): He leaves it unread (hands close the scroll) > sat down (S09 seated) ----
    sc.append(dict(id="pgF", f0=509, f1=638, paper=True, panels=[
        P("K", "S07", BG, 509, 2.0, .55, .3, 1.0, 1.1, 575, show=[509, 575]),
        P("L", "S09", BG, 575, 5.0, .5, .3, 1.0, 1.08, 638, show=[575, 638]),
        P("M", "S03", SMW, 509, 0, .5, .33, 1.0, 1.08, 575, tilt=-.8, show=[509, 575])],
        moves=[slam("K", 509, 0), slam("M", 509, 8), slam("L", 575, 8)]))
    tr.append(dict(kind="iris", **{"from": "pgD", "to": "pgF"}, at=509, frames=10, center=[540, 500], ring=False))
    ND("F_Jesus_S07", BG, 509, 575); ND("F_Jesus_S03", SMW, 509, 575); ND("F_Jesus_S09", BG, 575, 638)
    # ---- Jesus line: S09 still, static splash border only ----
    sc.append(dict(id="jesus", f0=628, f1=777, splash=dict(inset=22, width=10), panels=[P("main", "S09", FULL, 628, 0, .5, .5, 1.0, 1.0, 777, border=0)]))
    tr.append(dict(kind="border_fall", **{"from": "pgF", "to": "jesus"}, at=628, frames=10))
    ND("jesus_line_S09", FULL, 628, 767)
    # ---- G (767-910): "He knew what His town would say" > Physician, heal thyself (Jesus panel) ----
    sc.append(dict(id="pgG", f0=767, f1=910, paper=True, panels=[
        P("A", "S12", BG, 767, 0, .5, .3, 1.0, 1.1, 910),
        P("B", "S10", SMW, 767, 1.0, .6, .33, 1.0, 1.08, 830, tilt=.8, show=[767, 830]),
        P("C", "S09", SMW, 830, 6.0, .5, .28, 1.3, 1.4, 910, tilt=-1)],
        moves=[slam("A", 767, 0), slam("B", 767, 8), slam("C", 830, 8)]))
    tr.append(dict(kind="punch_cut", **{"from": "jesus", "to": "pgG"}, at=767, frames=0))
    ND("G_Jesus_S09_crop", SMW, 830, 910)
    dd += [dict(kind="motion_ticks", at=772, frames=14, dir=270, n=3, len=110, tone="ink", seed=5, pos=dict(xy=[90, 420])),
           dict(kind="motion_ticks", at=772, frames=14, dir=270, n=3, len=110, tone="ink", seed=6, pos=dict(xy=[990, 420]))]
    # ---- H (900-1068): foreigners (Elijah + the widow, S18) > "not to them" (townsman) ----
    sc.append(dict(id="pgH", f0=900, f1=1068, paper=True, panels=[
        P("T", "S02", SMW, 900, 0, .5, .3, 1.0, 1.08, 963, tilt=.8, show=[900, 963]),
        P("E", "S18", BG, 910, 0, .5, .4, 1.0, 1.08, 1060, show=[910, 1060]),
        P("U", "S12", SMW, 970, 1.0, .5, .3, 1.0, 1.1, 1068, tilt=-.8)],
        moves=[slam("T", 900, 8), slam("E", 910, 0), slam("U", 970, 8)]))
    tr.append(dict(kind="punch_cut", **{"from": "pgG", "to": "pgH"}, at=900, frames=0))
    dd += [dict(kind="ink_splat", at=925, until=1000, pos=dict(xy=[1062, 1300]), r=16, seed=4, tone="ink", dir=90)]
    # ---- I (1062-1161): Furious, they led Him to a cliff (S15) ----
    sc.append(dict(id="pgI", f0=1062, f1=1161, paper=True, panels=[
        P("Y", "S15", BG, 1062, 0, .45, .3, 1.0, 1.08, 1161),
        P("A", "S10", SMW, 1062, 0, .6, .33, 1.0, 1.06, 1152, tilt=.8, show=[1062, 1152])],
        moves=[slam("Y", 1062, 8), slam("A", 1062, 0)]))
    tr.append(dict(kind="page_flip_up", **{"from": "pgH", "to": "pgI"}, at=1062, frames=6))
    ND("I_Jesus_S15", BG, 1062, 1161)
    dd += [dict(kind="pill_edge", at=pills[12]["f0"], until=pills[12]["f1"], style="spiky", pill=pb(12), radius=46, tone="ink", seed=4), dict(kind="jolt", at=1062, amp=8, frames=4),
           dict(kind="ink_splat", at=1100, until=1150, pos=dict(xy=[1062, 1300]), r=16, seed=5, tone="ink", dir=90)]
    # ---- J (1151-1215): He walked right through them (S16) ----
    sc.append(dict(id="pgJ", f0=1151, f1=1215, paper=True, panels=[
        P("R", "S16", BG, 1151, 0, .5, .3, 1.0, 1.08, 1215),
        P("X", "S15", SMW, 1151, 3.0, .17, .26, 3.0, 3.1, 1215, tilt=.8)],
        moves=[slam("R", 1151, 0), slam("X", 1151, 8)]))
    tr.append(dict(kind="iris", **{"from": "pgI", "to": "pgJ"}, at=1151, frames=10, center=[540, 640], ring=False))
    ND("J_Jesus_S16", BG, 1151, 1215); ND("J_S15_crop", SMW, 1151, 1215)
    # ---- K (1205-1506): the cross, REVERENT. S17 wide on the cross; mocking leaders crop on "leaders"; nothing drawn ----
    sc.append(dict(id="pgK", f0=1205, f1=1506, paper=True, panels=[
        P("X", "S17", BG, 1205, 0, .5, .27, 1.0, 1.0, 1506),
        P("Y", "S17", SMW, 1241, (1241 - 1205) / 30.0, .5, .8, 1.0, 1.0, 1383, tilt=.5, show=[1241, 1383])],
        moves=[slam("X", 1205, 0), slam("Y", 1241, 0)]))
    tr.append(dict(kind="halftone_dissolve", **{"from": "pgJ", "to": "pgK"}, at=1205, frames=10, mode="radial", center=[540, 500]))
    ND("K_cross_S17", BG, 1215, 1496)
    # ---- landing + hold: S14 full-bleed, static border, nothing drawn ----
    sc.append(dict(id="land", f0=LAND, f1=FRAMES, splash=dict(inset=22, width=10), panels=[P("main", "S14", FULL, LAND, 0, .5, .5, 1.0, 1.0, FRAMES, border=0)]))
    tr.append(dict(kind="border_fall", **{"from": "pgK", "to": "land"}, at=LAND, frames=10))
    ND("landing_S14", FULL, LAND, FRAMES)
    ep = dict(fps=30, frames=FRAMES, assets="comic_nazareth", scenes=sc, transitions=tr, doodles=dd, tracks={}, no_draw=nd,
              pills=[dict(png=p["png"], f0=p["f0"], f1=p["f1"], box=p["box"], radius=p["radius"]) for p in pills], hook=dict(png="pills_v4/hook.png", f0=0, f1=66))
    (HERE / "nazareth_episode_v5.json").write_text(json.dumps(ep, indent=1)); print("ok", len(sc), "scenes", len(dd), "doodles")


if __name__ == "__main__":
    build()
