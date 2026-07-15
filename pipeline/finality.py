"""pipeline/finality.py — the ONE "what is the final video" rule + content sha.

Before this module, four callers (production_board, publish_pack, upload_engine,
thumbnails) each re-implemented finality with slightly different precedence, and
only thumbnails skipped `.bak` backups. All four now call here. See
v2/RELEASE_SYNC.md (incl. the 2026-07-15 red-team record).

Precedence (CAPTION POLICY 2026-07-08: comic boxes are the captions, the SFX bed
IS the postable final):

  pin          <piece>/FINAL_VIDEO.txt (first line = relative path) overrides
               everything — the escape hatch for lanes where the rule can't
               know (e.g. a legacy serif-captioned long whose postable is the
               *_sfx_captioned.mp4)
  short lane   visual/*_sfx.mp4 > visual/_byteplus/*_scored.mp4 > visual/*_scored.mp4
  long lane    *_sfx.mp4 ACROSS visual_16x9 + visual_16x9_inked, then
               *_captioned.mp4 across both — pattern outranks directory, so an
               inked-rebuild sfx beats an old visual_16x9 captioned (red-team C1)
  legacy       assembly/viral_cut_sfx_music_captioned.mp4 > _sfx_captioned
               > _captioned > any *_captioned.mp4

Ties inside a pattern prefer the DEEPER processing chain ("scored" in the name
wins: Isaiah53_16x9_scored_captioned.mp4 beats Isaiah53_16x9_captioned.mp4 —
red-team C1), then sort. `.bak*` files are NEVER a final.

Staleness is judged by CONTENT, never by mtime alone (dyncam-stale-cache
lesson). content_sha() trusts a cache entry only when size AND an
always-recomputed head+tail fingerprint match — a metadata-preserving file swap
(same size, restored mtime) cannot return a stale sha (red-team empirical find).
Cache: data/.sha_cache.json, atomic writes, dead keys pruned.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_SHA_CACHE = ROOT / "data" / ".sha_cache.json"
_PIN = "FINAL_VIDEO.txt"

# statuses
FINAL_SFX = "FINAL (sfx)"
FINAL_LEGACY = "FINAL (legacy)"
FINAL_PINNED = "FINAL (pinned)"
NEEDS_SFX = "scored (needs SFX)"
NO_VIDEO = "no video"

_LEGACY_ORDER = [
    "viral_cut_sfx_music_captioned.mp4",
    "viral_cut_sfx_captioned.mp4",
    "viral_cut_captioned.mp4",
]

_LONG_DIRS = ("visual_16x9", "visual_16x9_inked")


def _clean(hits) -> list[Path]:
    return [h for h in sorted(hits) if ".bak" not in h.name]


def _deepest(hits: list[Path]) -> Path:
    """Tie-break inside one pattern: the deeper processing chain wins
    (*_scored_captioned > *_captioned, *_scored_sfx > *_sfx)."""
    return sorted(hits, key=lambda h: ("scored" not in h.name, h.name))[0]


def final_video(piece_dir: str | Path) -> tuple[str, Path | None]:
    """(status, path) for a piece folder of ANY layout. Layout is detected, not
    declared: visual/ = living-page short, visual_16x9*/ = long, assembly/ = legacy."""
    root = Path(piece_dir).resolve()

    pin = root / _PIN
    if pin.is_file():
        rel = pin.read_text(encoding="utf-8").strip().splitlines()[0].strip()
        p = root / rel
        # a dangling pin is a defect, never a silent fallback (fail-closed)
        return (FINAL_PINNED, p) if p.is_file() else (NO_VIDEO, None)

    v = root / "visual"
    if v.is_dir():
        hits = _clean(v.glob("*_sfx.mp4"))
        if hits:
            return FINAL_SFX, _deepest(hits)
        for pat in ("_byteplus/*_scored.mp4", "*_scored.mp4"):
            hits = _clean(v.glob(pat))
            if hits:
                return NEEDS_SFX, hits[0]

    dirs16 = [root / s for s in _LONG_DIRS if (root / s).is_dir()]
    if dirs16:
        for pat, status in (("*_sfx.mp4", FINAL_SFX), ("*_captioned.mp4", FINAL_LEGACY)):
            hits: list[Path] = []
            for d in dirs16:
                hits += _clean(d.glob(pat))
            if hits:
                return status, _deepest(hits)

    a = root / "assembly"
    if a.is_dir():
        for name in _LEGACY_ORDER:
            if (a / name).is_file():
                return FINAL_LEGACY, a / name
        hits = _clean(a.glob("*_captioned.mp4"))
        if hits:
            return FINAL_LEGACY, hits[0]

    return NO_VIDEO, None


def rival_finals(piece_dir: str | Path) -> list[Path]:
    """Same-lane candidates the rule did NOT pick (long lanes only — that's
    where ambiguity is real, e.g. sfx vs sfx_captioned). Empty when pinned.
    The gate WARNs on these: pin with FINAL_VIDEO.txt to silence."""
    root = Path(piece_dir).resolve()
    if (root / _PIN).is_file():
        return []
    _status, video = final_video(root)
    if not video:
        return []
    dirs16 = [root / s for s in _LONG_DIRS if (root / s).is_dir()]
    if video.parent not in dirs16:
        return []
    rivals: list[Path] = []
    for d in dirs16:
        for pat in ("*_sfx.mp4", "*_captioned.mp4"):
            rivals += [h for h in _clean(d.glob(pat)) if h != video]
    return rivals


# ----------------------------------------------------------------------------
# content sha
# ----------------------------------------------------------------------------
def _quick_fp(p: Path, size: int) -> str:
    """Head+tail 64KB fingerprint, recomputed on EVERY call — the cache trust
    anchor (size+mtime alone is spoofable by a metadata-preserving swap)."""
    h = hashlib.sha256(str(size).encode())
    with p.open("rb") as fh:
        h.update(fh.read(65536))
        if size > 131072:
            fh.seek(-65536, 2)
            h.update(fh.read(65536))
    return h.hexdigest()


def _load_cache() -> dict:
    try:
        return json.loads(_SHA_CACHE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def content_sha(path: str | Path) -> str:
    """sha256 of the file, cached; trust = (size, head+tail fingerprint).
    '' if the file is absent."""
    p = Path(path)
    if not p.is_file():
        return ""
    size = p.stat().st_size
    qfp = _quick_fp(p, size)
    key = str(p.resolve())
    hit = _load_cache().get(key)
    if hit and hit.get("size") == size and hit.get("qfp") == qfp:
        return hit["sha"]
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    sha = h.hexdigest()
    cache = _load_cache()  # re-read: merge with any concurrent writer
    cache[key] = {"size": size, "qfp": qfp, "sha": sha}
    cache = {k: v for k, v in cache.items() if Path(k).is_file()}  # prune dead keys
    _SHA_CACHE.parent.mkdir(parents=True, exist_ok=True)
    tmp = _SHA_CACHE.with_suffix(f".{os.getpid()}.tmp")
    try:
        tmp.write_text(json.dumps(cache, indent=1), encoding="utf-8")
        os.replace(tmp, _SHA_CACHE)
    except OSError:
        tmp.unlink(missing_ok=True)  # caching is best-effort; the sha is correct
    return sha
