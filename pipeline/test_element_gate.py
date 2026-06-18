"""Regression tests for the Visual-v3 SPINE (INV-25): the element manifest contract,
the deterministic cut-plan manifest-grounding, and the clip element gate aggregation.

Locks in the 2026-06-18 design (post 6x-REVISE review + the HF/direct bake-off):
  - declare -> reconcile -> LOCK, png_sha256-bound (silent re-render busts the lock).
  - a missing declared element is CUT from the tour (not auto-re-rendered), still locks on the rest.
  - the cut-plan may only target VERIFIED manifest elements; an invented titulus (the 'BINTX'
    bake-off defect) is blocked at the prompt layer.
  - the element gate is ANY-FAIL + default-PASS + hash-pooled (deterministic), fail-closed.

Run: .venv\\Scripts\\python.exe -m pipeline.test_element_gate
"""
from __future__ import annotations
import tempfile
from pathlib import Path

from pipeline import element_manifest as M
from pipeline import clip_element_gate as G
from pipeline import validators as V

_ALL_PASS = {k: "pass" for k in M.PERIOD_REAL_KEYS}


def _png(d, name="01_x.png", body=b"PNGDATA-A"):
    p = Path(d) / name
    p.write_bytes(body)
    return p


# ---- manifest contract: declare -> reconcile -> lock --------------------------

def test_declare_then_reconcile_lock():
    with tempfile.TemporaryDirectory() as d:
        png = _png(d)
        M.declare(png, "01_x", [{"id": "full", "label": "the full crucified face"},
                                {"id": "mouth", "label": "the open crying mouth"},
                                {"id": "crown", "label": "crown of thorns on the brow"}])
        assert not M.is_locked(png), "declared-but-not-reconciled must NOT be locked"
        M.reconcile_and_lock(png, verified_ids=["full", "mouth", "crown"], period_real=_ALL_PASS)
        assert M.is_locked(png), "all elements verified + period pass -> locked"
        assert set(M.verified_ids(png)) == {"full", "mouth", "crown"}


def test_missing_element_is_cut_from_tour():
    with tempfile.TemporaryDirectory() as d:
        png = _png(d)
        M.declare(png, "01_x", [{"id": "full", "label": "full composition"},
                                {"id": "tear", "label": "a tear track down the cheek"}])
        # vision could not confirm 'tear' -> it is simply not verified (cut from the tour)
        M.reconcile_and_lock(png, verified_ids=["full"], period_real=_ALL_PASS)
        assert M.is_locked(png), "locks on the verified remainder"
        assert M.verified_ids(png) == ["full"], "unconfirmed 'tear' must not be targetable"


def test_period_fail_blocks_lock():
    with tempfile.TemporaryDirectory() as d:
        png = _png(d)
        M.declare(png, "01_x", [{"id": "full", "label": "full"}])
        bad = dict(_ALL_PASS, T1="fail")          # a modern/anachronism guardrail failed
        M.reconcile_and_lock(png, verified_ids=["full"], period_real=bad)
        assert not M.is_locked(png), "a failed period guardrail must block the lock"


def test_silent_rerender_busts_lock():
    with tempfile.TemporaryDirectory() as d:
        png = _png(d, body=b"ORIGINAL-BYTES")
        M.declare(png, "01_x", [{"id": "full", "label": "full"}])
        M.reconcile_and_lock(png, verified_ids=["full"], period_real=_ALL_PASS)
        assert M.is_locked(png)
        png.write_bytes(b"SILENTLY-RERENDERED")    # tamper, no relock
        assert not M.is_locked(png), "hash mismatch must bust the lock (fail-closed)"


def test_relock_after_approved_rerender():
    with tempfile.TemporaryDirectory() as d:
        png = _png(d, body=b"ORIGINAL-BYTES")
        M.declare(png, "01_x", [{"id": "full", "label": "full"}])
        M.reconcile_and_lock(png, verified_ids=["full"], period_real=_ALL_PASS)
        v0 = M.read(png)["lock_version"]
        png.write_bytes(b"APPROVED-RERENDER")
        M.relock(png, verified_ids=["full"], period_real=_ALL_PASS)
        assert M.is_locked(png), "approved relock must re-bind the hash"
        assert M.read(png)["lock_version"] == v0 + 1, "lock_version must bump on relock"


# ---- cut-plan manifest grounding (deterministic) ------------------------------

