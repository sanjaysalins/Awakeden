"""IMG-COHERENT — whole-figure physical-plausibility verification (the fail-closed core).

See `v2/SPEC.md` §5 (INV-23). This module is the deterministic SCAFFOLDING of the gate:
the sidecar contract, the fail-closed verdict logic, and the hash binding. The vision judgement
(`coherence_gate.py`, a blind default-PASS F1-F5 look) records its verdict THROUGH `record_verdict`
here; the k-vote `aggregate` is the bulk-sweep / determinism path.

The live fail classes are F1-F5 (NOT FIT FOR USE on a clear defect; default-PASS otherwise):
  F1 modern/anachronism · F2 frame/border/split-screen · F3 broken face/grotesque expression ·
  F4 impossible anatomy (floating head/limb, through-object, giant head) · F5 dominant garbled text.

Fail-closed rules the red-team forced in:
  - `audited` is SEPARATE from `passed`. A skipped audit (e.g. Anthropic usage cap) writes
    audited=false -> UNVERIFIED, never a green light (closes the verify_image usage-cap hole).
  - `png_sha256` BINDS the verdict to the exact image. A silent in-place re-render leaves a
    stale sidecar; is_verified recomputes the hash and treats a mismatch as UNVERIFIED.
  - is_verified is the only gate: True ONLY when audited AND passed AND the hash matches.

Run:  .venv\\Scripts\\python.exe -m pipeline.coherence "<short folder>"   # status of every still
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

# The criteria the vision fan-out must satisfy (carried here so the gate prompt and the
# rule registry share one source of truth).
CRITERIA = (
    "A still is NOT FIT FOR USE only for a CLEAR, OBVIOUS defect (default to PASS otherwise):\n"
    "  F1 MODERN/ANACHRONISM: an obviously modern/out-of-period object, dress, hairstyle, "
    "flag/banner, or a glossy modern photo-portrait look.\n"
    "  F2 FRAME/BORDER: a picture-frame, wooden border, canvas edge, triptych side-panel, or "
    "split-screen (the image must be full-bleed).\n"
    "  F3 BROKEN FACE: a clearly melted/warped/asymmetric face, two merged faces, plainly "
    "malformed eyes (not merely looking up/away), or a grotesque/leering/unsettling expression.\n"
    "  F4 IMPOSSIBLE ANATOMY: a detached/FLOATING head or limb, a limb passing THROUGH a solid "
    "object, a giant-head/tiny-body proportion, an extra/missing limb, or an obviously bad hand.\n"
    "  F5 DOMINANT GARBLED TEXT: large gibberish lettering that DOMINATES the image as its "
    "subject (a small background scroll is fine).\n"
    "Suffering-Christ traits PASS: gaunt/sorrowful/upward-gaze faces, upright crucifixion, "
    "background scrolls. Default to PASS; fail only on an unmistakable F1-F5 defect."
)


def _sidecar(png: Path) -> Path:
    return png.with_suffix(png.suffix + ".coherence.json")


def png_sha256(png: Path) -> str:
    return hashlib.sha256(Path(png).read_bytes()).hexdigest()


def _write_sidecar(png: Path, *, audited: bool, passed: bool, png_sha256_val: str | None = None,
                   votes: list | None = None, n_votes: int | None = None, split: bool = False,
                   failed_dims: list | None = None, passes: dict | None = None,
                   fail_reasons: list | None = None, note: str = "") -> Path:
    """The single sidecar writer (shared by the single-shot and the ensemble paths) so both
    emit one schema. audited=False ALWAYS persists passed=False (closes the usage-cap hole)."""
    png = Path(png)
    sc = _sidecar(png)
    sha = png_sha256_val if png_sha256_val is not None else (png_sha256(png) if png.exists() else "")
    sc.write_text(
        json.dumps({
            "audited": bool(audited),
            "passed": bool(audited and passed),      # un-audited can never be passed
            "png_sha256": sha,
            "n_votes": n_votes if n_votes is not None else (1 if audited else 0),
            "split": bool(split),                    # votes disagreed -> noise surfaced
            "failed_dims": failed_dims or [],         # union of F1..F5 that failed
            "passes": passes or {},
            "fail_reasons": fail_reasons or [],
            "votes": votes or [],
            "note": note,
        }, ensure_ascii=False, indent=1),
        encoding="utf-8",
    )
    return sc


def record_verdict(
    png: Path,
    *,
    audited: bool,
    passed: bool,
    passes: dict | None = None,
    fail_reasons: list | None = None,
    note: str = "",
) -> Path:
    """Single-shot verdict writer (production audit_still path / a skip).

    audited=False (e.g. usage cap / no look taken) ALWAYS yields an UNVERIFIED sidecar even
    if passed is mistakenly True. The PNG hash is stamped so a later re-render busts it."""
    return _write_sidecar(png, audited=audited, passed=passed, passes=passes,
                          fail_reasons=fail_reasons, note=note)


def is_verified(png: Path) -> bool:
    """A still is coherence-verified ONLY if a sidecar exists AND audited AND passed AND its
    png_sha256 matches the current file (fail-closed on every missing/false/mismatch)."""
    png = Path(png)
    sc = _sidecar(png)
    if not sc.exists() or not png.exists():
        return False
    try:
        d = json.loads(sc.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    if not (d.get("audited") and d.get("passed")):
        return False
    recorded = d.get("png_sha256") or ""
    return bool(recorded) and recorded == png_sha256(png)


def verdict_reason(png: Path) -> str:
    """Human-readable why for status output."""
    png = Path(png)
    sc = _sidecar(png)
    if not sc.exists():
        return "UNVERIFIED (no coherence sidecar)"
    try:
        d = json.loads(sc.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return "BAD-SIDECAR"
    if not d.get("audited"):
        return "UNVERIFIED (audit skipped — no look taken)"
    if not d.get("passed"):
        return f"FAIL ({', '.join(d.get('fail_reasons') or []) or 'see sidecar'})"
    if (d.get("png_sha256") or "") != (png_sha256(png) if png.exists() else ""):
        return "STALE (image changed since verdict — re-audit)"
    return "PASS"


# ---------------------------------------------------------------- ensemble voting
# Single-pass LLM verdicts are non-deterministic — byte-identical stills got OPPOSITE
# verdicts (proven). Two fixes:
#   1. record_vote(): each independent look writes its OWN vote file (no concurrent-write race).
#   2. aggregate(): pools votes BY CONTENT HASH, so byte-identical images share ONE consensus
#      (deterministic for identical input, by construction), and uses ANY-FAIL (fail-closed):
#      a still passes only if EVERY vote passed. Disagreement is recorded as split=true (the
#      noise made visible) rather than silently resolved.

def _vote_path(png: Path, idx: int) -> Path:
    return png.with_name(f"{png.name}.vote.{idx}.json")


def record_vote(png: Path, idx: int, *, passed: bool, dims_failed: list | None = None,
                reasons: list | None = None) -> Path:
    """One independent look's vote. Distinct file per idx -> safe under parallel agents."""
    png = Path(png)
    vp = _vote_path(png, idx)
    vp.write_text(json.dumps({"passed": bool(passed),
                              "dims_failed": dims_failed or [],
                              "reasons": reasons or []}, ensure_ascii=False), encoding="utf-8")
    return vp


