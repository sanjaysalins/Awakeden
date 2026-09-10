# Independent review — cursor (OK, 72s)

## Findings

### 1. Feasibility — unproven assumptions about Google Flow’s agent

The plan’s core mechanism is: paste one ~850-line doc into a **Flow agent**, which then runs **18 generations unattended**, labels outputs in-session, attaches them as **Ingredients**, self-QCs every still/clip, and returns a FINAL REPORT.

Nothing in this repo validates that Flow’s agent can do that. The Swirls pipeline here is **OpenArt bridge + `swirls_page.py` / `swirls_cover.py` + `swirls_verify.py`**, or HF CLI — not an automated Flow agent loop. You are betting the whole run on UI/agent behavior that is never specified or smoke-tested.

Specific fragile claims:

- **Section 0, rule 4**: *“Attach exactly the ones named — those images from this conversation, never a file”* — assumes cross-step in-conversation image retrieval by label. If Flow drops context or can’t re-attach prior gens, S4–S7 (two Ingredients) fail silently via the fallback in Section 2.
- **Section 2**: *“If Flow has no such field, keep the label in your own working notes”* — after 18 steps, label↔asset mapping is a single point of failure with no checksum or sidecar files.
- **Section 0**: *“You send me exactly two messages”* — no resume/checkpoint if the session dies at S5; *“split at any `### Step` boundary”* only helps paste size, not mid-run recovery.

### 2. Direct contradiction with the companion brief (and missing ref files)

**Section 0 / header** claims: *“Nothing in this file contradicts”* `GOOGLE_FLOW_BRIEF.md` — **false**.

| Doc | R1/R2 reference step |
|---|---|
| `FLOW_RUN_SHEET` Step R1/R2 | *“Ingredients: none. This reference is made from the text alone.”* |
| `GOOGLE_FLOW_BRIEF` Step 1a/1b | *“Ingredients to attach: `thomas_ref_hd_face.png` + `thomas_ref_hd_full.png`”* and *“`jesus_ref_upscaled3x.png` … already in this folder”* |

Those PNGs **do not exist** in `swirls_pilot_02_my_lord_and_my_god/` (only narration + docs). The brief’s assumption is stale; the run sheet fixed it one way but didn’t update the brief or acknowledge the drift. An operator reading both gets conflicting instructions on the most load-bearing step.

### 3. QC model conflicts with this project’s own verification stack

**Section 3** and every step’s check lists assume the Flow agent can reliably:

- Watch full 8s clips *“from first frame to last frame”*
- Verify *“pixel-for-pixel identical”* baked title text (S1-B, S6-B, S8-B)
- Judge subtle ink-line traits (*“broken, doubled, and tremored”* vs *“one single unbroken confident line”*)

The repo already has tools because eyeball/LLM QC is known unreliable:

- `pipeline/flow_check.py` — deterministic morph/melt pre-filter for clips
- `poc_living_water_ink_style_test/swirls_verify.py` — V0–V3 gates including cover lighting/text locks
- `check_landing_hold.py` — mandatory ≥3.0s post-narration hold (INV-26)

**None appear in the run sheet.** `GOOGLE_FLOW_BRIEF` even documents a **confirmed zero-motion batch** (*“pixel-diffing actual frames”*) and House Style **F0** (motion must lead prompts). The run sheet inherits motion-first wording in individual clip prompts but **drops F0 + Known Traps entirely**, so the agent gets checks without the project’s evidence for why they exist or how to verify motion rigorously.

Project rule: don’t trust pass/fail blindly. This plan trusts the Flow agent for all 18 gens with **one retry each**, then ships the “better of two” and continues (**Section 0 rule 5**). That will propagate known defects the brief already logged: door opening on Front Cover, F05 caption truncating to *“My Lord and”*, zero-motion clips.

### 4. Human gates removed at the worst point

`GOOGLE_FLOW_BRIEF` Step 1: *“Do not start any story shot until both are approved.”*

`FLOW_RUN_SHEET` Section 0: *“without pausing for approval and without asking me anything. I am not watching between steps.”*

If R1/R2 likeness is wrong, **Section 2** locks it: *“REF_THOMAS is never regenerated after this step”* and later still failures cannot fix the root ref. That’s ~16 downstream generations spent on a bad foundation with no stop condition.

### 5. Missing post-Flow steps / stale assembly wiring

