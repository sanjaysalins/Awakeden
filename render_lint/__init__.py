"""render_lint — the render-quality loop (KNOW / CHECK / VERIFY / LEARN).

Phase 1 (this): rules.json (KNOW) + lint.py (CHECK, pre-flight before spend).
Later phases: verify.py (VERIFY, post-render Vision audit) + learn.py (LEARN, write new rules back).
"""
from .lint import load_rules, lint, redteam_brief, report  # noqa: F401


def guard_prompt(prompt: str) -> str:
    """Fail-closed pre-flight for a PAID render call (P0-4, 2026-07-08): auto-apply the
    safe positive rewrites (poison-token swaps + negation stripping) so a known-bad
    token never reaches a paid model. lint() only WARNS; this actually fixes."""
    from .autofix import positivize
    fixed, changes, _guidance = positivize(prompt)
    for c in changes:
        print(f"   [autofix {c['rule']}] {c['from']!r} -> {c['to']!r}")
    return fixed


def arm_audit(image) -> None:
    """Arm the fail-closed gate for a freshly rendered image: write a pending-FAIL
    audit sidecar so verify.gate_dir stays RED until a real eyeball/vision PASS is
    recorded. Renders used to write NO sidecar at all — the exact fail-open shape
    that shipped 84 unaudited stills. Never overwrites an existing verdict."""
    from pathlib import Path
    from .verify import audit_status, write_audit
    img = Path(image)
    if audit_status(img) is None:
        write_audit(img, "FAIL", ["pending vision review (auto-armed at render)"],
                    reviewer="render-arm")
