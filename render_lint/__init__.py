"""render_lint — the render-quality loop (KNOW / CHECK / VERIFY / LEARN).

Phase 1 (this): rules.json (KNOW) + lint.py (CHECK, pre-flight before spend).
Later phases: verify.py (VERIFY, post-render Vision audit) + learn.py (LEARN, write new rules back).
"""
from .lint import load_rules, lint, redteam_brief, report  # noqa: F401
