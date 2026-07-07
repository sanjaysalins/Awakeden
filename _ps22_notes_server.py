#!/usr/bin/env python
"""Local review server for Psalm-22 redo notes. Serves the gallery over http://localhost
so the Save button works (same-origin fetch -> writes _ps22_redo_notes.txt). $0, offline."""
import json, http.server, socketserver, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EP = ROOT / "longform/02_Psalm_22_Song_From_The_Cross/v1/visual_16x9_inked"
NOTES_OUT = ROOT / "_ps22_redo_notes.txt"
PORT = 8777

spec = json.load(open(EP / "livingpage_full.spec.json", encoding="utf-8"))
occ = {}
for i, b in enumerate(spec["beats"], 1):
    for c in b.get("clips", []):
        s = c.get("slug")
        if s:
            occ.setdefault(s, []).append((i, round(b["t"][0], 1)))
slugs = sorted(occ, key=lambda s: occ[s][0][1])

cards = []
for s in slugs:
    times = ", ".join(f"{t:.0f}s" for _, t in occ[s])
    beats = ", ".join(str(b) for b, _ in occ[s])
    cards.append(
        '<div class="card" data-slug="' + s + '">'
        '<img src="/img/' + s + '.png" loading="lazy">'
        '<div class="meta"><div class="slug">' + s + '</div>'
        '<div class="times">appears @ ' + times + ' &nbsp;&middot;&nbsp; beat ' + beats + '</div>'
        '<label class="chk"><input type="checkbox" class="redoStill"> redo STILL</label>'
        '<label class="chk"><input type="checkbox" class="redoAnim"> redo ANIMATION</label>'
        '<textarea class="note" placeholder="notes - what is wrong / what to change"></textarea>'
        '</div></div>')

HEAD = """<!doctype html><html><head><meta charset="utf-8"><title>Psalm 22 - redo notes</title><style>
body{background:#14120e;color:#f0ece3;font-family:system-ui,Arial;margin:0;padding:0 20px 60px}
.bar{position:sticky;top:0;background:#14120e;padding:16px 0;z-index:9;border-bottom:1px solid #3a352b}
h1{font-size:22px;margin:0 0 6px}
.hint{color:#b9ab8c;font-size:14px;margin:0 0 10px;line-height:1.5}
.btn{font-size:17px;font-weight:700;padding:11px 20px;border-radius:8px;border:0;cursor:pointer;background:#2f6b34;color:#fff;margin-right:8px}
.btn.r{background:#c6472e}
.count{margin-left:6px;color:#ffd86b;font-weight:700}
#saved{margin-left:10px;color:#8fe39a;font-weight:700}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:18px;margin-top:18px}
.card{background:#211d16;border-radius:10px;overflow:hidden;border:1px solid #33301f}
.card.flagged{border-color:#c6472e;box-shadow:0 0 0 2px #c6472e55}
.card img{width:100%;display:block;cursor:zoom-in}
.meta{padding:10px 12px}
.slug{font-weight:700;font-size:15px}
.times{color:#9b8f74;font-size:12.5px;margin:2px 0 8px}
.chk{display:inline-block;font-size:13px;font-weight:600;margin-right:14px;cursor:pointer;user-select:none}
.chk input{transform:scale(1.3);margin-right:5px;vertical-align:middle}
textarea.note{width:100%;box-sizing:border-box;margin-top:8px;min-height:52px;background:#171410;color:#f0ece3;border:1px solid #44402f;border-radius:6px;padding:7px;font-size:14px;font-family:inherit;resize:vertical}
dialog{border:0;background:#000;padding:0;max-width:96vw;max-height:96vh}
dialog img{max-width:96vw;max-height:92vh;display:block}
.x{position:fixed;top:14px;right:22px;font-size:30px;color:#fff;cursor:pointer}
</style></head><body>
<div class="bar">
 <h1>Psalm 22 long-form - redo review (SLUGS stills)</h1>
 <p class="hint">Tick <b>redo STILL</b> / <b>redo ANIMATION</b> on any card and type what is wrong. Click a picture to zoom. Notes auto-save. When done click <b>&#128190; SAVE &amp; SEND TO CLAUDE</b> - then type <b>done</b> in the chat.</p>
 <button class="btn" onclick="sendNotes()">&#128190; SAVE &amp; SEND TO CLAUDE</button>
 <button class="btn r" onclick="scrollFlagged()">&#9660; jump to flagged</button>
 <span class="count" id="count"></span><span id="saved"></span>
</div>
<div class="grid">"""

