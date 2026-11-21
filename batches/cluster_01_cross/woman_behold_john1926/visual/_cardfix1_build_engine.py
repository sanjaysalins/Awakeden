r"""cardfix1 engine wrapper: runs the STOCK livingpage engine on _cardfix1_pool (beats 7-8 of the fix1 spec, no gloss card).
ONE seam patched: cap["box_y"] (the fix1 spec's explicit quote-box y, 720 on 'Woman, behold thy son!') is honoured by
overriding the solved box's y. Nothing else in the engine is touched.
  .venv\Scripts\python.exe visual\_cardfix1_build_engine.py [--only N]"""
import sys
from pathlib import Path
ENG = Path(r"F:\slk\PycharmProjects\JesusInTheBible\longform\02_Psalm_22_Song_From_The_Cross")
sys.path.insert(0, str(ENG))
import build_livingpage_16x9 as E
cl = E.cl
_solve = cl.solve

def solve(page, panels, cap):
    sol = _solve(page, panels, cap)
    if cap.get("box_y") is not None and sol.get("box"):
        x, y, bw, bh = sol["box"]
        sol["box"] = (x, int(cap["box_y"]), bw, bh)
    return sol

cl.solve = solve
POOL = Path(__file__).resolve().parent / "_cardfix1_pool"
extra = sys.argv[1:]
sys.argv = ["build_livingpage_16x9.py", "--pool", str(POOL), "--spec", "livingpage_short.cardfix1.spec.json",
            "--page", "1080x1920", "--clips", "--no-sfx"] + extra
E.main()
