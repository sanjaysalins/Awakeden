"""Unit tests for the v2 deterministic assembly servicer's decision logic (bridge_lib).

Pure, $0, no live bridge run. Run:
  .venv\\Scripts\\python.exe v2\\servicers\\test_servicers.py
"""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bridge_lib as B  # noqa: E402

_PRECHECKS_PASS = """
=== DETERMINISTIC GATE PRE-CHECKS (authoritative on AS-G1..G7) ===
- AS-G1 Timeline Coverage: PASS — 9 slots tile 0->64.14s contiguously.
- AS-G2 No Reuse: PASS — 8 distinct body clips; hero #07 close only.
- AS-G3 Speed/Trim Health: PASS — avg 0.94x, max 2.20x.
- AS-G4 Min Slot: PASS — all >= 0.8s.
- AS-G5 Section Coverage: PASS — hook covered.
- AS-G6 Hero Close: PASS — hero #07 closes.
- AS-G7 Gospel Frame: PASS — lands on Christ.
- AS-G9 Beat Density: CONDITIONAL — 8 moments avg 7.8s.
"""

_PRECHECKS_FAIL = _PRECHECKS_PASS.replace("AS-G2 No Reuse: PASS", "AS-G2 No Reuse: FAIL")

EPISODE_FIT = "<!-- id=1 -->\n# AGENT-BRIDGE REQUEST 0001 — text (assembly-episode-fit)\nYou are a topical-coherence auditor..."
SELF_REVIEW = "# AGENT-BRIDGE REQUEST 0003 — text (text)\nYou are the self-review panel for a 60-second vertical gospel Short's EDIT PLAN.\n" + _PRECHECKS_PASS
SELF_REVIEW_FAIL = "# REQUEST\nYou are the self-review panel for a 60-second vertical gospel Short's EDIT PLAN.\n" + _PRECHECKS_FAIL
INDEPENDENT = "# REQUEST\nYou are a FRESH, INDEPENDENT red-team auditor. You did not build this cut.\n" + _PRECHECKS_PASS
JIGSAW = "# AGENT-BRIDGE REQUEST 0002 — text (text)\nYou are the EDITOR of a 60-second vertical gospel Short. Pin each clip...\nbeat_assignment"
SLOT_VERIFY = "# AGENT-BRIDGE REQUEST 0010 — vision  slot-verify:His Name Is Jesus [SACRED]\n"


def test_classify():
    assert B.classify(EPISODE_FIT) == "episode-fit"
    assert B.classify(SELF_REVIEW) == "self-review"
    assert B.classify(INDEPENDENT) == "independent"
    assert B.classify(JIGSAW) == "jigsaw"
    assert B.classify(SLOT_VERIFY) == "slot-verify"
    assert B.classify("# random\nnothing here") == "other"


def test_prechecks_parse():
    pc = B.parse_prechecks(_PRECHECKS_PASS)
    assert len(pc) == 8, [g for g, _, _ in pc]
    assert pc[0][0].startswith("AS-G1") and pc[0][1] == "PASS"
    assert pc[-1][1] == "CONDITIONAL"


def test_overall_locked_and_revise():
    assert B.overall_from_prechecks(B.parse_prechecks(_PRECHECKS_PASS)) == "LOCKED"
    assert B.overall_from_prechecks(B.parse_prechecks(_PRECHECKS_FAIL)) == "REVISE"
    assert B.overall_from_prechecks([]) == "UNKNOWN"


def test_episode_fit_response():
    action, payload = B.response_for("episode-fit", EPISODE_FIT)
    assert action == "write" and payload == {"offtopic": []}


def test_self_review_locks_when_clean():
    action, payload = B.response_for("self-review", SELF_REVIEW)
    assert action == "write", payload
    assert payload["overall"] == "LOCKED"
    assert len(payload["panel"]) == 6
    # AS-G8 (panel's own call) injected since it's not in the deterministic pre-checks
    assert any(g["gate"].startswith("AS-G8") for g in payload["gates"])


def test_independent_locks_when_clean():
    action, payload = B.response_for("independent", INDEPENDENT)
    assert action == "write" and payload["overall"] == "LOCKED"


def test_review_with_fail_is_left_for_human():
    action, reason = B.response_for("self-review", SELF_REVIEW_FAIL)
    assert action == "skip", f"a FAILing gate must NOT auto-lock; got {action}"


def test_jigsaw_is_skipped():
    action, reason = B.response_for("jigsaw", JIGSAW)
    assert action == "skip" and "semantic" in reason


def test_slot_verify_is_skipped_here():
    action, reason = B.response_for("slot-verify", SLOT_VERIFY)
    assert action == "skip" and "clip_qc" in reason


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