_MANIFEST = {"elements": [
    {"id": "full", "label": "the full crucified figure on the cross", "verified": True},
    {"id": "face", "label": "the upturned anguished face", "verified": True},
    {"id": "hand", "label": "the nailed hand on the crossbeam", "verified": True},
    {"id": "eclipse", "label": "the eclipse ring in the dark sky", "verified": True}],
    "ambient_layer": ["slow shadow shift"]}


def _kling(beats):
    return {"beats": [{"description": b} for b in beats]}


def test_manifest_grounded_clean_tour_passes():
    ok, probs = V.cutplan_manifest_grounded(_kling([
        "Start on the full composition of the figure on the cross",
        "Cut to the upturned anguished face",
        "Cut to the nailed hand on the crossbeam",
        "Cut to the eclipse ring in the sky",
        "Return to the full composition"]), _MANIFEST)
    assert ok, probs


def test_manifest_grounded_blocks_invented_titulus():
    # the 'BINTX' defect at the PROMPT layer: a beat targeting a titulus absent from the manifest
    ok, probs = V.cutplan_manifest_grounded(_kling([
        "Start on the full composition",
        "Cut to the titulus inscription nailed above his head"]), _MANIFEST)
    assert not ok and any("titulus" in p for p in probs), probs


def test_manifest_grounded_blocks_offmanifest_beat():
    ok, probs = V.cutplan_manifest_grounded(_kling([
        "Cut to a soaring white dove descending"]), _MANIFEST)
    assert not ok, "a beat targeting nothing in the manifest must fail"


def test_manifest_grounded_ignores_unverified_elements():
    # an element present but NOT verified must not be a legal target
    man = {"elements": [{"id": "full", "label": "the full figure", "verified": True},
                        {"id": "dove", "label": "a white dove", "verified": False}]}
    ok, probs = V.cutplan_manifest_grounded(_kling(["Cut to the white dove"]), man)
    assert not ok, "an UNVERIFIED element must not be targetable"


def test_gate_cutplan_runs_manifest_when_supplied():
    plan = {"prompt": "frozen tableau, only the camera reframes, nothing inside the painting moves",
            "beats": [{"description": b} for b in
                      ["full composition", "the face", "the nailed hand", "the eclipse ring",
                       "the titulus sign above", "return to full"]]}
    ok, probs = V.gate_cutplan(plan, manifest=_MANIFEST)
    assert not ok and any("MANIFEST-GROUNDED" in p for p in probs), probs


# ---- element gate aggregation (any-fail, default-pass, hash-pooled) -----------

def test_aggregate_any_fail():
    passed, foreign, split = G.aggregate_votes(
        [{"verdict": "pass"}, {"verdict": "fail", "foreign": ["faceted gem"]}, {"verdict": "pass"}])
    assert not passed and "faceted gem" in foreign and split


def test_aggregate_default_pass_on_unsure():
    passed, _, split = G.aggregate_votes([{"verdict": "pass"}, {"verdict": "unsure"}])
    assert passed and not split, "unsure must default to PASS"


def test_aggregate_all_pass():
    passed, _, split = G.aggregate_votes([{"verdict": "pass"}, {"verdict": "pass"}])
    assert passed and not split


def test_hash_pool_collapses_identical_frames():
    votes = [{"frame_sha": "AAA", "verdict": "pass"}, {"frame_sha": "AAA", "verdict": "pass"},
             {"frame_sha": "BBB", "verdict": "fail", "foreign": ["garbled titulus"]}]
    pooled = G._hash_pool(votes)
    assert len(pooled) == 2, "byte-identical frames must collapse to one verdict"
    passed, foreign, _ = G.aggregate_votes(pooled)
    assert not passed and "garbled titulus" in foreign


def test_element_gate_failclosed_sidecar():
    with tempfile.TemporaryDirectory() as d:
        mp4 = Path(d) / "01_x.mp4"
        mp4.write_bytes(b"")
        assert not G.is_verified(mp4), "no sidecar -> UNVERIFIED (fail-closed)"
        G.record_verdict(mp4, True, note="clean tour")
        assert G.is_verified(mp4)
        G.record_verdict(mp4, False, foreign=["BINTX titulus"])
        assert not G.is_verified(mp4)
        G.record_verdict(mp4, True, audited=False)
        assert not G.is_verified(mp4), "unaudited can never pass (usage-cap hole closed)"


