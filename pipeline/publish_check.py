"""pipeline/publish_check.py — the GREEN gate for a JITB publish pack (Stage 6).

"The gate is the success bar." A pack is DONE only when this is GREEN. It does not
judge how good the copy *reads* (that's the panel red-team + your eye); it enforces
the mechanical things that quietly sink a post, by parsing the ON-DISK pack files
(the source of truth after any panel/hand edit) back into an UploadKit and running
the same UK-G1..G7 gates the engine uses — no second rulebook.

Checks:
  - every required platform file present AND filled (no TODO placeholder)
  - UK-G1 length · UK-G2 KJV-strict · UK-G3 doctrine · UK-G4 brand/footer ·
    UK-G5 platform/hashtags · UK-G6 no-title-collision · UK-G7 anti-slop+grace+SEO
  - captions.srt present for each unit, and parses
  - YouTube CHAPTERS start at 0:00 and ascend (long only)
  - thumbnail referenced exists (WARN — JITB has no thumbnail stage yet)

Importable:  fails, warns = publish_check.check_unit(media_dir)
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from pipeline import upload_engine, upload_gates
from pipeline.publish_pack import (
    LONG_PLATFORMS,
    PLATFORM_FILE,
    SHORT_PLATFORMS,
    _CAPTION_PLATFORMS,
    _TAGS_PLATFORMS,
    _is_placeholder,
    parse_copy,
)
from pipeline.upload_models import PlatformMeta, UploadKit

_TS_RE = re.compile(r"^(\d+):(\d{2})(?::(\d{2}))?\s+\S")

# ToS / publishing landmines (ported from fg-publish's banlist): naming a real
# composer/artist or claiming "official audio" in published copy is a copyright/ToS
# trap (the ElevenLabs/Suno lesson). UK-G3 covers clickbait; this covers ToS.
_TOS_BANLIST = [
    "hans zimmer", "john williams", "ennio morricone", "thomas bekker", "hans-zimmer",
    "official audio", "copyrighted music", "no copyright intended",
]


def _check_tos(kit, fails: list[str]) -> None:
    for p in kit.platforms:
        blob = "\n".join([p.title, p.description] + p.tags + p.hashtags).lower()
        for term in _TOS_BANLIST:
            if term in blob:
                fails.append(f"{p.platform}: ToS/banlist term present -> '{term}' (strip it)")


def _body_section(plat: str) -> str:
    return "CAPTION" if plat in _CAPTION_PLATFORMS else "DESCRIPTION"


def _kit_from_pack(media_dir: str | Path, specs: dict) -> tuple[UploadKit, list[str]]:
    """Re-harvest the facts, rebuild the PlatformMeta list from the on-disk pack."""
    facts = upload_engine.harvest_facts(str(media_dir))
    pub = Path(media_dir).resolve() / "publish"
    platforms = LONG_PLATFORMS if facts.format == "long" else SHORT_PLATFORMS
    metas: list[PlatformMeta] = []
    missing: list[str] = []
    for plat in platforms:
        path = pub / PLATFORM_FILE[plat]
        if not path.exists():
            missing.append(PLATFORM_FILE[plat])
            continue
        f = parse_copy(path)
        body = f.get(_body_section(plat), "")
        tags = [t.strip() for t in f.get("TAGS", "").split(",") if t.strip()] if plat in _TAGS_PLATFORMS else []
        hashtags = [h.strip() for h in f.get("HASHTAGS", "").split() if h.strip()]
        metas.append(PlatformMeta(
            platform=plat,
            label=specs.get(plat, {}).get("label", plat),
            title=f.get("TITLE", "").strip(),
            description=body.strip(),
            tags=tags,
            hashtags=hashtags,
        ))
    return UploadKit(source=facts, platforms=metas), missing


def _check_placeholders(media_dir: Path, is_long: bool, fails: list[str]) -> None:
    pub = media_dir / "publish"
    platforms = LONG_PLATFORMS if is_long else SHORT_PLATFORMS
    for plat in platforms:
        path = pub / PLATFORM_FILE[plat]
        if not path.exists():
            fails.append(f"{PLATFORM_FILE[plat]}: MISSING (run cli_publish.py)")
            continue
        for sec, txt in parse_copy(path).items():
            if _is_placeholder(txt):
                fails.append(f"{PLATFORM_FILE[plat]}: ## {sec} still a placeholder / empty")


def _check_srt(pub: Path, fails: list[str]) -> None:
    p = pub / "captions.srt"
    if not p.exists():
        fails.append("captions.srt missing (no <final video>.words.json, or video not rendered)")
        return
    txt = p.read_text(encoding="utf-8")
    if not re.search(r"\d\d:\d\d:\d\d,\d\d\d\s*-->\s*\d\d:\d\d:\d\d,\d\d\d", txt):
        fails.append("captions.srt has no valid cues / malformed timestamps")


def _check_chapters(pub: Path, fails: list[str], warns: list[str]) -> None:
    f = parse_copy(pub / "youtube_long.md")
    ch = f.get("CHAPTERS", "")
    if _is_placeholder(ch):
        return  # placeholder already failed elsewhere
    lines = [ln.strip() for ln in ch.splitlines() if ln.strip()]
    first = _TS_RE.match(lines[0]) if lines else None
    if not first or (int(first.group(1)), int(first.group(2))) != (0, 0):
        fails.append("youtube_long.md: CHAPTERS must start at '0:00 <label>'")
    secs = []
    for ln in lines:
        m = _TS_RE.match(ln)
        if not m:
            warns.append(f"youtube_long.md: chapter line not 'M:SS Label': {ln[:40]!r}")
            continue
        h, mi, s = int(m.group(1)), int(m.group(2)), int(m.group(3) or 0)
        secs.append(h * 3600 + mi * 60 + s if m.group(3) else h * 60 + mi)
    if secs and secs != sorted(secs):
        fails.append("youtube_long.md: CHAPTERS timestamps not increasing")


def check_unit(media_dir: str | Path, *, sibling_titles: list[str] | None = None,
               ) -> tuple[list[str], list[str]]:
    """Gate ONE unit's publish pack. Returns (fails, warns)."""
    media = Path(media_dir).resolve()
    pub = media / "publish"
    fails: list[str] = []
    warns: list[str] = []
    if not pub.is_dir():
        return [f"no publish pack at {pub} — run cli_publish.py first"], warns

    specs = upload_gates.load_specs()
    brand = upload_engine.load_brand()
    kit, missing = _kit_from_pack(media, specs)
    for fname in missing:
        fails.append(f"{fname}: MISSING (run cli_publish.py)")

    is_long = kit.source.format == "long"
    _check_placeholders(media, is_long, fails)

    # the same deterministic gates the engine uses (one rulebook)
    if kit.platforms:
        for g in upload_gates.run_all(kit, brand, sibling_titles or []):
            if not g.passed:
                fails.append(f"{g.gate} {g.name}: {g.detail}")
        _check_tos(kit, fails)

    _check_srt(pub, fails)
    if is_long:
        _check_chapters(pub, fails, warns)

    # thumbnail (WARN — no thumbnail stage in JITB yet)
    src = pub / "_source.json"
    if src.exists():
        thumb = json.loads(src.read_text(encoding="utf-8")).get("thumbnail", "")
        if not thumb:
            warns.append("no thumbnail (JITB has no thumbnail stage yet - add a cover before posting)")
        elif not Path(thumb).exists():
            warns.append(f"thumbnail referenced but missing: {thumb}")

    return fails, warns


def report(media_dir: str | Path, *, strict: bool = False,
           sibling_titles: list[str] | None = None) -> bool:
    fails, warns = check_unit(media_dir, sibling_titles=sibling_titles)
    if strict:
        fails, warns = fails + warns, []
    name = Path(media_dir).name
    print(f"=== publish_check: {name} ===")
    for w in warns:
        print(f"  WARN  {w}")
    for f in fails:
        print(f"  FAIL  {f}")
    if fails:
        print(f"\nRED ({len(fails)} fail, {len(warns)} warn) — fix and re-run.")
        return False
    print(f"\nGREEN (0 fail, {len(warns)} warn). Pack is gate-clean.")
    return True
