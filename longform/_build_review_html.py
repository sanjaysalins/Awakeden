"""Build ONE review HTML for the two finished shorts (EW01, EW02): per painting show the
source still + the animated gallery clip + a strip of slice-frames (the framings the tour
cut to), so the user can flag which clips to redo. Slices are sampled with ffmpeg."""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LF = ROOT / "longform"
SL = LF / "_shorts_review_slices"; SL.mkdir(exist_ok=True)
OUT = LF / "_shorts_review.html"

def uri(p): return "file:///" + str(Path(p)).replace("\\", "/")
def dur(f):
    o = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of",
        "default=nk=1:nw=1",str(f)],capture_output=True,text=True).stdout.strip()
    return float(o) if o else 0.0

def slices(clip, tag, n=6):
    """sample n frames across the clip -> list of file:/// uris"""
    d = dur(clip); out = []
    if d <= 0: return out
    for i, fr in enumerate([0.08,0.26,0.44,0.62,0.80,0.94][:n]):
        p = SL / f"{tag}_{i}.jpg"
        subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",f"{d*fr:.2f}","-i",str(clip),
            "-vframes","1","-vf","scale=180:-1",str(p)], check=False)
        if p.exists(): out.append(uri(p))
    return out

EW01 = LF/"EW01_Two_Goats/v1/short"
GC1 = EW01/"gallery_clips"; VT1 = EW01/"visual_9x16_test"
EW02 = LF/"EW02_Abraham/v1/short"; GC2 = EW02/"gallery_clips"

# (id, label, still, clip)
SHORTS = {
 "EW01 — The Two Goats": {
   "final": GC1/"ew01_short_v2.mp4",
   "paintings": [
    ("01","Hook — behind the veil", VT1/"hook.png", GC1/"01_hook.mp4"),
    ("02","Overview — the whole day", VT1/"gallery_demo/rich_atonement.png", GC1/"02_overview.mp4"),
    ("03","Two goats", VT1/"variants/s2_two_goats.png", GC1/"03_two_goats.mp4"),
    ("04","Blood within the veil", VT1/"variants/s3_blood_veil.png", GC1/"04_blood_veil.mp4"),
    ("05","Hands / confession", VT1/"variants/s4_hands_confess.png", GC1/"05_confess.mp4"),
    ("06","Scapegoat into the desert", VT1/"variants/s5_scapegoat_desert.png", GC1/"06_scapegoat.mp4"),
    ("07","Turn — the cross", GC1/"christ_turn.png", GC1/"07_turn.mp4"),
    ("08","Punch — risen Christ", VT1/"christ.png", GC1/"08_punch.mp4"),
    ("09","Close — LIVING Christ (breathing CTA)", VT1/"christ.png", GC1/"living_christ.mp4"),
   ]},
 "EW02 — Abraham & the Lamb": {
   "final": GC2/"EW02_Abraham_short.mp4",
   "paintings": [
    ("01","Hook — father & sleeping son", GC2/"01_hook.png", GC2/"01_hook.mp4"),
    ("02","The wood on Isaac's back", GC2/"02_wood.png", GC2/"02_wood.mp4"),
    ("03","Where is the lamb?", GC2/"03_lamb.png", GC2/"03_lamb.mp4"),
    ("04","Bound son / stopped knife", GC2/"04_altar.png", GC2/"04_altar.mp4"),
    ("05","The ram — substitute", GC2/"05_ram.png", GC2/"05_ram.mp4"),
    ("06","Delivered, still waiting", GC2/"06_waiting.png", GC2/"06_waiting.mp4"),
    ("07","Turn — the true Lamb (generic cross)", LF/"_shorts_bank/crucifixion_generic.png", GC2/"07_turn.mp4"),
    ("08","Punch — risen Christ (reused)", VT1/"christ.png", GC1/"08_punch.mp4"),
    ("09","Close — LIVING Christ (reused)", VT1/"christ.png", GC1/"living_christ.mp4"),
   ]},
}

cards = []
for title, data in SHORTS.items():
    final = data["final"]
    rows = []
    for pid, label, still, clip in data["paintings"]:
        tag = (title.split()[0] + "_" + pid)
        frames = slices(clip, tag) if Path(clip).exists() else []
        fr_html = "".join(f'<img class="sl" src="{u}">' for u in frames) or '<span class="miss">no clip</span>'
        still_html = f'<img class="still" src="{uri(still)}">' if Path(still).exists() else '<span class="miss">no still</span>'
        clip_html = (f'<video class="clip" src="{uri(clip)}" controls preload="metadata"></video>'
                     if Path(clip).exists() else '<span class="miss">no clip</span>')
        rows.append(f'''<div class="card">
          <div class="badge">#{pid}</div>
          <div class="lbl">{label}</div>
          <div class="media"><div class="col"><div class="cap">painting</div>{still_html}</div>
            <div class="col"><div class="cap">clip ▶</div>{clip_html}</div></div>
          <div class="cap">slices the tour cut to →</div><div class="slices">{fr_html}</div>
        </div>''')
    final_html = (f'<video class="final" src="{uri(final)}" controls preload="metadata"></video>'
                  if Path(final).exists() else '')
    cards.append(f'<section><h2>{title}</h2><div class="finalwrap"><div class="cap">FULL SHORT ▶</div>{final_html}</div>'
                 f'<div class="grid">{"".join(rows)}</div></section>')

html = f'''<!doctype html><html><head><meta charset="utf-8"><title>Shorts review — flag clips to redo</title>
<style>
 body{{background:#13110e;color:#e9e1d3;font-family:system-ui,Segoe UI,sans-serif;margin:0;padding:24px}}
 h1{{margin:0 0 4px}} p.sub{{color:#a99;margin:0 0 20px}}
 h2{{margin:30px 0 10px;color:#e7c98a;border-bottom:1px solid #3a2f22;padding-bottom:6px}}
 .finalwrap{{margin-bottom:18px}} .final{{height:420px;background:#000;border-radius:8px}}
 .grid{{display:flex;flex-wrap:wrap;gap:16px}}
 .card{{background:#1d1813;border:1px solid #342a1f;border-radius:10px;padding:12px;width:430px;position:relative}}
 .badge{{position:absolute;top:10px;right:12px;background:#7a5a1f;color:#fff;font-weight:700;border-radius:6px;padding:2px 8px}}
 .lbl{{font-weight:600;margin-bottom:8px}}
 .media{{display:flex;gap:10px}} .col{{flex:1}}
 .cap{{font-size:11px;color:#b9a;text-transform:uppercase;letter-spacing:.04em;margin:4px 0}}
 .still{{width:100%;border-radius:6px;display:block}}
 .clip{{width:100%;height:300px;background:#000;border-radius:6px;display:block}}
 .slices{{display:flex;gap:4px;margin-top:4px}} .sl{{width:64px;border-radius:3px;border:1px solid #000}}
 .miss{{color:#c66;font-size:12px}}
</style></head><body>
<h1>Awakeden shorts — clip review</h1>
<p class="sub">Per painting: the source <b>still</b>, the animated <b>clip</b> (play it), and the <b>slice frames</b> the tour cut to.
Watch each clip + scan its slices — tell me by <b>#</b> which to <b>redo</b> (bad framing / morph / off-subject / dancing) or <b>reconsider</b> (wrong painting).</p>
{"".join(cards)}
</body></html>'''
OUT.write_text(html, encoding="utf-8")
print(f"wrote {OUT}")
