import json
from pathlib import Path
H=Path(__file__).resolve().parent; EP=H.parent
old=json.loads((EP/"narration.alignment.json").read_text(encoding="utf-8"))
r1=json.loads((H/"new_lines_words_rel.json").read_text(encoding="utf-8"))
r2=json.loads((H/"new_last2_words_rel.json").read_text(encoding="utf-8"))
def fmap(t): return t+0.08 if t<2.95 else t+0.08-0.40
CUTS=[(1.45,1.80),(3.25,3.70),(4.95,5.30)]
OFF=77.70-(4.072-0.80)
def tm(t): return t-sum(b-a for a,b in CUTS if b<=t)
W=[]
for w in r1["first_a"]["words"]:
    W.append({"text":w["w"],"start":round(fmap(w["start"]),3),"end":round(fmap(w["end"]),3),"loss":0.0}); W.append({"text":" ","start":round(fmap(w["end"]),3),"end":round(fmap(w["end"]),3)+0.001,"loss":0.0})
W+=[x for x in old["words"] if 5.80<=x["start"]<73.60]
for w in r2["last2_b"]["words"]:
    s=round(tm(w["start"])+OFF,3); e=round(tm(w["end"])+OFF,3)
    W.append({"text":" ","start":s-0.02,"end":s,"loss":0.0}); W.append({"text":w["w"],"start":s,"end":e,"loss":0.0})
    print(w["w"],s,e)
out={"characters":old.get("characters",[]),"words":W,"loss":old.get("loss"),"note":"linefix2: words only for srt"}
(H/"narration.alignment_linefix2.json").write_text(json.dumps(out,ensure_ascii=False,indent=1),encoding="utf-8")
d=H/"swirls_episode_11_where_are_the_nine_linefix2"; d.mkdir(exist_ok=True)
(d/"narration.alignment.json").write_text(json.dumps(out,ensure_ascii=False),encoding="utf-8")
