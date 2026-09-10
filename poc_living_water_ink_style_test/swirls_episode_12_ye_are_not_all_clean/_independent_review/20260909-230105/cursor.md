# Independent review — cursor (OK, 81s)

## Findings

### 1. “Validated pattern” overstates what the pilot actually proved

The header claims it follows *“the exact structural pattern validated on the first Flow pilot episode”*. The pilot’s own post-mortem (`swirls_pilot_02_my_lord_and_my_god/FLOW_RUN_SHEET.md`, “What changed in v2”) says v2 fixed **process** (phased refs→stills→clips, label log, SUCCESS lines) after v6 delivery — not content quality. Real v6 defects: wrong Front Cover style/composition, F04 rendered as pencil sketch, Thomas “doubt line” invisible, filename/label mismatch (`_flow_delivery_v6/_REVIEW.html`). Episode 12 is **harder** than that pilot (4 refs, crowd wide shot, spatial ZONE rule, coin-purse ID). Process validation ≠ readiness for this episode’s load-bearing checks.

### 2. Internal contradiction on the episode’s core mechanic (ZONE)

**Section 0, rule 2:** *“the blue-and-gold Swirls-of-Life ink motif… must never appear in the same frame as Judas, at any dose, on any page.”*

**Steps S3/S4 (F02/F03)** explicitly put Judas in the main scene **and** a blue thread at the basin on the **same page**. `_DESIGN_BRIEF.md` resolves this as **spatial zone separation** (“NO blue anywhere near Judas… he sits at a distance”), not literal frame exclusion.

**Section 3** makes it worse: *“any still or clip where Judas is in frame AND the motif dose is above 0 — that never happens by design.”* That is **false** for S3/S4. An agent following Section 0 literally will refuse or mis-execute F02/F03; an agent following Section 3’s parenthetical will distrust the whole sheet.

### 3. Upstream design drift not fully reconciled

The run sheet notes `_DESIGN_BRIEF.md` §3 vs §6 on F04/Jesus (`Global Settings` “A note on S5”), but **`_DESIGN_BRIEF.md` line 12** still says Jesus is absent on *“the two Judas-alone pages (F04, F05)”* — F04 is not Judas-alone in either §6 or Step S5. The sheet *“supersedes both on generation mechanics”* but leaves a live contradiction in the companion brief the operator may still read.

**NOTES.md** (lines 101–105): `episode.py` *“not yet done”* and generation route *“not yet decided”* — yet this sheet commits fully to Flow with no recorded decision or fallback to the locked OpenArt/`swirls_page.py` path.

### 4. Feasibility: agent self-QC on ZONE, coin-purse, and motion is a false safety net

