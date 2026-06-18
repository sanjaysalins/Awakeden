"""Generic reuse-swap for ANY short (generalizes the #03 one-off `do_reuse_swap.py`).

Substitute a clean catalogue clip into a short's scene slot, $0:
  - WRITE-ONCE backup of the old slot to <nbp>/_pre_reuse/ (never overwrites a real original),
  - copy the reused clip + still into the slot,
  - copy the source's REAL coherence verdict (never fabricate — INV-24),
  - lock an element manifest for the slot (elements from the source manifest if present, else minimal),
  - record an element-gate PASS (the caller must have looked / gated the candidate first).

Run:
  .venv\\Scripts\\python.exe -m pipeline.reuse_swap "<short>" --swap 08=<abs path to lib .mp4> [--swap ...]
"""
from __future__ import annotations
import argparse
import shutil
from pathlib import Path

from pipeline import element_manifest as M, clip_element_gate as G, coherence

ALL_PASS = {k: "pass" for k in M.PERIOD_REAL_KEYS}


def _slot_png(nbp: Path, scene: int) -> Path | None:
    hits = sorted(nbp.glob(f"{scene:02d}_*.png"))
    return hits[0] if hits else None


def _slot_png_or_create(nbp: Path, scene: int) -> Path | None:
    """Existing slot, else the path for a NEW slot named by the scene_plan's slug for this index
    (so the assembly — which looks for NN_<slug>.mp4 — will find the backfilled clip). Returns
    None only if the scene index isn't in the plan."""
    existing = _slot_png(nbp, scene)
    if existing:
        return existing
    sp = nbp.parent / "scene_plan.json"
    if not sp.exists():
        return None
    import json
    scenes = (json.loads(sp.read_text(encoding="utf-8")).get("plan", {}) or {}).get("scenes") or []
    slug = next((s.get("slug") for s in scenes if s.get("index") == scene), None)
    return nbp / f"{scene:02d}_{slug}.png" if slug else None


def swap(short: Path, scene: int, src_mp4: Path, provider: str = "nbp",
         elements: list | None = None, log=print) -> bool:
    nbp = Path(short) / "visual" / provider
    bak = nbp / "_pre_reuse"
    bak.mkdir(exist_ok=True)
    dst_png = _slot_png_or_create(nbp, scene)
    if dst_png is None:
        log(f"  !! no scene-{scene:02d} slot (not in {nbp}, and no scene_plan slug for it)")
        return False
    new_slot = not dst_png.exists()
    dst_mp4 = dst_png.with_suffix(".mp4")
    src_mp4 = Path(src_mp4)
    src_png = src_mp4.with_suffix(".png")
    if not src_mp4.exists() or not src_png.exists():
        log(f"  !! missing source {src_mp4}")
        return False

    # 0. FAIL-CLOSED BEFORE ANY MUTATION: a reused source must be coherence-verified (so the
    #    swap can copy a REAL verdict, never fabricate). Check up front so a refusal leaves the
    #    slot untouched — do NOT copy files first and bail after.
    if not coherence.is_verified(src_png):
        log(f"  !! scene {scene:02d}: source {src_png.name} is NOT coherence-verified — "
            f"refusing swap, slot left untouched. Re-audit the source first.")
        return False

    # 1. WRITE-ONCE backup (refuse to overwrite a real original on a re-run)
    for ext in (".png", ".mp4"):
        old = dst_png.with_suffix(ext)
        b = bak / old.name
        if old.exists() and not b.exists():
            shutil.copy2(old, b)
    # 2. clear stale sidecars so new content can't ride an old verdict, then substitute
    coherence.clear_sidecars(dst_png)
    shutil.copy2(src_png, dst_png)
    shutil.copy2(src_mp4, dst_mp4)
    # 3. copy the source's REAL coherence verdict (re-stamped to the dst hash) — never fabricate.
    #    FAIL-CLOSED: if the source had no real coherence verdict, do NOT lock the manifest or
    #    stamp an element-gate PASS (that would be a false green on an unverified still).
    copied = coherence.copy_verdict(src_png, dst_png)
    if not copied or not coherence.is_verified(dst_png):
        log(f"  !! scene {scene:02d}: source {src_png.name} has no real coherence verdict — "
            f"slot left UNVERIFIED (no lock, no element-gate PASS). Re-audit the source first.")
        return False
    # 4. element manifest: prefer the source's, else a minimal locked one
    src_manifest = M.read(src_png)
    els = elements or (src_manifest.get("elements") if src_manifest else None) or \
        [{"id": "full", "label": f"reused: {src_png.stem}"}]
    M.declare(dst_png, dst_png.stem, [{"id": e["id"], "label": e["label"]} for e in els],
              subject_type=(src_manifest or {}).get("subject_type", "hero"),
              role=(src_manifest or {}).get("role", "hero"))
    M.reconcile_and_lock(dst_png, verified_ids=[e["id"] for e in els], period_real=ALL_PASS,
                         note=f"reuse-swap from {src_mp4}")
    # 4b. RE-POINT the scene's macro_elements at the swapped still (these drive the HF gallery-tour
    #     cut-plan). Leaving the slot's OLD macro_elements made the animator hunt for elements not in
    #     the new image and crane off-subject (caught on #03 scene 12: a dawn-cross still still carried
    #     "David's pen on the scroll / lamp flame" so Kling craned off the cross into empty sky). Use
    #     the swapped still's VERIFIED element labels — the only things that are actually in it.
    labels = [e["label"] for e in els
              if e.get("label") and not str(e["label"]).startswith("reused:")][:4]
    if labels:
        sp = nbp.parent / "scene_plan.json"
        if sp.exists():
            import json as _j
            plan = _j.loads(sp.read_text(encoding="utf-8"))
            sc_list = (plan.get("plan", {}) or {}).get("scenes") or plan.get("scenes") or []
            for s in sc_list:
                if s.get("index") == scene:
                    s["macro_elements"] = labels
            sp.write_text(_j.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
            log(f"  scene {scene:02d} macro_elements re-pointed at swapped still: {labels}")
    # 5. element-gate PASS (caller gated the candidate by eye first)
    G.record_verdict(dst_mp4, True, note=f"reuse-gated clean from {src_png.name}")
    # 5b. write the verify_image audit sidecar too, so cli_visual's render idempotence
    #     ('exists and audit passed') SKIPS this reused slot instead of re-rendering over it.
    import json as _json
    dst_png.with_suffix(dst_png.suffix + ".audit.json").write_text(
        _json.dumps({"passed": True, "issues": [], "banned_token_hits": [],
                     "note": f"reuse from {src_png.name}"}), encoding="utf-8")
    log(f"  scene {scene:02d} <- {src_png.name}  coherence={coherence.is_verified(dst_png)} "
        f"manifest_locked={M.is_locked(dst_png)} elemgate={G.is_verified(dst_mp4)}")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("short")
    ap.add_argument("--provider", default="nbp")
    ap.add_argument("--swap", action="append", default=[],
                    help="scene=<abs path to library .mp4>  (repeatable)")
    a = ap.parse_args()
    short = Path(a.short)
    ok = 0
    for s in a.swap:
        scene_str, _, src = s.partition("=")
        if swap(short, int(scene_str), Path(src), provider=a.provider):
            ok += 1
    print(f"\n{ok}/{len(a.swap)} swaps done. Backups -> _pre_reuse/ (write-once). "
          f"Re-assemble with cli_assemble (the swapped slots now carry locked manifests + element-gate PASS).")


if __name__ == "__main__":
    main()
