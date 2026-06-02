"""Write the generated narration into the existing audio-pipeline tree and
optionally run that pipeline end-to-end.

Output contract (matches PythonProject1/jesus/narration/):
    <NN_Title>/v1/   (NEW folders use underscores, no spaces; legacy folders kept as-is)
        narration.md             <- plain prose, paragraphs = beats (the input)
        voices.json              <- speaker -> {voice_id, audio_tag} roster
        narration.creation.json  <- our provenance (draft + review summary)
        narration.creation-review.md  <- human-readable red-team report
Then `narration_pipeline.py <folder>` runs verify -> tag -> audit -> synth.
"""
from __future__ import annotations

import json
import re
import subprocess
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

import config
from pipeline.models import Draft, Review, Thread
from pipeline.series import Episode, Series
from pipeline.structures import Structure

_INVALID = re.compile(r'[\\/:*?"<>|]')
# Leading 2-3 digit prefix followed by a space (legacy folders) or underscore
# (new folders). Both forms must be counted by _next_number so prefixes don't collide.
_LEADING_NUM = re.compile(r"^(\d{2,3})[ _]")


def _safe_title(title: str) -> str:
    """Filesystem-safe title with NO spaces — whitespace runs collapse to single
    underscores so paths are click-to-open without quoting (user preference)."""
    cleaned = _INVALID.sub("", title).strip()
    cleaned = re.sub(r"\s+", "_", cleaned)
    return cleaned or "untitled"


def _next_number() -> int:
    """Next 2/3-digit folder prefix, scanning existing numbered folders."""
    tree = config.NARRATION_TREE_DIR
    highest = 0
    if tree.exists():
        for child in tree.iterdir():
            if child.is_dir():
                m = _LEADING_NUM.match(child.name)
                if m:
                    highest = max(highest, int(m.group(1)))
    return highest + 1


def _build_voices(speakers: list[str]) -> tuple[dict, list[str]]:
    """voices.json roster for the speakers present. Returns (roster, unknown)."""
    roster: dict[str, dict] = {
        "narrator": {"voice_id": config.VOICE_MAP["narrator"], "audio_tag": None}
    }
    unknown: list[str] = []
    for sp in speakers:
        if sp == "narrator":
            continue
        if sp in config.VOICE_MAP:
            roster[sp] = {
                "voice_id": config.VOICE_MAP[sp],
                "audio_tag": config.VOICE_AUDIO_TAGS.get(sp),
            }
        else:
            unknown.append(sp)
    return roster, unknown


def _review_dict(review: Review) -> dict:
    return {
        "overall": review.overall,
        "panel": [asdict(a) for a in review.panel],
        "gates": [asdict(g) for g in review.gates],
        "priority_fixes": review.priority_fixes,
    }


