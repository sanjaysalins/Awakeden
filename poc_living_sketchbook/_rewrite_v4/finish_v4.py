import json, sys, subprocess
from pathlib import Path
R = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(R)); sys.path.insert(0, str(R/"poc_living_sketchbook"))
import _short_captions as C
H = Path(__file__).resolve().parent
for n in ["jericho","two_goats","bronze_serpent"]:
    words = [{"w": x["w"], "start": x["start"], "end": x["end"]} for x in json.load(open(H/"audio"/n/"alignment.json"))]
    src = H/"video"/f"{n}_v4.mp4"; out = H/"video"/f"{n}_v4_cc.mp4"
    wd = H/"video"/f"_cc_{n}"; wd.mkdir(exist_ok=True)
    C.burn(src, out, words, [], wd); print("captioned", out)
    subprocess.run([str(R/".venv/Scripts/python.exe"), str(R/"add_watermark.py"), str(out)], check=True)
