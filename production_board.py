#!/usr/bin/env python
"""production_board.py — ONE board that validates every piece from start to publish.

Renders the SAME per-piece state as release_check.py (pipeline/release_state.py):
the catalogue (`_website/manifest.yaml`, HARD-joined via source:/read_source:/
study_source: — the fuzzy matcher is dead), the pipeline lane
(cli_livingpage.detect), the policy final (pipeline/finality.py, sha-anchored),
the publish pack + thumbnails freshness, the site read page, and the dated
per-platform posting ledger (data/release_ledger.json).

Clusters group with their LONG first and its shorts nested (parent: linkage).

CAPTION POLICY (user, 2026-07-08): living-page pieces carry their text as COMIC
BOXES baked into the build — the postable final is `<piece>_sfx.mp4`. Legacy
narration-only pieces keep their captioned finals.

  .venv\\Scripts\\python.exe production_board.py            # console + _PRODUCTION_BOARD.html
"""
from __future__ import annotations

import html
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import cli_livingpage  # noqa: E402
from pipeline import release_state  # noqa: E402
from pipeline.episode_state import gather_episodes  # noqa: E402

OUT_HTML = ROOT / "_PRODUCTION_BOARD.html"
PLAT_ABBR = {"youtube": "YT", "tiktok": "TT", "facebook": "FB", "instagram": "IG"}


def lane_state(s: release_state.PieceState) -> str:
    if not s.source_dir:
        return "-"
    if not (s.source_dir / "piece.json").is_file():
        return "legacy lane" if s.finality.startswith("FINAL") else "-"
    steps = cli_livingpage.detect(s.source_dir)
    open_steps = [x.name for x in steps if not x.done]
    return "COMPLETE" if not open_steps else f"next: {open_steps[0]}"