**Section 3:** *“for a clip, watch it end to end AND listen to its audio track”* plus per-step ZONE checks (*“no blue ink anywhere near the man matching REF_JUDAS”*, *“at least an arm's length from the basin”*).

The repo already treats this class of check as unreliable without tooling (`swirls_verify.py` V2 Vision audit, `pipeline/flow_check.py` morph/motion pre-filter). This plan replaces those with Flow-agent eyeballing. Spatial proximity (“arm’s length”, “near Judas”) and subtle line discipline (*“one single confident unbroken line”* on R1) are exactly what the pilot failed on (steady vs tremored line, style bleed) while still “passing” enough to continue.

**Section 0, rule 5:** *“keep the better of the two… write the failure under Flags… and continue. Never stop the run”* — guarantees shipping CRITICAL ZONE failures into paid clip generation (Phase 3) with no stop condition.

### 5. Missing human image gate = guaranteed wasted video spend

**Section 0:** *“without pausing for approval… I am not watching between steps”* and **Phase 2 → Phase 3** runs all 8 clips regardless.

Project cost lever: bad still caught at image gate never gets animated. Here, a failed S3 ZONE check after 3 attempts still proceeds to V3 (`generate_video_with_first_frame` on `STILL_03`). With 4 LONG clips and up to 3 attempts each, worst-case spend exceeds the sheet’s own ceiling (below).

### 6. Retry / cost math is wrong

**Section 0.5, item 3:** *“real range is 20-45 generation attempts”* with CRITICAL steps getting **3 attempts** (Section 3, Global Settings). If many/all 20 steps hit CRITICAL retry budget: **20 × 3 = 60**, not 45. No Flow credit estimate, no comparison to the locked OpenArt billing path documented in `CLAUDE.md`.

**Global Settings:** *“Image model | whatever this Flow project's image model is currently set to”* — no model lock. Pilot v6 style drift (woodcut cover → comic poster; interior → pencil) came from exactly this hand-waving.

### 7. Circular / unenforceable cross-step checks

**Step S1 CRITICAL:** *“rendered in the same woodcut-engraving technique as Step S8's Back Cover”* — S8 does not exist yet when S1 runs. Same failure mode as pilot Front Cover vs Back Cover style mismatch; the check cannot be executed at generation time.

**Step V1:** *“baked title lettering… pixel-for-pixel identical throughout”* contradicts **Section 3**’s own allowance that *“unchanged… does not mean literal pixel equality, which no eye or agent can actually certify.”*

### 8. Ingredient chaining at S3/S4 scale is unproven

**Step S3:** *“REF: REF_JESUS (uploaded), REF_SUPPER_ROOM, REF_JUDAS, REF_BASIN_TOWEL”* — four references. Pilot mostly used 1–2; v6 already struggled with label↔file mapping. **Section 0, rule 4** assumes the agent can re-attach prior in-session gens by label with zero human re-upload. No smoke test for **4-ingredient** interior stills before the full 20-gen run.

**Section 0.5, item 4:** Windows path `F:\slk\PycharmProjects\JesusInTheBible\.claude\skills\swirls-of-life\references\jesus_ref.png` — meaningless inside Flow; relies on manual pre-upload with no verification step that the uploaded file is the correct Jesus ref.

### 9. Palette wording fights the no-gold rule on refs

**Step R1 prompt:** palette includes *“touches of soft gold wash”* while CRITICAL checklist says *“No blue and no gold anywhere on him.”* Same pattern on R2–R4. Models often follow palette lines over negatives; this invites gold on Judas/basin refs that downstream ZONE checks then have to catch (via unreliable agent QC).

### 10. Woodcut hybrid top panels vs ZONE on Judas pages

Interior still prompts (e.g. **S3**) require top panels in *“deep teal shadows, golden-hour glow”* on the **same page** as Judas in the main scene. Step check says blue/gold must not appear *“near”* Judas, not *“on the page.”* Generators routinely bleed panel palette into the main scene — a known failure mode with no deterministic lint (contrast `swirls_verify.py` SW-L* gates on assembled prompts).

### 11. Assembly path is documented but not buildable in-repo

**“After the zip comes back”** references `ASSEMBLY_PLAN.md` timing (including F04→F05 *“0.00s gap”* hard cut) and `check_landing_hold.py` — good.

But this folder has **no `episode.py`**, **no `build_cut.py`**, **no `_assembly_*`**. Pilot explicitly warned `_assembly_v2/build_cut.py` *“does not yet know about the 8-shot filenames”* and needs updating. Episode 12 repeats FINAL REPORT filenames with no step to create/update an assembler. **`ASSEMBLY_PLAN.md`** also notes F03/F06/back cover likely need **3–5s / 1–3s freeze-holds** beyond longest native clip — the run sheet mentions trim/freeze for Front Cover and F05 but not an explicit F03 freeze-hold step in the post-Flow section.

### 12. Session fragility: no resume, context rot at scale

**Section 0:** single conversation, *“You send me exactly two messages”*; split only at paste time (*“split it at any `## Step` or `## PHASE` heading”*). No checkpoint if the session dies at V5. **~1,100 lines / 20–60 generations** in one agent context — label log (**Section 0, rule 4**) is the only continuity mechanism; pilot confirmed Flow filenames don’t preserve labels.

### 13. Reuse: parallel manual orchestration instead of existing Swirls stack

Locked Swirls default: `swirls_episode.py` → `swirls_page.py` / `swirls_cover.py` → `swirls_verify.py` (V0–V3) → animate → `swirls_assemble.py`. This sheet is a fourth parallel source of truth (alongside `_DESIGN_BRIEF.md`, future `episode.py`, and `ASSEMBLY_PLAN.md`) with **no** `swirls_verify`, **no** `flow_check`, **no** idempotent sidecars, **no** OpenArt bridge accounting — despite `NOTES.md` saying the route isn’t decided yet.

### 14. Clip audio vs assembly unspecified

Clip prompts (e.g. **V1**) request ambient audio (*“faint distant night ambience, footsteps”*). Post-Flow assembly section doesn’t say whether clip audio is stripped, ducked, or kept when narration is muxed — a gap for a narration-driven short.

---

VERDICT: REVISE
TOP FIXES:
1. **Fix the ZONE contradiction in Section 0 / Section 3** — replace “never in the same frame as Judas” with the brief’s actual rule (basin-anchored ink, explicit distance, F02–F03 allowed, F04+ zero dose); remove the false *“never happens by design”* parenthetical so the agent isn’t given conflicting geometry.
2. **Add a mandatory human GATE 2 (stills-only) before Phase 3**, plus a 3-step smoke test (R1 → S3 with 4 Ingredients → one ZONE-critical clip) proving label log and re-attach work; do not run all 8 animations unattended until S3 ZONE passes human + `swirls_verify`/eyeball review.
3. **Build assembly before spend** — implement `episode.py` or at minimum an ep12 `build_cut.py` wired to `ASSEMBLY_PLAN.md` (F04→F05 hard cut, F03/F06/back-cover freeze-holds, `check_landing_hold.py`); wire post-download `flow_check.py` on clips; formally decide Flow vs OpenArt in `NOTES.md` with credit ceiling using corrected retry math (up to ~60 attempts).
