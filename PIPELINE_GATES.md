# Still pipeline gates — the standing flow (Layers 1–3)

Built 2026-07-04 after a corpus red-team found 84 flawed stills that had shipped with **0 audit
sidecars**. Root cause: pieces were rendered by bespoke one-off scripts that bypassed the quality
machinery, and the one vision audit that existed (`pipeline/visual_render.py:verify_image`) **fails
OPEN** — it passes a still when the (now-dead) Anthropic API can't check it. A gate that passes when
it can't check is not a gate.

This is the enforced flow for EVERY still, short or long. A piece is not "done" — it may not be
animated or assembled — until its ship gate is GREEN.

## The flow

1. **PROMPT — autofix before spend (Layer 2).** Run the prompt through the positivizer; it applies
   the safe pure-positive rewrites we've learned (candle/lantern → clay oil lamp, dice/dominoes →
   knucklebone astragali, Parthenon/dome/minaret/Gothic → period stone, foreign art-style words
   stripped, negation clauses stripped) and surfaces the risky ones as guidance (drop the word
   "nail", describe only the wound; keep coin faces soft).
   ```
   .venv\Scripts\python.exe -m render_lint.autofix --prompt "…"
   .venv\Scripts\python.exe -m render_lint.lint    --prompt "…"   # + the block/warn flags & guidance
   ```

2. **RENDER through the grounded path, never a bespoke `render_*.py` script.** The one-off
   per-piece renderers (`render_stills.py`, `render_new_stills.py`, `refix_stills.py`,
   `tier1_restills.py`, …) are the thing that shipped 0 audits — do not add more. Ground every
   prompt in `still_specs.json` and render from there.

3. **VERIFY — fail-closed content gate (Layer 1).** After rendering, a vision Agent reads each PNG
   and applies the checklist (19 always-on defect classes + the rule-derived checks), recording a
   PASS/FAIL sidecar. The gate is GREEN only if EVERY production still is PASS; missing or non-PASS
   = BLOCKED.
   ```
   .venv\Scripts\python.exe -m render_lint.verify --worklist <visual_dir>   # the audit batch + checklist
   .venv\Scripts\python.exe -m render_lint.verify --record <png> --verdict PASS|FAIL --flags "note; note"
   .venv\Scripts\python.exe -m render_lint.verify --gate <visual_dir>       # exit 1 until all PASS
   ```

4. **SHIP GATE + shared-still propagation (Layer 3).** One composed check the finishing step runs;
   it also knows which stills are shared across pieces (many are BYTE-IDENTICAL copies — e.g.
   `face_on_cross` and `risen_mercy_hand` are each one file in 9 pieces). Audit a shared still once;
   when you re-render + PASS it, propagate the fixed PNG + its audit to every copy.
   ```
   .venv\Scripts\python.exe ship_gate.py --check <visual_dir>       # composed FAIL-CLOSED gate, exit-coded
   .venv\Scripts\python.exe ship_gate.py --shared                   # cross-piece shared-still map
   .venv\Scripts\python.exe ship_gate.py --propagate <fixed.png>    # push a fixed+PASSed shared still everywhere
   ```

5. **LEARN.** Every new defect class becomes a rule in `render_lint/rules.json` (the KNOW store), so
   it shapes the next prompt (regex lint) and the next audit (it auto-joins the checklist via
   `content_brief`). 44 rules as of 2026-07-04.

## Wired into the finishing skills (done 2026-07-04)
Every finishing skill now opens with a blocking **Step 0 — STILL SHIP GATE** that runs
`ship_gate.py --check` and refuses to proceed on BLOCKED: `/animate`, `/assemble`, `/livingpage`
(gate between still-render and animate), `/animate-long`, `/assemble-long`, `/witness-cut`. A shared
still is audited/fixed once then `--propagate`d. So a BLOCKED piece can no longer be animated or
assembled by the standard flow.

## verify_image fail-open FLIPPED (done 2026-07-04)
`pipeline/visual_render.py:verify_image` used to return `passed=True` when the (dead) Anthropic
vision API couldn't be reached — the fail-OPEN that let 84 stills through. It now returns
`passed=False` with an `AUDIT_SKIPPED_NEEDS_EYE` marker (fail-CLOSED); `render_scene` keeps the
render but does NOT burn a retry on a check it can't run; and the ship gate's `_sidecar_verdict`
now reads the pipeline `passed` schema too, so a NEEDS-EYE (`passed:false`) sidecar correctly BLOCKS.
The real audit then happens via the render_lint vision-Agent gate before ship.

## Still TODO
- Route the shorts through a single grounded renderer and quarantine the bespoke `render_*.py`
  scripts (so no future piece can bypass the gate the way the 11 Cross shorts did).

Memory: `stills-fail-closed-vision-gate`. Related: `feedback-no-lazy-still-prompting`,
`render-quality-loop`, `feedback-api-key-dead-use-inchat`, `global-asset-index`.
