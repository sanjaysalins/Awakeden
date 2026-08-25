"""swirls_episode.py -- ONE entry point for a Swirls of Life episode, instead
of "which script do I run" (render_the_X.py, assemble_book_v2.py,
assemble_ashes.py, ...). An episode's own episode.py exports PAGES (dict[str,
PageSpec]), COVERS (dict[str, CoverSpec]), and MANIFEST (EpisodeManifest);
this runner drives plan/still/animate/verify/assemble over them, with the
$0 gates (swirls_verify.py) run automatically at the points that matter --
and ENFORCED, not just computed: `still`/`animate`/`assemble` refuse to
spend or to declare success on a FAIL unless `_overrides.json` explicitly
excuses it (see swirls_verify.load_overrides/apply_overrides).

Usage:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode.py <episode_dir> plan
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode.py <episode_dir> still <id>
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode.py <episode_dir> animate <id>
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode.py <episode_dir> verify
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode.py <episode_dir> assemble [--score NAME]

<id> is a page id ("f01") or a cover side ("front"/"back"). Human QC steps
(eyeball at 1:1, ref crops, contact sheets, real playback) are unchanged --
this adds deterministic floors under them, it does not replace them.
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "test_the_cross"))

import swirls_assemble as sa  # noqa: E402
import swirls_verify as sv  # noqa: E402
from swirls_cover import render_cover_animation, render_cover_still  # noqa: E402
from swirls_page import render_animation, render_still  # noqa: E402
import build_srt  # noqa: E402
import swirls_upload_tracker  # noqa: E402


def _load_episode(episode_dir: Path):
    spec = importlib.util.spec_from_file_location("episode", episode_dir / "episode.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _model_tier_map(ep) -> dict[str, str]:
    m = {pid: p.model_tier for pid, p in ep.PAGES.items()}
    for side in ep.COVERS:
        m[side] = "veo3_1_lite"
    return m


def _clip_duration_map(ep) -> dict[str, int | None]:
    m = {pid: p.clip_duration for pid, p in ep.PAGES.items()}
    for side, cover in ep.COVERS.items():
        m[side] = cover.clip_duration
    return m


def _report(gates: list, episode_dir: Path) -> bool:
    """Apply overrides, print, return whether everything is spend/ship-safe
    (no un-overridden FAIL)."""
    gates = sv.apply_overrides(gates, episode_dir)
    ok = True
    for g in gates:
        print(f"[{g.verdict:11}] {g.gate}: {g.evidence}" + (f"  FIX: {g.fix}" if g.fix else ""))
        if g.verdict == "FAIL":
            ok = False
    return ok


def cmd_plan(ep) -> bool:
    plan = sa.plan_units(ep.MANIFEST)
    print(f"{'tag':8} {'mode':10} {'words':>6} {'slot':>8} {'native':>8}")
    for p in plan:
        native = f"{p['native']:.2f}s" if p["native"] is not None else "  n/a "
        print(f"{p['tag']:8} {p['mode']:10} {p['words']:>6} {p['slot']:>7.2f}s {native:>8}")

    gates = []
    gates += sv.sw_f1_freeze_budget(plan, _model_tier_map(ep), _clip_duration_map(ep))
    for side, cover in ep.COVERS.items():
        gates.append(sv.sw_l1_cover_lighting_contrast(cover))
        gates.append(sv.sw_l2_cover_text_lock(cover))
    gates.append(sv.sw_l3_panel_style_consistency(ep.MANIFEST.panel_style, ep.PAGES))
    all_specs = list(ep.PAGES.values()) + list(ep.COVERS.values())
    gates.append(sv.sw_l4_refs_exist(all_specs))
    unit_words = [u.words for u in ep.MANIFEST.units]
    gates.append(sv.sw_l5_word_count_parity(
        unit_words, sv.narration_word_count(ep.MANIFEST.episode_dir)))

    print("\n-- gates --")
    return _report(gates, ep.MANIFEST.episode_dir)


def cmd_still(ep, id_: str) -> bool:
    """ENFORCED 2026-08-23 (independent-review catch, codex): the original
    version called render_still()/render_cover_still() directly with no
    pre-spend lint pass at all -- SW-L1 (cover lighting) could FAIL and a
    defective cover would still render, only caught later by `plan` if
    someone remembered to re-run it. Now runs the relevant V0 lints first
    and refuses to spend on a FAIL (refs-exist was already a hard stop
    inside render_still/render_cover_still; this adds the cover-lighting/
    text-lock checks that weren't enforced anywhere before assemble time)."""
    if id_ in ep.PAGES:
        page = ep.PAGES[id_]
        gate = sv.sw_l4_refs_exist([page])
        if not _report([gate], ep.MANIFEST.episode_dir):
            return False
        out = ep.MANIFEST.episode_dir / f"{ep.MANIFEST.episode_dir.name}_{id_}_9x16.png"
        return render_still(page, out)
    if id_ in ep.COVERS:
        cover = ep.COVERS[id_]
        gates = [sv.sw_l1_cover_lighting_contrast(cover), sv.sw_l2_cover_text_lock(cover),
                 sv.sw_l4_refs_exist([cover])]
        if not _report(gates, ep.MANIFEST.episode_dir):
            return False
        out = ep.MANIFEST.episode_dir / f"{id_}_cover.png"
        return render_cover_still(cover, out)
    print(f"FAILED: {id_!r} is not a page id in PAGES or a side in COVERS")
    return False


def cmd_animate(ep, id_: str) -> bool:
    plan = sa.plan_units(ep.MANIFEST)
    freeze_gates = sv.apply_overrides(
        sv.sw_f1_freeze_budget(plan, _model_tier_map(ep), _clip_duration_map(ep)),
        ep.MANIFEST.episode_dir)
    gate = next((g for g in freeze_gates if g.gate == f"SW-F1[{id_}]"), None)
    if gate and gate.verdict == "FAIL":
        print(f"BLOCKED by {gate.gate}: {gate.evidence}\n  FIX: {gate.fix}")
        print("  (set the spec's clip_duration per the fix above, or add an entry to "
              "_overrides.json if you understand the tradeoff)")
        return False
    if id_ in ep.PAGES:
        page = ep.PAGES[id_]
        png = ep.MANIFEST.episode_dir / f"{ep.MANIFEST.episode_dir.name}_{id_}_9x16.png"
        mp4 = png.with_suffix(".mp4")
        return render_animation(page, png, mp4)
    if id_ in ep.COVERS:
        cover = ep.COVERS[id_]
        png = ep.MANIFEST.episode_dir / f"{id_}_cover.png"
        mp4 = png.with_suffix(".mp4")
        return render_cover_animation(cover, png, mp4)
    print(f"FAILED: {id_!r} is not a page id in PAGES or a side in COVERS")
    return False


def _still_path(ep, id_: str) -> Path:
    if id_ in ep.PAGES:
        return ep.MANIFEST.episode_dir / f"{ep.MANIFEST.episode_dir.name}_{id_}_9x16.png"
    return ep.MANIFEST.episode_dir / f"{id_}_cover.png"


def cmd_verify(ep) -> bool:
    ok = True
    for pid, page in ep.PAGES.items():
        png = _still_path(ep, pid)
        if not png.exists():
            print(f"[SKIP] {pid}: not rendered yet")
            continue
        audit = sv.audit_page_still(png, page)
        print(f"[{'PASS' if audit.passed else 'FAIL'}] {pid} image audit"
              + (f" -- {audit.issues}" if not audit.passed else ""))
        ok = ok and audit.passed
    for side, cover in ep.COVERS.items():
        png = _still_path(ep, side)
        if not png.exists():
            print(f"[SKIP] {side}: not rendered yet")
            continue
        audit = sv.audit_cover_still(png, cover)
        print(f"[{'PASS' if audit.passed else 'FAIL'}] {side} cover image audit"
              + (f" -- {audit.issues}" if not audit.passed else ""))
        ok = ok and audit.passed
    return ok


def cmd_assemble(ep, score_name: str) -> bool:
    """ENFORCED 2026-08-23 (independent-review catch, codex): the original
    version called sa.assemble() immediately and only evaluated A1-A4
    afterward -- a still with a FAILing or missing V2 audit never blocked
    assembly at all, contradicting the plan's own "a failing/missing audit
    blocks assemble" claim. Now runs V2 (via cmd_verify's logic) FIRST and
    refuses to spend the ffmpeg encode time on unaudited/failing stills."""
    all_ids = list(ep.PAGES) + list(ep.COVERS)
    missing_or_failing = []
    for id_ in all_ids:
        png = _still_path(ep, id_)
        if not png.exists():
            missing_or_failing.append(f"{id_} (not rendered)")
            continue
        spec = ep.PAGES.get(id_) or ep.COVERS.get(id_)
        audit = sv.audit_page_still(png, spec) if id_ in ep.PAGES else sv.audit_cover_still(png, spec)
        if not audit.passed:
            missing_or_failing.append(f"{id_} (audit FAIL: {audit.issues})")
    v2_gate = sv.GateResult(
        "SW-V2-gate", "FAIL" if missing_or_failing else "PASS",
        f"unaudited/failing stills: {missing_or_failing}" if missing_or_failing else
        f"all {len(all_ids)} stills have a passing V2 audit",
    )
    if not _report([v2_gate], ep.MANIFEST.episode_dir):
        return False

    result = sa.assemble(ep.MANIFEST, score_name)
    gates = [sv.sw_a1_duration_parity(result["out"])]
    gates += sv.sw_a2_unit_duration(result["units"])
    gates.append(sv.sw_a3_total_duration(result["final_duration"], result["narration_len"],
                                          ep.MANIFEST.outro_hold))
    ok = _report(gates, ep.MANIFEST.episode_dir)
    if ok:
        # AUTOMATED (user, 2026-08-25): a clean assemble means a real, current
        # cut exists, so the timestamped .srt and the tracker board should
        # exist too -- no separate manual step to remember per episode.
        try:
            build_srt.build(ep.MANIFEST.episode_dir)
        except Exception as e:
            print(f"[warn] .srt build failed (non-fatal, assemble itself still succeeded): {e}")
        try:
            swirls_upload_tracker.build()
        except Exception as e:
            print(f"[warn] upload tracker refresh failed (non-fatal): {e}")
    return ok


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("episode_dir", type=Path)
    parser.add_argument("command", choices=["plan", "still", "animate", "verify", "assemble"])
    parser.add_argument("id", nargs="?", default=None)
    parser.add_argument("--score", default="original")
    args = parser.parse_args()

    ep = _load_episode(args.episode_dir.resolve())

    if args.command == "plan":
        ok = cmd_plan(ep)
    elif args.command == "still":
        ok = cmd_still(ep, args.id)
    elif args.command == "animate":
        ok = cmd_animate(ep, args.id)
    elif args.command == "verify":
        ok = cmd_verify(ep)
    else:
        ok = cmd_assemble(ep, args.score)

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
