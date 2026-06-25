"""Regression tests for the Awakeden eyewitness deterministic gates (EW-G1..EW-G6).

Proves each gate FAILS-CLOSED on a fixture that trips exactly it, and that a clean
eyewitness narration passes all six. Mirrors pipeline/test_validation.py style.

Run: .venv\\Scripts\\python.exe -m pytest pipeline/test_eyewitness.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from pipeline import eyewitness_gates as EW

FX = Path(__file__).resolve().parent / "eyewitness_fixtures"
REPO = Path(__file__).resolve().parent.parent


def _gates(name: str, form: str = "short") -> dict[str, EW.GateResult]:
    f = FX / name
    md = (f / "narration.md").read_text(encoding="utf-8")
    passage = EW.load_passage(f)
    return {r.gate: r for r in EW.run_gates(md, form, passage)}


def _fails(name: str, form: str = "short") -> list[str]:
    return [g for g, r in _gates(name, form).items() if not r.ok and r.blocking]


# ---- the GOOD fixture passes all six -----------------------------------------

def test_good_short_passes_all_gates():
    fails = _fails("good_short")
    assert fails == [], f"good fixture should pass every gate; failed {fails}"


# ---- each BAD fixture trips EXACTLY one gate (fail-closed) --------------------

def test_bad_altered_kjv_trips_only_g1():
    assert _fails("bad_altered_kjv") == ["EW-G1"]


def test_bad_missing_beat_trips_only_g2():
    assert _fails("bad_missing_beat") == ["EW-G2"]


def test_bad_words_under_trips_only_g3():
    assert _fails("bad_words_under") == ["EW-G3"]


def test_bad_words_over_trips_only_g3():
    assert _fails("bad_words_over") == ["EW-G3"]


def test_bad_cta_no_jesus_trips_only_g4():
    assert _fails("bad_cta_no_jesus") == ["EW-G4"]


def test_bad_third_person_trips_only_g5():
    assert _fails("bad_third_person") == ["EW-G5"]


def test_bad_single_voice_trips_only_g6():
    assert _fails("bad_single_voice") == ["EW-G6"]


# ---- each NEW / TIGHTENED-gate BAD fixture trips EXACTLY its one gate ---------

def test_bad_invented_god_speech_trips_only_g11():
    # a **[the LORD]** line of invented prose with NO **"..."** KJV quote
    assert _fails("bad_invented_god_speech") == ["EW-G11"]


def test_bad_templated_reveal_trips_only_g12():
    # spoken text contains the banned templated stinger "at last I understood"
    assert _fails("bad_templated_reveal") == ["EW-G12"]


def test_bad_reveal_no_christ_trips_only_g12():
    # reveal beat body never names Jesus/Christ; everything else is fine
    assert _fails("bad_reveal_no_christ") == ["EW-G12"]


def test_bad_fear_cta_trips_only_g4():
    # close names Jesus + a verb but adds a fear / gain-loss phrase
    assert _fails("bad_fear_cta") == ["EW-G4"]


def test_bad_essay_density_trips_only_g5():
    # clears the raw first-person FLOOR by count but density < 4.0 (essay-narrator)
    assert _fails("bad_essay_density") == ["EW-G5"]


def test_bad_essay_density_clears_floor_but_fails_on_density():
    # prove the trip is the DENSITY teeth, not the raw floor
    md = (FX / "bad_essay_density" / "narration.md").read_text(encoding="utf-8")
    res = {r.gate: r for r in EW.run_gates(md, "short", EW.load_passage(FX / "bad_essay_density"))}
    g5 = res["EW-G5"]
    assert not g5.ok and "density" in g5.detail.lower(), g5.detail


def test_bad_misattributed_kjv_trips_only_g1():
    # a VERBATIM real KJV quote whose words are NOT in this folder's passage.txt
    assert _fails("bad_misattributed_kjv") == ["EW-G1"]


# ---- the failing gates are BLOCKING (would refuse the LOCK) -------------------

def test_blocking_findings_nonempty_for_each_bad():
    for name, gate in [
        ("bad_altered_kjv", "EW-G1"), ("bad_missing_beat", "EW-G2"),
        ("bad_words_under", "EW-G3"), ("bad_cta_no_jesus", "EW-G4"),
        ("bad_third_person", "EW-G5"), ("bad_single_voice", "EW-G6"),
        ("bad_invented_god_speech", "EW-G11"), ("bad_templated_reveal", "EW-G12"),
        ("bad_reveal_no_christ", "EW-G12"), ("bad_fear_cta", "EW-G4"),
        ("bad_essay_density", "EW-G5"), ("bad_misattributed_kjv", "EW-G1"),
    ]:
        f = FX / name
        md = (f / "narration.md").read_text(encoding="utf-8")
        res = EW.run_gates(md, "short", EW.load_passage(f))
        blk = EW.blocking_findings(res)
        assert any(gate in b for b in blk), f"{name}: expected a blocking {gate} finding; got {blk}"


# ---- EW-G1 fail-closes when quotes exist but no passage is supplied -----------

def test_g1_failcloses_without_passage():
    md = (FX / "good_short" / "narration.md").read_text(encoding="utf-8")
    parsed = EW.parse_witness(md)
    r = EW.ew_g1_kjv(parsed, passage=None)
    assert not r.ok and r.blocking, "quotes present but no corpus must fail-closed"


def test_g1_passes_when_no_quotes():
    md = (FX / "bad_single_voice" / "narration.md").read_text(encoding="utf-8")  # has no KJV quotes
    parsed = EW.parse_witness(md)
    r = EW.ew_g1_kjv(parsed, passage=None)
    assert r.ok, "a narration with no bold KJV quotes passes G1 vacuously"


# ---- EW-G4 catches the banned bare-CTA template ------------------------------

_BANNED_CTA_MD = """# X — Awakeden eyewitness (short)
**Witness:** y
---
## Beat 1 — I was there
I stood and I watched and I remember it all with my own eyes.
## Beat 2 — The act
I did the thing with my own two hands that day at the altar.
## Beat 3 — The reveal
And at last I understood what it had always pointed to.
## Beat 4 — The invitation
Will you trust Him? Come to Jesus today.
"""


def test_g4_blocks_banned_cta_template():
    rules = EW.load_rules()
    parsed = EW.parse_witness(_BANNED_CTA_MD)
    r = EW.ew_g4_cta(parsed, rules)
    assert not r.ok and any("banned" in f.lower() for f in r.findings), r.findings


# ---- LONG form: spine (7 beats) + word budget --------------------------------

def _long_md(beats: list[tuple[int, str]], words_per_beat: int) -> str:
    head = ("# Long Witness — Awakeden eyewitness (long)\n"
            "**Witness:** a long witness\n---\n")
    filler = "I carried the bowl to the altar and my hands did not tremble that day. "
    reps = max(1, words_per_beat // len(filler.split()))
    body = []
    for i, (n, name) in enumerate(beats):
        body.append(f"## Beat {n} — {name}")
        line = (filler * reps).strip()
        if i == 0:
            line = "**[the priest]** " + line  # a named voice -> cast >= 2 (witness + scripture/priest)
        if n == 6:                              # EW-G12: the reveal beat body must NAME Christ
            line += (" It was Christ all along, the true and final sacrifice that the "
                     "altar had only ever foreshadowed.")
        if i == len(beats) - 1:
            line += " Come to Jesus, and trust Him, and receive His mercy."
        body.append(line)
    return head + "\n".join(body) + "\n"


_LONG_BEATS = [
    (1, "I was there"), (2, "The world"), (3, "The act"), (4, "The strange detail"),
    (5, "The wrestling"), (6, "The reveal"), (7, "The invitation"),
]


def test_long_good_passes_all_gates():
    md = _long_md(_LONG_BEATS, words_per_beat=210)
    res = {r.gate: r for r in EW.run_gates(md, "long", passage=None)}
    fails = [g for g, r in res.items() if not r.ok]
    n = len(EW.parse_witness(md).spoken_text.split())
    assert fails == [], f"clean LONG should pass all; failed {fails} (words={n})"
    assert 1300 <= n <= 1650, f"sanity: builder produced {n} words"


def test_long_missing_beat_fails_g2():
    md = _long_md([b for b in _LONG_BEATS if b[0] != 5], words_per_beat=240)  # drop beat 5
    res = {r.gate: r for r in EW.run_gates(md, "long", passage=None)}
    assert not res["EW-G2"].ok, "LONG missing one of the 7 beats must fail spine"


def test_long_under_budget_fails_g3():
    md = _long_md(_LONG_BEATS, words_per_beat=40)  # ~280 words, way under the long floor
    res = {r.gate: r for r in EW.run_gates(md, "long", passage=None)}
    assert not res["EW-G3"].ok, "LONG under 1300 words must fail the budget gate"


def test_long_budget_rejects_short_sized_script():
    # a SHORT-sized 268-word script is far below the LONG floor
    md = (FX / "good_short" / "narration.md").read_text(encoding="utf-8")
    res = {r.gate: r for r in EW.run_gates(md, "long", passage=EW.load_passage(FX / "good_short"))}
    assert not res["EW-G3"].ok, "a short-length script must fail the LONG word budget"


# ---- parser sanity -----------------------------------------------------------

def test_parser_extracts_spine_quotes_and_cast():
    md = (FX / "good_short" / "narration.md").read_text(encoding="utf-8")
    p = EW.parse_witness(md)
    assert [b.n for b in p.beats] == [1, 2, 3, 4]
    assert len(p.kjv_quotes) == 1
    assert p.speaker_tags == ["the Pharisees"]
    assert p.has_witness_prose


# ---- the CLI lock chokepoint -------------------------------------------------

def test_cli_lock_locks_good_and_refuses_bad(tmp_path):
    # GOOD: copy to a temp folder so we don't write .locked into the repo fixtures
    good = tmp_path / "good"
    good.mkdir()
    (good / "narration.md").write_text((FX / "good_short" / "narration.md").read_text(encoding="utf-8"), encoding="utf-8")
    (good / "passage.txt").write_text((FX / "good_short" / "passage.txt").read_text(encoding="utf-8"), encoding="utf-8")
    r = subprocess.run([sys.executable, "cli_witness_lock.py", str(good), "--form", "short"],
                       cwd=REPO, capture_output=True, text=True)
    assert r.returncode == 0, f"good fixture should LOCK; stdout:\n{r.stdout}\n{r.stderr}"
    assert (good / ".locked").is_file(), "a passing lock must write .locked"
    data = json.loads((good / ".locked").read_text(encoding="utf-8"))
    assert data["form"] == "short" and data["gates_run"]

    # --status now reports LOCKED
    rs = subprocess.run([sys.executable, "cli_witness_lock.py", str(good), "--form", "short", "--status"],
                        cwd=REPO, capture_output=True, text=True)
    assert rs.returncode == 0 and "LOCKED" in rs.stdout

    # editing the spoken text busts the lock (stale)
    (good / "narration.md").write_text(
        (good / "narration.md").read_text(encoding="utf-8") + "\nI add a stray spoken line here.\n",
        encoding="utf-8")
    rs2 = subprocess.run([sys.executable, "cli_witness_lock.py", str(good), "--form", "short", "--status"],
                         cwd=REPO, capture_output=True, text=True)
    assert rs2.returncode == 1 and "UNLOCKED" in rs2.stdout, "an edit must stale-bust the lock"

    # BAD: a fixture that trips a gate must be REFUSED (non-zero, no .locked)
    bad = tmp_path / "bad"
    bad.mkdir()
    (bad / "narration.md").write_text((FX / "bad_altered_kjv" / "narration.md").read_text(encoding="utf-8"), encoding="utf-8")
    (bad / "passage.txt").write_text((FX / "bad_altered_kjv" / "passage.txt").read_text(encoding="utf-8"), encoding="utf-8")
    rb = subprocess.run([sys.executable, "cli_witness_lock.py", str(bad), "--form", "short"],
                        cwd=REPO, capture_output=True, text=True)
    assert rb.returncode == 1, "a blocking finding must exit non-zero"
    assert not (bad / ".locked").is_file(), "a refused lock must NOT write .locked"


# ---- cross-episode cluster guard (block a slate of near-identical episodes) ---

def _seed_episode(folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "narration.md").write_text(
        (FX / "good_short" / "narration.md").read_text(encoding="utf-8"), encoding="utf-8")
    (folder / "passage.txt").write_text(
        (FX / "good_short" / "passage.txt").read_text(encoding="utf-8"), encoding="utf-8")


def test_cluster_blocks_near_identical_sibling(tmp_path):
    import cli_witness_lock as WL
    parent = tmp_path / "slate"
    ep_a = parent / "ep_a"
    ep_b = parent / "ep_b"

    # lock the FIRST while it stands alone (no sibling yet -> no cluster collision)
    _seed_episode(ep_a)
    r1 = subprocess.run([sys.executable, "cli_witness_lock.py", str(ep_a), "--form", "short"],
                        cwd=REPO, capture_output=True, text=True)
    assert r1.returncode == 0, f"first episode should LOCK; stdout:\n{r1.stdout}\n{r1.stderr}"
    assert (ep_a / ".locked").is_file()

    # now drop a near-identical second episode beside it -> the cluster guard must catch it
    _seed_episode(ep_b)
    findings = WL.cluster_findings(ep_b, WL.EW.load_rules())
    assert findings and any("gram" in f for f in findings), \
        f"a near-identical sibling must yield a cluster finding; got {findings}"

    r2 = subprocess.run([sys.executable, "cli_witness_lock.py", str(ep_b), "--form", "short"],
                        cwd=REPO, capture_output=True, text=True)
    assert r2.returncode == 1, f"the second near-identical episode must be BLOCKED; stdout:\n{r2.stdout}"
    assert "CLUSTER" in r2.stdout, f"expected an EW-CLUSTER finding; stdout:\n{r2.stdout}"
    assert not (ep_b / ".locked").is_file(), "a clustered-blocked episode must NOT write .locked"


# ---- require_lock enforcement guard ------------------------------------------

def test_require_lock_raises_on_unlocked_and_returns_on_locked(tmp_path):
    import cli_witness_lock as WL
    import pytest

    ep = tmp_path / "ep"
    _seed_episode(ep)

    # unlocked -> SystemExit (audio/video may never render an unlocked narration)
    with pytest.raises(SystemExit):
        WL.require_lock(ep, "short")

    # lock it, then require_lock returns cleanly
    r = subprocess.run([sys.executable, "cli_witness_lock.py", str(ep), "--form", "short"],
                       cwd=REPO, capture_output=True, text=True)
    assert r.returncode == 0, f"should LOCK; stdout:\n{r.stdout}\n{r.stderr}"
    WL.require_lock(ep, "short")  # must NOT raise

    # editing the spoken text stales the lock -> require_lock raises again
    (ep / "narration.md").write_text(
        (ep / "narration.md").read_text(encoding="utf-8") + "\nI add one more spoken line.\n",
        encoding="utf-8")
    with pytest.raises(SystemExit):
        WL.require_lock(ep, "short")


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-q"]))
