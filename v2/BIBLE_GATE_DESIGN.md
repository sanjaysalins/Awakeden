# Bible-check enforcement + regression — design (for panel review)

Goal: make the biblical-accuracy check (location/time/place/customs/characters)
a BAKED-IN, fail-closed part of the pipeline, with regression that proves it
still has teeth, so no still that contradicts Scripture gets animated or shipped.

## Three layers

### Layer 1 — deterministic teeth ($0, every commit, no LLM)
`pipeline/bible_kb.over_reach_scan(facts)`: a SPECIFIED claim that names a
COLOUR / NUMBER / MATERIAL absent from its cited (fetched) KJV is flagged —
e.g. "white linen" vs KJV "holy linen". Negation-aware ("not plain white" is a
guard, not a claim). Plus the existing citation-hydration downgrade (an
unverifiable `specified` fact auto-drops). Golden fixtures in
`test_bible_kb_regression.py` (known-bad MUST flag, known-good MUST pass) — 25
tests; if anyone blinds the check, they go red.

### Layer 2 — image-audit calibration (occasional, agent-mode)
`bible_kb/_calibration/labels.json` (real EW01 stills paired with a fact + a
blind human pass/fail) + `bible_calibrate.py` → confusion matrix +
precision/recall vs the labels. Seeded with 8 (incl. ark-in-court FAIL,
one-goat-vs-two FAIL). First run: P=1.00 R=1.00 (n=8). Caveat: in agent-mode the
same model audits, so this is a sanity signal until a different vision model runs
it; it is a real regression when expanded / run cross-model.

### Layer 3 — fail-closed chokepoint (ship/spend time)
`bible_kb.check_status(v1)` → GREEN only if: scene_facts current (scene_plan not
newer), every rendered still has a SceneFacts entry + a `.bib_audit.json`
passed=true, no unverified `specified` fact, over_reach clean. Writes
`bible_check.status.json`. `bible_kb.gate(v1, stage)` wraps it with policy:
- `BIBLE_GATE=off` → skip · `<v1>/.bible_gate_exempt` → skip · no `_bible_check/`
  dir and not `strict` → grandfather-skip · else enforce (raise) · `warn` → warn
  only · `strict` → enforce even without the dir.
`bible_gate.py` is the CLI (exit 3 = not green).

## Wired in (going-forward only)
- BEFORE ANIMATE: `longform/_animate_16x9.py` + `_animate_directional.py` call
  `bible_kb.gate(ep.v1, "animate")` before any veo3/Kling spend.
- NOT at narration-lock (`cli_witness_lock` locks TEXT before stills exist);
  the gate belongs at the visual spend/ship stages.
- Grandfathering: existing episodes (no `_bible_check/`) are skipped; EW01 (which
  adopted the stage) is enforced and currently blocks (only 6/25 scenes covered).

## Panel review (2026-06-29) — codex FAIL + cursor/claude REVISE → fixes applied
The 5-CLI panel reviewed this design and was RIGHT to fail it. Real holes found + fixed:
- **Forgeable / stale sidecars (the killer).** `.bib_audit.json` wasn't bound to the
  PNG or the facts, and staleness used fragile mtime. FIXED: scene_facts now carries
  `scene_plan_sha256`; each sidecar carries `image_sha256` + `facts_sha256`;
  `check_status` recomputes + compares → `stale`/`stale_audit` reasons. Proof: EW01
  scene 1's old `passed:true` sidecar (audited before the ark fact existed) is now
  detected stale; re-audited → it FAILS (ark in open court). Re-audit also caught
  scene 3 (hanging lamps vs the lampstand fact). Two real errors caught end-to-end.
- **Driver wasn't fail-closed at the shell.** FIXED: `bib_validate.py` exits 3 on any
  failed/skipped audit; `bible_calibrate.py` exits 3 on any false-negative (miss).
- **Tests not in /validate.** FIXED: `/validate` now runs the 29 bible tests
  (7 logic + 22 regression — earlier "25" was wrong).
- **`--all-scenes` was weaker, not stronger.** FIXED: it now requires every PLANNED
  scene covered + audited (strict superset).
- **Over-claim corrected:** the deterministic over_reach_scan only catches
  colour/number/material over-reach — NOT the project's main error class (an actor
  over-claiming an act Scripture assigns to another). The BINDING bar is: verified
  citations + coverage + per-scene image-audit passed + hash-current + over_reach
  clean. The colour/number/material scan is a cheap ADD, not the whole teeth.
- **Calibration P=1.00/R=1.00 (n=8) is a SANITY signal, not evidence** (same model
  audits in agent-mode; synthetic inverted facts). It is a real regression only when
  run cross-model / expanded.

## Known limits (honest, still open)
- Coverage is per-rendered-scene; a piece is only as checked as its fact sheet is
  complete (EW01 POC = 6 scenes).
- Layer 2 independence is weak in agent-mode (same model).
- The facts PANEL verdict oscillates (adversarial) — it is recorded as evidence,
  NOT a hard gate; the deterministic set + verified citations are the binding bar.
- Ship-time net currently = before-animate; assembly/publish gate is a follow-on.
