#!/usr/bin/env python3
"""Generate PLACEHOLDER catalogue entries for the back-catalogue narrations.

The back-catalogue lives in the separate PythonProject1 repo and is still in the
older (pre-v2) format. We do NOT build rich study pages for it yet -- those come
when the main pipeline re-processes each piece into the v2 scope. For now this
just emits manifest items (title / verse / series / status) so the public site
tracks the whole body of work as the v2 migration progresses.

  python _website/import_catalogue.py    # writes _website/_import_items.yaml
then merge the items into manifest.yaml and run build_catalog.py.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent
SRC = Path(r"C:/Users/sanjay/PycharmProjects/PythonProject1/jesus/narration")

OLD_VIDEO = {
    "08 The Well That Never Runs Dry", "12 The Kiss That Cut Off the Bargain",
    "16 The Fire Jesus Built", "18 He Never Said Yes", "32_The_Door_Was_a_Body",
    "33_The_Shepherd_In_The_Gap", "34_The_Hunger_Bread_Cant_Fill",
    "35_Manna_Fulfilled", "36_In_No_Wise_Cast_Out",
}
TEXT_ONLY = {
    "02 Why are you afraid", "05 He Said It Under the Lamps",
    "23 The Prepared Belly", "Who Do You Say I Am",
}
SERIES_MAP = {
    "questions": "questions-jesus-asked", "i am": "i-am-sayings", "i-am": "i-am-sayings",
    "encounters": "people-who-encountered-jesus", "parables": "parables-of-jesus",
    "old testament": "jesus-in-ot", "jesus in the ol": "jesus-in-ot", "miracles": "miracles-of-jesus",
}
SERIES_FIX = {
    "10 The Line He Never Got to Say": "parables-of-jesus",
    "11 The Confession He Never Finished": "parables-of-jesus",
    "12 The Kiss That Cut Off the Bargain": "people-who-encountered-jesus",
    "16 The Fire Jesus Built": "people-who-encountered-jesus",
    "08 The Well That Never Runs Dry": "people-who-encountered-jesus",
    "26 Jesus Walked Past the Pool": "miracles-of-jesus",
    "20 He Was Asleep in the Storm": "miracles-of-jesus",
    "Who Do You Say I Am": "questions-jesus-asked",
}
REF_FIX = {
    "04 psalms 22 part 2": "Psalm 22:1", "12 The Kiss That Cut Off the Bargain": "Luke 22:48",
    "33_The_Shepherd_In_The_Gap": "John 10:11", "34_The_Hunger_Bread_Cant_Fill": "John 6:35",
    "35_Manna_Fulfilled": "John 6:49", "36_In_No_Wise_Cast_Out": "John 6:37",
    "Who Do You Say I Am": "Matthew 16:15", "16 The Fire Jesus Built": "John 21:17",
}
TITLE_FIX = {  # creation.json title was templated/wrong
    "05 He Said It Under the Lamps": "He Said It Under the Lamps",
    "31 The Light You Can Stand In": "The Light You Can Stand In",
    "04 psalms 22 part 2": "Psalm 22, Part 2",
}


def title_of(folder: str) -> str:
    if folder in TITLE_FIX:
        return TITLE_FIX[folder]
    t = re.sub(r"^[0-9]+[ _]*", "", folder).replace("_", " ").strip()
    t = t.replace(" — ", ": ").replace("—", ", ").replace("–", "-").replace("’", "'")
    return t[:1].upper() + t[1:]


def slugify(folder: str) -> str:
    s = re.sub(r"^[0-9]+[ _]*", "", folder)
    return re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()[:48]


def best_narration(ep: Path):
    cands = list(ep.rglob("narration.md"))
    if not cands:
        return None
    cands.sort(key=lambda p: (not (p.parent / "narration.creation.json").is_file(), len(p.parts)))
    return cands[0]


def hook_of(md_text: str) -> str:
    for line in md_text.splitlines():
        s = line.strip()
        if not s or s[0] in "#-*>|`" or s.startswith("**["):
            continue
        if len(s) < 15:
            continue
        s = s.replace(" — ", ", ").replace("—", ", ").replace("’", "'").replace("…", "...")
        s = s.replace("“", '"').replace("”", '"').replace("–", "-")
        return s[:180]
    return ""


def yq(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main() -> int:
    out, counts = [], {}
    for ep in sorted(SRC.iterdir()):
        if not ep.is_dir() or ep.name.startswith("_"):
            continue
        nm = best_narration(ep)
        if not nm:
            continue
        series = ""
        cj = nm.parent / "narration.creation.json"
        ref = ""
        if cj.is_file():
            try:
                c = json.loads(cj.read_text(encoding="utf-8"))
                ref = (c.get("episode") or {}).get("primary_ref", "")
                series = (c.get("series") or {}).get("name", "")
            except Exception:
                pass
        ref = REF_FIX.get(ep.name) or ref or "?"
        sid = SERIES_FIX.get(ep.name) or next(
            (v for k, v in SERIES_MAP.items() if k in (series or "").lower()), "jesus-in-ot"
        )
        status = "planned" if ep.name in TEXT_ONLY else "in_production"
        hook = hook_of(nm.read_text(encoding="utf-8", errors="ignore"))
        out.append({
            "slug": slugify(ep.name), "title": title_of(ep.name),
            "ref": ref, "series": sid, "status": status, "hook": hook,
        })
        counts[sid] = counts.get(sid, 0) + 1

    lines = ["# --- Back-catalogue placeholders (auto-generated; rich pages land when v2 re-processes each) ---", ""]
    for it in out:
        lines += [
            f"  - slug: {it['slug']}",
            "    kind: short",
            f"    title: {yq(it['title'])}",
            f"    ref: {yq(it['ref'])}",
            f"    series_id: {it['series']}",
            "    cluster: null",
            f"    public_status: {it['status']}",
            "    featured: false",
            "    preview_approved: false",
            "    preview_source: null",
            "    youtube_id: null",
            f"    public_hook: {yq(it['hook'])}",
            f"    public_blurb: {yq(it['hook'])}",
            "",
        ]
    (SITE / "_import_items.yaml").write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {len(out)} placeholder items -> {SITE / '_import_items.yaml'}")
    for s, n in sorted(counts.items()):
        print(f"  {s}: {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
