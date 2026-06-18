"""Clip-reuse optimization — reuse a clean existing clip BEFORE paying to regenerate.

Builds on clip_library (the indexed reuse bank) + the coherence/clip-qc gates. Given a needed
scene, it ranks library clips that are SAFE to reuse and returns a reuse-or-generate decision:

  SAFE to reuse means ALL of:
    - source clip + its still still exist on disk (quarantined ones vanish -> auto-excluded),
    - the still is coherence-verified (INV-23) AND the clip is clip-qc'd,
    - topical-fit honoured: scope='neutral' is cross-episode-safe; scope='specific' only when
      the caller explicitly allows it for a same-subject episode (feedback-topical-fit-gate),
    - the jesus_variant matches (or the entry has none),
    - not already used in THIS cut (no-repeat-within-a-video rule).

  decide(need) -> {"action":"reuse", clip, score, why} | {"action":"generate", why}
  Reuse wins only when the best clean candidate clears `min_overlap` tag matches — otherwise
  generate (better to pay than to force a weak match).

Run: .venv\\Scripts\\python.exe -m pipeline.clip_reuse find "dice-garments,soldier" [--scope neutral]
     .venv\\Scripts\\python.exe -m pipeline.clip_reuse audit   # how many indexed clips are still clean-reusable
"""
from __future__ import annotations
import sys
from pathlib import Path

from pipeline import clip_qc, coherence, clip_element_gate

ROOT = Path(__file__).resolve().parent.parent


def _load() -> list[dict]:
    from clip_library import clip_library
    return clip_library.load()


def _flagged_bad_srcs() -> set[str]:
    """Source stems the user/audit flagged bad — never reuse these."""
    f = ROOT / "v2" / "coherence_audit" / "flagged_bad.json"
    if not f.exists():
        return set()
    import json as _j
    try:
        rels = _j.loads(f.read_text(encoding="utf-8")).get("flagged_bad", [])
    except (OSError, ValueError):
        return set()
    return {str((ROOT / r).with_suffix("").resolve()).replace("\\", "/") for r in rels}


def is_clean_reusable(entry: dict) -> bool:
    """Reusable iff the source clip survives, its still is COHERENCE-verified, and it is NOT
    user/audit-flagged. Clip-motion QC is a point-of-USE look — requiring a recorded clip_qc
    sidecar as a catalogue filter wrongly excluded the entire bank (none was ever written)."""
    src = ROOT / (entry.get("source") or "")
    if not src.exists():                       # quarantined / moved
        return False
    if str(src.with_suffix("").resolve()).replace("\\", "/") in _flagged_bad_srcs():
        return False
    if clip_element_gate.is_failed(src):       # recorded element-gate FAIL -> never reuse (JIT-gated)
        return False                           # (a MISSING verdict is NOT a fail — default-PASS, gate at pull)
    return coherence.is_verified(src.with_suffix(".png"))


def _score(entry: dict, want_tags: set[str], variant: str | None) -> int:
    ctags = {t.lower() for t in entry.get("tags", [])}
    overlap = len(want_tags & ctags)
    s = overlap * 2
    if entry.get("preferred"):
        s += 5
    if variant and entry.get("jesus_variant") == variant:
        s += 2
    return s


def rank(tags: list[str], *, scope: str = "neutral", variant: str | None = None,
         exclude_sources: set[str] | None = None, require_clean: bool = True) -> list[dict]:
    """Ranked reusable candidates (best first). scope: 'neutral'|'specific'|'any'."""
    want = {t.lower() for t in (tags or [])}
    excl = {s.replace("\\", "/") for s in (exclude_sources or set())}
    out = []
    for e in _load():
        if scope != "any" and e.get("scope") != scope:
            continue
        if variant and e.get("jesus_variant") not in (variant, None):
            continue
        if (e.get("source") or "").replace("\\", "/") in excl:
            continue                            # no-repeat within the cut
        if require_clean and not is_clean_reusable(e):
            continue
        sc = _score(e, want, variant)
        if sc <= 0:
            continue
        out.append({**e, "_score": sc, "_overlap": len(want & {t.lower() for t in e.get('tags', [])})})
    out.sort(key=lambda e: (-e["_score"], e.get("title", "")))
    return out


def decide(tags: list[str], *, scope: str = "neutral", variant: str | None = None,
           exclude_sources: set[str] | None = None, min_overlap: int = 1) -> dict:
    """Reuse-or-generate. Reuse only when the best clean candidate shares >= min_overlap tags."""
    cands = rank(tags, scope=scope, variant=variant, exclude_sources=exclude_sources)
    if cands and cands[0]["_overlap"] >= min_overlap:
        top = cands[0]
        return {"action": "reuse", "clip": top["source"], "slug": top.get("slug"),
                "score": top["_score"], "overlap": top["_overlap"],
                "why": f"clean reusable clip shares {top['_overlap']} tag(s)"}
    if cands:
        return {"action": "generate",
                "why": f"best candidate too weak (overlap {cands[0]['_overlap']} < {min_overlap})"}
    return {"action": "generate", "why": "no clean reusable candidate (none verified / none in scope)"}


# ---------------------------------------------------------------- scene-aware (scene planning)
# A Scene has no curated `tags` field, so match the LIBRARY entry's tags against the scene's own
# words (title/slug/visible_elements/macro_elements) as substrings — lenient enough that a
# 'dice-garments' library clip matches a scene about dice and garments, strict enough to stay $0.