def _read_votes(png: Path) -> list[dict]:
    out = []
    for vp in sorted(Path(png).parent.glob(f"{Path(png).name}.vote.*.json")):
        try:
            out.append(json.loads(vp.read_text(encoding="utf-8")))
        except (OSError, ValueError):
            continue
    return out


def aggregate(stills: list[Path]) -> dict:
    """Pool votes BY CONTENT HASH and write a consensus sidecar for every still.

    - consensus passed = ALL votes passed (any-fail, fail-closed). No votes -> unaudited.
    - byte-identical stills share the same hash bucket -> identical consensus (deterministic).
    - split=true when votes within a bucket disagree (noise surfaced for human review).
    Returns stats incl. any hash bucket whose written sidecars somehow disagree (must be 0)."""
    buckets: dict[str, list[Path]] = {}
    for p in stills:
        p = Path(p)
        if p.exists():
            buckets.setdefault(png_sha256(p), []).append(p)

    stats = {"stills": 0, "audited": 0, "passed": 0, "failed": 0, "split": 0,
             "unaudited": 0, "inconsistent_buckets": 0}
    for sha, members in buckets.items():
        votes: list[dict] = []
        for m in members:
            votes += _read_votes(m)
        stats["stills"] += len(members)
        if not votes:
            for m in members:
                record_verdict(m, audited=False, passed=False, note="no votes recorded")
                stats["unaudited"] += 1
            continue
        passed = all(v.get("passed") for v in votes)
        split = len({bool(v.get("passed")) for v in votes}) > 1
        failed_dims = sorted({d for v in votes for d in (v.get("dims_failed") or [])})
        reasons = [r for v in votes if not v.get("passed") for r in (v.get("reasons") or [])]
        verdicts = set()
        for m in members:
            _write_sidecar(m, audited=True, passed=passed, png_sha256_val=sha,
                           votes=votes, n_votes=len(votes), split=split,
                           failed_dims=failed_dims, fail_reasons=reasons,
                           note=f"ensemble of {len(votes)} vote(s), any-fail")
            verdicts.add(passed)
            stats["audited"] += 1
            stats["passed" if passed else "failed"] += 1
            if split:
                stats["split"] += 1
        if len(verdicts) > 1:                       # impossible by construction — guardrail
            stats["inconsistent_buckets"] += 1
    return stats


