"""Phase C — lock chokepoint tests.

Run: .venv\\Scripts\\python.exe -m pipeline.test_lock
"""
from __future__ import annotations

import tempfile
from pathlib import Path

from pipeline import lock as L

_SHORTS = (Path(__file__).resolve().parent.parent
           / "longform" / "02_Psalm_22_Song_From_The_Cross" / "v1" / "shorts")


def _mk(spoken_hook: str, cta: str, *, quote='"The LORD is my shepherd; I shall not want."',
        ref="Psalm 23:1", tagged: bool = True) -> Path:
    d = Path(tempfile.mkdtemp()) / "short"
    d.mkdir()
    (d / "narration.md").write_text(
        f"# T\n---\n**[narrator]**\n{spoken_hook}\n\n"
        f"**[narrator — KJV, {ref}]**\n{quote}\n\n**[narrator]**\n{cta}\n\n---\n## DEPTH\nx\n",
        encoding="utf-8")
    if tagged:
        # the REAL rendered format synth consumes: <speaker name=...> XML, no refs
        (d / "narration-tagged.md").write_text(
            f'<speaker name="narrator">{spoken_hook} {quote} {cta}</speaker>\n',
            encoding="utf-8")
    return d


def test_templated_short_is_blocked_by_cluster():
    # self-contained templated cluster (3 shorts all closing "Come to Him") — must NOT
    # lock. (The real Psalm 22 shorts have since been de-templated + locked, so this
    # uses a snapshot rather than live files.)
    parent = Path(tempfile.mkdtemp())
    folders = []
    for i, hook in enumerate(["First unique hook.", "Second unique hook.", "Third unique hook."]):
        f = parent / f"0{i+1}_x"; f.mkdir()
        (f / "narration.md").write_text(
            f"# T\n---\n**[narrator]**\n{hook}\n\n"
            f'**[narrator — KJV, Psalm 23:1]**\n"The LORD is my shepherd; I shall not want."\n\n'
            f"**[narrator]**\nA closing line. Come to Him.\n\n---\n## DEPTH\nx\n", encoding="utf-8")
        folders.append(f)
    rep = L.run_lock(folders[0], form="short", check_cluster=True)
    assert not rep["ok"], "a templated short must NOT lock"
    assert any("cta_repetition" in b for b in rep["blocking"]), rep["blocking"]
    assert not (folders[0] / ".locked").exists(), "must not write .locked on failure"


def test_clean_folder_locks_and_registers():
    d = _mk("A wholly unique opening about a quiet dawn.", "Rest in His care this hour.")
    rep = L.run_lock(d, form="short", check_cluster=True)
    assert rep["ok"], rep["blocking"]
    assert (d / ".locked").is_file()
    ok, _ = L.is_locked(d)
    assert ok


def test_stale_lock_detected_on_edit():
    d = _mk("Another unique opening, this time at dusk.", "Turn to Him tonight, friend.")
    L.run_lock(d, form="short")
    md = d / "narration.md"
    md.write_text(md.read_text(encoding="utf-8").replace("dusk", "dawn"), encoding="utf-8")
    ok, why = L.is_locked(d)
    assert not ok and "stale" in why, why


def test_require_lock_refuses_unlocked():
    d = _mk("Unlocked unique opening here.", "A distinct closing for this one.")
    try:
        L.require_lock(d)
    except PermissionError:
        return
    raise AssertionError("require_lock did not refuse an unlocked folder")


def test_kjv_misquote_blocks_lock():
    # altered KJV word must block the lock
    d = _mk("Unique opening for the misquote case.", "A distinct close here.",
            quote='"The LORD is my shepherd; I shall not lack."')  # 'lack' != KJV 'want'
    rep = L.run_lock(d, form="short", check_cluster=False)
    assert not rep["ok"] and any("KJV" in b for b in rep["blocking"]), rep["blocking"]


def test_rule8_too_many_quotes_blocks_short():
    d = Path(tempfile.mkdtemp()) / "s"
    d.mkdir()
    (d / "narration.md").write_text(
        '# T\n---\n**[narrator]**\nUnique opener.\n\n'
        '**[narrator — KJV, Psalm 23:1]**\n"The LORD is my shepherd; I shall not want."\n\n'
        '**[narrator — KJV, Psalm 23:2]**\n"He maketh me to lie down in green pastures."\n\n'
        '**[narrator — KJV, Psalm 23:3]**\n"He restoreth my soul: he leadeth me in the paths of righteousness."\n\n'
        '**[narrator]**\nA distinct close.\n\n---\n## DEPTH\nx\n', encoding="utf-8")
    rep = L.run_lock(d, form="short", check_cluster=False)
    assert not rep["ok"] and any("Rule-8" in b for b in rep["blocking"]), rep["blocking"]


