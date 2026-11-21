import json, subprocess, sys
from pathlib import Path
H=Path(__file__).resolve().parent; PIECE=H.parents[1]; ROOT=PIECE.parents[2]
sys.path.insert(0,str(ROOT)); import run_piece
pj=json.loads((PIECE/"piece.json").read_text(encoding="utf-8"))
sc=pj["score"]; sc["outro_hold"]=6.0; sc["fade_out"]=0.05
sc["src"]=str(PIECE/"visual/livingpage_short.spec_preview.mp4"); sc["out"]=str(H/"scored_ext.mp4")
r=subprocess.run(run_piece.score_cmd(PIECE,pj),capture_output=True,text=True)
if r.returncode: sys.exit(r.stderr[-1500:])
print("ok")
