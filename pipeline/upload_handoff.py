"""Write the finished Upload Kit beside the video.

Two artifacts in <media>/upload/:
  upload_kit.json   machine-readable (every candidate, gate, verdict)
  upload_kit.md     human, COPY-PASTE-READY, big clear blocks per platform
"""
from __future__ import annotations

import json
from pathlib import Path

from pipeline.upload_models import UploadKit


def out_dir(media_dir: str) -> Path:
    d = Path(media_dir).resolve() / "upload"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _gate_line(g) -> str:
    mark = "✅" if g.passed else "❌"
    return f"{mark} **{g.gate} {g.name}** — {g.detail}"


def _platform_block(p) -> str:
    lines = [f"## {p.label}", ""]
    if p.title:
        lines += ["**TITLE** (copy):", "```", p.title, "```",
                  f"_{len(p.title)} characters_", ""]
    lines += ["**DESCRIPTION / CAPTION** (copy):", "```", p.description, "```",
              f"_{len(p.description)} characters_", ""]
    if p.tags:
        lines += ["**TAGS** (copy — paste into the keyword/tags field):", "```",
                  ", ".join(p.tags), "```", ""]
    if p.hashtags:
        lines += ["**HASHTAGS** (copy):", "```", " ".join(p.hashtags), "```", ""]
    lines.append("---")
    return "\n".join(lines)


def render_md(kit: UploadKit) -> str:
    s = kit.source
    head = [
        f"# Upload Kit — {s.episode_title}",
        "",
        f"**Status:** {kit.status}  ·  **Gates:** {'ALL PASS ✅' if kit.all_gates_pass else 'FAILURES ❌'}",
        f"**Video:** `{s.video_path or '(not found)'}`",
        f"**Format:** {s.format}  ·  **Series:** {s.series_name}  ·  **Anchor:** {s.anchor_ref}",
        "",
        "> Copy each block straight into the platform's upload form. Title, description,",
        "> tags and hashtags are pre-checked, red-teamed and panel-reviewed.",
        "",
        "## ✔ Verification",
        "",
        *[_gate_line(g) for g in kit.gates],
        "",
    ]
    if kit.redteam:
        head += ["### Red-team (in-engine hostile auditor)", "", "```", kit.redteam.strip(), "```", ""]
    if kit.panel_verdict:
        head += ["### Independent AI panel (merged)", "", "```", kit.panel_verdict.strip(), "```", ""]

    titles = ["## Title options (chosen first)", ""]
    for i, c in enumerate(kit.title_candidates):
        star = " ⟵ CHOSEN" if c.chosen else ""
        titles.append(f"{i+1}. **{c.text}**{star}  \n   _angle: {c.angle}_")
    titles.append("")

    body = "\n".join(_platform_block(p) for p in kit.platforms)
    return "\n".join(head) + "\n" + "\n".join(titles) + "\n" + body + "\n"


def write_kit(kit: UploadKit) -> dict[str, str]:
    d = out_dir(kit.source.media_dir)
    j = d / "upload_kit.json"
    m = d / "upload_kit.md"
    j.write_text(json.dumps(kit.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    m.write_text(render_md(kit), encoding="utf-8")
    return {"json": str(j), "md": str(m)}
