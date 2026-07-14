# Independent review — gemini (OK, 56s)

Here is the adversarial review of the CORPUS ROLLOUT PLAN. 

### Findings

**1. Feasibility & Codebase Mismatch (Image Provider)**
* **Citation:** *"de-dup stills ~15 × $0.05 BytePlus"* in the Budget and *"Wave D adds de-dup stills via BytePlus"* in Waves.
* **Finding:** The locked `CLAUDE.md` architecture specifies exactly two providers for Phase B still generation: `HFProvider` (Higgsfield) and `NBPProvider` (Nano Banana Pro / Gemini). There is no "BytePlus" still provider in the pipeline. `CLAUDE.md` only mentions Seedance (ByteDance/BytePlus) as a *video* fallback (`seedance1_5`). If you are assuming the existence of a BytePlus image generator, it is unsupported by the codebase. If you are generating stills via a video model, you are breaking the Phase B → Phase C architecture. This is a critical feasibility failure.

**2. Missing Verification (The Double-Lighting Collision)**
* **Citation:** *"Double-lighting — beats carried by a living-light clip must NOT also carry fx.rays"* versus *"pipeline/rollout_gate.py... motion=smooth · full-bleed ≤60% · ≥3 templates... no dash/ellipsis/mojibake captions."*
* **Finding:** You explicitly name double-lighting as a known risk that will ruin clips, yet you failed to include a check for it in `pipeline/rollout_gate.py`. If the gate is deterministic, it must automatically `FAIL` any beat that has both `animate.living_light` and `fx.rays` applied. Relying on human diligence during a "$0 spec upgrade" across 13 pieces is a single point of failure that violates the engine's gate-driven design.

**3. Cost / Spend & False Assumptions (Margin Math)**
* **Citation:** *"~50% QC-lottery re-roll margin"* and *"Kling QC lottery (~1 in 3 first rolls fails...)"*
* **Finding:** Your math for the safety margin is flawed. If 1 in 3 rolls fails, you have a 33% failure rate. The expected number of rolls to get 1 usable clip is 1 / 0.66 = 1.5. A 50% margin only covers the *mathematical average*, it does not provide an actual "margin" for variance. With hard "per-episode ceilings enforced", a bad run of variance will cause the pipeline to hard-stop mid-batch. A true safety margin for a 33% fail rate should budget for at least 2 rolls per clip (100% margin). 

**4. Hidden Risks (The `mocomic` Migration)**
* **Citation:** *"father_forgive_them needs mocomic→livingpage spec migration first"*
* **Finding:** You have waved off a structural migration as a mere footnote in Wave C. `mocomic` and `livingpage` specs have fundamentally different architectures (comic timing vs. living page anchors/panels). Do you have an automated script to translate this, or does it require a manual rewrite? If manual, it breaks your "repeatable transform" claim. This must be a discrete Phase 0.5 step with its own verification, not a hidden prerequisite swallowed inside Wave C.

VERDICT: REVISE
TOP FIXES:
1. Add a deterministic collision check for `fx.rays` + `living_light` directly to `rollout_gate.py`.
2. Clarify the "BytePlus" still generator discrepancy (use approved HF/NBP or explicitly spec a new provider).
3. Recalculate the budget margin to a minimum of 100% to survive actual Kling QC variance without hitting hard caps.
