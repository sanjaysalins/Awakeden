"""Build _CLIPS_REVIEW.html for the Bronze Serpent LONG pilot -- all 68
spreads in spread-number order, each showing its animated clip (playable
<video>) if one exists, or a clear "pending $0 deterministic fallback"
placeholder for the 8 spreads deferred there. Reuses _build_review.py's own
ROWS table (spread metadata) so the two galleries never drift apart.

Safe to re-run at any point -- reflects whatever is on disk right now.

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent_long/_build_clips_review.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _build_review as br

OUT_HTML = HERE / "_CLIPS_REVIEW.html"
CLIPS = HERE / "clips"

# All 11 spreads with no animated clip: 3 were ALWAYS $0-by-design (never in
# the animation JOBS list at all), the other 8 failed real content defects
# twice and were deferred there per this project's 2-strikes rule.
DETERMINISTIC_PENDING = {
    "s43_insert_scholars_margin2": "always $0 by design -- insert page, lift_away + camera pan only",
    "s67_insert_gilded_proclamation2": "always $0 by design -- insert page, lift_away + camera pan only",
    "s68_landing": "always $0 by design -- the landing's own torn-page device",
    "s28_forge_acting": "3-strikes failure (hammer-strike) -- same class as the short's s06_forge",
    "s55_hezekiah_breaks": "same 3-strikes failure class, caught by eye-check before spending",
    "s44_shadow_cross": "the cross-shaped shadow inverted into a serpent silhouette -- doctrinally too risky for a 3rd generative attempt",
    "s12_vc_wherefore": "invented gesture defect; the plan's own Device column already wanted a $0 push-in here",
    "s18_moses_empty_hands": "mouth-opening defect recurred on the redo (2-strikes)",
    "s14_serpent_hint": "serpent locomotion recurred on the redo (2-strikes)",
    "s46_thesis_pair": "serpent's mouth opening recurred on the redo (2-strikes)",
    "s51_christ_draw_all_men": "a new invented gesture appeared on the redo (2-strikes)",
}
ALWAYS_ZERO = {"s43_insert_scholars_margin2", "s67_insert_gilded_proclamation2", "s68_landing"}

CSS = """
  body { background:#16181d; color:#e8e4d8; font-family:Georgia, serif; line-height:1.55; padding:28px 18px 90px; }
  .wrap { max-width:1500px; margin:0 auto; }
  h1 { color:#e9c877; font-size:1.8rem; margin-bottom:4px; }
  .sub { color:#9aa0ad; margin-bottom:24px; font-size:14px; max-width:90ch; }
  .bar { background:#1e2129; border:1px solid #333; border-radius:8px; padding:10px 16px; margin-bottom:22px; font-size:14px; }
  .bar b { color:#e9c877; }
  .grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(320px,1fr)); gap:16px; }
  .card { background:#1e2129; border-radius:8px; overflow:hidden; border:2px solid #333; }
  .card.clean { border-color:#3a4a3a; }
  .card.pending { border-color:#8a7a2a; }
  .card.bydesign { border-color:#3a3a4a; }
  .card video, .card img { width:100%; display:block; background:#000; }
  .noclip { aspect-ratio:16/9; display:flex; align-items:center; justify-content:center; flex-direction:column;
    color:#e9c877; font-size:.85rem; background:#2a2418; text-align:center; padding:14px; }
  .noclip .reason { color:#9aa0ad; font-size:.78rem; margin-top:6px; }
  .cap { padding:10px 12px; font-size:.85rem; color:#c9c4b6; }
  .cap b { color:#e8e4d8; display:block; }
  .win { color:#8a95a8; font-size:.75rem; display:block; margin:2px 0 6px; }
  .status { display:inline-block; font-size:.7rem; padding:2px 7px; border-radius:4px; margin-top:6px; }
  .status.clean { background:#2a3a2a; color:#9fd39f; }
  .status.pending { background:#3a3320; color:#e9c877; }
  .status.bydesign { background:#2a2a3a; color:#a9b4d9; }
"""


def build():
    clean_n = 0
    pending_n = 0
    bydesign_n = 0
    cards = []
    for num, name, beat, window, cap, _pre in br.ROWS:
        clip = CLIPS / f"{name}.mp4"
        if clip.exists():
            clean_n += 1
            media = f'<video src="clips/{name}.mp4" controls preload="metadata" muted loop></video>'
            status_cls, status_txt = "clean", "clean clip"
        elif name in ALWAYS_ZERO:
            bydesign_n += 1
            reason = DETERMINISTIC_PENDING.get(name, "")
            media = f'<div class="noclip">$0 deterministic device<br>not yet built<div class="reason">{reason}</div></div>'
            status_cls, status_txt = "bydesign", "$0 by design, not a failure"
        else:
            pending_n += 1
            reason = DETERMINISTIC_PENDING.get(name, "not yet built")
            media = f'<div class="noclip">$0 deterministic push-in<br>not yet built<div class="reason">{reason}</div></div>'
            status_cls, status_txt = "pending", "deferred after 2 failures"
        cards.append(f"""  <div class="card {status_cls}">{media}
    <div class="cap"><b>#{num:02d} {name}</b><span class="win">Beat {beat} · {window}</span>
    {cap}
    <div class="status {status_cls}">{status_txt}</div></div></div>""")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bronze Serpent LONG — clips review</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<h1>BRONZE SERPENT LONG — 68 spreads, animation status</h1>
<div class="sub">Full-length (~9:50) pilot, Numbers 21 / John 3:14 typology. Click any clip to play.
Amber-bordered cards failed a real content defect twice and were deferred to the $0 device per this
project's 2-strikes rule. Blue-bordered cards were ALWAYS meant to be $0 (insert pages + the landing) --
not failures, just not built yet.</div>
<div class="bar"><b>{clean_n}</b> clean clips &nbsp;·&nbsp; <b>{pending_n}</b> deferred after failures &nbsp;·&nbsp;
<b>{bydesign_n}</b> always-$0 by design &nbsp;·&nbsp; {clean_n + pending_n + bydesign_n} spreads total</div>
<div class="grid">
{chr(10).join(cards)}
</div>
</div>
</body>
</html>
"""
    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"[clips-review] {clean_n} clean, {pending_n} pending -> {OUT_HTML}")


if __name__ == "__main__":
    build()
