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
    # cap raised 2->3 (2026-06-25): 4 substantial KJV quotes still blocks a 60s short
    d = Path(tempfile.mkdtemp()) / "s"
    d.mkdir()
    (d / "narration.md").write_text(
        '# T\n---\n**[narrator]**\nUnique opener.\n\n'
        '**[narrator — KJV, Psalm 23:1]**\n"The LORD is my shepherd; I shall not want."\n\n'
        '**[narrator — KJV, Psalm 23:2]**\n"He maketh me to lie down in green pastures."\n\n'
        '**[narrator — KJV, Psalm 23:3]**\n"He restoreth my soul: he leadeth me in the paths of righteousness."\n\n'
        '**[narrator — KJV, Psalm 23:4]**\n"Yea, though I walk through the valley of the shadow of death, I will fear no evil."\n\n'
        '**[narrator]**\nA distinct close.\n\n---\n## DEPTH\nx\n', encoding="utf-8")
    rep = L.run_lock(d, form="short", check_cluster=False)
    assert not rep["ok"] and any("Rule-8" in b for b in rep["blocking"]), rep["blocking"]


def test_rule8_three_quotes_allowed_short():
    # cap raised 2->3 (2026-06-25, user): a tight quoted EXCHANGE of 3 substantial KJV
    # quotes paces in 59s (proven on #24) — must NOT be Rule-8 blocked
    d = Path(tempfile.mkdtemp()) / "s3"
    d.mkdir()
    (d / "narration.md").write_text(
        '# T\n---\n**[narrator]**\nUnique opener that sets the scene plainly.\n\n'
        '**[jesus — KJV, Psalm 23:1]**\n"The LORD is my shepherd; I shall not want."\n\n'
        '**[narrator — KJV, Psalm 23:2]**\n"He maketh me to lie down in green pastures."\n\n'
        '**[jesus — KJV, Psalm 23:3]**\n"He restoreth my soul: he leadeth me in the paths of righteousness."\n\n'
        '**[narrator]**\nA distinct close that lands the point.\n\n---\n## DEPTH\nx\n', encoding="utf-8")
    rep = L.run_lock(d, form="short", check_cluster=False)
    assert not any("Rule-8" in b for b in rep.get("blocking", [])), rep.get("blocking")


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


def test_stock_closer_blocks_lock():
    """Earned gate (narration_gate, promoted to blocking 2026-07-08): a 'Come to Jesus'
    closer with no KJV warrant for 'come' must refuse the lock."""
    d = _mk("The soldiers gambled for his clothes at the cross. They never looked up.",
            "But mercy stood over that cross all along. Come to Jesus today, and be saved.")
    rep = L.run_lock(d, form="short", check_cluster=False)
    assert not rep["ok"], "a stock closer must NOT lock"
    assert any(b.startswith("earned:") and "STOCK-CLOSER" in b for b in rep["blocking"]), rep["blocking"]
    assert not (d / ".locked").exists()


def test_unmarked_kjv_landing_locks():
    """A landing built on an UNMARKED verbatim KJV span (Rom 5:8 in narrator prose,
    no quote marks — the father_forgive_them shape) counts as the piece's own
    Scripture material and must lock cleanly."""
    d = _mk("A unique opening about the men with the hammer. They did not know whom they held.",
            "This is the gospel: while we were yet sinners, Christ died for us. "
            "That mercy is held out to you now, and it is enough.")
    rep = L.run_lock(d, form="short", check_cluster=False)
    assert rep["ok"], rep["blocking"]


def test_lf_movements_valid_structure_passes():
    """LF-G5: a well-formed 7-movement narration (>100 words each, total in band)
    returns no blocking findings."""
    from pipeline import validators as V
    body = ("word " * 160).strip()   # 160 spoken words per movement -> 1120 total
    md = "\n\n".join(f"## Movement {n} — Part {n}\n\n{body}" for n in range(1, 8))
    blocking, warnings = V.lf_movements(md)
    assert not blocking, blocking
    assert not warnings, warnings


def test_lf_movements_missing_and_short_blocks():
    """LF-G5: a missing movement (1..6 only) and an under-100-word movement both block."""
    from pipeline import validators as V
    body = ("word " * 160).strip()
    md6 = "\n\n".join(f"## Movement {n} — Part {n}\n\n{body}" for n in range(1, 7))
    blocking, _ = V.lf_movements(md6)
    assert any("expected exactly 1..7" in b for b in blocking), blocking

    thin = "\n\n".join(
        f"## Movement {n} — Part {n}\n\n" + (("word " * 160).strip() if n != 3 else "too short")
        for n in range(1, 8))
    blocking, _ = V.lf_movements(thin)
    assert any("Movement 3" in b for b in blocking), blocking


def test_lf_movements_word_budget_calibration():
    """LF-G5 word budget: within 10% of the 950-1400 band -> WARN only (Day of
    Atonement locked at 1426); beyond 10% -> BLOCK; delivery notes not counted."""
    from pipeline import validators as V
    # ~1430 total (within 1400*1.1) -> warn, not block
    body = ("word " * 204).strip()   # 204*7 = 1428
    md = "\n\n".join(f"## Movement {n} — X\n\n[not spoken delivery note]\n\n{body}" for n in range(1, 8))
    blocking, warnings = V.lf_movements(md)
    assert not blocking, blocking
    assert any("tolerance" in w for w in warnings), warnings
    # ~1800 total (>1400*1.1) -> block
    body = ("word " * 260).strip()
    md = "\n\n".join(f"## Movement {n} — X\n\n{body}" for n in range(1, 8))
    blocking, _ = V.lf_movements(md)
    assert any("total spoken words" in b for b in blocking), blocking


