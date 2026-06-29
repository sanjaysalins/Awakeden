r"""bible_calibrate.py — Layer 2: prove the IMAGE audit actually discriminates.

Runs the bible image-audit over a blind-labelled set (bible_kb/_calibration/labels.json)
and measures it against the human labels — so we TRUST the gate's fail-rate instead of
assuming it (per memory feedback-gate-calibration-human-authority: calibrate vs blind
human labels before trusting an LLM-vision gate).

A 'fail' label = the still violates the fact = the positive the gate must CATCH.
  true positive  : expected fail, audit said fail   (caught a real error)
  false negative : expected fail, audit said pass    (MISS - dangerous)
  false positive : expected pass, audit said fail    (over-strict)
  true negative  : expected pass, audit said pass

Routes through agent-bridge (no metered API) — run in the background and service
the vision requests from chat.

Usage:  .venv\Scripts\python.exe bible_calibrate.py
"""
from __future__ import annotations

import json
from pathlib import Path

from pipeline import bible_kb
from pipeline.bible_kb import FactCard

ROOT = Path(__file__).resolve().parent
LABELS = ROOT / "bible_kb" / "_calibration" / "labels.json"


def main() -> int:
    data = json.loads(LABELS.read_text(encoding="utf-8"))
    items = data["items"]
    rows = []
    tp = fp = tn = fn = 0
    for it in items:
        facts = [FactCard.from_json(f) for f in it["facts"]]
        bible_kb.hydrate_citations(facts)
        png = ROOT / it["image"]
        audit = bible_kb.verify_biblical_accuracy(
            it["scene_title"], it["subject"], facts, [], png.read_bytes())
        predicted = "skip" if audit.skipped else ("pass" if audit.passed else "fail")
        expected = it["expected"]
        ok = (predicted == expected)
        if expected == "fail" and predicted == "fail":
            tp += 1; tag = "TP (caught)"
        elif expected == "fail" and predicted == "pass":
            fn += 1; tag = "FN *** MISS ***"
        elif expected == "pass" and predicted == "fail":
            fp += 1; tag = "FP (over-strict)"
        elif expected == "pass" and predicted == "pass":
            tn += 1; tag = "TN"
        else:
            tag = f"({predicted})"
        rows.append({"id": it["id"], "expected": expected, "predicted": predicted,
                     "ok": ok, "tag": tag, "notes": audit.notes})
        print(f"  [{'ok ' if ok else 'XX '}] {it['id']:<22} expected={expected:<4} "
              f"predicted={predicted:<5} {tag}")

    prec = tp / (tp + fp) if (tp + fp) else 1.0
    rec = tp / (tp + fn) if (tp + fn) else 1.0
    acc = (tp + tn) / len(items) if items else 0.0
    print(f"\n  confusion: TP={tp} FP={fp} TN={tn} FN={fn}  (FN = dangerous misses)")
    print(f"  precision={prec:.2f}  recall={rec:.2f}  accuracy={acc:.2f}  (n={len(items)})")
    if fn:
        print("  *** the gate MISSED a known-bad image — investigate before trusting it ***")
    out = LABELS.parent / "result.json"
    out.write_text(json.dumps(
        {"tp": tp, "fp": fp, "tn": tn, "fn": fn, "precision": prec, "recall": rec,
         "accuracy": acc, "rows": rows}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  -> {out}")
    # Real regression teeth: a MISS (known-bad image the gate let pass) fails the run.
    return 3 if fn else 0


if __name__ == "__main__":
    raise SystemExit(main())
