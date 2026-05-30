"""Single-topic pipeline orchestrator with three human quality gates.

Composes the existing stage runners — it does NOT re-implement any stage:
  SEG A  text + audio        runner.create_narration
  == GATE 1: listen to narration.mp3 ==
  SEG B  scene plan + images visual_runner.create_visuals(animate=False)
  == GATE 2: review images, confirm hero, --reroll N,N ==
  SEG C  Kling clips          visual_handoff.run_kling_pipeline(non-excluded only)
  == GATE 3: review clips, --exclude N,N the glitchy ones ==
  SEG D  assemble             assembly_runner.run_assembly(minus excluded)

Position is detected from artifacts on disk (idempotent, like visual_runner's
LOCKED-reuse). Cross-invocation choices (provider / hero / excluded) persist in
`<v1>/pipeline.state.json`. `--continue` crosses exactly one gate.

Excluding a bad IMAGE at GATE 2 means SEG C never animates it — that is the
image-gate-before-Kling cost saver. Excluding a clip at GATE 3 just drops the
(already-rendered) clip from the cut.
"""
from __future__ import annotations

import json
from pathlib import Path

import config
from pipeline import runner, visual_handoff, visual_runner
from pipeline import assembly_runner
from pipeline.series import Episode, Series
from pipeline.visual_models import ScenePlan


STATE_NAME = "pipeline.state.json"
# Baroque content makes the Kling Stage A.5 audit nit-pick (feedback memory
# `feedback-kling-skip-audit`), so the orchestrator always skips it.
KLING_SKIP_AUDIT = True


# --------------------------------------------------------------------------
# State
# --------------------------------------------------------------------------
def _state_path(v1: Path) -> Path:
    return v1 / STATE_NAME


def _load_state(v1: Path) -> dict:
    p = _state_path(v1)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"provider": "hf", "hero": 0, "excluded": [], "notes": ""}


def _save_state(v1: Path, st: dict) -> None:
    _state_path(v1).write_text(json.dumps(st, indent=2, ensure_ascii=False), encoding="utf-8")


# --------------------------------------------------------------------------
# Scene plan helpers
# --------------------------------------------------------------------------
def _load_plan(v1: Path) -> ScenePlan | None:
    p = v1 / "visual" / "scene_plan.json"
    if not p.exists():
        return None
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
        if doc.get("authoritative_overall", "").upper().strip() != "LOCKED":
            return None
        return ScenePlan.from_json(doc.get("plan", {}))
    except Exception:
        return None


def _all_scene_indices(plan: ScenePlan) -> list[int]:
    return [s.index for s in plan.scenes]


_PIVOT_ARC = ("nt-gospel-link", "gospel-link", "passion", "resurrection")
_CROSS_RE = __import__("re").compile(r"\b(cross|crucif|calvary|golgotha)", 2)  # 2 = IGNORECASE


def _scene_is_pivot(s) -> bool:
    arc = s.arc_position or ""
    if any(tok in arc for tok in _PIVOT_ARC):
        return True
    if getattr(s, "jesus_variant", None) in ("passion", "resurrection"):
        return True
    return bool(_CROSS_RE.search(s.title))


def _hero_candidate(plan: ScenePlan) -> int:
    """Proposed hero for GATE 2. MUST be a gospel-pivot (cross / Christ) so the cut
    lands on Jesus — never the merely-emotional climax. Part 2 will add an explicit
    ScenePlan.hero_candidate; honour it only if it is itself a pivot."""
    hc = getattr(plan, "hero_candidate", 0) or 0
    by_idx = {s.index: s for s in plan.scenes}
    if hc and hc in by_idx and _scene_is_pivot(by_idx[hc]):
        return hc
    crosses = [s for s in plan.scenes
               if _CROSS_RE.search(s.title) or getattr(s, "jesus_variant", None) == "passion"]
    if crosses:
        return crosses[0].index
    pivots = [s for s in plan.scenes if _scene_is_pivot(s)]
    if pivots:
        pivots.sort(key=lambda s: (s.viral_role not in ("climax", "close"), s.index))
        return pivots[0].index
    return plan.scenes[0].index if plan.scenes else 0


# --------------------------------------------------------------------------
# Position detection
# --------------------------------------------------------------------------
def detect_position(v1: Path, provider: str, excluded: set[int]) -> str:
    """One of: start | audio_done | images_done | clips_done | assembled."""
    if not (v1 / "narration.mp3").exists():
        return "start"
    plan = _load_plan(v1)
    render_dir = v1 / "visual" / provider
    if plan is None:
        return "audio_done"
    pngs_ok = all((render_dir / f"{s.filename_stem}.png").exists() for s in plan.scenes)
    if not pngs_ok:
        return "audio_done"
    wanted = [s for s in plan.scenes if s.index not in excluded]
    mp4s_ok = wanted and all((render_dir / f"{s.filename_stem}.mp4").exists() for s in wanted)
    if not mp4s_ok:
        return "images_done"
    if not (v1 / "assembly" / "viral_cut.mp4").exists():
        return "clips_done"
    return "assembled"


