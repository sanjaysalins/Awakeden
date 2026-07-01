#!/usr/bin/env python
"""GLOBAL asset index — every still & clip we produce, with rich metadata for reuse.

Standing rule (user, 2026-07-01): every still or clip we make must be registered here
with rich metadata so it can be reused later in other clips and videos. Assets the user
asks to REDO are DELETED from disk and DE-INDEXED — they must never enter the index.

Single canonical file: asset_index.json (repo root). Upsert by `id` (idempotent).

  import asset_index as ax
  ax.register({...})          # add / update one asset by id
  ax.deindex(id="fft_05")     # remove a redo'd asset (or deindex(path=...))
  ax.load()                   # -> {"version":1, "assets":[...]}

Rich schema per asset (author as much as is known):
  id, type(still|clip), media(image|video), path, aspect, style,
  cluster, piece, piece_title, verse, beat, beat_role, title,
  subject, characters[], elements[], setting, palette, mood, doctrine,
  reuse_scope(neutral|specific|hero), tags[], prompt, source, created, used_in[]
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "asset_index.json"

_DOC = ("GLOBAL asset index — every still/clip we produce, rich metadata for cross-piece "
        "reuse. Redo'd assets are DELETED from disk and DE-INDEXED, never kept here.")


def load() -> dict:
    if INDEX.exists():
        return json.loads(INDEX.read_text(encoding="utf-8"))
    return {"_doc": _DOC, "version": 1, "assets": []}


def save(data: dict) -> None:
    data.setdefault("_doc", _DOC)
    data.setdefault("version", 1)
    INDEX.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _norm(p) -> str:
    """Repo-relative POSIX path for stable comparison across OSes."""
    p = Path(p)
    try:
        p = p.resolve().relative_to(ROOT)
    except ValueError:
        pass
    return p.as_posix()


def register(entry: dict) -> None:
    """Upsert one asset by id. `path` is stored repo-relative."""
    if "id" not in entry:
        raise ValueError("asset entry needs an 'id'")
    if "path" in entry:
        entry = {**entry, "path": _norm(entry["path"])}
    data = load()
    assets = data["assets"]
    for i, a in enumerate(assets):
        if a.get("id") == entry["id"]:
            assets[i] = {**a, **entry}
            break
    else:
        assets.append(entry)
    save(data)


def deindex(id: str | None = None, path: str | None = None) -> int:
    """Remove assets matching id and/or path. Returns count removed."""
    data = load()
    npath = _norm(path) if path else None
    before = len(data["assets"])
    data["assets"] = [a for a in data["assets"]
                      if not ((id and a.get("id") == id) or (npath and a.get("path") == npath))]
    save(data)
    return before - len(data["assets"])


if __name__ == "__main__":
    d = load()
    print(f"asset_index.json — {len(d['assets'])} assets")
    for a in d["assets"]:
        print(f"  {a.get('id'):28} {a.get('type','?'):5} {a.get('path','')}")
