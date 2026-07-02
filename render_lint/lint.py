#!/usr/bin/env python
"""CHECK layer — pre-flight prompt linter. Run BEFORE spending a render credit.

Two passes:
  1. DETERMINISTIC ($0): regex rules from rules.json flag known risks + give the positive fix.
  2. LLM RED-TEAM (agent): `redteam_brief()` produces a structured instruction for the in-chat
     Agent (Anthropic API is dead) to rewrite the prompt best-possible against the 5-axis rubric.

Gate policy = ADVISE + AUTO-FIX, human decides (user rule 2026-07-01): nothing blocks; the
report proposes fixes and a hardened prompt; the human/agent applies them and keeps final say.

  # deterministic report on a prompt:
  .venv\\Scripts\\python.exe -m render_lint.lint --stage still --prompt "…"
  # or from a file:
  .venv\\Scripts\\python.exe -m render_lint.lint --stage still --file prompt.txt

  # in a render driver:
  from render_lint import lint, report
  findings = lint(prompt, stage="still")
  report(prompt, stage="still")            # prints the pre-flight report
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RULES_PATH = HERE / "rules.json"
AXES = ["context", "character", "biblical", "physics", "anti-hallucination", "composition"]
_SEV_ORDER = {"block": 0, "warn": 1, "note": 2}


def load_rules() -> list[dict]:
    return json.loads(RULES_PATH.read_text(encoding="utf-8"))["rules"]


def _stage_match(rule_stage: str, stage: str) -> bool:
    return rule_stage in (stage, "both")


def lint(prompt: str, stage: str = "still", rules: list[dict] | None = None) -> list[dict]:
    """Run the deterministic (regex) rules. Returns findings sorted by severity."""
    rules = rules if rules is not None else load_rules()
    findings = []
    for r in rules:
        if r.get("check") != "regex" or not _stage_match(r.get("stage", "both"), stage):
            continue
        flags = re.I if "i" in (r.get("flags") or "") else 0
        for m in re.finditer(r["pattern"], prompt, flags):
            findings.append({
                "id": r["id"], "axis": r["axis"], "severity": r["severity"],
                "match": m.group(0), "message": r["message"], "fix": r["fix"],
                "provenance": r.get("provenance", ""),
            })
    findings.sort(key=lambda f: (_SEV_ORDER.get(f["severity"], 9), f["axis"]))
    return findings


def llm_rules(stage: str = "still", rules: list[dict] | None = None) -> list[dict]:
    """The check=llm rules the red-team / verify pass should apply for this stage."""
    rules = rules if rules is not None else load_rules()
    return [r for r in rules if r.get("check") == "llm" and _stage_match(r.get("stage", "both"), stage)]


def redteam_brief(prompt: str, stage: str = "still", context: str = "") -> str:
    """Instruction for the in-chat Agent to rewrite the prompt best-possible.
    (Anthropic API is dead → the main agent or a spawned Agent executes this.)"""
    det = lint(prompt, stage)
    llm = llm_rules(stage)
    lines = [
        "You are a render-prompt RED-TEAM. Rewrite the prompt below so the resulting image is the",
        "best we can get FIRST TIME — saving a paid redo. Judge against these 5 axes:",
        "  context-fit · character/world consistency · biblical accuracy · laws of nature (physics/anatomy) · no AI hallucination",
        "",
        f"STAGE: {stage}",
    ]
    if context:
        lines += [f"CONTEXT (the beat this serves): {context}", ""]
    lines += ["PROMPT UNDER REVIEW:", prompt, ""]
    if det:
        lines += ["DETERMINISTIC FLAGS already found (fix each):"]
        for f in det:
            lines.append(f"  - [{f['severity']}] {f['id']} — matched '{f['match']}': {f['fix']}")
        lines.append("")
    if llm:
        lines += ["JUDGEMENT RULES to apply (from what we've learned the hard way):"]
        for r in llm:
            lines.append(f"  - {r['id']}: {r['message']} → {r['fix']}")
        lines.append("")
    lines += [
        "RETURN: (1) a REWRITTEN prompt (positive end-states only, never name what to omit),",
        "(2) a one-line risk note per change, (3) a PASS/REVISE verdict on first-time render quality.",
    ]
    return "\n".join(lines)


def report(prompt: str, stage: str = "still", context: str = "") -> list[dict]:
    """Print a human-readable pre-flight report. Returns the deterministic findings."""
    det = lint(prompt, stage)
    print(f"\n=== render_lint pre-flight ({stage}) ===")
    if not det:
        print("  deterministic: clean (no known-poison tokens)")
    else:
        for f in det:
            print(f"  [{f['severity'].upper():4}] {f['id']}  (matched: '{f['match']}')")
            print(f"         {f['message']}")
            print(f"         FIX: {f['fix']}")
    n_llm = len(llm_rules(stage))
    print(f"  + {n_llm} judgement rule(s) for the LLM red-team (run redteam_brief() via the agent).")
    print("  gate: ADVISORY — apply fixes, human decides. Nothing blocked.")
    return det


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="still", choices=["still", "animation", "both"])
    ap.add_argument("--prompt", default="")
    ap.add_argument("--file", default="")
    ap.add_argument("--context", default="")
    ap.add_argument("--brief", action="store_true", help="print the LLM red-team brief instead of the report")
    a = ap.parse_args()
    prompt = a.prompt or (Path(a.file).read_text(encoding="utf-8") if a.file else sys.stdin.read())
    if a.brief:
        print(redteam_brief(prompt, a.stage, a.context))
    else:
        report(prompt, a.stage, a.context)


if __name__ == "__main__":
    main()
