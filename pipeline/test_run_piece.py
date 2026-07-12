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


def test_check_refs_flags_peopled_null_ref():
    """A recurring PEOPLED subject's stills must each carry a character ref; a tomb/
    landscape group is exempt. Guards the ref:null generic-faces trap."""
    pj = {"stills": {"jobs": {
        "women_a": {"prompt": "x", "ref": "../ref.png"},
        "women_b": {"prompt": "x", "ref": None},        # peopled + null -> flagged
        "tomb_a":  {"prompt": "x", "ref": None},        # not people -> exempt
    }, "world": {
        "women_group": {"canon": "the same three Judean women in wool tunics",
                        "applies_to": ["women_a", "women_b"]},
        "tomb": {"canon": "a low rock-hewn tomb with a great round stone",
                 "applies_to": ["tomb_a"]},
    }}}
    problems = RP.check_refs(pj)
    assert len(problems) == 1 and "women_b" in problems[0]
    # once anchored, the group passes
    pj["stills"]["jobs"]["women_b"]["ref"] = "../ref.png"
    assert RP.check_refs(pj) == []


def test_clip_hash_binding(tmp_path):
    """A clip is fresh only while (still bytes + prompt + params) are unchanged;
    pre-hash clips are judged by mtime (still newer = stale)."""
    import os
    an = {"duration": 5, "aspect_ratio": "9:16"}
    still = tmp_path / "s.png"
    clip = tmp_path / "s.mp4"
    still.write_bytes(b"png1")
    clip.write_bytes(b"vid1")
    # no sidecar, clip newer than still -> unhashed (grandfathered skip)
    os.utime(still, (1000, 1000)); os.utime(clip, (2000, 2000))
    assert RP._clip_state(still, clip, "move A", an) == "unhashed"
    # no sidecar, still newer -> stale
    os.utime(still, (3000, 3000))
    assert RP._clip_state(still, clip, "move A", an) == "stale"
    # bind -> fresh
    clip.with_suffix(".src.sha").write_text(
        RP.clip_src_hash(still, "move A", 5, "9:16"), encoding="utf-8")
    assert RP._clip_state(still, clip, "move A", an) == "fresh"
    # prompt edit -> stale
    assert RP._clip_state(still, clip, "move B", an) == "stale"
    # still re-render -> stale
    still.write_bytes(b"png2")
    assert RP._clip_state(still, clip, "move A", an) == "stale"
    # missing clip
    clip.unlink()
    assert RP._clip_state(still, clip, "move A", an) == "missing"


def _mini_piece(root, name, slug, prompt, with_png=False, verdict=None):
    import json
    d = root / name
    (d / "visual").mkdir(parents=True)
    (d / "piece.json").write_text(json.dumps({
        "piece": name, "title": name, "cluster": "t", "verse": "t",
        "stills": {"model": "m", "size": "1x1", "jobs": {slug: {"prompt": prompt, "ref": None}}},
        "animate": None,
        "score": {}, "register": {"stills": {}},
    }), encoding="utf-8")
    if with_png:
        png = d / "visual" / f"{slug}.png"
        png.write_bytes(b"\x89PNG fake")
        if verdict:
            from render_lint.verify import write_audit
            write_audit(png, verdict, ["test"])
    return d


def test_reuse_check_only_on_identical_pass(tmp_path):
    """Reuse fires ONLY for an identical prompt with a PASS audit in a sibling."""
    a = _mini_piece(tmp_path, "piece_a", "shared_plate", "a hill at dawn",
                    with_png=True, verdict="PASS")
    b = _mini_piece(tmp_path, "piece_b", "shared_plate", "a hill at dawn")
    job = RP.load_piece(b)["stills"]["jobs"]["shared_plate"]
    hit = RP.reuse_check(b, "shared_plate", job)
    assert hit is not None and hit.parent.parent == a
    # different prompt -> no reuse
    c = _mini_piece(tmp_path, "piece_c", "shared_plate", "a DIFFERENT hill")
    assert RP.reuse_check(c, "shared_plate",
                          RP.load_piece(c)["stills"]["jobs"]["shared_plate"]) is None


def test_reuse_check_rejects_unaudited(tmp_path):
    _mini_piece(tmp_path, "piece_a", "plate", "same prompt", with_png=True, verdict="FAIL")
    b = _mini_piece(tmp_path, "piece_b", "plate", "same prompt")
    assert RP.reuse_check(b, "plate", RP.load_piece(b)["stills"]["jobs"]["plate"]) is None


