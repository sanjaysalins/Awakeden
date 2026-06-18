"""Regression tests for the validation engine (see VALIDATION_ENGINE_PLAN.md).

Locks in the 2026-06-14 fixes so they cannot silently regress:
  - the viral crop-cut edit (vs the slow-zoom over-correction)
  - the image-grounded cut-plan (vs the rich-text hallucination seed)
  - the period/tone + text + anatomy checks in verify_image
  - the rules.json registry integrity

Run: .venv\\Scripts\\python.exe -m pipeline.test_validation
"""
from __future__ import annotations
import json
from pathlib import Path

from pipeline import validators as V

FX = Path(__file__).resolve().parent / "validation_fixtures"


def _load(name: str) -> dict:
    return json.loads((FX / name).read_text(encoding="utf-8"))


# ---- CLIP-VIRAL: crop-cuts required, slow zoom rejected -----------------------

def test_slowzoom_fails_viral():
    ok, reason = V.cutplan_viral(_load("cutplan_slowzoom_bad.json"))
    assert not ok, f"slow-zoom should FAIL viral check; got pass ({reason})"


def test_richtext_passes_viral_but_fails_grounding():
    # the old rich-text plan DID have crop-cut beats (viral ok) ...
    ok, _ = V.cutplan_viral(_load("cutplan_richtext_bad.json"))
    assert ok, "rich-text plan has 6 crop-cut beats; viral check should pass"


def test_cropcut_clean_passes_viral():
    ok, reason = V.cutplan_viral(_load("cutplan_cropcut_clean_good.json"))
    assert ok, f"clean crop-cut plan should PASS viral; got fail ({reason})"


# ---- CLIP-IMAGE-GROUNDED: no rich-text injection -----------------------------

def test_richtext_fails_grounding():
    ok, reason = V.cutplan_image_grounded(_load("cutplan_richtext_bad.json"))
    assert not ok, f"rich-text plan should FAIL grounding; got pass ({reason})"


def test_slowzoom_passes_grounding():
    # slow zoom is image-grounded (no rich text) — it fails only the VIRAL check.
    ok, _ = V.cutplan_image_grounded(_load("cutplan_slowzoom_bad.json"))
    assert ok, "slow-zoom has the anti-invention clause and no rich text; grounding should pass"


def test_cropcut_clean_passes_grounding():
    ok, reason = V.cutplan_image_grounded(_load("cutplan_cropcut_clean_good.json"))
    assert ok, f"clean crop-cut plan should PASS grounding; got fail ({reason})"


# ---- the real servicer output must satisfy both checks -----------------------

def test_live_servicer_cutplan_is_viral_and_grounded():
    """Build a cut-plan via the live _gen_servicer.build_cutplan and assert it passes both
    deterministic clip rules. Catches a future edit that breaks the servicer."""
    # the servicer reads env (SHORT_DIR) + scene_plan at import; exec ONLY the NEG
    # constant and the build_cutplan function (skip the PLAN/SCENES loading block).
    src = (Path(__file__).resolve().parent.parent / ".agent_bridge" / "_gen_servicer.py").read_text(encoding="utf-8")
    neg_block = src[src.index("NEG ="):src.index("\nPACE_HDR")]
    func_block = src[src.index("def build_cutplan"):src.index("\ndef title_line")]
    ns: dict = {"re": __import__("re")}
    exec(neg_block + "\n" + func_block, ns)
    scene = {"macro_elements": ["the bowed head", "the nailed hand", "the dark sky", "the cross beam"],
             "subject_block": "a crucified man, blood on his side, warm lamplight spilling",
             "mood_block": "reverent", "emotional_tone": "grief", "pacing": "slower"}
    cp = ns["build_cutplan"](scene)
    ok1, r1 = V.cutplan_viral(cp)
    ok2, r2 = V.cutplan_image_grounded(cp)
    assert ok1, f"live servicer cut-plan not viral: {r1}"
    assert ok2, f"live servicer cut-plan not image-grounded: {r2}"


# ---- CLIP-NOWRITING: never animate a writing surface (INV-17) ----------------

def test_writing_scene_fails_animate():
    scene = {"title": "The First Line, Centuries Early",
             "subject_block": "an open scroll on a wooden table, the verse inscribed in dark Hebrew lettering across the parchment"}
    ok, reason = V.never_animate_writing(scene)
    assert not ok, f"a scroll/inscription scene must FAIL the animate guard; got pass ({reason})"


