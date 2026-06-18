# Independent review — cursor (OK, 105s)

## Independent adversarial review

### Feasibility vs. the real codebase

**1. The core enforcement mechanism is mostly unbuilt, while the plan treats it as a wiring job.**

Section 7 marks **CLIP-FROZEN / NOMORPH** as “(exists)” with “frame-diff spikes at cuts.” In code, `pipeline/clip_qc.py` only extracts frames and stores a **manual** sidecar via `record_verdict` after “a real look.” There is no automated frame-diff, no morph detector, and no vision pass in that module. The plan’s new **CLIP-ELEMENT-GATE** (“sampled frames' detected object classes must be ⊆ the locked element set”) has **zero** implementation path — no object-class taxonomy, no detector, no tests. This is the plan’s central “teeth,” and it is greenfield R&D dressed as “add frame-sample object-subset check vs manifest.”

**2. Downstream animation does not consume structured contracts today.**

Section 9 says element-gated edit plugs into `image_to_kling` / `.agent_bridge`. But `visual_render.py` already documents the reality:

```482:501:pipeline/visual_render.py
    """Write `<stem>.cut_hint.json` containing the Kling-stage metadata
    (macro_elements, pacing, viral_role). Forward-compatible: the current
    image_to_kling.py doesn't read it, but the V8 Kling subprocess wrapper
    will, and the user can inspect it manually now."""
    ...
            "Advisory metadata for the downstream Kling cut planner. The current "
            "image_to_kling.py reads only the image; V8 wiring will inject these "
            "hints into the cut-plan director prompt."
```

The plan adds a third sidecar (`*.png.manifest.json`) without resolving that **even `cut_hint.json` is unread** by the live Kling path. Step **F** (“build the gallery-tour cut-plan from the LOCKED manifest ONLY”) assumes integration that has been “V8”-queued for months.

**3. Existing `CLIP-IMAGE-GROUNDED` does not do what Section 5 implies.**

Section 5: “The cut-plan is **generated from the locked manifest**, not free macro prose” and “Forbidden: any element not in the manifest.” Today’s gate is prose-marker checking only:

```81:91:pipeline/validators.py
def cutplan_image_grounded(kling_json: dict) -> tuple[bool, str]:
    """CLIP-IMAGE-GROUNDED: prompt must NOT inject rich scene-text nouns, and MUST carry
    the anti-invention clause."""
    ...
    if not any(m in prompt for m in _FROZEN_MARKERS):
        return False, "prompt lacks the anti-invention clause ..."
    return True, "camera-only, image-grounded ..."
```

It does **not** verify that beat descriptions match manifest element IDs. `v2/SPEC.md` even auto-passes `kling-audit` when `gate_cutplan` passes — a shallow check the plan never retires.

**4. Reuse-first claims capabilities the catalogue lacks.**

Section 6: query by “concept + **element-fit** + topical-fit”; “A reused clip **carries its own already-locked manifest**.” Reality:
- `clip_library.find()` ranks **tag overlap**, not element manifests (`clip_library/clip_library.py`).
- `pipeline/clip_reuse.py` scores tags + `preferred`, not manifests.
- Glob search finds **zero** `*.manifest.json` files in the repo.
- Section 6 cites “`clip_library/` **115** clean-reusable” — index currently has **125** clips; `/scene-plan` skill documents only **~34/125** are clean-reusable post-coherence quarantine.

Reused clips today copy audit/coherence sidecars in `materialize()`, not manifests. INV-28 as written is not implementable on the current bank without a backfill step the proof plan omits.

**5. Wrong file paths and artifact naming.**

Section 9: `clip_library.py` at repo root — actual module is `clip_library/clip_library.py`.  
Step **E**: “write `element_manifest.json`” vs Section 3: `visual/<provider>/<stem>.png.manifest.json` vs “Extends the existing `coherence.json` sidecar” — live sidecars are `*.png.coherence.json` (`coherence.py`). Three names for one contract guarantees wiring bugs.

**6. `region` fields have no consumer.**

Manifest JSON includes `"region":"center-left"`, `"upper-center"`, etc. Nothing in this repo maps regions to crop boxes for Kling or ffmpeg. Without bbox computation (vision or manual), regions are decorative prose — the same failure mode Section 0 criticizes.

---

### Hidden risks and false assumptions

**7. Section 0 misdiagnoses the still audit — overstates the gap, understates duplication.**

“The element list is free prose, never verified against the actual render” is only half true. `verify_image()` already runs a six-check Vision audit against `subject_block`, `visible_elements`, and vignettes including period/reverent/anatomy (`visual_render.py` lines 352–408). What’s missing is **per-element ID binding for the gallery tour** and **post-animation subset checking** — not “nothing checks the still.” The plan adds **STILL-RECONCILE**, **PERIOD-REAL**, **IMG-COHERENT**, and manifest `period_real` on top of `verify_image` + `coherence_gate` — triple/quadruple Vision spend on the same still with **contradictory postures** (`coherence_gate.py`: “DEFAULT TO PASS: when in doubt, PASS” vs Section 3: “A still cannot LOCK unless every declared element reconciled `verified:true`” fail-closed).

**8. Assembly rewrite conflicts with live v2 architecture without acknowledging the tradeoff.**

Step **H**: “lay clips in beat-board order, speed-to-fit each beat” — deterministic order replaces semantic jigsaw. But `v2/SPEC.md` line 255 locks `jigsaw (plan_edit)` as **“agent-only (never auto)”** because meaning-level phrase↔clip matching matters. `#03`’s shipped `edit_plan.json` already uses `beat_index` / `beat_phrase` per slot with **non-monotonic scene order** (e.g. scenes 5→7→8→6) because narration meaning overrides strict scene-index order. Forcing beat-board order will produce cuts where the **gallery tour rhythm** (the plan’s stated goal) fights **phrase semantics** — the plan never specifies which wins.

**9. Section 0’s complaint about speed-up is contradicted by Section 6.**

Section 0: “gallery rhythm destroyed by an arbitrary speed-up at jigsaw time.”  
Section 6: “Reuse a finished CLIP loosely … **speed/trim to fit** even though its motion was tuned to other words.” That preserves the exact jigsaw-time speed arbitrariness for ~34 reusable clips, while claiming to fix it for new stills.

**10. Clip-count math hides extreme speed factors.**

Section 2: “12 stills pack a 60s cut … double it and speed up.” For #03 (~54s, 11 beats ≈ 5s each), body slots in the live plan already hit **1.24×–1.30×** on new clips. Reused ~10s Kling clips trimmed to ~4–5s beats routinely need **2×+** — the plan has no AS-G3-style speed-cap guardrail for the new flow, and no ear-review gate for “hypercut” reuse.

**11. Hero semantics are muddy against locked invariants.**

Step **H**: “hero bookend (open on the **hook clip**, CLOSE on the gospel-pivot Christ).” That aligns with current `ASSEMBLY_OPEN_MODE=hook` default, but INV language elsewhere still says “hero bookends open AND close.” Section 2’s “gospel-pivot hero is the **closing** bookend” vs `visual_engine.py` contract still telling the planner hero “bookends the final cut (**open + close**).” Spec drift inside the plan itself.

**12. Rollout stacking before prior gates are enforced.**

Section 7: “All behind `JITB_REQUIRE_*` until shipped shorts carry manifests.” `JITB_REQUIRE_COHERENCE` and `JITB_REQUIRE_STILL_REVIEW` are **still OFF** per `RESUME.md`. Adding INV-25..28 + four new gates before backfilling coherence sidecars on shipped shorts repeats the exact rollout debt the project is already stuck in.

---

### Over-engineering / premature build

**13. Full stack before the risky hypothesis is proven.**

The decisive unknown is whether **Kling will obey manifest-bound crop tours** any better than today’s macro prose. Historical evidence says no — that’s why `clip_qc` exists. The plan proposes: new models (`ElementManifest`), new artifacts (`beat_board.json`), seven gates, four invariants, assembly rewrite, **and** external `image_to_kling` changes — before Step 10 proves one clip passes **CLIP-ELEMENT-GATE** automatically. Minimum viable proof would be: one still → manifest → cut-plan constrained to manifest IDs → render → **automated** frame gate. Everything else is premature.

**14. `beat_board.json` largely duplicates existing timeline-aware planning.**

`discover_scenes` already accepts `timeline`, produces `beat_coverage`, `hero_candidate`, and insert shots for tiny beats (`visual_engine.py`). The plan retires the 14–20 scene pool + SP-G9 mix in favor of scale-to-length 6–20 stills without updating SP-G1..G9, cohesion audit, or `/scene-plan` skill — a cross-cutting spec change bundled into “surgical” Section 9.

---

### Missing steps, edge cases, verification gaps

**15. No backfill/migration strategy.**

125 library clips, existing `scene_plan.json` + `cut_hint.json` sidecars on every shipped short, zero manifests. Proof plan Step 1 says “mostly $0 — agent-mode + existing renders” but never says: retrofit manifests from `macro_elements` + Vision reconcile, or greenfield-only on #03 gaps. Reuse-first (Step **C**) is blocked for the majority of the bank until backfilled.

**16. “No jarring extra” (STILL-RECONCILE) is unoperationalizable.**

Subjective Vision criterion with no schema for “extra object class,” no tie-in to deterministic validators, and a human escape hatch (“human-cut the element”) that bypasses the fail-closed contract the invariants claim to enforce.

**17. Multi-story beats at 1:1 phrase granularity are underspecified.**

Section 2: “~50% multi-story (3–5 sub-vignettes)” + Step **B**: “one beat per narration phrase.” A single narration phrase rarely maps to a unified 3–5 vignette scene. Either phrase count drops (contradicting scale-to-length) or multi-story density collapses.

**18. Proof plan verification is human-only at the end.**

Step 3: “User signs off on #03 (by ear + eye).” No acceptance criteria for CLIP-ELEMENT-GATE pass rate, no fixture in `validation_fixtures/` for manifest-subset violations, and `validators.py` explicitly excludes Vision rules from unit tests. Step 5 flips flags after “green regression” that isn’t defined for the new gates.

**19. Cost claim in Section 10 is false comfort.**

“Building + #03 is **near-$0**” ignores: Vision reconcile per new still (Opus unless agent-mode), Kling re-rolls on CLIP-ELEMENT-GATE failure ($0.65 each), and NBP/HF gap renders quoted correctly but not “near-$0” in aggregate if manifests force re-renders of existing pool stills whose `macro_elements` don’t match reconciled reality.

**20. Section 9 table omits orchestrator / v2 servicer / lock chokepoints.**

Live assembly flows through `v2/servicers/assembly_servicer.py`, `assembly_runner`, and `lock.require_visual_coherence`. None appear in the plug-in table. A plan that skips the actual execution path will ship “implemented” code that never runs in production.

---

### Reuse vs. duplication

**21. Creates parallel artifact stacks instead of extending what exists.**

| Existing | Plan adds |
|---|---|
| `Scene.macro_elements` + `cut_hint.json` | `elements[]` with IDs + regions |
| `scene_plan.json` + `beat_coverage` | `beat_board.json` |
| `*.png.coherence.json` (F1–F5) | `period_real` four-flag block |
| `verify_image` content audit | STILL-RECONCILE |
| `clip_qc` manual criteria | CLIP-ELEMENT-GATE (automated subset) |

A tighter plan would **promote `macro_elements` → locked manifest elements** and wire `cut_hint` consumption in Kling — not introduce a parallel schema while `cut_hint` remains unread.

---

VERDICT: REVISE

TOP FIXES:
1. **Prove the hard part first:** one still → manifest → manifest-only cut-plan → Kling render → **automated** CLIP-ELEMENT-GATE (define object-class schema + implement in `clip_qc` or a new vision runner) before beat boards, INV-25..28, or assembly rewrites.
2. **Reconcile with live tools:** extend `macro_elements`/`cut_hint.json` + wire `image_to_kling` to read them; add deterministic manifest-subset checking to `validators.gate_cutplan`; fix artifact naming (`*.png.manifest.json` vs `element_manifest.json` vs `coherence.json`); correct reuse path to `clip_library/clip_library.py` and honest ~34 clean-reusable count with a manifest backfill step.
3. **Resolve architecture conflicts explicitly:** state whether beat-board order **replaces** semantic jigsaw (and update `v2/SPEC.md` agent-only jigsaw row) or whether beat board is a **prior** that jigsaw still refines; retire duplicate Vision gates (pick `verify_image` OR coherence OR manifest reconcile, not all three); define speed-cap/ear-review for loose reuse so Section 6 doesn’t reintroduce the speed problem Section 0 diagnoses.