TAIL = """</div>
<dialog id="zoom"><span class="x" onclick="document.getElementById('zoom').close()">&#10005;</span><img id="zoomimg"></dialog>
<script>
var KEY="ps22_redo_notes_v1";
var store=JSON.parse(localStorage.getItem(KEY)||"{}");
function save(){
  var o={};
  document.querySelectorAll(".card").forEach(function(c){
    var s=c.dataset.slug, n=c.querySelector(".note").value.trim(),
      st=c.querySelector(".redoStill").checked, an=c.querySelector(".redoAnim").checked;
    if(n||st||an) o[s]={n:n,st:st,an:an};
    c.classList.toggle("flagged", !!(n||st||an));
  });
  localStorage.setItem(KEY, JSON.stringify(o));
  var k=Object.keys(o).length;
  document.getElementById("count").textContent = k? k+" flagged" : "";
}
document.querySelectorAll(".card").forEach(function(c){
  var s=c.dataset.slug, d=store[s];
  if(d){ c.querySelector(".note").value=d.n||""; c.querySelector(".redoStill").checked=!!d.st; c.querySelector(".redoAnim").checked=!!d.an; }
  c.querySelectorAll("input,textarea").forEach(function(el){el.addEventListener("input",save);});
  c.querySelector("img").addEventListener("click",function(){document.getElementById("zoomimg").src=c.querySelector("img").src;document.getElementById("zoom").showModal();});
});
save();
function buildText(){
  var lines=["REDO NOTES - Psalm 22 long-form",""];
  document.querySelectorAll(".card").forEach(function(c){
    var s=c.dataset.slug, n=c.querySelector(".note").value.trim(),
      st=c.querySelector(".redoStill").checked, an=c.querySelector(".redoAnim").checked;
    if(!(n||st||an)) return;
    var tag = st&&an?"STILL+ANIM":st?"STILL":an?"ANIM":"NOTE";
    lines.push("["+tag+"] "+s+" - "+(n||"(no note)"));
  });
  return lines.length>2 ? lines.join("\\n") : "";
}
function sendNotes(){
  var t=buildText();
  if(!t){alert("Nothing flagged yet - tick a box or type a note first.");return;}
  fetch("/save",{method:"POST",body:t}).then(function(r){
    document.getElementById("saved").textContent = r.ok ? "\\u2705 Saved! Now type 'done' in the chat." : "save failed";
  }).catch(function(){document.getElementById("saved").textContent="save failed - is the server running?";});
}
function scrollFlagged(){var f=document.querySelector(".card.flagged"); if(f) f.scrollIntoView({behavior:"smooth",block:"center"}); else alert("Nothing flagged yet.");}
</script></body></html>"""

HTML = (HEAD.replace("SLUGS", str(len(slugs))) + "".join(cards) + TAIL).encode("utf-8")


class H(http.server.BaseHTTPRequestHandler):
    def _send(self, code, ct, body):
        self.send_response(code)
        self.send_header("Content-Type", ct)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html") or self.path.startswith("/?"):
            self._send(200, "text/html; charset=utf-8", HTML)
        elif self.path.startswith("/img/"):
            name = urllib.parse.unquote(self.path[len("/img/"):])
            f = EP / name
            if f.suffix == ".png" and f.exists() and f.resolve().parent == EP.resolve():
                self._send(200, "image/png", f.read_bytes())
            else:
                self._send(404, "text/plain", b"not found")
        else:
            self._send(404, "text/plain", b"not found")

    def do_POST(self):
        if self.path == "/save":
            n = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(n)
            NOTES_OUT.write_bytes(body)
            print("SAVED notes ->", NOTES_OUT, flush=True)
            self._send(200, "text/plain", b"saved")
        else:
            self._send(404, "text/plain", b"no")

    def log_message(self, *a):
        pass


socketserver.TCPServer.allow_reuse_address = True
print(f"Psalm-22 redo review: http://localhost:{PORT}/   ({len(slugs)} stills)  notes -> {NOTES_OUT}", flush=True)
with socketserver.TCPServer(("127.0.0.1", PORT), H) as s:
    s.serve_forever()
