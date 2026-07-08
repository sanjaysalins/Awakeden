"""Fail-closed render guards (P0-4, 2026-07-08).

Locks in the three teeth added after the engine audit:
  1. guard_prompt — poison tokens are FIXED (not just warned) before a paid call.
  2. arm_audit    — a fresh render gets a pending-FAIL sidecar (gate stays RED until
                    a real PASS), and an existing verdict is never overwritten.
  3. hf_animate   — refuses to pay Kling for a production still without a PASS sidecar.

Run: .venv\\Scripts\\python.exe -m pytest pipeline/test_render_guard.py
"""
from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path

import pytest

from render_lint import arm_audit, guard_prompt
from render_lint.verify import audit_status, write_audit

REPO = Path(__file__).resolve().parent.parent


def _tmp_png(name: str = "01_test_scene.png") -> Path:
    p = Path(tempfile.mkdtemp()) / name
    p.write_bytes(b"\x89PNG\r\n\x1a\nfake")
    return p


def test_guard_prompt_fixes_poison_negation():
    # "no text" style negation draws the noun — guard must strip/rewrite it
    fixed = guard_prompt("a quiet hillside at dawn, no text, no watermark")
    assert "no text" not in fixed.lower(), fixed


def test_arm_audit_writes_pending_fail_once():
    png = _tmp_png()
    arm_audit(png)
    assert audit_status(png) == "FAIL"
    # an existing verdict is never clobbered
    write_audit(png, "PASS", ["eyeballed"])
    arm_audit(png)
    assert audit_status(png) == "PASS"


def _load_animator():
    spec = importlib.util.spec_from_file_location("hfa", REPO / "_hf_animate_short.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_hf_animate_refuses_unaudited_still(monkeypatch):
    monkeypatch.delenv("JITB_SKIP_STILL_GATE", raising=False)
    mod = _load_animator()
    png = _tmp_png()
    with pytest.raises(PermissionError):
        mod.hf_animate(png, png.with_suffix(".mp4"), "prompt", 5)


def test_hf_animate_refuses_failed_still(monkeypatch):
    monkeypatch.delenv("JITB_SKIP_STILL_GATE", raising=False)
    mod = _load_animator()
    png = _tmp_png()
    arm_audit(png)                       # pending FAIL
    with pytest.raises(PermissionError):
        mod.hf_animate(png, png.with_suffix(".mp4"), "prompt", 5)
