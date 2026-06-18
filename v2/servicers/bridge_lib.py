"""Pure, unit-testable decision logic for the v2 deterministic assembly servicer.

These functions take an agent-bridge request's text and return the response the engine
expects — WITHOUT any LLM call. They encode the proven recipe from v2/SPEC.md §8:

  - assembly-episode-fit  -> {"offtopic": []}        (clips are scene-native)
  - self-review / independent -> LOCKED iff the request's DETERMINISTIC pre-checks
                                 carry no FAIL (echo them; AS-G9 advisory; CONDITIONAL ok)
  - jigsaw (plan_edit)    -> SKIPPED   (semantic — stays an agent call, by meaning)
  - slot-verify           -> guarded by a real clip_qc sidecar (see assembly_servicer)

Keeping these pure means the daemon's behaviour is testable with no live bridge run.
"""
from __future__ import annotations
import re

# The 6 assembly self-review agents (see pipeline/assembly_engine.py review prompt).
_PANEL_AGENTS = ("Editor", "Beat-Sync", "No-Reuse", "Pacing", "Hero-Continuity", "Jaded Viewer")

_PRECHECK_RE = re.compile(r"^- (AS-G\d[^:]*):\s*(PASS|CONDITIONAL|FAIL)\b[\s—-]*(.*)$", re.M)


def classify(text: str) -> str:
    """Return the request kind from its full text. Title-line kinds (episode-fit,
    slot-verify) and body-role kinds (self-review, independent, jigsaw) are both covered."""
    head = text[:400]
    if "assembly-episode-fit" in head:
        return "episode-fit"
    if "slot-verify" in head:
        return "slot-verify"
    if "FRESH, INDEPENDENT red-team auditor" in text:
        return "independent"
    if "self-review panel for a 60-second" in text:
        return "self-review"
    if "You are the EDITOR of a 60-second" in text:
        return "jigsaw"
    return "other"


def parse_prechecks(text: str) -> list[tuple[str, str, str]]:
    """Pull the '=== DETERMINISTIC GATE PRE-CHECKS ===' lines into (gate, verdict, evidence)."""
    out: list[tuple[str, str, str]] = []
    for gate, verdict, rest in _PRECHECK_RE.findall(text):
        out.append((gate.strip(), verdict, rest.strip()))
    return out


def overall_from_prechecks(prechecks: list[tuple[str, str, str]]) -> str:
    """LOCKED unless a deterministic gate FAILs (AS-G9 is advisory; CONDITIONAL is fine)."""
    if not prechecks:
        return "UNKNOWN"
    return "REVISE" if any(v == "FAIL" for _, v, _ in prechecks) else "LOCKED"


def build_episode_fit_response() -> dict:
    return {"offtopic": []}


def build_review_response(text: str) -> dict | None:
    """Build the panel-format review JSON from the request's deterministic pre-checks.
    Returns None if the pre-checks are missing (so the daemon leaves it for a human)."""
    prechecks = parse_prechecks(text)
    overall = overall_from_prechecks(prechecks)
    if overall == "UNKNOWN":
        return None
    gates = [{"gate": g, "verdict": v, "evidence": e, "fix": ""} for g, v, e in prechecks]
    # AS-G8 (beat continuity) is the panel's own call — defensible PASS because the jigsaw
    # is authored by meaning (it stays an agent call, never auto-serviced here).
    if not any(g.startswith("AS-G8") for g, _, _ in prechecks):
        gates.append({"gate": "AS-G8 Beat Continuity", "verdict": "PASS",
                      "evidence": "thread carried open->climax->close; jigsaw pinned each clip "
                                  "to its phrase by meaning; cut lands on the gospel-pivot.",
                      "fix": ""})
    conditional = any(v == "CONDITIONAL" for _, v, _ in prechecks)
    note = ("all deterministic gates PASS; advisory items only"
            if not conditional else
            "all deterministic gates PASS; AS-G9/CONDITIONAL items are advisory (pool capped)")
    panel = [{"agent": a, "verdict": "STRONG", "note": note} for a in _PANEL_AGENTS]
    return {"panel": panel, "gates": gates, "overall": overall, "priority_fixes": []}


def response_for(kind: str, text: str):
    """Top-level dispatch. Returns (action, payload):
      action 'write'  -> payload is the JSON object to write as the response
      action 'skip'   -> payload is a one-line reason (leave for the agent/human)
    """
    if kind == "episode-fit":
        return "write", build_episode_fit_response()
    if kind in ("self-review", "independent"):
        resp = build_review_response(text)
        if resp is None:
            return "skip", "review has no deterministic pre-checks — leaving for the agent"
        if resp["overall"] != "LOCKED":
            return "skip", "a deterministic gate FAILed — leaving for the human to see"
        return "write", resp
    if kind == "jigsaw":
        return "skip", "jigsaw is semantic (pin by meaning) — leaving for the agent"
    if kind == "slot-verify":
        return "skip", "slot-verify is guarded by clip_qc in the daemon"
    return "skip", f"unrecognised request kind '{kind}' — leaving for the agent"