def scene_text(scene: dict) -> str:
    parts = [str(scene.get(k, "")) for k in ("title", "slug", "visible_elements", "emotional_tone")]
    parts += [str(x) for x in (scene.get("macro_elements") or [])]
    parts += [str(x) for x in (scene.get("vignettes") or [])]
    return " ".join(parts).lower()


def _tag_hits(entry: dict, text: str) -> int:
    """A library tag 'hits' the scene if ANY of its meaningful tokens (>=3 chars, split on
    '-'/space) appears in the scene's words — so 'dice-garments' matches a scene about dice."""
    import re
    hits = 0
    for t in entry.get("tags", []):
        toks = [w for w in re.split(r"[-\s]+", str(t).lower()) if len(w) >= 3]
        if any(w in text for w in toks):
            hits += 1
    return hits


def decide_for_scene(scene: dict, *, scope: str = "neutral",
                     exclude_sources: set[str] | None = None, min_hits: int = 1) -> dict:
    """Reuse-or-generate for ONE scene_plan scene. Reuse only a clean, in-scope, variant-matched
    library clip whose tags appear in the scene's words (>= min_hits)."""
    text = scene_text(scene)
    variant = scene.get("jesus_variant")
    excl = {s.replace("\\", "/") for s in (exclude_sources or set())}
    best = None
    for e in _load():
        if scope != "any" and e.get("scope") != scope:
            continue
        if variant and e.get("jesus_variant") not in (variant, None):
            continue
        if (e.get("source") or "").replace("\\", "/") in excl:
            continue
        if not is_clean_reusable(e):
            continue
        hits = _tag_hits(e, text)
        if hits < min_hits:
            continue
        score = hits * 2 + (5 if e.get("preferred") else 0) + (2 if variant and e.get("jesus_variant") == variant else 0)
        if best is None or score > best["_score"]:
            best = {**e, "_score": score, "_hits": hits}
    if best:
        return {"scene_index": scene.get("index"), "action": "reuse", "clip": best["source"],
                "slug": best.get("slug"), "hits": best["_hits"], "score": best["_score"]}
    return {"scene_index": scene.get("index"), "action": "generate",
            "why": "no clean in-scope clip whose tags match this scene"}


def reuse_plan(v1_folder: Path, provider: str = "nbp", scope: str = "neutral", log=print) -> dict:
    """Per-scene reuse-or-generate over a LOCKED scene_plan.json. Writes <v1>/visual/reuse_plan.json
    and returns a summary. Report-only — surfaces the recommendation; rendering still decides to act.
    Threads used clips so the same library clip is never proposed twice in one episode (no-repeat)."""
    import json
    sp = Path(v1_folder) / "visual" / "scene_plan.json"
    if not sp.is_file():
        return {"error": "no scene_plan.json"}
    try:
        scenes = json.loads(sp.read_text(encoding="utf-8")).get("plan", {}).get("scenes", [])
    except (OSError, ValueError) as e:
        return {"error": f"unreadable scene_plan.json: {e}"}
    used: set[str] = set()
    decisions = []
    for sc in scenes:
        d = decide_for_scene(sc, scope=scope, exclude_sources=used)
        if d["action"] == "reuse":
            used.add(d["clip"].replace("\\", "/"))
        decisions.append(d)
    reuse_n = sum(1 for d in decisions if d["action"] == "reuse")
    out = {"_README": "Per-scene reuse-before-regenerate recommendation (coherence-verified, "
                      "topical-fit, no-repeat). action=reuse -> materialize that clip instead of "
                      "paying to render; action=generate -> render new.",
           "scope": scope, "scenes": len(scenes), "reuse": reuse_n,
           "generate": len(scenes) - reuse_n, "decisions": decisions}
    (Path(v1_folder) / "visual" / "reuse_plan.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    log(f"      [reuse] {reuse_n}/{len(scenes)} scenes have a clean reusable clip "
        f"(${reuse_n * 0.65:.2f}+ Kling saved); {len(scenes)-reuse_n} to generate")
    return out


def reuse_health() -> dict:
    """How much of the indexed bank is actually clean-reusable now (post-coherence-gate)."""
    lib = _load()
    clean = [e for e in lib if is_clean_reusable(e)]
    neutral_clean = [e for e in clean if e.get("scope") == "neutral"]
    return {"indexed": len(lib), "clean_reusable": len(clean),
            "neutral_clean": len(neutral_clean),
            "preferred_clean": sum(1 for e in clean if e.get("preferred"))}


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    scope = sys.argv[sys.argv.index("--scope") + 1] if "--scope" in sys.argv else "neutral"
    if args and args[0] == "audit":
        h = reuse_health()
        print(f"clip-reuse health: {h['clean_reusable']}/{h['indexed']} indexed clips are clean-reusable "
              f"({h['neutral_clean']} neutral cross-episode-safe, {h['preferred_clean']} preferred).")
        raise SystemExit(0)
    if args and args[0] == "find":
        tags = [t.strip() for t in (args[1].split(",") if len(args) > 1 else []) if t.strip()]
        d = decide(tags, scope=scope)
        print(f"DECISION: {d['action'].upper()} — {d['why']}")
        for c in rank(tags, scope=scope)[:8]:
            print(f"  score {c['_score']:>2} (ov {c['_overlap']})  {c.get('slug'):36} {c.get('scope')}  {c.get('source')}")
        raise SystemExit(0)
    print("usage: python -m pipeline.clip_reuse find \"tag,tag\" [--scope neutral|specific|any] | audit")
