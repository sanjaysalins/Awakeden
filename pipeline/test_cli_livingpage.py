"""cli_livingpage tests (P2-4, 2026-07-08): artifact-derived position detection.

Run: .venv\\Scripts\\python.exe -m pytest pipeline/test_cli_livingpage.py
"""
from __future__ import annotations

import tempfile
from pathlib import Path

import cli_livingpage as CLI


def test_fresh_piece_points_at_narration():
    d = Path(tempfile.mkdtemp()) / "fresh"
    d.mkdir()
    steps = CLI.detect(d)
    assert steps[0].name == "narration" and not steps[0].done
    first_open = next(s for s in steps if not s.done)
    assert first_open.name == "narration"


def test_progression_narration_then_voice_then_spec():
    d = Path(tempfile.mkdtemp()) / "p"
    (d / "audio").mkdir(parents=True)
    (d / "narration.md").write_text("# t", encoding="utf-8")
    steps = {s.name: s for s in CLI.detect(d)}
    assert steps["narration"].done and not steps["voice"].done
    (d / "audio" / "narration.mp3").write_bytes(b"x")
    (d / "audio" / "alignment.json").write_text("[]", encoding="utf-8")
    steps = {s.name: s for s in CLI.detect(d)}
    assert steps["voice"].done and not steps["spec"].done
    # without piece.json the machine stops at manifest (later stages need it)
    names = [s.name for s in CLI.detect(d)]
    assert names[-1] == "manifest"


def test_paid_steps_are_not_auto():
    """--continue must never auto-run a paid or human-gated step."""
    d = Path(tempfile.mkdtemp()) / "q"
    d.mkdir()
    for s in CLI.detect(d):
        if any(tok in s.next_cmd for tok in ("PAID", "HUMAN GATE")):
            assert not s.auto, f"{s.name} is paid/human-gated but marked auto"
