"""Tests for pipeline/release_state.py — the SYNC gates (SYNC-G1..G7).

run_gates() is pure over PieceState, so most cases need no filesystem."""
from __future__ import annotations

from pathlib import Path

import pytest

from pipeline import finality, release_state
from pipeline.release_state import PieceState, run_gates


def hits(findings, gate, slug, lvl=None):
    return [f for f in findings if f[0] == gate and f[2] == slug
            and (lvl is None or f[1] == lvl)]


def _shipped(**kw) -> PieceState:
    base = dict(slug="p", status="studio_complete", source_dir=Path("x"),
                finality=finality.FINAL_SFX, video=Path("x/v_sfx.mp4"), video_sha="S",
                pack_exists=True, pack_sha="S", thumbs_exist=True, thumbs_sha="S")
    base.update(kw)
    return PieceState(**base)


# ---- SYNC-G1 join -----------------------------------------------------------
def test_g1_shipped_without_join_fails():
    f = run_gates([PieceState(slug="p", status="studio_complete")], [])
    assert hits(f, "SYNC-G1", "p", "FAIL")


def test_g1_in_production_without_join_warns_planned_silent():
    f = run_gates([PieceState(slug="a", status="in_production"),
                   PieceState(slug="b", status="planned")], [])
    assert hits(f, "SYNC-G1", "a", "WARN") and not hits(f, "SYNC-G1", "b")


def test_g1_every_dangling_source_field_fails():
    s = PieceState(slug="p", status="planned", dangling=["source", "study_source"])
    assert len(hits(run_gates([s], []), "SYNC-G1", "p", "FAIL")) == 2


def test_g1_orphan_lane_piece_warns():
    assert hits(run_gates([], ["stray_folder"]), "SYNC-G1", "stray_folder", "WARN")


# ---- SYNC-G2 finality -------------------------------------------------------
def test_g2_shipped_without_final_fails():
    s = PieceState(slug="p", status="studio_complete", source_dir=Path("x"),
                   finality=finality.NEEDS_SFX, video=Path("x/v_scored.mp4"))
    assert hits(run_gates([s], []), "SYNC-G2", "p", "FAIL")


# ---- SYNC-G3/G4 pack + thumbs freshness --------------------------------------
def test_g3_pack_missing_unstamped_stale():
    assert hits(run_gates([_shipped(pack_exists=False)], []), "SYNC-G3", "p", "FAIL")
    assert hits(run_gates([_shipped(pack_sha="")], []), "SYNC-G3", "p", "FAIL")
    assert hits(run_gates([_shipped(pack_sha="OLD")], []), "SYNC-G3", "p", "FAIL")
    assert not hits(run_gates([_shipped()], []), "SYNC-G3", "p")


def test_g4_thumbs_warn_when_studio_fail_when_live():
    assert hits(run_gates([_shipped(thumbs_exist=False)], []), "SYNC-G4", "p", "WARN")
    live = _shipped(status="live", youtube_id="A" * 11, thumbs_exist=False,
                    ledger={"youtube": {"url": "u", "posted": "2026-07-15",
                                        "video_id": "A" * 11, "final_sha": "S"}})
    assert hits(run_gates([live], []), "SYNC-G4", "p", "FAIL")


# ---- SYNC-G5 website ---------------------------------------------------------
def test_g5_read_url_mismatch_fails():
    s = _shipped(read_page=True, has_read_source=True,
                 read_url_meta="https://awakeden.com/read/WRONG.html")
    assert hits(run_gates([s], []), "SYNC-G5", "p", "FAIL")


def test_g5_stale_read_frames_warn():
    s = _shipped(read_page=True, has_read_source=True,
                 read_url_meta="https://awakeden.com/read/p.html",
                 read_video=Path("x/v_scored.mp4"), read_video_sha="NEW", read_meta_sha="OLD")
    assert hits(run_gates([s], []), "SYNC-G5", "p", "WARN")


def test_g5_read_page_without_read_source_warns():
    # red-team M5: deleting read_source silently disarmed frame freshness
    s = _shipped(read_page=True, has_read_source=False,
                 read_url_meta="https://awakeden.com/read/p.html")
    assert hits(run_gates([s], []), "SYNC-G5", "p", "WARN")


def test_g5_orphan_read_page_warns():
    f = run_gates([], [], ["ghost-page"])
    assert hits(f, "SYNC-G5", "ghost-page", "WARN")


# ---- SYNC-G6 published coherence (must fire even with NO folder/video) -------
def test_g6_youtube_id_without_ledger_fails_even_without_folder():
    s = PieceState(slug="p", status="live", youtube_id="A" * 11)  # no source_dir at all
    f = run_gates([s], [])
    assert hits(f, "SYNC-G6", "p", "FAIL")


def test_g6_live_without_youtube_id_fails():
    assert hits(run_gates([_shipped(status="live")], []), "SYNC-G6", "p", "FAIL")


def test_g6_youtube_id_but_not_live_fails():
    s = _shipped(youtube_id="A" * 11,
                 ledger={"youtube": {"url": "u", "posted": "d", "video_id": "A" * 11}})
    assert hits(run_gates([s], []), "SYNC-G6", "p", "FAIL")


def test_g6_posted_sha_divergence_fails():
    s = _shipped(status="live", youtube_id="A" * 11,
                 ledger={"youtube": {"url": "u", "posted": "d", "video_id": "A" * 11,
                                     "final_sha": "DIFFERENT"}})
    assert hits(run_gates([s], []), "SYNC-G6", "p", "FAIL")


