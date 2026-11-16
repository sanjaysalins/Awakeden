# Independent review — cursor (OK, 117s)

## Independent adversarial review (plan)

### Feasibility vs real codebase

**“Repeatable pipeline” vs OpenArt bridge** — The title and §2 (“One runner drives everything”) imply something you can run to completion. Step 5 still says a **“live Claude session must service the bridge”**, and `openart_bridge.py` blocks on a human-serviced MCP loop with no silent HF fallback. That is not repeatable the way `cli_pipeline.py` is; it is the old bridge discipline with more gates. Any skill that says “run step 5–6 unattended” would lie.

**SWS-G0 credit accounting** — “The runner adds up credits from bridge responses and stops at the cap” assumes every job response includes accurate `credits_spent`. `AGENT_BRIDGE.md` already says the **servicer** must call `openart_model_cost` or balance-delta and write the response, and that ledger rows are also servicer-written. The plan does not specify fail-closed behavior when `credits_spent` is missing, wrong, or the servicer forgets the ledger row—so G0 can be bypassed or double-counted.

**Step 1 “pipeline” is mostly a ceremony** — “4-5 blind writers (Fable, Sonnet, Codex, Gemini, Grok)” and “Reuse `ArkAIology\...\guardrail_panel_template\`” describe **manual multi-CLI orchestration**, not code the runner executes. On disk, `guardrail_panel_template` is only `format.txt` / `header.txt` / `lenses.json`—no runner, no IDs, no merge logic. Step 1 is underspecified for feasibility: who invokes whom, where artifacts land, and how `LOCKED_WORDS.md` gets written without human glue.

**`units.json` + timing (Step 3)** — `swirls_timing.py` is new input. Ep13 today uses a one-off `_compute_unit_timing.py` with **hardcoded per-unit word counts** walked through `narration.alignment.json`. The plan never defines how `units.json` stays **byte-synced** with the locked narration split (edits in step 1–2), or what FAILs when alignment token count ≠ unit words (ep13 `assert len(words) == 227`).

**Publish path (Step 12)** — “`cli_publish.py` … Swirls is already supported” is only half true: `upload_engine._harvest_swirls_facts` exists, but it takes **`anchor_ref` from `_DESIGN_BRIEF.md`’s first line** when present. Step 0’s template outputs `words\BRIEF.md` and `PAGE_PLAN.md` and **drops `_DESIGN_BRIEF.md`**. Unless `FRONT_COVER.subtitle` always carries a parseable reference, harvest falls back to cover subtitle only—easy publish/copy bug. Step 12 also pulls in `release_check.py`, which swirls episodes have not been using; no schema/checklist mapping is given.

**Animation entry point not fully migrated** — Plan locks **“One animator in v1: Kling 3 Omni”** and trim-only assembly, but `swirls_episode.py` still sets **covers to `veo3_1_lite`** in `_model_tier_map` and `cmd_animate` still **blocks on `SW-F1` freeze budget** before spend. §4.1 does not list disabling SW-F1 / retiering covers under `trim_only` / `short_v2`. You can build trim mode and still hit legacy freeze gates on animate.

**G9 still audit wording** — “through the agent bridge” oversimplifies: `swirls_verify._vision_audit` uses **agent_bridge only when `config.agent_mode()`**, otherwise **direct Anthropic API**. New `texts_seen` compare logic is fine, but cost/mode behavior differs by environment; the plan treats audit as one path.

**SWS-G16 dependencies** — References `check_no_dead_intro`; that lives in per-episode `generate_score_piano.py` copies today. Lifting to `swirls_score.py` is reasonable but **not yet a shared module**—build order item 6 “dry-run” should name the exact import source or you ship a gate that imports a missing symbol.

### Hidden risks / false assumptions / SPOFs

**Front-cover / hook (§1.2)** — The plan admits “no real viewer has tested this.” Baked title + voice from 0.0s + 2–3 s cover is the highest-leverage UX change in the doc, yet there is **no bake-off step** before committing template + skill (contrast `_bakeoff_format_v2` arm B work already on disk).

**§1.4 rule 5 vs “hero always animated”** — Speaker frozen with closed mouth while “the hero scene always has real motion” breaks on **single-figure speaking pages**; §8.3 flags it but Step 3 `PAGE_PLAN` has no required **fallback motion spec** or WARN gate when `figure_count == 1` and `speaker` is the only figure.

**SWS-G12 (§2 Step 6)** — “blue-ink mask area grows <= 15%” needs a **per-still mask definition** that is not in Step 3 outputs (`PAGE_PLAN` lists motif stage, not mask geometry). Thresholds “calibrated at $0” on old clips is good, but **false positives on woodcut hatching** could force expensive clip rerolls; no pilot tolerance policy.

**Clips have no owner gate (Step 6)** — Table says clips are a paid step with “yes to price”; body says **“Owner: no separate gate. They see the clips in the draft film.”** That pushes the largest spend (§6: clips ~80% of OpenArt) past human eyes until after render, contradicting the defect table’s “catch right after” principle and your own image-gate-before-Kling discipline elsewhere.

**Shared 8,000 cr (§0, §6)** — “other sessions also spend from it” plus per-episode caps does not stop **account-level insolvency** mid-episode; runner might hit OpenArt errors without a pre-flight balance check.

**§1.5 character rules** — “**no digits** (except frame numbers and Scripture references on covers)” vs “panel numbers 1 2 3” and `F01`..`F08`—baked-text lint must encode exceptions or G4 will fight the layout.

**Hard cuts on word starts (SWS-G15)** — Requires alignment quality and that each unit’s **first word** is unambiguous in `narration.alignment.json`. No gate for “first word of unit not found” / multi-speaker overlap / re-record drift after step 3.

### Over-engineering before proof

**Gate surface (SWS-G0–G20)** — Twenty named gates, seven new modules (`swirls_state`, `swirls_pages`, `redteam-pack`, `clipqc`, etc.), and **eight owner HTML page kinds** before §4.5’s pilot. §7 honestly lists thin evidence, but §4.5 still builds **1–6 in full** then pilot. A thinner MVP (trim + timing + one still audit path + draft assemble) would prove §1.1 pacing and §1.2 hook before investing in G12 pixel masks and G19 film red-team packs.

**Dual gate stacks** — “The three existing `_validate_swirls_*.py` scripts must still pass” **and** SWS-G1–G20 **and** legacy SW-* on old episodes. §4.1 only gates SWS on `trim_only` for `plan`; it does not document how SW-F1/SW-A* interact with trim episodes on `verify`/`assemble`—risk of contradictory FAIL/WARN forests.

**Step 11 film red-team** — Another full blind panel round after step 1’s panel. Valuable, but expensive in **owner attention and CLI seats**; not justified until one pilot fails a simpler checklist.

### Missing steps / verification gaps

- **`_overrides.json` vs `episode_state.json`** — Today spend safety uses `_overrides.json` on gate FAILs (`swirls_episode.py` animate path). G0 approvals are a parallel system; no migration, precedence, or “override does not bypass cap” rule.
- **Step 4 north-star before Step 3 G7** — Step 3 `plan` lists **SWS-G7 refs: “files exist (after step 4)”** but runs under step 3 **before** step 4. Need explicit split: lint-only (paths declared) vs exist-check (post–north-star).
- **`narration_pipeline.py verify` (SWS-G1)** — Cross-repo subprocess to `PythonProject1`; not spelled as a hard dependency or expected voice/split format for swirls `narration.md`.
- **`job_id` in bridge responses (§4.1 `AGENT_BRIDGE.md`)** — Plan adds `_jobs.jsonl` but not how the runner reconciles partial jobs after bridge timeout (stale request files).
- **30 s score bend (§8.1)** — “each part audible in its first 10 s (`check_no_dead_intro`)” conflicts with a **~13 s single generation** for 30 s films unless G16 is length-aware.
- **Interior density (§7)** — “5-6 s storyboard page may be too dense”—no acceptance test (phone mock / safe-zone) in gates beyond caption 85% WARN.

### Reuse vs duplication

Good: trim in `swirls_assemble.py`, lift score/SFX from ep13, keep `openart_bridge.py`, `build_srt.py`, `narration_gate.py`, `check_landing_hold.py`.

Weak:

- **`swirls_pages.py`** — Large new HTML generator family; ep16 already has ad hoc `_PICK_*.html` patterns—plan does not reuse one builder.
- **SWS gates in `swirls_verify.py`** — Adds G1–G10 beside SW-L/SW-F/SW-A; consider thin wrappers instead of a second registry unless old gates are explicitly retired for `short_v2`.
- **Spend** — `data\spend_ledger.jsonl` already exists with OpenArt rows; G0 + per-step ledger rows may duplicate servicer ledger writes unless deduped by `job_id`.

### Cost / spend

Model arithmetic (35 cr/s, 40 cr stills) matches OpenArt quotes in §0. **Buffer 30% / 25%** is admitted guesswork; pilot cap “~$9” (§9) sits tight against “~$7 with buffer” for 45 s if rerolls look like ep13.

Quoting in Step 3 (“sum of clip seconds x 35 cr”) omits stills in the same view the owner sees before step 5—minor UX gap for “4 paid asks.”

Dropping to `std` correctly rejected for 1080p—but **no plan B** if Kling `pro` returns sub-1900 height intermittently (G11 FAIL) except reroll; no OpenArt ticket/escalation path.

---

VERDICT: REVISE  
TOP FIXES:  
1. Reconcile “repeatable pipeline” with bridge reality: document attended servicer as a hard prerequisite, define G0 fail-closed credit accounting (`credits_spent` required), and add a **minimum pilot slice** (timing + trim + one page still/clip/assemble) before building SWS-G12–G20.  
2. Fix the **trim_only migration gap** in `swirls_episode.py`: retire SW-F1/`veo` cover defaults for `short_v2`, add a **clip owner gate** (or per-clip QC page) before batch spend, and align Step 6 owner flow with the step table.  
3. Close **publish/timing data contracts**: keep a harvest-safe scripture anchor (template `_DESIGN_BRIEF` stub or mandated `FRONT_COVER.subtitle`), specify `units.json` ↔ alignment word-count invariants, and split SWS-G7 into pre–step 4 lint vs post–step 4 file-exists checks.
