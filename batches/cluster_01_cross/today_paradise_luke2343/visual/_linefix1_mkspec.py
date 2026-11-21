import json
from pathlib import Path
V=Path(__file__).resolve().parent
old=json.loads((V/"livingpage_short.spec.json").read_text(encoding="utf-8"))
nw=json.loads((V.parent/"audio/_linefix1/new_first_words_rel.json").read_text())["a"]["words"]
al=json.loads((V.parent/"audio/alignment.json").read_text())
LEAD=0.25; B1=4.7; END=8.9
b0=json.loads(json.dumps(old["beats"][0])); b3=json.loads(json.dumps(old["beats"][3]))
b0["t"]=[0.0,B1]
b0["cap"]={"type":"caption","text":"Two guilty men were dying beside Jesus, with no time left to fix anything","kw":"NO TIME LEFT","word_t":[round(w["start"]+LEAD,3) for w in nw]}
ws=[w for w in al if 7.8<w["start"]<11.5]
assert [w["w"] for w in ws]==["Both","guilty.","Both","just","as","close.","Both","spoke."],ws
b3["t"]=[B1,END]
b3["cap"]={"type":"caption","text":"Both guilty. Both just as close. Both spoke.","kw":"BOTH","word_t":[round(w["start"]-7.8333,3) for w in ws]}
spec={"_doc":"linefix1: new line + corrected 'Both guilty...' caption (old said 'Both spoke to him' - not spoken). Beats 0+3 only, 8.9 s.","audio":"../../audio/_linefix1/head_narr_new.wav","total":END,"cut_ticks":False,"motion":"smooth","beats":[b0,b3]}
(V/"_linefix1_pool/livingpage_short.linefix1.spec.json").write_text(json.dumps(spec,indent=1),encoding="utf-8")
print(b0["cap"]["word_t"],b3["cap"]["word_t"])
