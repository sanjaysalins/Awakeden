"""Golden regression for the Bible-check TEETH (Layer 1 over-reach scan + Layer 3
chokepoint). $0, no network, no LLM — pass KJV text in directly.

If a future change blinds the check, these go RED.

Run: .venv\\Scripts\\python.exe -m pytest test_bible_kb_regression.py -q
"""
import json

from pipeline import bible_kb
from pipeline.bible_kb import FactCard


def _spec(claim, kjv, scripture=("Lev 16:4",), bucket="specified"):
    return FactCard(claim=claim, bucket=bucket, scripture=list(scripture),
                    kjv_text=kjv, verified=True)


# ---- Layer 1: over-reach scan -------------------------------------------------
# KNOWN-BAD — the descriptor is NOT in the cited KJV → MUST be flagged.
def test_white_linen_is_flagged():
    f = _spec("the high priest wore plain white linen",
              "[Lev 16:4] He shall put on the holy linen coat ...")
    flags = bible_kb.over_reach_scan([f])
    assert any(fl["descriptor"] == "white" and fl["category"] == "colour" for fl in flags)


def test_gold_ephod_not_in_verse_is_flagged():
    f = _spec("the high priest's gold-set ephod",
              "[Ex 28:4] a breastplate, and an ephod, and a robe, and a broidered coat",
              scripture=("Ex 28:4",))
    flags = bible_kb.over_reach_scan([f])
    assert any(fl["descriptor"] == "gold" for fl in flags)


def test_wrong_number_is_flagged():
    f = _spec("three goats for the sin offering",
              "[Lev 16:7] And he shall take the two goats ...", scripture=("Lev 16:7",))
    flags = bible_kb.over_reach_scan([f])
    assert any(fl["descriptor"] == "three" and fl["category"] == "number" for fl in flags)


# KNOWN-GOOD — the descriptor IS in the cited KJV → MUST pass clean.
def test_two_goats_passes():
    f = _spec("two goats taken together", "[Lev 16:7] And he shall take the two goats ...",
              scripture=("Lev 16:7",))
    assert bible_kb.over_reach_scan([f]) == []


def test_gold_cherubim_passes():
    f = _spec("a gold lid bearing two cherubim of beaten gold",
              "[Ex 25:18] two cherubims of gold, of beaten work shalt thou make them",
              scripture=("Ex 25:18",))
    assert bible_kb.over_reach_scan([f]) == []


def test_golden_normalizes_to_gold():
    f = _spec("the golden mercy seat", "[Ex 25:17] thou shalt make a mercy seat of pure gold",
              scripture=("Ex 25:17",))
    assert bible_kb.over_reach_scan([f]) == []


def test_twelve_stones_passes():
    f = _spec("a breastplate set with twelve stones",
              "[Ex 28:21] the stones shall be ... twelve, according to the names",
              scripture=("Ex 28:21",))
    assert bible_kb.over_reach_scan([f]) == []


# NO false positives / correct scoping
def test_sacred_does_not_trigger_red():
    f = _spec("the sacred tent at dawn", "[Ex 40:2] set up the tabernacle of the tent")
    assert bible_kb.over_reach_scan([f]) == []   # 'sacred' is one token, not 'red'


def test_negated_descriptor_not_flagged():
    # "not plain white" is a guard against white, not a claim the veil IS white.
    f = _spec("a coloured curtain of blue, purple and scarlet, not plain white",
              "[Ex 26:31] blue, and purple, and scarlet, and fine twined linen",
              scripture=("Ex 26:31",))
    assert bible_kb.over_reach_scan([f]) == []


def test_constrained_and_free_are_not_scanned():
    bad = "white linen"
    kjv = "[Lev 16:4] He shall put on the holy linen coat"
    assert bible_kb.over_reach_scan([_spec(bad, kjv, bucket="constrained")]) == []
    assert bible_kb.over_reach_scan([_spec(bad, kjv, bucket="free")]) == []


def test_no_kjv_text_is_skipped_here():
    f = FactCard(claim="white linen", bucket="specified", scripture=["Lev 16:4"],
                 kjv_text="", verified=False)
    assert bible_kb.over_reach_scan([f]) == []   # hydration gate's job, not this one


