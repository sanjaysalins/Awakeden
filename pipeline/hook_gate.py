"""hook_gate.py - the HOOK + 60s-budget quality gate for a gospel SHORT.

Fills the exact gap the gate-analysis found: data/structures.json DEFINES the Gospel Five-Beat
(hook 0-8s ... 60s total, with word budgets) but NOTHING enforces it - runner._log_conformance()
only LOGS a beat mismatch. The real, recurring failures this catches:
  * shorts OVERRUNNING the 60s budget (Psalm-22 short #2 = 65.0s vs a 59s target; the pilots ran
    69-76s). final_total_seconds is reliable -> this is the highest-value deterministic teeth.
  * a weak / slow / MANUFACTURED hook (the constitution warns the hook must be EARNED, not manufactured).
  * a hook that leads with FEAR or GAIN/LOSS (a binding grace-anchored violation).
  * a landing that does not point to Christ (the CTA-to-Jesus rule).

REUSES (never duplicates): doctrine_gate.scan (fear-pressure / gain-loss / works-selfhelp landmines),
narration_parse (the canonical block parser), and - for --judge - independent_review (free local CLIs).
KJV verbatim + quote-count stay with kjv_strict + lock; this gate does NOT re-check them.

It returns the {ok, blocking, warnings} shape lock.run_lock() consumes, so it can be wired in as an
advisory check beside doctrine_gate. Deterministic halves run with zero cost; --judge is free on the
local CLI subscriptions.

CLI:
  .venv\\Scripts\\python.exe -m pipeline.hook_gate "<folder>"            # report
  .venv\\Scripts\\python.exe -m pipeline.hook_gate "<folder>" --strict   # exit 1 on a blocking finding
  .venv\\Scripts\\python.exe -m pipeline.hook_gate "<folder>" --judge    # + free scroll-test (independent_review)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

from pipeline import narration_parse as NP
from pipeline import doctrine_gate

# landmines that are BINDING in the HOOK specifically (grace-anchored conviction is non-negotiable);
# elsewhere doctrine_gate stays advisory.
HOOK_BLOCKING_LANDMINES = {"fear-pressure", "gain-loss", "works-selfhelp"}

# the constitution's "hook must be EARNED, not MANUFACTURED" - clickbait / fake-urgency tells (WARN).
_MANUFACTURED = [
    (re.compile(r"you\s*won'?t\s+believe", re.I), "you won't believe"),
    (re.compile(r"this\s+(will|could|might)\s+change\s+your\s+life", re.I), "change your life"),
    (re.compile(r"nobody\s+(tells|told|talks)\b", re.I), "nobody tells you"),
    (re.compile(r"\bthe\s+(one\s+)?secret\b", re.I), "the secret"),
    (re.compile(r"\bshocking\b", re.I), "shocking"),
    (re.compile(r"watch\s+(till|until)\s+the\s+end", re.I), "watch till the end"),
    (re.compile(r"you\s+need\s+to\s+(see|hear)\s+this", re.I), "you need to see this"),
    (re.compile(r"\bwarning:\b", re.I), "warning:"),
    (re.compile(r"\b(\d+)\s+things\s+(nobody|no one)\b", re.I), "N things nobody"),
]

# the landing must point to WHO CHRIST IS / come to Him (the CTA-to-Jesus model is a locked invariant).
_CHRIST = ("jesus", "christ", "the cross", "saviour", "savior", "the lord", "come to him",
           "the lamb", "the son", "calvary", "risen", "the gospel")

DEFAULTS = {
    "target_seconds": 59.0,    # Gospel Five-Beat budget (structures.json total_seconds = 60)
    "ceiling_seconds": float(os.getenv("JITB_HOOK_CEILING_S", "66")),  # hard ceiling for a "60s" short
    "hook_max_seconds": float(os.getenv("JITB_HOOK_MAX_S", "12")),     # the hook line should land fast
    "words_min": 110,          # ~60s of narration, low end
    "words_max": 210,          # ~60s of narration, high end (overlong = will not fit)
}


def _first_turn_seconds(meta: dict):
    turns = meta.get("turns") or []
    if not turns:
        return None
    v = turns[0].get("final_seconds")
    return float(v) if v is not None else None


def hook_findings(meta: dict, blocks, cfg: dict = DEFAULTS) -> tuple[list[str], list[str], dict]:
    """PURE gate (test_hook_gate.py fixture-tests this). meta = narration.meta.json dict (may be {}),
    blocks = list of (speaker, text) spoken blocks in order. Returns (blocking, warnings, info)."""
    blocking: list[str] = []
    warnings: list[str] = []

    if not blocks:
        return (["no spoken blocks found (is this a narration folder?)"], [], {})

    # --- DURATION vs the 60s budget (the highest-value, most-reliable check) ---
    dur = float(meta.get("final_total_seconds") or 0) or None
    target = float(meta.get("target_seconds") or cfg["target_seconds"])
    if dur is not None:
        if dur > cfg["ceiling_seconds"]:
            blocking.append(f"short is {dur:.0f}s - over the {cfg['ceiling_seconds']:.0f}s hard ceiling "
                            f"for a 60s short; cut it down")
        elif dur > target + 1.0:
            warnings.append(f"short is {dur:.0f}s vs the {target:.0f}s target - tighten toward 60s")

    # --- HOOK (first spoken block) ---
    hook_text = blocks[0][1]
    t0 = _first_turn_seconds(meta)
    if t0 is not None and t0 > cfg["hook_max_seconds"]:
        warnings.append(f"the hook (first line) runs {t0:.0f}s of audio (> {cfg['hook_max_seconds']:.0f}s) - "
                        f"land the scroll-stop faster; the first ~3s decide the swipe")
    for f in doctrine_gate.scan(hook_text):
        if f["landmine"] in HOOK_BLOCKING_LANDMINES:
            blocking.append(f"hook leads with a grace-anchored violation [{f['landmine']}] "
                            f"\"{f['matched']}\" - the hook must not open on fear / gain-loss / self-effort")
        else:
            warnings.append(f"hook: [{f['landmine']}] \"{f['matched']}\" - {f['note']}")
    for rx, label in _MANUFACTURED:
        if rx.search(hook_text):
            warnings.append(f"hook may be MANUFACTURED ('{label}') - the constitution: the hook is earned "
                            f"by the text, never manufactured/clickbait")

    # --- LANDING (last spoken block) must point to Christ ---
    land_text = blocks[-1][1].lower()
    if not any(m in land_text for m in _CHRIST):
        warnings.append("the landing does not clearly point to Christ - a short must land on WHO CHRIST IS "
                        "/ come to Him (CTA-to-Jesus is a locked invariant)")

    # --- WORD budget (does the script fit 60s of narration?) ---
    words = sum(len(t.split()) for _, t in blocks)
    if words > cfg["words_max"]:
        warnings.append(f"{words} spoken words - likely over 60s; trim to ~{cfg['words_max']}")
    elif words < cfg["words_min"]:
        warnings.append(f"only {words} spoken words - may underfill the 60s budget")

    return blocking, warnings, {"duration_s": dur, "hook_seconds": t0, "words": words,
                                "n_blocks": len(blocks)}


def _load_blocks(folder: Path) -> list[tuple[str, str]]:
    """Prefer the clean tagged file; fall back to narration.md. Returns [(speaker, text), ...]."""
    for name in ("narration-tagged.md", "narration.md"):
        p = folder / name
        if p.exists():
            n = NP.parse(p.read_text(encoding="utf-8"))
            blocks = [(b.speaker, b.text) for b in n.blocks if b.text.strip()]
            if blocks:
                return blocks
    return []


def check(folder: str | Path, form: str = "short", judge: bool = False,
          providers: str | None = None) -> dict:
    """Run the hook gate on a narration folder. Returns {ok, blocking, warnings, info}."""
    folder = Path(folder)
    blocks = _load_blocks(folder)
    meta = {}
    mp = folder / "narration.meta.json"
    if mp.exists():
        try:
            meta = json.loads(mp.read_text(encoding="utf-8"))
        except Exception:
            meta = {}
    cfg = dict(DEFAULTS)
    blocking, warnings, info = hook_findings(meta, blocks, cfg)
    result = {"ok": not blocking, "blocking": blocking, "warnings": warnings, "info": info,
              "folder": str(folder)}
    if judge and blocks:
        result["judge"] = _run_judge(folder, blocks, providers)
    return result


# --- judgment half: a focused scroll-test via the repo's local-CLI reviewers (free) -------------
JUDGE_LENS = """You are a strict SHORT-FORM SCROLL-TEST editor for a KJV gospel-shorts channel
(Awakeden / Salt and Light Kingdom). Judge ONLY the opening HOOK and the closing LANDING of this 60s
short. Score each 0-5:
  hook_stop_power  - would a thumb actually stop in the first 3 seconds?
  hook_earned      - is the hook EARNED by the text (a real, true thing), NOT manufactured/clickbait?
  grace_anchored   - is it free of fear / gain-loss / self-effort pressure (the Holy Spirit convicts)?
  landing_to_christ- does the landing point to WHO CHRIST IS and invite the viewer to Jesus?
