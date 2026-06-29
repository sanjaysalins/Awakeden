"""Deterministic tests for the bible_kb fail-closed logic (no network / no LLM).

Run: .venv\\Scripts\\python.exe -m pytest test_bible_kb.py -q
"""
from pipeline import bible_kb


def test_uncited_specified_is_downgraded():
    """A 'specified' fact with NO citation can never gate a pass on a guess."""
    f = bible_kb.FactCard(claim="x", bucket="specified", scripture=[])
    bible_kb.hydrate_citations([f])
    assert f.bucket == "constrained"
    assert f.verified is False
    assert "DOWNGRADED" in f.claim


def test_unverifiable_specified_is_downgraded(monkeypatch):
    """A 'specified' fact whose citation can't be fetched is downgraded + flagged."""
    monkeypatch.setattr(bible_kb.scripture, "fetch_kjv", lambda ref: None)
    f = bible_kb.FactCard(claim="y", bucket="specified", scripture=["Nowhere 9:9"])
    bible_kb.hydrate_citations([f])
    assert f.bucket == "constrained"
    assert f.verified is False
    assert f.kjv_text == ""


def test_verified_specified_stays_specified(monkeypatch):
    monkeypatch.setattr(bible_kb.scripture, "fetch_kjv", lambda ref: "And he shall take the two goats")
    f = bible_kb.FactCard(claim="two goats", bucket="specified", scripture=["Leviticus 16:7"])
    bible_kb.hydrate_citations([f])
    assert f.bucket == "specified"
    assert f.verified is True
    assert "two goats" in f.kjv_text


def test_audit_skip_on_error_is_fail_closed(monkeypatch):
    """If the Vision audit errors, the image is flagged needs-review (not passed)."""
    def boom(*a, **k):
        raise RuntimeError("vision down")
    monkeypatch.setattr(bible_kb.agent_bridge, "call_vision", boom)
    a = bible_kb.verify_biblical_accuracy("t", "s", [], [], b"\x89PNG")
    assert a.passed is False
    assert a.skipped is True


def test_free_facts_excluded_from_audit_lines():
    facts = [
        bible_kb.FactCard(claim="spec", bucket="specified", scripture=["Lev 16:7"], kjv_text="x"),
        bible_kb.FactCard(claim="licence", bucket="free", scripture=[]),
    ]
    lines = bible_kb._fact_lines(facts)
    assert "spec" in lines
    assert "licence" not in lines


def test_enrich_appends_only_checkable_directives():
    facts = [
        bible_kb.FactCard(claim="a", bucket="specified", visual_directive="show two goats"),
        bible_kb.FactCard(claim="b", bucket="free", visual_directive="any face"),
    ]
    out = bible_kb.enrich_subject_block("A scene.", facts, [])
    assert "show two goats" in out
    assert "any face" not in out


def test_enrich_for_scene_folds_cited_directives(tmp_path):
    import json
    bc = tmp_path / "_bible_check"
    bc.mkdir()
    facts = {"episode": "T", "world_facts": [
        {"claim": "tent", "bucket": "specified", "scripture": ["Ex 26:1"],
         "visual_directive": "a curtained tent", "verified": True}],
        "scenes": [{"id": 7, "title": "t", "subject_block": "s",
                    "facts": [{"claim": "two goats", "bucket": "specified",
                               "scripture": ["Lev 16:7"], "visual_directive": "show TWO goats together",
                               "verified": True}]}]}
    (bc / "scene_facts.json").write_text(json.dumps(facts), encoding="utf-8")
    subj, banned = bible_kb.enrich_for_scene(tmp_path, 7, "Two goats before the priest.")
    assert "Biblically faithful detail" in subj
    assert "show TWO goats together" in subj          # scene directive folded in
    assert "a curtained tent" in subj                 # specified world directive folded in


def test_enrich_for_scene_noop_without_facts(tmp_path):
    subj, banned = bible_kb.enrich_for_scene(tmp_path, 1, "Untouched.")
    assert subj == "Untouched." and banned == []


def test_only_verified_facts_promote(tmp_path, monkeypatch):
    monkeypatch.setattr(bible_kb, "KB_DIR", tmp_path)
    ep = bible_kb.EpisodeFacts(
        episode="t", source_narration="", source_scene_plan="",
        world_facts=[
            bible_kb.FactCard(claim="good", bucket="specified", scripture=["Lev 16:7"],
                              kjv_text="x", verified=True, entity="day-of-atonement"),
            bible_kb.FactCard(claim="guess", bucket="specified", scripture=[],
                              verified=False, entity="day-of-atonement"),
        ],
    )
    written = bible_kb.promote_to_kb(ep)
    assert len(written) == 1
    import json
    data = json.loads(open(written[0], encoding="utf-8").read())
    claims = [f["claim"] for f in data["facts"]]
    assert "good" in claims
    assert "guess" not in claims
