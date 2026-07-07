#!/usr/bin/env python
"""LAYER 3 — the ONE ship gate a finishing step must pass before it animates/assembles a piece,
plus the cross-piece shared-still tooling.

WHY this exists: the 84-flawed-stills problem (2026-07-04) happened because (a) pieces were rendered
by bespoke one-off scripts that never audited (0 sidecars), and (b) the reuse-bank stills are
BYTE-IDENTICAL copies across pieces, so one bad shared still = the same defect in 8-9 public shorts.

Standing process (enforced by this file + the render_lint gate):
  1. render a piece's stills through the grounded path (render_lint.autofix on the prompt first),
     NOT a bespoke render_*.py script;
  2. `--check <piece_visual_dir>`  -> composes the FAIL-CLOSED content gate (render_lint.verify) and
     the shared-still membership note; exit 0 only when every still is PASS;
  3. a piece is NOT "done" (may not animate/assemble) until --check is 0;
  4. when a SHARED still is re-rendered + PASSes, `--propagate <fixed.png>` pushes the fixed PNG +
     its PASS audit to every identical-slug copy across the cluster, so the fix lands everywhere and
     the audit is done ONCE.

  .venv\\Scripts\\python.exe ship_gate.py --check batches/cluster_01_cross/thirty_pieces_zech11/visual
  .venv\\Scripts\\python.exe ship_gate.py --shared                      # cross-piece shared-still map
  .venv\\Scripts\\python.exe ship_gate.py --propagate <fixed_still.png> # push a fixed shared still everywhere
"""
from __future__ import annotations
import argparse, hashlib, shutil, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from render_lint.verify import gate_dir, is_production_png, _sidecar_verdict  # reuse the authority

# where finished pieces live (piece -> its stills folder)
SCAN_ROOTS = [ROOT / "batches" / "cluster_01_cross"]
STILL_DIRNAMES = ("visual", "nbp", "visual_16x9_inked")


def _sha1(p: Path) -> str:
    return hashlib.sha1(p.read_bytes()).hexdigest()[:12]


def _piece_of(p: Path) -> str:
    """The piece name = the folder under a scan root (e.g. 'thirty_pieces_zech11')."""
    parts = p.parts
    for root in SCAN_ROOTS:
        rp = root.parts
        if parts[:len(rp)] == rp and len(parts) > len(rp):
            return parts[len(rp)]
    return p.parent.name


def all_production_stills() -> list[Path]:
    out = []
    for root in SCAN_ROOTS:
        if not root.exists():
            continue
        for p in root.rglob("*.png"):
            if is_production_png(p):
                out.append(p)
    return out


def shared_map() -> dict:
    """slug -> {hash: [pieces]} for slugs that appear in more than one piece."""
    by_slug: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for p in all_production_stills():
        by_slug[p.stem][_sha1(p)].append(_piece_of(p))
    return {slug: dict(h) for slug, h in by_slug.items()
            if sum(len(v) for v in h.values()) > 1}


def report_shared() -> None:
    m = shared_map()
    if not m:
        print("no stills are shared across pieces.")
        return
    print(f"=== SHARED STILLS across pieces ({len(m)} slugs) ===")
    print("(fix once -> --propagate to every copy; a still audited once covers all identical copies)\n")
    for slug in sorted(m):
        hashes = m[slug]
        total = sum(len(v) for v in hashes.values())
        if len(hashes) == 1:
            h, pieces = next(iter(hashes.items()))
            print(f"  {slug}  x{total} pieces  [identical {h}] -> TRUE SHARED, one fix propagates")
        else:
            print(f"  {slug}  x{total} pieces  [DRIFTED — {len(hashes)} versions] -> re-rendered copies, fix each:")
            for h, pieces in hashes.items():
                print(f"       {h}: {', '.join(sorted(pieces))}")


def report_check(folder: Path) -> int:
    folder = Path(folder)
    g = gate_dir(folder)
    print(f"=== SHIP GATE — {folder} ===")
    print(f"stills {g['total']}  |  PASS {len(g['pass'])}  FAIL {len(g['fail'])}  UNAUDITED {len(g['unaudited'])}")
    for n in g["fail"]:
        print(f"  X FAIL      {n}")
    for n in g["unaudited"]:
        print(f"  ? UNAUDITED {n}")
    # shared-still membership note: which of this piece's stills are copied elsewhere
    m = shared_map()
    here = {p.stem for p in folder.glob("*.png") if is_production_png(p)}
    shared_here = sorted(here & set(m))
    if shared_here:
        print("\n  shared with other pieces (a fix here should --propagate):")
        for slug in shared_here:
            total = sum(len(v) for v in m[slug].values())
            print(f"    {slug} (in {total} pieces)")
    ok = g["green"]
    print(f"\nSHIP GATE: {'GREEN - clear to animate/assemble' if ok else 'BLOCKED - not shippable'}")
    if not ok:
        print("  run:  .venv\\Scripts\\python.exe -m render_lint.verify --worklist " + str(folder))
    return 0 if ok else 1


def propagate(png: Path, force: bool = False) -> int:
    png = Path(png).resolve()
    if not png.exists():
        print(f"no such file: {png}"); return 1
    slug = png.stem
    verdict = _sidecar_verdict(png)
    if verdict != "PASS" and not force:
        print(f"REFUSED: {png.name} has no PASS audit (verdict={verdict}); audit it first, or pass --force.")
        return 1
    src_audit = png.with_suffix(".audit.json")
    targets = [p for p in all_production_stills() if p.stem == slug and p.resolve() != png]
    if not targets:
        print(f"{slug}: no other copies found — nothing to propagate.")
        return 0
    print(f"propagating fixed {slug} (verdict {verdict}) to {len(targets)} copy(ies):")
    for t in targets:
        shutil.copy2(png, t)
        note = "png"
        if src_audit.exists():
            shutil.copy2(src_audit, t.with_suffix(".audit.json"))
            note = "png+audit"
        print(f"  -> {_piece_of(t)}/{t.name}  ({note})")
    print("done. re-run --check on each affected piece to confirm GREEN.")
    return 0


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", help="a piece's stills folder -> composed FAIL-CLOSED ship gate")
    ap.add_argument("--shared", action="store_true", help="cross-piece shared-still map")
    ap.add_argument("--propagate", help="a fixed+PASSed still -> copy it (and its audit) to every identical-slug copy")
    ap.add_argument("--force", action="store_true", help="with --propagate: allow a non-PASS source")
    a = ap.parse_args()
    if a.check:
        sys.exit(report_check(Path(a.check)))
    elif a.shared:
        report_shared()
    elif a.propagate:
        sys.exit(propagate(Path(a.propagate), a.force))
    else:
        ap.error("pass --check <dir> / --shared / --propagate <png>")


if __name__ == "__main__":
    main()
