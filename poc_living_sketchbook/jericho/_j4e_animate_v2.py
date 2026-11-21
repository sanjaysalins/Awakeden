"""linefix2: Kling 3.0 pro clips, all >= slot, written as clips/<name>_v2.mp4 (old kept). Usage: _j4e_animate_v2.py <name>"""
import importlib.util, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT))
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("_anim", ROOT/"poc_comic_page"/"_animate_piece1_v2.py")
A = importlib.util.module_from_spec(spec); spec.loader.exec_module(A)
A.EPISODE = "LS_Jericho"; A.OUT = HERE/"clips"
S = HERE/"stills"
LOCK = ("The camera does not move, zoom, or change angle at all. INVENT NOTHING new -- no new figures, objects, or marks appear; the paper texture, torn edges, and every sketch line hold perfectly still. ")
NG = "the light stays a steady, even glow -- it does not sparkle, flicker into particles, or scatter into glitter. "
J = {
 "j02_feet": (S/"j02_feet.png", 8, "Only: the marching feet keep walking forward, left to right, in one steady natural stride that continues the whole time, never reversing; the robe hems swing with each step, low dust drifts behind them. The ground and paper hold still. Nothing else changes."),
 "j06_thread": (S/"j06_thread.png", 6, "The scarlet thread holds perfectly still. Only: a soft warm light across the paper breathes very gently, "+NG+"Nothing else changes."),
 "j10_stage_c": (S/"j10_stage_c_v2.png", 5, "The rubble, the standing wall fragment, the window, and the scarlet cord all hold perfectly still and keep their exact shape; the cord stays a thin straight line. Only: fine dust drifts slowly across the scene, the first warm light on the fragment breathes gently. Nothing else changes."),
 "j11_spared": (S/"j11_spared_v2.png", 8, "The woman and every family figure stay perfectly frozen like statues in their exact places -- no steps, no head turns, no face changes, nobody moves or merges. The wall fragment and window hold still. Only: the morning gold light breathes softly and evenly, "+NG+"the scarlet cord hangs from the window and sways very slightly, faint dust drifts in the light. Nothing else changes."),
 "j12_line": (S/"j12_line.png", 8, "The scarlet thread and every faint generation sketch hold perfectly still. Only: the warm gold glow at the right edge breathes slowly, "+NG+"Nothing else changes."),
 "j13_landing": (S/"j13_landing.png", 12, "The torn paper edges, the faint cross silhouette, and the scarlet thread all hold perfectly still: the scarlet thread is printed flat on the paper, it keeps its exact shape and position in every frame, it does not slide, drift, shrink, or move at all. Only: the warm gold glow beneath the torn page breathes very slowly, "+NG+"Nothing else changes."),
}
n = sys.argv[1]; still, d, m = J[n]
if n=="j12_line" and (S/"j12_line_v2.png").exists(): still = S/"j12_line_v2.png"
A.OUT.mkdir(exist_ok=True)
tmp = A.OUT/f"{n}.mp4"; final = A.OUT/f"{n}_v2.mp4"
assert not final.exists(), "exists"
assert not tmp.exists() or n not in () ,""
# run_job writes OUT/<name>.mp4: use name_v2 as the job name so old clip untouched
ok = A.run_job(n+"_v2", "kling", still, "9:16", LOCK+m, duration=d)
print("RESULT", n, ok)
