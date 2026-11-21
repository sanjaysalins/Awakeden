import json
from pathlib import Path
V=Path(__file__).resolve().parent; P=V/"_linefix1_pool"
old=json.loads((V/"livingpage_short.spec.json").read_text(encoding="utf-8")); al=json.loads((V.parent/"audio/alignment.json").read_text())
def words(a,b): return [w for w in al if a-0.05<=w["start"]<b]
def mk(name,beats,t0,t1):
    spec={"audio":"../../audio/_linefix2/silence70.wav","total":t1,"cut_ticks":False,"motion":"smooth","beats":beats}
    (P/f"linefix2_{name}.spec.json").write_text(json.dumps(spec,indent=1),encoding="utf-8")
B=old["beats"]
# A: confession beat (old idx 7)
b=json.loads(json.dumps(B[7])); t0=b["t"][0]; ws=words(26.7,31.5)
assert [w["w"] for w in ws]==["A","confession.","A","verdict:","innocent.","Then","one","request."],ws
b["cap"]={"type":"caption","text":"A confession. A verdict: innocent. Then one request.","kw":"INNOCENT","word_t":[max(0,round(w["start"]-t0,3)) for w in ws]}
mk("A",[b,json.loads(json.dumps(B[8]))],B[7]["t"][0],B[8]["t"][1])
# B: jesus beat (idx 9, no gloss in spec) + He got beat (idx 10)
b10=json.loads(json.dumps(B[9])); b11=json.loads(json.dumps(B[10])); t0=b11["t"][0]; ws=words(42.8,46.3)
assert [w["w"] for w in ws]==["He","asked","for","someday.","Jesus","gave","him","that","same","afternoon."],ws
b11["cap"]={"type":"caption","text":"He asked for someday. Jesus gave him that same afternoon.","kw":"SAME AFTERNOON","word_t":[max(0.0,round(w["start"]-t0,3)) for w in ws]}
mk("B",[b10,b11],b10["t"][0],b11["t"][1])
# C: paradise beat, extended to the clip's real length (5.04 s) => no stretch
b=json.loads(json.dumps(B[15])); t0=b["t"][0]; b["t"]=[t0,round(t0+5.03,2)]
b["cap"]={"type":"caption","text":"Paradise","kw":"PARADISE","word_t":[round(58.531-t0,3)]}
mk("C",[b],*b["t"])
print("ok")
