"""Visual-stage handoff: write scene_plan.json + reviews + cohesion + the
match_images-compatible _source_prompts.md into <v1_folder>/visual/.

V3 covers paper artifacts only (Phase A). Phase B (rendered images) lands in
V5; Phase C (Kling subprocess) lands in V8.
"""
from __future__ import annotations

import json
import os
import subprocess
from dataclasses import asdict
from pathlib import Path

import config
from pipeline.visual_models import (
    AgentVerdict,
    CohesionAudit,
    GateResult,
    ScenePlan,
    ScenePlanReview,
)
from pipeline.visual_render import assemble_final_prompt


VISUAL_SUBDIR = "visual"
REVIEW_INDEX_FILENAME = "index.html"


def visual_dir(v1_folder: Path) -> Path:
    return v1_folder / VISUAL_SUBDIR


def run_kling_pipeline(
    v1_folder: Path,
    provider: str,
    short_only_indices: list[int] | None = None,
    skip_audit: bool = False,
    log=print,
) -> int:
    """Drive PythonProject1/jesus/image_to_kling.py against the provider's
    render subfolder. Each PNG produces:
      <stem>.kling.json  (Stage A — Claude Vision cut plan)
      <stem>.audit.json  (Stage A.5 — audit sidecar)
      <stem>.mp4         (Stage B — Kling 3.0 image-to-video render)

    image_to_kling.py is idempotent: re-runs skip any image that already has
    BOTH .kling.json and .mp4. The locked-discipline SKILL is passed via the
    KLING_SKILL_PATH env (per HANDOVER.md).

    If `short_only_indices` is provided, only renders the listed scene indices
    by temporarily passing each PNG path individually (image_to_kling accepts
    either a folder or a single file).
    """
    render_dir = visual_dir(v1_folder) / provider
    if not render_dir.exists():
        log(f"      ! no render dir at {render_dir}")
        return 1

    script = config.NARRATION_PROJECT_DIR / "image_to_kling.py"
    if not script.exists():
        log(f"      ! image_to_kling.py not found at {script}")
        return 1

    if not config.KLING_SKILL_PATH.exists():
        log(f"      ! KLING_SKILL_PATH does not exist: {config.KLING_SKILL_PATH}")
        return 1

    env = os.environ.copy()
    env["KLING_SKILL_PATH"] = str(config.KLING_SKILL_PATH)
    env["PYTHONIOENCODING"] = "utf-8"
    # Route the image_to_kling.py subprocess's Vision calls through the SAME bridge.
    config.inject_agent_env(env)

    py = config.NARRATION_PYTHON

    # If a subset of scene indices is requested, walk the dir and pass each
    # matching PNG individually. Otherwise hand off the whole folder.
    targets: list[str] = []
    if short_only_indices:
        wanted = {f"{i:02d}_" for i in short_only_indices}
        for png in sorted(p for p in render_dir.iterdir() if p.suffix.lower() == ".png"):
            if any(png.name.startswith(prefix) for prefix in wanted):
                targets.append(str(png))
        if not targets:
            log("      ! no PNGs matched the short_only_indices.")
            return 1
        log(f"      [kling] {len(targets)} short-priority PNG(s) targeted")
    else:
        targets = [str(render_dir)]
        log(f"      [kling] full folder: {render_dir}")

    final_code = 0
    extra_flags = ["--skip-audit"] if skip_audit else []
    for target in targets:
        cmd = [py, str(script), target, *extra_flags]
        log(f"      [kling] $ {' '.join(cmd)}")
        try:
            result = subprocess.run(
                cmd,
                cwd=str(config.NARRATION_PROJECT_DIR.parent),
                env=env,
            )
        except FileNotFoundError:
            log(f"      [kling] FAILED — interpreter not found: {py}")
            return 1
        if result.returncode != 0:
            log(f"      [kling] target {target} exited {result.returncode}")
            final_code = result.returncode
    return final_code


