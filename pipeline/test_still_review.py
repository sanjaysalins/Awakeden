"""Tests for the human still-review gate (pipeline/still_review.py).

Run: .venv\\Scripts\\python.exe -m pipeline.test_still_review
"""
from __future__ import annotations
import os
import tempfile
from pathlib import Path

from pipeline import still_review as SR


def _short(d: Path, n: int = 2) -> Path:
    nbp = d / "visual" / "nbp"
    nbp.mkdir(parents=True)
    for i in range(1, n + 1):
        (nbp / f"{i:02d}_scene.png").write_bytes(f"PNG-{i}".encode())
    return d


def test_unreviewed_is_pending():
    with tempfile.TemporaryDirectory() as d:
        v1 = _short(Path(d))
        ok, why = SR.is_reviewed(v1)
        assert not ok and "no .stills_reviewed" in why


def test_signoff_then_reviewed():
    with tempfile.TemporaryDirectory() as d:
        v1 = _short(Path(d))
        SR.sign_off(v1)
        ok, _ = SR.is_reviewed(v1)
        assert ok, "after sign-off it must read reviewed"


def test_changed_still_busts_signoff():
    with tempfile.TemporaryDirectory() as d:
        v1 = _short(Path(d))
        SR.sign_off(v1)
        assert SR.is_reviewed(v1)[0]
        # replace a still's bytes -> set hash changes -> sign-off stale
        (v1 / "visual" / "nbp" / "01_scene.png").write_bytes(b"PNG-CHANGED")
        ok, why = SR.is_reviewed(v1)
        assert not ok and "stale" in why


def test_added_still_busts_signoff():
    with tempfile.TemporaryDirectory() as d:
        v1 = _short(Path(d))
        SR.sign_off(v1)
        (v1 / "visual" / "nbp" / "09_new.png").write_bytes(b"PNG-NEW")  # a new still appears
        assert not SR.is_reviewed(v1)[0], "a newly-added still must bust the sign-off"


def test_require_off_does_not_raise_on_does_when_enabled():
    with tempfile.TemporaryDirectory() as d:
        v1 = _short(Path(d))
        os.environ.pop("JITB_REQUIRE_STILL_REVIEW", None)
        SR.require_review(v1)            # OFF (rollout) -> must not raise
        os.environ["JITB_REQUIRE_STILL_REVIEW"] = "1"
        try:
            raised = False
            try:
                SR.require_review(v1)    # ON + unreviewed -> raises
            except PermissionError:
                raised = True
            assert raised
            SR.sign_off(v1)
            SR.require_review(v1)        # ON + reviewed -> passes
        finally:
            os.environ.pop("JITB_REQUIRE_STILL_REVIEW", None)


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for t in tests:
        try:
            t(); print(f"[PASS] {t.__name__}"); passed += 1
        except AssertionError as e:
            print(f"[FAIL] {t.__name__}: {e}")
        except Exception as e:  # noqa
            print(f"[ERROR] {t.__name__}: {type(e).__name__}: {e}")
    print(f"\n{passed}/{len(tests)} passed")
    raise SystemExit(0 if passed == len(tests) else 1)
