"""build_nazareth_v6_linefix1.py - $0. Reads nazareth_episode_v6.json (NOT edited) and writes nazareth_episode_v6_lf1.json for the SAME NazarethComicV6 composition.
New first line (3.62 s) pushes everything after the opening 1.2 s = 36 frames later: every frame value >= 90 shifts +36; pgA (opening page) is stretched;
S01 dive stays at frame 54 (inside the pause), full-bleed Jesus holds through 'Watch where Jesus stopped reading.'. New caption pills + hook card replace the old first line's."""
import json
from pathlib import Path
H = Path(__file__).parent; S = 36; CUT = 90
e = json.load(open(H / "nazareth_episode_v6.json")); newp = json.load(open(H / "pills_v6_lf1.json"))
FK = {"f0", "f1", "f_start", "f_z0", "f_z1", "mount", "at", "until"}; seen = set()
def sh(v): return v + S if isinstance(v, (int, float)) and v >= CUT else v
def walk(o, parent_key=None):
    if isinstance(o, dict):
        for k, v in list(o.items()):
            if k in FK and isinstance(v, (int, float)): o[k] = sh(v); seen.add(k)
            elif k == "show" and isinstance(v, list): o[k] = [sh(x) for x in v]
            elif k in ("pills", "hook"): continue
            else: walk(v, k)
    elif isinstance(o, list):
        for x in o: walk(x, parent_key)
old_pills = e.pop("pills"); old_hook = e.pop("hook")
walk(e)
for p in old_pills[1:]: p["f0"] += S; p["f1"] += S
e["pills"] = newp_list = [dict(png=p["png"], f0=p["f0"], f1=p["f1"], box=p["box"], radius=p["radius"]) for p in newp[:2]] + old_pills[1:]
e["hook"] = dict(png="pills_v6_lf1/hook.png", f0=0, f1=46)
e["frames"] = 1796 + S
(H / "nazareth_episode_v6_lf1.json").write_text(json.dumps(e, indent=1)); print("ok frames", e["frames"], "keys shifted", sorted(seen))
