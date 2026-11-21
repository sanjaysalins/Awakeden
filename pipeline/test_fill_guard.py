"""Fail-closed FILL + landing-hold guards (owner rule 2026-11-21).

A clip shorter than its slot must RAISE (no reverse / boomerang / ping-pong / freeze / slow-mo > 1.15x /
Ken Burns on a still) unless the loud opt-in is set; a NEW film whose last word ends < 3.0 s before the end
must FAIL the hold gate. $0, deterministic, no network.
"""
from __future__ import annotations

import ast
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import fill_guard  # noqa: E402
import check_landing_hold as clh  # noqa: E402
from pipeline import score_mix  # noqa: E402


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- core guard
def test_clip_shorter_than_slot_raises_by_default(monkeypatch):
    monkeypatch.delenv(fill_guard.ENV_FLAG, raising=False)
    with pytest.raises(fill_guard.ClipShorterThanSlot) as e:
        fill_guard.require_clip_covers_slot("f03", 5.0, 7.5)
    m = str(e.value)
    assert "clip shorter than slot" in m and "f03" in m and "5.00" in m and "7.50" in m
    fill_guard.require_clip_covers_slot("f03", 7.5, 7.5)       # equal is fine
    fill_guard.require_clip_covers_slot("f03", 9.0, 7.5)       # longer is fine (trim)


def test_opt_in_still_works(monkeypatch):
    monkeypatch.delenv(fill_guard.ENV_FLAG, raising=False)
    fill_guard.require_clip_covers_slot("f03", 5.0, 7.5, allow_fill=True)
    monkeypatch.setenv(fill_guard.ENV_FLAG, "1")
    fill_guard.require_clip_covers_slot("f03", 5.0, 7.5)
    fill_guard.require_fill_opt_in("loop")
    fill_guard.forbid_still_kenburns("s1")
    with pytest.raises(fill_guard.ClipShorterThanSlot):      # explicit False beats the env
        fill_guard.require_clip_covers_slot("f03", 5.0, 7.5, allow_fill=False)


def test_slowmo_over_1_15_counts_as_fill(monkeypatch):
    monkeypatch.delenv(fill_guard.ENV_FLAG, raising=False)
    fill_guard.require_stretch_ok("s", 5.0, 5.7)             # 1.14x ok
    with pytest.raises(fill_guard.ClipShorterThanSlot):
        fill_guard.require_stretch_ok("s", 5.0, 5.9)         # 1.18x fill
    fill_guard.require_stretch_ok("s", 5.0, 5.9, allow_fill=True)


def test_still_kenburns_forbidden_by_default(monkeypatch):
    monkeypatch.delenv(fill_guard.ENV_FLAG, raising=False)
    with pytest.raises(fill_guard.ClipShorterThanSlot):
        fill_guard.forbid_still_kenburns("s9")


# ---------------------------------------------------------------- builders
def test_swirls_assemble_helpers_refuse_fill(monkeypatch, tmp_path):
    monkeypatch.delenv(fill_guard.ENV_FLAG, raising=False)
    sa = _load(ROOT / "poc_living_water_ink_style_test" / "swirls_assemble.py", "_t_swirls_assemble")
    for fn in (sa.make_boomerang, sa.make_freeze, sa.make_freeze_tail_loop):
        with pytest.raises(fill_guard.ClipShorterThanSlot) as e:
            fn(tmp_path / "a.mp4", tmp_path / "o.mp4", 8.0, 5.0, tmp_path, "f02", None)
        assert "f02" in str(e.value)


def test_comic_engine_temporal_refuses_fill(monkeypatch):
    monkeypatch.delenv(fill_guard.ENV_FLAG, raising=False)
    ce = _load(ROOT / "longform" / "_style_poc" / "ew04" / "_mocomic" / "comic_engine.py", "_t_comic_engine")
    assert "trim=duration" in ce._temporal(0, 4.0, "static", 5.0, "t0")          # clip >= slot: fine
    with pytest.raises(fill_guard.ClipShorterThanSlot):
        ce._temporal(0, 8.0, "static", 5.0, "t0")                                # boomerang
    with pytest.raises(fill_guard.ClipShorterThanSlot):
        ce._temporal(0, 8.0, "directional", 5.0, "t0")                           # 1.6x slow-mo
    assert "setpts" in ce._temporal(0, 5.5, "directional", 5.0, "t0")            # 1.10x allowed
    monkeypatch.setenv(fill_guard.ENV_FLAG, "1")
    assert "reverse" in ce._temporal(0, 8.0, "static", 5.0, "t0")                # opt-in: old behaviour


def _ppindex_sources():
    files = sorted((ROOT / "poc_living_sketchbook").glob("*/_s3_assemble.py")) + [
        ROOT / "poc_living_sketchbook" / "bronze_serpent" / "_s4_assemble.py"]
    assert len(files) >= 8
    return files


