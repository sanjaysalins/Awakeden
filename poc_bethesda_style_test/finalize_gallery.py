"""THROWAWAY POC — rebuild the gallery now that all 12 stills (incl. 2 retries) exist."""
from __future__ import annotations
from pathlib import Path
import build_stills as b

results = []
for item in b.STILLS:
    stem = f"{item['concept']}_{item['id']}"
    ok = (b.OUT_DIR / f"{stem}.png").exists()
    results.append({**item, "stem": stem, "ok": ok, "error": None})

b.build_gallery(results)
