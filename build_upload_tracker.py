#!/usr/bin/env python
"""build_upload_tracker.py — the paste-ready UPLOAD TRACKER page (_UPLOAD_TRACKER.html).

The browser runbook for posting: every ready piece as a card (video file,
publish pack, captions.srt, thumbnails, tech check), one
row per platform. Paste the URL you got after uploading into the row's box and
click COPY — you get the exact `upload_tracker.py --set` command; run it in the
repo terminal. That command is THE one write path: it records the dated ledger
entry (YouTube only) and rebuilds this page.

Durable state lives in data/release_ledger.json — NEVER in this page (the
HF-POC localStorage tracker lost batches; this one is a stateless view that
regenerates from the ledger).

  .venv\\Scripts\\python.exe build_upload_tracker.py
"""
from __future__ import annotations

import html
import re
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from pipeline import release_state  # noqa: E402
from pipeline.episode_state import gather_episodes  # noqa: E402

SWIRLS_DIR = ROOT / "poc_living_water_ink_style_test"
SWIRLS_PLATFORMS = ["youtube"]  # owner rule 2026-11-16: track YouTube only

OUT = ROOT / "_UPLOAD_TRACKER.html"
PLAT_LABEL = {"youtube": "▶ YouTube"}


def hide_btn(key: str) -> str:
    """Hide/unhide toggle for a card that already has a posted link (owner ask
    2026-11-16). Per-viewer view setting only, kept in browser storage; the
    ledger is never touched."""
    return (f"<button class=hide onclick=\"toggleHide('{esc(key)}')\">Hide</button>")

