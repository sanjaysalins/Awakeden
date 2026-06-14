# VALIDATION_ENGINE_PLAN.md — rules + regression validation across all stages

**Status:** APPROVED 2026-06-14 (user). Build order: **rules + fixtures FIRST**, then close the bypasses.
**Production hold:** ALL 8 Psalm 22 shorts are ON HOLD until the engine exists, then every short is re-audited through it.

## Context — why this exists

In one session we shipped, then had to redo, a string of defects the pipeline *should* have caught:
modern-looking faces, a horror-tone hand, an NSFW mouth, clips that animated things **not in the
image** (a bleeding toe, "lava" pouring from a lamplit door, a writing hand), a still where "only one
hand is nailed to a cross", garbled titulus text hidden in a still, and — when over-corrected — clips
that lost the viral crop-cut edit and became slow zooms.

**Root cause:** the engine already HAS strong validators, but in agent-mode we ran *shortcut servicers*
(`.agent_bridge/_gen_servicer.py`, `_gen_verify_servicer.py`) that **bypass** them:
- `kling-audit` → auto-passed `{"passed":true}` (the real Stage-A.5 image-fidelity audit was off → invented elements slipped).
- `slot-verify` → auto-passed (the real per-slot Vision + sacred-doctrine check was off).
- cut-plan (`kling-director`) → built from the scene **TEXT** (subject_block), never from the rendered **image** → Kling animated described nouns.

And the *new* checks we add by hand (period/tone) have **no regression fixture**, so the next edit can
silently break them. The visual/clip side has **zero** automated fixtures today (text side has 52 tests).

## Goal

One place that says "what good looks like" (rules), validators that enforce it at each stage with **no
silent bypass**, and a **regression suite** so fixing one thing can't break another — plus a learning
loop so every new defect becomes a rule + fixture automatically.

## Build on what exists (do NOT duplicate)

- Gate data model: `pipeline/models.py` `GateResult`, `AgentVerdict` (reused across stages).
- Deterministic gate pattern: `visual_engine._deterministic_gates`, `assembly_engine._deterministic_gates`,
  `lock.py` (KJV-strict / cluster / doctrine / Rule-8, fail-closed).
- Learning loop: `pipeline/learning.py` + `data/learning/{calibration.jsonl,defect_classes.json}` + `_calibrate.py`.
- Real image-grounded validators that the shortcuts bypass:
  - `PythonProject1/jesus/image_to_kling.py` Stage A (Vision cut-plan FROM the image) + Stage A.5 (`verify_cut_plan` image-fidelity audit).
  - `pipeline/visual_render.py` `verify_image` (6 checks incl. the new period/tone check).
  - `pipeline/assembly_render.py` `verify_cut` / `_verify_slot_vision` (per-slot + sacred doctrine check).
- Test pattern: standalone `pipeline/test_*.py` (run via `python -m pipeline.test_x`); inline fixtures.

## The three pillars

### Pillar 2 (FIRST) — Rules registry: `data/rules.json`
Machine-readable list. One object per rule:
```json
{
  "id": "CLIP-FROZEN",
  "scope": "clip",                     // still | clip | cut | text | audio
  "title": "Frozen tableau — only the camera moves",
  "description": "A clip animates ONLY the camera (crop-cuts/push-in). Nothing in the painting moves, flows, brightens, bleeds, or appears (no invented blood/water/light/lava/motion).",
  "severity": "fail",                  // fail | warn
  "check": "vision",                   // vision | deterministic
  "validator": "validators.clip.frozen",   // where enforced / how tested
  "memory": "feedback-...-...",        // birthing memory slug
  "fixtures": ["clip_lava_13_bad", "clip_hero_14_good"]
}
```
Seeds (grounded in today + existing):
- `IMG-PERIOD`, `IMG-TONE`, `IMG-COHERENT`, `IMG-NOTEXT`, `IMG-ANATOMY`, `IMG-SUBJECT`, `IMG-VIGNETTES` (still)
- `CLIP-FROZEN`, `CLIP-VIRAL` (≥6 crop-cut beats, not a 1–2-beat slow zoom), `CLIP-NOMORPH`, `CLIP-IMAGE-GROUNDED` (cut-plan prompt must NOT inject rich subject_block nouns) (clip)
- `CUT-HERO-CLOSE`, `CUT-NO-REUSE`, `CUT-GOSPEL-FRAME` (cut)
- `TXT-KJV-STRICT`, `TXT-DOCTRINE-*`, `TXT-CLUSTER`, `TXT-RULE8` (text — already enforced; registry just points to them)