def test_g6_clean_live_piece_is_silent():
    s = _shipped(status="live", youtube_id="A" * 11, read_page=True,
                 has_read_source=True,
                 read_url_meta="https://awakeden.com/read/p.html",
                 ledger={"youtube": {"url": "u", "posted": "2026-07-15",
                                     "video_id": "A" * 11, "final_sha": "S"}})
    assert not [x for x in run_gates([s], []) if x[1] == "FAIL"]


def test_g6_ledger_entry_without_manifest_youtube_id_fails():
    # red-team M1/M3: the interrupted --set half-state was invisible and the
    # piece re-listed as not-yet-uploaded -> double upload
    s = _shipped(ledger={"youtube": {"url": "u", "posted": "d",
                                     "video_id": "A" * 11, "final_sha": "S"}})
    assert hits(run_gates([s], []), "SYNC-G6", "p", "FAIL")


def test_g6_ledger_entry_without_final_sha_warns():
    s = _shipped(status="live", youtube_id="A" * 11,
                 ledger={"youtube": {"url": "u", "posted": "d", "video_id": "A" * 11}})
    assert hits(run_gates([s], []), "SYNC-G6", "p", "WARN")


# ---- SYNC-G2 rivals / SYNC-G3 copy staleness ----------------------------------
def test_g2_rival_finals_warn():
    s = _shipped(rivals=["A_scored_sfx_captioned.mp4"])
    assert hits(run_gates([s], []), "SYNC-G2", "p", "WARN")


def test_g3_copy_authored_against_older_final_warns():
    # red-team M1: a bare --index restamp must not launder unreviewed copy
    s = _shipped(pack_copy_sha="OLD")
    assert hits(run_gates([s], []), "SYNC-G3", "p", "WARN")
    assert not hits(run_gates([_shipped(pack_copy_sha="S")], []), "SYNC-G3", "p")


# ---- SYNC-G7 long<->short (manifest-only: fires with no folder) ---------------
def test_g7_cluster_long_requires_parent_even_without_folder():
    long = PieceState(slug="the-long", kind="long", cluster="c1", status="in_production")
    short = PieceState(slug="the-short", kind="short", cluster="c1", status="planned")
    assert hits(run_gates([long, short], []), "SYNC-G7", "the-short", "FAIL")


def test_g7_parent_must_exist_and_be_long():
    a = PieceState(slug="a", kind="short", parent="ghost")
    assert hits(run_gates([a], []), "SYNC-G7", "a", "FAIL")
    b = PieceState(slug="b", kind="short", parent="c")
    c = PieceState(slug="c", kind="short")
    assert hits(run_gates([b, c], []), "SYNC-G7", "b", "FAIL")


def test_g7_correct_parent_is_silent():
    long = PieceState(slug="the-long", kind="long", cluster="c1")
    short = PieceState(slug="s", kind="short", cluster="c1", parent="the-long")
    assert not hits(run_gates([long, short], []), "SYNC-G7", "s")


def test_g7_mismatched_cluster_fails_even_when_short_cluster_is_none():
    # red-team 2026-07-15: the FIRST G7 block only fires when s.cluster already
    # matches some long's cluster, so cluster: null + a typo'd/copy-pasted
    # parent: sailed through undetected. This is the second, independent check.
    long = PieceState(slug="the-long", kind="long", cluster="psalm-22")
    stray = PieceState(slug="stray", kind="short", cluster=None, parent="the-long")
    assert hits(run_gates([long, stray], []), "SYNC-G7", "stray", "FAIL")


# ---- hard join (the ew-jonah false-FINAL regression) --------------------------
def test_resolve_source_no_fuzzy_ever(tmp_path, monkeypatch):
    monkeypatch.setattr(release_state, "SITE", tmp_path / "_website")
    (tmp_path / "_website").mkdir()
    (tmp_path / "batches" / "sign_of_jonah").mkdir(parents=True)
    # ew-jonah names NO source field -> must resolve to nothing, never letter-match
    assert release_state.resolve_source({"slug": "ew-jonah"}) == (None, None)


def test_resolve_source_precedence_and_dangling(tmp_path, monkeypatch):
    monkeypatch.setattr(release_state, "SITE", tmp_path / "_website")
    (tmp_path / "_website").mkdir()
    (tmp_path / "real").mkdir()
    d, join = release_state.resolve_source({"source": "../real", "read_source": "../gone"})
    assert join == "source" and d == (tmp_path / "real").resolve()
    d, join = release_state.resolve_source({"source": "../gone"})
    assert d is None and join == "source"  # named-but-missing keeps the field name


# ---- to_post queue -----------------------------------------------------------
def test_to_post_long_first_then_cluster_order():
    long = _shipped(slug="L", kind="long", cluster="c1")
    s2 = _shipped(slug="s2", cluster="c1", cluster_order=2)
    s1 = _shipped(slug="s1", cluster="c1", cluster_order=1)
    q = release_state.to_post([s2, long, s1])
    assert [s.slug for s, _ in q] == ["L", "s1", "s2"]
    assert q[0][1] == ["youtube"]                      # long posts YouTube only
    assert q[1][1] == release_state.PLATFORMS          # shorts post all four


def test_to_post_skips_unshipped_and_posted():
    posted = _shipped(slug="done", ledger={p: {"url": "u", "posted": "d"}
                                           for p in release_state.PLATFORMS})
    unfinished = _shipped(slug="wip", finality=finality.NEEDS_SFX)
    planned = PieceState(slug="idea", status="planned")
    assert release_state.to_post([posted, unfinished, planned]) == []


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-q"]))
