#!/usr/bin/env python
"""build_upload_tracker.py — the paste-ready UPLOAD TRACKER page (_UPLOAD_TRACKER.html).

The browser runbook for posting: every ready piece as a card (video file,
publish pack, captions.srt, all four thumbnails, read page, tech check), one
row per platform. Paste the URL you got after uploading into the row's box and
click COPY — you get the exact `upload_tracker.py --set` command; run it in the
repo terminal. That command is THE one write path: it records the dated ledger
entry and (for YouTube) updates the website manifest + read pages.

Durable state lives in data/release_ledger.json — NEVER in this page (the
HF-POC localStorage tracker lost batches; this one is a stateless view that
regenerates from the ledger).

  .venv\\Scripts\\python.exe build_upload_tracker.py
"""
from __future__ import annotations

import html
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from pipeline import release_state  # noqa: E402
from pipeline.episode_state import gather_episodes  # noqa: E402

OUT = ROOT / "_UPLOAD_TRACKER.html"
PLAT_LABEL = {"youtube": "▶ YouTube", "tiktok": "♪ TikTok",
              "facebook": "f Facebook", "instagram": "◎ Instagram"}

CANON = [
    ("Audience", "NOT made for kids"),
    ("Altered content / AI disclosure", "YES (synthetic/altered imagery)"),
    ("Category", "Education"),
    ("License", "Standard YouTube licence"),
    ("Comments", "On — hold potentially inappropriate for review"),
    ("Visibility", "Public (YouTube first; TikTok/FB/IG within 24–48h)"),
]


def probe(video: Path) -> dict:
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-show_entries", "format=duration",
             "-of", "json", str(video)], capture_output=True, text=True, timeout=30)
        d = json.loads(out.stdout)
        st = (d.get("streams") or [{}])[0]
        return {"w": st.get("width", 0), "h": st.get("height", 0),
                "dur": float((d.get("format") or {}).get("duration", 0))}
    except Exception:
        return {"w": 0, "h": 0, "dur": 0.0}


def flink(p: Path, label: str) -> str:
    return f"<a href='file:///{str(p).replace(chr(92), '/')}'>{html.escape(label)}</a>"


def esc(x) -> str:
    return html.escape(str(x), quote=True)


def card(s: release_state.PieceState, missing: list[str]) -> str:
    pub = s.source_dir / "publish"
    thumbs = pub / "thumbs"
    links = []
    if s.video:
        links.append(flink(s.video, "▶ video file"))
    if (pub / "PUBLISH_INDEX.html").is_file():
        links.append(flink(pub / "PUBLISH_INDEX.html", "📦 publish pack (copy buttons)"))
    if (pub / "captions.srt").is_file():
        links.append(flink(pub / "captions.srt", "📝 captions.srt"))
    for key, lbl in (("16x9", "🖼 16:9 (YouTube)"), ("9x16", "🖼 9:16 (Shorts)"),
                     ("tiktok", "🖼 TikTok cover"), ("1x1", "🖼 1:1")):
        t = thumbs / f"thumb_{key}.jpg"
        if t.is_file():
            links.append(flink(t, lbl))
    if s.read_page:
        links.append(f"<a href='https://awakeden.com/read/{esc(s.slug)}.html'>📖 read page</a>")

    tech = ""
    if s.video:
        p = probe(s.video)
        if p["w"]:
            want_916 = s.kind == "short"
            ok = (p["h"] > p["w"]) if want_916 else (p["w"] > p["h"])
            aspect = f"{p['w']}x{p['h']}"
            tech = (f"<span class='tech'>{p['dur']:.1f}s · {aspect} · "
                    + (f"<b class='ok'>aspect OK</b>" if ok else
                       f"<b class='bad'>WRONG ASPECT for a {esc(s.kind)}</b>") + "</span>")

    rows = []
    for plat in s.post_platforms:
        e = s.ledger.get(plat)
        if e:
            url = esc(e.get("url", ""))
            rows.append(
                f"<tr class=done><td>{PLAT_LABEL[plat]}</td>"
                f"<td colspan=2>✅ posted {esc(e.get('posted', '?'))} — "
                f"<a href='{url}'>{url}</a></td></tr>")
        else:
            iid = f"u_{s.slug}_{plat}"
            rows.append(
                f"<tr><td>{PLAT_LABEL[plat]}</td>"
                f"<td><input id='{iid}' placeholder='paste the {esc(plat)} URL after uploading'></td>"
                f"<td><button onclick=\"cmd(this,'{esc(s.slug)}','{esc(plat)}')\">COPY command</button></td></tr>")

    badge = "<span class='c long'>LONG</span> " if s.kind == "long" else ""
    todo = (f"<span class='c warn'>to post: {', '.join(missing)}</span>"
            if missing else "<span class='c ok'>all platforms posted</span>")
    return (f"<div class=card id='{esc(s.slug)}'>"
            f"<h3>{badge}{esc(s.title)} <span class=slug>{esc(s.slug)}"
            f"{' · ' + esc(s.cluster) if s.cluster else ''}</span> {todo}</h3>"
            f"<div class=links>{' · '.join(links)} {tech}</div>"
            f"<table>{''.join(rows)}</table></div>")