# --------------------------------------------------------------------------
# Segment runners
# --------------------------------------------------------------------------
def _seg_b(v1: Path, provider: str, log) -> None:
    log("\n[SEG B] Scene plan + images (deep pool, no animation)...")
    visual_runner.create_visuals(
        v1, provider=provider, short_only=False, animate=False,
        plan_only=False, kling_skip_audit=KLING_SKIP_AUDIT, log=log,
    )


def _seg_c(v1: Path, provider: str, excluded: set[int], log) -> None:
    plan = _load_plan(v1)
    indices = [i for i in _all_scene_indices(plan) if i not in excluded] if plan else None
    n = len(indices) if indices else 0
    log(f"\n[SEG C] Animating {n} non-excluded clip(s) via VIDEO_PROVIDER="
        f"'{config.VIDEO_PROVIDER}'" + (f" (skipping {sorted(excluded)})" if excluded else "") + "...")
    if config.VIDEO_PROVIDER == "kling":
        # legacy path: direct-Kling for the whole subset via image_to_kling
        code = visual_handoff.run_kling_pipeline(
            v1, provider, short_only_indices=indices, skip_audit=KLING_SKIP_AUDIT, log=log)
        log(f"[SEG C] Kling exit code: {code}")
    else:
        # hybrid (default): HF Kling per clip, auto-fallback to direct-Kling on NSFW
        from pipeline import video_render
        video_render.animate_scenes(v1, provider, indices=indices, log=log)
    try:
        visual_handoff.write_review_index_html(v1, provider, plan=plan)
    except Exception:
        pass


def _seg_d(v1: Path, provider: str, excluded: set[int], hero: int, log) -> None:
    log("\n[SEG D] Assembling the cut from the approved, non-excluded pool...")
    assembly_runner.run_assembly(
        v1, provider=provider, exclude=excluded, hero=hero,
        rebuild=True, log=log,
    )


def _reroll_images(v1: Path, provider: str, reroll: set[int], log) -> None:
    plan = _load_plan(v1)
    if plan is None:
        log("      ! no LOCKED scene plan — cannot re-roll.")
        return
    render_dir = v1 / "visual" / provider
    for s in plan.scenes:
        if s.index in reroll:
            for suffix in (".png", ".png.audit.json"):
                f = render_dir / f"{s.filename_stem}{suffix}"
                if f.exists():
                    f.unlink()
                    log(f"      [reroll] deleted {f.name}")
    log("      re-rendering the deleted image(s)...")
    visual_runner.create_visuals(
        v1, provider=provider, short_only=False, animate=False,
        plan_only=False, kling_skip_audit=KLING_SKIP_AUDIT, log=log,
    )


# --------------------------------------------------------------------------
# Gate printing
# --------------------------------------------------------------------------
def _cmd(v1: Path) -> str:
    return f'.venv\\Scripts\\python.exe cli_pipeline.py "{v1}"'


def _gate1(v1: Path, log) -> None:
    log("\n" + "=" * 64)
    log("  GATE 1 — listen to the narration")
    log("=" * 64)
    log(f"  Play:  {v1 / 'narration.mp3'}")
    log("  If it sounds right, continue to scene plan + images:")
    log(f"    {_cmd(v1)} --continue")
    log("  (Not happy? re-run the text stage with cli.py before continuing.)")
    log("=" * 64)


def _gate2(v1: Path, provider: str, st: dict, log) -> None:
    plan = _load_plan(v1)
    hero = st.get("hero") or (_hero_candidate(plan) if plan else 0)
    index = v1 / "visual" / provider / "index.html"
    log("\n" + "=" * 64)
    log("  GATE 2 — review the images")
    log("=" * 64)
    log(f"  Open:  {index}")
    log(f"  Proposed HERO (bookends start+end): #{hero:02d}"
        + ("" if st.get("hero") else "  (auto; override with --hero N)"))
    log("  Re-roll any weak images (re-renders just those, stays at this gate):")
    log(f"    {_cmd(v1)} --reroll 6,11")
    log("  Drop obviously-bad images so we DON'T pay to animate them, then continue:")
    log(f"    {_cmd(v1)} --exclude 4 --continue       # excludes #4, animates the rest")
    log(f"    {_cmd(v1)} --continue                    # animate all")
    log("=" * 64)


