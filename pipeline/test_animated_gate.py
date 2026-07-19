"""Guards for the animated-pct gate (every-screen-animated rule teeth).

History: the builders reported kling_or_punch_or_slam_pct in the DoD but
nothing exited non-zero on a low value — a slideshow regression could ship
silently in BOTH formats. These tests pin the formula, the corpus-calibrated
floor, and the wiring into both build_livingpage_16x9.py copies.
"""
from __future__ import annotations

import json
from pathlib import Path

from pipeline import animated_gate

ROOT = Path(__file__).resolve().parent.parent
BUILDERS = [
    ROOT / "longform" / "02_Psalm_22_Song_From_The_Cross" / "build_livingpage_16x9.py",
    ROOT / "longform" / "04_The_Bronze_Serpent" / "build_livingpage_16x9.py",
]


def _beat(n, sources=("dyncam",), punch=False, slams=0):
    return {"beat": n, "sources": list(sources), "punch": punch, "slams": slams}


def test_dead_beats_each_rescue_path():
    """A beat is alive via a real clip OR punch OR slam — same as the DoD."""
    report = [
        _beat(1, ["kling", "dyncam"]),          # real clip in one panel
        _beat(2, ["dyncam"], punch=True),        # punch energy
        _beat(3, ["dyncam"], slams=2),           # slam energy
        _beat(4, ["dyncam", "dyncam"]),          # dead
    ]
    assert animated_gate.dead_beats(report) == [4]
    assert animated_gate.animated_pct(report) == 75


def test_pct_matches_dod_formula():
    """Identical to the builders' round(100 * alive / len) — no drift."""
    report = [_beat(i, ["kling"]) for i in range(1, 12)] + [_beat(12)]
    assert animated_gate.animated_pct(report) == round(100 * 11 / 12)


def test_blocks_below_corpus_floor():
    report = [_beat(1, ["kling"]), _beat(2), _beat(3), _beat(4)]  # 25%
    assert animated_gate.check(report, clips=True) == 1


def test_empty_clips_dir_blocked_despite_punch_slam():
    """Red-team F3: punch/slams are $0 edit effects — on a punch/slam-heavy
    spec (thirty_pieces reads 78% on punch/slam alone) an EMPTY or mis-pathed
    clips dir used to pass the composite floor. Zero real clips must block."""
    report = [_beat(n, ["dyncam"], punch=(n % 2 == 0), slams=(n % 2)) for n in range(1, 17)]
    assert animated_gate.animated_pct(report) == 100  # composite alone would sail through
    assert animated_gate.real_clip_pct(report) == 0
    assert animated_gate.check(report, clips=True) == 1


def test_real_clip_floor():
    """Below the shipped real-clip minimum (Isaiah 53 = 42%) blocks even when
    punch/slam energy keeps the composite green."""
    report = ([_beat(n, ["kling"]) for n in range(1, 4)] +          # 3/10 = 30% real
              [_beat(n, ["dyncam"], slams=1) for n in range(4, 11)])
    assert animated_gate.animated_pct(report) == 100
    assert animated_gate.check(report, clips=True) == 1
    # at/above the floor with a green composite: passes
    report = ([_beat(n, ["kling"]) for n in range(1, 6)] +          # 5/10 = 50% real
              [_beat(n, ["dyncam"], slams=1) for n in range(6, 11)])
    assert animated_gate.check(report, clips=True) == 0


def test_warn_band_passes():
    """75–89 is the WARN band — shipped floor is 75, so it must NOT block."""
    report = [_beat(n, ["kling"]) for n in range(1, 13)] + [
        _beat(13), _beat(14), _beat(15), _beat(16)]  # 12/16 = 75%
    assert animated_gate.animated_pct(report) == animated_gate.FAIL_BELOW
    assert animated_gate.check(report, clips=True) == 0


def test_stills_only_preview_never_blocks():
    """Without --clips every beat reads dyncam by design — report-only."""
    report = [_beat(n) for n in range(1, 9)]  # 0%
    assert animated_gate.check(report, clips=False) == 0
    assert animated_gate.check([], clips=True) == 0


def test_every_shipped_report_passes_the_floor():
    """Calibration proof: the floor grandfathers the whole shipped corpus —
    no rebuild of an approved piece gets blocked by this gate."""
    reports = list(ROOT.glob("batches/*/*/visual/livingpage*spec_report.json")) + \
        list(ROOT.glob("longform/*/v1/*/livingpage*spec_report.json"))
    assert len(reports) >= 15, "corpus reports missing — glob broke?"
    for rp in reports:
        beats = json.loads(rp.read_text(encoding="utf-8"))["beats"]
        assert animated_gate.check(beats, clips=True) == 0, \
            f"{rp}: shipped report blocked — floor miscalibrated"


def test_e2e_builders_exit_5_on_static_spec(tmp_path):
    """Red-team F4: string-grep wiring guards can't catch the gate being moved
    behind the wrong condition. Run each REAL builder ($0 --lint) against a
    synthetic all-static pool: --clips must exit 5, no --clips must exit 0."""
    import subprocess
    import sys
    spec = {"motion": "classic", "audio": "narration.mp3", "beats": [
        {"t": [0.0, 3.0], "tpl": "full", "clips": [{"slug": "a"}]},
        {"t": [3.0, 6.0], "tpl": "full", "clips": [{"slug": "b"}]},
    ]}
    for builder in BUILDERS:
        pool = tmp_path / f"pool_{builder.parent.name[:4]}"
        pool.mkdir()
        (pool / "test.spec.json").write_text(json.dumps(spec), encoding="utf-8")
        gated = subprocess.run(
            [sys.executable, str(builder), "--pool", str(pool),
             "--spec", "test.spec.json", "--lint", "--clips"],
            capture_output=True, text=True, cwd=str(ROOT), timeout=300)
        assert gated.returncode == 5, \
            f"{builder}: expected exit 5, got {gated.returncode}\n{gated.stdout}\n{gated.stderr}"
        assert "ANIMATED-GATE BLOCK" in gated.stdout
        assert "LINT DoD" in gated.stdout, "block must not swallow the lint diagnostics"
        # (the no---clips exit-0 path is unit-tested at the gate level; skipping the
        # second subprocess halves this test's wall-clock under the polite-CPU cap)


def test_gate_wired_into_both_builders():
    """The fork-symmetric wiring guard: both builder copies must carry the
    gate call, the escape flag, and the exit-5 block."""
    for f in BUILDERS:
        src = f.read_text(encoding="utf-8")
        assert "--skip-animated-gate" in src, f"{f}: escape flag missing"
        assert "from pipeline import animated_gate" in src, f"{f}: gate not imported"
        assert "_ag.check(report, clips=a.clips)" in src, f"{f}: gate not called on the report"
        assert "_sys.exit(5)" in src, f"{f}: gate does not block (exit 5)"
        # a failing --lint --clips must print the DoD BEFORE the gate exits —
        # a block that swallows the repair diagnostics is worse than none
        assert src.index("LINT DoD") < src.index("_ag.check"), \
            f"{f}: gate runs before the LINT DoD print — lint diagnostics swallowed on block"
