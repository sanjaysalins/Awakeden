"""Build panel_request.md for an EXISTING locked v1 folder (skipped the gate).
Usage: python _panel_existing.py "<v1 folder>"
"""
import sys, json
from pathlib import Path
from pipeline.models import Draft, Review, Thread
from pipeline.series import get_series
from pipeline import panel

folder = Path(sys.argv[1])
d = json.loads((folder / "narration.creation.json").read_text(encoding="utf-8"))

draft = Draft.from_json(d["draft"])
review = Review.from_json(d["self_review"])
thread = Thread.from_json(d["thread"]) if d.get("thread") else None
kjv = d.get("kjv_text")

# Episode with theme from series.json (creation.json stores only title/primary_ref)
ep = None
series = get_series(d["series"]["id"])
for e in series.episodes:
    if e.primary_ref == d["episode"]["primary_ref"]:
        ep = e
        break
if ep is None:  # fall back to a minimal Episode
    from pipeline.series import Episode
    ep = Episode(title=d["episode"]["title"], primary_ref=d["episode"]["primary_ref"],
                 refs=[d["episode"]["primary_ref"]], theme=d["episode"].get("theme",""))

# Verify the creation.json beats match the canonical narration.md
nar = (folder / "narration.md").read_text(encoding="utf-8").strip()
beat_texts = [b.text.strip() for b in draft.beats]
joined = "\n\n".join(beat_texts)
print("=== BEATS (creation.json) ===")
for b in draft.beats:
    print(f"[{b.id}] {b.text.strip()}")
print("\n=== MATCH narration.md? ===")
print("EXACT" if joined == nar else "DIFFERS — will reconcile")

out = panel.write_panel_request(folder, series, ep, draft, kjv, review, thread)
print(f"\nwrote {out}")
