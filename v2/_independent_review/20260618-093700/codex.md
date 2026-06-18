# Independent review — codex (OK, 207s)

**Findings**

- Line 125, “each frame's detected object classes must be ⊆ the locked element set,” and line 195, “CLIP-ELEMENT-GATE,” assume tooling that does not exist. `pipeline/clip_qc.py` only extracts frames and records a manual pass/fail sidecar; it has no detector, no vision call, no object taxonomy, and no subset logic. `validators.py` also says vision-based clip rules are not unit-tested. This is the central gate, and it is greenfield R&D, not a surgical add.

- Lines 160 and 228, “cut-plan is generated from the locked manifest” / “consume the manifest,” are not feasible against the live animation path. The existing sidecar already has macro anchors, but `pipeline/visual_render.py:500` says current `image_to_kling.py` reads only the image and that V8 wiring will inject hints later. Adding `*.png.manifest.json` before wiring even `cut_hint.json` repeats the same unread-sidecar problem.

- Line 173, “`clip_library/` 115 clean-reusable,” is stale and materially overstates reuse. `v2/SPEC.md:215` says reality is only about 34/125 clean-reusable clips. Line 231 also points to `clip_library.py (find)`, but the current spec explicitly says reuse decisions must go through `clip_reuse.py`, not raw `clip_library.find`, because that is where topical/coherence/no-repeat gating lives.

- Line 180, “A reused clip carries its own already-locked manifest,” is false for the current bank. A repo scan found no `*.manifest.json` / `element_manifest.json` files. Reused assets copy audit/coherence/clip-qc sidecars, not element manifests. The proof plan omits the required backfill step.

- Line 21, “The element list is free prose, never verified against the actual render,” overstates the gap. `verify_image()` already audits `subject_block`, `visible_elements`, vignettes, period, reverence, text, and anatomy. The real missing piece is ID-bound crop targets and post-animation checking. As written, the plan adds overlapping STILL-RECONCILE, PERIOD-REAL, IMG-COHERENT, and manifest period flags, increasing Vision spend and conflict risk.

- Lines 55, 94, and 95 use three names for one artifact: `element_manifest.json`, `<stem>.png.manifest.json`, and “existing `coherence.json`.” The actual coherence sidecar is `<stem>.png.coherence.json`. This naming inconsistency is a wiring bug waiting to happen.

- Lines 135 and 225 introduce `beat_board.json`, but the repo already has visual `beat_coverage` and assembly phrase-level beat pinning. `assembly_engine.py` already tells the matcher to pin clips to numbered beats, no reuse, hook open, and hero close. The plan does not say whether beat board replaces the semantic jigsaw or feeds it, which conflicts with `v2/SPEC.md` saying jigsaw stays agent-only.

- Line 230, “Period-real ... existing F1/F3 checks,” is technically wrong. F1 is modern/anachronism and F3 is broken face; they do not cover `grounded_real`, `reverent`, or `baroque_oil` as manifest fields. Also `coherence_gate.py` is deliberately default-pass for clear F1-F5 defects, while line 127 makes locking fail-closed on every declared element. Those postures need reconciliation.

- Line 247, “building + #03 is near-$0,” is not justified. The plan requires new Vision reconciliation, manifest backfill for reuse, possible re-renders, and Kling re-rolls when the new element gate fails. It also says line 158 “HF Kling pro,” while `config.py` and `v2/SPEC.md` make direct-Kling the shorts default because HF is not cheaper and blocks crucifixion.

- Lines 243 and 245, “User signs off on #03” and “green regression,” are not acceptance criteria. There is no defined pass rate, fixture set, manifest-subset validator, object-class schema, or regression command for INV-25. Human ear/eye signoff does not prove the new automated gate works.

VERDICT: REVISE
TOP FIXES:
1. Prove one manifest-only clip path end to end, including an automated element gate, before adding beat boards or new invariants.
2. Wire the live animation path to consume existing `macro_elements`/`cut_hint.json` or a renamed manifest, then add a deterministic cut-plan validator for non-manifest targets.
3. Correct reuse, rollout, and cost assumptions: use `clip_reuse.py`, add a manifest backfill plan, define exact `JITB_REQUIRE_*` flags, and quote #03 spend before rerenders.
