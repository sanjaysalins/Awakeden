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
    # Lock chokepoint: refuse to assemble a cut from an unlocked / stale narration
    # (a templated short already has narration.mp3 and would otherwise sail into the
    # cut un-verified — the multi-door bypass the panel flagged). Override: JITB_REQUIRE_LOCK=0.
    from pipeline import lock as _lock
    _lock.require_lock(v1_folder)

    clip_budget = clip_budget if clip_budget is not None else config.ASSEMBLY_CLIP_BUDGET
    reel = config.ASSEMBLY_REEL if reel is None else reel
    exclude = exclude or set()
    out_dir = H.assembly_dir(v1_folder)
    narration_mp3 = v1_folder / "narration.mp3"

    log("[A1] Building narration timeline from per-turn audio...")
    segments = T.build_timeline(v1_folder, log=log)

    # Beat board (Rule 3): forced-alignment → per-word times → clause-sized phrases the
    # matcher pins clips to. Falls back to section-level matching if alignment is
    # unavailable (e.g. key lacks the forced_alignment permission).
    beats = None
    if config.ASSEMBLY_BEAT_MATCH:
        log("[A1b] Forced-alignment + phrase board (beat-accurate matching)...")
        try:
            from pipeline import assembly_align as AL
            words = AL.align(v1_folder, log=log)
            beats = T.build_phrase_board(segments, words, log=log)
            T.print_phrase_board(beats, log=log)
        except SystemExit as e:
            log(f"      ! beat alignment unavailable — {e}")
            log("      ! FALLING BACK to section-level matching (set up forced-alignment "
                "for beat-accurate clip placement).")
            beats = None

    clips = T.load_clips(v1_folder, provider, exclude=exclude, log=log)
    if exclude:
        log(f"      (excluded {sorted(exclude)} from the cut)")
    if not clips:
        raise SystemExit(f"No rendered clips for provider '{provider}'. Run the visual stage first.")

    # Episode-fit safety net: drop clips that visibly tell ANOTHER story (foreign to this
    # narration), protecting the gospel-pivot/Christ clips. Behind the library gate; also
    # covers non-library episodes. Skipped when reusing a LOCKED plan (no re-match).
    if config.ASSEMBLY_EPISODE_FIT and (replan or _load_existing(out_dir) is None):
        narr_md = v1_folder / "narration.md"
        if narr_md.exists():
            flagged = E.flag_offtopic_clips(clips, narr_md.read_text(encoding="utf-8"), log=log)
            drop = {i for i, _why in flagged.items()
                    if i in {c.scene_index for c in clips} and not E._is_gospel_pivot(
                        next(c for c in clips if c.scene_index == i))}
            for i in sorted(drop):
                why = flagged[i]
                title = next(c.title for c in clips if c.scene_index == i)
                log(f"      [episode-fit] DROP #{i:02d} '{title}' — foreign to this episode: {why}")
            if drop:
                exclude = set(exclude) | drop
                clips = [c for c in clips if c.scene_index not in drop]
            kept_foreign = [i for i in flagged if i not in drop]
            if kept_foreign:
                log(f"      [episode-fit] kept {sorted(kept_foreign)} (gospel-pivot — protected; "
                    "review the image manually)")
    if not clips:
        raise SystemExit("Episode-fit dropped all clips — pool is off-topic; re-select the visual pool.")
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
        match_mode = "beat" if beats else "section"
        log(f"\n[A2] Jigsaw matching ({match_mode} mode, budget={clip_budget}, "
            f"hero_pref={hero_pref or 'auto'})...")
        plan = E.plan_edit(segments, clips, clip_budget=clip_budget,
                           thread_summary=thread, hero_pref=hero_pref, beats=beats, log=log)
        log(f"      reading: {plan.narration_reading[:120]}...")

        log("[A3] Self-review (panel + AS-G1..G9 deterministic + AS-G8 beat continuity)...")
        self_review = E.review_edit_plan(segments, clips, plan, beats=beats)
        log(f"      {self_review.overall} ({len(self_review.failed_gates)} FAIL)")
        while self_review.failed_gates and revisions < config.MAX_REVISIONS:
            revisions += 1
            log(f"      revising ({revisions}/{config.MAX_REVISIONS})...")
            plan = E.revise_edit_plan(segments, clips, plan, self_review,
                                      thread_summary=thread, beats=beats, log=log)
            self_review = E.review_edit_plan(segments, clips, plan, beats=beats)
            log(f"      {self_review.overall} ({len(self_review.failed_gates)} FAIL)")

        independent_review = None
        if config.ASSEMBLY_INDEPENDENT_REVIEW:
            log("[A4] INDEPENDENT red-team audit (authoritative)...")
            independent_review = E.independent_review_edit_plan(segments, clips, plan, beats=beats)
            log(f"      independent: {independent_review.overall} "
                f"({len(independent_review.failed_gates)} FAIL)")
            while independent_review.failed_gates and revisions < config.MAX_REVISIONS:
                revisions += 1
                log(f"      revising from independent ({revisions}/{config.MAX_REVISIONS})...")
                plan = E.revise_edit_plan(segments, clips, plan, independent_review,
                                          thread_summary=thread, beats=beats, log=log)
                independent_review = E.independent_review_edit_plan(segments, clips, plan, beats=beats)
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
