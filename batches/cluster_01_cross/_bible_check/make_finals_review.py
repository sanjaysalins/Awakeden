# -*- coding: utf-8 -*-
"""FINALS_REVIEW.html — the 10 rebuilt Cross-short finals in one page.
Each card gets a freshness badge computed at generation time: FRESH = the _sfx.mp4 is
newer than every still/clip that feeds it; REBUILDING = the chain hasn't reached it yet
(the video shown is still the OLD final). Re-run this script any time to restamp."""
import sys, time
from pathlib import Path
sys.stdout.reconfigure(errors="replace")
CL = Path(__file__).resolve().parents[1]

PIECES = ["crucifixion_foretold_ps2218","forsaken_cry_ps221","i_thirst_john1928",
 "into_thy_hands_luke2346","it_is_finished_john1930","pierced_zech1210",
 "thirty_pieces_zech11","today_paradise_luke2343","watch_one_hour_matt2640",
 "woman_behold_john1926"]
TITLES = {
 "crucifixion_foretold_ps2218":"Crucifixion Foretold (Ps 22:18)",
 "forsaken_cry_ps221":"The Forsaken Cry (Ps 22:1)",
 "i_thirst_john1928":"I Thirst (John 19:28)",
 "into_thy_hands_luke2346":"Into Thy Hands (Luke 23:46)",
 "it_is_finished_john1930":"It Is Finished (John 19:30)",
 "pierced_zech1210":"Pierced (Zech 12:10)",
 "thirty_pieces_zech11":"Thirty Pieces (Zech 11:12-13)",
 "today_paradise_luke2343":"Today Paradise (Luke 23:43)",
 "watch_one_hour_matt2640":"Watch One Hour (Matt 26:40)",
 "woman_behold_john1926":"Woman Behold (John 19:26-27)",
}

cards, fresh_n = [], 0
for p in PIECES:
    v = CL / p / "visual"
    final = v / f"{p}_sfx.mp4"
    srcs = list(v.glob("*.png")) + list((v / "clips").glob("*.mp4"))
    newest = max((s.stat().st_mtime for s in srcs), default=0)
    ok = final.is_file() and final.stat().st_mtime >= newest
    fresh_n += ok
    badge = ('<span class="b fresh">FRESH — rebuilt from the fact-card stills</span>' if ok else
             '<span class="b old">REBUILDING — this file is still the OLD final</span>')
    stamp = time.strftime("%H:%M", time.localtime(final.stat().st_mtime)) if final.is_file() else "—"
    cards.append(
        f'<div class="card"><div class="t">{TITLES[p]}</div>{badge}'
        f'<div class="m">{p}_sfx.mp4 · file time {stamp}</div>'
        f'<video controls preload="none" src="../{p}/visual/{p}_sfx.mp4"></video></div>')

html = f"""<!doctype html><meta charset="utf-8"><title>Cross cluster — rebuilt finals review</title>
<style>body{{font-family:system-ui,sans-serif;background:#111;color:#eee;margin:20px}}
h1{{font-size:20px}} p{{color:#ccc;font-size:14px;max-width:860px}}
.grid{{display:flex;flex-wrap:wrap;gap:16px}}
.card{{background:#1c1c1c;border:1px solid #333;border-radius:8px;padding:12px;width:330px}}
video{{width:100%;margin-top:8px;border-radius:4px}}
.t{{font-weight:700;font-size:14px;margin-bottom:6px}}
.m{{color:#888;font-size:11px;margin-top:4px}}
.b{{font-size:11px;padding:2px 8px;border-radius:10px}}
.fresh{{background:#153;color:#8f8}} .old{{background:#431;color:#fa6}}</style>
<h1>Rebuilt Cross-short finals — {fresh_n}/10 fresh (generated {time.strftime("%Y-%m-%d %H:%M")})</h1>
<p>The rebuild chain replaces each final in place (build &rarr; score &rarr; SFX bed; the comic
boxes are the captions). A card marked REBUILDING still plays the OLD video — check back or
ask me to restamp this page. Stills: <a href="REBUILD_REVIEW.html">REBUILD_REVIEW.html</a> ·
Clips: <a href="CLIP_QC.html">CLIP_QC.html</a></p>
<div class="grid">{chr(10).join(cards)}</div>"""
out = CL / "_bible_check" / "FINALS_REVIEW.html"
out.write_text(html, encoding="utf-8")
print(f"wrote {out}  ({fresh_n}/10 fresh)")
