#!/usr/bin/env python
"""v3 transform pass 2: resolve the last >2-use and twice-full-bleed violations."""
import json
from pathlib import Path
from collections import Counter

POOL = Path(__file__).resolve().parent / "v1" / "visual_16x9_inked"
spec = json.loads((POOL / "livingpage_full.spec.json").read_text(encoding="utf-8"))
B = spec["beats"]

def clip(slug, motion="pushin", **kw):
    d = {"slug": slug, "motion": motion}; d.update(kw); return d

def setb(i, tpl=None, clips=None):
    if tpl: B[i - 1]["tpl"] = tpl
    if clips is not None: B[i - 1]["clips"] = clips

setb(38, "full", [clip("john_at_cross_foot")])                       # crane 3rd use -> the witness
setb(25, "two_v", [clip("water_spilled_stone", "static", cam="arc", at=95.52, slide="left"),
                   clip("seventy_scribes_lamps", "static", cam="arc", at=95.78, slide="right")])
setb(85, "full", [clip("old_king_hands_rings", "static", cam="arc")])  # lyre 3rd -> the king's hands at rest
setb(62, "two_v", [clip("face_anguish_closeup", at=260.50, slide="left"),
                   clip("cry_face_tears", at=261.26, slide="right")])
setb(86, "two_v", [clip("convergence_on_cross", at=364.62, slide="left"),
                   clip("roads_converge_valley", "static", cam="arc", zoom=1.2, at=365.33, slide="right")])
setb(57, "two_v", [clip("cross_hill_pullback", "pullback", at=234.49, slide="left"),
                   clip("kneeling_at_cross", at=235.36, slide="right")])
setb(78, "two_v", [clip("empty_tomb_open", at=328.19, slide="left"),
                   clip("stone_rolled_groove", "static", cam="arc", at=331.49, slide="right")])

(POOL / "livingpage_full.spec.json").write_text(json.dumps(spec, indent=1), encoding="utf-8")
cnt = Counter(); fb = Counter()
for b in B:
    for c in b["clips"]:
        cnt[c["slug"]] += 1
        if b["tpl"] == "full": fb[c["slug"]] += 1
print("stills >2x:", {s: n for s, n in cnt.items() if n > 2} or "NONE")
print("full-bleed >1x:", {s: n for s, n in fb.items() if n > 1} or "NONE")
print("full-bleed beats:", sum(1 for b in B if b["tpl"] == "full"), "/", len(B))
print("distinct stills:", len(cnt), " slots:", sum(cnt.values()))
