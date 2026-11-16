import os
V="../../batches/cluster_01_cross/mockers_words_ps227/visual/"
ROOT=r"F:\slk\PycharmProjects\JesusInTheBible\batches\cluster_01_cross\mockers_words_ps227\visual"
M=[("m01","Jesus dying; leaders shout","golgotha_hill_wide"),("m02","Leader shouts (Matt 27:43)","rulers_sneering"),
("m03","King David","david_writing_psalm"),("m04","Psalm scroll (Ps 22:8)","psalm_scroll_night"),
("m05","People passing by","wagging_heads_close"),("m06","Come down (Matt 27:40)","crowd_mocking"),
("m07","He stayed","face_on_cross"),("m08","Father, forgive","jesus_looks_down"),
("m09","Every nation turns","look_up_faces"),("m10","Landing: turn to Him","us_under_cross_shadow")]
rows=""; nc=0; ns=0
for pid,lab,f in M:
    clip=os.path.exists(os.path.join(ROOT,"clips",f+".mp4")); nc+=clip; ns+=(not clip)
    tag='<b class=g>clip ready ($0)</b>' if clip else '<b class=r>still only: needs a clip</b>'
    rows+=f'<div class=c><a href="{V}{f}.png"><img src="{V}{f}.png"></a><div><b>{pid}</b> {lab}<br>{tag}</div></div>'
open("_MOCKERS_REUSE.html","w",encoding="utf-8").write(f'''<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Mockers: reuse check</title>
<style>body{{margin:0;background:#f7f3ea;color:#1b1b1b;font:20px/1.5 system-ui;padding:0 16px 50px}}@media(prefers-color-scheme:dark){{body{{background:#15171c;color:#f1ede2}}}}
.w{{max-width:1000px;margin:auto}}h1{{font-size:2rem}}.g{{color:#1e7a3c}}.r{{color:#b3261e}}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}}
.c{{background:#8881;border-radius:10px;padding:8px;font-size:.9rem}}img{{width:100%;border-radius:6px}}.box{{border:3px solid #b8860b;border-radius:12px;padding:12px 16px;margin:14px 0}}</style></head><body><div class=w>
<h1>Mockers: what we can reuse</h1>
<div class=box>The old Mockers short already has stills and clips. I matched them to the 10 new panels. <b>{nc} have a clip. {ns} are still only.</b><br>
Only m09 (every nation) is a weak match. Click any picture to see it big.</div>
<div class=grid>{rows}</div>
<div class=box><b>Cost if you say yes:</b><br>New stills: $0 to about $0.40 (only m09, if the old one looks wrong).<br>
New clips for the {ns} still-only panels: about $3 to $4.50 (Seedance $0.72, Kling $1.13).<br>
Total about $3 to $5, down from $13. Nothing is spent yet.<br>
Narration to hear first: <a href="file:///F:/slk/PycharmProjects/JesusInTheBible/batches/cluster_01_cross/mockers_words_ps227/audio_y4/narration.mp3">narration.mp3 (71s)</a></div>
<div class=box><b>My pick: A.</b> Reuse all old pictures. Make only the {ns} missing clips, about $3 to $4.50.<br>B. Make new pictures for everything. About $13. The old look is the same style, so I do not advise it.<br><b>Say A or B?</b> (Please listen to the narration first.)</div>
</div></body></html>''')
print(nc,ns)
