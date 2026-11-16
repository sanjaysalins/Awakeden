"""build_nazareth_v6.py - writes nazareth_episode_v6.json for the NazarethComicV6 composition. $0.  (words v7 + new voice, audio 59.85 s -> 1796 frames @30)
  .venv\\Scripts\\python.exe prophecy/02_nazareth/build/build_nazareth_v6.py
Pages: A hook > B village/reading/hands > C poor/welcome > D Isaiah sentence + his line > F unread, sat down > [Jesus line S09 still] > G 'It was about Him' + townsmen + 'Physician' (S12)
> H foreigners (S18) > I furious crowd (S15) > J walked through them (S16) > K the cross (S17, reverent, nothing drawn) > [S14 landing starts on 'rose again' + hold]."""
import json, sys
from pathlib import Path
HERE = Path(__file__).parent
TB = Path(r"F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_ELEVATE\formula\build"); sys.path.insert(0, str(TB))
from geo import FW, FH
from pages import page_layout
FULL = [0, 0, FW, FH]; FRAMES = 1796; LAND = 1496
pills = json.load(open(HERE / "pills_v6.json"))
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
    # ---- A hook (0-96): S01 + Isaiah writing (S08, first 2.2 s); S01 dives full-bleed on "sentence." (53) ----
    sc.append(dict(id="pgA", f0=0, f1=96, paper=True, panels=[
        P("J", "S01", S2[0], 0, 0, .5, .27, 1.0, 1.1, 94, tilt=-1),
        P("W", "S08", S2[1], 0, 0, .4, .38, 1.0, 1.08, 66, tilt=1, show=[0, 66])],
        moves=[slam("J", 0, 8), slam("W", 0, 0), dict(kind="panel_dive", panel="J", at=54, frames=12)]))
    ND("A_Jesus_S01", S2[0], 0, 54); ND("A_Jesus_S01_full", FULL, 54, 90)
    dd += [dict(kind="ink_splat", at=10, until=54, pos=dict(xy=[1056, 975]), r=16, seed=1, tone="ink", dir=90)]
    # ---- B (90-181): village (1.6 s) > Jesus reads on "He read" ; attendant's hands (S04 hands only) ----
    sc.append(dict(id="pgB", f0=90, f1=181, paper=True, panels=[
        P("V", "S02", BG, 90, 0, .5, .35, 1.0, 1.08, 137, show=[90, 137]),
        P("L", "S03", BG, 137, 0, .5, .33, 1.0, 1.08, 181),
        P("H", "S04", SMW, 90, 0, .5, .68, 1.0, 1.1, 181, tilt=-.8)],
        moves=[slam("V", 90, 0), slam("H", 90, 8), slam("L", 137, 8)]))
    tr.append(dict(kind="slam_cut", **{"from": "pgA", "to": "pgB"}, at=90, frames=6, tilt=3))
    ND("B_Jesus_S03", BG, 137, 181)
    dd += [dict(kind="ink_splat", at=94, until=170, pos=dict(xy=[1062, 1112]), r=16, seed=2, tone="ink", dir=90)]
    # ---- C (175-315): someone sent for the poor (S05) > God's welcome (S03); whisperers S11 ----
    sc.append(dict(id="pgC", f0=175, f1=315, paper=True, panels=[
        P("P", "S05", BG, 175, 0, .45, .3, 1.0, 1.1, 254, show=[175, 254]),
        P("S", "S03", BG, 254, 0, .5, .33, 1.0, 1.08, 315, tilt=.6),
        P("Q", "S11", SMW, 175, 0, .5, .37, 1.0, 1.08, 315, tilt=.8)],
        moves=[slam("P", 175, 0), slam("Q", 175, 8), slam("S", 254, 8)]))
    tr.append(dict(kind="page_flip_up", **{"from": "pgB", "to": "pgC"}, at=175, frames=6))
    ND("C_Jesus_S03", BG, 254, 315)
    dd += [dict(kind="rays", at=207, until=227, mode="soft", pos=dict(xy=[760, 130]), clear_r=150, len=280, arc=[60, 130], n=5, opacity=.7, tone="two", seed=12)]
    # ---- D (303-472): "The prophet Isaiah's sentence goes on" (S08 hush) > Isaiah's unread line (scroll in Jesus' hands) ----
    sc.append(dict(id="pgD", f0=303, f1=472, paper=True, panels=[
        P("I", "S08", BG, 303, 0, .4, .35, 1.0, 1.08, 374, show=[303, 374]),
        P("J", "S07", BG, 374, .5, .55, .3, 1.0, 1.1, 472),
        P("M", "S04", SMW, 303, 0, .5, .68, 1.0, 1.1, 450, tilt=.8, show=[303, 450])],
        moves=[slam("I", 303, 0), slam("M", 303, 8), slam("J", 374, 0)]))
    tr.append(dict(kind="halftone_dissolve", **{"from": "pgC", "to": "pgD"}, at=303, frames=12, mode="radial", center=[540, 500]))
    ND("D_Jesus_S07", BG, 374, 472)
    dd += [dict(kind="halftone_vignette", at=315, until=370, center=[540, 560], rx=520, ry=420, rmax=10.5, tone="bone", rect=[40, 200, 1000, 730]),
           dict(kind="jolt", at=317, amp=8, frames=4),
           dict(kind="pill_edge", at=pills[5]["f0"], until=pills[5]["f1"], style="dashed", pill=pb(5), radius=46, seed=9)]
    # ---- F (462-586): He leaves it unread (hands close the scroll) > sat down (S09 seated) ----
    sc.append(dict(id="pgF", f0=462, f1=586, paper=True, panels=[
        P("K", "S07", BG, 462, 2.0, .55, .3, 1.0, 1.1, 529, show=[462, 529]),
        P("L", "S09", BG, 529, 5.0, .5, .3, 1.0, 1.08, 586, show=[529, 586]),
        P("M", "S02", SMW, 462, 0, .5, .35, 1.0, 1.08, 527, tilt=-.8, show=[462, 527])],
        moves=[slam("K", 462, 0), slam("M", 462, 8), slam("L", 529, 8)]))
    tr.append(dict(kind="iris", **{"from": "pgD", "to": "pgF"}, at=462, frames=10, center=[540, 500], ring=False))
    ND("F_Jesus_S07", BG, 462, 529); ND("F_Jesus_S09", BG, 529, 586)
    # ---- Jesus line 19.19-22.19: S09 still, static splash border only ----
    sc.append(dict(id="jesus", f0=576, f1=688, splash=dict(inset=22, width=10), panels=[P("main", "S09", FULL, 576, 0, .5, .5, 1.0, 1.0, 688, border=0)]))
    tr.append(dict(kind="border_fall", **{"from": "pgF", "to": "jesus"}, at=576, frames=10))
    ND("jesus_line_S09", FULL, 576, 678)
    # ---- G (678-895): "It was about Him" (S03) > townsmen want miracles (S11, S10) > Physician, heal thyself (S12 townsman + Jesus listens) ----
    sc.append(dict(id="pgG", f0=678, f1=895, paper=True, panels=[
        P("A", "S03", BG, 678, 0, .5, .33, 1.0, 1.08, 739, show=[678, 739]),
        P("B", "S11", BG, 739, 1.5, .5, .37, 1.0, 1.08, 809, show=[739, 809]),
        P("C", "S10", SMW, 678, 0, .6, .33, 1.0, 1.08, 770, tilt=.8, show=[678, 770]),
        P("D", "S12", BG, 809, 0, .5, .3, 1.0, 1.1, 895),
        P("E", "S09", SMW, 770, 5.5, .5, .28, 1.3, 1.4, 895, tilt=-1)],
        moves=[slam("A", 678, 0), slam("B", 739, 0), slam("C", 678, 8), slam("D", 809, 0), slam("E", 770, 8)]))
    tr.append(dict(kind="punch_cut", **{"from": "jesus", "to": "pgG"}, at=678, frames=0))
    ND("G_Jesus_S03", BG, 678, 739); ND("G_Jesus_S09_crop", SMW, 770, 895)
    dd += [dict(kind="motion_ticks", at=745, frames=14, dir=270, n=3, len=110, tone="ink", seed=5, pos=dict(xy=[90, 420])),
           dict(kind="motion_ticks", at=745, frames=14, dir=270, n=3, len=110, tone="ink", seed=6, pos=dict(xy=[990, 420]))]
    # ---- H (885-1064): foreigners (Elijah + the widow, S18); Jesus teaches (S01 crop) > "not to their own" (townsman) ----
    sc.append(dict(id="pgH", f0=885, f1=1064, paper=True, panels=[
        P("T", "S01", SMW, 885, .5, .5, .2, 1.3, 1.4, 989, tilt=.8, show=[885, 989]),
        P("E", "S18", BG, 911, 0, .5, .4, 1.0, 1.08, 1060, show=[911, 1060]),
        P("U", "S12", SMW, 989, 1.0, .5, .3, 1.0, 1.1, 1064, tilt=-.8)],
        moves=[slam("T", 885, 8), slam("E", 911, 0), slam("U", 989, 8)]))
    tr.append(dict(kind="punch_cut", **{"from": "pgG", "to": "pgH"}, at=885, frames=0))
    ND("H_Jesus_S01_crop", SMW, 885, 989)
    dd += [dict(kind="ink_splat", at=895, until=960, pos=dict(xy=[1062, 700]), r=16, seed=4, tone="ink", dir=90)]
    # ---- I (1058-1162): Furious, they took Him to a cliff (S15) ----
    sc.append(dict(id="pgI", f0=1058, f1=1162, paper=True, panels=[
        P("Y", "S15", BG, 1058, 0, .45, .3, 1.0, 1.08, 1162),
        P("A", "S10", SMW, 1058, 0, .6, .33, 1.0, 1.06, 1150, tilt=.8, show=[1058, 1150])],
        moves=[slam("Y", 1058, 8), slam("A", 1058, 0)]))
    tr.append(dict(kind="page_flip_up", **{"from": "pgH", "to": "pgI"}, at=1058, frames=6))
    ND("I_Jesus_S15", BG, 1058, 1162)
    dd += [dict(kind="pill_edge", at=pills[12]["f0"], until=pills[12]["f1"], style="spiky", pill=pb(12), radius=46, tone="ink", seed=4), dict(kind="jolt", at=1058, amp=8, frames=4),
           dict(kind="ink_splat", at=1100, until=1146, pos=dict(xy=[1062, 1300]), r=16, seed=5, tone="ink", dir=90)]
    # ---- J (1152-1220): He walked right through them (S16) ----
    sc.append(dict(id="pgJ", f0=1152, f1=1220, paper=True, panels=[
        P("R", "S16", BG, 1152, 0, .5, .3, 1.0, 1.08, 1220),
        P("X", "S15", SMW, 1159, 3.0, .17, .26, 3.0, 3.1, 1220, tilt=.8)],
        moves=[slam("R", 1152, 0), slam("X", 1159, 8)]))
    tr.append(dict(kind="iris", **{"from": "pgI", "to": "pgJ"}, at=1152, frames=10, center=[540, 640], ring=False))
    ND("J_Jesus_S16", BG, 1152, 1220); ND("J_S15_crop", SMW, 1159, 1220)
    # ---- K (1210-1506): the cross, REVERENT. S17 wide on the cross; mocking leaders crop on "cross,"; nothing drawn ----
    sc.append(dict(id="pgK", f0=1210, f1=1506, paper=True, panels=[
        P("X", "S17", BG, 1210, 0, .5, .27, 1.0, 1.0, 1506),
        P("Y", "S17", SMW, 1237, (1237 - 1210) / 30.0, .5, .8, 1.0, 1.0, 1380, tilt=.5, show=[1237, 1380])],
        moves=[slam("X", 1210, 0), slam("Y", 1237, 0)]))
    tr.append(dict(kind="halftone_dissolve", **{"from": "pgJ", "to": "pgK"}, at=1210, frames=10, mode="radial", center=[540, 500]))
    ND("K_cross_S17", BG, 1220, 1496)
    # ---- landing + hold: S14 full-bleed STARTS on "rose again" (49.86 s), static border, nothing drawn ----
    sc.append(dict(id="land", f0=LAND, f1=FRAMES, splash=dict(inset=22, width=10), panels=[P("main", "S14", FULL, LAND, 0, .5, .5, 1.0, 1.0, FRAMES, border=0)]))
    tr.append(dict(kind="border_fall", **{"from": "pgK", "to": "land"}, at=LAND, frames=10))
    ND("landing_S14", FULL, LAND, FRAMES)
    ep = dict(fps=30, frames=FRAMES, assets="comic_nazareth", scenes=sc, transitions=tr, doodles=dd, tracks={}, no_draw=nd,
              pills=[dict(png=p["png"], f0=p["f0"], f1=p["f1"], box=p["box"], radius=p["radius"]) for p in pills], hook=dict(png="pills_v6/hook.png", f0=0, f1=66))
    (HERE / "nazareth_episode_v6.json").write_text(json.dumps(ep, indent=1)); print("ok", len(sc), "scenes", len(dd), "doodles")


if __name__ == "__main__":
    build()
