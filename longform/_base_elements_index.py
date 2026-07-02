#!/usr/bin/env python
"""Base-elements master index builder.

Step 1 of the base-elements library: merge the per-batch element extractions
(scratchpad/extract_*.json, authored by the in-chat extraction agents) into ONE
canonical "cast & props & sets" sheet for the whole Awakeden corpus.

Output:
  ref_library/master_index.json   -- canonical, machine-readable
  ref_library/master_index.html   -- human-readable review sheet

$0 / no LLM. Deterministic merge + alias collapse + frequency ranking.
Synonym collapse is driven by ALIASES below (hand-curated after a first dry run).
Anything still looking like a near-duplicate is surfaced in a "review" section.

Run:  .venv\\Scripts\\python.exe longform\\_base_elements_index.py
      (add --extract-dir <dir> to point at the scratchpad batch files)
"""
from __future__ import annotations
import argparse
import collections
import datetime as _dt
import glob
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF_LIB = os.path.join(ROOT, "ref_library")
DEFAULT_EXTRACT_DIR = os.path.join(
    os.environ.get("TEMP", "/tmp"),
    "claude", "C--Users-sanjay-PycharmProjects-JesusInTheBible",
    "e0aa43da-d36d-4497-93e1-0f3678698d23", "scratchpad",
)

# --- synonym collapse: map any alias -> the one canonical name -----------------
# Built by the canonicalization agent over the full extracted name list, then
# verified + extended by hand (a few high-confidence merges it was conservative on).
# Conservative on purpose: only TRUE visual duplicates; biblically-distinct things
# (NOAHS_ARK vs ARK_OF_THE_COVENANT, BOAT vs STORM_TOSSED_SHIP, 20 vs 30 silver) stay split.
ALIASES = {
    # characters
    "ISAIAH_PROPHET": "ISAIAH", "PROPHET_ISAIAH": "ISAIAH",
    "AARON_HIGH_PRIEST": "AARON", "PHILIP_EVANGELIST": "PHILIP",
    "ISRAELITE_FAMILY": "ISRAELITE_HOUSEHOLD", "ISRAELITES": "ISRAELITE_CROWD",
    "MOCKERS": "MOCKING_CROWD", "MOCKING_NEIGHBOURS": "MOCKING_CROWD",
    "SHIP_SAILORS": "SAILORS", "FATHER": "THE_FATHER",
    "LAME_MAN": "LAME_MAN_OF_BETHESDA", "SCRIBES": "SCRIBES_PHARISEES",
    "ACCUSERS": "SCRIBES_PHARISEES", "SHEEP": "SHEEP_FLOCK",
    "STRAYING_SHEEP": "SHEEP_FLOCK",
    # objects
    "BRONZE_SERPENT": "BRONZE_SERPENT_STANDARD",
    "BRONZE_SERPENT_POLE": "BRONZE_SERPENT_STANDARD",
    "SERPENT_POLE": "BRONZE_SERPENT_STANDARD", "WOODEN_POLE": "BRONZE_SERPENT_STANDARD",
    "BASIN_OF_BLOOD": "BLOOD_BASIN", "SACRIFICIAL_BLOOD": "BLOOD",
    "BLOOD_ON_DOORPOSTS": "BLOOD_ON_DOORPOST", "BLOODED_DOORWAY": "BLOOD_ON_DOORPOST",
    "JOPPA_SHIP": "STORM_TOSSED_SHIP", "WOODEN_SHIP": "STORM_TOSSED_SHIP",
    "GARMENTS_AND_LOTS": "CASTING_LOTS", "MAT": "SLEEPING_MAT",
    "STONE_ALTAR": "ALTAR", "ROCK_TOMB": "RICH_MANS_TOMB",
    "OFFERING_WOOD": "BUNDLE_OF_WOOD", "PROPHETS_SCROLL": "ISAIAH_SCROLL",
    # locations
    "GOLGOTHA_HILL": "GOLGOTHA", "GAZA_ROAD": "DESERT_ROAD",
    "DESERT_WILDERNESS": "WILDERNESS", "ISRAELITE_CAMP": "WILDERNESS_CAMP",
    "CAMP_EDGE": "WILDERNESS_CAMP", "RAGING_SEA": "STORM_SEA",
    "FISH_BELLY": "BELLY_OF_THE_FISH", "EGYPTIAN_PRISON": "EGYPTIAN_DUNGEON",
    "NIGHT_INTERIOR": "JERUSALEM_NIGHT_INTERIOR", "THE_FLOOD": "FLOOD_WATERS",
    "TEMPLE_COURT": "TEMPLE", "JERUSALEM_TEACHING_PLACE": "TEMPLE",
    "DRY_LAND": "SHORE", "DRY_LAND_SHORE": "SHORE",
    # element motifs
    "PIERCED_HANDS_FEET": "PIERCED_HANDS_AND_FEET",
    "STRIPES_WOUNDS": "STRIPES_AND_WOUNDS",
    "MAN_OVERBOARD": "MAN_CAST_INTO_SEA", "ONE_CAST_INTO_SEA": "MAN_CAST_INTO_SEA",
    "HANDS_ON_THE_HEAD": "LAYING_ON_OF_HANDS", "BLOOD_ON_THE_DOOR": "BLOOD_MARKED_DOOR",
    # --- red-team round 2: confirmed-identical dupes (verified by reading both canonicals) ---
    "TORN_VEIL": "RENT_VEIL",                       # both: temple veil rent top-to-bottom
    "THE_ARK": "NOAHS_ARK",                         # THE_ARK's own text says "Noah's ark"
    "SACRIFICIAL_GOAT_SLAIN": "SLAIN_GOAT",         # same slain sin-offering goat
    "SCAPEGOAT_LIVE": "SCAPEGOAT",                  # same live azazel goat
    "SLAUGHTER_LAMB": "LAMB",                       # same Isaiah suffering-servant lamb
    "PIECES_OF_SILVER": "TWENTY_PIECES_SILVER",     # Joseph-short = the 20-piece sale
    "ARK_AND_MERCY_SEAT": "ARK_OF_THE_COVENANT",    # panel: near-duplicate gold cherubim chest
    # NOTE kept DISTINCT on purpose (looked identical but aren't): OUTSTRETCHED_PIERCED_HANDS
    # (welcoming wounded arms) vs PIERCED_HANDS_AND_FEET (wound close-up); SCROLL (generic) vs
    # ISAIAH_SCROLL; SHEEP_FLOCK (flock) vs SHEEP_GONE_ASTRAY (scattered-astray motif).
}