Name the single weakest of {hook, landing} and give ONE punchier, KJV-truthful rewrite (no hype, no
invented facts). End with: VERDICT: PASS | REVISE | FAIL."""


def _run_judge(folder: Path, blocks, providers: str | None) -> dict:
    """Reuse independent_review's local CLIs for a free hook scroll-test. Best-effort; advisory."""
    try:
        import independent_review as IR
    except Exception as e:  # pragma: no cover - optional path
        return {"ran": False, "reason": f"independent_review unavailable: {e}"}
    hook = blocks[0][1].strip()
    landing = blocks[-1][1].strip()
    prompt = (f"{JUDGE_LENS}\n\nHOOK (first line):\n{hook}\n\nLANDING (last line):\n{landing}\n")
    names = [p.strip() for p in (providers or "cursor").split(",") if p.strip()]
    outdir = folder / "_hook_review"
    outdir.mkdir(exist_ok=True)
    results = {}
    for nm in names:
        try:
            _, ok, output, secs = IR.run_one(nm, prompt, outdir)
            results[nm] = {"ok": ok, "elapsed_s": round(secs, 1),
                           "output_path": str(outdir / f"{nm}.md")}
            (outdir / f"{nm}.md").write_text(output, encoding="utf-8")
        except Exception as e:  # pragma: no cover
            results[nm] = {"ok": False, "error": str(e)}
    return {"ran": True, "lens": "hook scroll-test", "providers": results,
            "note": "advisory - read the verdicts, reconcile; the gate + human own truth"}


