import json, re
from pathlib import Path
H=Path(__file__).resolve().parent; U=H.parent
raw=json.loads((H/"_raw_film.json").read_text())
txt=" ".join(l.split(": ",1)[1] for l in (U/"narration.md").read_text(encoding="utf-8").splitlines() if l[:3] in("NAR","GOD","JES")).replace("(pause)","")
toks=txt.split()
assert len(toks)==len(raw),(len(toks),len(raw))
key=lambda s:re.sub(r"[^a-z0-9']","",s.lower())
for t,r in zip(toks,raw):
    if key(t)!=key(r["w"]): print("diff",t,r["w"])
out=[{"w":t,"start":r["start"],"end":r["end"]} for t,r in zip(toks,raw)]
(U/"visual"/"can_one_man_final.words.json").write_text(json.dumps(out,indent=1),encoding="utf-8"); print(len(out))
