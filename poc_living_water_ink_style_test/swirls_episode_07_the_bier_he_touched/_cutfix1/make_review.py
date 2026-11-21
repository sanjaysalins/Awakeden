import subprocess
from pathlib import Path
H=Path(__file__).resolve().parent; EP=H.parent
OLD=EP/"redo_v2"/"ep07_redo_v2_final.mp4"; NEW=H/"ep07_redo_v2_cutfix1_final.mp4"
def fr(src,t,name):
    subprocess.run(["ffmpeg","-y","-v","error","-ss",str(t),"-i",str(src),"-frames:v","1","-vf","scale=360:640",str(H/"rv"/name)],check=True)
    return "rv/"+name
sets=[
 ("CUT 1 - cut: 'Everyone kept their distance. That was survival, not cruelty.'",
  [(OLD,11.5,"says: ...and you were unclean."),(OLD,14.5,"CUT: 'kept their distance'"),(OLD,16.0,"CUT: 'not cruelty'"),(OLD,17.8,"Jesus walked toward her")],
  [(NEW,11.5,"says: ...and you were unclean."),(NEW,12.2,"(gap, 0.9 s)"),(NEW,12.9,"Jesus walked toward her"),(NEW,13.6,"Jesus walked toward her")]),
 ("CUT 2 - cut: 'Then he touched what no one else would touch:'",
  [(OLD,25.0,"Weep not."),(OLD,26.5,"CUT: 'Then he touched what no one else...'"),(OLD,29.5,"and he came and touched the bier"),(OLD,31.0,"touched the bier")],
  [(NEW,20.0,"Weep not."),(NEW,21.2,"(gap)"),(NEW,22.2,"and he came and touched the bier"),(NEW,23.6,"touched the bier")]),
]
h=['<!doctype html><meta charset=utf-8><title>Cutfix1 review</title><style>body{font:22px Arial;background:#f6f1e6;margin:20px}h1{font-size:34px}h2{font-size:26px;margin-top:40px}.row{display:flex;gap:12px;margin:8px 0}.c{width:24%}.c img{width:100%;border:2px solid #444}.c p{margin:4px 0;font-size:18px}.old{color:#a33}.new{color:#276}.big{font-size:26px;font-weight:bold}</style>',
 '<h1>Ep07 Bier - CUTFIX1</h1><p class=big>Two false lines cut. Nothing else changed. Film 71.9 s to 64.6 s.</p>',
 '<p>Old: redo_v2/ep07_redo_v2_final.mp4<br>New: _cutfix1/ep07_redo_v2_cutfix1_final.mp4</p>']
for title,o,n in sets:
    h.append(f"<h2>{title}</h2><p class=old><b>OLD</b></p><div class=row>")
    for i,(s,t,l) in enumerate(o): h.append(f"<div class=c><img src='{fr(s,t,'o%d_%s.png'%(int(t*10),title[4]))}'><p>{t}s - {l}</p></div>")
    h.append("</div><p class=new><b>NEW</b></p><div class=row>")
    for i,(s,t,l) in enumerate(n): h.append(f"<div class=c><img src='{fr(s,t,'n%d_%s.png'%(int(t*10),title[4]))}'><p>{t}s - {l}</p></div>")
    h.append("</div>")
h.append("""<h2>Baked words still on the pages (not regenerated)</h2><ul>
<li><b>0:08 to 0:12.4 (page F01):</b> small caption 'kept their distance' and note 'NOTE: survival, not cruelty'. The narrator no longer says these.</li>
<li><b>0:20.9 to 0:22.6 (page F03A, 1.7 s):</b> panel label 'no one else would'. The narrator no longer says it.</li>
<li>Page F01B (all of it, labelled 'kept their distance' / 'survival') was removed whole. No text left from it.</li></ul>""")
(H/"..\_CUTFIX1_REVIEW.html").write_text("\n".join(h),encoding="utf-8") if False else (EP/"_CUTFIX1_REVIEW.html").write_text("\n".join(h).replace("rv/","_cutfix1/rv/"),encoding="utf-8")
print("ok")
