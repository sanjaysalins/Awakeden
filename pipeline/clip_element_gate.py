"""CLIP ELEMENT GATE (INV-25) — the post-animation teeth: catch a clip that INVENTED
something not in the still's locked element manifest (a gem on a wound, an extra figure,
a garbled titulus — the 2026-06-18 bake-off 'BINTX' defect).

NOT object-class set-math (the repo has no detector; the red-team killed that framing). It is
a calibrated VISION JUDGMENT, default-PASS, fail-closed only on a CLEAR foreign object:

  per frame, vision answers ONE question (the prompt below). A frame FAILs only on a clear
  object/figure/text NOT described by the manifest's verified labels. Unsure -> PASS.

Determinism (the INV-23 lesson — single-pass LLM verdicts are noisy):
  - votes pool BY FRAME CONTENT HASH, so byte-identical frames share one verdict.
  - clip verdict = ANY-FAIL across frames (a foreign object in any frame fails the clip).
  - CALIBRATE against blind human labels before enabling as a hard gate (default-PASS until then).

The vision look itself is serviced by the agent (LLM_PROVIDER=agent) or a Vision call; this
module is the deterministic scaffolding (frames, aggregation, sidecar, calibration scoring).

Run:  .venv\\Scripts\\python.exe -m pipeline.clip_element_gate record "<mp4>" 1|0 "foreign;objects"
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

from . import element_manifest


def prompt_for(labels: list[str]) -> str:
    """The single fail-closed question asked per frame."""
    listing = "; ".join(labels) if labels else "(none declared)"
    return (
        "This is one frame of an animated clip made from a single Baroque oil painting.\n"
        f"The painting's LOCKED elements are: {listing}.\n"
        "List anything in THIS frame that is a distinct object, figure, or text NOT described "
        "by that list — specifically a gem/jewel, an extra person/figure, legible or garbled "
        "lettering/inscription/titulus, or a modern item. ALSO fail an IMPOSSIBLE/UNGROUNDED "
        "body: a figure cut off at the chest/waist that appears to FLOAT with no grounded body, "
        "a detached or floating head/limb, or a giant-head/tiny-body proportion (F4). ALSO fail an "
        "obvious ANACHRONISM in dress/items — 1st-century Judea had NONE of these: GLOVES, a "
        "suit/blazer/jacket with lapels, buttons or zippers, eyeglasses, a wristwatch, or modern "
        "shoes (period figures wear robes/tunics + sandals or bare feet).\n"
        "If you find a CLEAR foreign object/figure/text/floating-body -> verdict FAIL. If only the listed "
        "elements and their natural paint detail (brushwork, shadow, craquelure) are present "
        "-> verdict PASS. When unsure, PASS (default-PASS)."
    )


def _sidecar(mp4: Path) -> Path:
    return Path(mp4).with_suffix(Path(mp4).suffix + ".elementgate.json")


def aggregate_votes(votes: list[dict]) -> tuple[bool, list[str], bool]:
    """Pure aggregation. votes = [{"verdict":"pass"|"fail"|"unsure", "foreign":[...]}].
    Returns (passed, foreign_union, split). ANY-FAIL + default-PASS (unsure==pass).
    No votes -> UNVERIFIED (passed False) handled by the caller."""
    verdicts = [str(v.get("verdict", "unsure")).lower() for v in votes]
    foreign = sorted({f for v in votes for f in (v.get("foreign") or [])})
    passed = not any(v == "fail" for v in verdicts)            # default-PASS; any fail fails
    split = len({v for v in verdicts if v in ("pass", "fail")}) > 1
    return passed, foreign, split


def _hash_pool(frame_votes: list[dict]) -> list[dict]:
    """Collapse votes on byte-identical frames to one verdict (determinism by construction).
    frame_votes = [{"frame_sha":..., "verdict":..., "foreign":[...]}]."""
    by_hash: dict[str, dict] = {}
    for v in frame_votes:
        h = v.get("frame_sha") or ""
        if h and h in by_hash:
            # any-fail within a bucket
            if str(v.get("verdict")).lower() == "fail":
                by_hash[h] = v
        else:
            by_hash[h or id(v)] = v
    return list(by_hash.values())


def frame_sha(frame: Path) -> str:
    return hashlib.sha256(Path(frame).read_bytes()).hexdigest()


def record_verdict(mp4: Path, passed: bool, foreign: list | None = None,
                   note: str = "", audited: bool = True, split: bool = False) -> Path:
    """Fail-closed element-gate sidecar. audited=False -> always UNVERIFIED (usage-cap hole)."""
    sc = _sidecar(mp4)
    sc.write_text(json.dumps({
        "audited": bool(audited),
        "passed": bool(audited and passed),
        "foreign": foreign or [],
        "split": bool(split),
        "note": note,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    return sc


def record_from_frame_votes(mp4: Path, frame_votes: list[dict], note: str = "") -> Path:
    """Pool frame votes by content hash, aggregate any-fail/default-pass, write the sidecar."""
    pooled = _hash_pool(frame_votes)
    passed, foreign, split = aggregate_votes(pooled)
    return record_verdict(mp4, passed, foreign=foreign, split=split,
                          note=note or f"{len(pooled)} unique frame(s), any-fail/default-pass")


def is_verified(mp4: Path) -> bool:
    sc = _sidecar(mp4)
    if not sc.exists():
        return False
    try:
        d = json.loads(sc.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return bool(d.get("audited") and d.get("passed"))


def is_failed(mp4: Path) -> bool:
    """True ONLY when a sidecar records an audited FAIL. A MISSING sidecar is NOT a fail —
    JIT reuse gating must gate-then-decide (default-PASS on missing), never auto-exclude the
    whole un-swept bank (the trap clip_reuse already warns about for clip_qc)."""
    sc = _sidecar(mp4)
    if not sc.exists():
        return False
    try:
        d = json.loads(sc.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return bool(d.get("audited") and not d.get("passed"))


def labels_for_clip(mp4: Path) -> list[str]:
    """The verified element labels the sibling still's manifest allows (the gate's allow-list)."""
    png = Path(mp4).with_suffix(".png")
    return element_manifest.verified_labels(png) if png.exists() else []


def calibrate(cases: list[dict]) -> dict:
    """Score the gate against blind truth labels (the locked calibration discipline).
    cases = [{"clip":name, "truth":"pass"|"fail", "gate":"pass"|"fail"}]. Returns
    precision/recall on the FAIL class + the confusion counts."""
    tp = sum(1 for c in cases if c["truth"] == "fail" and c["gate"] == "fail")
    fp = sum(1 for c in cases if c["truth"] == "pass" and c["gate"] == "fail")
    fn = sum(1 for c in cases if c["truth"] == "fail" and c["gate"] == "pass")
    tn = sum(1 for c in cases if c["truth"] == "pass" and c["gate"] == "pass")
    prec = tp / (tp + fp) if (tp + fp) else 1.0
    rec = tp / (tp + fn) if (tp + fn) else 1.0
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "precision": round(prec, 3), "recall": round(rec, 3),
            "discriminates": tp >= 1 and fp == 0 and fn == 0}


if __name__ == "__main__":
    import sys
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) >= 3 and args[0] == "record":
        mp4 = Path(args[1])
        passed = args[2] in ("1", "true", "pass", "PASS")
        foreign = [x.strip() for x in (args[3].split(";") if len(args) > 3 else []) if x.strip()]
        sc = record_verdict(mp4, passed, foreign=foreign)
        print(f"recorded {'PASS' if passed else 'FAIL'} -> {sc}")
        raise SystemExit(0)
    print("usage: python -m pipeline.clip_element_gate record <mp4> 1|0 \"foreign;objects\"")
