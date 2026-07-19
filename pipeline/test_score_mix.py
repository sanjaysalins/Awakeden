"""Guards for the ONE shared score-mix tail (INV-26).

History: three independent copies of the final mix filter graph grew two
DIFFERENT audio-padding bugs in two different places (2026-07-19, both live in
shipped files). These tests pin the consolidated contract AND fail if any of
the three scorers ever grows a local mix graph again.
"""
from __future__ import annotations

from pathlib import Path

from pipeline import score_mix

ROOT = Path(__file__).resolve().parent.parent
SCORERS = [
    ROOT / "run_piece.py",
    ROOT / "longform" / "_add_score_lf.py",
    ROOT / "longform" / "04_The_Bronze_Serpent" / "_add_score_inked.py",
]


def test_mix_tail_pads_to_absolute_target():
    """INV-26: the narration pad must be apad=whole_dur (absolute), never
    pad_dur (relative) — relative padding preserves a pre-existing short-audio
    gap instead of correcting it (the Bronze Serpent 1.01s desync)."""
    tail = score_mix.mix_tail(480.0, 3.0)
    assert "apad=whole_dur=480.0" in tail, tail
    assert "pad_dur" not in tail, tail
    assert "tpad=stop_mode=clone:stop_duration=3.0" in tail
    assert "sidechaincompress=" in tail and "alimiter=limit=0.97" in tail


def test_mix_tail_fmt_narration_flag():
    plain = score_mix.mix_tail(60.0, 3.0)
    fmt = score_mix.mix_tail(60.0, 3.0, fmt_narration=True)
    assert score_mix.AFMT not in plain.split(";")[0]
    assert score_mix.AFMT in fmt.split(";")[0]


def test_output_args_total_bounds():
    args = score_mix.output_args("out.mp4", preset="veryfast", total=421.2)
    assert args[-1] == "out.mp4"
    assert "-t" in args and args[args.index("-t") + 1] == "421.200"
    args_unbounded = score_mix.output_args("out.mp4", preset="medium")
    assert "-t" not in args_unbounded


def test_no_scorer_owns_a_local_mix_graph():
    """Every scorer must delegate the tail to score_mix — a local
    sidechaincompress/apad in any of the three files means the fork pattern
    (the root cause of the 2026-07-19 bug pair) has crept back."""
    for f in SCORERS:
        src = f.read_text(encoding="utf-8")
        assert "score_mix.mix_tail" in src, f"{f.name}: does not delegate to score_mix.mix_tail"
        # match the FILTER TOKENS (with '='), not prose comments about the bug history
        assert "sidechaincompress=" not in src, f"{f.name}: local sidechain graph reintroduced"
        assert "apad=" not in src, f"{f.name}: local narration pad reintroduced"
