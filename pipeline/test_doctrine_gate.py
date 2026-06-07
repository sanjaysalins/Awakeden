"""Doctrine-landmine gate tests — every known trap the panel caught LATE must now
be flagged deterministically; clean grace-anchored text must pass.

Run: .venv\\Scripts\\python.exe -m pipeline.test_doctrine_gate
"""
from __future__ import annotations

from pipeline import doctrine_gate as DG


def _hit(text, name):
    return name in [f["landmine"] for f in DG.scan(text)]


def test_inability_concession():
    assert _hit("they were right, He couldn't save Himself", "inability-concession")


def test_broken_bones():
    assert _hit("He was broken in your place", "broken-bones")
    assert not _hit("He was crushed in your place", "broken-bones")  # Isa 53:5 wording is fine


def test_died_of_thirst():
    assert _hit("The God who fills every ocean died of thirst", "died-of-thirst")
    assert not _hit("He cried out in thirst on the cross", "died-of-thirst")


def test_thirst_ps22():
    assert _hit("'I thirst' — Psalm 22 foretold that cry", "thirst-fulfils-ps22")


def test_universalism():
    assert _hit("He looked at the world that nailed Him down and called it brethren", "universalism")
    assert not _hit("the risen Christ is not ashamed to call His own brethren", "universalism")


def test_trinity_severed():
    assert _hit("at the cross the Trinity was torn apart", "trinity-severed")
    assert _hit("God turned His back on His own Son", "trinity-severed")


def test_works_and_fear_and_gainloss():
    assert _hit("just clean yourself up and try harder", "works-selfhelp")
    assert _hit("come to Him before it's too late or you'll burn", "fear-pressure")
    assert _hit("trust Him for your best life and your breakthrough", "gain-loss")


def test_clean_grace_text_passes():
    clean = ("He was forsaken so that you never will be. The risen Christ is not ashamed "
             "to call His own brethren. Come and rest in the One who said it is done.")
    assert DG.scan(clean) == []


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for t in tests:
        try:
            t(); print(f"[PASS] {t.__name__}"); passed += 1
        except AssertionError as e:
            print(f"[FAIL] {t.__name__}: {e}")
    print(f"\n{passed}/{len(tests)} passed")
    raise SystemExit(0 if passed == len(tests) else 1)
