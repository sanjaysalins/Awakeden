# Independent review — cursor (OK, 82s)

## Findings (adversarial, plan vs codebase)

### 1. Goal oversells what Layer 1 actually enforces

The **Goal** claims enforcement of “location/time/place/customs/characters.” **Layer 1** only runs `over_reach_scan` on **colour / number / material** tokens in `specified` claims. The implementation matches that narrow scope (`_HIGH_RISK = _COLOURS | _MATERIALS | set(_NUMBERS)` in `pipeline/bible_kb.py`), not places, people, eras, or customs.

So the plan’s opening promise and Layer 1 are misaligned. A “wrong location” or “wrong character count” error can pass Layer 1 and Layer 3 if the fact sheet never uses a flagged descriptor.

---

### 2. “BAKED-IN, fail-closed … every commit” is not true in practice

**“$0, every commit”** — the standing `/validate` skill runs `pipeline/test_*` modules only; it does **not** include `test_bible_kb.py` or `test_bible_kb_regression.py`. There is no `.github/` CI and no pre-commit hook wiring these 25 tests. “Every commit” is aspirational, not enforced.

**“BAKED-IN, fail-closed”** — `bible_kb.gate()` has **three bypasses** before enforce:
- `BIBLE_GATE=off`
- `<v1>/.bible_gate_exempt`
- **Grandfathering**: “no `_bible_check/` dir and not `strict` → grandfather-skip”

That means almost all existing episodes skip the gate by default. “Fail-closed” applies only to pieces that opt in by creating `_bible_check/`.

---

### 3. Wiring is partial; the expensive holes are *before* animate, not after

The plan says the gate is wired **“BEFORE ANIMATE”** in `_animate_16x9.py` and `_animate_directional.py`. That part exists.

But the **still-render spend path is untouched**:
- `longform/_render_world.py` renders via `visual_render` and writes `.audit.json` from `verify_image()` — **not** `.bib_audit.json` from `bible_kb`.
- `enrich_subject_block()` is never called from any render driver; facts do not automatically drive prompts.
- `bib_validate.py` is a **manual** step between render and animate.

So you can spend on NBP/HF stills, ship PNGs into the tree, and only hit the bible gate at animation. That contradicts “no still that contradicts Scripture gets animated **or shipped**” when “shipped” includes still review / assembly / publish (which the plan itself defers: “assembly/publish gate is a follow-on”).

Also missing from **“Wired in”** entirely:
- Shorts: `_hf_animate_short.py`, `cli_visual.py`, `pipeline/visual_runner.py`
- Gallery / witness still builders
- Any assembly / publish / caption stage

The plan understates how narrow “going-forward only” really is.

---

### 4. Duplicate audit stacks instead of reuse

The repo already has `pipeline/visual_render.verify_image()` (period/anachronism/reverence), used at render time in `_render_world.py`. The bible plan adds a **parallel** stack: `bible_kb.verify_biblical_accuracy()` + `.bib_audit.json`.

Layer 3’s chokepoint checks **only** `.bib_audit.json`, not `.audit.json`. A still can pass the period gate and still have **no** bible sidecar. EW01’s `_render_world` path and `_bible_check` path are disconnected unless someone runs `bib_validate.py` by hand.

That is duplication plus an integration gap, not reuse.

---

### 5. Layer 2 calibration is weak evidence (plan admits part of this, but understates the rest)

The plan’s caveat — **“in agent-mode the same model audits”** — is right but insufficient.

Problems with **“First run: P=1.00 R=1.00 (n=8)”**:
- **n=8** with **4 items reusing the same PNG** and **synthetic inverted facts** (e.g. `one-goat-FAIL` uses the two-goat image with a deliberately wrong “one goat” claim). That measures “does the auditor obey the prompt?” not “does `build_episode_facts` + real fact sheets catch real errors?”
- Labels are **not blind human labels** in a rigorous sense; they are engineered expected outcomes paired with hand-written facts in `labels.json`.
- **End-to-end proof fails on the flagship case**: calibration includes `ark-in-court-FAIL`, but EW01 scene 01’s real `.bib_audit.json` has `"passed": true` while `notes` explicitly flag the ark in the open court as **“OUT-OF-SCOPE … real coverage gap.”** Layer 2 proves the auditor *can* catch ark placement when given that fact; Layer 3 does **not** require that fact in `scene_facts.json`.

So P=R=1.00 is a **sanity check on the audit function**, not proof the pipeline stops bad stills.

---

### 6. Layer 3 trusts artifacts that are forgeable and loosely bound