def _print_report(res: dict) -> None:
    info = res.get("info", {})
    print(f"=== hook gate: {Path(res['folder']).name} ===")
    d = info.get("duration_s")
    print(f"  duration: {d:.1f}s" if d else "  duration: (no meta)",
          f"| hook: {info.get('hook_seconds')}s" if info.get("hook_seconds") else "",
          f"| words: {info.get('words')}" if info.get("words") else "")
    for b in res["blocking"]:
        print(f"  BLOCK  {b}")
    for w in res["warnings"]:
        print(f"  warn   {w}")
    if not res["blocking"] and not res["warnings"]:
        print("  OK - hook lands fast + earned, grace-anchored, within the 60s budget, lands on Christ.")
    elif not res["blocking"]:
        print("  PASS (with warnings).")
    if "judge" in res:
        j = res["judge"]
        print(f"  judge: {'ran ('+', '.join(j.get('providers', {}))+')' if j.get('ran') else j.get('reason')}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", help="narration folder, e.g. longform/02_.../v1/shorts/02_The_Mockers_Words")
    ap.add_argument("--form", default="short", choices=["short", "long"])
    ap.add_argument("--strict", action="store_true", help="exit 1 on a blocking finding")
    ap.add_argument("--judge", action="store_true", help="also run the free scroll-test (independent_review)")
    ap.add_argument("--providers", default=None, help="comma list for --judge (default: cursor)")
    a = ap.parse_args(argv)
    folder = Path(a.folder)
    if not folder.exists():
        print(f"ERROR: no folder {folder}"); return 2
    res = check(folder, form=a.form, judge=a.judge, providers=a.providers)
    _print_report(res)
    return 1 if (res["blocking"] and a.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
