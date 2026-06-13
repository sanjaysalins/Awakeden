"""Orchestrate the Upload Kit stage for one finished media folder:

  harvest facts -> generate metadata -> assemble + stamp footer
  -> deterministic gates -> in-engine red-team -> (optional external panel)
  -> pick best -> write upload_kit.{json,md} beside the video.

Idempotent-ish: re-running regenerates; pass an already-built kit dict to skip
generation (used by the agent-authored sample path).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import config
from pipeline import upload_engine, upload_gates, upload_handoff
from pipeline.upload_models import UploadKit


def _sibling_titles(media_dir: str) -> list[str]:
    """Chosen titles from neighbouring kits (so UK-G6 can flag collisions)."""
    me = Path(media_dir).resolve()
    parent = me.parent
    out: list[str] = []
    for kj in parent.glob("*/upload/upload_kit.json"):
        if kj.resolve().parent.parent == me:
            continue
        try:
            data = json.loads(kj.read_text(encoding="utf-8"))
            for p in data.get("platforms", []):
                if p.get("platform") == "youtube_short" and p.get("title"):
                    out.append(p["title"])
        except Exception:
            pass
    return out


def run_one(media_dir: str, *, run_panel: bool = False,
            raw_override: dict | None = None) -> dict:
    """Produce + verify + write a kit. Returns {kit, paths, gates_pass}."""
    brand = upload_engine.load_brand()
    facts = upload_engine.harvest_facts(media_dir)

    raw = raw_override if raw_override is not None else upload_engine.generate(facts)
    kit = upload_engine.assemble_kit(facts, raw, brand)

    kit.gates = upload_gates.run_all(kit, brand, _sibling_titles(media_dir))
    kit.status = "RED-TEAMED"
    kit.redteam = upload_engine.redteam(kit)

    paths = upload_handoff.write_kit(kit)

    panel = None
    if run_panel:
        panel = launch_panel(paths["md"])
        kit.notes.append(f"panel launched -> {panel}")
        upload_handoff.write_kit(kit)  # rewrite with the note

    return {
        "kit": kit,
        "paths": paths,
        "gates_pass": kit.all_gates_pass,
        "panel_dir": panel,
    }


def launch_panel(artifact_md: str) -> str:
    """Fan the kit out to the external CLI panel via independent_review.py (--type upload)."""
    cmd = [
        sys.executable, str(config.PROJECT_ROOT / "independent_review.py"),
        artifact_md, "--type", "upload",
    ]
    subprocess.run(cmd, cwd=str(config.PROJECT_ROOT), check=False)
    stamp_root = Path(artifact_md).resolve().parent / "_independent_review"
    if stamp_root.is_dir():
        stamps = sorted(stamp_root.glob("*"))
        if stamps:
            return str(stamps[-1])
    return ""
