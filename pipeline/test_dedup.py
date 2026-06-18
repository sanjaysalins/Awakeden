"""Tests for the dedup + canonical-reuse pass (pipeline/dedup.py).

Run: .venv\\Scripts\\python.exe -m pipeline.test_dedup
"""
from __future__ import annotations
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

from pipeline import coherence
from pipeline import dedup as D


def _img(path: Path, arr: np.ndarray) -> Path:
    Image.fromarray(arr.astype("uint8")).save(path)
    return path


def _gradient(seed: int, noise: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    base = np.tile(np.linspace(0, 255, 64).astype("uint8"), (64, 1))
    if noise:
        base = np.clip(base.astype(int) + rng.integers(-noise, noise + 1, base.shape), 0, 255)
    return base


def test_dhash_stable_and_distinguishing():
    with tempfile.TemporaryDirectory() as d:
        a = _img(Path(d) / "a.png", _gradient(1))
        a2 = _img(Path(d) / "a2.png", _gradient(1, noise=4))      # near-identical
        b = _img(Path(d) / "b.png", np.fliplr(_gradient(1)))      # very different (mirror gradient)
        ha, ha2, hb = D.dhash(a), D.dhash(a2), D.dhash(b)
        assert D.hamming(ha, ha2) <= D.DEFAULT_THRESHOLD, "near-identical must be within threshold"
        assert D.hamming(ha, hb) > D.DEFAULT_THRESHOLD, "a mirror gradient must be far"


def test_slug_strips_index_prefix():
    assert D._slug(Path("x/07_a-thousand-years-apart.png")) == "a-thousand-years-apart"
    assert D._slug(Path("x/the-king.png")) == "the-king"


def test_cluster_groups_lookalikes_and_distinct_names():
    with tempfile.TemporaryDirectory() as d:
        dd = Path(d)
        # two visually-similar stills with DIFFERENT names -> must still cluster (pHash)
        _img(dd / "01_alpha.png", _gradient(2))
        _img(dd / "05_beta.png", _gradient(2, noise=3))
        # an unrelated still -> must NOT join
        _img(dd / "09_gamma.png", np.fliplr(_gradient(2)))
        clusters = D.cluster(list(dd.glob("*.png")))
        assert len(clusters) == 1 and len(clusters[0]) == 2, clusters
        names = {p.name for p in clusters[0]}
        assert names == {"01_alpha.png", "05_beta.png"}, names


def test_cluster_forces_exact_slug_dupes():
    with tempfile.TemporaryDirectory() as d:
        dd = Path(d)
        # same slug, but pixels differ a lot -> still clustered by slug rule
        _img(dd / "01_twin.png", _gradient(3))
        _img(dd / "08_twin.png", np.fliplr(_gradient(3)))
        clusters = D.cluster(list(dd.glob("*.png")), threshold=2)
        assert len(clusters) == 1 and len(clusters[0]) == 2, "same-slug must cluster regardless of pixels"


def test_pick_canonical_prefers_coherence_verified():
    with tempfile.TemporaryDirectory() as d:
        dd = Path(d)
        good = _img(dd / "01_x.png", _gradient(4))
        bad = _img(dd / "05_x.png", _gradient(4, noise=2))
        coherence.record_verdict(good, audited=True, passed=True)   # good is verified
        coherence.record_verdict(bad, audited=True, passed=False, fail_reasons=["floating head"])
        canon = D.pick_canonical([bad, good], flagged=set())
        assert canon == good, "the coherence-verified still must be chosen canonical"


def test_pick_canonical_avoids_flagged():
    with tempfile.TemporaryDirectory() as d:
        dd = Path(d)
        flagged = _img(dd / "01_y.png", _gradient(5))
        clean = _img(dd / "05_y.png", _gradient(5, noise=2))
        # neither verified; the non-flagged one must win
        canon = D.pick_canonical([flagged, clean],
                                 flagged={str(flagged).replace("\\", "/")})
        assert canon == clean, "a flagged-bad still must not be chosen canonical"


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
