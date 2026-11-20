"""narration.md tokens aligned to the voice word times (threads/t13_job_sea/audio/narration_final.words.json)."""
import json, re, difflib
from pathlib import Path
H=Path(__file__).resolve().parent; U=H.parent
raw=json.loads((H/"_raw_voice.json").read_text())
txt=" ".join(l.split(": ",1)[1] for l in (U/"narration.md").read_text(encoding="utf-8").splitlines() if l[:3] in("NAR","JOB","JES")).replace("(pause)","")
toks=txt.split()
key=lambda s:re.sub(r"[^a-z0-9']","",s.lower())
a=[key(t) for t in toks]; b=[key(r["w"]) for r in raw]
print(len(toks),len(raw))
sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
out=[]
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag=="equal":
        for k in range(i2-i1): out.append({"w":toks[i1+k],"start":raw[j1+k]["start"],"end":raw[j1+k]["end"]})
    else:
        print("diff",tag,toks[i1:i2],[r["w"] for r in raw[j1:j2]])
        if i2-i1==j2-j1:
            for k in range(i2-i1): out.append({"w":toks[i1+k],"start":raw[j1+k]["start"],"end":raw[j1+k]["end"]})
        else:
            raise SystemExit("unaligned")
(U/"visual"/"job_sea_final.words.json").write_text(json.dumps(out,indent=1),encoding="utf-8"); print(len(out))