def test_record_from_frame_votes_fails_on_foreign():
    with tempfile.TemporaryDirectory() as d:
        mp4 = Path(d) / "04_x.mp4"
        mp4.write_bytes(b"")
        G.record_from_frame_votes(mp4, [
            {"frame_sha": "a", "verdict": "pass"},
            {"frame_sha": "b", "verdict": "fail", "foreign": ["BINTX titulus"]}])
        assert not G.is_verified(mp4), "a foreign object in any frame fails the clip"


# ---- declare-from-scene-plan (the automated DECLARE step) ---------------------

def test_declare_from_scene_plan():
    import json
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        nbp = root / "visual" / "nbp"
        nbp.mkdir(parents=True)
        (nbp / "01_the-cry.png").write_bytes(b"A")
        (nbp / "02_unified.png").write_bytes(b"B")
        sp = {"plan": {"scenes": [
            {"index": 1, "slug": "the-cry", "title": "The Cry", "viral_role": "hook-open",
             "macro_elements": ["the crying mouth", "the crown of thorns"], "vignettes": []},
            {"index": 2, "slug": "unified", "title": "Unified", "viral_role": "build",
             "macro_elements": [], "vignettes": [{"name": "a"}, {"name": "b"}, {"name": "c"}]},
        ]}}
        (root / "visual" / "scene_plan.json").write_text(json.dumps(sp), encoding="utf-8")
        names = M.declare_from_scene_plan(root)
        assert len(names) == 2, names
        m1 = M.read(nbp / "01_the-cry.png")
        assert m1["role"] == "hook-open" and m1["subject_type"] == "hero"
        assert {e["id"] for e in m1["elements"]} >= {"full"}
        assert not M.is_locked(nbp / "01_the-cry.png"), "declared is UNVERIFIED until reconcile"
        m2 = M.read(nbp / "02_unified.png")
        assert m2["subject_type"] == "multi-story", "3+ vignettes -> multi-story"


def test_declare_from_scene_plan_skips_locked():
    import json
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        nbp = root / "visual" / "nbp"
        nbp.mkdir(parents=True)
        png = nbp / "01_x.png"
        png.write_bytes(b"A")
        M.declare(png, "01_x", [{"id": "full", "label": "full"}])
        M.reconcile_and_lock(png, verified_ids=["full"], period_real=_ALL_PASS)
        sp = {"plan": {"scenes": [{"index": 1, "slug": "x", "title": "X",
                                   "macro_elements": ["a"], "vignettes": []}]}}
        (root / "visual" / "scene_plan.json").write_text(json.dumps(sp), encoding="utf-8")
        names = M.declare_from_scene_plan(root)
        assert M.is_locked(png), "a locked manifest must NOT be clobbered by re-declare"
        assert any("already locked" in n for n in names)


# ---- calibration scoring (the locked discipline) ------------------------------

def test_calibration_discriminates_on_bakeoff():
    # the #03 bake-off truth: direct-Kling #04 invented a titulus (FAIL); the rest are clean
    cases = [{"clip": "04_DIRECT", "truth": "fail", "gate": "fail"},
             {"clip": "04_HF", "truth": "pass", "gate": "pass"},
             {"clip": "01_HF", "truth": "pass", "gate": "pass"},
             {"clip": "01_DIRECT", "truth": "pass", "gate": "pass"}]
    r = G.calibrate(cases)
    assert r["discriminates"] and r["precision"] == 1.0 and r["recall"] == 1.0, r


def test_calibration_flags_overstrict():
    # if the gate failed a GOOD clip, discriminates must be False (precision < 1)
    cases = [{"clip": "a", "truth": "fail", "gate": "fail"},
             {"clip": "b", "truth": "pass", "gate": "fail"}]
    r = G.calibrate(cases)
    assert not r["discriminates"] and r["fp"] == 1, r


# ---- JIT element-gate predicate (gate-then-decide; missing != fail) -----------

def test_is_failed_only_on_recorded_fail():
    with tempfile.TemporaryDirectory() as d:
        mp4 = Path(d) / "01_x.mp4"
        mp4.write_bytes(b"")
        assert not G.is_failed(mp4), "missing sidecar must NOT be a fail (default-PASS / gate-at-pull)"
        G.record_verdict(mp4, True)
        assert not G.is_failed(mp4), "a PASS is not a fail"
        G.record_verdict(mp4, False, foreign=["gem"])
        assert G.is_failed(mp4), "a recorded audited FAIL is a fail"
        G.record_verdict(mp4, True, audited=False)
        assert not G.is_failed(mp4), "unaudited is not a fail"


