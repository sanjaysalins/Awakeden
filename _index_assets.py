"""Build the reusable-asset INDEX — one searchable database of every image / clip /
music asset, so the engine (and you) can find and REUSE assets across episodes.

Scans:
  _library/plates/*/    reusable Baroque background plates (image, reusable=True)
  _library/souls/*/     character refs / Soul anchors (image, reusable=True)
  _library/music/*/     reusable music beds (music, reusable=True, by mood)
  (episodes later: visual/hf/*.png + *.mp4 — registered with reusable per the doctrine guard)

Writes:
  _library/index.json   machine-readable list the engine queries before generating
  _library/index.html   human browse page (all asset types, with tags)

Re-run any time; it rebuilds from disk + each asset's <name>.meta.json.
Usage:  python _index_assets.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIB = ROOT / "_library"

# light tag derivation so search works even before hand-tagging
TAG_HINTS = {
    "storm": ["storm", "sea", "waves", "galilee", "night"],
    "calm": ["calm", "sea", "shore", "galilee", "dawn", "peace"],
    "charcoal": ["fire", "coals", "shore", "dawn"],
    "wilderness": ["desert", "wilderness", "rocks", "barren"],
    "jerusalem": ["jerusalem", "street", "stone", "city"],
    "synagogue": ["synagogue", "interior", "columns", "temple"],
    "crowd": ["crowd", "multitude", "people", "hillside"],
    "dawn": ["sky", "dawn", "light", "clouds"],
    "well": ["well", "water", "jar", "samaritan"],
    "olive": ["olive", "grove", "gethsemane", "trees", "dusk"],
    "tomb": ["tomb", "empty", "resurrection", "stone"],
    "lamp": ["lamp", "interior", "night", "room"],
}


def _tags_for(slug: str, subject: str) -> list[str]:
    tags: set[str] = set()
    text = f"{slug} {subject}".lower()
    for key, ts in TAG_HINTS.items():
        if key in text:
            tags.update(ts)
    for w in slug.replace("_", "-").split("-"):
        if len(w) > 2:
            tags.add(w)
    return sorted(tags)


def _scan_dir(subdir: str, atype: str, key: str) -> list[dict]:
    """Scan _library/<subdir>/*/ for an asset PNG/MP4 + its meta.json."""
    out: list[dict] = []
    base = LIB / subdir
    if not base.exists():
        return out
    for d in sorted(p for p in base.iterdir() if p.is_dir()):
        # find the primary media file (png/jpg/mp4), skip helper files
        media = next((f for f in sorted(d.glob("*"))
                      if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".mp4")
                      and not f.name.startswith("_")), None)
        if not media:
            continue
        meta = {}
        mp = d / f"{d.name}.meta.json"
        if mp.exists():
            try:
                meta = json.loads(mp.read_text(encoding="utf-8"))
            except Exception:
                meta = {}
        slug = d.name
        subject = str(meta.get("subject", ""))
        motif = meta.get("motif") or meta.get("mood") or slug
        rec = {
            "id": f"{key}:{slug}",
            "type": atype,                       # image | clip | music
            "subtype": key,                      # plate | soul | music
            "slug": slug,
            "motif": motif,
            "reusable": bool(meta.get("reusable", True)),
            "tags": meta.get("tags") or _tags_for(slug, subject),
            "subject": subject,
            "style": meta.get("style", "baroque-rubens"),
            "path": str(media.relative_to(ROOT)).replace("\\", "/"),
            "episodes_used_in": meta.get("episodes_used_in", []),
        }
        out.append(rec)
    return out


def build_index() -> list[dict]:
    records: list[dict] = []
    records += _scan_dir("plates", "image", "plate")
    records += _scan_dir("souls", "image", "soul")
    records += _scan_dir("music", "music", "music")
    (LIB / "index.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
    return records


def write_browse(records: list[dict]) -> None:
    def card(r):
        thumb = (f'<img src="{Path(r["path"]).relative_to("_library")}" loading=lazy>'
                 if r["type"] != "music" else '<div class=mu>♪ music bed</div>')
        reuse = "♻ reusable" if r["reusable"] else "🔒 episode-only"
        tags = " ".join(f"<i>{t}</i>" for t in r["tags"][:8])
        return (f'<div class=c>{thumb}<div class=l>{r["slug"]} '
                f'<span>[{r["type"]}/{r["subtype"]}]</span></div>'
                f'<div class=r>{reuse} · {r["motif"]}</div><div class=t>{tags}</div></div>')
    by_type: dict[str, list] = {}
    for r in records:
        by_type.setdefault(r["type"], []).append(r)
    sections = ""
    for t in ("image", "clip", "music"):
        rs = by_type.get(t, [])
        if not rs:
            continue
        sections += f"<h2>{t} ({len(rs)})</h2><div class=g>{''.join(card(r) for r in rs)}</div>"
    html = f"""<!doctype html><meta charset=utf-8><title>SLK Asset Library Index</title>
<style>body{{background:#16161a;color:#eee;font:15px system-ui;margin:0;padding:20px}}
h1{{font-size:21px}} h2{{font-size:16px;color:#ffd86c;margin-top:28px;text-transform:capitalize}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px}}
.c{{background:#222;border-radius:8px;overflow:hidden}} .c img{{width:100%;display:block}}
.mu{{padding:40px 10px;text-align:center;color:#9cf;background:#1c2030}}
.l{{padding:7px 10px 1px;font-weight:700}} .l span{{color:#888;font-weight:400;font-size:12px}}
.r{{padding:0 10px;color:#9c9;font-size:12px}} .t{{padding:4px 10px 10px;color:#888;font-size:11px}}
.t i{{font-style:normal;background:#333;border-radius:3px;padding:1px 5px;margin-right:3px;display:inline-block;margin-top:2px}}</style>
<h1>Salt &amp; Light Kingdom — Asset Library Index ({len(records)} assets)</h1>
<p style="color:#aaa">Searchable reuse database. ♻ = reusable across episodes · 🔒 = episode-only
(sacred/specific, doctrine guard). The engine queries <code>index.json</code> before generating new.</p>
{sections}"""
    (LIB / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    recs = build_index()
    write_browse(recs)
    reuse = sum(1 for r in recs if r["reusable"])
    print(f"indexed {len(recs)} assets ({reuse} reusable) -> _library/index.json + index.html")
    for r in recs:
        print(f"  {r['id']:<22} {r['type']:<6} reuse={r['reusable']} tags={r['tags'][:5]}")
