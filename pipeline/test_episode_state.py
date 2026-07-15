"""Tests for pipeline/episode_state.py — the Episode unit of work.

Includes regression tests for the 2026-07-15 red-team findings: `status` must
never contradict `long_ready` (a confirmed live bug — the board said "ready to
release" while the tracker correctly said "not yet marked ready" for the SAME
Psalm 22 episode, because status checked bare finality instead of
long_ready); "shorts building" must not claim progress on untouched shorts;
a LIVE long whose final regresses must never silently read as "in production"."""
from __future__ import annotations

import pytest

from pipeline import finality
from pipeline.episode_state import EpisodeState, gather_episodes, standalone_shorts
from pipeline.release_state import PieceState


def _long(slug="the-long", built=True, posted=False, catalogue_ready=None) -> PieceState:
    # catalogue_ready defaults to following `built` (the common case: finality
    # and public_status move together) but can be forced apart to test drift
    ready = built if catalogue_ready is None else catalogue_ready
    return PieceState(slug=slug, kind="long", title="The Long",
                      finality=finality.FINAL_SFX if built else finality.NO_VIDEO,
                      status="studio_complete" if ready else "in_production",
                      youtube_id="X" * 11 if posted else None)


def _short(slug, parent="the-long", order=1, built=True, posted_all=False, planned=False) -> PieceState:
    s = PieceState(slug=slug, kind="short", title=slug, parent=parent, cluster_order=order,
                   finality=finality.FINAL_SFX if built else finality.NEEDS_SFX,
                   status="planned" if planned else ("studio_complete" if built else "in_production"))
    if posted_all:
        s.ledger = {p: {"url": "u"} for p in s.post_platforms}
    return s


# ---- gather_episodes ----------------------------------------------------------
def test_no_shorts_no_episode():
    assert gather_episodes([_long()]) == []


def test_one_short_makes_an_episode():
    eps = gather_episodes([_long(), _short("s1")])
    assert len(eps) == 1 and eps[0].slug == "the-long" and len(eps[0].shorts) == 1


def test_shorts_without_a_real_long_are_ignored():
    # parent points at a slug that isn't kind=long in the state set (SYNC-G7's job to flag)
    eps = gather_episodes([_short("s1", parent="ghost")])
    assert eps == []


def test_shorts_sorted_by_cluster_order():
    eps = gather_episodes([_long(), _short("s3", order=3), _short("s1", order=1), _short("s2", order=2)])
    assert [s.slug for s in eps[0].shorts] == ["s1", "s2", "s3"]


def test_standalone_shorts_excluded_from_episodes():
    states = [_long(), _short("s1"), PieceState(slug="lonely", kind="short", parent=None)]
    eps = gather_episodes(states)
    assert len(eps[0].shorts) == 1
    assert [s.slug for s in standalone_shorts(states)] == ["lonely"]


# ---- EpisodeState status/progress ----------------------------------------------
def test_status_long_in_production():
    ep = EpisodeState(slug="x", long=_long(built=False), shorts=[])
    assert ep.status == "long in production"


def test_status_long_done_no_shorts():
    ep = EpisodeState(slug="x", long=_long(), shorts=[])
    assert ep.status == "long done, no shorts yet"


def test_status_shorts_building():
    ep = EpisodeState(slug="x", long=_long(),
                      shorts=[_short("a", built=True), _short("b", built=False)])
    assert ep.status.startswith("shorts building")
    assert ep.shorts_built == 1 and ep.shorts_total == 2


def test_status_ready_to_release():
    ep = EpisodeState(slug="x", long=_long(built=True, posted=False),
                      shorts=[_short("a", built=True), _short("b", built=True)])
    assert ep.status == "built, ready to release"


def test_status_complete_requires_long_and_every_short_posted():
    ep = EpisodeState(slug="x", long=_long(built=True, posted=True),
                      shorts=[_short("a", built=True, posted_all=True),
                              _short("b", built=True, posted_all=True)])
    assert ep.is_complete
    assert ep.shorts_posted == 2


def test_status_partially_released():
    ep = EpisodeState(slug="x", long=_long(built=True, posted=True),
                      shorts=[_short("a", built=True, posted_all=True),
                              _short("b", built=True, posted_all=False)])
    assert not ep.is_complete
    assert "releasing" in ep.status
    assert ep.shorts_posted == 1


# ---- red-team regressions, 2026-07-15 -------------------------------------------
def test_status_never_contradicts_long_ready():
    # the confirmed live bug: finality FINAL but public_status still
    # in_production must NOT advance past "awaiting approval" / "in production"
    ep = EpisodeState(slug="x", long=_long(built=True, catalogue_ready=False),
                      shorts=[_short("a", built=True), _short("b", built=True)])
    assert not ep.long_ready
    assert "ready to release" not in ep.status
    assert "COMPLETE" not in ep.status
    assert "awaiting catalogue approval" in ep.status


def test_status_long_ready_false_blocks_even_with_finished_shorts():
    # every OTHER condition for "built, ready to release" is true except
    # catalogue approval - status must still refuse to say it's ready
    ep = EpisodeState(slug="x", long=_long(built=True, catalogue_ready=False), shorts=[])
    assert ep.status == "long in production" or "awaiting" in ep.status
    assert ep.status != "built, ready to release"


def test_status_distinguishes_untouched_from_in_progress_shorts():
    # a short sitting at status=planned with nothing done must not read as
    # "building" (implies active work) the same as one actually mid-pipeline
    untouched = EpisodeState(slug="x", long=_long(),
                             shorts=[_short("a", built=True), _short("b", built=False, planned=True)])
    assert "planned, none started" in untouched.status

    in_progress = EpisodeState(slug="x", long=_long(),
                               shorts=[_short("a", built=True),
                                      _short("b", built=False, planned=False)])
    assert in_progress.status.startswith("shorts building")
    assert "none started" not in in_progress.status


def test_status_live_long_with_regressed_final_never_hides_as_in_production():
    # posted once (youtube_id set) then the final video vanished/changed after
    # a rebuild - must surface loudly, never silently read as "long in production"
    ep = EpisodeState(slug="x", long=_long(built=False, posted=True), shorts=[])
    assert "in production" not in ep.status
    assert "LIVE" in ep.status


def test_shorts_posted_any_vs_fully_posted():
    partial_ledger = _short("a", built=True)
    partial_ledger.ledger = {"youtube": {"url": "u"}}  # only 1 of 4 platforms
    ep = EpisodeState(slug="x", long=_long(built=True, posted=True),
                      shorts=[partial_ledger, _short("b", built=True)])
    assert ep.shorts_posted == 0          # not fully posted anywhere
    assert ep.shorts_posted_any == 1      # but real progress exists
    assert "releasing" in ep.status
    assert "posted somewhere" in ep.status


def test_shorts_started_ignores_built_shorts():
    ep = EpisodeState(slug="x", long=_long(),
                      shorts=[_short("a", built=True), _short("b", built=True)])
    assert ep.shorts_started == 0  # both already built, none "in progress"


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-q"]))
