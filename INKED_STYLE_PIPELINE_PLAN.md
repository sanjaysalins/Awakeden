# Inked-Style Default Pipeline — Guardrail Plan (v2, post-panel)

**Status:** PROPOSAL, pre-build. The inked graphic-novel style is validated on EW04
(full 60s short). It is approved to replace the Baroque oil-painting look — **but not
until these guardrails exist.** v1 of this plan went to the independent 5-CLI panel;
3/5 ran (gemini + grok died on infra), verdicts **REVISE / REVISE / FAIL**, convergent.
Every load-bearing flag was verified against the code by hand. This v2 corrects them.

## Corrections forced by the panel (all verified in code)

1. **Unify-by-slug was built on a false premise.** `ref_library` cards key by uppercase
   **`name`** (no `slug` field). `bible_kb/` has **only `customs/`** (3 files) +
   `_calibration/` — **zero** character/object/place entities. There is nothing to
   "merge by slug, nothing regenerated"; the truth-half of every entity would be
   **authored from scratch**. Also `bible_kb` is **scene-scoped/per-episode**
   (`enrich_for_scene` reads `<v1>/_bible_check/scene_facts.json`), not a persistent
   per-entity store — a single merged card fights its data model. **→ Unify-by-slug is
   dropped from v1. If we ever couple them, it is cross-reference by a normalized slug,
   never a merged file (a look reroll must not churn a verified-fact record).**

2. **EW04 root cause was mis-diagnosed.** The render scripts DID attach `ref_library`
   anchors via `--image` on every scene, and `BRONZE_SERPENT_STANDARD` already carried
   the "NOT a caduceus" shape-negatives. The caduceus / inaccurate-nails / neck-snake
   defects happened **anyway**. So the gap is **NOT** "no lookup-before-render" (that
   existed). The real gap = **(a) prompt iconography** + **(b) the Vision audit is
   uncalibrated for these motifs and is Baroque-hardcoded**, so it passed them.

3. **"Route through `bible_kb`" does not close the accuracy gap and is oversold.**
   `bible_kb`'s automated half is exactly what FAILED (Vision passed the caduceus). The
   5-CLI panel is recorded as evidence, **not a hard gate** (`bible_kb.py:739`), and the
   gate has escape hatches (`BIBLE_GATE=off`, `.bible_gate_exempt`, grandfather-skip).
   The default shorts/witness path (`visual_runner`, `_hf_animate_short`) never calls it.
   **→ Honest framing: the human Read + a per-motif checklist is the AUTHORITY on these
   subtle morphs; `bible_kb` catches fact-card violations at scale. Neither alone.**

4. **`verify_image` is hardcoded to "17th-century Baroque devotional OIL PAINTING"**
   (`visual_render.py` ~389–415). Shipping inked stills through it would fail good
   frames / pass wrong ones. **Rewriting this rubric for inked is Phase 0 work, not
   optional polish.**

5. **Don't add a 5th reuse bank.** Repo already has `image_library/`, `_hero_library/`
   (`hero_library.py`, topical-fit audit), `clip_library/` (`clip_reuse.py`), plus
   `ref_library/`. `TODO.md` already queues unifying the first two. Guardrail-1 lookup
   and Learning-4 reuse must **wire into the existing banks**, not invent another layer.

6. **Prompt-lint must be card-specific, not a blanket noun ban.** "serpent" is the
   scriptural subject and lives legitimately in cards' negatives. Lint = ban the *bare*
   trigger noun in the **positive subject only**, keep it in negatives / fact text.

## What survives from v1 (low-risk, keep)

- **Guardrail 1** — an authoritative reference index with lookup-before-render + a
  coverage rule. Reframed: anchors already help consistency; the missing piece is
  **enforcement in the production path** + richer grids (¾/profile/expression/costume).