def write_narration_folder(
    series: Series,
    episode: Episode,
    draft: Draft,
    review: Review,
    kjv_text: str | None,
    structure: Structure,
    self_review: Review | None = None,
    thread: Thread | None = None,
) -> tuple[Path, list[str]]:
    """Create the <NN Title>/v1 folder with narration.md + voices.json + sidecars.

    `review` is the authoritative (independent) verdict; `self_review` is the
    internal review that drove revisions. `thread` is the chosen freshness
    thread (with all candidates), stored for traceability and rendered in the
    review report. Returns (v1_folder, unknown_speakers).
    """
    n = _next_number()
    width = max(2, len(str(n)))
    folder_name = f"{n:0{width}d}_{_safe_title(draft.title or episode.title)}"
    v1 = config.NARRATION_TREE_DIR / folder_name / "v1"
    v1.mkdir(parents=True, exist_ok=True)

    # 1. narration.md — the canonical input for the audio pipeline.
    (v1 / "narration.md").write_text(draft.narration.strip() + "\n", encoding="utf-8")

    # 2. voices.json — always written (at least the narrator). per_turn_synth.py
    #    requires it even for monologue, and the dialogue synth uses it too.
    roster, unknown = _build_voices(draft.speakers)
    (v1 / "voices.json").write_text(
        json.dumps(roster, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 3. creation provenance (does not collide with pipeline sidecars).
    creation = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "model": config.MODEL,
        "review_model": config.REVIEW_MODEL or config.MODEL,
        "structure": {"id": structure.id, "name": structure.name, "beats": structure.beat_ids},
        "series": {"id": series.id, "name": series.name, "brand": series.brand},
        "episode": {"title": episode.title, "primary_ref": episode.primary_ref},
        "kjv_verified": bool(kjv_text),
        "kjv_text": kjv_text,
        "thread": asdict(thread) if thread else None,
        "draft": asdict(draft),
        "beat_ids": draft.beat_ids,
        "word_count": draft.word_count,
        "char_count": draft.char_count,
        "authoritative_review": "independent" if config.INDEPENDENT_REVIEW else "self",
        "review_overall": review.overall,
        "independent_review": _review_dict(review) if config.INDEPENDENT_REVIEW else None,
        "self_review": _review_dict(self_review) if self_review else None,
        "unknown_speakers": unknown,
    }
    (v1 / "narration.creation.json").write_text(
        json.dumps(creation, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 4. human-readable review report.
    (v1 / "narration.creation-review.md").write_text(
        _render_review_md(series, episode, draft, review, kjv_text, structure, self_review, thread),
        encoding="utf-8",
    )

    return v1, unknown


def _render_review_md(
    series: Series, episode: Episode, draft: Draft, review: Review,
    kjv_text: str | None, structure: Structure, self_review: Review | None,
    thread: Thread | None = None,
) -> str:
    authoritative = "INDEPENDENT audit" if config.INDEPENDENT_REVIEW else "self-review"
    lines = [
        f"# {draft.title}",
        "",
        f"**Series:** {series.name} ({series.brand})  ",
        f"**Episode:** {episode.title} — {draft.scripture_reference}  ",
        f"**Structure:** {structure.name} — beats {draft.beat_ids}  ",
        f"**Hook type:** {draft.hook_type}  ",
        f"**Words:** {draft.word_count}  ·  **Chars:** {draft.char_count}  ",
        f"**KJV verified:** {'yes' if kjv_text else 'NO — verify the verse manually'}  ",
        f"**Authoritative verdict ({authoritative}):** {review.overall}"
        + (f"  ·  self-review: {self_review.overall}" if self_review else ""),
        "",
    ]
    if thread and not thread.is_empty:
        lines += [
            "## Thread (freshness spine)",
            f"**Thread:** {thread.thread}  ",
            f"**Lever:** {thread.lever}  ",
            f"**Anchor:** {thread.anchor_ref} — {thread.anchor_detail}  ",
            f"**Why fresh:** {thread.why_fresh}  ",
            f"**Gospel landing:** {thread.gospel_landing}  ",
            f"**Why chosen:** {thread.rationale}" if thread.rationale else "",
            "",
        ]
        if thread.candidates:
            lines.append("<details><summary>Candidates considered "
                         f"({len(thread.candidates)})</summary>\n")
            for i, c in enumerate(thread.candidates):
                mark = " *(chosen)*" if c.thread == thread.thread else ""
                lines += [
                    f"{i + 1}. **{c.thread}**{mark} — _{c.lever}_  ",
                    f"   anchor: {c.anchor_ref} — {c.anchor_detail}  ",
                    f"   why fresh: {c.why_fresh}  ",
                    f"   gospel landing: {c.gospel_landing}",
                    "",
                ]
            lines.append("</details>")
            lines.append("")
    lines += [
        "## Hook",
        f"> {draft.hook}",
        "",
        "## CTA (Landing)",
        f"> {draft.cta}",
        "",
        f"## Independent red-team panel"
        if config.INDEPENDENT_REVIEW else "## Red-team panel",
    ]
    for a in review.panel:
        lines.append(f"- **{a.agent}** — `{a.verdict}` — {a.note}")
    lines += ["", "## Quality gates (4 pillars + structure + craft + freshness)"]
    for g in review.gates:
        line = f"- **{g.gate}** — `{g.verdict}` — {g.evidence}"
        if g.verdict.upper() != "PASS" and g.fix:
            line += f"  \n  _fix:_ {g.fix}"
        lines.append(line)
    if review.priority_fixes:
        lines += ["", "## Priority fixes"]
        lines += [f"{i}. {f}" for i, f in enumerate(review.priority_fixes, 1)]
    return "\n".join(lines) + "\n"


def _run(cmd: list[str]) -> int:
    """Run a subprocess in the narration project, streaming output."""
    print(f"  [audio] $ {' '.join(cmd)}")
    try:
        return subprocess.run(cmd, cwd=str(config.NARRATION_PROJECT_DIR)).returncode
    except FileNotFoundError:
        print(
            f"  [audio] FAILED — interpreter not found: {config.NARRATION_PYTHON}\n"
            f"          Set NARRATION_PYTHON to the PythonProject1 venv python."
        )
        return 1


def run_audio_pipeline(v1_folder: Path) -> int:
    """Drive the audio pipeline. In SHORTS_MODE (default) this runs the three
    Anthropic stages then the duration-locked per_turn_synth (PLAYBOOK_shorts);
    otherwise it runs the natural-length narration_pipeline.py in one shot.
    Returns 0 on success.
    """
    py = config.NARRATION_PYTHON
    pipeline = config.NARRATION_PIPELINE_SCRIPT
    if not pipeline.exists():
        print(f"  [audio] SKIPPED — pipeline script not found at {pipeline}")
        print(f"          Set NARRATION_PROJECT_DIR or run it yourself on:\n          {v1_folder}")
        return 1

    if not config.SHORTS_MODE:
        return _run([py, str(pipeline), str(v1_folder)])

    # --- Shorts path: verify -> tag -> audit, then duration-locked synth ---
    synth = config.PER_TURN_SYNTH_SCRIPT
    if not synth.exists():
        print(f"  [audio] SKIPPED — per_turn_synth not found at {synth}")
        return 1

    for stage in ("verify", "tag", "audit"):
        code = _run([py, str(pipeline), str(v1_folder), "--stage", stage])
        if code != 0:
            print(
                f"  [audio] BLOCKED at stage '{stage}' (exit {code}). "
                f"Not synthesising. Check the sidecar in:\n          {v1_folder}"
            )
            return code

    synth_cmd = [
        py, str(synth), str(v1_folder),
        "--target", str(config.SHORTS_TARGET_SECONDS),
        "--pre-quote-pause", str(config.SHORTS_PRE_QUOTE_PAUSE),
        "--stability", str(config.SHORTS_STABILITY),
    ]
    # Natural speed (default): --target is a ceiling, the voice is never stretched.
    if config.SHORTS_NATURAL_SPEED:
        synth_cmd.append("--natural")
    return _run(synth_cmd)
