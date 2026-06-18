# COHERENCE GATE SPEC — body-plausibility verification + asset cleanup

> # ⚠️ SUPERSEDED (2026-06-17) — DO NOT treat as a live contract.
> The durable rules are folded into **`v2/SPEC.md`** (INV-23/24, the IMG-COHERENT + STILL-REVIEW
> gate rows, the clip_reuse/dedup manifest). **`v2/SPEC.md` is the single source of truth.**
> This file is kept as the build LOG of how the gate came to be. Several parts are
> **history-overtaken — do NOT carry them forward:**
> - the **C1–C7 "when unsure FAIL" 3-pass** design (calibration replaced it with a blind,
>   **default-PASS F1–F5** single look — precision 0.08 → 0.50);
> - the **"$110 rebuild"** plan (the user chose **quarantine + prevent**, not paid rebuild);
> - the **§4 build order** (done) and the "head-count seatbelt as built" (deferred).
> The lesson lives in memory `feedback-gate-calibration-human-authority`.

> **Status (historical):** REVISED after red-team round 1 (3 hostile reviewers, all REVISE; findings
> verified against code). Authored 2026-06-17. Addresses a recurring defect class:
> stills that are anatomically/physically *impossible* (floating head on the cross,
> giant head + tiny body, a figure standing on the floor with one hand nailed).
> Two halves: **A) build the gate** (stop new bad stills), **B) clean the past**
> (reject + rebuild + reassemble + a clean reusable-asset index).
>
> Binds to the v2 contract (`v2/SPEC.md`) and the fail-closed validation engine
> (`data/rules.json` + `pipeline/validators.py` + the lock chokepoint pattern).
> This spec is itself a SIGNIFICANT plan → runs the external panel before "done"
> (panel-doctor `--smoke` FIRST; the panel is degraded — see §7).

---

## 1. The defect class (what we are catching)