- **Guardrail 3** — SUBTLE/DYNAMIC motion presets. **UNPROVEN** (EW04 talking beats
  already used frozen-tableau wording and the bake-off rated the model "rock-steady").
  Must map onto existing `video_render.motion_prompt()` / `clip_anim_qc.choose_anim_mode()`,
  not duplicate them, and prove on one paid test beat first.
- **Learning 2** — content-hash idempotence for animation (re-animate iff still hash
  changed). Sound; store the source-still hash in the clip sidecar.
- **Learnings 5/6** — assemble to mp3 length; minterpolate long holds (pull into the
  main `assembly_*` path, currently only in the EW04 hand script).

## Revised plan — PHASED, correctness before unification

**Phase 0 — make the audit actually catch EW04's failures (highest value).**
Rewrite `verify_image`'s Baroque rubric for the inked style. Add **deterministic /
calibrated checks for the known failure motifs** (caduceus-vs-serpent-on-a-pole,
nails-through-hands-not-daggers, neck-snake, roped-vs-nailed wrists, cross-in-water
inversion). Extend `bible_kb/_calibration/labels.json` (today: 8 EW01 goat scenarios,
nothing for these motifs) so the audit is proven to discriminate. This is what would
actually have caught EW04 — and it's mostly editing existing tooling.

**Phase 1 — put the inked style on the real production path.**
Add an inked `ImageProvider` (`seedream_v4_5`) + `VideoProvider`
(`cinematic_studio_video_v2`) into `visual_render`/`video_render` + config + the
witness-world skill — so it's not hand scripts. Make `ref_library` lookup authoritative
there (entity extraction → registered card → anchor as `--image`; no card → mint+approve
+register, THEN render). Reuse `hero_library`/`clip_reuse` topical-fit for Learning 4.

**Phase 2 — prove the motion presets.**
One paid SUBTLE test beat (talking head) vs DYNAMIC, mapped onto the existing motion
controls. Keep only if it beats the current wording (test-gate-before-batch).

**Phase 3 — only if 0–2 prove out: connect truth + look, loosely.**
Cross-reference `ref_library` (look) and `bible_kb` (truth) by a **normalized slug +
alias map** (uppercase-name ↔ kebab-slug). Author the from-scratch `bible_kb` entity
cards for the entities we actually reuse. **No merged file.** Decide whether shorts need
a lighter `bible_kb` profile than the long-form derive+panel+audit (cost/cadence).

## Versioning design — `VISUAL_STYLE` master switch (for review, pre-build)

**Principle (user directive, 2026-06-29):** the pipeline does not change. Only *how
we create stills* and *how we animate* changes. Version it so old = `baroque`,
new = `inked`, both selectable; everything else is preserved and reused.

### One switch, one registry
```python
# config.py
VISUAL_STYLE = os.getenv("VISUAL_STYLE", "baroque").strip().lower()   # master switch

STYLE_REGISTRY = {
  "baroque": {                                   # the existing oil-painting way (default)
    "style_base":  VISUAL_STYLE_BASE_BAROQUE,    # current Rubens prompt text
    "style_tail":  VISUAL_STYLE_TAIL_BAROQUE,
    "still_model": ("hf", "nano_banana_2"),      # (provider, model id) — NBP also allowed
    "anim_model":  ("hf", "veo3_1_lite"),
    "audit_rubric":  STYLE_AUDIT_RUBRIC["baroque"],
    "audit_medium":  STYLE_MEDIUM_PHRASE["baroque"],
  },
  "graphic_novel": {                             # the new inked graphic-novel way
    "style_base":  VISUAL_STYLE_BASE_INKED,      # inked linework prompt text
    "style_tail":  VISUAL_STYLE_TAIL_INKED,
    "still_model": ("hf", "seedream_v4_5"),
    "anim_model":  ("hf", "cinematic_studio_video_v2"),
    "audit_rubric":  STYLE_AUDIT_RUBRIC["inked"],
    "audit_medium":  STYLE_MEDIUM_PHRASE["inked"],
  },
}
def style() -> dict: return STYLE_REGISTRY[VISUAL_STYLE]
```

