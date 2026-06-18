"""Blind calibration set — measure the gate's PRECISION and RECALL honestly.

The red-team's point: recall was only ever measured against the user's 24 flags (not an
exhaustive label set), and the ~87 machine flags have NO ground truth — so we cannot tell
true catches from false alarms. Fix: draw a STRATIFIED RANDOM sample (predicted-PASS +
predicted-FAIL, across sources), present it BLIND (machine verdict hidden), let the human/panel
label each PASS/BAD, then SCORE labels vs machine to get precision + recall with a real denominator.

  sample : pick a seeded stratified sample -> calibration_sample.html (blind) + calibration_targets.json
  score  : read your labels (calibration_labels.json: {"bad":[paths]}) vs machine -> precision/recall

Run: .venv\\Scripts\\python.exe v2\\coherence_audit\\build_calibration_set.py sample [--n 50] [--seed 7]
     .venv\\Scripts\\python.exe v2\\coherence_audit\\build_calibration_set.py score
"""
from __future__ import annotations
import html
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))
from pipeline import coherence  # noqa: E402

TARGETS = HERE / "calibration_targets.json"
LABELS = HERE / "calibration_labels.json"


def _machine_verdict(png: Path):
    """(audited, passed) from the coherence sidecar, or (False, None) if none."""
    sc = png.with_suffix(png.suffix + ".coherence.json")
    if not sc.exists():
        return (False, None)
    try:
        d = json.loads(sc.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return (False, None)
    return (bool(d.get("audited")), d.get("passed"))


def sample(n: int = 50, seed: int = 7) -> dict:
    stills = coherence.sweep_pool()
    preds = {"pass": [], "fail": []}
    for p in stills:
        aud, passed = _machine_verdict(p)
        if not aud:
            continue
        preds["pass" if passed else "fail"].append(p)
    rng = random.Random(seed)
    half = n // 2
    chosen = (rng.sample(preds["pass"], min(half, len(preds["pass"]))) +
              rng.sample(preds["fail"], min(n - half, len(preds["fail"]))))
    rng.shuffle(chosen)            # shuffle so the order doesn't leak the stratum
    targets = []
    for p in chosen:
        aud, passed = _machine_verdict(p)
        targets.append({"still": str(p.relative_to(ROOT)).replace("\\", "/"),
                        "machine_passed": bool(passed)})
    TARGETS.write_text(json.dumps({"_README": "Blind calibration targets + the HIDDEN machine "
                                   "verdict (for scoring only — not shown on the blind page).",
                                   "seed": seed, "n": len(targets), "targets": targets},
                                  indent=2, ensure_ascii=False), encoding="utf-8")
    _write_blind_html(targets)
    return {"n": len(targets), "pool_pass": len(preds["pass"]), "pool_fail": len(preds["fail"])}


def _write_blind_html(targets: list[dict]) -> Path:
    cards = []
    for t in targets:
        src = "file:///" + str(ROOT / t["still"]).replace("\\", "/")
        cards.append(f'''<div class="card" data-path="{html.escape(t["still"])}" onclick="flag(this)">
  <img loading="lazy" src="{html.escape(src)}">
  <div class="flagtag">BAD</div></div>''')
    doc = f'''<!doctype html><html><head><meta charset="utf-8"><title>Blind calibration — flag BAD</title>
<style>
 body{{font-family:system-ui,Arial;margin:0;background:#14161a;color:#e8e6e0}}
 .bar{{position:sticky;top:0;background:#0d0f12;border-bottom:1px solid #333;padding:12px 18px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}}
 .count{{color:#ff5252;font-weight:700;font-size:20px}}
 button{{font-size:15px;padding:8px 14px;border-radius:8px;border:0;cursor:pointer;background:#2a6;color:#fff}}
 .row{{display:flex;flex-wrap:wrap;gap:12px;padding:14px}}
 .card{{width:260px;border:3px solid #2a2e36;border-radius:9px;overflow:hidden;cursor:pointer;position:relative;background:#1d2026}}
 .card.flagged{{border-color:#ff3b3b;box-shadow:0 0 0 2px #ff3b3b inset}}
 .card img{{width:100%;display:block;background:#000}}
 .flagtag{{position:absolute;top:6px;right:6px;background:#ff3b3b;color:#fff;font-weight:700;padding:3px 8px;border-radius:6px;display:none}}
 .card.flagged .flagtag{{display:block}}
</style></head><body>
<div class="bar"><b>BLIND calibration — no verdicts shown. Click every still you judge NOT fit for use.</b>
 <span class="count"><span id="n">0</span> flagged</span>
 <button onclick="cp()">Copy flagged JSON</button>
 <span style="color:#9a9">{len(targets)} stills · paste the JSON back to score precision/recall</span></div>
<div class="row">{''.join(cards)}</div>
<script>
 const f=new Set();
 function flag(c){{const p=c.dataset.path; if(c.classList.toggle('flagged'))f.add(p);else f.delete(p); document.getElementById('n').textContent=f.size;}}
 function cp(){{navigator.clipboard.writeText(JSON.stringify({{bad:[...f].sort()}},null,2)); alert(f.size+' flagged copied — paste back to Claude or save as calibration_labels.json');}}
</script></body></html>'''
    p = HERE / "calibration_sample.html"
    p.write_text(doc, encoding="utf-8")
    return p


def score() -> dict:
    if not (TARGETS.exists() and LABELS.exists()):
        raise SystemExit("need calibration_targets.json (run sample) AND calibration_labels.json (your labels)")
    targets = json.loads(TARGETS.read_text(encoding="utf-8"))["targets"]
    human_bad = set(json.loads(LABELS.read_text(encoding="utf-8")).get("bad", []))
    tp = fp = tn = fn = 0
    for t in targets:
        aud, passed = _machine_verdict(ROOT / t["still"])   # LIVE verdict (reflects retunes)
        machine_bad = aud and (passed is False)              # machine says FAIL == predicts bad
        human = t["still"] in human_bad
        if machine_bad and human: tp += 1
        elif machine_bad and not human: fp += 1
        elif not machine_bad and human: fn += 1
        else: tn += 1
    precision = tp / (tp + fp) if (tp + fp) else None
    recall = tp / (tp + fn) if (tp + fn) else None
    return {"n": len(targets), "tp": tp, "fp": fp, "tn": tn, "fn": fn,
            "precision": precision, "recall": recall}


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "score":
        r = score()
        print(f"calibration (n={r['n']}): TP {r['tp']} FP {r['fp']} TN {r['tn']} FN {r['fn']}")
        print(f"  precision = {r['precision']}  (of machine-FAILs, how many were truly bad)")
        print(f"  recall    = {r['recall']}  (of truly-bad, how many machine caught)")
    else:
        n = 50; seed = 7
        if "--n" in args: n = int(args[args.index("--n") + 1])
        if "--seed" in args: seed = int(args[args.index("--seed") + 1])
        st = sample(n, seed)
        print(f"blind sample of {st['n']} (pool: {st['pool_pass']} pred-PASS / {st['pool_fail']} pred-FAIL)")
        print(f"  -> {HERE / 'calibration_sample.html'}  (label it blind)")
        print(f"  -> {HERE / 'calibration_targets.json'}  (hidden verdicts for scoring)")