**Name:** `IMG-COHERENT` — *whole-figure physical plausibility* ("human conditions
and natural human order"). Distinct from `IMG-ANATOMY`, which checks the **parts**
(finger counts, fused fingers, extra arm). `IMG-COHERENT` checks the **whole** and
the figure's relationship to the world:

| # | Sub-check | FAIL example |
|---|---|---|
| C1 | **Assembly** — head joined to neck to torso; limbs at correct joints; one head per body; no detached/floating part | floating head of Jesus on the cross |
| C2 | **Proportion** — head-to-body ratio human (~1:7–8 adult); no giant-head/tiny-body; limb lengths plausible | massive head, small body hiding behind |
| C3 | **Pose physics** — pose achievable by a real body; weight/support consistent | standing on the floor with one hand nailed |
| C4 | **World contact** — standing figures touch ground; seated have a surface; a crucified figure hangs ON the cross with BOTH attachment points; no figure floating in space | one hand nailed, body not on the cross |
| C5 | **Count + connectivity** — sane head/limb/person count; no duplicate central subject; **no two figures sharing/merged at a limb; no duplicated part** | duplicate central Christ; merged figures |
| C6 | **World-interpenetration** — no limb/body passes THROUGH a solid object (cross beam, pillar, another body) | arm through the cross beam |
| C7 | **Light coherence** — one consistent light direction across each figure (a "lit from left face on a right-lit body" = assembled-from-parts tell) | face lit left, torso shadowed as if lit right |

**Root cause of the misses (today's `verify_image`):**
1. Check 5 audits **parts** (fingers/limbs), never the **gestalt** (assembly/proportion/pose/contact/interpenetration/light).
2. `IMG-COHERENT` is already a row in `data/rules.json` but its validator field reads
   *"candidate new explicit check"* — **it was never implemented.** A rule with no teeth.
3. It is **one** Vision call, one shot, with "minor nits are not failures" — a single
   model waves a floating head through as "looks fine" (it already misses fingers it is
   explicitly told to count: `visual_render.py:372-381`).

---

## 2. Half A — the gate (stop new bad stills)

Honest constraint: this is mostly a **vision** check (pose estimators are unreliable on
painterly Baroque and crucifixion poses). But a single structured LLM pass *confabulates
confident `true`s* on Baroque art — so the design is **heterogeneous + adversarial +
fail-closed**, with one cheap deterministic seatbelt.

### A1. Three HETEROGENEOUS passes (not three identical ones)
The red-team killed the original "3 identical auditors" — in agent-mode that is one agent
answering the same prompt thrice (no real independence) and the SAME agent that authored
the `subject_block` (author/auditor circularity). Replace with three *materially different*
passes:

- **Pass 1 — BLIND caption (spec WITHHELD).** "Describe the body of the central figure,
  joint by joint, as if to a sculptor." The auditor does NOT see the subject_block, so it
  cannot confirm the expected anatomy from a prior. A deterministic post-check then asserts
  the caption describes a single attached head + a plausibly-proportioned body.
- **Pass 2 — adversarial localization.** "Point to the single most physically impossible
  region of any body (quadrant/bbox) and explain. If none, say NONE." Forces a *search for
  the anomaly* rather than rubber-stamping a checklist.
- **Pass 3 — the C1–C7 structured schema** (below), spec-aware.

At least Pass 1 is blind-of-spec; where possible route ONE pass to a genuinely different
verifier (real-API Claude or a CLI-panel reviewer) so a rebuilt still is not certified by
the same agent that just rewrote its prompt.

**Deterministic seatbelt ($0):** a face/head detector flags >1 head or a head region with
no body-mask continuity below it. Imperfect on Baroque, but it catches the *literal
floating-head / multi-head* case the LLM keeps waving through, and it is free.

### A2. Structured schema (Pass 3)
Per visible figure, explicit boolean + evidence (forced via StructuredOutput — no vibes):
```json
{"figures":[{"who":"central|figure-2|...",
  "c1_assembly_ok":true|false,"c1_evidence":"...",
  "c2_proportion_ok":true|false,"c2_evidence":"...",
  "c3_pose_ok":true|false,"c3_evidence":"...",
  "c4_world_contact_ok":true|false,"c4_evidence":"...",
  "c5_count_connectivity_ok":true|false,"c5_evidence":"...",
  "c6_interpenetration_ok":true|false,"c6_evidence":"...",
  "c7_light_ok":true|false,"c7_evidence":"..."}],
 "passed":true|false,"fail_reasons":["<C# + which figure>"]}
```
Background figures dissolved into shadow get latitude on C2/C4/C7 (note, don't fail).

### A3. Convergence — fail-closed to REVIEW, not to re-spend
"Any 1 of 3 fails → auto-reject + re-render" has an unmeasured false-reject rate and would
burn money re-rendering clean foreshortened/shadow Baroque heroes. Instead:
- **≥2 of 3 passes fail → auto-REJECT.**
- **exactly 1 fails (incl. the seatbelt) → HUMAN-REVIEW queue** (no auto-spend).
- The human reject-list gate (B2 → §4 step 5) is where a flagged still is confirmed before
  any rebuild. Fail-closed to a *cheap human look*, not to a *paid re-render*.

### A4. Fail-closed sidecar (with the holes the red-team found, closed)
A still is **coherence-verified** only when a passing `<stem>.png.coherence.json` exists:
```json
{"audited":true|false,"passed":true|false,"png_sha256":"<hash>",
 "passes":{"blind":..,"localize":..,"schema":..},"fail_reasons":[...]}
```
- **`audited` is separate from `passed`.** The usage-cap escape hatch in `verify_image`
  (`visual_render.py:457-464`) returns `passed=True` when the Anthropic cap hits — a green
  light for an UN-audited image. Coherence MUST write `audited=false` on any skip →
  UNVERIFIED → blocked. INV-23 requires `audited=true AND passed=true`.
- **`png_sha256` binds the verdict to the exact image.** A silent in-place re-render leaves
  a stale sidecar; the chokepoint recomputes the hash and treats a mismatch as UNVERIFIED.
- On rebuild, DELETE all sidecars for the stem (`.png.audit.json`, `.clipqc.json`,
  `.coherence.json`) and add `.coherence.json` to the orchestrator reroll-cleanup
  (`orchestrator.py:182` suffix list).

### A5. ENFORCEMENT at a chokepoint nobody can skip (the load-bearing fix)
The red-team confirmed the original plan would make coherence an **orphan check** — exactly
the bypass the validation engine exists to kill. Verified: `assembly_runner.py:120` calls
only `_lock.require_lock` (text-only — KJV/parity/cluster/narrative-presence, no image
check), then `load_clips` at `:148` with no gate. So:
- Add a fail-closed **`visual_lock`** (or extend `lock.run_lock`) that `assembly_runner`
  calls **before `load_clips`**, raising `PermissionError` on any selected still/clip
  lacking a passing `*.coherence.json` (+ the clip's `*.clipqc.json`).
- **Close ALL THREE auto-bless doors** (each fabricates `passed=True` without a look):
  `clip_library.materialize()` (`clip_library.py:62-65`), `_build_zech_reuse.py:108-110`,
  and `assembly_servicer._clips_all_qcd`/`:80-82` (must require the coherence sidecar too,
  not just `clip_qc`). 
- **INV-24 is a PATTERN, not one function:** no copy/reuse/servicer path may fabricate a
  verdict — it copies a real sidecar from the source or marks UNVERIFIED.

### A6. Registry + regression + CALIBRATION (prove it works before trusting it)
- Implement the `IMG-COHERENT` validator (fan-out runner + schema) and update its
  `data/rules.json` pointer (drop "candidate"). Add new rules `IMG-INTERPENETRATION`/
  `IMG-LIGHT` or fold C6/C7 under `IMG-COHERENT`.
- The 3 stills B2 surfaces (floating head / giant head / one-hand-nailed) become permanent
  `*_bad` fixtures under `pipeline/validation_fixtures/` **and entries in
  `manifest.json`** (so `rules_integrity` covers them). Add **≥3–5 `*_good`** including a
  *foreshortened* and a *shadow-dissolved* shipped hero (not just one frontal Velázquez).
- **CALIBRATION GATE (per `feedback-test-gate-before-batch`):** before B2 runs on the full
  pool, run the gate on the fixtures — it MUST reject all known-bad AND pass the known-good
  with a measured **false-reject rate under a set threshold (e.g. ≤10%)**. Only then proceed.

**Half-A cost:** ~$0 to author. Re-running the gate over an image = 3 passes; $0 in
agent-mode (hand-serviced / Workflow agents); ~3 Haiku Vision calls/image if `LLM_PROVIDER=api`.

---

## 3. Half B — clean the past (reject → rebuild → reassemble → clean index)

Per the user decision: **audit first (free), then quote the rebuild; spend nothing until approved.**

### B1. Inventory (free) — find-driven, not hand-listed
Sweep ALL of disk (the red-team caught omissions + a double-count):
- `longform/**/visual/nbp/*.png|*.mp4` — **including `longform/01_Isaiah_53_*`** (≈108 PNG /
  155 MP4), which the first draft omitted.
- `v2/pilot/**` (≈71 PNG / 84 MP4).
- `image_library/` (≈21 PNG); the hero `_library/` at **repo root** `./_library/{plates,stills}` (≈13 PNG).
- `clip_library/index.json` is **a VIEW** (136 entries, each a `source` pointer into the
  shorts folders) — dereference it, do NOT count it as a separate pool.
Output: `v2/coherence_audit/inventory.json` (path, kind, sha256, which short/cut uses it).

### B2. Re-audit through the new gate (free in agent-mode)
Run the Half-A fan-out over every still. **Cost honesty:** $0 ONLY in agent-mode — and the
real cost is the **human-servicing toil** (~3 bridge services × N stills; I hand-serviced
~42 audits in one session and that toil is the whole reason for the fan-out Workflow). In
`LLM_PROVIDER=api` it is ~3 Haiku Vision calls × N (a visible $ number). Clips inherit a
still's *rejection*; a clip on a *passing* still still owes its own `clip_qc` look (Kling
introduces morph/melt defects a clean still doesn't have). Output:
`v2/coherence_audit/reject_list.json` (each reject: failed C-code + evidence + downstream
clips + which finished cuts used it) + a full-res `index.html` review page. Capture the 3
canonical failures here as the A6 fixtures.

### B3. Quarantine + de-index (free)
Move rejects to `_rejected_coherence/` (DO NOT delete — evidence + fixtures); leave a
pointer. Rebuild `clip_library/index.json` by **MERGING** (preserve the 13 hand-marked
`preferred` + the 8 reclassified `scope` edits — a naive regenerate loses that curation),
excluding rejects.

### B4. Rebuild (METERED — realistic quote + hard caps)
Per rejected still:
1. Edit `scene_plan.json` `subject_block` to make pose + contact explicit.
2. Re-render → must pass the new (stricter) gate.
3. Re-animate the clip → must pass `clip_qc`.
**The red-team's central risk:** the SAME model that drew the impossible body re-draws it;
reword-and-retry is not a guaranteed fix for a gestalt failure. So B4 has a **bounded
fallback ladder** with a **hard per-asset attempt cap of 3**:
  reword → switch provider (HF↔NBP) → re-crop the impossible region out of frame →
  **EXCLUDE the scene from the cut** (the existing curation lever, as with writing scenes).
No infinite re-render loop; a still that fails 3× goes to a manual list, not more spend.
**Realistic cost (NOT the single-attempt floor):** `per-asset × expected-attempts × N`.
Using the project's own re-roll history (~2.5 render attempts/still, ~1.6/clip) and a
36–48-reject estimate: stills ≈ 48 × 2.5 × $0.50 ≈ **$60**; clips ≈ 48 × 1.6 × $0.65 ≈
**$50**; **worst-case ≈ $110** (vs the first draft's implied ~$55). The user gate (§4)
shows this range + the attempt multiplier; B4 re-prompts if actual spend exceeds the
approved ceiling.

### B5. Reassemble (mostly free) — explicit provenance
For every finished cut that used a rejected clip: the join is
`edit_plan.json` → `plan.slots[].scene_index` (+ `selected_scene_indices`) → scene index →
`<NN>_<slug>.png`. Re-run `/assemble --replan --rebuild` with the rebuilt clip → `/sfx` →
`/caption`. Back up **each** finished variant (`viral_cut`, `_sfx`, `_sfx_captioned`,
`_sfx_music_captioned`) as `<name>_PRE_COHERENCE.mp4` — not one collapsed backup name.

### B6. Clean index (free) — reusable = coherent AND neutral AND clip-clean
"Reusable" is not coherence alone — the topical-fit rule (`clip_library.py:35`,
`feedback-topical-fit-gate`) governs it. Final index entry is reusable only if:
`coherence_verified:true` (still) **AND** `clip_qc passed:true` (clip motion) **AND** a
valid `scope` (neutral = cross-episode-safe; specific = same-subject only). Re-classify
every rebuilt asset's `scope`/`preferred`. Store `png_sha256` so a later silent swap busts it.

---

## 4. Build order (everything up to step 5 is $0)

1. **A4 sidecar + A5 enforcement + INV-24 door-closing + A6 registry/fixtures/manifest** (deterministic scaffolding, tests).
2. **A1–A3 heterogeneous fan-out gate** (Workflow) + the deterministic head-count seatbelt.
3. **A6 CALIBRATION** — run on known-bad (must reject all) + known-good (false-reject ≤ threshold). **Do not proceed if it fails calibration.**
4. **B1 + B2 inventory + re-audit** — $0 (agent-mode) → reject list + review page + fixtures.
5. **→ USER GATE:** review rejects + approve the realistic rebuild quote (range, not the floor).
6. **B3 quarantine + de-index** → **B4 rebuild** (metered, capped) → **B5 reassemble** → **B6 clean index**.
7. **Panel:** `panel_doctor.py --smoke` FIRST; if degraded (grok flaky / codex garbled per
   `panel-doctor`), repair or honestly down-scope to "3-CLI degraded" — don't claim a 5-CLI
   review that didn't happen. Then panel this spec + the gate before "done".

## 5. Invariants (candidate INV-23/24 for v2/SPEC.md)

- **INV-23 (coherence):** No still ships or enters the reuse library without a
  `*.coherence.json` where `audited=true AND passed=true` and `png_sha256` matches the file
  (C1–C7, heterogeneous fan-out, fail-closed). A clip needs its own passing `clip_qc` too;
  a clip never rides a still's PASS for motion defects.
- **INV-24 (no fabricated verdicts):** NO copy / reuse / servicer path may fabricate a
  passing audit/coherence/clip-qc verdict. It copies a real sidecar from the source or marks
  UNVERIFIED. (Closes `clip_library.materialize`, `_build_zech_reuse.py`,
  `assembly_servicer._clips_all_qcd`.)
- Enforcement lives at a chokepoint `assembly_runner` hits **before `load_clips`** (a
  `visual_lock`/extended `run_lock`), same fail-closed shape as `require_lock` — not a
  standalone module the servicers sail past.

## 6. Open honesty notes

- The gate is vision-based; *hardened*, not infallible. Heterogeneous passes + blind-of-spec
  + adversarial localization + a deterministic seatbelt + fail-closed-to-review reduce both
  the confabulation (false-pass) and the over-reject (false-fail) risks, but neither is zero
  — hence the calibration gate (A6) measures the false-reject rate before we trust it.
- Pure-code pose estimation is out of scope EXCEPT the cheap head-count seatbelt.
- B4 is the only real spend; bounded by the attempt cap + fallback-to-exclude, gated behind
  user approval with a realistic worst-case quote (~$110, not ~$55).
- In agent-mode the fan-out's "independence" is heterogeneous PROMPTS on one agent, not
  three independent models. Where a rebuilt still is re-certified, route ≥1 pass off the
  authoring agent (real-API Claude / CLI panel) to break circularity.