def episode_block(ep, members: list) -> str:
    """One release CAMPAIGN, not N unrelated rows: the long, then its shorts in
    order, wrapped together the way Furgiven groups an episode's whole rollout.

    Does NOT assert a generic posting cadence ("long first, then shorts") —
    red-team 2026-07-15 found that false for the one real episode: Psalm 22's
    OWN RELEASE_CALENDAR.md schedules two of its shorts as pre-long trailers,
    the opposite order. Point at the calendar instead of inventing a rule."""
    inner = "".join(card(s, missing) for s, missing in members)
    # shorts_posted_any (bar): real progress the 24-48h cross-post lag (this
    # file's own CANON table) would otherwise hide behind a stuck 0% bar for
    # days after a genuine YouTube post (red-team 2026-07-15)
    pct = int(100 * ep.shorts_posted_any / ep.shorts_total) if ep.shorts_total else 0
    return (
        f"<div class=epblock><div class=epblock-head>"
        f"<h3>{esc(ep.title)} <span class=slug>episode</span> "
        f"<span class='c warn'>{esc(ep.status)}</span></h3>"
        f"<div class=sub>{ep.shorts_posted}/{ep.shorts_total} shorts fully posted"
        f" ({ep.shorts_posted_any}/{ep.shorts_total} posted somewhere) · long "
        + (esc("posted") if ep.long_posted else
           esc("ready to post (not shown below — mark it studio_complete in the manifest first)")
           if ep.long_ready else esc("not yet marked ready in the catalogue"))
        + " — check RELEASE_CALENDAR.md for this episode's actual posting order"
          "</div>"
        f"<div class=barwrap><div class='bar posted' style='width:{pct}%'></div></div>"
        f"</div>{inner}</div>")


def _group_by_episode(items: list, episodes: list, missing_by_slug: dict) -> tuple[str, str]:
    """(episode blocks html, standalone cards html) for one section (todo/posted)."""
    ep_of_short = {s.slug: ep for ep in episodes for s in ep.shorts}
    ep_of_long = {ep.long.slug: ep for ep in episodes}
    grouped: dict[str, list] = {}
    standalone = []
    for s in items:
        ep = ep_of_long.get(s.slug) or ep_of_short.get(s.slug)
        if ep:
            grouped.setdefault(ep.slug, []).append((s, missing_by_slug.get(s.slug, [])))
        else:
            standalone.append(s)
    ep_html = "".join(
        episode_block(next(e for e in episodes if e.slug == slug), members)
        for slug, members in grouped.items())
    standalone_html = "".join(card(s, missing_by_slug.get(s.slug, [])) for s in standalone)
    return ep_html, standalone_html


