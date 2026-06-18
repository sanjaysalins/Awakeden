"""Tests for the clip-reuse optimization engine (pipeline/clip_reuse.py).

Run: .venv\\Scripts\\python.exe -m pipeline.test_clip_reuse
"""
from __future__ import annotations
import tempfile
from pathlib import Path
from unittest import mock

from pipeline import clip_reuse as R


def _entry(slug, tags, scope="neutral", variant=None, preferred=False, source="x.mp4"):
    return {"slug": slug, "tags": tags, "scope": scope, "jesus_variant": variant,
            "preferred": preferred, "source": source, "title": slug}


def test_rank_orders_by_overlap_and_preferred():
    lib = [
        _entry("a", ["cross", "dawn"], source="a.mp4"),
        _entry("b", ["cross"], preferred=True, source="b.mp4"),
        _entry("c", ["sheep"], source="c.mp4"),
    ]
    with mock.patch.object(R, "_load", return_value=lib), \
         mock.patch.object(R, "is_clean_reusable", return_value=True):
        out = R.rank(["cross", "dawn"], scope="neutral")
        slugs = [e["slug"] for e in out]
        assert "c" not in slugs, "no tag overlap -> excluded"
        # b is preferred (+5) but a has 2 overlaps (*2=4); preferred should rank b first
        assert slugs[0] == "b" and "a" in slugs, slugs


def test_decide_reuse_when_overlap():
    lib = [_entry("a", ["cross", "dawn"], source="a.mp4")]
    with mock.patch.object(R, "_load", return_value=lib), \
         mock.patch.object(R, "is_clean_reusable", return_value=True):
        d = R.decide(["cross"], scope="neutral")
        assert d["action"] == "reuse" and d["slug"] == "a", d


def test_decide_generate_when_no_overlap():
    lib = [_entry("a", ["sheep"], source="a.mp4")]
    with mock.patch.object(R, "_load", return_value=lib), \
         mock.patch.object(R, "is_clean_reusable", return_value=True):
        d = R.decide(["cross"], scope="neutral")
        assert d["action"] == "generate", d


def test_unclean_excluded():
    lib = [_entry("a", ["cross"], source="a.mp4")]
    with mock.patch.object(R, "_load", return_value=lib), \
         mock.patch.object(R, "is_clean_reusable", return_value=False):
        assert R.decide(["cross"])["action"] == "generate", "an unverified clip must not be reused"


def test_no_repeat_within_cut():
    lib = [_entry("a", ["cross"], source="dir/a.mp4")]
    with mock.patch.object(R, "_load", return_value=lib), \
         mock.patch.object(R, "is_clean_reusable", return_value=True):
        d = R.decide(["cross"], exclude_sources={"dir/a.mp4"})
        assert d["action"] == "generate", "an already-used clip must not be reused again in the same cut"


def test_specific_scope_not_returned_by_default_neutral():
    lib = [_entry("a", ["cross"], scope="specific", source="a.mp4")]
    with mock.patch.object(R, "_load", return_value=lib), \
         mock.patch.object(R, "is_clean_reusable", return_value=True):
        assert R.decide(["cross"], scope="neutral")["action"] == "generate", \
            "a story-specific clip must not be reused cross-episode (topical-fit)"
        assert R.decide(["cross"], scope="specific")["action"] == "reuse"


def test_is_clean_reusable_checks_existence():
    with tempfile.TemporaryDirectory() as d:
        # source that doesn't exist under ROOT -> not reusable (quarantine safety)
        assert not R.is_clean_reusable({"source": "does/not/exist.mp4"})


def test_decide_for_scene_matches_tokenized_tag():
    # library tag 'dice-garments' must match a scene whose words contain 'dice'
    lib = [_entry("a", ["dice-garments", "soldier"], source="a.mp4")]
    scene = {"index": 6, "title": "Soldiers Cast Lots", "slug": "06_dice-in-the-dust",
             "visible_elements": "dice in the dust, a seamless garment", "macro_elements": []}
    with mock.patch.object(R, "_load", return_value=lib), \
         mock.patch.object(R, "is_clean_reusable", return_value=True):
        d = R.decide_for_scene(scene, scope="any")
        assert d["action"] == "reuse" and d["hits"] >= 1, d


def test_decide_for_scene_generate_when_unrelated():
    lib = [_entry("a", ["sheep", "shepherd"], source="a.mp4")]
    scene = {"index": 2, "title": "The Mockers", "slug": "02_the-mockers",
             "visible_elements": "a jeering crowd at the cross", "macro_elements": []}
    with mock.patch.object(R, "_load", return_value=lib), \
         mock.patch.object(R, "is_clean_reusable", return_value=True):
        assert R.decide_for_scene(scene, scope="any")["action"] == "generate"


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