def copy_verdict(src_png: Path, dst_png: Path) -> bool:
    """Propagate a REAL source coherence verdict onto a reused/copied still (INV-24: copy a
    real sidecar, never fabricate one). Returns True if a real verdict was copied; False if the
    source had none (dst is then left UNVERIFIED — the reuse helper must not invent a pass)."""
    src_sc = _sidecar(Path(src_png))
    if not src_sc.exists():
        return False
    try:
        d = json.loads(src_sc.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    # re-stamp with the destination's own hash so the binding stays valid after the copy
    record_verdict(
        Path(dst_png),
        audited=bool(d.get("audited")),
        passed=bool(d.get("passed")),
        passes=d.get("passes"),
        fail_reasons=d.get("fail_reasons"),
        note=f"copied coherence verdict from {Path(src_png).name}",
    )
    return True


def clear_sidecars(png: Path) -> None:
    """On rebuild, remove ALL stale verdict sidecars for a stem so an overwritten image cannot
    ride an old judgement (idempotence/staleness fix)."""
    png = Path(png)
    stem = png.with_suffix("")  # strips .png
    for cand in (
        png.with_suffix(png.suffix + ".audit.json"),      # <stem>.png.audit.json
        png.with_suffix(png.suffix + ".coherence.json"),  # <stem>.png.coherence.json
        Path(str(stem) + ".mp4.clipqc.json"),             # the sibling clip's QC verdict
    ):
        if cand.exists():
            cand.unlink()


def short_status(short_folder: Path, provider: str = "nbp") -> list[dict]:
    nbp = Path(short_folder) / "visual" / provider
    rows = []
    for png in sorted(nbp.glob("*.png")):
        rows.append({"still": png.name, "state": verdict_reason(png),
                     "verified": is_verified(png)})
    return rows


def sweep_pool() -> list[Path]:
    """Every still in the audit pool (shorts/pilots render dirs + the libraries)."""
    repo = Path(__file__).resolve().parent.parent
    out: list[Path] = []
    for base in ("longform", "v2/pilot"):
        for p in (repo / base).rglob("*.png"):
            s = str(p).replace("\\", "/")
            if "/visual/" not in s:
                continue
            if any(t in s for t in ("_qc", "_old", "_rejected", "_clipqc", "/refs/", "/_audit")):
                continue
            out.append(p)
    for base in ("image_library", "_library"):
        for p in (repo / base).rglob("*.png"):
            if not any(t in str(p).replace("\\", "/") for t in ("_qc", "/refs/")):
                out.append(p)
    return sorted(set(out))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    # record mode (used by the fan-out audit agents):
    #   python -m pipeline.coherence record "<png>" 1|0 "reason a;reason b"
    if args and args[0] == "record":
        png = Path(args[1])
        passed = args[2] in ("1", "true", "pass", "PASS")
        reasons = [r.strip() for r in (args[3].split(";") if len(args) > 3 else []) if r.strip()]
        sc = record_verdict(png, audited=True, passed=passed, fail_reasons=reasons)
        print(f"recorded {'PASS' if passed else 'FAIL'} -> {sc}")
        raise SystemExit(0)
    # ensemble vote (one independent look):
    #   python -m pipeline.coherence vote "<png>" <idx> 1|0 "reasons;..." "F1,F4"
    if args and args[0] == "vote":
        png = Path(args[1]); idx = int(args[2])
        passed = args[3] in ("1", "true", "pass", "PASS")
        reasons = [r.strip() for r in (args[4].split(";") if len(args) > 4 else []) if r.strip()]
        dims = [d.strip() for d in (args[5].split(",") if len(args) > 5 else []) if d.strip()]
        vp = record_vote(png, idx, passed=passed, dims_failed=dims, reasons=reasons)
        print(f"vote {idx} {'PASS' if passed else 'FAIL'} -> {vp}")
        raise SystemExit(0)
    # aggregate all votes -> consensus sidecars (hash-shared, any-fail):
    #   python -m pipeline.coherence aggregate
    if args and args[0] == "aggregate":
        st = aggregate(sweep_pool())
        print(f"aggregated: {st['audited']} audited ({st['passed']} pass / {st['failed']} fail), "
              f"{st['split']} split-vote, {st['unaudited']} unaudited, "
              f"{st['inconsistent_buckets']} inconsistent hash-buckets (must be 0).")
        raise SystemExit(0)
    if not args:
        print("usage: python -m pipeline.coherence <short folder> | record <png> 1|0 \"reasons\" "
              "| vote <png> <idx> 1|0 \"reasons\" \"F1,F4\" | aggregate")
        raise SystemExit(2)
    rows = short_status(Path(args[0]))
    ok = sum(1 for r in rows if r["verified"])
    for r in rows:
        print(f"  [{'PASS' if r['verified'] else 'BLOCK':>5}] {r['still']:40} {r['state']}")
    print(f"\n{ok}/{len(rows)} stills coherence-verified.\n\nCRITERIA:\n{CRITERIA}")
