#!/usr/bin/env python
"""Resolve beats_raw.json -> livingpage_full.spec.json: merge adjacent same-slug
'full' beats (which would violate the >=8-beat reuse gate), resolve each beat's
'start' phrase to an absolute time via the word-timed alignment, chain t1=next t0,
and self-check the SAME reuse rule the engine enforces (crop_seen >=8 beats apart)
before ever calling the real build script."""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wordtime import Cursor

HERE = Path(__file__).resolve().parent
POOL = HERE.parents[0] / "v1" / "visual_16x9_inked"
raw = json.loads((HERE / "beats_raw.json").read_text(encoding="utf-8"))

# ---------------- 1) merge adjacent 'full' beats sharing the same slug ----------------
merged = []
for b in raw:
    if (merged and b["tpl"] == "full" and merged[-1]["tpl"] == "full"
            and b["clips"][0]["slug"] == merged[-1]["clips"][0]["slug"]):
        prev = merged[-1]
        # keep the LATER beat's caption (usually the actual KJV quote / payoff line);
        # keep the earlier beat's start (so the merged beat covers both text spans).
        prev["cap"] = b["cap"]
        if b.get("punch"):
            prev["punch"] = True
        if b.get("cam"):
            prev["clips"][0]["cam"] = b["clips"][0].get("cam")
        if b.get("ramp"):
            prev["ramp"] = True
        if b.get("inserts"):
            prev.setdefault("inserts", []).extend(b["inserts"])
        print(f"  [merge] {prev['start']!r} + {b['start']!r} -> one beat (slug {b['clips'][0]['slug']})")
    else:
        merged.append(dict(b))

print(f"\n{len(raw)} raw beats -> {len(merged)} after adjacent-slug merge\n")

# ---------------- 2) resolve times ----------------
c = Cursor()
t0s = []
for b in merged:
    t0s.append(c.t0(b["start"]))
total_end = round(c.total_end() + 1.3, 2)   # short tail after the last word

for i, b in enumerate(merged):
    t0 = t0s[i]
    t1 = t0s[i + 1] if i + 1 < len(merged) else total_end
    b["t"] = [round(t0, 3), round(t1, 3)]
    del b["start"]
    # convert authoring-time fractional offsets -> absolute times the engine expects
    if b.get("inserts"):
        for ins in b["inserts"]:
            if "at_frac" in ins:
                ins["at"] = round(t0 + ins.pop("at_frac") * (t1 - t0), 3)
            ins.setdefault("frames", 4)
    if b.get("takeover"):
        tk = b["takeover"]
        if "start_frac" in tk:
            tk["start"] = round(t0 + tk.pop("start_frac") * (t1 - t0), 3)
    # fracture beats: convert panel slide list + spread panel_at across the beat
    if b["tpl"] == "hero_frac3":
        slides = b.pop("_panel_slide", ["left", "up", "right"])
        b["panel_slide"] = slides
        n = len(b["anchors"])
        fracs = [0.0, 0.38, 0.7][:n]
        b["panel_at"] = [round(t0 + f * (t1 - t0), 3) for f in fracs]

# ---------------- 3) self-check the reuse gate (mirrors base._reuse_check) ----------------
crop_seen = {}
violations = []
for i, b in enumerate(merged, 1):
    tpl = b["tpl"]
    if tpl == "hero_frac3":
        slug = b["clips"][0]["slug"]
        crop_id = ("frac", tuple(tuple(a) for a in b["anchors"]))
        slugs_this_beat = [(slug, crop_id)]
    elif tpl == "full":
        slug = b["clips"][0]["slug"]
        crop_id = ("full", b["clips"][0].get("cam"))
        slugs_this_beat = [(slug, crop_id)]
    else:  # grid modes: one crop_id check per clip
        slugs_this_beat = [(cd["slug"], ("grid", tpl, cd.get("cam"))) for cd in b["clips"]]
    for slug, crop_id in slugs_this_beat:
        if slug in crop_seen:
            prev_beat, prev_id = crop_seen[slug]
            if i - prev_beat < 8:
                violations.append(f"beat {prev_beat}->{i} slug={slug} gap={i - prev_beat} (<8)")
            elif crop_id == prev_id:
                violations.append(f"beat {prev_beat}->{i} slug={slug} SAME CROP {crop_id}")
        crop_seen[slug] = (i, crop_id)

print(f"total beats: {len(merged)}  total duration: {total_end}s")
print("\n--- beat index : tpl : slugs : t0-t1 ---")
for i, b in enumerate(merged, 1):
    slugs = ",".join(cd["slug"] for cd in b["clips"])
    print(f"  {i:3} {b['tpl']:10} {slugs:70} {b['t']}")
if violations:
    print(f"\n!!! {len(violations)} REUSE VIOLATIONS:")
    for v in violations:
        print("  " + v)
else:
    print("\nreuse gate: CLEAN (0 violations)")

durs = [b["t"][1] - b["t"][0] for b in merged]
from collections import Counter
tplc = Counter(b["tpl"] for b in merged)
print(f"avg dur: {sum(durs)/len(durs):.2f}s  median approx: {sorted(durs)[len(durs)//2]:.2f}s  max: {max(durs):.2f}s")
print("template mix:", dict(tplc))

# strip helper-only key
for b in merged:
    b.pop("_panel_slide", None)

out = {
    "_doc": "BRONZE SERPENT - dense living-page rebuild (2026-07-16). Re-authored from the flat "
            "27-beat/'full' version to a comic-grid pacing matching the Isaiah 53 reference: fracture "
            "(hero_frac3) on multi-figure OT stills, two_v/triptych_v/big_inset grids in the NT/typology "
            "section mixing this episode's own 27 inked stills with 21 reused neutral inked Cross-cluster "
            "clips (batches/cluster_01_cross/*/visual/clips, scope=thread-neutral crucifixion/resurrection "
            "iconography). Sacred red-letter beats (THE LORD/JESUS/SCRIPTURE quotes) carry no punch.",
    "audio": "../narration.mp3",
    "total": total_end,
    "cut_ticks": True,
    "beats": merged,
}
(POOL / "livingpage_full.spec.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(f"\nwrote {POOL / 'livingpage_full.spec.json'}")
