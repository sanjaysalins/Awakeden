"""Fixture teeth for hook_gate - the planted-bad cases MUST be caught and the good one MUST pass.
Run: .venv\\Scripts\\python.exe -m pytest pipeline/test_hook_gate.py -q
"""
from pipeline.hook_gate import hook_findings, DEFAULTS

GOOD_HOOK = "What if your darkest cry was written down a thousand years before you were born?"
# ~140 spoken words across three blocks, lands on Christ, within the 60s budget.
GOOD_BLOCKS = [
    ("narrator", GOOD_HOOK),
    ("narrator", ("David wrote a song of a forsaken, pierced and mocked man, and a thousand years "
                  "later every line of it came true at one Roman cross outside Jerusalem, watched by "
                  "the very people who unknowingly quoted the psalm as they jeered, proving in their "
                  "own scorn that this dying man was the One the whole song had always been about, the "
                  "promised deliverer the prophets had carried for a thousand long and waiting years, "
                  "the suffering servant whose every wound and every word the Father had set down in "
                  "ink centuries before a single Roman nail was ever forged or driven home.")),
    ("narrator", "He could have come down. He stayed, to deliver you. That is Jesus. Come to Him."),
]
GOOD_META = {"final_total_seconds": 58.0, "target_seconds": 59.0}


def test_good_short_passes_clean():
    blocking, warnings, info = hook_findings(GOOD_META, GOOD_BLOCKS, DEFAULTS)
    assert blocking == []
    assert warnings == [], warnings          # within budget, lands on Christ, ~140 words, no meta hook timing


def test_overlong_short_blocks_on_duration():
    blocking, _, _ = hook_findings({"final_total_seconds": 73.0, "target_seconds": 59.0}, GOOD_BLOCKS)
    assert any("hard ceiling" in b for b in blocking)


def test_slightly_over_target_warns_not_blocks():
    blocking, warnings, _ = hook_findings({"final_total_seconds": 64.0, "target_seconds": 59.0}, GOOD_BLOCKS)
    assert blocking == []
    assert any("tighten toward 60s" in w for w in warnings)


def test_fear_pressure_hook_blocks():
    blocks = [("narrator", "Turn to God now, because time is running out and it will soon be too late."),
              ("narrator", "Jesus is Lord. Come to Him.")]
    blocking, _, _ = hook_findings({"final_total_seconds": 58.0}, blocks)
    assert any("grace-anchored violation" in b and "fear-pressure" in b for b in blocking)


def test_manufactured_hook_warns():
    blocks = [("narrator", "You won't believe what this one verse secretly predicted."),
              ("narrator", "Jesus is the Lamb of God. Come to Him.")]
    _, warnings, _ = hook_findings({"final_total_seconds": 58.0}, blocks)
    assert any("MANUFACTURED" in w for w in warnings)


def test_landing_without_christ_warns():
    blocks = [("narrator", "A thousand-year-old psalm named the cross before it stood."),
              ("narrator", "And that is why the story still matters to every one of us today.")]
    blocking, warnings, _ = hook_findings({"final_total_seconds": 58.0}, blocks)
    assert blocking == []
    assert any("point to Christ" in w for w in warnings)


def test_empty_blocks_block():
    blocking, _, _ = hook_findings({}, [])
    assert blocking and "no spoken blocks" in blocking[0]


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
