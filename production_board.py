#!/usr/bin/env python
"""production_board.py — ONE board that validates every piece from start to publish.

Joins the three sources of truth:
  1. `_website/manifest.yaml` — the planned catalogue (slug, title, cluster, public_status,
     youtube_id = actually published)
  2. The pipeline lane state — `cli_livingpage.detect()` for batches pieces (narration →
     voice → spec → manifest → stills → gate → animate → build → score → register)
  3. The finishing/publishing state — SFX bed, read page on the site, publish pack,
     youtube_id

CAPTION POLICY (user, 2026-07-08): living-page pieces carry their text as COMIC BOXES
baked into the build — the postable final is `<piece>_sfx.mp4` (NO ivory caption layer;
double text is clutter). Legacy narration-only pieces (Psalm-22 shorts, 16:9 longs)
keep their captioned finals.

  .venv\\Scripts\\python.exe production_board.py            # console + _PRODUCTION_BOARD.html
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import cli_livingpage  # noqa: E402

SITE = ROOT / "_website"
OUT_HTML = ROOT / "_PRODUCTION_BOARD.html"


def _norm_tokens(s: str) -> set[str]:
    stop = {"the", "of", "a", "in", "from", "thy", "ye", "not"}
    return {w for w in re.findall(r"[a-z0-9]+", (s or "").lower()) if w not in stop and len(w) > 2}


def load_manifest() -> list[dict]:
    m = yaml.safe_load((SITE / "manifest.yaml").read_text(encoding="utf-8"))
    return m["items"]


def lane_pieces() -> dict[str, Path]:
    return {p.parent.name: p.parent for p in (ROOT / "batches").glob("*/*/piece.json")}


def final_video(piece_dir: Path, pj_title: str = "") -> tuple[str, Path | None]:
    """(finality, path) for a lane piece under the caption policy: sfx > scored."""
    v = piece_dir / "visual"
    cands = list(v.glob("*_sfx.mp4")) + list(v.glob("_byteplus/*_scored.mp4")) + list(v.glob("*_scored.mp4"))
    sfx = [c for c in cands if c.name.endswith("_sfx.mp4")]
    if sfx:
        return "FINAL (sfx)", sfx[0]
    scored = [c for c in cands if c.name.endswith("_scored.mp4")]
    if scored:
        return "scored (needs SFX)", scored[0]
    return "no video", None


def _letters(s: str) -> str:
    return re.sub(r"[^a-z]", "", (s or "").lower())


def match_manifest(item_title: str, item_slug: str, pieces: dict[str, Path]) -> str | None:
    """Best lane piece for a manifest item: letters-only containment (handles short
    titles + the ps22-NN- prefixes) with token overlap as the tie-breaker."""
    # NOTE: do NOT strip "ew" - the eyewitness lane lives in longform/, never in
    # batches/, and stripping it made ew-jonah letter-match sign_of_jonah's piece
    # (the board then showed a FINAL for a piece with no video at all, 2026-07-15)
    slug_l = _letters(item_slug.replace("ps22", ""))
    title_l = _letters(item_title)
    want = _norm_tokens(item_title) | _norm_tokens(item_slug.replace("-", " "))
    best, score = None, 0
    for name, d in pieces.items():
        folder_l = _letters(re.sub(r"_[a-z]*\d+[a-z]*$", "", name))  # strip verse suffix
        contained = (slug_l and (slug_l in folder_l or folder_l in slug_l)) or \
                    (title_l and (title_l in folder_l or folder_l in title_l))
        have = _norm_tokens(name.replace("_", " "))
        meta = d / "publish_meta.json"
        if meta.is_file():
            try:
                have |= _norm_tokens(json.loads(meta.read_text(encoding="utf-8")).get("title", ""))
            except Exception:
                pass
        s = len(want & have) + (10 if contained else 0)
        if s > score:
            best, score = name, s
    return best if score >= 2 else None


def main() -> int:
    items = load_manifest()
    pieces = lane_pieces()
    read_pages = {p.stem for p in (SITE / "read").glob("*.html")} - {"index"}
    matched: set[str] = set()
    rows = []

    for it in items:
        slug, title = it.get("slug", ""), it.get("title", "")
        cluster = it.get("cluster") or "-"
        status = it.get("public_status", "?")
        yt = bool(it.get("youtube_id"))
        page = slug in read_pages
        piece_name = match_manifest(title, slug, pieces)
        lane = video = ""
        vpath = None
        ready = False
        if piece_name:
            matched.add(piece_name)
            d = pieces[piece_name]
            steps = cli_livingpage.detect(d)
            open_steps = [s.name for s in steps if not s.done]
            lane = "COMPLETE" if not open_steps else f"next: {open_steps[0]}"
            video, vpath = final_video(d)
            ready = (not open_steps) and video.startswith("FINAL")
        else:
            # legacy / long-form: is there a finished final anywhere obvious?
            hints = [ROOT / "longform", ROOT / "v2" / "pilot"]
            pats = ["*captioned.mp4", "*_sfx.mp4", "*_scored.mp4"]
            hit = None
            want = _norm_tokens(title) | _norm_tokens(slug.replace("-", " "))
            for base in hints:
                for pat in pats:
                    for f in base.rglob(pat):
                        if len(want & _norm_tokens(str(f.relative_to(base)).replace("_", " ").replace("\\", " "))) >= 2:
                            hit = f
                            break
                    if hit:
                        break
                if hit:
                    break
            if hit:
                video, vpath, lane = "FINAL (legacy)", hit, "legacy lane"
                ready = True
            else:
                video, lane = "not built", "-"
        rows.append(dict(slug=slug, title=title, cluster=cluster, status=status,
                         lane=lane, video=video, vpath=vpath, page=page, yt=yt, ready=ready))

    orphans = sorted(set(pieces) - matched)
    n_ready = sum(r["ready"] for r in rows)
    n_pub = sum(r["yt"] for r in rows)
    n_page = sum(r["page"] for r in rows)

    # ---- console ----
    print(f"{'slug':34} {'status':16} {'pipeline':22} {'video':20} page yt")
    for r in rows:
        print(f"{r['slug'][:34]:34} {r['status'][:16]:16} {r['lane'][:22]:22} "
              f"{r['video'][:20]:20} {'Y' if r['page'] else '-'}    {'Y' if r['yt'] else '-'}")
    print(f"\n{len(rows)} catalogue items · {n_ready} production-ready · {n_page} read pages · "
          f"{n_pub} published (youtube_id)")
    if orphans:
        print(f"! lane pieces NOT in the site manifest: {orphans}")

    # ---- html ----
    def chip(txt, cls):
        return f"<span class='c {cls}'>{html.escape(str(txt))}</span>"

    trs = []
    for r in sorted(rows, key=lambda x: (x["cluster"], x["slug"])):
        vlink = (f"<a href='file:///{str(r['vpath']).replace(chr(92), '/')}'>video</a>"
                 if r["vpath"] else "")
        plink = (f"<a href='read/{r['slug']}.html'>read page</a>" if r["page"] else chip("no page", "warn"))
        trs.append(
            "<tr>"
            f"<td>{html.escape(r['title'])}<div class=slug>{r['slug']} · {r['cluster']}</div></td>"
            f"<td>{chip(r['status'], 'ok' if r['status'] == 'studio_complete' else 'warn' if r['status'] == 'in_production' else 'mut')}</td>"
            f"<td>{chip(r['lane'], 'ok' if r['lane'] in ('COMPLETE', 'legacy lane') else 'warn' if r['lane'] != '-' else 'mut')}</td>"
            f"<td>{chip(r['video'], 'ok' if r['video'].startswith('FINAL') else 'warn' if r['video'] != 'not built' else 'mut')} {vlink}</td>"
            f"<td>{plink}</td>"
            f"<td>{chip('PUBLISHED', 'ok') if r['yt'] else chip('not yet', 'mut')}</td>"
            "</tr>")
    page = f"""<!doctype html><meta charset=utf-8><title>Awakeden production board</title>