`check_status()` treats GREEN as: sidecar exists + `"passed": true`. There is:
- No hash tying `.bib_audit.json` to PNG bytes
- No hash tying sidecar to `scene_facts.json` content
- No check that audit was rerun after fact-sheet edits (staleness is **mtime** of `scene_plan.json` vs `scene_facts.json` only)

An operator (or agent) can hand-write `"passed": true` sidecars and pass the gate without rerunning vision audit.

Regression tests also miss **`unverified_specified`** blocking in `check_status` — only over-reach, stale, coverage, and audit pass/fail are covered in `test_bible_kb_regression.py`.

---

### 7. `bib_validate.py` is not fail-closed (undermines Layer 3’s upstream)

The plan positions Layer 3 as the ship/spend chokepoint, but the **driver that produces** `_bible_check/` and `.bib_audit.json` always **`return 0`** even when audits fail (`fails = [...]` is printed; exit code stays 0). Panel subprocess uses `check=False`; panel errors **“(continuing)”**.

So the manual stage that feeds the gate can report FAIL and still succeed at the shell level — easy to miss in agent/automation flows.

---

### 8. Internal contradiction: lock vs animate

The plan says: **“NOT at narration-lock (`cli_witness_lock` locks TEXT before stills exist)”**.

But `bible_gate.py`’s docstring says a piece **“must not LOCK without a green bible-check”** and exposes `--stage lock`. That contradicts the plan and will confuse operators about where enforcement lives.

---

### 9. EW01 POC status is honest but worse than “6/25 covered” implies

The plan says EW01 **“currently blocks (only 6/25 scenes covered).”** `bible_check.status.json` confirms block (`ok: false`).

Finer grain:
- **6 scenes** have derived facts in `scene_facts.json` (ids 1, 2, 3, 7, 8, 9)
- **5 scenes** have `.bib_audit.json` sidecars (01, 02, 03, 07, 09 — **scene 8 has facts but missing audit**)
- **19 rendered scenes** lack facts entirely

Animation is blocked, but **still spend already happened** on the full set via `_render_world`, and scene 01 already has a **passed** bible audit despite a known ark-placement error noted in the audit text — because the fact sheet never encoded that constraint.

---

### 10. Over-engineering before end-to-end proof

The plan builds **three layers**, a policy matrix (`off` / `warn` / `strict` / exempt / grandfather), calibration tooling, panel integration, and a CLI — before:
- Wiring fact derivation or bible audit into `_render_world` / shorts render
- Proving one episode green end-to-end (EW01 is red)
- Adding bible tests to `/validate`
- Gating assembly/publish

That is a lot of machinery for a chokepoint that currently blocks one POC episode at animation only, while grandfathering the rest of the catalog.

---

### 11. Cost / spend justification is partial

Blocking **animation spend** when not green is a good cost lever (~$11/episode Kling/veo). But the plan does not account for:
- Manual `bib_validate` agent/Opus cost to derive facts + panel + per-scene vision audits
- **Un gated still render spend** on episodes that will later fail the gate
- Duplicate vision audits (`verify_image` + `verify_biblical_accuracy`) if both run

Spend control is real at animate; it is not “fail-closed across the pipeline.”

---

### 12. Missing verification steps the plan should name explicitly

Not in the plan but required for the stated goal:
- Wire `test_bible_kb*.py` into `/validate` (and CI if “every commit” is meant literally)
- Gate **still render** (or auto-run `bib_validate --audit-only`) before image spend
- Require **full-scene fact coverage** (`--all-scenes`) before animate, not just `rendered_only` default
- Add regression for `unverified_specified`, sidecar/PNG staleness, and tamper detection
- Resolve **verify_image vs verify_biblical_accuracy** — one audit path or explicit merge
- Assembly/publish gate (acknowledged as follow-on but leaves “shipped” false)
- Coverage checklist for known EW01 gaps (ark placement) so “passed=true + notes flag OUT-OF-SCOPE” cannot happen again

---

VERDICT: REVISE

TOP FIXES:
1. **Align scope and wiring with the Goal** — either expand Layer 1 beyond colour/number/material or narrow the Goal; wire bible check into still render (or block render spend) and add shorts/assembly paths, not only long-form animate.
2. **Make enforcement real, not optional** — add `test_bible_kb*.py` to `/validate`, make `bib_validate.py` exit non-zero on FAIL/skipped audits, and reduce grandfather bypasses (or document that “fail-closed” applies only to `_bible_check` adopters).
3. **Fix the proof chain for Layer 2/3** — calibration must use end-to-end derived facts (not synthetic inverted prompts on the same PNG), require facts for known failures like ark-in-court in EW01, and bind `.bib_audit.json` to image + fact-sheet hashes so GREEN cannot be hand-waved.