### Pillar 3 (FIRST) — Regression fixtures + runner
- `validation/fixtures/` — labeled samples + a `manifest.json` mapping each fixture → {rule_id, expect: pass|fail, asset path/notes}. Capture today's misses:
  - `still_modern_crowd_07-06_v1` → IMG-PERIOD = FAIL
  - `still_garbled_titulus_07-01` → IMG-NOTEXT = FAIL
  - `still_velazquez_hero` → all still rules = PASS
  - `clip_lava_13_textplan` (the old text-based cut-plan output) → CLIP-FROZEN = FAIL
  - `cutplan_slowzoom` (single-push-in json) → CLIP-VIRAL = FAIL
  - `cutplan_richtext` (old build_cutplan output w/ subject_block) → CLIP-IMAGE-GROUNDED = FAIL
  - `cutplan_cropcut_clean` (new build_cutplan output) → CLIP-VIRAL = PASS, CLIP-IMAGE-GROUNDED = PASS
- **Deterministic validators** (`pipeline/validators/…` or `validation/…`) — pure code, unit-tested every change ($0):
  - `cutplan_shape(kling_json)` → checks ≥6 crop-cut beats (viral) AND prompt has the anti-invention clause AND prompt does NOT contain rich-scene nouns (blood/lamplight/first light/pen…). Catches BOTH the slow-zoom regression and the hallucination-seeding text.
  - `prompt_has_criteria()` → asserts `verify_image`'s role string still contains the period/tone + banned-text + anatomy checks (catches accidental removal).
  - `banned_tokens(text)` → reuse config.VISUAL_BANNED_TOKENS.
  - `rules_integrity()` → every rule has a validator + memory; every referenced fixture exists.
- `pipeline/test_validation.py` — runs the above against fixtures; asserts verdicts match labels.
- **Vision calibration runner** (on-demand, small cost; like `_calibrate.py`): feeds the image/clip fixtures through the *real* Vision validators and asserts the verdict matches the label. Not every-commit (non-deterministic + costs); run after changing a Vision prompt.

### Pillar 1 (SECOND) — Close the bypasses
- Retire / replace the auto-pass servicers. Options:
  - (a) For clips: run the REAL `image_to_kling` Stage A (image-grounded cut-plan) + Stage A.5 audit instead of the text-template servicer; keep the viral crop-cut discipline in `SKILL_locked.md`.
  - (b) If keeping a servicer, it MUST look at the rendered image and apply the rule criteria — never blanket `{"passed":true}`.
- `assembly` slot-verify + episode-fit: stop auto-passing; require a real per-frame check (sacred frames fail-closed, already in `assembly_render`).
- Add a deterministic backstop: before Kling submit, `cutplan_shape()` must pass (viral + image-grounded); a clip whose source still failed an IMG-* rule cannot animate.

### Learning loop (extends existing)
- Add `scope` + `rule_id` to `calibration.jsonl` records for visual/clip defects; `_calibrate.py` proposes a new rule + fixture when a defect recurs. Each new memory → rule in `rules.json` → fixture in the manifest.

## Verification
- `python -m pipeline.test_validation` (new) + existing `python -m pipeline.test_{kjv_strict,cluster_gate,doctrine_gate,lock}` all green.
- `cutplan_shape` fixtures: slow-zoom FAILS, rich-text FAILS, new crop-cut PASSES.
- On-demand: vision calibration run over the still/clip fixtures → verdicts match labels.
- Then: re-audit #01–#08 (stills + clips) through the validators; fix any flagged before shipping.

## Files (new vs. touch)
- NEW: `data/rules.json`, `validation/fixtures/manifest.json` (+ small sample assets), `pipeline/validators.py` (or `validation/validators.py`), `pipeline/test_validation.py`, on-demand `validate_fixtures.py`.
- TOUCH: `.agent_bridge/_gen_servicer.py` + `_gen_verify_servicer.py` (retire auto-pass), `pipeline/visual_handoff.py` (gate on cutplan_shape), `pipeline/learning.py` + `data/learning/defect_classes.json` (scope/rule_id), `config.py` (register rules path).
- Memories: link each rule to its birthing memory; new defects spawn new memories.
