"""Human still-review GATE — a recurring quality gate that requires a human pass over a
short's stills before it ships (user request 2026-06-17).

The automated coherence gate (F1-F5) catches the OBVIOUS at scale; the human is authority on
the SUBTLE (faces, anachronism) it misses by design. This makes "I looked at all the stills"
a real, fail-closed sign-off rather than an honour-system habit:

  still_set_hash(folder, provider) : a hash binding the EXACT set of stills (name + bytes).
  sign_off(folder, provider)       : write <folder>/.stills_reviewed bound to that hash
                                     (after the human has reviewed stills_review.html).
  is_reviewed(folder, provider)    : True only if the token exists AND matches the current set
                                     — adding/replacing/removing ANY still busts the sign-off.
  require_review(folder, provider) : reports always; raises only when JITB_REQUIRE_STILL_REVIEW=1
                                     (rollout flag, OFF by default, same pattern as coherence).

Periodic POOL review: re-run v2/coherence_audit/build_review_page.py to regenerate the page,
eyeball it, then sign-off each short you ship.

Run: .venv\\Scripts\\python.exe -m pipeline.still_review "<short folder>"            # status
     .venv\\Scripts\\python.exe -m pipeline.still_review "<short folder>" --sign-off  # mark reviewed
"""
from __future__ import annotations
import hashlib
import json
import os
import sys
from pathlib import Path

from pipeline import coherence

TOKEN = ".stills_reviewed"


def _stills(folder: Path, provider: str) -> list[Path]:
    d = Path(folder) / "visual" / provider
    return sorted(d.glob("*.png")) if d.is_dir() else []


def still_set_hash(folder: Path, provider: str = "nbp") -> str:
    """Hash of the EXACT still set: each (filename, content-sha). Any add/remove/change busts it."""
    parts = [f"{p.name}:{coherence.png_sha256(p)}" for p in _stills(folder, provider)]
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()


def sign_off(folder: Path, provider: str = "nbp", note: str = "") -> Path:
    folder = Path(folder)
    stills = _stills(folder, provider)
    tok = folder / TOKEN
    tok.write_text(json.dumps({
        "version": 1, "provider": provider,
        "still_set_sha256": still_set_hash(folder, provider),
        "n_stills": len(stills), "note": note or "human-reviewed via stills_review.html",
    }, indent=2), encoding="utf-8")
    return tok


def is_reviewed(folder: Path, provider: str = "nbp") -> tuple[bool, str]:
    tok = Path(folder) / TOKEN
    if not tok.is_file():
        return (False, "no .stills_reviewed sign-off")
    try:
        d = json.loads(tok.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return (False, ".stills_reviewed unreadable")
    if d.get("still_set_sha256") != still_set_hash(folder, provider):
        return (False, "stale: stills changed since review — re-review + re-sign-off")
    return (True, f"reviewed ({d.get('n_stills')} stills)")


def require_review_enabled() -> bool:
    return os.getenv("JITB_REQUIRE_STILL_REVIEW", "0") not in ("0", "false", "no")


def require_review(folder: Path, provider: str = "nbp") -> None:
    """Report the review status; raise only when JITB_REQUIRE_STILL_REVIEW=1 (rollout)."""
    ok, why = is_reviewed(folder, provider)
    if ok:
        return
    print(f"  [still-review] {Path(folder).name}: NOT signed off — {why}")
    if not require_review_enabled():
        print("  [still-review] WARNING: JITB_REQUIRE_STILL_REVIEW is OFF (rollout) — not blocking. "
              "Regenerate stills_review.html, eyeball it, then: python -m pipeline.still_review "
              f"\"{folder}\" --sign-off")
        return
    raise PermissionError(
        f"REFUSING to ship {Path(folder).name}: stills not human-reviewed ({why}). Review "
        f"stills_review.html, then run:  python -m pipeline.still_review \"{folder}\" --sign-off")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print("usage: python -m pipeline.still_review <short folder> [--sign-off] [--provider nbp]")
        raise SystemExit(2)
    folder = Path(args[0])
    prov = args[args.index("--provider") + 1] if "--provider" in sys.argv else "nbp"
    if "--sign-off" in sys.argv:
        tok = sign_off(folder, prov)
        print(f"signed off {still_set_hash(folder, prov)[:12]} -> {tok}")
    else:
        ok, why = is_reviewed(folder, prov)
        print(f"[{'REVIEWED' if ok else 'PENDING'}] {folder.name} ({prov}): {why}")
