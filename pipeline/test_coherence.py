"""Regression tests for the IMG-COHERENT fail-closed scaffolding (v2/COHERENCE_GATE_SPEC.md).

Locks in the holes the red-team forced closed:
  - no sidecar / failing / un-audited / hash-mismatch -> UNVERIFIED (fail-closed)
  - the usage-cap hole: audited=False can never be passed, even if passed=True is recorded
  - png_sha256 binds the verdict to the exact image (silent re-render busts it)
  - INV-24: copy_verdict propagates a REAL verdict, never fabricates one
  - the assembly chokepoint (require_visual_coherence) reports always, blocks only when enabled
  - the rule registry stays integrity-clean after the IMG-COHERENT rewrite

Run: .venv\\Scripts\\python.exe -m pipeline.test_coherence
"""
from __future__ import annotations
import os
import tempfile
from pathlib import Path

from pipeline import coherence as C
from pipeline import lock as L
from pipeline import validators as V


def _png(d: Path, name: str = "07_test.png", data: bytes = b"\x89PNG-fake-bytes") -> Path:
    p = d / name
    p.write_bytes(data)
    return p


# ---- fail-closed sidecar logic ----------------------------------------------

def test_no_sidecar_is_unverified():
    with tempfile.TemporaryDirectory() as d:
        png = _png(Path(d))
        assert not C.is_verified(png), "no coherence sidecar must be UNVERIFIED"


def test_passing_audited_is_verified():
    with tempfile.TemporaryDirectory() as d:
        png = _png(Path(d))
        C.record_verdict(png, audited=True, passed=True, note="looked, plausible body")
        assert C.is_verified(png), "audited+passed+hash-match must verify"


def test_failing_is_unverified():
    with tempfile.TemporaryDirectory() as d:
        png = _png(Path(d))
        C.record_verdict(png, audited=True, passed=False, fail_reasons=["C1 floating head"])
        assert not C.is_verified(png), "a FAIL verdict must be UNVERIFIED"


def test_usage_cap_hole_closed():
    # the verify_image usage-cap path returns passed=True; coherence must refuse to bless an
    # UN-audited image even if passed=True is passed in.
    with tempfile.TemporaryDirectory() as d:
        png = _png(Path(d))
        sc = C.record_verdict(png, audited=False, passed=True, note="audit skipped (cap)")
        assert not C.is_verified(png), "audited=False must never be verified, even if passed=True"
        import json
        assert json.loads(sc.read_text())["passed"] is False, "un-audited must persist passed=False"


def test_hash_binding_busts_on_rerender():
    with tempfile.TemporaryDirectory() as d:
        png = _png(Path(d))
        C.record_verdict(png, audited=True, passed=True)
        assert C.is_verified(png)
        png.write_bytes(b"\x89PNG-DIFFERENT-bytes")  # silent in-place re-render
        assert not C.is_verified(png), "a changed image must bust the stale verdict (STALE)"
        assert "STALE" in C.verdict_reason(png)


# ---- INV-24: copy a real verdict, never fabricate ---------------------------

def test_copy_verdict_propagates_real_pass_and_rehashes():
    with tempfile.TemporaryDirectory() as d:
        src = _png(Path(d), "src.png", data=b"\x89PNG-SRC-bytes")
        C.record_verdict(src, audited=True, passed=True)
        # dst has DIFFERENT bytes -> proves copy_verdict re-hashes to the dst, not the src hash
        dst = _png(Path(d), "dst.png", data=b"\x89PNG-DST-different-bytes")
        ok = C.copy_verdict(src, dst)
        assert ok and C.is_verified(dst), "a real source verdict must copy and verify the dst (re-hashed)"
        import json
        rec = json.loads(dst.with_suffix(".png.coherence.json").read_text())["png_sha256"]
        assert rec == C.png_sha256(dst) and rec != C.png_sha256(src), "must bind to dst's own hash"


def test_copy_verdict_no_source_leaves_unverified():
    with tempfile.TemporaryDirectory() as d:
        src = _png(Path(d), "src.png")           # no coherence sidecar on the source
        dst = _png(Path(d), "dst.png")
        ok = C.copy_verdict(src, dst)
        assert not ok and not C.is_verified(dst), "no source verdict -> dst stays UNVERIFIED (no fabrication)"


# ---- ensemble voting + hash-shared consensus (determinism fix) --------------

def test_ensemble_any_fail_consensus():
    with tempfile.TemporaryDirectory() as d:
        png = _png(Path(d))
        C.record_vote(png, 0, passed=True)
        C.record_vote(png, 1, passed=False, dims_failed=["D1"], reasons=["off eyes"])
        C.record_vote(png, 2, passed=True)
        C.aggregate([png])
        assert not C.is_verified(png), "any-fail: one FAIL vote must fail the consensus"
        import json
        d2 = json.loads(png.with_suffix(".png.coherence.json").read_text())
        assert d2["split"] is True, "disagreeing votes must be marked split"
        assert d2["n_votes"] == 3 and "D1" in d2["failed_dims"]


def test_ensemble_unanimous_pass_verifies():
    with tempfile.TemporaryDirectory() as d:
        png = _png(Path(d))
        for i in range(3):
            C.record_vote(png, i, passed=True)
        C.aggregate([png])
        assert C.is_verified(png), "3 unanimous PASS votes -> verified"


