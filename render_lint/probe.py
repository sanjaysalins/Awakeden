#!/usr/bin/env python
"""Model-calibration PROBE harness — learn what THIS model (HF seedream_v4_5, inked) actually
renders, by holding everything constant and varying ONLY the wording under test.

Why: with 1000+ stills ahead, guessing one redo at a time is too costly. A probe renders a
labelled MATRIX of prompt variants for one hard primitive (nail, healed scar, hands, face,
period, pose…), side by side, so we can SEE which phrasing the model gets right — then distil
the winner into rules.json + MODEL_COOKBOOK.md.

Probe renders live in `_probe/<name>/` and are NEVER added to the global asset index (they are
experiments, not deliverables).

  from render_lint import probe
  probe.run_matrix(out_dir, jobs, render_fn)   # jobs = [(label, full_prompt), ...]
"""
from __future__ import annotations
import html
from pathlib import Path


def run_matrix(out_dir: Path, jobs: list[tuple[str, str]], render_fn) -> list[tuple[str, str, str]]:
    """Render each (label, prompt) to out_dir/<NN_label>.png (idempotent) and build compare.html.
    render_fn(prompt, dest) -> status str ('ok'|'skip'|'fail'). Returns [(label, prompt, status)]."""
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for i, (label, prompt) in enumerate(jobs, 1):
        dest = out_dir / f"{i:02d}_{label}.png"
        status = "skip" if (dest.exists() and dest.stat().st_size > 0) else render_fn(prompt, dest)
        results.append((label, prompt, status))
        print(f"  [{status:4}] {dest.name}")
    build_compare_html(out_dir, results)
    return results


def build_compare_html(out_dir: Path, results: list[tuple[str, str, str]]) -> Path:
    cards = []
    for i, (label, prompt, status) in enumerate(results, 1):
        cards.append(
            f'<figure><img src="{i:02d}_{html.escape(label)}.png" alt="{html.escape(label)}">'
            f'<figcaption><b>{i:02d} · {html.escape(label)}</b> <small>[{status}]</small><br>'
            f'<span class=p>{html.escape(prompt)}</span></figcaption></figure>'
        )
    doc = (
        "<!doctype html><meta charset=utf-8><title>probe compare</title><style>"
        "body{background:#111;color:#eee;font-family:system-ui;margin:20px}"
        "h1{font-size:16px}.g{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}"
        "figure{margin:0}img{width:100%;border:1px solid #444;border-radius:6px}"
        "figcaption{font-size:12px;color:#ccc;margin-top:4px}.p{color:#8ab;font-size:11px}"
        "small{color:#888}</style>"
        f"<h1>Probe matrix — {html.escape(out_dir.name)} (vary only the tested clause)</h1>"
        '<div class=g>' + "".join(cards) + "</div>"
    )
    p = out_dir / "compare.html"
    p.write_text(doc, encoding="utf-8")
    print(f"\n  compare -> {p}")
    return p
