"""run_piece.py regression tests (P1 keystone, 2026-07-08).

The manifest runner replaced the per-piece quartet scripts after a byte-parity proof
on all 10 cluster_01 pieces (request bodies, Kling prompts, ffmpeg argv, asset rows).
These tests keep the runner honest against every committed piece.json.

Run: .venv\\Scripts\\python.exe -m pytest pipeline/test_run_piece.py
"""
from __future__ import annotations

from pathlib import Path

import pytest

import run_piece as RP

REPO = Path(__file__).resolve().parent.parent
PIECES = sorted(p.parent for p in (REPO / "batches").glob("*/*/piece.json"))


def test_pieces_discovered():
    assert len(PIECES) >= 10, f"expected the 10 cluster_01 pieces, found {len(PIECES)}"


@pytest.mark.parametrize("piece_dir", PIECES, ids=lambda p: p.name)
def test_piece_json_drives_all_stages(piece_dir):
    pj = RP.load_piece(piece_dir)
    # stills: every job builds a full request body with the house style tail
    bodies = RP.stills_bodies(piece_dir, pj)
    assert bodies, "no stills jobs"
    for slug, (body, dest) in bodies.items():
        assert body["model"] and body["size"] and body["prompt"], slug
        assert dest.name == f"{slug}.png"
        if pj["stills"]["jobs"][slug]["ref"]:
            assert "image" in body, f"{slug}: ref not attached"
            # the referenced source still must actually exist
            assert (piece_dir / pj["stills"]["jobs"][slug]["ref"]).resolve().exists(), slug
    # animate: prompts contain the frozen-tableau contract
    for slug, prompt in RP.animate_prompts(pj).items():
        assert "INVENT NOTHING" in prompt and "only the camera moves" in prompt, slug
    # score: a complete ffmpeg argv builds
    cmd = RP.score_cmd(piece_dir, pj)
    assert cmd[0] == "ffmpeg" and "-filter_complex" in cmd and str(cmd[-1]).endswith(".mp4")
    # register: rows are unique by id and carry the piece identity
    rows = RP.register_rows(piece_dir, pj)
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)), "duplicate register ids"
    assert all(r["piece"] == pj["piece"] for r in rows)


def test_animate_absent_is_clean():
    # 3 pieces have no animate section — prompts must be empty, not crash
    for piece_dir in PIECES:
        pj = RP.load_piece(piece_dir)
        if pj.get("animate") is None:
            assert RP.animate_prompts(pj) == {}
            return
    pytest.skip("no animate-less piece found")
