"""Offline tests for the publisher (Stage 6) mechanical layer.

Repo convention: no pytest installed — run via the __main__ block:
    .venv\\Scripts\\python.exe -m pipeline.test_publish
"""
from __future__ import annotations

import tempfile
from pathlib import Path

from pipeline import publish_pack as pp
from pipeline.publish_check import _TS_RE
from pipeline.upload_models import PlatformMeta

_PASS = 0
_FAIL = 0


def ok(cond: bool, msg: str) -> None:
    global _PASS, _FAIL
    if cond:
        _PASS += 1
    else:
        _FAIL += 1
        print(f"  FAIL: {msg}")


# ---- _ts -------------------------------------------------------------------
def test_ts() -> None:
    ok(pp._ts(0) == "00:00:00,000", "_ts(0)")
    ok(pp._ts(1.5) == "00:00:01,500", "_ts(1.5)")
    ok(pp._ts(65.25) == "00:01:05,250", "_ts(65.25)")
    ok(pp._ts(-3) == "00:00:00,000", "_ts negative clamps to 0")


# ---- build_srt -------------------------------------------------------------
def test_build_srt() -> None:
    words = [
        {"w": "My", "start": 0.0, "end": 0.2},
        {"w": "God.", "start": 0.2, "end": 0.6},
        {"w": "Why", "start": 0.6, "end": 0.9},
        {"w": "hast", "start": 0.9, "end": 1.2},
        {"w": "thou", "start": 1.2, "end": 1.5},
        {"w": "forsaken", "start": 1.5, "end": 2.0},
        {"w": "me?", "start": 2.0, "end": 2.4},
    ]
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "w.json"
        import json
        p.write_text(json.dumps(words), encoding="utf-8")
        srt = pp.build_srt(p, max_chars=999, max_dur=999)
    ok("-->" in srt, "srt has a cue arrow")
    # two sentences -> two cues (closes on '?' and on '.'/'?' punctuation)
    ok(srt.count("-->") == 2, f"expected 2 cues, got {srt.count('-->')}")
    ok("forsaken me?" in srt, "second cue text present")
    ok(srt.startswith("1\n00:00:00,000 -->"), "first cue starts at 0")


def test_build_srt_max_chars_split() -> None:
    words = [{"w": f"w{i}", "start": i * 0.5, "end": i * 0.5 + 0.4} for i in range(20)]
    with tempfile.TemporaryDirectory() as d:
        import json
        p = Path(d) / "w.json"
        p.write_text(json.dumps(words), encoding="utf-8")
        srt = pp.build_srt(p, max_chars=12, max_dur=999)
    ok(srt.count("-->") > 1, "long run splits into multiple cues by char budget")


# ---- copy file round-trip --------------------------------------------------
def test_render_parse_roundtrip() -> None:
    meta = PlatformMeta(
        platform="youtube_short", label="YouTube (Short)",
        title="Why did Jesus quote Psalm 22 from the cross?",
        description="From the cross He cried a psalm written 1000 years before.\n\nSubscribe.",
        tags=["psalm 22", "jesus", "cross"],
        hashtags=["#Bible", "#Jesus", "#KJV"],
    )
    md = pp.render_platform_md(meta, is_long=False)
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "youtube_short.md"
        p.write_text(md, encoding="utf-8")
        f = pp.parse_copy(p)
    ok(f.get("TITLE") == meta.title, "TITLE round-trips")
    ok(f.get("DESCRIPTION", "").startswith("From the cross"), "DESCRIPTION round-trips")
    ok(f.get("TAGS") == "psalm 22, jesus, cross", "TAGS round-trip as CSV")
    ok(f.get("HASHTAGS") == "#Bible #Jesus #KJV", "HASHTAGS round-trip space-joined")
    ok("CHAPTERS" not in f, "short has no CHAPTERS section")


def test_caption_platform_uses_caption_label() -> None:
    meta = PlatformMeta(platform="tiktok", label="TikTok", title="",
                        description="Hook line here.", tags=[], hashtags=["#Bible"])
    md = pp.render_platform_md(meta, is_long=False)
    ok("## CAPTION" in md, "tiktok body labelled CAPTION")
    ok("## TITLE" not in md, "tiktok has no TITLE section (empty title)")
    ok("## TAGS" not in md, "tiktok has no TAGS section")


def test_long_has_chapters_pinned() -> None:
    meta = PlatformMeta(platform="youtube_long", label="YouTube (Long)", title="T",
                        description="D", tags=["a"], hashtags=["#B"])
    md = pp.render_platform_md(meta, is_long=True, chapters="0:00 Intro\n1:20 The cry", pinned="What stood out?")
    ok("## CHAPTERS" in md and "0:00 Intro" in md, "long carries CHAPTERS")
    ok("## PINNED_COMMENT" in md, "long carries PINNED_COMMENT")


# ---- placeholder + chapter regex ------------------------------------------
def test_placeholder() -> None:
    ok(pp._is_placeholder(""), "empty is placeholder")
    ok(pp._is_placeholder("TODO  <-- write this"), "TODO is placeholder")
    ok(not pp._is_placeholder("Real copy."), "real copy is not placeholder")


def test_chapter_ts_re() -> None:
    ok(bool(_TS_RE.match("0:00 Intro")), "0:00 Intro matches")
    ok(bool(_TS_RE.match("12:34 Later")), "M:SS matches")
    ok(not _TS_RE.match("no timestamp here"), "non-timestamp rejected")


def main() -> int:
    for fn in [test_ts, test_build_srt, test_build_srt_max_chars_split,
               test_render_parse_roundtrip, test_caption_platform_uses_caption_label,
               test_long_has_chapters_pinned, test_placeholder, test_chapter_ts_re]:
        fn()
    print(f"\npublish tests: {_PASS} passed, {_FAIL} failed")
    return 1 if _FAIL else 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