# ---- Layer 3: chokepoint ------------------------------------------------------
def _build_v1(tmp_path, *, audit_passed=True, with_audit=True, cover=True,
              over_reach=False, verified=True, bind_plan=True,
              good_image_hash=True, good_facts_hash=True):
    """Build a fake episode whose facts + sidecar are correctly hash-BOUND, then
    let individual flags break one thing at a time."""
    v1 = tmp_path / "v1"
    vis = v1 / "visual_16x9"
    bc = v1 / "_bible_check"
    vis.mkdir(parents=True)
    bc.mkdir(parents=True)
    (vis / "scene_plan.json").write_text(json.dumps({"scenes": [{"id": 1, "title": "t"}]}),
                                         encoding="utf-8")
    png = vis / "01_scene.png"
    png.write_bytes(b"\x89PNG-bytes")
    claim = ("white linen" if over_reach else "two goats together")
    kjv = ("[Lev 16:4] He shall put on the holy linen coat" if over_reach
           else "[Lev 16:7] And he shall take the two goats")
    facts = {
        "episode": "T", "source_narration": "", "source_scene_plan": "",
        "world_facts": [],
        "scenes": [{"id": (1 if cover else 9), "title": "t", "subject_block": "s",
                    "facts": [{"claim": claim, "bucket": "specified",
                               "scripture": ["Lev 16:7"], "kjv_text": kjv,
                               "verified": verified, "entity": ""}]}],
    }
    if bind_plan:
        facts["scene_plan_sha256"] = bible_kb.sha_file(vis / "scene_plan.json")
    (bc / "scene_facts.json").write_text(json.dumps(facts), encoding="utf-8")

    if with_audit:
        ep = bible_kb.EpisodeFacts.from_json(facts)
        scene = ep.scenes[0]
        img_sha = bible_kb.sha_bytes(png.read_bytes()) if good_image_hash else "deadbeef"
        facts_sha = bible_kb.scene_facts_sha(scene) if good_facts_hash else "deadbeef"
        (vis / "01_scene.bib_audit.json").write_text(
            json.dumps({"passed": audit_passed, "skipped": False,
                        "image_sha256": img_sha, "facts_sha256": facts_sha}), encoding="utf-8")
    return v1


def test_chokepoint_green(tmp_path):
    st = bible_kb.check_status(_build_v1(tmp_path))
    assert st.ok, st.reasons


def test_chokepoint_blocks_missing_audit(tmp_path):
    st = bible_kb.check_status(_build_v1(tmp_path, with_audit=False))
    assert not st.ok and st.missing_audit == [1]


def test_chokepoint_blocks_failed_audit(tmp_path):
    st = bible_kb.check_status(_build_v1(tmp_path, audit_passed=False))
    assert not st.ok and st.failed_audit == [1]


def test_chokepoint_blocks_coverage_gap(tmp_path):
    st = bible_kb.check_status(_build_v1(tmp_path, cover=False))
    assert not st.ok and st.missing_facts == [1]


def test_chokepoint_blocks_over_reach(tmp_path):
    st = bible_kb.check_status(_build_v1(tmp_path, over_reach=True))
    assert not st.ok and st.over_reach


def test_chokepoint_blocks_unverified_specified(tmp_path):
    st = bible_kb.check_status(_build_v1(tmp_path, verified=False))
    assert not st.ok and st.unverified_specified == 1


def test_chokepoint_blocks_unbound_facts(tmp_path):
    # scene_facts.json with no scene_plan_sha256 = not bound = stale
    st = bible_kb.check_status(_build_v1(tmp_path, bind_plan=False))
    assert not st.ok and st.stale


def test_chokepoint_blocks_changed_scene_plan(tmp_path):
    v1 = _build_v1(tmp_path)
    (v1 / "visual_16x9" / "scene_plan.json").write_text(
        json.dumps({"scenes": [{"id": 1, "title": "CHANGED"}]}), encoding="utf-8")
    st = bible_kb.check_status(v1)
    assert not st.ok and st.stale            # hash mismatch detected


def test_chokepoint_blocks_stale_sidecar_facts(tmp_path):
    # audit ran against a DIFFERENT fact set (facts edited since) → stale audit
    st = bible_kb.check_status(_build_v1(tmp_path, good_facts_hash=False))
    assert not st.ok and st.stale_audit == [1]


def test_chokepoint_blocks_tampered_sidecar(tmp_path):
    # a hand-written passed=true sidecar whose image hash doesn't match the PNG
    st = bible_kb.check_status(_build_v1(tmp_path, good_image_hash=False))
    assert not st.ok and st.stale_audit == [1]


def test_assert_green_raises_when_not_green(tmp_path):
    import pytest
    with pytest.raises(RuntimeError):
        bible_kb.assert_green(_build_v1(tmp_path, audit_passed=False), stage="lock")
