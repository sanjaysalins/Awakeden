"""Generic element-gate sweep for ANY short (generalizes the #03 one-off `_bakeoff/03sweep`).

Phase-0 tooling for the fix-all plan. Per short:
  sweep   — extract a filmstrip per clip + build <short>/_sweep/sweep_review.html, seed queue_state.
  record  — the agent records its look as an element-gate verdict (clip_element_gate sidecar).
  status  — show the per-clip verdicts + queue state.

The vision LOOK is done by the agent (reads the strips); this tool does the deterministic parts:
strip extraction, the review page, verdict recording, and the cross-short queue_state.json so
'park-and-proceed' is real persisted state, not manual bookkeeping.

Run:
  .venv\\Scripts\\python.exe -m pipeline.element_gate_sweep sweep "<short folder>"
  .venv\\Scripts\\python.exe -m pipeline.element_gate_sweep record "<short folder>" <scene> pass|fail "foreign;.."
  .venv\\Scripts\\python.exe -m pipeline.element_gate_sweep status "<short folder>"
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

from pipeline import clip_element_gate as G


def _nbp(short: Path, provider: str = "nbp") -> Path:
    return Path(short) / "visual" / provider


def _sweep_dir(short: Path) -> Path:
    d = Path(short) / "_sweep"
    d.mkdir(exist_ok=True)
    return d


def _clips(short: Path, provider: str = "nbp") -> list[Path]:
    return sorted(_nbp(short, provider).glob("[0-9][0-9]_*.mp4"))


def build_strips(short: Path, provider: str = "nbp") -> list[Path]:
    """One 5-frame filmstrip per clip for the agent look (deterministic ffmpeg)."""
    sd = _sweep_dir(short)
    strips = []
    for mp4 in _clips(short, provider):
        out = sd / f"strip_{mp4.stem}.jpg"
        # 12 frames (4x3) over the clip — 5 was too sparse and let invented motion (a hand on
        # a punch-in) slip past the agent look. Denser sampling catches clip-level invention.
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(mp4),
                        "-vf", "fps=2.4,scale=210:-1,tile=4x3", "-frames:v", "1", str(out)],
                       check=False)
        if out.exists():
            strips.append(out)
    return strips


def _verdict_row(mp4: Path) -> dict:
    sc = mp4.with_suffix(mp4.suffix + ".elementgate.json")
    if not sc.exists():
        return {"state": "UNSWEPT", "foreign": []}
    try:
        d = json.loads(sc.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"state": "BAD-SIDECAR", "foreign": []}
    if not d.get("audited"):
        return {"state": "UNSWEPT", "foreign": []}
    return {"state": "PASS" if d.get("passed") else "FAIL", "foreign": d.get("foreign", [])}


def queue_state(short: Path, provider: str = "nbp") -> dict:
    rows = []
    for mp4 in _clips(short, provider):
        rows.append({"scene": int(mp4.stem[:2]), "clip": mp4.stem, **_verdict_row(mp4)})
    swept = all(r["state"] not in ("UNSWEPT", "BAD-SIDECAR") for r in rows) and bool(rows)
    fails = [r for r in rows if r["state"] == "FAIL"]
    st = {"short": Path(short).name, "clips": len(rows),
          "status": "swept" if swept else "in-progress",
          "fails": [r["clip"] for r in fails], "rows": rows}
    (_sweep_dir(short) / "queue_state.json").write_text(json.dumps(st, indent=2), encoding="utf-8")
    return st


def build_page(short: Path, provider: str = "nbp") -> Path:
    rows = queue_state(short, provider)["rows"]
    cards = []
    for r in rows:
        cls = {"PASS": "pass", "FAIL": "fail"}.get(r["state"], "unswept")
        cards.append(
            f'<div class="card {cls}"><div class="lab">scene {r["scene"]:02d} · {r["clip"][3:]} '
            f'· <b>{r["state"]}</b></div><img src="strip_{r["clip"]}.jpg">'
            + (f'<div class="bad">foreign: {", ".join(r["foreign"])}</div>' if r["foreign"] else "")
            + '</div>')
    html = ("<!doctype html><meta charset=utf-8><title>element-gate sweep</title><style>"
            "body{background:#111;color:#eee;font-family:system-ui;padding:18px}"
            ".card{margin:8px 0;padding:8px;border-radius:8px;border:1px solid #333}"
            ".pass{border-color:#3a6}.fail{border-color:#e44;background:#2a1414}"
            ".unswept{border-color:#a80;opacity:.85}img{width:100%;max-width:1000px;border-radius:6px;margin:6px 0}"
            ".lab{font-size:14px}.bad{color:#f88;font-size:12px}</style>"
            f"<h1>{Path(short).name} — element-gate sweep</h1>"
            f"<p>{sum(1 for r in rows if r['state']=='PASS')} PASS · "
            f"{sum(1 for r in rows if r['state']=='FAIL')} FAIL · "
            f"{sum(1 for r in rows if r['state']=='UNSWEPT')} unswept</p>" + "".join(cards))
    p = _sweep_dir(short) / "sweep_review.html"
    p.write_text(html, encoding="utf-8")
    return p


def record(short: Path, scene: int, passed: bool, foreign: list[str], provider: str = "nbp") -> Path:
    matches = [m for m in _clips(short, provider) if int(m.stem[:2]) == scene]
    if not matches:
        raise FileNotFoundError(f"no clip for scene {scene} in {short}")
    if len(matches) > 1:                       # ambiguous — don't silently verdict the wrong one
        raise ValueError(f"scene {scene} matches {len(matches)} clips ({[m.stem for m in matches]}); "
                         "pass a unique slot")
    mp4 = matches[0]
    sc = G.record_verdict(mp4, passed, foreign=foreign, note="element-gate sweep (agent look)")
    queue_state(short, provider)
    return sc


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if len(a) >= 2 and a[0] == "sweep":
        short = Path(a[1])
        n = len(build_strips(short))
        page = build_page(short)
        print(f"swept {n} clips -> {page}\n  record each: python -m pipeline.element_gate_sweep "
              f"record \"{short}\" <scene> pass|fail \"foreign;..\"")
        raise SystemExit(0)
    if len(a) >= 4 and a[0] == "record":
        passed = a[3] in ("1", "pass", "PASS", "true")
        foreign = [x.strip() for x in (a[4].split(";") if len(a) > 4 else []) if x.strip()]
        sc = record(Path(a[1]), int(a[2]), passed, foreign)
        print(f"recorded scene {a[2]} {'PASS' if passed else 'FAIL'} -> {sc}")
        build_page(Path(a[1]))
        raise SystemExit(0)
    if len(a) >= 2 and a[0] == "status":
        st = queue_state(Path(a[1]))
        print(f"{st['short']}: {st['status']} — {st['clips']} clips, FAIL: {st['fails'] or 'none'}")
        raise SystemExit(0)
    print("usage: element_gate_sweep sweep|record|status <short> ...")