def test_clip_reuse_excludes_only_recorded_fail():
    # the ACTUAL JIT-gate wiring: is_clean_reusable() consults is_failed(). A clean+coherence-
    # verified source is reusable; a recorded element-gate FAIL drops it; a MISSING verdict does not.
    from pipeline import clip_reuse, coherence
    with tempfile.TemporaryDirectory() as d:
        png = Path(d) / "c.png"
        png.write_bytes(b"IMG")
        mp4 = Path(d) / "c.mp4"
        mp4.write_bytes(b"")
        coherence.record_verdict(png, audited=True, passed=True)        # coherence clean
        entry = {"source": str(mp4)}            # absolute -> ROOT/abs == abs on Windows
        assert clip_reuse.is_clean_reusable(entry), "clean + coherence-verified + no elemgate verdict -> reusable"
        G.record_verdict(mp4, False, foreign=["garbled titulus"])       # recorded element-gate FAIL
        assert not clip_reuse.is_clean_reusable(entry), "a recorded element-gate FAIL must exclude from reuse"
        G.record_verdict(mp4, True, note="re-gated clean")              # now passes
        assert clip_reuse.is_clean_reusable(entry), "a recorded PASS is reusable again"


def test_reuse_swap_writeonce_backup():
    from pipeline import reuse_swap, coherence
    with tempfile.TemporaryDirectory() as d:
        short = Path(d)
        nbp = short / "visual" / "nbp"
        nbp.mkdir(parents=True)
        (nbp / "08_orig.png").write_bytes(b"ORIGINAL-STILL")
        (nbp / "08_orig.mp4").write_bytes(b"ORIGINAL-CLIP")
        srcdir = short / "src"
        srcdir.mkdir()
        for name, body in (("a", b"REUSE-A"), ("b", b"REUSE-B")):
            (srcdir / f"{name}.png").write_bytes(body + b"-STILL")
            (srcdir / f"{name}.mp4").write_bytes(body + b"-CLIP")
            coherence.record_verdict(srcdir / f"{name}.png", audited=True, passed=True)  # real verdict so swap proceeds
        # first swap
        assert reuse_swap.swap(short, 8, srcdir / "a.mp4", log=lambda *a: None)
        assert (nbp / "08_orig.mp4").read_bytes() == b"REUSE-A-CLIP", "slot now carries reuse A"
        assert (nbp / "_pre_reuse" / "08_orig.mp4").read_bytes() == b"ORIGINAL-CLIP", "backup = original"
        # second swap with a DIFFERENT source must NOT overwrite the real original backup
        assert reuse_swap.swap(short, 8, srcdir / "b.mp4", log=lambda *a: None)
        assert (nbp / "08_orig.mp4").read_bytes() == b"REUSE-B-CLIP", "slot now carries reuse B"
        assert (nbp / "_pre_reuse" / "08_orig.mp4").read_bytes() == b"ORIGINAL-CLIP", \
            "write-once: backup must STILL be the true original, not reuse-A"


def test_reuse_swap_failclosed_leaves_slot_untouched():
    # a source with NO coherence verdict must be REFUSED before any file mutation (no half-swap)
    from pipeline import reuse_swap
    with tempfile.TemporaryDirectory() as d:
        short = Path(d)
        nbp = short / "visual" / "nbp"
        nbp.mkdir(parents=True)
        (nbp / "01_x.png").write_bytes(b"ORIG-STILL")
        (nbp / "01_x.mp4").write_bytes(b"ORIG-CLIP")
        src = short / "src"
        src.mkdir()
        (src / "q.png").write_bytes(b"UNVERIFIED-STILL")   # NO coherence verdict on the source
        (src / "q.mp4").write_bytes(b"UNVERIFIED-CLIP")
        ok = reuse_swap.swap(short, 1, src / "q.mp4", log=lambda *a: None)
        assert not ok, "swap must refuse an un-coherence-verified source"
        assert (nbp / "01_x.mp4").read_bytes() == b"ORIG-CLIP", "slot must be UNTOUCHED on refusal"
        assert not (nbp / "_pre_reuse").exists() or not list((nbp / "_pre_reuse").glob("*")), \
            "no backup should be created on a refused swap"


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
