"""Visual stage orchestrator: load a locked narration v1 folder, run the
scene-planning pipeline (discover -> review -> independent -> revise loop ->
paper_cohesion), and hand off paper artifacts.

Phase B (render) and Phase C (animate) are added in V5 / V8; for V3 the runner
stops after paper_cohesion regardless of `--no-render` etc.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import config
from pipeline import scripture, visual_engine, visual_handoff, visual_render
from pipeline.models import Beat, Draft, Thread
from pipeline.series import Episode, Series, get_series
from pipeline.visual_models import (
    CohesionAudit,
    ImageAudit,
    Scene,
    ScenePlan,
    ScenePlanReview,
)


@dataclass
class VisualRunResult:
    folder: Path                      # the v1/visual/ output folder
    plan: ScenePlan
    self_review: ScenePlanReview
    independent_review: ScenePlanReview | None
    paper_cohesion: CohesionAudit
    revisions_used: int
    rendered: list[tuple[Scene, Path, ImageAudit]] = None     # filled by Phase B
    provider_used: str = ""


# --------------------------------------------------------------------------
# Reload helpers — reconstruct Draft / Thread / Series / Episode from the
# narration.creation.json that text_handoff already wrote.
# --------------------------------------------------------------------------
def _load_creation(v1_folder: Path) -> dict:
    path = v1_folder / "narration.creation.json"
    if not path.exists():
        raise SystemExit(
            f"Missing narration.creation.json at {path}. "
            "Run the text pipeline first (cli.py)."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def _draft_from_dict(d: dict) -> Draft:
    """The text engine's Draft.from_json accepts the same shape asdict(draft)
    produced — beats are an array of {id, text} dicts."""
    return Draft.from_json(d)


def _thread_from_creation_dict(d: dict | None) -> Thread | None:
    """The creation.json stores `thread` as `asdict(Thread)` — flat fields
    plus a candidates list. Thread.from_json expects the discover_thread JSON
    shape (candidates + chosen_index), so we rehydrate manually."""
    if not d or not d.get("thread"):
        return None
    from pipeline.models import ThreadCandidate
    candidates = [
        ThreadCandidate(
            thread=str(c.get("thread", "")).strip(),
            lever=str(c.get("lever", "")).strip(),
            anchor_ref=str(c.get("anchor_ref", "")).strip(),
            anchor_detail=str(c.get("anchor_detail", "")).strip(),
            why_fresh=str(c.get("why_fresh", "")).strip(),
            gospel_landing=str(c.get("gospel_landing", "")).strip(),
        )
        for c in (d.get("candidates") or [])
        if str(c.get("thread", "")).strip()
    ]
    return Thread(
        thread=str(d.get("thread", "")).strip(),
        lever=str(d.get("lever", "")).strip(),
        anchor_ref=str(d.get("anchor_ref", "")).strip(),
        anchor_detail=str(d.get("anchor_detail", "")).strip(),
        why_fresh=str(d.get("why_fresh", "")).strip(),
        gospel_landing=str(d.get("gospel_landing", "")).strip(),
        rationale=str(d.get("rationale", "")).strip(),
        candidates=candidates,
    )


def _episode_from_creation(d: dict) -> Episode:
    """The creation.json's `episode` block only stores title + primary_ref. We
    populate refs and theme with sensible empties — the scene planner gets
    the wider passage separately, so the episode block is mainly cosmetic."""
    return Episode(
        title=str(d.get("title", "")).strip() or "(untitled)",
        primary_ref=str(d.get("primary_ref", "")).strip(),
        refs=[str(d.get("primary_ref", "")).strip()] if d.get("primary_ref") else [],
        theme="",
    )


def _series_from_creation(d: dict) -> Series:
    """Look up the full Series object from data/series.json by id, so the
    scene planner sees brand / hook pattern / guardrails — same context the
    text generator had."""
    sid = str(d.get("id", "")).strip()
    if not sid:
        raise SystemExit("creation.json has no series id — cannot reconstruct.")
    return get_series(sid)


# --------------------------------------------------------------------------
# Phase A orchestrator
# --------------------------------------------------------------------------
def create_visuals(
    v1_folder: Path,
    provider: str = "",
    short_only: bool = True,
    animate: bool = True,
    plan_only: bool = False,
    kling_skip_audit: bool = False,        # forward to image_to_kling.py; True bypasses Stage A.5 audit gate (use when audit nit-picks per HANDOVER.md)
    replan: bool = False,                  # ignore an existing LOCKED scene_plan.json and regenerate (Part 2 cut-aware re-plan)
    log=print,
) -> VisualRunResult:
    """Run Phase A (paper scene plan + reviews + paper cohesion) end-to-end
    against an existing v1 narration folder. Phase B / C are gated behind
    later sequencing chunks."""
    creation = _load_creation(v1_folder)
    draft = _draft_from_dict(creation.get("draft", {}))
    thread = _thread_from_creation_dict(creation.get("thread"))
    series = _series_from_creation(creation.get("series", {}))
    episode = _episode_from_creation(creation.get("episode", {}))

    log(f"\n=== Visual stage — {episode.title}  ({episode.primary_ref}) ===")
    log(f"    series: {series.name}  ·  beats: {draft.beat_ids}  ·  thread: "
        + (thread.thread if thread else "(none)"))

    # Cut-aware planning (Part 2): when the audio timeline exists, feed it to the
    # planner so scenes map to spoken windows + it nominates a gospel-pivot hero and
    # ~2s inserts for tiny beats. Graceful when audio isn't rendered yet.
    timeline = None
    try:
        from pipeline import assembly_timing
        if (v1_folder / "_turns").exists():
            timeline = assembly_timing.build_timeline(v1_folder, log=lambda *_: None)
            log(f"    cut-aware: narration timeline built ({len(timeline)} sections)")
    except Exception as e:
        log(f"    (timeline unavailable — planning without cut context: {e})")

    # Idempotency: if a paper scene plan already exists at LOCKED, reuse it
    # instead of re-burning ~$3 of Opus on every invocation. Hardened in V9.
    # --replan bypasses reuse to regenerate (e.g. cut-aware re-plan).
    existing_plan_path = v1_folder / visual_handoff.VISUAL_SUBDIR / "scene_plan.json"
    reuse_payload: dict | None = None
    if existing_plan_path.exists() and not replan:
        try:
            existing = json.loads(existing_plan_path.read_text(encoding="utf-8"))
            if (existing.get("authoritative_overall", "").upper() == "LOCKED"
                    and existing.get("paper_cohesion", {}).get("passed")):
                reuse_payload = existing
        except Exception as e:
            log(f"      ! could not parse existing scene_plan.json ({e}); regenerating.")

    if reuse_payload is not None:
        log(f"[reuse] scene_plan.json LOCKED at {existing_plan_path} — skipping Phase A.")
        plan = ScenePlan.from_json(reuse_payload.get("plan", {}))
        self_review = ScenePlanReview.from_json(reuse_payload.get("self_review") or {})
        ind_doc = reuse_payload.get("independent_review")
        independent_review = (
            ScenePlanReview.from_json(ind_doc) if ind_doc else None
        )
        paper = CohesionAudit.from_json(reuse_payload.get("paper_cohesion") or {"scope": "paper"})
        folder = v1_folder / visual_handoff.VISUAL_SUBDIR
        return _run_phase_bc(
            v1_folder=v1_folder, folder=folder, plan=plan,
            self_review=self_review, independent_review=independent_review,
            paper=paper, revisions=0, provider=provider,
            short_only=short_only, animate=animate, plan_only=plan_only,
            kling_skip_audit=kling_skip_audit, log=log,
        )

    log("[V1/4] Fetching wider pericope...")
    passage = scripture.fetch_kjv_passage(episode.primary_ref, window=config.PASSAGE_WINDOW)
    if passage:
        log(f"      pericope: {len(passage.splitlines())} verses")
    else:
        log("      ! pericope unavailable — scene planner will work without it.")

    log("[V2/4] Discovering scenes (visual cliché blocklist + 4 levers + cut-aware)...")
    plan = visual_engine.discover_scenes(series, episode, draft, thread, passage, timeline=timeline)
    log(f"      {len(plan.scenes)} scenes  ·  {len(plan.candidates)} candidates  ·  short_priority {plan.short_priority}"
        + (f"  ·  hero_candidate #{plan.hero_candidate:02d}" if plan.hero_candidate else ""))

    log("[V3/4] Self-review (6 agents + 8 gates; deterministic SP-G2/G5/G8)...")
    self_review = visual_engine.review_scene_plan(
        series, episode, draft, plan, thread, passage, timeline=timeline,
    )
    log(f"      {self_review.overall}  ({len(self_review.failed_gates)} FAIL gate(s))")

    revisions = 0
    while self_review.failed_gates and revisions < config.MAX_REVISIONS:
        revisions += 1
        log(f"      revising (pass {revisions}/{config.MAX_REVISIONS})...")
        plan = visual_engine.revise_scene_plan(
            series, episode, draft, plan, self_review, thread, passage, timeline=timeline,
        )
        self_review = visual_engine.review_scene_plan(
            series, episode, draft, plan, thread, passage, timeline=timeline,
        )
        log(f"      {self_review.overall}  ({len(self_review.failed_gates)} FAIL gate(s))")

    review: ScenePlanReview = self_review
    independent_review: ScenePlanReview | None = None
    if config.VISUAL_INDEPENDENT_REVIEW:
        log("[V4/4] INDEPENDENT scene-plan audit (authoritative)...")
        independent_review = visual_engine.independent_review_scene_plan(
            series, episode, draft, plan, thread, passage, timeline=timeline,
        )
        log(f"      independent: {independent_review.overall}  "
            f"({len(independent_review.failed_gates)} FAIL gate(s))")
        while independent_review.failed_gates and revisions < config.MAX_REVISIONS:
            revisions += 1
            log(f"      revising from independent audit (pass {revisions}/{config.MAX_REVISIONS})...")
            plan = visual_engine.revise_scene_plan(
                series, episode, draft, plan, independent_review, thread, passage, timeline=timeline,
            )
            independent_review = visual_engine.independent_review_scene_plan(
                series, episode, draft, plan, thread, passage, timeline=timeline,
            )
            log(f"      independent: {independent_review.overall}  "
                f"({len(independent_review.failed_gates)} FAIL gate(s))")
        if independent_review.failed_gates:
            log("      ! independent audit still has FAIL gate(s) - see review report before rendering.")
        review = independent_review

    log("[paper cohesion] one Opus pass over narration + plan...")
    paper = visual_engine.paper_cohesion(series, episode, draft, plan, thread, passage)
    log(f"      paper cohesion: {'PASS' if paper.passed else 'FAIL'}"
        + (f" — conflict scenes: {paper.conflict_scenes}" if paper.conflict_scenes else ""))

    log("[handoff] writing paper artifacts...")
    folder = visual_handoff.write_visual_paper_artifacts(
        v1_folder, plan, self_review, independent_review, paper,
    )
    log(f"      {folder}")

    return _run_phase_bc(
        v1_folder=v1_folder, folder=folder, plan=plan,
        self_review=self_review, independent_review=independent_review,
        paper=paper, revisions=revisions, provider=provider,
        short_only=short_only, animate=animate, plan_only=plan_only,
        kling_skip_audit=kling_skip_audit, log=log,
    )


# --------------------------------------------------------------------------
# Phase B (render) + Phase C (animate — wired in V8) — shared by the fresh-
# Phase-A path and the idempotent reuse path.
# --------------------------------------------------------------------------
def _run_phase_bc(
    v1_folder: Path,
    folder: Path,
    plan: ScenePlan,
    self_review: ScenePlanReview,
    independent_review: ScenePlanReview | None,
    paper: CohesionAudit,
    revisions: int,
    provider: str,
    short_only: bool,
    animate: bool,
    plan_only: bool,
    kling_skip_audit: bool = False,
    log=print,
) -> VisualRunResult:
    rendered: list[tuple[Scene, Path, ImageAudit]] = []
    provider_used = ""

    if plan_only:
        log("\n(plan-only — stopping after paper artifacts.)")
        return VisualRunResult(
            folder=folder, plan=plan, self_review=self_review,
            independent_review=independent_review, paper_cohesion=paper,
            revisions_used=revisions, rendered=[], provider_used="",
        )

    if not paper.passed:
        log("\n! paper cohesion FAILED — refusing to render. Review the plan first.")
        return VisualRunResult(
            folder=folder, plan=plan, self_review=self_review,
            independent_review=independent_review, paper_cohesion=paper,
            revisions_used=revisions, rendered=[], provider_used="",
        )

    provider_obj = visual_render.get_provider(provider)
    provider_used = provider_obj.name
    render_dir = folder / provider_obj.name
    render_dir.mkdir(parents=True, exist_ok=True)

    scenes_to_render: list[Scene] = (
        plan.short_scenes() if short_only else plan.scenes
    )
    if not scenes_to_render:
        log("\n! no scenes selected for rendering (short_priority empty?).")
        return VisualRunResult(
            folder=folder, plan=plan, self_review=self_review,
            independent_review=independent_review, paper_cohesion=paper,
            revisions_used=revisions, rendered=[], provider_used=provider_used,
        )

    log(f"\n[render] {len(scenes_to_render)} scenes via '{provider_obj.name}' "
        f"-> {render_dir}")
    log(f"        max retries per image: {config.MAX_NBP_RETRIES}")
    for scene in scenes_to_render:
        png_path, audit = visual_render.render_scene(
            scene, provider_obj, render_dir,
            max_retries=config.MAX_NBP_RETRIES, log=log,
        )
        rendered.append((scene, png_path, audit))

    passed = sum(1 for _, _, a in rendered if a.passed)
    log(f"\n[render] complete: {passed}/{len(rendered)} passed content audit.")
    if passed < len(rendered):
        log("        ! some images failed audit; see <stem>.png.audit.json sidecars.")

    index_path = visual_handoff.write_review_index_html(
        v1_folder, provider_obj.name, plan=plan,
    )
    if index_path:
        log(f"[review] index.html written: {index_path}")

    if not animate:
        log("\n(--no-animate — stopping after Phase B.)")
    else:
        # Phase C — Kling animation via image_to_kling.py subprocess.
        log(f"\n--- Phase C — Kling animation via image_to_kling.py ---")
        if short_only:
            indices = [s.index for s in scenes_to_render]
        else:
            indices = None
        kling_code = visual_handoff.run_kling_pipeline(
            v1_folder, provider_obj.name,
            short_only_indices=indices,
            skip_audit=kling_skip_audit,
            log=log,
        )
        log(f"--- Kling exit code: {kling_code} ---")
        # Regenerate index.html so the .mp4 sidecars are visible alongside PNGs.
        try:
            visual_handoff.write_review_index_html(v1_folder, provider_obj.name, plan=plan)
        except Exception:
            pass

    return VisualRunResult(
        folder=folder, plan=plan, self_review=self_review,
        independent_review=independent_review, paper_cohesion=paper,
        revisions_used=revisions, rendered=rendered, provider_used=provider_used,
    )