def test_no_votes_is_unaudited():
    with tempfile.TemporaryDirectory() as d:
        png = _png(Path(d))
        C.aggregate([png])
        assert not C.is_verified(png), "no votes -> unaudited -> blocked"


def test_byte_identical_get_identical_verdict():
    # THE determinism proof: two stills with identical bytes but different names + different
    # individual votes must end with the SAME consensus (hash-pooled), never opposite verdicts.
    with tempfile.TemporaryDirectory() as d:
        data = b"\x89PNG-identical-bytes-xyz"
        a = _png(Path(d), "08_that-water.png", data=data)
        b = _png(Path(d), "02_the-pierced-side.png", data=data)
        C.record_vote(a, 0, passed=True)            # copy A looked PASS
        C.record_vote(b, 0, passed=False, dims_failed=["D4"], reasons=["standing not hanging"])  # copy B looked FAIL
        C.aggregate([a, b])
        import json
        va = json.loads(a.with_suffix(".png.coherence.json").read_text())["passed"]
        vb = json.loads(b.with_suffix(".png.coherence.json").read_text())["passed"]
        assert va == vb, f"byte-identical stills must share one verdict; got {va} vs {vb}"
        assert va is False, "pooled any-fail: the FAIL vote must win across the identical pair"


def test_clear_sidecars_removes_stale():
    with tempfile.TemporaryDirectory() as d:
        png = _png(Path(d))
        C.record_verdict(png, audited=True, passed=True)
        (png.with_suffix(".png.audit.json")).write_text("{}", encoding="utf-8")
        C.clear_sidecars(png)
        assert not (png.with_suffix(".png.coherence.json")).exists()
        assert not (png.with_suffix(".png.audit.json")).exists()


# ---- assembly chokepoint: report always, block only when enabled ------------

def _mk_short(d: Path) -> Path:
    nbp = d / "visual" / "nbp"
    nbp.mkdir(parents=True)
    (nbp / "01_scene.png").write_bytes(b"\x89PNG")
    (nbp / "01_scene.mp4").write_bytes(b"")
    return d


def test_blockers_lists_unverified():
    with tempfile.TemporaryDirectory() as d:
        v1 = _mk_short(Path(d))
        blk = L.visual_coherence_blockers(v1, "nbp")
        assert any("01_scene.png" in b for b in blk), blk


def test_require_coherence_off_does_not_raise():
    with tempfile.TemporaryDirectory() as d:
        v1 = _mk_short(Path(d))
        os.environ.pop("JITB_REQUIRE_COHERENCE", None)  # default off
        L.require_visual_coherence(v1, "nbp")  # must NOT raise during rollout


def test_require_coherence_on_raises():
    with tempfile.TemporaryDirectory() as d:
        v1 = _mk_short(Path(d))
        os.environ["JITB_REQUIRE_COHERENCE"] = "1"
        try:
            raised = False
            try:
                L.require_visual_coherence(v1, "nbp")
            except PermissionError:
                raised = True
            assert raised, "with the flag ON, unverified assets must raise"
        finally:
            os.environ.pop("JITB_REQUIRE_COHERENCE", None)


def test_require_coherence_passes_when_all_verified():
    with tempfile.TemporaryDirectory() as d:
        v1 = _mk_short(Path(d))
        from pipeline import clip_qc
        png = v1 / "visual" / "nbp" / "01_scene.png"
        mp4 = v1 / "visual" / "nbp" / "01_scene.mp4"
        C.record_verdict(png, audited=True, passed=True)
        clip_qc.record_verdict(mp4, passed=True, note="frozen")
        os.environ["JITB_REQUIRE_COHERENCE"] = "1"
        try:
            L.require_visual_coherence(v1, "nbp")  # must NOT raise — all verified
        finally:
            os.environ.pop("JITB_REQUIRE_COHERENCE", None)


def test_exclude_skips_unverified():
    with tempfile.TemporaryDirectory() as d:
        v1 = _mk_short(Path(d))
        blk = L.visual_coherence_blockers(v1, "nbp", exclude={1})
        assert not blk, f"excluded scene 1 should not block; got {blk}"


def test_scene_indices_scopes_to_selected_cut():
    # an UNSELECTED but unverified pool still must NOT block; only the selected set is checked
    with tempfile.TemporaryDirectory() as d:
        v1 = Path(d)
        nbp = v1 / "visual" / "nbp"; nbp.mkdir(parents=True)
        (nbp / "01_used.png").write_bytes(b"\x89PNG-a")
        (nbp / "01_used.mp4").write_bytes(b"")
        (nbp / "09_unused_pool.png").write_bytes(b"\x89PNG-b")   # rendered, never selected
        # nothing verified yet -> scoped to {1} flags only scene 1, not the unused 9
        blk = L.visual_coherence_blockers(v1, "nbp", scene_indices={1})
        assert any("01_used" in b for b in blk), blk
        assert not any("09_unused" in b for b in blk), f"unselected pool still must not block: {blk}"


# ---- registry still clean after the IMG-COHERENT rewrite --------------------

def test_rules_integrity_after_rewrite():
    ok, problems = V.rules_integrity()
    assert ok, "rules.json problems:\n  " + "\n  ".join(problems)


def test_img_coherent_still_registered():
    ids = {r["id"] for r in V.load_rules()}
    assert "IMG-COHERENT" in ids


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