CANON = [
    ("Audience", "NOT made for kids"),
    ("Altered content (a YouTube Studio setting, not text)", "YES"),
    ("Category", "Education"),
    ("License", "Standard YouTube licence"),
    ("Comments", "On — hold potentially inappropriate for review"),
    ("Visibility", "Public"),
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


def thumb_img(thumbs: Path, prefer: str) -> str:
    """Small clickable thumbnail so each card shows at a glance what the video is."""
    for key in (prefer, "9x16", "16x9", "1x1"):
        t = thumbs / f"thumb_{key}.jpg"
        if t.is_file():
            u = "file:///" + str(t).replace(chr(92), "/")
            return f"<a href='{u}'><img class=thumb src='{u}' alt='thumbnail'></a>"
    return ""


def esc(x) -> str:
    return html.escape(str(x), quote=True)


def _load_v5() -> dict:
    """v5 hook/decode-card candidates from poc_comic_page/_audit/fixes (review first; NOT the pinned final)."""
    out = {}
    for f in (ROOT / "poc_comic_page" / "_audit" / "fixes").glob("*.json"):
        try:
            d = json.loads(f.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        o = d.get("output")
        if d.get("verified") and o and Path(o).is_file():
            out[d["id"]] = (Path(o), d)
    return out


V5 = _load_v5()


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
    for key, lbl in (("16x9", "🖼 16:9 (YouTube)"), ("9x16", "🖼 9:16 (Shorts)")):
        t = thumbs / f"thumb_{key}.jpg"
        if t.is_file():
            links.append(flink(t, lbl))

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
    todo = (f"<span class='c warn'>to post on YouTube</span>"
            if missing else "<span class='c ok'>on YouTube</span>")
    posted = bool(s.ledger.get("youtube"))
    return (f"<div class=card id='{esc(s.slug)}'" + (f" data-hide='{esc(s.slug)}'" if posted else "") + ">"
            + (hide_btn(s.slug) if posted else "")
            + thumb_img(thumbs, "16x9" if s.kind == "long" else "9x16") +
            f"<h3>{badge}{esc(s.title)} <span class=slug>{esc(s.slug)}"
            f"{' · ' + esc(s.cluster) if s.cluster else ''}</span> {todo}</h3>"
            f"<div class=links>{' · '.join(links)} {tech}</div>"
            f"<table>{''.join(rows)}</table></div>")


def _load_swirls_tracker():
    """Swirls-of-Life keeps its OWN ledger/posting command (a deliberate 2026-08-25
    choice -- it isn't in _website/manifest.yaml, so it can't share release_state's
    PieceState machinery). This page still shows it alongside the main catalogue
    (one tracker to look at), it just posts through swirls_upload_tracker.py's own
    --set command, not upload_tracker.py's."""
    spec = importlib.util.spec_from_file_location(
        "swirls_upload_tracker", SWIRLS_DIR / "swirls_upload_tracker.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def swirls_card(title: str, slug: str, final: Path | None, ledger_entry: dict) -> tuple[str, list[str]]:
    folder = SWIRLS_DIR / slug
    pub = folder / "publish"

    # Resolve the REAL postable video the same way the publish pack itself does
    # (pipeline.finality's FINAL_VIDEO.txt pin, which prefers the _sfx.mp4 sibling)
    # rather than trusting discover()'s raw MANIFEST `.out` -- that's the pre-SFX
    # file, and this page must never link the wrong one as "the" video.
    ref = ""
    video = final
    try:
        from pipeline import upload_engine
        facts = upload_engine.harvest_facts(str(folder))
        ref = facts.anchor_ref
        if facts.video_path:
            video = Path(facts.video_path)
    except Exception:
        pass

    links = []
    if video and video.is_file():
        links.append(flink(video, "▶ video file"))
    if (pub / "PUBLISH_INDEX.html").is_file():
        links.append(flink(pub / "PUBLISH_INDEX.html", "📦 publish pack (copy buttons)"))
    if (pub / "captions.srt").is_file():
        links.append(flink(pub / "captions.srt", "📝 captions.srt"))
    for key, lbl in (("16x9", "🖼 16:9"), ("9x16", "🖼 9:16 (Shorts)")):
        t = pub / "thumbs" / f"thumb_{key}.jpg"
        if t.is_file():
            links.append(flink(t, lbl))

    missing = [p for p in SWIRLS_PLATFORMS if p not in ledger_entry]
    rows = []
    for plat in SWIRLS_PLATFORMS:
        e = ledger_entry.get(plat)
        if e:
            url, posted = e[0], e[1]
            rows.append(f"<tr class=done><td>{PLAT_LABEL[plat]}</td>"
                        f"<td colspan=2>✅ posted {esc(posted)} — <a href='{esc(url)}'>{esc(url)}</a></td></tr>")
        else:
            iid = f"sw_{slug}_{plat}"
            rows.append(
                f"<tr><td>{PLAT_LABEL[plat]}</td>"
                f"<td><input id='{iid}' placeholder='paste the {esc(plat)} URL after uploading'></td>"
                f"<td><button onclick=\"swirls_cmd(this,'{esc(slug)}','{esc(plat)}')\">COPY command</button></td></tr>")

    todo = (f"<span class='c warn'>to post on YouTube</span>"
            if missing else "<span class='c ok'>on YouTube</span>")
    subref = f" · {esc(ref)}" if ref else ""
    posted = "youtube" in ledger_entry
    card_html = (f"<div class=card id='swirls-{esc(slug)}'"
                 + (f" data-hide='swirls-{esc(slug)}'" if posted else "") + ">"
                 + (hide_btn(f"swirls-{slug}") if posted else "")
                + thumb_img(pub / "thumbs", "9x16") +
                f"<h3><span class='c swirls'>SWIRLS OF LIFE</span> {esc(title)} "
                f"<span class=slug>{esc(slug)}{subref}</span> {todo}</h3>"
                f"<div class=links>{' · '.join(links)}</div>"
                f"<table>{''.join(rows)}</table></div>")
    return card_html, missing


def look(s) -> str:
    """Which visual style a catalogue piece is in (owner ask 2026-11-16: group
    the shorts by style so each group is handled the same way)."""
    v = str(s.video).replace("\\", "/").lower()
    if "poc_living_sketchbook" in v:
        return "Living sketchbook"
    for key, name in (("mary_martha", "Warm storybook"), ("second_fire", "Folk print"),
                      ("bartimaeus", "Desert storybook"), ("zacchaeus", "Scratchy ink"),
                      ("woman_at_well", "Pop halftone")):
        if key in v:
            return name
    return "Graphic comic"


GROUP_HOW = {
    "long": "Normal YouTube video (not a Short). Use the 16:9 thumbnail. Add the captions file.",
    "swirls": "YouTube Short. Use the 9:16 thumbnail. Add the captions file.",
    "comic": "YouTube Short. Use the 9:16 thumbnail. Add the captions file.",
    "other": "YouTube Short. Use the 9:16 thumbnail. Add the captions file. The tag shows the style.",
}


def group_head(title: str, n: int, how: str) -> str:
    return (f"<h3 class=grp>{esc(title)} ({n})</h3>"
            f"<div class=how>{esc(how)}</div>")


def blocked(card_html: str, reason: str) -> str:
    """A finished card that must NOT be posted yet: red reason, no URL box."""
    card_html = re.sub(r"<table>.*?</table>", "", card_html, flags=re.S)
    card_html = card_html.replace("<span class='c warn'>to post on YouTube</span>", "")
    return card_html.replace("</h3>", f" <span class='c bad'>{esc(reason)}</span></h3>", 1)


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
        f"<div class=sub>{ep.shorts_posted} of {ep.shorts_total} shorts on YouTube · long: "
        + (esc("on YouTube") if ep.long_posted else esc("in Next up") if ep.long_ready else esc("not ready yet"))
        + "</div>"
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


SKETCH_DIR = ROOT / "poc_living_sketchbook"
_SKETCH_LONGS = {"seed_of_the_woman", "bronze_serpent_long", "day_of_atonement"}  # already catalogue longs


def _has(folder: Path, *rel: str) -> bool:
    return all((folder / r).is_file() for r in rel)


def _row(name: str, kind: str, video: Path | None, folder: Path, state: str, tone: str) -> str:
    pub = folder / "publish"
    def yn(ok, label, link=None):
        if ok and link:
            return f"<a href='{flink(link, '').split(chr(39))[1]}'>✅ {label}</a>"
        return f"✅ {label}" if ok else f"<span class='bad'>✗ {label}</span>"
    thumbs = pub / "thumbs"
    n_th = len(list(thumbs.glob("thumb_*.jpg"))) if thumbs.is_dir() else 0
    srt = list(pub.glob("captions.srt")) + list(folder.glob("*.srt"))
    return (f"<tr><td><b>{esc(name)}</b><br><span class=slug>{esc(kind)}</span></td>"
            f"<td>{flink(video, '▶ video') if video else '<span class=bad>✗ no final</span>'}</td>"
            f"<td>{yn((pub / 'PUBLISH_INDEX.html').is_file(), 'pack', pub / 'PUBLISH_INDEX.html') if (pub / 'PUBLISH_INDEX.html').is_file() else yn(False, 'pack')}</td>"
            f"<td>{yn(n_th >= 3, f'thumbs ({n_th})')}</td>"
            f"<td>{yn(bool(srt), 'captions')}</td>"
            f"<td><span class='c {tone}'>{esc(state)}</span></td></tr>")


def finished_inventory(states, queue_slugs: set) -> tuple[str, dict]:
    """ONE table of EVERY finished video on disk and its ready state, so nothing
    finished is invisible just because the catalogue hasn't cleared it."""
    rows, counts = [], {"ready": 0, "blocked": 0, "hold": 0}
    # 1. catalogue pieces with a FINAL video that are not in the post queue and not posted
    for st in states:
        if st.video and st.finality.startswith("FINAL") and st.slug not in queue_slugs and not st.ledger:
            has_pack = (st.source_dir / "publish" / "PUBLISH_INDEX.html").is_file()
            state = ("NEEDS CATALOGUE APPROVAL (set studio_complete) — files ready" if has_pack
                     else "NEEDS PUBLISH PACK")
            rows.append(_row(st.title, st.kind, st.video, st.source_dir, state, "warn"))
            counts["blocked"] += 1
    # 2. Swirls of Life: no longer listed here (they are cards above: Next up / blocked / posted)
    # 3. Living-sketchbook ink shorts / longs not in the catalogue
    _pinned = " ".join(
        pf.read_text(encoding="utf-8") for pf in (ROOT / "batches").glob("cluster_*/*/FINAL_VIDEO.txt"))
    for d in sorted(SKETCH_DIR.iterdir()) if SKETCH_DIR.is_dir() else []:
        if not d.is_dir() or d.name in _SKETCH_LONGS or d.name.startswith("_"):
            continue
        _p = _pinned.replace(chr(92), "/")
        if f"poc_living_sketchbook/{d.name}/" in _p or f"/{d.name}_v" in _p:
            continue  # already a catalogue piece (see the post queue above); also v3/v4 rewrites pinned from _rewrite_v*/video/
        cc = sorted(d.glob("*_cc.mp4"))
        if cc:
            rows.append(_row(d.name.replace("_", " ").title(), "ink short", cc[-1], d,
                             "BLOCKED: narration failed doctrine panel (all seats REVISE) - needs rewrite + re-record",
                             "bad"))
            counts["blocked"] += 1
    html_ = ("<table class=inv><tr><th>Piece</th><th>Video</th><th>Pack</th><th>Thumbs</th><th>Captions</th>"
             "<th>State</th></tr>" + "".join(rows) + "</table>")
    return html_, counts


# Posting order from RELEASE_CALENDAR.md (slug -> slot label). Anything not listed
# sorts last. The 5 "spare bank" Psalm-22 shorts are older-identity pieces the
# calendar says to publish only after a style check.
POST_ORDER = [
    ("zechariah-12-10-pierced", "Wk1 Mon - LAUNCH"),
    ("thirty-pieces-of-silver", "Wk1 Wed - LAUNCH"),
    ("ps22-01-crucifixion-foretold", "Wk1 Fri - LAUNCH"),
    ("could-ye-not-watch-one-hour", "Wk2 Mon - LAUNCH"),
    ("father-forgive-them", "Wk2 Wed - LAUNCH"),
    ("today-in-paradise", "Wk2 Fri - LAUNCH"),
    ("woman-behold-thy-son", "Wk3 Mon"),
    ("ps22-03-forsaken-cry", "Wk3 Wed"),
    ("ps22-08-i-thirst", "Wk3 Fri (short slot)"),
    ("it-is-finished", "Wk4 Mon - HERO"),
    ("father-into-thy-hands", "Wk4 Wed"),
    ("isaiah-53-suffering-servant", "Wk4 Fri - LONG"),
    ("sign-of-jonah", "Season 2 opener"),
    ("the-empty-tomb", "Season 2"),
    ("women-first-witnesses", "Season 2"),
    ("seed-of-woman-01-first-gospel-in-the-curse", "Season 3 - Seed of the Woman"),
    ("seed-of-woman-02-her-seed", "Season 3 - Seed of the Woman"),
    ("seed-of-woman-03-heel-vs-head", "Season 3 - Seed of the Woman"),
    ("seed-of-woman-04-serpent-crusher-promised", "Season 3 - Seed of the Woman"),
    ("bronze-serpent-02-the-thing-that-killed-them", "Season 3 - Bronze Serpent"),
    ("bronze-serpent-03-son-of-man-lifted-up", "Season 3 - Bronze Serpent"),
    ("rahab-and-the-scarlet-cord", "Season 3 - Ink shorts (v3)"),
    ("aaron-and-the-two-goats", "Season 3 - Ink shorts (v3)"),
    ("moses-and-the-snake-on-a-pole", "Season 3 - Ink shorts (v3)"),
    ("ps22-02-mockers-words", "Psalm 22 - y7 look OK by owner 2026-11-19"),
    ("ps22-04-declared-to-brethren", "Psalm 22 - style checked 2026-11-19"),
    ("ps22-05-he-hath-done-this", "Psalm 22 - style checked 2026-11-19"),
    ("ps22-06-ends-of-the-earth", "Psalm 22 - style checked 2026-11-19"),
    ("ps22-07-body-foretold", "Psalm 22 - spear fix v3 2026-11-19"),
]
# 30-episode hold LIFTED by the owner 2026-11-16 ("if they are ready, we should
# start looking at posting them already"). Ready Swirls episodes join Next up.
SWIRLS_HOLD = False
# Finished but NOT postable yet (shown in their own small section, never in Next up).
SWIRLS_BLOCKED = {"swirls_episode_12_ye_are_not_all_clean": "BLOCKED: 'cuts off' playback bug still open"}


def main() -> int:
    states, _orphans, _pages = release_state.gather()
    episodes = gather_episodes(states)
    queue = release_state.to_post(states)
    q_slugs = {s.slug for s, _ in queue}
    posted = [s for s in states if s.ledger and s.slug not in q_slugs]
    partial = {s.slug: missing for s, missing in queue}

    todo_items = [s for s, _ in queue]
    # TO-POST list: flat, in calendar order, numbered (not grouped by episode).
    rank = {slug: i for i, (slug, _l) in enumerate(POST_ORDER)}
    label = dict(POST_ORDER)
    todo_sorted = sorted(todo_items, key=lambda x: rank.get(x.slug, 999))
    check_first = [x for x in todo_sorted if label.get(x.slug, "").startswith("SPARE BANK")]
    todo_sorted = [x for x in todo_sorted if x not in check_first]
    # Next up, split: long films / shorts by style (owner ask 2026-11-16).
    groups = {"long": [], "comic": [], "other": [], "swirls": []}
    for x in todo_sorted:
        if x.kind == "long":
            groups["long"].append(("", card(x, partial.get(x.slug, [])).replace(
            "</h3>", f" <span class='c style'>{esc(look(x))}</span></h3>", 1)))
        else:
            st = look(x)
            c = card(x, partial.get(x.slug, []))
            if st != "Graphic comic":
                c = c.replace("</h3>", f" <span class='c style'>{esc(st)}</span></h3>", 1)
            groups["comic" if st == "Graphic comic" else "other"].append((st, c))
    ep_todo = standalone_todo = ""
    _e, _s = _group_by_episode([], episodes, partial)
    ep_done, standalone_done = _group_by_episode(posted, episodes, partial)
    cards_todo = ep_todo + standalone_todo
    cards_done = ep_done + standalone_done

    # Swirls-of-Life: same page, its own section-agnostic cards (separate ledger,
    # separate --set command — see _load_swirls_tracker's own docstring for why).
    swirls_mod = _load_swirls_tracker()
    swirls_ledger = swirls_mod.load_ledger()
    swirls_entries = ([(t, s, SWIRLS_DIR / s / f) for t, s, f in swirls_mod.LEGACY]
                      + swirls_mod.discover())
    n_swirls_todo = n_swirls_done = 0
    cards_held = "".join(blocked(card(x, partial.get(x.slug, [])), "Check the style first (older look)")
                         for x in check_first)
    n_swirls_held = len(check_first)
    _seen_sw = set()
    for title, slug, final in swirls_entries:
        if slug in _seen_sw:
            continue
        _seen_sw.add(slug)
        card_html, missing = swirls_card(title, slug, final, swirls_ledger.get(slug, {}))
        if slug in SWIRLS_BLOCKED:
            cards_held += blocked(card_html, SWIRLS_BLOCKED[slug])
            n_swirls_held += 1
        elif not missing:
            cards_done += card_html          # fully posted -> Posted, hold or not
            n_swirls_done += 1
        elif SWIRLS_HOLD:
            cards_held += card_html          # 30-ep hold: tracked, URL boxes live, not in Next up
            n_swirls_held += 1
        else:
            groups["swirls"].append(("", card_html))
            n_swirls_todo += 1

    def numbered(cards: list) -> str:
        # keep each style together (stable sort keeps calendar order inside a style)
        cards = sorted(cards, key=lambda t: t[0])
        return "".join(f"<div class=sub><b>#{i}</b></div>{c}" for i, (_st, c) in enumerate(cards, 1))
    cards_todo = (
        f"<h2>Long films ({len(groups['long'])})</h2><div class=how>{esc(GROUP_HOW['long'])}</div>"
        + (numbered(groups["long"]) or "<div class=sub>none</div>")
        + f"<h2>Shorts ({len(groups['swirls']) + len(groups['comic']) + len(groups['other'])})</h2>"
        + group_head("Swirls of Life", len(groups["swirls"]), GROUP_HOW["swirls"]) + (numbered(groups["swirls"]) or "<div class=sub>none</div>")
        + group_head("Graphic comic", len(groups["comic"]), GROUP_HOW["comic"]) + (numbered(groups["comic"]) or "<div class=sub>none</div>")
        + group_head("Other styles", len(groups["other"]), GROUP_HOW["other"]) + (numbered(groups["other"]) or "<div class=sub>none</div>"))
    inv_html, inv_counts = finished_inventory(states, q_slugs)
    n_queue, n_posted = len(todo_sorted) + n_swirls_todo, len(posted) + n_swirls_done
    n_inv = inv_counts["blocked"] + inv_counts["hold"]
    inv_block = (f"<h2>Other finished videos, not ready ({n_inv})</h2>"
                 "<div class=sub>Finished on disk but not in the lists above. Red ✗ = what is missing.</div>"
                 + inv_html) if n_inv else ""
    canon = "".join(f"<tr><td>{esc(k)}</td><td>{esc(v)}</td></tr>" for k, v in CANON)

    page = f"""<!doctype html><meta charset=utf-8><title>YouTube upload tracker</title>
<style>body{{font-family:Segoe UI,system-ui,sans-serif;background:#171410;color:#ece5d8;margin:0;padding:24px;max-width:1080px}}
h1{{font-family:Georgia,serif;font-size:22px;margin:0 0 4px}} h2{{font-family:Georgia,serif;font-size:17px;margin:26px 0 8px}}
.sub{{color:#a89e8e;font-size:13px;margin-bottom:6px;line-height:1.5}}
.flow{{background:#211d17;border:1px solid #38322a;border-radius:8px;padding:12px 16px;font-size:13px;line-height:1.7;margin:14px 0}}
.card{{background:#211d17;border:1px solid #38322a;border-radius:8px;padding:12px 16px;margin:12px 0}}
.card{{overflow:hidden}} .thumb{{float:left;height:150px;max-width:150px;object-fit:cover;border-radius:6px;margin:0 14px 6px 0;border:1px solid #38322a}}
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
.c.swirls{{background:#1c2e3a;color:#7ab8d9}} .c.style{{background:#2a2a1a;color:#e0d27a}}
h3.grp{{font-family:Georgia,serif;font-size:19px;margin:22px 0 2px;color:#e8c27a}} .how{{font-size:15px;color:#ece5d8;background:#2a241b;border-left:4px solid #c9a55a;padding:6px 10px;margin:4px 0 10px}}
h1.big2{{font-size:24px;margin:30px 0 4px}} .c.bad{{background:#3a1c1c;color:#e08a7a}}
button.hide{{float:right;background:#38322a;color:#ece5d8;margin-left:8px}}
.card.hidden{{display:none}} body.showhid .card.hidden{{display:block;opacity:.45}}
.canon td:first-child{{color:#a89e8e;width:280px}}
.epblock{{border:1px solid #4a3f2e;border-radius:10px;padding:4px 12px 12px;margin:16px 0;background:#1b1712}}
.epblock-head h3{{margin:10px 0 4px;font-size:16px;font-family:Georgia,serif}}
.epblock .barwrap{{background:#171410;border-radius:99px;height:6px;margin:6px 0 4px;overflow:hidden}}
.epblock .bar.posted{{background:#c9a55a;height:100%}}
.epblock .card{{background:#211d17}}
.inv th{{text-align:left;color:#b59e86;font-size:12px}} .inv .bad{{color:#e0675d}} .inv a{{color:#c9a55a}}</style>
<h1>YouTube upload tracker</h1>
<div class=sub>YouTube links only. Every upload-ready piece, longs and shorts, in one place — the main catalogue
(<code>data/release_ledger.json</code>) AND <span class='c swirls'>SWIRLS OF LIFE</span>
(its own <code>poc_living_water_ink_style_test/_swirls_release_ledger.json</code> — a
separate ledger and COPY command, since it isn't part of the site catalogue). This page
is a view; regenerate: <code>.venv\\Scripts\\python.exe build_upload_tracker.py</code></div>
<div class=flow><b>The loop, per video:</b><br>
1. Open the piece's <b>📦 publish pack</b> — copy buttons for title, description, tags, captions.<br>
2. Upload to YouTube by hand (video file + thumbnail: 16:9 for longs, 9:16 for Shorts).<br>
3. Paste the YouTube URL into the box below → <b>COPY command</b> → paste + run it in the repo terminal.<br>
4. Run <code>release_check.py</code> (must be GREEN).<br>
<b>Hide</b> on a posted card tucks it away. <b>Show hidden</b> brings them back.</div>
<button class=big onclick="all_cmds(this)">COPY ALL filled boxes as one script</button>
<h2>YouTube settings — same every video</h2>
<div class=card><table class=canon>{canon}</table></div>
<h1 class=big2>Ready to post ({n_queue})</h1>
<div class=sub>Not on YouTube yet, all ready. Split into long films and shorts, and the shorts by style. Post from the top of each group.</div>
{cards_todo}
<h2>Finished but not ready ({n_swirls_held})</h2>
<div class=sub>Do not post these yet. The red note says why.</div>
{cards_held or "<div class=sub>none</div>"}
{inv_block}
<h2>Posted ({n_posted}) <button id=showhid onclick="toggleShow()">Show hidden</button></h2>
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
function swirls_cmd(btn, slug, plat) {{
  const inp = document.getElementById('sw_' + slug + '_' + plat);
  const url = inp.value.trim();
  if (!url) {{ inp.focus(); inp.placeholder = 'paste the URL first!'; return; }}
  copy('.venv\\\\Scripts\\\\python.exe poc_living_water_ink_style_test\\\\swirls_upload_tracker.py --set '
       + slug + ' ' + plat + ' "' + url + '"', btn);
}}
let HID = [];
try {{ HID = JSON.parse(localStorage.getItem('yt_tracker_hidden') || '[]'); }} catch (e) {{ HID = []; }}
function saveHid() {{ try {{ localStorage.setItem('yt_tracker_hidden', JSON.stringify(HID)); }} catch (e) {{}} }}
function paint() {{
  let n = 0;
  document.querySelectorAll('.card[data-hide]').forEach(c => {{
    const h = HID.includes(c.dataset.hide); if (h) n++;
    c.classList.toggle('hidden', h);
    const b = c.querySelector('button.hide'); if (b) b.textContent = h ? 'Unhide' : 'Hide';
  }});
  const s = document.getElementById('showhid');
  if (s) s.textContent = (document.body.classList.contains('showhid') ? 'Hide hidden' : 'Show hidden') + ' (' + n + ')';
}}
function toggleHide(k) {{ HID = HID.includes(k) ? HID.filter(x => x !== k) : HID.concat([k]); saveHid(); paint(); }}
function toggleShow() {{ document.body.classList.toggle('showhid'); paint(); }}
paint();
function all_cmds(btn) {{
  const lines = [];
  document.querySelectorAll('input[id^="u_"]').forEach(i => {{
    const url = i.value.trim();
    if (!url) return;
    const parts = i.id.slice(2).split('_');
    const plat = parts.pop(); const slug = parts.join('_');
    lines.push('.venv\\\\Scripts\\\\python.exe upload_tracker.py --set ' + slug + ' ' + plat + ' "' + url + '"');
  }});
  document.querySelectorAll('input[id^="sw_"]').forEach(i => {{
    const url = i.value.trim();
    if (!url) return;
    const parts = i.id.slice(3).split('_');
    const plat = parts.pop(); const slug = parts.join('_');
    lines.push('.venv\\\\Scripts\\\\python.exe poc_living_water_ink_style_test\\\\swirls_upload_tracker.py --set '
               + slug + ' ' + plat + ' "' + url + '"');
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