def test_long_form_not_rule8_blocked():
    # same 3 quotes are fine for a long-form (Rule-8 is short-only)
    d = Path(tempfile.mkdtemp()) / "l"
    d.mkdir()
    (d / "narration.md").write_text(
        '# T\n---\n**[narrator]**\nUnique opener.\n\n'
        '**[narrator — KJV, Psalm 23:1]**\n"The LORD is my shepherd; I shall not want."\n\n'
        '**[narrator — KJV, Psalm 23:2]**\n"He maketh me to lie down in green pastures."\n\n'
        '**[narrator — KJV, Psalm 23:3]**\n"He restoreth my soul."\n\n'
        '**[narrator]**\nA distinct close.\n\n---\n## DEPTH\nx\n', encoding="utf-8")
    rep = L.run_lock(d, form="long", check_cluster=False)
    assert not any("Rule-8" in b for b in rep["blocking"]), rep["blocking"]


def test_real_xml_tagged_file_locks_and_hashes():
    """The rendered narration-tagged.md is XML; spoken_hash/is_locked must work on
    it (the original Phase C crashed here)."""
    d = _mk("A unique opening about a still lake at dawn.", "Rest with Him now.", tagged=True)
    rep = L.run_lock(d, form="short", check_cluster=False)
    assert rep["ok"], rep["blocking"]
    ok, _ = L.is_locked(d)
    assert ok, "real XML tagged file failed to lock/hash"


def test_parity_mismatch_blocks():
    """If narration-tagged.md (rendered) diverges from narration.md (verified), lock
    must refuse (split-brain guard)."""
    d = _mk("A unique opening about a still lake at dawn.", "Rest with Him now.", tagged=True)
    # tamper ONLY the rendered tagged file
    (d / "narration-tagged.md").write_text(
        '<speaker name="narrator">A COMPLETELY DIFFERENT rendered script that was never verified.</speaker>\n',
        encoding="utf-8")
    rep = L.run_lock(d, form="short", check_cluster=False)
    assert not rep["ok"] and any("parity" in b for b in rep["blocking"]), rep["blocking"]


def test_punctuation_edit_busts_lock():
    """A comma edit (the exact Phase B defect) must make is_locked report stale —
    the hash must be punctuation-preserving."""
    d = _mk("A unique opening line, with a clause.", "Turn to Him, friend.", tagged=True)
    assert L.run_lock(d, form="short", check_cluster=False)["ok"]
    tg = d / "narration-tagged.md"
    tg.write_text(tg.read_text(encoding="utf-8").replace("opening line, with", "opening line with"),
                  encoding="utf-8")
    ok, why = L.is_locked(d)
    assert not ok, f"punctuation edit did not bust the lock: {why}"


def test_bad_sibling_does_not_crash_lock():
    """A garbage/empty sibling must be skipped, not crash an unrelated clean lock."""
    parent = Path(tempfile.mkdtemp())
    good = parent / "good"; good.mkdir()
    (good / "narration.md").write_text(
        '# T\n---\n**[narrator]**\nUnique opener here today.\n\n'
        '**[narrator — KJV, Psalm 23:1]**\n"The LORD is my shepherd; I shall not want."\n\n'
        '**[narrator]**\nA distinct close.\n\n---\n## DEPTH\nx\n', encoding="utf-8")
    bad = parent / "bad"; bad.mkdir()
    (bad / "narration.md").write_text("# garbage, no speaker blocks at all\n", encoding="utf-8")
    rep = L.run_lock(good, form="short", check_cluster=True)  # must not raise
    assert "bad" in (rep.get("warnings") or []), rep


def test_assembly_refuses_unlocked():
    """The assembly door must refuse an unlocked narration (multi-door enforcement)."""
    from pipeline import assembly_runner
    d = _mk("A unique opener for the assembly guard test.", "A distinct close here.", tagged=True)
    try:
        assembly_runner.run_assembly(d)
    except PermissionError:
        return
    except Exception as e:  # noqa - any other error means the guard didn't fire first
        raise AssertionError(f"assembly did not refuse-first on unlocked folder (got {type(e).__name__})")
    raise AssertionError("run_assembly did not refuse an unlocked folder")


def test_assembly_allows_locked():
    """After locking, the assembly guard must let it through (it then fails later for
    lack of clips/plan, which is fine — we only assert the guard didn't block)."""
    from pipeline import assembly_runner
    d = _mk("A unique opener for the locked assembly test.", "A distinct close here.", tagged=True)
    assert L.run_lock(d, form="short", check_cluster=False)["ok"]
    try:
        assembly_runner.run_assembly(d)
    except PermissionError:
        raise AssertionError("guard wrongly blocked a LOCKED folder")
    except BaseException:  # noqa - SystemExit/other downstream failure (no _turns) is fine
        pass  # we only assert the lock guard did NOT block a locked folder


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for t in tests:
        try:
            t(); print(f"[PASS] {t.__name__}"); passed += 1
        except AssertionError as e:
            print(f"[FAIL] {t.__name__}: {e}")
        except Exception as e:  # noqa
            print(f"[ERROR] {t.__name__}: {type(e).__name__}: {e}")
    print(f"\n{passed}/{len(tests)} tests passed")
    raise SystemExit(0 if passed == len(tests) else 1)
