"""Tests for pipeline/finality.py — the ONE final-video rule + content sha."""
from __future__ import annotations

from pathlib import Path

import pytest

from pipeline import finality


def _mk(p: Path, content: bytes = b"x") -> Path:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(content)
    return p


# ---- short (living-page) lane precedence -----------------------------------
def test_short_lane_sfx_wins(tmp_path):
    _mk(tmp_path / "visual" / "piece_scored.mp4")
    _mk(tmp_path / "visual" / "piece_sfx.mp4")
    status, video = finality.final_video(tmp_path)
    assert status == finality.FINAL_SFX
    assert video.name == "piece_sfx.mp4"


def test_short_lane_scored_needs_sfx(tmp_path):
    _mk(tmp_path / "visual" / "piece_scored.mp4")
    status, video = finality.final_video(tmp_path)
    assert status == finality.NEEDS_SFX


def test_short_lane_byteplus_pilot_outranks_plain_scored(tmp_path):
    _mk(tmp_path / "visual" / "piece_scored.mp4")
    _mk(tmp_path / "visual" / "_byteplus" / "piece_scored.mp4")
    _status, video = finality.final_video(tmp_path)
    assert video.parent.name == "_byteplus"


def test_bak_backup_never_final(tmp_path):
    # the wave rollout parks *_sfx.bak_prelivinglight.mp4 which sorts BEFORE *_sfx.mp4
    _mk(tmp_path / "visual" / "a_sfx.bak_prelivinglight_sfx.mp4")
    _mk(tmp_path / "visual" / "piece_sfx.mp4")
    _status, video = finality.final_video(tmp_path)
    assert ".bak" not in video.name


# ---- long (16:9) lane -------------------------------------------------------
def test_long_lane_sfx_outranks_captioned(tmp_path):
    _mk(tmp_path / "visual_16x9" / "LivingPage_captioned.mp4")
    _mk(tmp_path / "visual_16x9" / "LivingPage_scored_sfx.mp4")
    status, video = finality.final_video(tmp_path)
    assert status == finality.FINAL_SFX
    assert video.name.endswith("_sfx.mp4")


def test_long_lane_inked_dir_reachable(tmp_path):
    _mk(tmp_path / "visual_16x9_inked" / "LivingPage_scored_sfx.mp4")
    status, video = finality.final_video(tmp_path)
    assert status == finality.FINAL_SFX


def test_long_lane_pattern_beats_directory(tmp_path):
    # red-team C1: an inked-rebuild sfx must beat an OLD visual_16x9 captioned
    _mk(tmp_path / "visual_16x9" / "Old_captioned.mp4")
    _mk(tmp_path / "visual_16x9_inked" / "LivingPage_scored_sfx.mp4")
    status, video = finality.final_video(tmp_path)
    assert status == finality.FINAL_SFX
    assert video.parent.name == "visual_16x9_inked"


def test_long_lane_scored_beats_unscored_tie(tmp_path):
    # red-team C1 live case: Isaiah53_16x9_captioned (unscored) sorted before
    # Isaiah53_16x9_scored_captioned — the deeper chain must win
    _mk(tmp_path / "visual_16x9" / "Isaiah53_16x9_captioned.mp4")
    _mk(tmp_path / "visual_16x9" / "Isaiah53_16x9_scored_captioned.mp4")
    _status, video = finality.final_video(tmp_path)
    assert video.name == "Isaiah53_16x9_scored_captioned.mp4"


# ---- pin + rivals -------------------------------------------------------------
def test_pin_overrides_everything(tmp_path):
    _mk(tmp_path / "visual_16x9" / "A_scored_sfx.mp4")
    cap = _mk(tmp_path / "visual_16x9" / "A_scored_sfx_captioned.mp4")
    (tmp_path / "FINAL_VIDEO.txt").write_text("visual_16x9/A_scored_sfx_captioned.mp4",
                                              encoding="utf-8")
    status, video = finality.final_video(tmp_path)
    assert status == finality.FINAL_PINNED and video == cap
    assert finality.rival_finals(tmp_path) == []   # pinned lanes are never ambiguous


def test_dangling_pin_fails_closed(tmp_path):
    _mk(tmp_path / "visual_16x9" / "A_scored_sfx.mp4")
    (tmp_path / "FINAL_VIDEO.txt").write_text("visual_16x9/GONE.mp4", encoding="utf-8")
    assert finality.final_video(tmp_path) == (finality.NO_VIDEO, None)


def test_rival_finals_flags_long_lane_ambiguity(tmp_path):
    _mk(tmp_path / "visual_16x9" / "A_scored_sfx.mp4")
    _mk(tmp_path / "visual_16x9" / "A_scored_sfx_captioned.mp4")
    rivals = finality.rival_finals(tmp_path)
    assert [r.name for r in rivals] == ["A_scored_sfx_captioned.mp4"]


# ---- legacy assembly lane ---------------------------------------------------
def test_legacy_assembly_order(tmp_path):
    _mk(tmp_path / "assembly" / "viral_cut_captioned.mp4")
    _mk(tmp_path / "assembly" / "viral_cut_sfx_music_captioned.mp4")
    status, video = finality.final_video(tmp_path)
    assert status == finality.FINAL_LEGACY
    assert video.name == "viral_cut_sfx_music_captioned.mp4"


def test_no_video(tmp_path):
    (tmp_path / "visual").mkdir()
    status, video = finality.final_video(tmp_path)
    assert (status, video) == (finality.NO_VIDEO, None)


# ---- content sha ------------------------------------------------------------
def test_content_sha_tracks_content_not_path(tmp_path, monkeypatch):
    monkeypatch.setattr(finality, "_SHA_CACHE", tmp_path / "cache.json")
    f = _mk(tmp_path / "v.mp4", b"AAA")
    sha1 = finality.content_sha(f)
    assert sha1 == finality.content_sha(f)          # cache hit, same value
    f.write_bytes(b"BBBB")                          # size change busts the cache
    assert finality.content_sha(f) != sha1


def test_content_sha_survives_metadata_preserving_swap(tmp_path, monkeypatch):
    # red-team empirical find: same SIZE + restored mtime must NOT return the
    # stale cached sha (robocopy-style restore) — the head/tail fingerprint busts it
    import os
    monkeypatch.setattr(finality, "_SHA_CACHE", tmp_path / "cache.json")
    f = _mk(tmp_path / "v.mp4", b"AAAA")
    st = f.stat()
    sha1 = finality.content_sha(f)
    f.write_bytes(b"BBBB")                                        # same size
    os.utime(f, ns=(st.st_atime_ns, st.st_mtime_ns))              # restore mtime
    assert finality.content_sha(f) != sha1


def test_content_sha_missing_file_is_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(finality, "_SHA_CACHE", tmp_path / "cache.json")
    assert finality.content_sha(tmp_path / "nope.mp4") == ""


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-q"]))
