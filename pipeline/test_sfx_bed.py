"""Guards for the ONE shared long-form SFX cue-bed engine.

History: seven per-episode copies of the same ffmpeg engine (render cues ->
sum bed -> mix under the scored film) — the same fork pattern that grew the
score-mix pad bug pair (see pipeline/test_score_mix.py). These tests pin the
engine's contract AND fail if any episode script ever regrows a local engine.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from pipeline import sfx_bed

ROOT = Path(__file__).resolve().parent.parent
# Discovered, not hardcoded (red-team 2026-07-19): a hardcoded list guards the
# past seven files, not the pattern — an eighth episode's copy-pasted local
# engine would escape entirely. The glob auto-covers every future episode.
EPISODE_SCRIPTS = sorted(ROOT.glob("longform/*/_sfx_*.py"))


def test_episode_script_discovery_is_sane():
    """The glob must keep finding the known seven (a rename/move that silently
    empties the guard is itself a failure)."""
    names = {p.name for p in EPISODE_SCRIPTS}
    assert len(EPISODE_SCRIPTS) >= 7, f"guard glob collapsed: {names}"
    assert {"_sfx_psalm22_lf.py", "_sfx_passover.py", "_sfx_bronze.py",
            "_sfx_bronze_inked.py", "_sfx_seed.py", "_sfx_atonement.py",
            "_sfx_two_goats.py"} <= names, names


def test_cue_af_matches_historical_filter():
    """The per-cue chain must stay byte-identical to what every shipped bed
    used: gain, 1.0s fade-in, 1.5s fade-out at end-1.5, ms-precise delay."""
    af = sfx_bed.cue_af(-37, 477.7, 0.0)
    assert af == ("volume=-37dB,afade=t=in:d=1.0,"
                  "afade=t=out:st=476.20:d=1.5,adelay=0|0")
    af = sfx_bed.cue_af(-15, 3.0, 275.5)
    assert af == ("volume=-15dB,afade=t=in:d=1.0,"
                  "afade=t=out:st=1.50:d=1.5,adelay=275500|275500")


def test_cue_af_short_cue_fade_floor():
    """A cue shorter than the 1.5s fade-out must floor st at 0, not go negative."""
    assert "afade=t=out:st=0.00:d=1.5" in sfx_bed.cue_af(-22, 1.0, 121.3)


def test_build_fails_closed_on_missing_scored(tmp_path):
    with pytest.raises(SystemExit, match="missing scored film"):
        sfx_bed.build(tmp_path / "nope.mp4", tmp_path / "out.mp4", [], 60.0)


def test_build_fails_closed_on_missing_sound(tmp_path):
    scored = tmp_path / "scored.mp4"
    scored.write_bytes(b"x")
    with pytest.raises(SystemExit, match="missing sound"):
        sfx_bed.build(scored, tmp_path / "out.mp4",
                      [("no_such_slug", 0.0, 5.0, -30)], 60.0,
                      lib=tmp_path, work=tmp_path / "_w")


def test_no_episode_script_owns_a_local_engine():
    """Every long-form SFX script must delegate to pipeline.sfx_bed — a local
    ffmpeg graph in any of the seven files means the fork pattern is back."""
    for f in EPISODE_SCRIPTS:
        src = f.read_text(encoding="utf-8")
        assert "from pipeline.sfx_bed import build" in src, \
            f"{f.name}: does not delegate to pipeline.sfx_bed"
        assert "build(SCORED, OUT, CUES, TOTAL" in src, \
            f"{f.name}: imports the engine but never calls it"
        # substring scan over the WHOLE file, docstrings included — a wrapper
        # docstring mentioning these tokens fails too (fail-closed nuisance,
        # accepted; keep engine words out of cue-sheet prose)
        for token in ("amix=", "afade=", "stream_loop", "filter_complex", "subprocess"):
            assert token not in src, f"{f.name}: local engine reintroduced ({token})"


def test_episode_scripts_keep_their_own_cue_sheets():
    """The cue sheet (the actual per-piece sound design) stays in the episode
    script — the engine must never grow a hardcoded cue list."""
    for f in EPISODE_SCRIPTS:
        src = f.read_text(encoding="utf-8")
        assert "CUES = [" in src and "TOTAL = " in src, f"{f.name}: missing cue sheet"
    engine = (ROOT / "pipeline" / "sfx_bed.py").read_text(encoding="utf-8")
    assert "CUES = [" not in engine
