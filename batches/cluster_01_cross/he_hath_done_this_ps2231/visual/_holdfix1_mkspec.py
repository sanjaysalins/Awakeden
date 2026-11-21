r"""he_hath_done_this holdfix1: rebuild beat 12 (4.05->4.1667 s, real clip 5.04 s, no stretch) and the LAST beat at the
real clip length (5.0333 s of 5.0417 s) so the film ends >= 3.0 s after the last spoken word ('done.' ends 42.637)."""
import json
from pathlib import Path
V=Path(__file__).resolve().parent; P=V/"_holdfix1_pool"
old=json.loads((V/"livingpage_short.spec.json").read_text(encoding="utf-8")); al=json.loads((V.parent/"audio/alignment.json").read_text())
B=old["beats"]; CUT=40.633333; END=45.666667
b12=json.loads(json.dumps(B[11])); b13=json.loads(json.dumps(B[12]))
assert b12["t"]==[36.45,40.5] and b13["t"]==[40.5,42.7]
b12["t"]=[36.45,CUT]; b13["t"]=[CUT,END]
ws=[w for w in al if w["start"]>=40.5]
assert [w["w"] for w in ws]==["the","One","who","said","it","is","done."],ws
b13["cap"]["word_t"]=[max(0.0,round(w["start"]-CUT,3)) for w in ws]
b13["border_break"]={"at":round(CUT+0.25,3)}          # same 0.25 s into the beat as before
b13["sfx"]=[["dawn_morning_warm",round(CUT+0.15,3),-13]]  # (tail-only build is --no-sfx; audio comes from the existing final)
spec={"audio":"silence70.wav","total":END,"cut_ticks":False,"motion":"smooth","beats":[b12,b13]}
(P/"holdfix1_tail.spec.json").write_text(json.dumps(spec,indent=1),encoding="utf-8"); print("ok",b13["cap"]["word_t"])
