r"""wordsfix1 post chain (same as trim_v6/build_v6.py score -> sfx -> final, re-anchored; all outputs in visual/_wordsfix1_pool, nothing overwritten)
  .venv\Scripts\python.exe post.py score|sfx|final"""
import json, subprocess, sys
from pathlib import Path
H=Path(__file__).resolve().parent; P=H.parent; ROOT=P.parents[2]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT/"sfx_pilots"))
POOL=P/"visual"/"_wordsfix1_pool"; STEM="sign_of_jonah_matt1240"
PREV=POOL/"livingpage_short.wordsfix1.spec_preview.mp4"; SCORED=POOL/f"{STEM}_scored_wordsfix1.mp4"; SFX=POOL/f"{STEM}_sfx_wordsfix1.mp4"
FINAL=P/"visual"/f"{STEM}_sfx_v6trim_wordsfix1.mp4"
spec=json.load(open(POOL/"livingpage_short.wordsfix1.spec.json",encoding="utf-8")); Bt=spec["beats"]; total=spec["total"]
al=json.load(open(H/"alignment_wordsfix1.json",encoding="utf-8"))
def st(i): return Bt[i]["t"][0]
def en(i): return Bt[i]["t"][1]
# beat indexes (new spec): 5 lot, 6 scribes, 7 deep, 12 HE ROSE, 13 'sure', 14 'that far'
def score():
    import run_piece
    pj=json.load(open(P/"piece.json",encoding="utf-8")); sc=pj["score"]
    w_my=next(w["start"] for w in al if w["w"]=="my" and w["start"]>st(6))
    w_heart=next(w["end"] for w in al if w["w"].startswith("heart") and w["start"]>st(7))
    that=next(w["start"] for w in al if w["w"]=="that" and w["start"]>50)
    sc.update(src=str(PREV), out=str(SCORED), base_seconds=total, outro_hold=0.0, tpad="0", fade_out=2.5,
              dark_trim_end=f"{st(12)-0.08:.1f}", dips=[[f"{w_my-0.13:.2f}", f"{w_heart+0.35:.2f}", sc["dips"][0][2]]],
              cta_dip=[f"{that:.2f}", sc["cta_dip"][1]])
    print(sc); cmd=run_piece.score_cmd(P, {"score":sc})
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode: sys.exit(r.stderr[-1500:])
    print("scored",SCORED)
def sfx():
    import sfxlib; from sfxlib import layer
    s=st; e=en
    L=[layer("sea","sea_waves_shore","loop",0.0,s(6)-1.0,-35.0,fin=0.3,fout=2.5),
       layer("thunder1","thunder_low_roll","oneshot",0.3,4.0,-30.0,fout=2.0),
       layer("thunder2","thunder_low_roll","oneshot",s(5)+0.1,4.0,-33.0,fout=2.5),
       layer("creak","boat_creak_oars","loop",s(2),e(5)-s(2),-40.0,fin=1.0,fout=2.0),
       layer("plunge","rumble_deep_sub","oneshot",e(5),4.5,-32.0,fin=0.2,fout=2.5),
       layer("murmur","crowd_murmur_distant","loop",s(6),e(6)-s(6),-38.0,fin=0.8,fout=1.2),
       layer("hollow2","air_hollow_desolate","loop",s(7),s(10)-s(7),-38.0,filt="lowpass=f=3000",fin=1.5,fout=2.0),
       layer("wind","wind_desert_bleak","loop",s(10),e(11)-s(10),-41.0,fin=2.0,fout=1.5),
       layer("stone","stone_roll_tomb","oneshot",s(12)-0.08,2.2,-27.0,fout=0.8),
       layer("dawn","dawn_morning_warm","loop",s(12)+0.4,total-s(12)-0.4,-36.0,filt="lowpass=f=3400",fin=3.0)]
    sfxlib.show_plan("Jonah wordsfix1",L); sfxlib.build(SCORED,SFX,L); sfxlib.measure(SFX)
def final():
    fx=json.loads((ROOT/"poc_comic_page/_audit/fixes/sign-of-jonah.json").read_text(encoding="utf-8-sig"))
    v5=json.load(open(P/"trim_v6/_v5_backup/audio__alignment.json",encoding="utf-8"))
    d=fx["decode_cards"][0]
    old_jonas=next(w["start"] for w in v5 if w["w"].startswith("Jonas"))
    jonas=next(w["start"] for w in al if w["w"].startswith("Jonas"))
    j0,j1=jonas+(d["t0"]-old_jonas),jonas+(d["t1"]-old_jonas)
    l1,l2=[x.strip() for x in fx["hook_text"].split("/")]
    FONT="C\:/Windows/Fonts/impact.ttf"
    cards=[(l1,104,"white",930,0,2.0),(l2,104,"0xF2C14E",1080,0,2.0),(d["old"],104,"white",930,j0,j1),("= "+d["plain"],110,"0xF2C14E",1080,j0,j1)]
    vf=",".join(f"drawtext=fontfile='{FONT}':text='{t.replace(':',chr(92)+':')}':fontsize={sz}:fontcolor={c}:box=1:boxcolor=black@0.64:boxborderw=20:x=(w-text_w)/2:y={y}:enable='between(t,{a:.2f},{b:.2f})'" for t,sz,c,y,a,b in cards)
    subprocess.run(["ffmpeg","-y","-v","error","-i",str(SFX),"-vf",vf,"-c:v","libx264","-crf","18","-preset","medium","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",str(FINAL)],check=True)
    print("FINAL",FINAL, "jonas card",j0,j1)
for n in sys.argv[1:]: globals()[n]()
