"""Tests for the Eleven-Music RECIPE library (Phase-0 tooling).

Locks: recipes (not mp3s) + upsert, the SHARED doctrine gate (imported from music_library/_specs,
single source of truth), approval refuses an out-of-doctrine mood, find_for_beat returns only
APPROVED + doctrine-allowed recipes (never a proposal, never a Suno bed), the locked directive
rides on the recipe.

Run: .venv\\Scripts\\python.exe -m pipeline.test_eleven_music
"""
from __future__ import annotations
import tempfile
from pathlib import Path

from pipeline import eleven_music as EM


def _iso(tmp):
    """Isolate the store to a tempdir (module-level INDEX/STORE)."""
    EM.STORE = Path(tmp)
    EM.INDEX = Path(tmp) / "recipes.json"


def test_recipe_roundtrip_upsert():
    with tempfile.TemporaryDirectory() as d:
        _iso(d)
        EM.add_recipe(EM.ElevenRecipe(slug="x", title="X", lens="Minimalist-Ambient", prompt="p"))
        assert len(EM.load()) == 1
        EM.add_recipe(EM.ElevenRecipe(slug="x", title="X2"))      # upsert by slug, not duplicate
        assert len(EM.load()) == 1 and EM.load()[0]["title"] == "X2"


def test_directive_locked_on_recipe():
    r = EM.ElevenRecipe(slug="x")
    assert r.gain_db == -8.0 and r.outro_s == 2.5
    assert r.directive()["duck_threshold"] == 0.12 and r.directive()["model_id"] == "music_v1"


def test_doctrine_gate_is_shared_specs():
    ba = EM.beat_allowed()
    assert "hook" in ba and "landing" in ba, "the gate is the real Gospel-Five-Beat table"
    import sys
    sys.path.insert(0, "music_library")
    import _specs  # noqa
    assert ba == dict(_specs.BEAT_ALLOWED), "must be the SAME table as music_library (one source)"


def test_find_skips_proposed_and_returns_approved():
    with tempfile.TemporaryDirectory() as d:
        _iso(d)
        EM.add_recipe(EM.ElevenRecipe(slug="p", mood="lament", beat="hook", status="proposed"))
        assert EM.find_for_beat("hook") is None, "a PROPOSED recipe is never selectable"
        EM.add_recipe(EM.ElevenRecipe(slug="a", lens="Minimalist-Ambient", prompt="p"))
        EM.approve("a", mood="lament", beat="hook")               # lament IS allowed for hook
        r = EM.find_for_beat("hook")
        assert r and r["slug"] == "a", "approved + doctrine-allowed recipe is returned"


def test_find_lens_filter():
    with tempfile.TemporaryDirectory() as d:
        _iso(d)
        EM.add_recipe(EM.ElevenRecipe(slug="a", lens="Minimalist-Ambient", prompt="p"))
        EM.approve("a", mood="lament", beat="hook")
        assert EM.find_for_beat("hook", lens="Cinematic") is None, "lens filter excludes the wrong lens"
        assert EM.find_for_beat("hook", lens="Minimalist") is not None


def test_approve_refuses_offdoctrine_mood():
    with tempfile.TemporaryDirectory() as d:
        _iso(d)
        EM.add_recipe(EM.ElevenRecipe(slug="a"))
        try:
            EM.approve("a", mood="glory", beat="hook")            # 'glory' is layer-only, not hook-allowed
            assert False, "must refuse an out-of-doctrine mood/beat pairing"
        except ValueError:
            pass


def test_approve_refuses_unknown_beat():
    with tempfile.TemporaryDirectory() as d:
        _iso(d)
        EM.add_recipe(EM.ElevenRecipe(slug="a"))
        try:
            EM.approve("a", mood="lament", beat="chorus")
            assert False, "must refuse an unknown beat"
        except ValueError:
            pass


def test_find_rejects_mood_wrong_for_THIS_beat():
    # the key doctrine test at the FIND layer: a mood legal for hook must NOT be served on a beat
    # that forbids it (lament is allowed for hook, NOT for 'point').
    with tempfile.TemporaryDirectory() as d:
        _iso(d)
        EM.add_recipe(EM.ElevenRecipe(slug="a", lens="Minimalist-Ambient", prompt="p"))
        EM.approve("a", mood="lament", beat="hook")
        assert EM.find_for_beat("hook") is not None, "legal on its own beat"
        assert EM.find_for_beat("point") is None, "lament must NOT be served on 'point' (doctrine gate)"


def test_approve_refuses_empty_prompt():
    with tempfile.TemporaryDirectory() as d:
        _iso(d)
        EM.add_recipe(EM.ElevenRecipe(slug="blank", prompt="   "))   # whitespace-only prompt
        try:
            EM.approve("blank", mood="lament", beat="hook")
            assert False, "must refuse approving an empty-prompt recipe (would spend on garbage)"
        except ValueError:
            pass


def test_approve_refuses_bad_lens():
    with tempfile.TemporaryDirectory() as d:
        _iso(d)
        EM.add_recipe(EM.ElevenRecipe(slug="x", lens="Jazz-Fusion", prompt="p"))
        try:
            EM.approve("x", mood="lament", beat="hook")
            assert False, "must refuse an unknown lens"
        except ValueError:
            pass


def test_allowed_primary_subtracts_layer_only():
    import sys
    sys.path.insert(0, "music_library")
    import _specs  # noqa
    layer = set(getattr(_specs, "LAYER_ONLY_MOODS", set()))
    for beat in EM.beat_allowed():
        assert not (EM.allowed_primary(beat) & layer), \
            f"layer-only moods must be subtracted from primary-allowed at beat {beat}"


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