@pytest.mark.parametrize("path", _ppindex_sources(), ids=lambda p: p.parent.name)
def test_ppindex_loop_refuses_fill(path, monkeypatch):
    """Extract each assembler's own _ppindex and prove the ping-pong branch is now fail-closed."""
    monkeypatch.delenv(fill_guard.ENV_FLAG, raising=False)
    tree = ast.parse(path.read_text(encoding="utf-8"))
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_ppindex")
    ns = {"__file__": str(path)}
    exec(compile(ast.Module([fn], []), str(path), "exec"), ns)
    assert ns["_ppindex"](10, 100) == 10                       # inside the clip: unchanged
    with pytest.raises(fill_guard.ClipShorterThanSlot):
        ns["_ppindex"](150, 100)                               # past the clip: would ping-pong
    monkeypatch.setenv(fill_guard.ENV_FLAG, "1")
    assert ns["_ppindex"](150, 100) == 48                      # opt-in: old ping-pong index


def test_storm_pick_loop_index_refuses_fill(monkeypatch):
    monkeypatch.delenv(fill_guard.ENV_FLAG, raising=False)
    path = ROOT / "poc_living_sketchbook" / "storm" / "_s6_assemble.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_pick_loop_index")
    ns = {"__file__": str(path), "FPS": 30}
    exec(compile(ast.Module([fn], []), str(path), "exec"), ns)
    assert ns["_pick_loop_index"](1.0, 0.0, 100) == 30
    with pytest.raises(fill_guard.ClipShorterThanSlot):
        ns["_pick_loop_index"](9.0, 0.0, 100)


PATCHED = [
    "longform/_assemble_16x9.py",
    "longform/02_Psalm_22_Song_From_The_Cross/build_livingpage_16x9.py",
    "poc_comic_page/_living_comic/lc_compose.py",
    "poc_living_sketchbook/_rewrite_v3/retime_v3.py",
    "poc_living_sketchbook/_rewrite_v4/retime_v4.py",
    "poc_living_sketchbook/bronze_serpent_long/_s7_assemble.py",
    "poc_living_sketchbook/day_of_atonement/_s6_assemble.py",
    "poc_living_sketchbook/seed_of_the_woman/_s6_assemble.py",
    "poc_living_water_ink_style_test/swirls_episode_16_let_the_little_children/build_v1.py",
    "poc_living_water_ink_style_test/swirls_episode_12_ye_are_not_all_clean/v3_retro/build_v3.py",
]


@pytest.mark.parametrize("rel", PATCHED)
def test_fill_builders_call_the_guard(rel):
    """These builders cannot run as unit tests (ffmpeg + real clips); pin that the guard stays wired in
    and that each file still parses."""
    src = (ROOT / rel).read_text(encoding="utf-8")
    ast.parse(src)
    assert "fill_guard.require_" in src or "fill_guard.forbid_" in src, rel


# ---------------------------------------------------------------- landing hold
def test_mix_tail_short_hold_raises(monkeypatch):
    monkeypatch.delenv(score_mix.HOLD_ENV_FLAG, raising=False)
    with pytest.raises(score_mix.ShortLandingHold):
        score_mix.mix_tail(60.0, 1.5)
    assert "tpad=stop_mode=clone:stop_duration=3.0" in score_mix.mix_tail(60.0, 3.0)
    assert "stop_duration=1.5" in score_mix.mix_tail(60.0, 1.5, allow_short_hold=True)
    monkeypatch.setenv(score_mix.HOLD_ENV_FLAG, "1")
    assert "stop_duration=1.5" in score_mix.mix_tail(60.0, 1.5)


def _mk_film(path: Path, fade: bool) -> None:
    af = "sine=frequency=330:duration=10"
    if fade:
        af += ",afade=t=out:st=7.0:d=2.5"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "color=c=black:s=64x64:d=10:r=10",
                    "-f", "lavfi", "-i", af, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
                    "-t", "10", str(path)], check=True)


@pytest.mark.skipif(not (shutil.which("ffmpeg") and shutil.which("ffprobe")), reason="needs ffmpeg")
def test_hold_gate_fails_short_hold_and_passes_long(tmp_path, monkeypatch):
    short = tmp_path / "short_hold.mp4"
    good = tmp_path / "good_hold.mp4"
    _mk_film(short, fade=False)
    _mk_film(good, fade=True)
    (tmp_path / "short_hold.words.json").write_text('[{"w":"x","start":9.0,"end":9.9}]', encoding="utf-8")   # 0.1 s hold
    (tmp_path / "good_hold.words.json").write_text('{"words":[{"w":"x","start":6.0,"end":6.8}]}', encoding="utf-8")  # 3.2 s hold
    ok, msg = clh.check_hold(short)
    assert not ok and "standard" in msg, msg
    ok, msg = clh.check_hold(good)
    assert ok, msg
    # CLI: a new film fails (exit 1), a "shipped" one only warns
    monkeypatch.setattr(clh, "SHIPPED_LIST", tmp_path / "shipped.json")
    assert clh.main([str(short)]) == 1
    (tmp_path / "shipped.json").write_text('["short_hold.mp4"]', encoding="utf-8")
    assert clh.main([str(short)]) == 0
    assert clh.main([str(good)]) == 0
    # no words json + --require-words = FAIL; without the flag it is a SKIP
    (tmp_path / "good_hold.words.json").unlink()
    assert clh.main([str(good), "--require-words"]) == 1
    assert clh.main([str(good)]) == 0
