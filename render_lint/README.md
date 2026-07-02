# render_lint — the render-quality loop

Goal (user, 2026-07-01): make every still/animation prompt the best we can FIRST TIME —
right for context, character ref, biblical accuracy, laws of nature, and free of the
hallucinations AI is prone to — so we stop paying for redos. And keep it **always learning**:
every redo teaches the system a new rule.

## The loop (5 layers)

```
1. KNOW    rules.json — one growing rule base, seeded from every memory + past redo
2. BUILD   prompt builders inject the locked ref_library descriptor + write positive end-states
3. CHECK   lint.py — pre-flight BEFORE spend: deterministic regex flags + an LLM red-team brief
4. VERIFY  (Phase 2) verify.py — post-render Vision audit vs the 5-axis rubric; fail → redo
5. LEARN   (Phase 3) learn.py — every redo/fail writes a NEW rule back into rules.json + the ledger
```

Layer 5 feeds layer 1 → the "always learning" part.

## The 5 quality axes (rubric + rule categories)
context-fit · character/world consistency · biblical accuracy · laws of nature (physics/anatomy) · anti-hallucination

## Gate policy
ADVISE + AUTO-FIX, human decides. Nothing blocks a render; the report proposes fixes and a
hardened prompt; the agent/human applies them and keeps final say. (Matches the gate-calibration
rule: gate catches the obvious at scale, the human eye is authority on the subtle.)

## Constraint
The Anthropic API key is dead, so the LLM steps (red-team, Vision verify) run via the in-chat
Agent / local CLIs — i.e. when the agent is in the loop, not fully unattended. The deterministic
regex layer is $0 and always-on.

## Use
```
# pre-flight report on a prompt (deterministic, $0):
.venv\Scripts\python.exe -m render_lint.lint --stage still --prompt "…"
# the LLM red-team brief (hand to an Agent to rewrite the prompt):
.venv\Scripts\python.exe -m render_lint.lint --stage still --brief --prompt "…"

# in a render driver:
from render_lint import lint, report, redteam_brief
report(prompt, stage="still", context="<the beat>")   # print pre-flight
```

## Status
- Phase 1 (KNOW + CHECK): built 2026-07-01, ~22 seed rules, proven on the 5 new
  "Father, forgive them" panels. Reuses `_base_elements_refs.lint_canonical` lessons,
  the memories, `bible_kb`, `ref_library`, `physics_motion_check`.
- Phase 2 (VERIFY) + Phase 3 (LEARN): next. Wire lint into cli_visual + the batch drivers.
- SIGNIFICANT plan → run the external 5-CLI panel before rolling corpus-wide.
