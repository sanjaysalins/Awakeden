"""Build a one-page still-review gallery for the EW01 ink migration HUMAN
stills gate. $0, no render. Lists all 25 stills with scene id/title/fix-note,
flags scenes still under question, and gives each still its own notes box
(autosaved to the browser, and copy-able as one paste-ready block for chat).

Writes v1/visual_16x9_inked/_STILLS_REVIEW.html.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DIR = HERE / "v1" / "visual_16x9_inked"
plan = json.loads((DIR / "scene_plan.json").read_text(encoding="utf-8"))

NEEDS_LOOK = set()  # all eye-audit items cleared (2026-07-21 session 2)

rows = []
for s in plan["scenes"]:
    sid = s["id"]
    matches = sorted(DIR.glob(f"{sid:02d}_*.png"))
    fname = matches[0].name if matches else "MISSING.png"
    fix = s.get("_fix_note", "")
    flag = sid in NEEDS_LOOK
    rows.append((sid, s["title"], fname, fix, flag))

cards = []
for sid, title, fname, fix, flag in rows:
    badge = ""
    if flag:
        badge = '<div class="flag">NEEDS ANOTHER LOOK — faint star mark on hands survived 2 fix rounds</div>'
    elif fix:
        badge = f'<div class="fixed">re-rolled: {fix}</div>'
    cards.append(f"""
    <div class="card{' flagged' if flag else ''}">
      <div class="num">#{sid:02d}</div>
      <img src="{fname}" loading="lazy">
      <div class="title" data-title="{title}">{title}</div>
      {badge}
      <textarea class="notebox" data-sid="{sid}" placeholder="Type your note on #{sid:02d} here..."></textarea>
    </div>""")

html = f"""<!doctype html><html><head><meta charset="utf-8">
<title>EW01 Two Goats — inked stills review (HUMAN GATE)</title>
<style>
body {{ background:#111; color:#eee; font-family:system-ui,sans-serif; margin:0; padding:24px; }}
h1 {{ font-size:20px; }}
.toolbar {{ position:sticky; top:0; background:#111; padding:12px 0 18px; z-index:10; border-bottom:1px solid #333; margin-bottom:18px; }}
.copybtn {{ font-size:16px; font-weight:bold; padding:12px 22px; border-radius:8px; border:none;
           background:#2a7; color:#fff; cursor:pointer; }}
.copybtn:hover {{ background:#3c8; }}
#copystatus {{ margin-left:14px; font-size:14px; color:#9cf; }}
#compiled {{ display:none; width:100%; height:140px; margin-top:12px; background:#000; color:#9f9;
            font-family:monospace; font-size:13px; padding:10px; border-radius:6px; border:1px solid #444; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(340px,1fr)); gap:18px; }}
.card {{ background:#1c1c1c; border-radius:10px; overflow:hidden; border:2px solid #333; display:flex; flex-direction:column; }}
.card.flagged {{ border-color:#e33; }}
.card img {{ width:100%; display:block; }}
.num {{ padding:6px 10px; font-weight:bold; color:#9cf; }}
.title {{ padding:0 10px 10px; font-size:14px; }}
.fixed {{ padding:0 10px 10px; font-size:12px; color:#8f8; }}
.flag {{ padding:8px 10px; font-size:13px; color:#fff; background:#a22; font-weight:bold; }}
.notebox {{ margin:0 10px 12px; width:calc(100% - 20px); min-height:56px; resize:vertical;
           background:#111; color:#eee; border:1px solid #444; border-radius:6px; padding:8px;
           font-family:inherit; font-size:13px; }}
.notebox:focus {{ border-color:#2a7; outline:none; }}
</style></head><body>
<h1>EW01 Two Goats — 25 inked stills — HUMAN stills gate</h1>
<p>All 25 rendered and eye-audited. Fixed: gray-hair witness identity,
period-correct Ark/skyline, dry altar, hand positions (scenes 2, 19), witness
identity (12), and all gore removed (goats at rest, no blood — scenes 11, 18).
Christ's hands are now CLEAN on all 6 close-ups (17,18,19,20,22,25) — the ink
style could not render a nail scar cleanly, so per the user's call the hands
carry no mark and the wound theology stays in the narration.</p>
<p>Type a note under any still that needs a change. Notes save automatically
as you type (safe to close the page and come back). When done, press the
green button and paste into the chat.</p>
<div class="toolbar">
  <button class="copybtn" onclick="copyNotes()">Copy All Notes</button>
  <span id="copystatus"></span>
  <textarea id="compiled" readonly></textarea>
</div>
<div class="grid">
{"".join(cards)}
</div>
<script>
function saveNote(id, value) {{
  localStorage.setItem('ew01_note_' + id, value);
}}
window.addEventListener('DOMContentLoaded', () => {{
  document.querySelectorAll('textarea.notebox').forEach(ta => {{
    const id = ta.dataset.sid;
    const saved = localStorage.getItem('ew01_note_' + id);
    if (saved) ta.value = saved;
    ta.addEventListener('input', () => saveNote(id, ta.value));
  }});
}});
function compileNotes() {{
  let lines = [];
  document.querySelectorAll('.card').forEach(card => {{
    const ta = card.querySelector('textarea.notebox');
    const id = ta.dataset.sid;
    const title = card.querySelector('.title').dataset.title;
    const note = ta.value.trim();
    if (note) {{
      lines.push('Scene #' + id + ' (' + title + '): ' + note);
    }}
  }});
  return lines.join('\\n');
}}
function copyNotes() {{
  const text = compileNotes();
  const out = document.getElementById('compiled');
  out.value = text || '(no notes yet — type in the boxes under each still first)';
  out.style.display = 'block';
  out.focus();
  out.select();
  const status = document.getElementById('copystatus');
  if (navigator.clipboard && window.isSecureContext) {{
    navigator.clipboard.writeText(out.value).then(() => {{
      status.textContent = 'Copied! Paste it into the chat.';
    }}).catch(() => {{
      status.textContent = 'Could not auto-copy — text is selected below, press Ctrl+C.';
    }});
  }} else {{
    try {{
      document.execCommand('copy');
      status.textContent = 'Copied! Paste it into the chat.';
    }} catch (e) {{
      status.textContent = 'Could not auto-copy — text is selected below, press Ctrl+C.';
    }}
  }}
}}
</script>
</body></html>"""

out = DIR / "_STILLS_REVIEW.html"
out.write_text(html, encoding="utf-8")
print("wrote", out)
