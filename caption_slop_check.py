#!/usr/bin/env python
r"""caption_slop_check.py — $0 corpus-wide AI-slop text gate (2026-07-10,
extended 2026-08-10 after a real-content audit found 96 burned-in dash-joint/
ellipsis captions across 14 episodes' FINAL captions.srt -- never caught
before because this tool only scanned the pre-transcription caption spec,
never the rendered .srt those episodes' transcription-based caption builders
actually ship. Also extended to upload_kit.json, the older Stage-5 standalone
kit format that publish/*.md's own header-skip logic doesn't cover).

User rule (memory feedback-no-dash-caption-slop): on-screen caption boxes and
publish copy must never use the dash-joint "X - Y" / "X — Y" template, ellipsis
padding, curly/smart quotes, or mojibake. Plain short sentences only. KJV
red-letter text is exempt from rewriting but still scanned (it should never
contain these anyway).

Scans:
  - every visual/livingpage_short.spec.json beat caption (cap.text)
  - every publish/*.md TITLE/DESCRIPTION/CAPTION body (header lines skipped)
  - every publish/*.srt caption cue line (index/timestamp lines skipped)
  - every upload/upload_kit.json platforms[].title/description field
  - data/upload_brand.json footer lines

Usage:
  .venv\Scripts\python.exe caption_slop_check.py            # whole repo, exit 3 on hits
  .venv\Scripts\python.exe caption_slop_check.py <folder>   # scoped
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

sys.stdout.reconfigure(errors="replace")  # Windows cp1252 console vs ✝/em-dash

ROOT = Path(__file__).resolve().parent
TOKENS = (" - ", "—", "–", "...", "…", "“", "”", "‘", "’", "â€")
# " - ", em/en dash, ellipsis (ascii+char), curly double/single quotes+apostrophe, mojibake
URL = re.compile(r"https?://\S+")
SRT_INDEX_OR_TS = re.compile(r"^\d+$|-->")


def _hits(text: str) -> list[str]:
    t = URL.sub("", text or "")
    return [tok for tok in TOKENS if tok in t]


def scan(root: Path) -> int:
    bad = 0
    for spec in sorted(root.rglob("livingpage_short.spec.json")):
        if "_stale" in str(spec) or spec.name.endswith(".pre_deslop"):
            continue
        try:
            beats = json.loads(spec.read_text(encoding="utf-8")).get("beats", [])
        except Exception as e:  # noqa - a broken spec should be visible, not fatal
            print(f"[warn] unreadable {spec}: {e}")
            continue
        for i, b in enumerate(beats, 1):
            cap = b.get("cap") or {}
            h = _hits(cap.get("text", ""))
            if h:
                bad += 1
                print(f"SPEC  {spec.parent.parent.name:28} beat {i:2} {h}: {cap.get('text','')[:80]!r}")
    for md in sorted(root.rglob("publish/*.md")):
        if ".claude" in md.parts or "archive" in md.parts or md.name.upper() == "SKILL.MD":
            continue
        for n, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            if line.startswith("#") or line.startswith("##"):
                continue
            h = _hits(line)
            if h:
                bad += 1
                print(f"PACK  {md.parent.parent.name:28} {md.name}:{n} {h}: {line.strip()[:80]!r}")
    for srt in sorted(root.rglob("publish/*.srt")):
        if ".claude" in srt.parts or "archive" in srt.parts:
            continue
        for n, line in enumerate(srt.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if not line.strip() or SRT_INDEX_OR_TS.search(line):
                continue
            h = _hits(line)
            if h:
                bad += 1
                print(f"SRT   {srt.parent.parent.name:28} :{n} {h}: {line.strip()[:80]!r}")
    for kit in sorted(root.rglob("upload/upload_kit.json")):
        if ".claude" in kit.parts or "archive" in kit.parts:
            continue
        try:
            d = json.loads(kit.read_text(encoding="utf-8"))
        except Exception as e:  # noqa - a broken kit should be visible, not fatal
            print(f"[warn] unreadable {kit}: {e}")
            continue
        for plat in d.get("platforms", []):
            for field in ("title", "description"):
                v = plat.get(field) or ""
                h = _hits(v)
                if h:
                    bad += 1
                    print(f"KIT   {kit.parent.parent.name:28} {plat.get('platform')}.{field} {h}: {v[:80]!r}")
    brand = root / "data" / "upload_brand.json"
    if brand.is_file():
        for k, v in json.loads(brand.read_text(encoding="utf-8")).items():
            if k.startswith("_"):  # internal config notes, never shipped
                continue
            if isinstance(v, str) and _hits(v):
                bad += 1
                print(f"BRAND upload_brand.json {k}: {v[:80]!r}")
    print(f"\n{'SLOP RED - ' + str(bad) + ' hit(s); fix before ship.' if bad else 'SLOP GREEN - corpus clean.'}")
    return 3 if bad else 0


if __name__ == "__main__":
    sys.exit(scan(Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT))