<style>body{{font-family:Segoe UI,system-ui,sans-serif;background:#171410;color:#ece5d8;margin:0;padding:24px}}
h1{{font-family:Georgia,serif;font-size:22px;margin:0 0 4px}} .sub{{color:#a89e8e;font-size:13px;margin-bottom:16px}}
.tiles{{display:flex;gap:10px;margin-bottom:18px;flex-wrap:wrap}}
.tile{{background:#211d17;border:1px solid #38322a;padding:10px 16px;border-radius:6px}}
.tile b{{font-family:Georgia,serif;font-size:22px;display:block}}
table{{border-collapse:collapse;width:100%;font-size:13px;background:#211d17}}
th{{text-align:left;padding:8px;border-bottom:2px solid #38322a;color:#a89e8e;font-size:11px;text-transform:uppercase;letter-spacing:.06em}}
td{{padding:8px;border-bottom:1px solid #2a251d;vertical-align:top}}
.slug{{color:#a89e8e;font-size:11px}} a{{color:#c9a55a}}
.c{{display:inline-block;font-size:11px;font-weight:700;padding:1px 8px;border-radius:99px}}
.ok{{background:#1e3324;color:#7dbb8b}} .warn{{background:#37301c;color:#d9a94a}} .mut{{background:#2a251d;color:#a89e8e}}</style>
<h1>Awakeden — production board</h1>
<div class=sub>manifest × pipeline × finishing × site × published · regenerate:
<code>.venv\\Scripts\\python.exe production_board.py</code></div>
<div class=tiles>
<div class=tile><b>{len(rows)}</b>catalogue items</div>
<div class=tile><b>{n_ready}</b>production-ready</div>
<div class=tile><b>{n_page}</b>site read pages</div>
<div class=tile><b>{n_pub}</b>published</div>
</div>
<table><tr><th>Piece</th><th>Catalogue status</th><th>Pipeline</th><th>Video (policy final)</th><th>Website</th><th>Published</th></tr>
{''.join(trs)}</table>
{('<p class=sub>Lane pieces missing from the site manifest: ' + ', '.join(orphans) + '</p>') if orphans else ''}
"""
    OUT_HTML.write_text(page, encoding="utf-8")
    print(f"\nBOARD -> file:///{str(OUT_HTML).replace(chr(92), '/')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
