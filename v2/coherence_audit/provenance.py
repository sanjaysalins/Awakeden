"""Provenance map: which finished cut used which still, and which flagged-bad stills force a
reassembly. Deterministic, $0.

For each <...>/assembly/edit_plan.json: the used scene indices = selected_scene_indices +
hero_scene_index + every slot.scene_index. Scene index N -> the still visual/<prov>/NN_*.png.
Cross-referenced with v2/coherence_audit/flagged_bad.json -> per finished short: the bad stills
it used, the clips to redo, and the finished mp4 variants to reassemble.

Run: .venv\\Scripts\\python.exe v2\\coherence_audit\\provenance.py
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = Path(__file__).resolve().parent / "provenance.json"


def _flagged() -> set[str]:
    f = Path(__file__).resolve().parent / "flagged_bad.json"
    if not f.exists():
        return set()
    try:
        rels = json.loads(f.read_text(encoding="utf-8")).get("flagged_bad", [])
    except (OSError, ValueError):
        return set()
    return {str((ROOT / r).resolve()).replace("\\", "/") for r in rels}


def _used_indices(plan: dict) -> set[int]:
    p = plan.get("plan", plan)
    idx: set[int] = set()
    for k in ("selected_scene_indices",):
        idx |= {int(i) for i in (p.get(k) or [])}
    if p.get("hero_scene_index"):
        idx.add(int(p["hero_scene_index"]))
    for s in (p.get("slots") or []):
        if s.get("scene_index") is not None:
            idx.add(int(s["scene_index"]))
    return idx


def _still_for(visual_dir: Path, index: int) -> Path | None:
    hits = sorted(visual_dir.glob(f"{index:02d}_*.png"))
    return hits[0] if hits else None


def build() -> dict:
    flagged = _flagged()
    rows = []
    for ep in sorted(ROOT.glob("longform/**/assembly/edit_plan.json")) + \
              sorted(ROOT.glob("v2/pilot/**/assembly/edit_plan.json")):
        base = ep.parent.parent                      # the v1 / short folder
        try:
            plan = json.loads(ep.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        # find the provider render dir actually used
        vdir = None
        for prov in ("nbp", "hf"):
            d = base / "visual" / prov
            if d.is_dir():
                vdir = d
                break
        if vdir is None:
            continue
        used = _used_indices(plan)
        bad_used = []
        for i in used:
            still = _still_for(vdir, i)
            if still and str(still.resolve()).replace("\\", "/") in flagged:
                clip = still.with_suffix(".mp4")
                bad_used.append({"index": i,
                                 "still": str(still.relative_to(ROOT)).replace("\\", "/"),
                                 "clip": str(clip.relative_to(ROOT)).replace("\\", "/"),
                                 "clip_exists": clip.exists()})
        finals = sorted(str(m.relative_to(ROOT)).replace("\\", "/")
                        for m in (base / "assembly").glob("*.mp4")
                        if "all_takes_reel" not in m.name and "_PRE_" not in m.name)
        rows.append({
            "short": str(base.relative_to(ROOT)).replace("\\", "/"),
            "needs_reassembly": bool(bad_used),
            "bad_stills_used": bad_used,
            "finished_variants": finals,
        })
    report = {
        "_README": "Per finished short: flagged-bad stills it actually used (redo the clip), and "
                    "the finished mp4 variants that must be reassembled after the redo.",
        "shorts": rows,
        "reassembly_needed": [r["short"] for r in rows if r["needs_reassembly"]],
    }
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


if __name__ == "__main__":
    rep = build()
    need = rep["reassembly_needed"]
    print(f"{len(rep['shorts'])} finished shorts scanned; {len(need)} need reassembly.\n")
    for r in rep["shorts"]:
        if not r["needs_reassembly"]:
            continue
        print(f"  {r['short'].split('/shorts/')[-1] if '/shorts/' in r['short'] else r['short']}")
        for b in r["bad_stills_used"]:
            print(f"      idx {b['index']:>2}  {b['still'].split('/nbp/')[-1]:42} clip={'yes' if b['clip_exists'] else 'MISSING'}")
    print(f"\n  -> {OUT}")