def test_retime_follows_a_revoice(tmp_path):
    """Simulate a re-voice: shift every word +0.7s and lengthen the audio — retime
    must move every dip window by the same shift and re-derive base_seconds."""
    import json
    import subprocess
    d = tmp_path / "piece"
    (d / "audio").mkdir(parents=True)
    words = [{"w": w, "start": 1.0 + i, "end": 1.6 + i}
             for i, w in enumerate("come unto me all ye that labour".split())]
    (d / "audio" / "alignment.json").write_text(json.dumps(words), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
                    "-i", "anullsrc=r=44100:cl=mono", "-t", "9.0",
                    str(d / "audio" / "narration.mp3")], check=True)
    pj = {"piece": "t", "title": "t", "cluster": "t", "verse": "t",
          "stills": {"model": "m", "size": "1x1", "jobs": {}}, "animate": None,
          "register": {"stills": {}},
          "score": {"src": "x.mp4", "out": "y.mp4", "dark": "d.mp3", "grace": "g.mp3",
                    "base_seconds": 9.0, "outro_hold": 1.5,
                    "dark_trim_end": "5.0", "grace_trim": ["20", "90"],
                    "crossfade": "6", "tpad": "1.5",
                    "dips": [["2.8", "5.9", "0.35"]],   # covers "me all ye" (3.0-5.6)
                    "cta_dip": ["6.9", "0.5"]}}         # covers "labour" (7.0-7.6)
    (d / "piece.json").write_text(json.dumps(pj), encoding="utf-8")
    assert RP.run_enrich_dips(d, RP.load_piece(d)) == 0
    enriched = RP.load_piece(d)
    assert enriched["score"]["dips_meta"][0]["phrase"] == "me all ye"
    # the re-voice: everything 0.7s later, audio 1s longer
    shifted = [{"w": w["w"], "start": round(w["start"] + 0.7, 2),
                "end": round(w["end"] + 0.7, 2)} for w in words]
    (d / "audio" / "alignment.json").write_text(json.dumps(shifted), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
                    "-i", "anullsrc=r=44100:cl=mono", "-t", "10.0",
                    str(d / "audio" / "narration.mp3")], check=True)
    new = RP.retime_score(d, enriched)
    assert new["base_seconds"] == pytest.approx(10.0, abs=0.1)
    a, b, vol = new["dips"][0]
    assert float(a) == pytest.approx(2.8 + 0.7, abs=0.02)
    assert float(b) == pytest.approx(5.9 + 0.7, abs=0.02)
    assert vol == "0.35"
    assert float(new["cta_dip"][0]) == pytest.approx(6.9 + 0.7, abs=0.02)


def test_retime_fails_loud_when_phrase_gone(tmp_path):
    import json
    import subprocess
    d = tmp_path / "piece"
    (d / "audio").mkdir(parents=True)
    (d / "audio" / "alignment.json").write_text(json.dumps(
        [{"w": "totally", "start": 0.1, "end": 0.5},
         {"w": "different", "start": 0.6, "end": 1.0}]), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
                    "-i", "anullsrc=r=44100:cl=mono", "-t", "2.0",
                    str(d / "audio" / "narration.mp3")], check=True)
    pj = {"score": {"base_seconds": 2.0, "outro_hold": 1.0, "dark_trim_end": "1.0",
                    "dips": [["0.1", "0.9", "0.35"]],
                    "dips_meta": [{"phrase": "come unto me", "pre": 0.0, "post": 0.0}],
                    "cta_meta": {"phrase": "x", "pre": 0.0}, "cta_dip": ["1.0", "0.5"]}}
    with pytest.raises(SystemExit, match="phrase not found"):
        RP.retime_score(d, pj)


def test_choose_engine_policy():
    """The paid-vs-$0 rule: writing->static, panels-only->dyncam, hook/close/sacred/
    long-holds->kling, short full-bleeds->dyncam."""
    pj = {"stills": {"jobs": {s: {"prompt": p, "ref": None} for s, p in {
        "scroll_close": "an open scroll of faded script beside a lamp",
        "grid_filler": "a quiet hillside path at dusk",
        "hook_shot": "a storm rolling over a dark hilltop",
        "christ_still": "Jesus crucified against the darkened sky",
        "short_full": "an empty stone doorway at night",
        "long_hold": "a shepherd walking a ridge at dawn",
    }.items()}}, "register": {"stills": {}}}
    spec = {"beats": [
        {"t": [0, 3.4], "tpl": "full", "clips": [{"slug": "hook_shot"}]},
        {"t": [3.4, 5], "tpl": "grid", "panels": [{"slug": "grid_filler"}, {"slug": "scroll_close"}]},
        {"t": [5, 7], "tpl": "full", "clips": [{"slug": "short_full"}]},
        {"t": [7, 11], "tpl": "full", "clips": [{"slug": "long_hold"}]},
        {"t": [11, 14], "tpl": "full", "clips": [{"slug": "christ_still"}]},
        {"t": [14, 17], "tpl": "full", "clips": [{"slug": "christ_still"}]},
    ]}
    usage = RP._slug_usage(spec)
    assert RP.choose_engine("scroll_close", pj, usage)[0] == "static"
    assert RP.choose_engine("grid_filler", pj, usage)[0] == "dyncam"
    assert RP.choose_engine("hook_shot", pj, usage)[0] == "kling"     # first beat
    assert RP.choose_engine("christ_still", pj, usage)[0] == "kling"  # close + sacred
    assert RP.choose_engine("short_full", pj, usage)[0] == "dyncam"   # 2.0s hold
    assert RP.choose_engine("long_hold", pj, usage)[0] == "kling"     # 4.0s hold


def test_animate_absent_is_clean():
    # 3 pieces have no animate section — prompts must be empty, not crash
    for piece_dir in PIECES:
        pj = RP.load_piece(piece_dir)
        if pj.get("animate") is None:
            assert RP.animate_prompts(pj) == {}
            return
    pytest.skip("no animate-less piece found")
