"""living-sketchbook -- Bronze Serpent LONG pilot: interactive redo/notes page.

Builds `_REDO_NOTES.html`: all 68 current (correct 16:9) stills in a grid,
each with a "flag for redo" checkbox + a free-text note field + a dropdown
to pick a replacement style from the now-tested style bake-off
(`poc_living_sketchbook/_style_identity_bakeoff/style_manifest.json`,
production_approved variants only -- 15 of 35, each proven to hold
character identity-lock on BOTH Moses and Jesus, per STYLE_SELECTION.md).

Pure static HTML + vanilla JS, no server needed (works from a file:// URL).
Notes autosave to localStorage as you type (survives an accidental reload)
and a "Download notes (JSON)" button saves a real file via a Blob download
link -- Claude reads that JSON back in to know what to redo and in which
style.

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent_long/_build_redo_notes.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _build_review as br  # reuse the same 68-row ROWS table, don't duplicate it

MANIFEST_PATH = HERE.parent / "_style_identity_bakeoff" / "style_manifest.json"
OUT_HTML = HERE / "_REDO_NOTES.html"
NOTES_JSON_OUT = HERE / "_redo_notes.json"  # written if a notes JSON is dropped here for a rebuild pass


def load_approved_styles():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    approved = []
    for sid, v in manifest.items():
        if v.get("status") != "production_approved":
            continue
        m_notes = v.get("scores", {}).get("moses", {}).get("note", "")
        j_notes = v.get("scores", {}).get("jesus", {}).get("note", "")
        approved.append({
            "id": sid,
            "name": v.get("name", sid),
            "family": v.get("family", ""),
            "beat_signal": v.get("beat_signal", []),
            "gold_leaf_conflict": v.get("gold_leaf_conflict", False),
            "moses_note": m_notes,
            "jesus_note": j_notes,
        })
    approved.sort(key=lambda s: s["family"])
    return approved


CSS = """
  :root { color-scheme: dark; }
  body { background:#16181d; color:#e8e4d8; font-family:Georgia, serif; line-height:1.55; padding:24px 18px 140px; }
  .wrap { max-width:1500px; margin:0 auto; }
  h1 { color:#e9c877; font-size:1.7rem; margin-bottom:4px; }
  .sub { color:#9aa0ad; margin-bottom:6px; font-size:14px; max-width:90ch; }
  .howto { background:#1e2129; border:1px solid #3a3a3a; border-left:4px solid #e9c877; border-radius:8px;
    padding:14px 18px; margin:16px 0 24px; font-size:14px; color:#c9c4b6; }
  .howto b { color:#e9c877; }
  .bar { position:sticky; top:0; z-index:10; background:#0f1014; border:1px solid #333; border-radius:8px;
    padding:10px 16px; margin-bottom:20px; display:flex; align-items:center; gap:16px; font-size:14px; flex-wrap:wrap; }
  .bar b { color:#e9c877; }
  .bar button { background:#e9c877; color:#16181d; border:none; padding:9px 18px; border-radius:6px;
    font-weight:700; cursor:pointer; font-size:14px; }
  .bar button.secondary { background:transparent; color:#e9c877; border:1px solid #e9c877; }
  .bar button:hover { opacity:.85; }
  .grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(340px,1fr)); gap:18px; }
  .card { background:#1e2129; border-radius:8px; overflow:hidden; border:2px solid #333; transition:border-color .15s; }
  .card.flagged { border-color:#c0504a; background:#241c1c; }
  .card img { width:100%; display:block; cursor:zoom-in; }
  .cap { padding:12px 14px 14px; font-size:13.5px; color:#c9c4b6; }
  .cap b { color:#e8e4d8; display:block; margin-bottom:2px; }
  .win { color:#8a95a8; font-size:12px; display:block; margin-bottom:6px; }
  .desc { margin-bottom:10px; }
  .row { display:flex; align-items:center; gap:8px; margin:8px 0 4px; }
  .row label { font-size:13px; color:#e8e4d8; cursor:pointer; user-select:none; }
  textarea.note { width:100%; box-sizing:border-box; background:#16181d; color:#e8e4d8; border:1px solid #3a3a3a;
    border-radius:6px; padding:8px; font-size:13px; font-family:inherit; resize:vertical; min-height:44px; margin-top:6px; }
  select.style-pick { width:100%; box-sizing:border-box; background:#16181d; color:#e8e4d8; border:1px solid #3a3a3a;
    border-radius:6px; padding:7px; font-size:13px; margin-top:6px; }
  .similar-tag { display:inline-block; background:#3a3320; color:#e9c877; font-size:11px; padding:2px 7px;
    border-radius:4px; margin-top:6px; }
  .lightbox { display:none; position:fixed; inset:0; background:rgba(0,0,0,.9); z-index:100; align-items:center;
    justify-content:center; padding:30px; }
  .lightbox.open { display:flex; }
  .lightbox img { max-width:100%; max-height:100%; }
"""

JS = """
const STORE_KEY = "bronzeSerpentLongRedoNotes_v1";

function loadState() {
  try { return JSON.parse(localStorage.getItem(STORE_KEY)) || {}; } catch (e) { return {}; }
}
function saveState(state) {
  localStorage.setItem(STORE_KEY, JSON.stringify(state));
  updateCount();
}
function getEntry(state, slug) {
  return state[slug] || { flagged: false, note: "", style: "" };
}
function updateCount() {
  const state = loadState();
  const n = Object.values(state).filter(e => e.flagged).length;
  document.getElementById("flagCount").textContent = n;
}

function onFlagChange(slug, checked) {
  const state = loadState();
  state[slug] = getEntry(state, slug);
  state[slug].flagged = checked;
  saveState(state);
  document.getElementById("card-" + slug).classList.toggle("flagged", checked);
}
function onNoteChange(slug, val) {
  const state = loadState();
  state[slug] = getEntry(state, slug);
  state[slug].note = val;
  saveState(state);
}
function onStyleChange(slug, val) {
  const state = loadState();
  state[slug] = getEntry(state, slug);
  state[slug].style = val;
  saveState(state);
}

function restoreUI() {
  const state = loadState();
  document.querySelectorAll(".card").forEach(card => {
    const slug = card.dataset.slug;
    const e = getEntry(state, slug);
    const cb = card.querySelector(".flag-cb");
    const note = card.querySelector(".note");
    const style = card.querySelector(".style-pick");
    cb.checked = !!e.flagged;
    note.value = e.note || "";
    style.value = e.style || "";
    card.classList.toggle("flagged", !!e.flagged);
  });
  updateCount();
}

function downloadNotes() {
  const state = loadState();
  const flagged = {};
  Object.keys(state).forEach(slug => {
    if (state[slug].flagged) flagged[slug] = state[slug];
  });
  const payload = {
    episode: "LS_BronzeSerpentLong",
    generated_note: "Exported from _REDO_NOTES.html by the user",
    flagged_spreads: flagged
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "_redo_notes.json";
  document.body.appendChild(a);
  a.click();
  a.remove();
}

function clearAll() {
  if (!confirm("Clear ALL flags and notes? This can't be undone.")) return;
  localStorage.removeItem(STORE_KEY);
  restoreUI();
}

function openLightbox(src) {
  document.getElementById("lbImg").src = src;
  document.getElementById("lightbox").classList.add("open");
}
function closeLightbox() {
  document.getElementById("lightbox").classList.remove("open");
}

window.addEventListener("DOMContentLoaded", restoreUI);
"""


def build():
    styles = load_approved_styles()
    style_options = ['<option value="">-- pick a replacement style (optional) --</option>']
    for s in styles:
        gold = " ⚠️gold-leaf, glory-beats-only" if s["gold_leaf_conflict"] else ""
        beat = ", ".join(s["beat_signal"]) if s["beat_signal"] else "general"
        label = f'{s["name"]} [{s["family"]} | {beat}]{gold}'
        style_options.append(f'<option value="{s["id"]}">{label}</option>')
    style_options_html = "\n".join(style_options)

    style_ref_rows = []
    for s in styles:
        gold = ' <span class="similar-tag">gold-leaf / glory beats only</span>' if s["gold_leaf_conflict"] else ""
        style_ref_rows.append(
            f'<div class="v" style="margin-bottom:8px"><b>{s["name"]}</b> '
            f'<span style="color:#8a95a8">[{s["family"]}]</span>{gold}<br>'
            f'<span style="font-size:12.5px;color:#9aa0ad">Moses: {s["moses_note"]} · Jesus: {s["jesus_note"]}</span></div>'
        )
    style_ref_html = "\n".join(style_ref_rows)

    cards = []
    for num, name, beat, window, cap, pre_approved in br.ROWS:
        png = br.s2.OUT / f"{name}.png"
        exists = png.exists() and png.stat().st_size > 1000
        img_html = (f'<img src="stills/{name}.png" loading="lazy" onclick="openLightbox(this.src)">'
                     if exists else '<div style="padding:60px 0;text-align:center;color:#666">not rendered</div>')
        cards.append(f"""  <div class="card" id="card-{name}" data-slug="{name}">
    {img_html}
    <div class="cap">
      <b>#{num:02d} {name}</b><span class="win">Beat {beat} · {window}</span>
      <div class="desc">{cap}</div>
      <div class="row">
        <input type="checkbox" class="flag-cb" id="flag-{name}" onchange="onFlagChange('{name}', this.checked)">
        <label for="flag-{name}">Flag this spread for redo</label>
      </div>
      <textarea class="note" placeholder="Why redo it? e.g. 'looks too similar to s09' or 'pose repeats s26'"
        onchange="onNoteChange('{name}', this.value)"></textarea>
      <select class="style-pick" onchange="onStyleChange('{name}', this.value)">
        {style_options_html}
      </select>
    </div>
  </div>""")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bronze Serpent LONG — redo notes</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<h1>BRONZE SERPENT LONG — flag redos + pick new styles</h1>
<div class="sub">All 68 spreads, correct 16:9. Flag any that need a redo (similar-looking ones, weak
compositions, whatever you catch), leave a note, and optionally pick a replacement style from the
15 now-tested, character-identity-proven styles below. Your picks autosave to this browser as you go —
click "Download notes" when done and send the file back.</div>

<div class="howto">
<b>How to use this page:</b> 1) Scroll the grid, click any image to zoom. 2) Tick "Flag this spread for
redo" on ones that need fixing. 3) In the note box, say why — especially if two spreads look too alike,
name both (e.g. "too similar to s26, redo this one"). 4) Optionally pick a new style from the dropdown —
leave blank to just re-roll the same style. 5) When done, click <b>"Download notes (JSON)"</b> below —
it saves a small file to your Downloads folder. Send that file (or its contents) back and it'll be read
in directly as the redo list.
</div>

<div class="bar">
  <span><b id="flagCount">0</b> spreads flagged</span>
  <button onclick="downloadNotes()">⬇ Download notes (JSON)</button>
  <button class="secondary" onclick="clearAll()">Clear all</button>
</div>

<details style="margin-bottom:22px">
<summary style="cursor:pointer;color:#e9c877;font-size:14px">Reference: the 15 approved replacement styles (click to expand)</summary>
<div style="margin-top:12px">{style_ref_html}</div>
</details>

<div class="grid">
{chr(10).join(cards)}
</div>
</div>

<div class="lightbox" id="lightbox" onclick="closeLightbox()">
  <img id="lbImg" src="">
</div>

<script>{JS}</script>
</body>
</html>
"""
    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"[redo-notes] {len(styles)} approved styles listed -> {OUT_HTML}")


if __name__ == "__main__":
    build()