The run sheet ends at **Section 6**: user downloads assets. Missing from the plan:

- Assembly per `ASSEMBLY_PLAN.md` (real per-shot targets: F01 ~11.4s, F04 ~**12.8s**, Back Cover ~**11.6s** incl. landing hold)
- **F04** is the *only* shot still needing a **~3–4s freeze-hold** at assembly — not mentioned anywhere in the run sheet (S8’s boomerang ban is documented; F04 extension is not)
- `check_landing_hold.py` run before calling the episode done (`ASSEMBLY_PLAN.md` line 82–83)
- Existing `_assembly_v2/build_cut.py` is **still the old 6-shot v1 delivery** (6 files, wrong durations), not the 8-shot FINAL REPORT filenames (`02_f01_doubt.mp4`, etc.). The plan assumes assembly-ready filenames with no step to update or run the v2 8-shot builder.

### 6. Cross-shot continuity checks vs “carry nothing forward”

**Section 0 rule 2**: *“Carry nothing forward from an earlier step except the images the step names by label.”*

But S3-A checks: *“The oil lamp … reads visibly lower/dimmer **than in STILL_02**”* and S4-A: *“Thomas's outline is UNCHANGED from STILL_02/STILL_03.”*

Those require comparing to prior stills the agent is told not to carry forward. Unless Flow keeps all prior images in context (unlikely by S6), these checks are unenforceable.

### 7. Retry budget vs defect rate — under-specified for spend

| Setting | Value |
|---|---|
| Retry budget | *“1 unchanged regeneration per generation”* (Section 1) |
| On second fail | *“keep the attempt that passes more lines … and continue. Never stop.”* |

For text-heavy stills (SEQ/F01/F05 two-line caption), woodcut title lettering, and motion-heavy clips with contradictory constraints (hand moves **but** gap never closes, door never moves), one retry is far below what this episode’s own history implies. You pay for 18 generations once; the plan accepts shipping partial failures into the zip instead of stopping spend.

### 8. Cost — no justification, no comparison

18 gens (10 stills + 8×8s clips) with zero cost estimate, no Flow credit math, no comparison to the **locked OpenArt path** (~1.4× cheaper than HF, with existing Vision audit in `swirls_verify.py`). Unattended 18-gen Flow run is higher blast radius than the project’s usual **image gate before animate** pattern.

### 9. Over-engineering / duplication

The run sheet is a near-verbatim duplicate of `GOOGLE_FLOW_BRIEF` prompts (~850 lines) while claiming to be *“the same content, restructured.”* Two sources of truth will drift (already have on R1/R2 Ingredients). Safer pattern: generate the run sheet from the brief + `ASSEMBLY_PLAN.md`, or one file with machine-readable steps.

The *“hand this whole file to Flow's agent, once”* framing is ambitious before a **3-generation smoke test** (R1 + one interior still + one clip) proves Ingredients, labeling, and motion QC work at all.

### 10. Style-mix risk on S1 (known hard case)

S1-A attaches **REF_THOMAS** (*ink-wash dev art*) for *“likeness only”* into a **Dürer woodcut** cover. The check only verifies facial traits, not style bleed. `GOOGLE_FLOW_BRIEF` documents cover/interior as *“TWO deliberately different visual styles”* — this is a recurring failure mode, not a solved problem, and woodcut + Ingredients likeness is the hardest combination in the set.

---

VERDICT: REVISE
TOP FIXES:
1. **Prove Flow agent mechanics before the full 18-gen run** — smoke test R1 → S2-A → S2-B for in-session labeling, Ingredient re-attach, and motion verification; add explicit **human stop after R1/R2** before story shots (brief’s own rule).
2. **Wire post-Flow verification and assembly into the plan** — run `swirls_verify` / `flow_check` / `check_landing_hold` on downloads; document F04 ~3–4s freeze-hold and landing hold; align/update `build_cut.py` to the 8-shot FINAL REPORT filenames and `ASSEMBLY_PLAN.md` durations.
3. **Reconcile the R1/R2 contradiction and QC doctrine** — pick text-only refs OR legacy PNG Ingredients (files don’t exist today); import **Known Traps + F0** into the run sheet; replace “agent eyeball + 1 retry + never stop” with fail-closed gates on the defects this episode has already shipped (door motion, caption truncation, zero-motion clips).