def write_visual_paper_artifacts(
    v1_folder: Path,
    plan: ScenePlan,
    self_review: ScenePlanReview,
    independent_review: ScenePlanReview | None,
    paper_cohesion_audit: CohesionAudit,
) -> Path:
    """Atomically (per-file) write the four paper artifacts. Returns the
    visual/ subfolder path. Overwrites any existing files — idempotency at
    the artifact level applies to expensive renders, not to plan paper."""
    out = visual_dir(v1_folder)
    out.mkdir(parents=True, exist_ok=True)

    # 1. scene_plan.json — source of truth, includes both reviews + cohesion.
    plan_doc = {
        "plan": asdict(plan),
        "self_review": _review_dict(self_review),
        "independent_review": _review_dict(independent_review) if independent_review else None,
        "paper_cohesion": asdict(paper_cohesion_audit),
        "authoritative_overall": (
            independent_review.overall if independent_review else self_review.overall
        ),
    }
    (out / "scene_plan.json").write_text(
        json.dumps(plan_doc, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 2. _source_prompts.md — match_images.py format, full assembled prompts.
    (out / "_source_prompts.md").write_text(
        _render_source_prompts_md(plan), encoding="utf-8"
    )

    # 3. scene_plan.review.md — human-readable self review.
    (out / "scene_plan.review.md").write_text(
        _render_review_md(plan, self_review, kind="self"), encoding="utf-8"
    )

    # 4. scene_plan.independent-review.md — human-readable independent audit.
    if independent_review is not None:
        (out / "scene_plan.independent-review.md").write_text(
            _render_review_md(plan, independent_review, kind="independent"),
            encoding="utf-8",
        )

    # 5. cohesion.paper.json — the structured paper cohesion sidecar.
    (out / "cohesion.paper.json").write_text(
        json.dumps(asdict(paper_cohesion_audit), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return out


# --------------------------------------------------------------------------
# Rendering helpers
# --------------------------------------------------------------------------
def _review_dict(review: ScenePlanReview) -> dict:
    return {
        "overall": review.overall,
        "panel": [asdict(a) for a in review.panel],
        "gates": [asdict(g) for g in review.gates],
        "priority_fixes": review.priority_fixes,
    }


def _render_source_prompts_md(plan: ScenePlan) -> str:
    """Format the chosen scenes as `## N. Title\\n<final prompt>` so the
    downstream match_images.py / image_to_kling.py conventions pick it up
    cleanly. Short-priority scenes are flagged in the heading."""
    short_set = set(plan.short_priority)
    lines: list[str] = [
        f"# Scene prompts ({len(plan.scenes)} scenes)",
        "",
        "Auto-generated by `pipeline/visual_handoff.py`. The style base + tail are",
        f"applied by the renderer; this file shows the **final assembled prompts**.",
        f"Short-priority indices: {plan.short_priority}.",
        "",
    ]
    for scene in plan.scenes:
        on_short = " ★ short" if scene.index in short_set else ""
        lines.append(f"## {scene.index}. {scene.title}{on_short}")
        lines.append("")
        lines.append(
            f"_{scene.scene_type} · {scene.framing} · {scene.arc_position}"
            + (f" · jesus={scene.jesus_variant}" if scene.jesus_variant else "")
            + f" · priority={scene.priority}_"
        )
        lines.append("")
        lines.append(assemble_final_prompt(scene))
        lines.append("")
    return "\n".join(lines)


def write_review_index_html(
    v1_folder: Path,
    provider: str,
    plan: ScenePlan | None = None,
) -> Path | None:
    """Build a browser-viewable review page at v1/visual/<provider>/index.html
    listing each rendered scene with its reference number, spec, audit
    verdict, and image. Lets the user point at scenes by ref number to say
    what to fix. Returns the index.html path, or None if no renders exist.

    `plan` is optional — if omitted, loaded from scene_plan.json on disk."""
    render_dir = visual_dir(v1_folder) / provider
    if not render_dir.exists():
        return None

    pngs = sorted(p for p in render_dir.iterdir() if p.suffix.lower() == ".png")
    if not pngs:
        return None

    if plan is None:
        plan_path = visual_dir(v1_folder) / "scene_plan.json"
        if plan_path.exists():
            plan_doc = json.loads(plan_path.read_text(encoding="utf-8"))
            plan = ScenePlan.from_json(plan_doc.get("plan", {}))

    # Index the renders by scene index (parsed from filename "NN_slug.png").
    rendered_by_index: dict[int, Path] = {}
    for p in pngs:
        try:
            rendered_by_index[int(p.stem.split("_", 1)[0])] = p
        except ValueError:
            continue

    cards: list[str] = []
    for idx in sorted(rendered_by_index):
        png_path = rendered_by_index[idx]
        audit_path = png_path.with_name(png_path.name + ".audit.json")
        audit_data: dict = {}
        if audit_path.exists():
            try:
                audit_data = json.loads(audit_path.read_text(encoding="utf-8"))
            except Exception:
                audit_data = {}
        scene = plan.scene_by_index(idx) if plan else None
        mp4_path = png_path.with_suffix(".mp4")
        mp4_name = mp4_path.name if mp4_path.exists() else None
        cards.append(
            _render_scene_card_html(idx, png_path.name, mp4_name, scene, audit_data)
        )

    title = v1_folder.parent.name + " / " + v1_folder.name + f" / {provider}"
    html = _REVIEW_INDEX_TEMPLATE.format(
        title=title,
        provider=provider,
        count=len(rendered_by_index),
        cards="\n".join(cards),
    )
    out = render_dir / REVIEW_INDEX_FILENAME
    out.write_text(html, encoding="utf-8")
    return out


_REVIEW_INDEX_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Visual review — {title}</title>
<style>
  :root {{
    --bg: #18181b;
    --card: #27272a;
    --card-soft: #3f3f46;
    --text: #e4e4e7;
    --text-dim: #a1a1aa;
    --accent: #fde68a;
    --pass: #4ade80;
    --fail: #f87171;
    --warn: #fbbf24;
    --border: #52525b;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, "Segoe UI", system-ui, sans-serif;
    background: var(--bg); color: var(--text);
    margin: 0; padding: 32px;
    line-height: 1.45;
  }}
  header {{
    max-width: 1280px; margin: 0 auto 32px;
  }}
  h1 {{ font-size: 22px; margin: 0 0 8px; font-weight: 600; }}
  .subtitle {{ color: var(--text-dim); font-size: 13px; }}
  .grid {{ max-width: 1280px; margin: 0 auto; display: flex; flex-direction: column; gap: 24px; }}
  .card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
    display: grid;
    grid-template-columns: 280px 1fr;
  }}
  .card .img-col {{
    background: #000;
    position: relative;
    display: flex; align-items: center; justify-content: center;
    padding: 12px;
  }}
  .card img, .card video {{ max-width: 100%; max-height: 480px; border-radius: 4px; display: block; }}
  .media-badge {{
    position: absolute; top: 16px; left: 16px;
    padding: 2px 8px; border-radius: 3px;
    font-size: 10px; font-weight: 700; letter-spacing: 0.04em;
    font-family: ui-monospace, monospace;
    pointer-events: none;
  }}
  .media-badge.clip {{ background: rgba(74,222,128,0.9); color: #18181b; }}
  .media-badge.still {{ background: rgba(161,161,170,0.85); color: #18181b; }}
  .card .meta-col {{ padding: 20px 24px; }}
  .ref {{
    display: inline-block;
    background: var(--accent);
    color: #18181b;
    font-weight: 700; font-size: 14px;
    padding: 4px 10px; border-radius: 4px;
    margin-right: 12px;
    font-family: ui-monospace, "Cascadia Code", monospace;
  }}
  .title {{ font-size: 18px; font-weight: 600; display: inline; }}
  .tags {{ margin: 10px 0 16px; }}
  .tag {{
    display: inline-block;
    background: var(--card-soft);
    color: var(--text-dim);
    padding: 2px 8px; margin-right: 6px;
    border-radius: 3px; font-size: 11px;
    font-family: ui-monospace, monospace;
  }}
  .verdict {{
    display: inline-block;
    padding: 3px 10px; border-radius: 4px;
    font-size: 12px; font-weight: 600;
    font-family: ui-monospace, monospace;
    margin-bottom: 16px;
  }}
  .verdict.pass {{ background: rgba(74,222,128,0.15); color: var(--pass); border: 1px solid var(--pass); }}
  .verdict.fail {{ background: rgba(248,113,113,0.15); color: var(--fail); border: 1px solid var(--fail); }}
  .verdict.none {{ background: var(--card-soft); color: var(--text-dim); }}
  .section {{ margin: 14px 0; }}
  .section-label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-dim); margin-bottom: 4px; }}
  .section-body {{ font-size: 14px; color: var(--text); }}
  ul.issues {{ margin: 6px 0 0; padding-left: 20px; font-size: 13px; }}
  ul.issues li {{ margin: 4px 0; }}
  ul.issues .claim {{ color: var(--warn); }}
  ul.issues .actual {{ color: var(--text-dim); }}
  .filename {{
    font-family: ui-monospace, monospace; font-size: 11px;
    color: var(--text-dim); margin-top: 12px;
  }}
</style>
</head>
<body>
<header>
  <h1>Visual review — {title}</h1>
  <div class="subtitle">{count} rendered scene(s) via <code>{provider}</code>. Scenes with a Kling clip play inline (looping, muted — unmute with the controls); reference any scene by its <code>#NN</code> badge.</div>
</header>
<div class="grid">
{cards}
</div>
</body>
</html>
"""


def _render_scene_card_html(
    idx: int, png_name: str, mp4_name: str | None, scene, audit: dict
) -> str:
    """One scene card. `scene` is the Scene dataclass (or None if missing
    from the plan); `audit` is the parsed audit JSON (or {} if missing).
    If `mp4_name` is given, the image column shows the Kling clip (PNG poster,
    looping muted playback) instead of the still."""
    if audit.get("passed") is True:
        verdict_class = "pass"
        verdict_text = "audit PASS"
    elif audit.get("passed") is False:
        verdict_class = "fail"
        verdict_text = "audit FAIL"
    else:
        verdict_class = "none"
        verdict_text = "no audit"

    title = (scene.title if scene else f"Scene {idx}")
    tags_html = ""
    spec_html = ""
    if scene is not None:
        tag_parts = [
            f'<span class="tag">{_h(scene.scene_type)}</span>',
            f'<span class="tag">{_h(scene.framing)}</span>',
            f'<span class="tag">{_h(scene.arc_position)}</span>',
        ]
        if scene.jesus_variant:
            tag_parts.append(f'<span class="tag">jesus={_h(scene.jesus_variant)}</span>')
        if scene.viral_role:
            tag_parts.append(f'<span class="tag">role={_h(scene.viral_role)}</span>')
        if scene.pacing:
            tag_parts.append(f'<span class="tag">pacing={_h(scene.pacing)}</span>')
        if scene.priority:
            tag_parts.append(f'<span class="tag">priority={scene.priority}</span>')
        tags_html = " ".join(tag_parts)
        macro_html = ""
        if scene.macro_elements:
            items = "".join(f"<li>{_h(m)}</li>" for m in scene.macro_elements)
            macro_html = (
                f'<div class="section"><div class="section-label">Macro elements (Kling cut anchors)</div>'
                f'<ul class="issues">{items}</ul></div>'
            )
        spec_html = (
            f'<div class="section"><div class="section-label">Required visible elements</div>'
            f'<div class="section-body">{_h(scene.visible_elements)}</div></div>'
            f'<div class="section"><div class="section-label">Emotional tone</div>'
            f'<div class="section-body">{_h(scene.emotional_tone)}</div></div>'
            f'<div class="section"><div class="section-label">Purpose</div>'
            f'<div class="section-body">{_h(scene.purpose)}</div></div>'
            f'{macro_html}'
        )

    issues = audit.get("issues") or []
    banned = audit.get("banned_token_hits") or []
    issues_html = ""
    if issues or banned:
        rows: list[str] = []
        for it in issues:
            claim = _h(it.get("claim", ""))
            actual = _h(it.get("actual", ""))
            rows.append(f'<li><span class="claim">spec:</span> {claim}<br>'
                        f'<span class="actual">actual:</span> {actual}</li>')
        for tok in banned:
            rows.append(f'<li><span class="claim">banned token visible:</span> {_h(str(tok))}</li>')
        issues_html = (
            '<div class="section"><div class="section-label">Audit issues</div>'
            '<ul class="issues">' + "".join(rows) + '</ul></div>'
        )

    if mp4_name:
        media_html = (
            f'<video src="{_h(mp4_name)}" poster="{_h(png_name)}" '
            'controls loop muted playsinline preload="metadata"></video>'
            '<span class="media-badge clip">▶ clip</span>'
        )
        filename = mp4_name
    else:
        media_html = (
            f'<img src="{_h(png_name)}" alt="Scene {idx}">'
            '<span class="media-badge still">still only</span>'
        )
        filename = png_name

    return (
        '<div class="card">'
        f'<div class="img-col">{media_html}</div>'
        '<div class="meta-col">'
        f'<span class="ref">#{idx:02d}</span><span class="title">{_h(title)}</span>'
        f'<div class="tags">{tags_html}</div>'
        f'<div class="verdict {verdict_class}">{verdict_text}</div>'
        f'{spec_html}{issues_html}'
        f'<div class="filename">{_h(filename)}</div>'
        '</div>'
        '</div>'
    )


def _h(s: str) -> str:
    """Minimal HTML-escape for user-supplied strings."""
    return (
        s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
         .replace('"', "&quot;").replace("'", "&#39;")
    )


def _render_review_md(
    plan: ScenePlan, review: ScenePlanReview, kind: str
) -> str:
    label = "Independent red-team audit" if kind == "independent" else "Self-review panel"
    lines: list[str] = [
        f"# Scene plan — {label}",
        "",
        f"**Verdict:** `{review.overall}`  ·  **Failed gates:** {len(review.failed_gates)}",
        "",
        "## Visual reading",
        plan.visual_reading or "_(not provided)_",
        "",
        "## Writer's own red-team notes",
        plan.red_team_notes or "_(not provided)_",
        "",
        "## Scenes",
    ]
    short_set = set(plan.short_priority)
    for s in plan.scenes:
        flag = " ★" if s.index in short_set else ""
        lines.append(
            f"- **{s.index}. {s.title}**{flag} "
            f"`[{s.scene_type}/{s.framing}/{s.arc_position}"
            + (f"/jesus={s.jesus_variant}" if s.jesus_variant else "")
            + "]`"
        )
        lines.append(f"  · purpose: {s.purpose}")
        lines.append(f"  · rationale: {s.rationale}")
        lines.append(f"  · visible: {s.visible_elements}")
    lines += [
        "",
        f"## {label.split(' ')[0]} panel",
    ]
    for a in review.panel:
        lines.append(f"- **{a.agent}** — `{a.verdict}` — {a.note}")
    lines += ["", "## Gates (8: SP-G1..SP-G8)"]
    for g in review.gates:
        line = f"- **{g.gate}** — `{g.verdict}` — {g.evidence}"
        if g.verdict.upper().strip() != "PASS" and g.fix:
            line += f"  \n  _fix:_ {g.fix}"
        lines.append(line)
    if review.priority_fixes:
        lines += ["", "## Priority fixes"]
        lines += [f"{i}. {f}" for i, f in enumerate(review.priority_fixes, 1)]
    lines += [
        "",
        f"## Short-priority rank: {plan.short_priority}",
        "",
        f"## Beat coverage",
    ]
    for k, v in plan.beat_coverage.items():
        lines.append(f"- `{k}`: {v}")
    return "\n".join(lines) + "\n"