KIND_ORDER = {"character": 0, "object": 1, "location": 2, "element": 3}


def norm(name: str) -> str:
    n = re.sub(r"[^A-Z0-9]+", "_", (name or "").upper()).strip("_")
    return ALIASES.get(n, n)


def load_batches(extract_dir: str):
    pieces = []
    files = sorted(glob.glob(os.path.join(extract_dir, "extract_*.json")))
    if not files:
        raise SystemExit(f"No extract_*.json found in {extract_dir}")
    for fp in files:
        with open(fp, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        for p in data.get("pieces", []):
            p["_batch"] = data.get("batch", os.path.basename(fp))
            pieces.append(p)
    return files, pieces


def existing_anchors():
    cat_fp = os.path.join(REF_LIB, "catalogue.json")
    have = {}
    if os.path.exists(cat_fp):
        with open(cat_fp, "r", encoding="utf-8") as fh:
            for e in json.load(fh):
                have[norm(e["name"])] = e.get("anchor")
    return have


def build(pieces):
    elems = {}  # name -> record
    for p in pieces:
        pid = p.get("piece_id", "?")
        form = p.get("form", "?")
        for el in p.get("elements", []):
            name = norm(el.get("name", ""))
            if not name:
                continue
            rec = elems.setdefault(name, {
                "name": name,
                "kinds": collections.Counter(),
                "roles": collections.Counter(),
                "descriptors": [],
                "appearances": [],
                "forms": collections.Counter(),
            })
            rec["kinds"][el.get("kind", "element")] += 1
            if el.get("role"):
                rec["roles"][el["role"]] += 1
            d = (el.get("descriptor") or "").strip()
            if d and d not in rec["descriptors"]:
                rec["descriptors"].append(d)
            if pid not in rec["appearances"]:
                rec["appearances"].append(pid)
            rec["forms"][form] += 1

    have = existing_anchors()
    out = []
    for name, rec in elems.items():
        kind = rec["kinds"].most_common(1)[0][0]
        role = rec["roles"].most_common(1)[0][0] if rec["roles"] else None
        out.append({
            "name": name,
            "kind": kind,
            "role": role,
            "count": len(rec["appearances"]),
            "appearances": sorted(rec["appearances"]),
            "forms": dict(rec["forms"]),
            "descriptors": rec["descriptors"],
            "has_anchor": name in have and bool(have[name]),
            "anchor": have.get(name),
        })
    out.sort(key=lambda e: (KIND_ORDER.get(e["kind"], 9), -e["count"], e["name"]))
    return out


def near_dups(elems):
    """Flag names that share a stem token — candidate un-merged synonyms."""
    by_token = collections.defaultdict(list)
    for e in elems:
        toks = [t for t in e["name"].split("_") if len(t) > 3]
        for t in set(toks):
            by_token[t].append(e["name"])
    flags = []
    for t, names in sorted(by_token.items()):
        if len(names) > 1:
            flags.append((t, sorted(names)))
    return flags


def write_html(elems, flags, n_files, n_pieces, out_fp):
    now = _dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    by_kind = collections.OrderedDict()
    for e in elems:
        by_kind.setdefault(e["kind"], []).append(e)
    tot = len(elems)
    recurring = sum(1 for e in elems if e["count"] > 1)
    locked = sum(1 for e in elems if e["has_anchor"])

    rows = []
    for kind, items in by_kind.items():
        rows.append(f'<h2>{html.escape(kind.upper())} '
                    f'<span class="muted">({len(items)})</span></h2>')
        rows.append('<table><tr><th>#</th><th>name</th><th>role</th>'
                    '<th>uses</th><th>appears in</th><th>descriptor (merged)</th>'
                    '<th>ref</th></tr>')
        for i, e in enumerate(items, 1):
            badge = ('<span class="lock">LOCKED</span>' if e["has_anchor"]
                     else '<span class="gap">needs ref</span>')
            apps = ", ".join(html.escape(a) for a in e["appearances"])
            desc = " · ".join(html.escape(d) for d in e["descriptors"][:4])
            hot = ' class="hot"' if e["count"] >= 4 else ''
            rows.append(
                f'<tr{hot}><td>{i}</td><td><b>{html.escape(e["name"])}</b></td>'
                f'<td>{html.escape(e["role"] or "")}</td><td>{e["count"]}</td>'
                f'<td class="apps">{apps}</td><td class="desc">{desc}</td>'
                f'<td>{badge}</td></tr>')
        rows.append('</table>')

    flag_rows = "".join(
        f'<tr><td>{html.escape(t)}</td><td>{html.escape(", ".join(n))}</td></tr>'
        for t, n in flags)

    doc = f"""<!doctype html><meta charset="utf-8">
<title>Awakeden — Base Elements Master Index</title>
<style>
 body{{font:14px/1.5 system-ui,Segoe UI,Arial;margin:24px;color:#1d2330;background:#fbfaf7}}
 h1{{margin:0 0 4px}} .muted{{color:#8a93a6;font-weight:400}}
 .summary{{background:#fff;border:1px solid #e6e2d8;border-radius:10px;padding:14px 18px;margin:12px 0 24px}}
 .summary b{{font-size:22px}}
 table{{border-collapse:collapse;width:100%;margin:6px 0 22px;background:#fff}}
 th,td{{border:1px solid #ece8de;padding:6px 9px;text-align:left;vertical-align:top;font-size:13px}}
 th{{background:#f3f0e8;position:sticky;top:0}}
 td.apps{{color:#5b6577;font-size:12px;max-width:280px}}
 td.desc{{color:#33405a;max-width:420px}}
 tr.hot td{{background:#fff7e6}}
 .lock{{background:#1f9d55;color:#fff;padding:2px 7px;border-radius:6px;font-size:11px}}
 .gap{{background:#e9ecf2;color:#7a8294;padding:2px 7px;border-radius:6px;font-size:11px}}
 h2{{margin:22px 0 6px;border-bottom:2px solid #e6e2d8;padding-bottom:3px}}
 .flags{{background:#fff;border:1px solid #e6e2d8;border-radius:10px;padding:10px 16px}}
</style>
<h1>Awakeden — Base Elements Master Index</h1>
<div class="muted">cast &amp; props &amp; sets across the whole corpus · built {now}
 · {n_pieces} pieces from {n_files} batches</div>
<div class="summary">
 <b>{tot}</b> distinct elements &nbsp;|&nbsp;
 <b>{recurring}</b> recurring (used in &gt;1 piece) &nbsp;|&nbsp;
 <b>{locked}</b> already ref-locked &nbsp;|&nbsp;
 <b>{tot-locked}</b> still need a reference image
 <div class="muted" style="margin-top:6px">Rows highlighted = used in 4+ pieces (highest reuse value — lock these first).</div>
</div>
{''.join(rows)}
<h2>⚠ possible un-merged synonyms <span class="muted">(share a stem token — eyeball)</span></h2>
<div class="flags"><table><tr><th>token</th><th>names sharing it</th></tr>{flag_rows}</table></div>
"""
    with open(out_fp, "w", encoding="utf-8") as fh:
        fh.write(doc)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--extract-dir", default=DEFAULT_EXTRACT_DIR)
    args = ap.parse_args()

    files, pieces = load_batches(args.extract_dir)
    elems = build(pieces)
    flags = near_dups(elems)

    os.makedirs(REF_LIB, exist_ok=True)
    json_fp = os.path.join(REF_LIB, "master_index.json")
    with open(json_fp, "w", encoding="utf-8") as fh:
        json.dump({
            "built": _dt.datetime.now().isoformat(timespec="seconds"),
            "n_batches": len(files),
            "n_pieces": len(pieces),
            "n_elements": len(elems),
            "elements": elems,
        }, fh, indent=2, ensure_ascii=False)

    html_fp = os.path.join(REF_LIB, "master_index.html")
    write_html(elems, flags, len(files), len(pieces), html_fp)

    rec = sum(1 for e in elems if e["count"] > 1)
    locked = sum(1 for e in elems if e["has_anchor"])
    print(f"pieces={len(pieces)}  elements={len(elems)}  recurring={rec}  "
          f"locked={locked}  needs_ref={len(elems)-locked}")
    print(f"  {json_fp}")
    print(f"  {html_fp}")
    print(f"  synonym-stem flags: {len(flags)} (review in HTML)")


if __name__ == "__main__":
    main()
