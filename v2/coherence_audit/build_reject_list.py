"""Consolidated REJECT LIST: merge user flags + machine audit + provenance + dedup canonical.

Per reject: who flagged it (user / audit / both), the defect dimensions, the concept slug, which
finished shorts used it (-> reassembly), its clip, and the ACTION:
  - reuse-canonical : a coherence-verified, non-flagged canonical exists for this concept -> $0 swap.
  - rebuild         : no clean copy -> a metered re-render (then re-animate + reassemble).

Re-runnable: picks up coherence sidecars (audit FAILs) whenever they exist.
Run: .venv\\Scripts\\python.exe v2\\coherence_audit\\build_reject_list.py
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))   # so `from pipeline import ...` works when run from anywhere


def _load(name: str, default):
    p = HERE / name
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _abs(rel: str) -> str:
    return str((ROOT / rel).resolve()).replace("\\", "/")


def _rel(ap: str) -> str:
    """Repo-relative path from a resolved absolute path — robust (no fragile string split)."""
    try:
        return str(Path(ap).resolve().relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return ap   # outside the repo — keep absolute rather than mangle


def _slug(rel: str) -> str:
    stem = Path(rel).stem
    parts = stem.split("_", 1)
    return parts[1] if len(parts) == 2 and parts[0].isdigit() else stem


# writing surfaces: per never-animate-writing, these must be REDESIGNED illegible or EXCLUDED
# from the cut — NOT rebuilt-and-animated (Kling re-garbles the lettering on the clip).
_WRITING = ("scroll", "titulus", "codex", "parchment", "lettering", "script", "inscription",
            "book", "tablet", "the-greek-word", "writing", "manuscript", "hebrew")


def _is_writing_scene(slug: str, reasons: list) -> bool:
    text = (slug + " " + " ".join(reasons)).lower()
    # only treat as a writing scene when the defect is the TEXT (not a frame/border on a normal scene)
    if any(w in text for w in _WRITING):
        return True
    return False


def build() -> dict:
    flagged = _load("flagged_bad.json", {}).get("flagged_bad", [])
    flagged_abs = {_abs(r) for r in flagged}
    prov = _load("provenance.json", {}).get("shorts", [])
    canon = _load("canonical_concepts.json", {}).get("canonical", {})

    # audit fails from coherence sidecars (present once the multidim sweep finishes)
    from pipeline import coherence
    audit_fail: dict[str, list] = {}
    for png in list((ROOT / "longform").rglob("*.png")) + list((ROOT / "v2/pilot").rglob("*.png")) \
            + list((ROOT / "image_library").rglob("*.png")) + list((ROOT / "_library").rglob("*.png")):
        sc = png.with_suffix(".png.coherence.json")
        if not sc.exists():
            continue
        try:
            d = json.loads(sc.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if d.get("audited") and not d.get("passed"):
            audit_fail[str(png.resolve()).replace("\\", "/")] = d.get("fail_reasons") or []

    # usage index: abs still path -> [finished shorts that used it]
    used_in: dict[str, list[str]] = {}
    for s in prov:
        for b in s.get("bad_stills_used", []):
            used_in.setdefault(_abs(b["still"]), []).append(s["short"])

    all_rejects = set(flagged_abs) | set(audit_fail)
    rejects = []
    for ap in sorted(all_rejects):
        rel = _rel(ap)
        slug = _slug(rel)
        reasons = audit_fail.get(ap, [])
        canon_rel = canon.get(slug)
        canon_abs = _abs(canon_rel) if canon_rel else None
        # a canonical is usable only if it exists, is coherence-verified, and is NOT itself flagged
        reuse_ok = bool(canon_abs and canon_abs != ap and canon_abs not in flagged_abs
                        and canon_abs not in audit_fail and coherence.is_verified(Path(canon_abs)))
        sources = []
        if ap in flagged_abs:
            sources.append("user")
        if ap in audit_fail:
            sources.append("audit")
        # ACTION routing (the red-team fix): writing scenes must NOT be rebuilt+animated.
        if _is_writing_scene(slug, reasons):
            action = "redesign-illegible-or-exclude"
        elif reuse_ok:
            action = "reuse-canonical"
        else:
            action = "rebuild"
        rejects.append({
            "still": rel,
            "concept": slug,
            "flagged_by": sources,
            "dims": reasons,
            "used_in_finished": [u.split("/shorts/")[-1] if "/shorts/" in u else u
                                 for u in used_in.get(ap, [])],
            "clip": str(Path(rel).with_suffix(".mp4")),
            "action": action,
            "canonical_reuse": canon_rel if reuse_ok else None,
        })

    rebuilds = [r for r in rejects if r["action"] == "rebuild"]
    reuses = [r for r in rejects if r["action"] == "reuse-canonical"]
    writing = [r for r in rejects if r["action"] == "redesign-illegible-or-exclude"]
    in_finished = [r for r in rejects if r["used_in_finished"]]
    report = {
        "_README": "Consolidated reject list. action=rebuild is metered (re-render+animate); "
                   "action=reuse-canonical is $0 ($0 swap to a verified twin); "
                   "action=redesign-illegible-or-exclude is a writing scene that must NOT be "
                   "rebuilt+animated (never-animate-writing) — show illegible marks or drop it.",
        "counts": {
            "total_rejects": len(rejects),
            "by_user": sum(1 for r in rejects if "user" in r["flagged_by"]),
            "by_audit": sum(1 for r in rejects if "audit" in r["flagged_by"]),
            "by_both": sum(1 for r in rejects if len(r["flagged_by"]) == 2),
            "rebuild": len(rebuilds),
            "reuse_canonical": len(reuses),
            "redesign_or_exclude": len(writing),
            "used_in_finished_cuts": len(in_finished),
        },
        "rejects": rejects,
    }
    (HERE / "reject_list.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


if __name__ == "__main__":
    rep = build()
    c = rep["counts"]
    print(f"REJECT LIST  ->  {HERE / 'reject_list.json'}\n")
    print(f"  total rejects ............. {c['total_rejects']}  (user {c['by_user']}, audit {c['by_audit']}, both {c['by_both']})")
    print(f"  -> rebuild (metered) ...... {c['rebuild']}")
    print(f"  -> reuse canonical ($0) ... {c['reuse_canonical']}")
    print(f"  -> redesign/exclude (text)  {c['redesign_or_exclude']}  (never-animate-writing)")
    print(f"  used in finished cuts ..... {c['used_in_finished_cuts']}  (force reassembly)")