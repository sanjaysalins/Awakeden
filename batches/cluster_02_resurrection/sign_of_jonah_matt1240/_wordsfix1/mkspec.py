"""wordsfix1 spec: current pinned spec; beats 0-2 unchanged; 3-4 rebuilt (Nineveh/fled + gracious/spare); 5 = old 5 re-timed; 6 re-timed
with word_t; 7..15 = old beats shifted +SH (audio block E is sample-exact old audio moved +SH); old 16-18 replaced by 3 beats for the new ending."""
import json, copy
from pathlib import Path
H=Path(__file__).resolve().parent; P=H.parent
old=json.load(open(P/"visual/livingpage_short.spec.json",encoding="utf-8"))
al=json.load(open(H/"alignment_wordsfix1.json",encoding="utf-8"))
blk=json.load(open(H/"blocks.json"))
SH=round(blk["old_map"][2][2]-blk["old_map"][2][0],3)   # block E shift (new_a - old_a)
print("SH",SH)
def W(a,b): return [w for w in al if w["w"]!="—" and a-0.02<=w["start"]<b]
def wt(text,t0,a,b):
    ws=W(a,b); assert len(ws)==len(text.split()),(len(ws),text)
    return [max(0.0,round(w["start"]-t0,3)) for w in ws]
B=old["beats"]; TOT=old["total"]
def shift(b):
    b=copy.deepcopy(b); b["t"]=[round(b["t"][0]+SH,3),round(b["t"][1]+SH,3)]
    if "panel_at" in b: b["panel_at"]=[round(x+SH,3) for x in b["panel_at"]]
    if b.get("takeover"): b["takeover"]["start"]=round(b["takeover"]["start"]+SH,3)
    if b.get("sfx"): b["sfx"]=[[n,round(t+SH,3),g] for n,t,g in b["sfx"]]
    if b.get("border_break"): b["border_break"]["at"]=round(b["border_break"]["at"]+SH,3)
    for c in b["clips"]:
        if "at" in c: c["at"]=round(c["at"]+SH,3)
    return b
def T(w): return next(x for x in al if x["w"]==w) 
def start(word,after): return next(x["start"] for x in al if x["w"]==word and x["start"]>=after)
t_I=start("I",13.0); t_The=start("The",16.5); t_Then=start("Then,",20.0)
t_For=B[7]["t"][0]+SH
nb=[]
nb+= [copy.deepcopy(x) for x in B[:3]]
# beat 3: He sent me to Nineveh, and I fled.
b3=copy.deepcopy(B[3]); b3["t"]=[B[3]["t"][0],round(t_I,3)]
txt="He sent me to Nineveh, and I fled."
b3["cap"]={"type":"caption","text":txt,"kw":"AND I FLED","word_t":wt(txt,b3["t"][0],10.7,t_I)}
b3["panel_at"]=[b3["t"][0],round(b3["t"][0]+0.35,3),round(b3["t"][0]+0.7,3)]
nb.append(b3)
# beat 4: I knew He is gracious, and would spare her.  (nineveh = the city to be spared)
txt="I knew He is gracious, and would spare her."
b4={"t":[round(t_I,3),round(t_The,3)],"tpl":"hero_band3","clips":[{"slug":"nineveh_distant_walls","motion":"pushin"}],
    "cap":{"type":"caption","text":txt,"kw":"WOULD SPARE HER","word_t":wt(txt,t_I,t_I-0.02,t_The)},
    "anchors":[[1.2,0.3,0.6],[1.6,0.5,0.3],[1.8,0.68,0.62]],"panel_at":[round(t_I,3),round(t_I+0.28,3),round(t_I+0.56,3)],
    "panel_slide":["up","left","down"],"flash":True,"fx":{"temp":7600}}
nb.append(b4)
# beat 5: storm/lot re-timed
b5=copy.deepcopy(B[5]); d=t_The-b5["t"][0]; b5["t"]=[round(t_The,3),round(t_Then,3)]
b5["panel_at"]=[round(x+d,3) for x in b5["panel_at"]]; nb.append(b5)
# beat 6: scribes
b6=copy.deepcopy(B[6]); b6["t"]=[round(t_Then,3),round(t_For,3)]
txt=b6["cap"]["text"]; ws=[w for w in al if w["w"]!="—" and t_Then<=w["start"]<t_For]
# spoken: Then, centuries later, scribes demanded a sign Jesus gave them only my name:  -> caption words = scribes..name:
sc=[w for w in ws if w["start"]>=start("scribes",t_Then)-0.01]
cw=txt.split(); assert len(sc)==len(cw),(len(sc),cw)
b6["cap"]["word_t"]=[round(max(0,w["start"]-t_Then),3) for w in sc]
nb.append(b6)
for i in range(7,15): nb.append(shift(B[i]))
# ending
tA=round(start("The",54.0),3); tB=round(start("and",56.5),3); tC=round(start("He",59.0),3)
assert abs(tA-(B[14]["t"][1]+SH))<0.06,(tA,B[14]["t"][1]+SH)
nb[-1]["t"][1]=tA
def cap(txt,kw,a,b): return {"type":"caption","text":txt,"kw":kw,"word_t":wt(txt,a,a-0.02,b)}
nb.append({"t":[tA,tB],"tpl":"full","whip":True,"clips":[{"slug":"three_days_dark_tomb","motion":"pushin"}],
           "cap":cap("The One who went down into your dark","YOUR DARK",tA,tB),"fx":{"temp":5800}})
nb.append({"t":[tB,tC],"tpl":"full","clips":[{"slug":"man_rising_from_water","motion":"pushin"}],
           "cap":cap("and rose again is Jesus.","JESUS",tB,tC),"fx":{"temp":5600}})
nb.append({"t":[tC,TOT],"tpl":"full","clips":[{"slug":"risen_christ_wounds","motion":"pushin"}],
           "cap":cap("He can bring you up.","BRING YOU UP",tC,TOT),
           "fx":{"temp":4900,"rays":{"at":[0.5,0.25],"strength":0.5,"opacity":0.5}}})
for i in range(len(nb)-1): assert abs(nb[i]["t"][1]-nb[i+1]["t"][0])<1e-6,(i,nb[i]["t"],nb[i+1]["t"])
spec=dict(old); spec["_doc"]="WORDS FIX 1 2026-11-21 (owner-locked W1 Jonah words: Nineveh/fled+gracious line, 'centuries later', new ending). "+old["_doc"]
spec["audio"]=str(H/"narration_wordsfix1.mp3"); spec["beats"]=nb
(H/"livingpage_short.wordsfix1.spec.json").write_text(json.dumps(spec,indent=1,ensure_ascii=False),encoding="utf-8")
for b in nb: print(f'{b["t"][0]:7.3f}-{b["t"][1]:7.3f} {b["tpl"]:11s} {b["clips"][0]["slug"]:24s} {b["cap"]["text"][:50]}')
