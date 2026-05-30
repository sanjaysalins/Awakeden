"""Orchestrate the assembly stage: timeline -> jigsaw plan -> self/independent
review + revise -> render (cut + reel) -> Vision verify -> handoff. Idempotent
on a LOCKED edit_plan.json (mirrors visual_runner)."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import config
from pipeline import assembly_engine as E
from pipeline import assembly_handoff as H
from pipeline import assembly_render as R
from pipeline import assembly_timing as T
from pipeline.assembly_models import (
    AssemblyAudit,
    ClipAsset,
    EditPlan,
    EditPlanReview,
    NarrationSegment,
)


@dataclass
class AssemblyRunResult:
    plan: EditPlan
    self_review: EditPlanReview
    independent_review: EditPlanReview | None
    audit: AssemblyAudit | None
    viral_cut: Path | None
    reel: Path | None
    index_html: Path | None
    revisions_used: int


def _scene_hero_candidate(v1_folder: Path) -> int:
    """The hero the SCENE PLAN nominated (Part 2 cut-aware planning). Used as the
    default hero_pref; _pick_hero still enforces it must be a gospel-pivot."""
    p = v1_folder / "visual" / "scene_plan.json"
    if not p.exists():
        return 0
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
        return int((doc.get("plan", {}) or {}).get("hero_candidate", 0) or 0)
    except Exception:
        return 0


def _thread_summary(v1_folder: Path) -> str:
    creation = v1_folder / "narration.creation.json"
    if not creation.exists():
        return ""
    try:
        d = json.loads(creation.read_text(encoding="utf-8"))
        th = d.get("thread") or {}
        parts = [th.get("thread", ""), th.get("gospel_landing", "")]
        return " — ".join(p for p in parts if p).strip()
    except Exception:
        return ""


def _sanity_table(plan: EditPlan, clips_by_index: dict[int, ClipAsset], log=print) -> None:
    by_section: dict[str, list] = {}
    for s in plan.body_slots:
        by_section.setdefault(s.section, []).append(s)
    log("\n      --- SANITY TABLE (per section) ---")
    log(f"      {'section':<9} {'clips':>5} {'window':>8} {'avgslot':>8} {'avgspd':>7} {'trimmed':>8}")
    for sec, slots in by_section.items():
        window = sum(s.slot_duration_s for s in slots)
        avg_slot = window / len(slots)
        avg_spd = sum(s.speed_factor for s in slots) / len(slots)
        trimmed = sum(1 for s in slots if s.op == "speed+trim")
        log(f"      {sec:<9} {len(slots):>5} {window:>7.2f}s {avg_slot:>7.2f}s "
            f"{avg_spd:>6.2f}x {trimmed:>4}/{len(slots)}")
    body = plan.body_slots
    if body:
        avg = sum(s.speed_factor for s in body) / len(body)
        mx = max(s.speed_factor for s in body)
        log(f"      OVERALL: {len(body)} clips · avg {avg:.2f}x · max {mx:.2f}x")
        if avg > 2.0:
            log("      ! WARNING: avg speed > 2.0x on slow footage may STROBE. "
                "Consider a lower --clips budget.")


def _load_existing(out_dir: Path):
    plan_path = out_dir / "edit_plan.json"
    if not plan_path.exists():
        return None
    try:
        doc = json.loads(plan_path.read_text(encoding="utf-8"))
        if (doc.get("authoritative_overall", "").upper().strip() != "LOCKED"):
            return None
        plan = EditPlan.from_json(doc.get("plan", {}))
        self_review = EditPlanReview.from_json(doc.get("self_review") or {})
        ind = doc.get("independent_review")
        independent = EditPlanReview.from_json(ind) if ind else None
        audit = AssemblyAudit.from_json(doc["audit"]) if doc.get("audit") else None
        return plan, self_review, independent, audit
    except Exception:
        return None


def run_assembly(
    v1_folder: Path,
    provider: str = "hf",
    clip_budget: int | None = None,
    plan_only: bool = False,
    reel: bool | None = None,
    verify: bool = True,
    hero: int = 0,
    exclude: set[int] | None = None,
    rebuild: bool = False,
    replan: bool = False,
    log=print,
) -> AssemblyRunResult:
    clip_budget = clip_budget if clip_budget is not None else config.ASSEMBLY_CLIP_BUDGET
    reel = config.ASSEMBLY_REEL if reel is None else reel
    exclude = exclude or set()
    out_dir = H.assembly_dir(v1_folder)
    narration_mp3 = v1_folder / "narration.mp3"

    log("[A1] Building narration timeline from per-turn audio...")
    segments = T.build_timeline(v1_folder, log=log)
    clips = T.load_clips(v1_folder, provider, exclude=exclude, log=log)
    if exclude:
        log(f"      (excluded {sorted(exclude)} from the cut)")
    if not clips:
        raise SystemExit(f"No rendered clips for provider '{provider}'. Run the visual stage first.")
    clips_by_index = {c.scene_index: c for c in clips}
    T.print_board(segments, clips, log=log)

    # idempotence: reuse a LOCKED plan unless --replan
    revisions = 0
    reused = None if replan else _load_existing(out_dir)
    if reused is not None:
        # A reused plan is only valid if every clip it references is still in the
        # approved pool. If the user excluded a clip the plan used, we MUST replan
        # against the new set (otherwise render hits a missing clip).
        stale = [s.scene_index for s in reused[0].body_slots if s.scene_index not in clips_by_index]
        if stale:
            log(f"\n[replan] existing plan references now-excluded/missing clips {sorted(set(stale))} "
                "— replanning against the approved pool.")
            reused = None
    if reused is not None:
        plan, self_review, independent_review, audit = reused
        log(f"\n[reuse] edit_plan.json LOCKED — skipping planning. ({len(plan.body_slots)} clips)")
    else:
        thread = _thread_summary(v1_folder)
        hero_pref = hero or config.ASSEMBLY_HERO_SCENE or _scene_hero_candidate(v1_folder)
        log(f"\n[A2] Jigsaw matching (budget={clip_budget}, hero_pref={hero_pref or 'auto'})...")
        plan = E.plan_edit(segments, clips, clip_budget=clip_budget,
                           thread_summary=thread, hero_pref=hero_pref, log=log)
        log(f"      reading: {plan.narration_reading[:120]}...")

        log("[A3] Self-review (6 agents + AS-G1..G7 deterministic + AS-G8 thread)...")
        self_review = E.review_edit_plan(segments, clips, plan)
        log(f"      {self_review.overall} ({len(self_review.failed_gates)} FAIL)")
        while self_review.failed_gates and revisions < config.MAX_REVISIONS:
            revisions += 1
            log(f"      revising ({revisions}/{config.MAX_REVISIONS})...")
            plan = E.revise_edit_plan(segments, clips, plan, self_review, thread_summary=thread, log=log)
            self_review = E.review_edit_plan(segments, clips, plan)
            log(f"      {self_review.overall} ({len(self_review.failed_gates)} FAIL)")

        independent_review = None
        if config.ASSEMBLY_INDEPENDENT_REVIEW:
            log("[A4] INDEPENDENT red-team audit (authoritative)...")
            independent_review = E.independent_review_edit_plan(segments, clips, plan)
            log(f"      independent: {independent_review.overall} "
                f"({len(independent_review.failed_gates)} FAIL)")
            while independent_review.failed_gates and revisions < config.MAX_REVISIONS:
                revisions += 1
                log(f"      revising from independent ({revisions}/{config.MAX_REVISIONS})...")
                plan = E.revise_edit_plan(segments, clips, plan, independent_review, thread_summary=thread, log=log)
                independent_review = E.independent_review_edit_plan(segments, clips, plan)
                log(f"      independent: {independent_review.overall} "
                    f"({len(independent_review.failed_gates)} FAIL)")
        audit = None

    _sanity_table(plan, clips_by_index, log=log)

    # write paper artifacts (idempotent overwrite)
    log("\n[handoff] writing edit_plan.json + reviews + timeline + upstream_notes...")
    H.write_assembly_artifacts(v1_folder, segments, clips, plan,
                               self_review, independent_review, audit)

    if plan_only:
        log("[plan-only] stopping before render.")
        H.write_index_html(v1_folder, plan, clips, segments, provider, audit)
        return AssemblyRunResult(plan, self_review, independent_review, audit,
                                 None, None, None, revisions)

    # render
    log("\n[B1] Rendering the 60s viral cut...")
    viral_cut = R.render_cut(plan, clips_by_index, narration_mp3, out_dir,
                             rebuild=rebuild, log=log)
    reel_path = None
    if reel:
        log("[B2] Rendering the all-takes reel...")
        reel_path = R.render_reel(clips, out_dir, rebuild=rebuild, log=log)

    # verify
    if verify and not (reused and audit is not None and not rebuild):
        log("[B3] Vision-verifying each clip against its words...")
        audit = R.verify_cut(plan, segments, clips_by_index, viral_cut, out_dir, log=log)
        if "BLOCKING" in audit.notes:
            log("      " + "!" * 56)
            log(f"      ! {audit.notes}")
            log("      " + "!" * 56)
        else:
            log(f"      verify: {'PASS' if audit.passed_overall else 'flags'} — {audit.notes}")
        # rewrite artifacts now that we have the audit
        H.write_assembly_artifacts(v1_folder, segments, clips, plan,
                                   self_review, independent_review, audit)

    index_html = H.write_index_html(v1_folder, plan, clips, segments, provider, audit)
    log(f"\n[done] index: {index_html}")
    return AssemblyRunResult(plan, self_review, independent_review, audit,
                             viral_cut, reel_path, index_html, revisions)