def test_illegible_writing_scene_passes_animate():
    scene = {"title": "The Titulus",
             "subject_block": "a crucifixion titulus above the cross, the lettering reduced to abstract illegible marks, no readable words"}
    ok, reason = V.never_animate_writing(scene)
    assert ok, f"an explicitly-illegible titulus is safe to animate; got fail ({reason})"


def test_normal_scene_passes_animate():
    scene = {"title": "The Cross, Foretold",
             "subject_block": "the crucified Christ lifted on a rough wooden cross against a darkening sky, head bowed"}
    ok, reason = V.never_animate_writing(scene)
    assert ok, f"a normal crucifixion scene has no writing subject; got fail ({reason})"


def test_negated_writing_mention_passes_animate():
    # explicitly EXCLUDING writing must not false-flag (found by the v2 Isaiah-53 build)
    for sb in ("the top of the cross bare and plain with no inscription board and no titulus and no lettering of any kind",
               "an aged prophet gazing at a dim far figure, no writing or scroll present"):
        ok, reason = V.never_animate_writing({"title": "x", "subject_block": sb})
        assert ok, f"an explicit 'no scroll/titulus' exclusion must pass; got fail ({reason})"


# ---- NARRATIVE-PRESENCE hard gate (invented-narrative-detail) ----------------

def test_narrative_presence_blocks_peter_watching():
    ok, fails = V.narrative_presence(
        "And Peter, who stood near enough to watch that scourging, reached back to Isaiah's words.")
    assert not ok and any("Peter" in f for f in fails), fails


def test_narrative_presence_blocks_matthew_watching():
    ok, fails = V.narrative_presence(
        "At the cross, Matthew watched it happen — the passers-by mocking and wagging their heads.")
    assert not ok and any("Matthew" in f for f in fails), fails


def test_narrative_presence_passes_fixed_versions():
    # the corrected drafts must PASS (no false-positive block)
    for spoken in (
        "And the apostle Peter took up Isaiah's words and laid them on Christ at the cross.",
        "At the cross, Matthew's gospel records it — the rulers sneering and the mockers wagging their heads.",
    ):
        ok, fails = V.narrative_presence(spoken)
        assert ok, f"fixed draft wrongly blocked: {fails}"


def test_narrative_presence_passes_true_eyewitness():
    # John WAS at the cross (John 19:26) and is not listed -> never trips
    ok, fails = V.narrative_presence(
        "A thousand years later, John watched it at the cross — soldiers dividing Jesus' clothes.")
    assert ok, f"a true eyewitness claim must pass; got {fails}"


# ---- verify_image criteria guard --------------------------------------------

def test_verify_image_has_period_tone_criteria():
    ok, reason = V.prompt_has_criteria()
    assert ok, reason


# ---- rules registry integrity -----------------------------------------------

def test_rules_integrity():
    ok, problems = V.rules_integrity()
    assert ok, "rules.json problems:\n  " + "\n  ".join(problems)


def test_rules_have_expected_core_ids():
    ids = {r["id"] for r in V.load_rules()}
    for need in ("IMG-PERIOD", "IMG-NOTEXT", "CLIP-FROZEN", "CLIP-VIRAL", "CLIP-IMAGE-GROUNDED"):
        assert need in ids, f"rules.json missing core rule {need}"


# ---- gate_cutplan (the submit gate wired into the servicer) ------------------

def test_gate_blocks_slowzoom():
    ok, problems = V.gate_cutplan(_load("cutplan_slowzoom_bad.json"))
    assert not ok and any("CLIP-VIRAL" in p for p in problems), problems


def test_gate_blocks_richtext():
    ok, problems = V.gate_cutplan(_load("cutplan_richtext_bad.json"))
    assert not ok and any("CLIP-IMAGE-GROUNDED" in p for p in problems), problems


def test_gate_passes_clean():
    ok, problems = V.gate_cutplan(_load("cutplan_cropcut_clean_good.json"))
    assert ok, problems


# ---- clip_qc fail-closed sidecar --------------------------------------------

def test_clipqc_is_failclosed():
    import tempfile
    from pipeline import clip_qc as Q
    with tempfile.TemporaryDirectory() as d:
        fake = Path(d) / "07_test.mp4"
        fake.write_bytes(b"")  # not a real clip; we only test the sidecar gate
        assert not Q.is_verified(fake), "no sidecar must be UNVERIFIED (fail-closed)"
        Q.record_verdict(fake, passed=True, note="looked, frozen + on-scene")
        assert Q.is_verified(fake), "passing sidecar -> verified"
        Q.record_verdict(fake, passed=False, note="melted hand")
        assert not Q.is_verified(fake), "failing sidecar -> not verified"


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