def main() -> int:
    states, _orphans, _pages = release_state.gather()
    episodes = gather_episodes(states)
    queue = release_state.to_post(states)
    q_slugs = {s.slug for s, _ in queue}
    posted = [s for s in states if s.ledger and s.slug not in q_slugs]
    partial = {s.slug: missing for s, missing in queue}

    todo_items = [s for s, _ in queue]
    ep_todo, standalone_todo = _group_by_episode(todo_items, episodes, partial)
    ep_done, standalone_done = _group_by_episode(posted, episodes, partial)
    cards_todo = ep_todo + standalone_todo
    cards_done = ep_done + standalone_done
    canon = "".join(f"<tr><td>{esc(k)}</td><td>{esc(v)}</td></tr>" for k, v in CANON)

    page = f"""<!doctype html><meta charset=utf-8><title>Awakeden upload tracker</title>
<style>body{{font-family:Segoe UI,system-ui,sans-serif;background:#171410;color:#ece5d8;margin:0;padding:24px;max-width:1080px}}
h1{{font-family:Georgia,serif;font-size:22px;margin:0 0 4px}} h2{{font-family:Georgia,serif;font-size:17px;margin:26px 0 8px}}
.sub{{color:#a89e8e;font-size:13px;margin-bottom:6px;line-height:1.5}}
.flow{{background:#211d17;border:1px solid #38322a;border-radius:8px;padding:12px 16px;font-size:13px;line-height:1.7;margin:14px 0}}
.card{{background:#211d17;border:1px solid #38322a;border-radius:8px;padding:12px 16px;margin:12px 0}}
.card h3{{margin:0 0 6px;font-size:15px}} .slug{{color:#a89e8e;font-size:11px;font-weight:400}}
.links{{font-size:12px;margin-bottom:8px;line-height:1.9}} a{{color:#c9a55a}}
.tech{{color:#a89e8e;margin-left:8px}} .ok{{color:#7dbb8b}} .bad{{color:#e08a7a}}
table{{border-collapse:collapse;width:100%;font-size:13px}}
td{{padding:5px 8px;border-bottom:1px solid #2a251d}} tr.done td{{color:#7dbb8b}}
input{{width:100%;box-sizing:border-box;background:#171410;color:#ece5d8;border:1px solid #38322a;border-radius:4px;padding:5px 8px;font-size:12px}}
button{{background:#a8231d;color:#f5f0d0;border:0;border-radius:4px;padding:6px 10px;font-size:12px;font-weight:700;cursor:pointer;white-space:nowrap}}
button.big{{padding:9px 16px;font-size:13px}}
.c{{display:inline-block;font-size:11px;font-weight:700;padding:1px 8px;border-radius:99px}}
.ok.c,.c.ok{{background:#1e3324;color:#7dbb8b}} .c.warn{{background:#37301c;color:#d9a94a}} .c.long{{background:#2a1d2e;color:#c99ad9}}
.canon td:first-child{{color:#a89e8e;width:280px}}
.epblock{{border:1px solid #4a3f2e;border-radius:10px;padding:4px 12px 12px;margin:16px 0;background:#1b1712}}
.epblock-head h3{{margin:10px 0 4px;font-size:16px;font-family:Georgia,serif}}
.epblock .barwrap{{background:#171410;border-radius:99px;height:6px;margin:6px 0 4px;overflow:hidden}}
.epblock .bar.posted{{background:#c9a55a;height:100%}}
.epblock .card{{background:#211d17}}</style>
<h1>Awakeden — upload tracker</h1>
<div class=sub>Truth lives in <code>data/release_ledger.json</code> — this page is a view.
Regenerate: <code>.venv\\Scripts\\python.exe build_upload_tracker.py</code></div>
<div class=flow><b>The loop, per video:</b><br>
1. Open the piece's <b>📦 publish pack</b> — copy buttons for title, description, tags, captions.<br>
2. Upload by hand (video file + the right thumbnail: 16:9 for YouTube longs, 9:16 for Shorts, TikTok cover for TikTok).<br>
3. Paste the published URL into the platform's box below → <b>COPY command</b> → paste + run it in the repo terminal.<br>
&nbsp;&nbsp;&nbsp;That logs the dated URL, and a YouTube URL also updates the website read page automatically.<br>
4. Batch finished → deploy <code>_website</code> → run <code>release_check.py</code> (must be GREEN).</div>
<button class=big onclick="all_cmds(this)">COPY ALL filled boxes as one script</button>
<h2>YouTube settings — same every video</h2>
<div class=card><table class=canon>{canon}</table></div>
<h2>Next up to post ({len(queue)})</h2>
{cards_todo or "<div class=sub>nothing ready and unposted</div>"}
<h2>Posted ({len(posted)})</h2>
{cards_done or "<div class=sub>nothing posted yet</div>"}
<script>
function copy(t, btn) {{
  (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject())
    .catch(() => {{ const a = document.createElement('textarea'); a.value = t;
      document.body.appendChild(a); a.select(); document.execCommand('copy'); a.remove(); }});
  const was = btn.textContent; btn.textContent = 'copied ✓';
  setTimeout(() => btn.textContent = was, 1500);
}}
function cmd(btn, slug, plat) {{
  const inp = document.getElementById('u_' + slug + '_' + plat);
  const url = inp.value.trim();
  if (!url) {{ inp.focus(); inp.placeholder = 'paste the URL first!'; return; }}
  copy('.venv\\\\Scripts\\\\python.exe upload_tracker.py --set ' + slug + ' ' + plat + ' "' + url + '"', btn);
}}
function all_cmds(btn) {{
  const lines = [];
  document.querySelectorAll('input[id^="u_"]').forEach(i => {{
    const url = i.value.trim();
    if (!url) return;
    const parts = i.id.slice(2).split('_');
    const plat = parts.pop(); const slug = parts.join('_');
    lines.push('.venv\\\\Scripts\\\\python.exe upload_tracker.py --set ' + slug + ' ' + plat + ' "' + url + '"');
  }});
  if (lines.length) copy(lines.join('\\r\\n'), btn);
}}
</script>
"""
    OUT.write_text(page, encoding="utf-8")
    print(f"TRACKER -> file:///{str(OUT).replace(chr(92), '/')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