### Exactly what reads the switch (the ONLY code that branches on style)
1. `visual_render.assemble_final_prompt()` → `config.style()["style_base"/"style_tail"]`
   instead of the module-level Baroque constants.
2. The still provider (HFProvider/NBP) → model id from `config.style()["still_model"]`.
3. `video_render` (animation) → model from `config.style()["anim_model"]`
   (+ the SUBTLE/DYNAMIC motion preset, Phase 2, once proven).
4. `visual_render._vision_call` (the audit) → already uses the style rubric ✅; folds
   into the registry for one source of truth.

**Nothing else branches on style.** Scene planning + SP-gates, the `/bible-check`
(bible_kb), assembly, scoring, SFX, captions, the 4 libraries, reviews/locks all run
unchanged — they consume whatever stills/clips the two switched stages produce.

### Provenance (so we always know which version made a file)
Each rendered still writes `style` into its existing audit sidecar; each clip writes
`style` + the model id into its sidecar. A piece may PIN its style in
`pipeline.state.json` so re-runs reproduce regardless of the env default — the
back-catalogue stays `baroque` forever, new pieces default-pin `inked`.

### Back-compat guarantee
`baroque` is the default; with the switch unset, behaviour is byte-identical to today.
Step 3 below is verified by rendering one baroque scene and diffing the final prompt
against the current output before any inked work ships.

### Migration order — each step independently reviewable
1. ✅ Audit made style-aware (`STYLE_AUDIT_RUBRIC` + `_vision_call`). Done; baroque default unchanged.
2. ✅ Iconography-trap auditor (`pipeline/inked_audit.py`) for the EW04 failure motifs. Done.
3. ✅ Added `STYLE_REGISTRY` + `config.style()`/`still_model()`/`anim_model()`/`style_provenance()` + the graphic-novel `style_base`/`style_tail`. No behaviour change at baroque default.
4. ✅ `assemble_final_prompt()` reads `config.style()`. **Verified baroque prompt BYTE-IDENTICAL** (automated assert).
5. ✅ Still provider model = `config.still_model()` (HF_MODEL_ID env still overrides). Baroque → `nano_banana_2` unchanged.
6. ✅ `video_render` model = `config.anim_model()` + registered `cinematic_studio_video_v2` flags/duration. Baroque → `veo3_1_lite` unchanged.
7. ✅ Provenance: every still writes `<stem>.style.json`, every clip writes `<clip>.style.json` ({style, still_model, anim_model}).
   - Verified: `baroque` and `graphic_novel` produce the correct switch values; 89 tests green (bible_kb + still_review + coherence + element_gate + …).
8. ✅ Wired the `/bible-check` GATE into the production animate path (`video_render.animate_scenes`
   calls `bible_kb.gate(v1, stage="animate")` — the same grandfather-safe call the long-form
   animators use). Verified: no-check piece skips, `BIBLE_GATE=off` bypasses, a checked piece
   (EW01) is BLOCKED until green. 56 tests green.
   - NOT auto-running `bib_validate` (the Opus DERIVE+PANEL) inside the hot loop, and NOT yet
     folding `enrich_for_scene()` into the render path — both depend on the open shorts cost/cadence
     decision + the scene-id↔Scene mapping. The gate enforces; the producer stays an explicit step.
9. (Test-gate, pending) Flip ONE piece to `graphic_novel` end-to-end and review before batch.

## Open decisions for the user
- **Unify-by-slug is withdrawn** (it was approved on my false premise). The replacement
  is Phase-3 loose cross-reference. OK to proceed phased, or do you still want a tighter
  coupling?
- **Phase order:** start with Phase 0 (audit correctness — what actually failed), or
  Phase 1 (get the style onto the production path) first?
- **Shorts vs long-form `bible_kb`:** is per-scene derive+panel+audit affordable on a
  14–20-scene short, or do we want a lighter shorts profile?