def _lf_plan(n_per_mvt=3, jesus_last=True, jesus_pct_scenes=None, atmos="dust drifts",
             subject="a lone figure on a hill, one continuous image, no frame, no border"):
    """Synthesize a minimal valid long scene plan (7 movements x n scenes)."""
    scenes, sid = [], 0
    for m in range(1, 8):
        for _ in range(n_per_mvt):
            sid += 1
            scenes.append({"id": sid, "mvt": f"M{m} Part", "t": [(sid - 1) * 20.0, sid * 20.0],
                           "jesus": False, "atmos": atmos, "subject_block": subject})
    if jesus_last:
        scenes[-1]["jesus"] = True
    return {"scenes": scenes}


def test_lf_scene_plan_valid_passes():
    from pipeline import validators as V
    blocking, _ = V.lf_scene_plan(_lf_plan())
    assert not blocking, blocking


def test_lf_scene_plan_gaps_block():
    """Missing movement coverage, no Christ-close, missing atmos, asserted banned
    token each block; negated tokens ('no frame') never do."""
    from pipeline import validators as V
    plan = _lf_plan()
    for s in plan["scenes"]:
        if s["mvt"].startswith("M5"):
            s["mvt"] = "M4 Part"          # M5 now has 0 scenes
    plan["scenes"][-1]["jesus"] = False   # no Christ-close
    plan["scenes"][0]["atmos"] = ""       # missing veo3 hint
    plan["scenes"][1]["subject_block"] = "a neon sign over a split screen diagram"
    blocking, _ = V.lf_scene_plan(plan)
    joined = " | ".join(blocking)
    assert "movement M5" in joined and "close on Christ" in joined
    assert "missing the veo3" in joined and "banned tokens" in joined


def test_lf_scene_plan_count_is_advisory():
    """Scene count out of the LF-INV-4 band WARNs, never blocks (the locked dense
    rebuilds run 27-32 scenes)."""
    from pipeline import validators as V
    blocking, warnings = V.lf_scene_plan(_lf_plan(n_per_mvt=5))   # 35 scenes
    assert not blocking, blocking
    assert any("cap of 25" in w for w in warnings), warnings


def test_lf_assembly_valid_passes():
    from pipeline import validators as V
    plan = _lf_plan()   # contiguous 20s windows, opens M1, closes jesus
    blocking, warnings = V.lf_assembly(plan, audio_dur=plan["scenes"][-1]["t"][1])
    assert not blocking, blocking
    assert any("hero" in w for w in warnings)   # no hero flag -> WARN, not block


def test_lf_assembly_tiling_and_frame_block():
    from pipeline import validators as V
    plan = _lf_plan()
    plan["scenes"][3]["t"][0] += 2.0             # 2s gap before scene 4
    plan["scenes"][0]["mvt"] = "M2 Wrong"        # doesn't open on M1
    plan["scenes"][-1]["jesus"] = False          # doesn't close on Christ
    audio = plan["scenes"][-1]["t"][1] + 10      # audio outruns the windows
    blocking, _ = V.lf_assembly(plan, audio_dur=audio)
    joined = " | ".join(blocking)
    assert "gap between scene" in joined and "must open on M1" in joined
    assert "close on Christ" in joined and "tail is uncovered" in joined


def test_lf_assembly_movement_clips_and_hero(tmp_path):
    from pipeline import validators as V
    plan = _lf_plan()
    # clips on disk for every scene except movement M4's three scenes
    m4_ids = {s["id"] for s in plan["scenes"] if s["mvt"].startswith("M4")}
    for s in plan["scenes"]:
        if s["id"] not in m4_ids:
            (tmp_path / f"{s['id']:02d}_x.mp4").write_bytes(b"0")
    plan["scenes"][2]["hero"] = True             # hero early in the film
    audio = plan["scenes"][-1]["t"][1]
    blocking, _ = V.lf_assembly(plan, audio_dur=audio, clips_dir=tmp_path)
    joined = " | ".join(blocking)
    assert "movement M4 has no rendered clip" in joined
    assert "end before the final 90s" in joined


def test_clip_qc_dir_status_and_lf_criteria(tmp_path):
    """The long-lane clip-QC surface: dir_status over any clips dir, fail-closed
    sidecar states, and the LF criteria carrying the veo3 rules."""
    from pipeline import clip_qc as CQ
    a, b, c = tmp_path / "01_a.mp4", tmp_path / "02_b.mp4", tmp_path / "03_c.mp4"
    for f in (a, b, c):
        f.write_bytes(b"0")
    CQ.record_verdict(a, True)
    CQ.record_verdict(b, False, issues=["subject locomotion"])
    rows = {r["clip"]: r["state"] for r in CQ.dir_status(tmp_path)}
    assert rows == {"01_a.mp4": "PASS", "02_b.mp4": "FAIL", "03_c.mp4": "UNVERIFIED"}
    assert CQ.is_verified(a) and not CQ.is_verified(b) and not CQ.is_verified(c)
    for needle in ("ATMOSPHERE-ONLY", "NO-INVENT", "NO-WRITING-ANIMATED"):
        assert needle in CQ.LF_CRITERIA


def test_lf_movements_non_movement_format_warns_only():
    """A long narration with no '## Movement' headers (legacy/witness format) must
    WARN, never block — re-locks of Isaiah 53 / Psalm 22 cannot be broken."""
    from pipeline import validators as V
    blocking, warnings = V.lf_movements("# Some Legacy Long\n\nProse without movement headers.")
    assert not blocking, blocking
    assert warnings and "NOT checked" in warnings[0], warnings


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