def main() -> int:
    states, orphans, orphan_pages = release_state.gather()
    findings = release_state.run_gates(states, orphans, orphan_pages)
    by_slug: dict[str, list] = {}
    for gate, lvl, slug, msg in findings:
        by_slug.setdefault(slug, []).append((gate, lvl, msg))
    queue = release_state.to_post(states)
    episodes = gather_episodes(states)

    rows = []
    for s in states:
        lane = lane_state(s)
        ready = s.finality.startswith("FINAL") and (lane in ("COMPLETE", "legacy lane", "-"))
        rows.append((s, lane, ready))

    n_ready = sum(r for _, _, r in rows)
    n_pack = sum(1 for s, _, _ in rows if s.pack_fresh)
    n_page = sum(1 for s, _, _ in rows if s.read_page)
    n_pub = sum(1 for s, _, _ in rows if s.youtube_id)

    # ---- console ----
    print(f"{'slug':34} {'status':16} {'pipeline':20} {'video':20} pack page yt")
    for s, lane, _ in rows:
        pk = "OK" if s.pack_fresh else ("st" if s.pack_exists else "-")
        print(f"{s.slug[:34]:34} {s.status[:16]:16} {lane[:20]:20} {s.finality[:20]:20} "
              f"{pk:4} {'Y' if s.read_page else '-'}    {'Y' if s.youtube_id else '-'}")
    n_fail = len([f for f in findings if f[1] == 'FAIL'])
    print(f"\n{len(rows)} catalogue items · {n_ready} production-ready · {n_pack} packs fresh · "
          f"{n_page} read pages · {n_pub} published · {n_fail} SYNC FAILs "
          f"(detail: .venv\\Scripts\\python.exe release_check.py)")
    if episodes:
        print(f"\n{len(episodes)} episode(s):")
        for ep in episodes:
            print(f"  {ep.title[:40]:40} {ep.status}")
    if orphans:
        print(f"! lane pieces NOT in the site manifest: {orphans}")

    # ---- html ----
    def chip(txt, cls):
        return f"<span class='c {cls}'>{html.escape(str(txt))}</span>"

    def freshness(exists: bool, sha_ok: bool, none_txt: str, stale_txt: str, ok_txt: str):
        if not exists:
            return chip(none_txt, "mut")
        return chip(ok_txt, "ok") if sha_ok else chip(stale_txt, "warn")

    def sort_key(row):
        s = row[0]
        group = s.cluster or (s.parent or "~zz-" + s.slug)
        return (group, s.kind != "long", s.cluster_order if s.cluster_order is not None else 99, s.slug)

    trs = []
    for s, lane, _ in sorted(rows, key=sort_key):
        probs = by_slug.get(s.slug, [])
        vlink = (f"<a href='file:///{str(s.video).replace(chr(92), '/')}'>video</a>" if s.video else "")
        plink = (f"<a href='_website/read/{s.slug}.html'>read page</a>" if s.read_page
                 else chip("no page", "mut"))
        plats = []
        for p in s.post_platforms:
            e = s.ledger.get(p)
            plats.append(chip(f"{PLAT_ABBR[p]} {e['posted']}", "ok") if e else chip(PLAT_ABBR[p], "mut"))
        prob_html = "".join(f"<div class='prob {lvl.lower()}'>{html.escape(gate)}: {html.escape(msg)}</div>"
                            for gate, lvl, msg in probs)
        indent = "&nbsp;&nbsp;&nbsp;&nbsp;↳ " if s.parent else ""
        kind_badge = chip("LONG", "long") if s.kind == "long" else ""
        trs.append(
            f"<tr id='row-{html.escape(s.slug)}'>"
            f"<td>{indent}{html.escape(s.title)} {kind_badge}"
            f"<div class=slug>{s.slug} · {s.cluster or '-'}</div>{prob_html}</td>"
            f"<td>{chip(s.status, 'ok' if s.status in ('studio_complete', 'live') else 'warn' if s.status == 'in_production' else 'mut')}</td>"
            f"<td>{chip(lane, 'ok' if lane in ('COMPLETE', 'legacy lane') else 'warn' if lane != '-' else 'mut')}</td>"
            f"<td>{chip(s.finality, 'ok' if s.finality.startswith('FINAL') else 'warn' if s.finality != 'no video' else 'mut')} {vlink}</td>"
            f"<td>{freshness(s.pack_exists, s.pack_fresh, 'no pack', 'STALE', 'fresh')}</td>"
            f"<td>{freshness(s.thumbs_exist, s.thumbs_fresh, 'none', 'stale', 'fresh')}</td>"
            f"<td>{plink}</td>"
            f"<td>{' '.join(plats)}</td>"
            "</tr>")

    ep_html = ""
    if episodes:
        cards = []
        for ep in episodes:
            idx = (ep.long.source_dir / "publish" / "PUBLISH_INDEX.html") if ep.long.source_dir else None
            long_link = (f"<a href='file:///{str(idx).replace(chr(92), chr(47))}'>publish pack</a>"
                        if idx and idx.is_file() else "")
            pct_built = int(100 * ep.shorts_built / ep.shorts_total) if ep.shorts_total else 0
            # posted-any (not fully-posted) drives the bar so real progress
            # (e.g. live on YouTube, TikTok/FB/IG still in the 24-48h cross-post
            # window) doesn't sit stuck at 0% — red-team 2026-07-15
            pct_posted = int(100 * ep.shorts_posted_any / ep.shorts_total) if ep.shorts_total else 0
            short_chips = "".join(
                f"<a class='c {'ok' if s.finality.startswith('FINAL') else 'warn' if s.finality != 'no video' else 'mut'}' "
                f"href='#row-{html.escape(s.slug)}'>{'?' if s.cluster_order is None else s.cluster_order}</a>"
                for s in ep.shorts)
            status_cls = "ok" if ep.is_complete else "warn" if ep.shorts_total else "mut"
            cards.append(
                "<div class=epcard>"
                f"<h3><a href='#row-{html.escape(ep.slug)}'>{html.escape(ep.title)}</a> {chip(ep.status, status_cls)}</h3>"
                f"<div class=sub>{ep.shorts_total} planned shorts"
                f"{' · ' + long_link if long_link else ''}</div>"
                f"<div class=barwrap><div class=bar style='width:{pct_built}%'></div></div>"
                f"<div class=barlabel>{ep.shorts_built}/{ep.shorts_total} built</div>"
                f"<div class=barwrap><div class='bar posted' style='width:{pct_posted}%'></div></div>"
                f"<div class=barlabel>{ep.shorts_posted}/{ep.shorts_total} fully posted"
                f" ({ep.shorts_posted_any}/{ep.shorts_total} posted somewhere)"
                f"{' · long ' + ('posted' if ep.long_posted else 'not posted') if ep.shorts_total else ''}</div>"
                f"<div class=epshorts>{short_chips}</div>"
                "</div>")
        ep_html = f"<h2>Episodes — long + shorts, one unit of work ({len(episodes)})</h2><div class=epgrid>{''.join(cards)}</div>"

    q_html = ""
    if queue:
        lis = []
        for s, missing in queue:
            idx = (s.source_dir / "publish" / "PUBLISH_INDEX.html") if s.source_dir else None
            link = (f" — <a href='file:///{str(idx).replace(chr(92), '/')}'>publish pack</a>"
                    if idx and idx.is_file() else "")
            lis.append(f"<li><b>{html.escape(s.title)}</b> <span class=slug>{s.slug}</span> "
                       f"→ {', '.join(missing)}{link}</li>")
        q_html = f"<h2>Next up to post ({len(queue)})</h2><ul class=queue>{''.join(lis)}</ul>"

    page = f"""<!doctype html><meta charset=utf-8><title>Awakeden production board</title>
<style>body{{font-family:Segoe UI,system-ui,sans-serif;background:#171410;color:#ece5d8;margin:0;padding:24px}}
h1{{font-family:Georgia,serif;font-size:22px;margin:0 0 4px}} h2{{font-family:Georgia,serif;font-size:17px;margin:22px 0 8px}}
.sub{{color:#a89e8e;font-size:13px;margin-bottom:16px}}
.tiles{{display:flex;gap:10px;margin-bottom:18px;flex-wrap:wrap}}
.tile{{background:#211d17;border:1px solid #38322a;padding:10px 16px;border-radius:6px}}
.tile b{{font-family:Georgia,serif;font-size:22px;display:block}}
table{{border-collapse:collapse;width:100%;font-size:13px;background:#211d17}}
th{{text-align:left;padding:8px;border-bottom:2px solid #38322a;color:#a89e8e;font-size:11px;text-transform:uppercase;letter-spacing:.06em}}
td{{padding:8px;border-bottom:1px solid #2a251d;vertical-align:top}}
.slug{{color:#a89e8e;font-size:11px}} a{{color:#c9a55a}}
.c{{display:inline-block;font-size:11px;font-weight:700;padding:1px 8px;border-radius:99px}}
.ok{{background:#1e3324;color:#7dbb8b}} .warn{{background:#37301c;color:#d9a94a}} .mut{{background:#2a251d;color:#a89e8e}}
.long{{background:#2a1d2e;color:#c99ad9}}
.prob{{font-size:11px;margin-top:3px;padding:2px 6px;border-radius:4px}}
.prob.fail{{background:#3a1d1a;color:#e08a7a}} .prob.warn{{background:#37301c;color:#d9a94a}}
.queue li{{margin:4px 0}}
.epgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;margin-bottom:8px}}
.epcard{{background:#211d17;border:1px solid #38322a;border-radius:8px;padding:12px 14px}}
.epcard h3{{margin:0 0 4px;font-size:15px;font-family:Georgia,serif}} .epcard h3 a{{color:#f3ece4}}
.barwrap{{background:#171410;border-radius:99px;height:7px;margin:8px 0 2px;overflow:hidden}}
.bar{{background:#7dbb8b;height:100%}} .bar.posted{{background:#c9a55a}}
.barlabel{{font-size:11px;color:#a89e8e;margin-bottom:6px}}
.epshorts{{display:flex;gap:4px;flex-wrap:wrap;margin-top:4px}}
.epshorts a{{text-decoration:none;min-width:18px;text-align:center}}</style>
<h1>Awakeden — production board</h1>
<div class=sub>manifest × pipeline × finality(sha) × pack × thumbs × site × posted-ledger ·
regenerate: <code>.venv\\Scripts\\python.exe production_board.py</code> ·
gate: <code>release_check.py</code> ·
<a href='_UPLOAD_TRACKER.html'>UPLOAD TRACKER (paste URLs here)</a></div>
<div class=tiles>
<div class=tile><b>{len(rows)}</b>catalogue items</div>
<div class=tile><b>{n_ready}</b>production-ready</div>
<div class=tile><b>{n_pack}</b>packs fresh</div>
<div class=tile><b>{n_page}</b>site read pages</div>
<div class=tile><b>{n_pub}</b>published</div>
<div class=tile><b>{len(queue)}</b>to post</div>
<div class=tile><b>{len(episodes)}</b>episodes</div>
</div>
{ep_html}
{q_html}
<h2>All pieces</h2>
<table><tr><th>Piece</th><th>Catalogue</th><th>Pipeline</th><th>Video (policy final)</th>
<th>Publish pack</th><th>Thumbs</th><th>Website</th><th>Posted</th></tr>
{''.join(trs)}</table>
{('<p class=sub>Lane pieces missing from the site manifest: ' + ', '.join(orphans) + '</p>') if orphans else ''}
"""
    OUT_HTML.write_text(page, encoding="utf-8")
    print(f"\nBOARD -> file:///{str(OUT_HTML).replace(chr(92), '/')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