def _gate3(v1: Path, provider: str, st: dict, log) -> None:
    index = v1 / "visual" / provider / "index.html"
    excluded = sorted(st.get("excluded", []))
    log("\n" + "=" * 64)
    log("  GATE 3 — review the clips")
    log("=" * 64)
    log(f"  Open:  {index}   (now shows the animated .mp4s)")
    log(f"  Currently excluded: {excluded or 'none'}")
    log("  Mark any glitchy / hallucinated clips to drop from the cut, then assemble:")
    log(f"    {_cmd(v1)} --exclude 3,10 --continue")
    log(f"    {_cmd(v1)} --continue                    # use all clips")
    log("=" * 64)


def _print_done(v1: Path, log) -> None:
    asm = v1 / "assembly"
    # Surface any doctrinal-fidelity flag from the verify pass loudly.
    plan_path = asm / "edit_plan.json"
    if plan_path.exists():
        try:
            audit = (json.loads(plan_path.read_text(encoding="utf-8")) or {}).get("audit") or {}
            notes = audit.get("notes", "")
            reroll = audit.get("reroll_scene_indices") or []
            if "BLOCKING" in notes:
                log("\n" + "!" * 64)
                log(f"  ! {notes}")
                log("  ! Review those frames yourself, then --exclude them and re-cut.")
                log("!" * 64)
            elif reroll:
                log(f"\n  (verify flagged scenes {reroll} — review; --exclude to drop.)")
        except Exception:
            pass
    log("\n" + "=" * 64)
    log("  DONE — final cut assembled")
    log("=" * 64)
    log(f"  Cut:    {asm / 'viral_cut.mp4'}")
    log(f"  Reel:   {asm / 'all_takes_reel.mp4'}")
    log(f"  Review: {asm / 'index.html'}")
    log("  Re-cut anytime (e.g. drop another clip):")
    log(f"    {_cmd(v1)} --exclude 3,10")
    log("=" * 64)


# --------------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------------
def start(series: Series, episode: Episode, notes: str, provider: str, log=print) -> Path:
    """SEG A: text + audio, then stop at GATE 1."""
    res = runner.create_narration(series, episode, notes=notes, run_audio=True, log=log)
    v1 = res.folder
    st = _load_state(v1)
    st.update({"provider": provider, "notes": notes})
    st.setdefault("hero", 0)
    st.setdefault("excluded", [])
    _save_state(v1, st)
    _gate1(v1, log)
    return v1


def advance(
    v1: Path,
    do_continue: bool = False,
    reroll: set[int] | None = None,
    exclude_add: set[int] | None = None,
    include_remove: set[int] | None = None,
    hero: int = 0,
    provider: str = "",
    log=print,
) -> str:
    """Drive the pipeline one step from wherever it is. Returns the position
    reached (after acting)."""
    st = _load_state(v1)
    provider = provider or st.get("provider") or "hf"
    st["provider"] = provider
    if hero:
        st["hero"] = hero
    excl = set(st.get("excluded", []))
    if exclude_add:
        excl |= set(exclude_add)
    if include_remove:
        excl -= set(include_remove)
    st["excluded"] = sorted(excl)
    _save_state(v1, st)
    excluded = set(st.get("excluded", []))
    reroll = reroll or set()

    pos = detect_position(v1, provider, excluded)

    if pos == "start":
        raise SystemExit(f"No narration.mp3 under {v1}. Start a new topic with `cli_pipeline.py` (no args).")

    if pos == "audio_done":
        if not do_continue:
            _gate1(v1, log); return pos
        _seg_b(v1, provider, log)
        _gate2(v1, provider, _load_state(v1), log)
        return detect_position(v1, provider, excluded)

    if pos == "images_done":
        if reroll:
            _reroll_images(v1, provider, reroll, log)
            _gate2(v1, provider, _load_state(v1), log)
            return "images_done"
        if not do_continue:
            _gate2(v1, provider, st, log); return pos
        _seg_c(v1, provider, excluded, log)
        _gate3(v1, provider, _load_state(v1), log)
        return detect_position(v1, provider, excluded)

    if pos == "clips_done":
        if not do_continue:
            _gate3(v1, provider, st, log); return pos
        _seg_d(v1, provider, excluded, st.get("hero", 0), log)
        _print_done(v1, log)
        return detect_position(v1, provider, excluded)

    # assembled
    if do_continue or exclude_add or hero:
        _seg_d(v1, provider, excluded, st.get("hero", 0), log)
        _print_done(v1, log)
    else:
        log("\n[pipeline] already assembled.")
        _print_done(v1, log)
    return "assembled"
