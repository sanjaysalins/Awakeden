"""Fixture teeth for UK-G7 (upload_gates._check_lint): plain-ASCII + grace-anchored + verse front-loaded.
Run: .venv\\Scripts\\python.exe -m pipeline.test_upload_lint
"""
from pipeline.upload_gates import _check_lint, load_specs
from pipeline.upload_models import PlatformMeta, SourceFacts, UploadKit

SPECS = load_specs()


def _kit(title, desc, ref="Psalm 22:7", platform="youtube_short"):
    src = SourceFacts(media_dir="x", video_path="x.mp4", format="short", series_name="s",
                      brand="Awakeden", episode_title="e", anchor_ref=ref, anchor_kjv="",
                      kjv_verified=True, thread="t", thread_lever="l", hook_line="h", spoken_script="")
    return UploadKit(source=src, platforms=[PlatformMeta(platform=platform, label="YT",
                                                         title=title, description=desc)])


def test_clean_copy_passes():
    g = _check_lint(_kit("The Cross Foretold in Psalm 22",
                         "Psalm 22 named the cross a thousand years early. Jesus is Lord. Come to Him."), SPECS)
    assert g.passed, g.detail


def test_em_dash_fails():
    g = _check_lint(_kit("Psalm 22 and the cross",
                         "Psalm 22 foretold it — every line of it. Jesus is Lord. Come to Him."), SPECS)
    assert not g.passed and "typography" in g.detail, g.detail


def test_curly_quote_fails():
    g = _check_lint(_kit("Psalm 22 and the cross",
                         "Psalm 22 foretold the “cross” centuries early. Come to Him."), SPECS)
    assert not g.passed and "typography" in g.detail, g.detail


def test_fear_pressure_copy_fails():
    g = _check_lint(_kit("Psalm 22 and the cross",
                         "Psalm 22 foretold the cross. Turn to Him now before it's too late."), SPECS)
    assert not g.passed and "fear-pressure" in g.detail, g.detail


def test_verse_not_frontloaded_fails():
    desc = ("A thousand years before the cross, a forsaken king wrote the whole scene in vivid detail, "
            "every wound and every word, for the people who would one day stand and read it. Psalm 22. Come to Him.")
    g = _check_lint(_kit("The cross foretold", desc), SPECS)
    assert not g.passed and "first 157 chars" in g.detail, g.detail


if __name__ == "__main__":   # run without pytest (repo convention)
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for t in tests:
        try:
            t(); print(f"[PASS] {t.__name__}"); passed += 1
        except AssertionError as e:
            print(f"[FAIL] {t.__name__}: {e}")
    print(f"\n{passed}/{len(tests)} passed")
    raise SystemExit(0 if passed == len(tests) else 1)
